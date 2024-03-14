import os
import grpc
from concurrent import futures
import server_pb2_grpc
from server_pb2 import DiffResult
from llama import Llama


class CodeKnowledgeServer(server_pb2_grpc.PeachyServerServicer):
    DEFAULT_TEMPERATURE = 0.2
    DEFAULT_GEN_LEN = 512
    DEFAULT_THRESHOLD = 0.95

    def __init__(self):
        self.generator = Llama.build(
            ckpt_dir=os.path.join(os.path.realpath(), 'llm_model'),
            tokenizer_path=os.path.join(os.path.realpath(), 'llm_model', 'tokenizer.model'),
            max_seq_len=512,
            max_batch_size=4
        )
        self.server = grpc.server(futures.ProcessPoolExecutor(max_workers=1))
    
    def Submit(self, request, context):
        results = self.generator.chat_completion(
            [request.Request],
            max_gen_len=self.DEFAULT_GEN_LEN,
            temperature=self.DEFAULT_TEMPERATURE,
            top_p=self.DEFAULT_THRESHOLD
        )
        return DiffResult(Result=[result['generation']['content'] for result in results])


