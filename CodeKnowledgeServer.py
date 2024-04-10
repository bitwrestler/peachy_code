import os
import grpc
import logging
import copy
from concurrent import futures
import server_pb2_grpc
from server_pb2 import DiffResult, DiffRequest, PromptItem, PromptType
import server_pb2_pyi_extensions
from ServerCommon import LISTEN_IF_ADDR,DEFAULT_MAX_LEN,DEFAULT_BATCH_SIZE,DEFAULT_NODES_COUNT
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
    
    def Start(self):
        path = self.settings.LLM_DIR
        self._single_generator = Llama.build(
            ckpt_dir=os.path.join(path, self.settings.LLM_RELATIVE_DIR),
            tokenizer_path=os.path.join(path, self.settings.LLM_RELATIVE_DIR, self.settings.TOKENIZER_MODEL_FILE),
            max_seq_len=self.settings.SEQ_LEN,
            max_batch_size=self.settings.MAX_BATCH_SIZE
        )

    @staticmethod
    def ConvertRole(role : PromptType) -> str:
        if role == PromptType.PromptType_SYSTEM:
            return "system"
        else:
            return "user"

    def ConvertItem(self, item : PromptItem):
        p = item.Prompt
        if not p.endswith('.'):
            p = p + '.'
        return {"role" : CodeKnowledgeServer.ConvertRole(item.Type), "content" : p}

    def ConvertPromptsToInstructions(self, request : DiffRequest):
        currentList = []
        inSystem = 0
        for item in request.Request:
            currentList.append(self.ConvertItem(item))
            if item.Type == PromptType.PromptType_USER:
                yield currentList
                currentList = []
                inSystem=0
            elif inSystem > 0:
                raise Exception("System prompt types (if used at all) must alternate System and User. Detected mulitple System types back to back")
            else:
                inSystem+=1

    def Submit(self, request : DiffRequest, context):
        logging.info(f"Recieved Prompt: {str(request)}")
        if self._single_generator:
            generator = copy.deepcopy(self._single_generator)
            results = generator.chat_completion(
                list(self.ConvertPromptsToInstructions(request)),
                max_gen_len=self.DEFAULT_GEN_LEN,
                temperature=self.DEFAULT_TEMPERATURE,
                top_p=self.DEFAULT_THRESHOLD
            )
            generator = None
            logging.info(f"Result -> {results}")
            return DiffResult(Result=[result['generation']['content'] for result in results])
        else:
            return DiffResult(Result=[])

    def Shutdown(self, request, context):
        self._single_generator = None

class CodeKnowledgeServerFactory:
    def CreateServer(self, settings : ServerParams):
        self.csServer = CodeKnowledgeServer(settings)
        self.csServer.Start()
        self.rpcServer = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        server_pb2_grpc.add_PeachyServerServicer_to_server(self.csServer,self.rpcServer)
        self.rpcServer.add_insecure_port(LISTEN_IF_ADDR)
        logging.info(f"gRPC server started on {LISTEN_IF_ADDR}...")
        self.rpcServer.start()
        logging.info(f"gRPC server listening...")
        self.rpcServer.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig(format='[%(asctime)s] %(levelname)s:%(message)s', level=logging.INFO)
    server_params = ServerParams(os.path.dirname(os.path.realpath(__file__)))
    factory = CodeKnowledgeServerFactory()
    factory.CreateServer(server_params)