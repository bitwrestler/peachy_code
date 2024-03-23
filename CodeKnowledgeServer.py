import os
import grpc
from concurrent import futures
import server_pb2_grpc
from server_pb2 import DiffResult
from ServerCommon import LISTEN_IF_PORT,DEFAULT_MAX_LEN,DEFAULT_BATCH_SIZE,DEFAULT_NODES_COUNT
from llama import Llama
from collections import namedtuple

ServerParams = namedtuple('ServerParams',['LLM_DIR','LLM_RELATIVE_DIR','TOKENIZER_MODEL_FILE','SEQ_LEN','MAX_BATCH_SIZE','NUM_NODES'], 
                          defaults=[None,'llm_model','tokenizer.model',DEFAULT_MAX_LEN,DEFAULT_BATCH_SIZE,DEFAULT_NODES_COUNT])

class CodeKnowledgeServer(server_pb2_grpc.PeachyServerServicer):
    DEFAULT_TEMPERATURE = 0.2
    DEFAULT_GEN_LEN = 512
    DEFAULT_THRESHOLD = 0.95

    def __init__(self,settings : ServerParams):
        self.settings = settings
        os.environ['LOCAL_WORLD_SIZE'] = str(settings.NUM_NODES)
        os.environ['WORLD_SIZE'] = os.environ['LOCAL_WORLD_SIZE']
        os.environ['LOCAL_RANK'] = str(0)
        os.environ['RANK'] = os.environ['LOCAL_RANK']
        os.environ['MASTER_ADDR'] = '127.0.0.1'
        os.environ['MASTER_PORT'] = '11002'
        self.server = grpc.server(futures.ProcessPoolExecutor(max_workers=1))
        self.server.add_insecure_port(LISTEN_IF_PORT)
    
    def Start(self):
        path = self.settings.LLM_DIR
        self.generator = Llama.build(
            ckpt_dir=os.path.join(path, self.settings.LLM_RELATIVE_DIR),
            tokenizer_path=os.path.join(path, self.settings.LLM_RELATIVE_DIR, self.settings.TOKENIZER_MODEL_FILE),
            max_seq_len=self.settings.SEQ_LEN,
            max_batch_size=self.settings.MAX_BATCH_SIZE
        )
        self.server.start()
        self.server.wait_for_termination()

    def Submit(self, request, context):
        if self.generator:
            results = self.generator.chat_completion(
                [request.Request],
                max_gen_len=self.DEFAULT_GEN_LEN,
                temperature=self.DEFAULT_TEMPERATURE,
                top_p=self.DEFAULT_THRESHOLD
            )
            return DiffResult(Result=[result['generation']['content'] for result in results])
        else:
            return DiffResult(Result=[])

    def Shutdown(self, request, context):
        self.generator = None
        self.server.stop()

if __name__ == "__main__":
    server_params = ServerParams(os.path.dirname(os.path.realpath(__file__)))
    server = CodeKnowledgeServer(server_params)
    server.Start()