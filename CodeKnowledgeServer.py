import os
import grpc
import logging
import argparse
from concurrent import futures
import server_pb2_grpc
import server_pb2_pyi_extensions
from ServerCommon import ServerParams, ServerType , LISTEN_IF_ADDR
from CodeLLamaDirectServer import CodeLLamaDirectServer
from CodeLLamaOLLamaServer import CodeLLamaOLLamaServer

"""
Server Factory for starting code server
"""
class CodeKnowledgeServerFactory:
    
    @staticmethod
    def _createServer(settings : ServerParams):
        if settings.server_type == ServerType.CODE_LLAMA_DIRECT:
            return CodeLLamaDirectServer(settings)
        elif settings.server_type == ServerType.CODE_LLAMA_OLLAMA:
            return CodeLLamaOLLamaServer(settings)
        else:
            raise Exception(f"Unknown server type {settings.server_type}")

    def CreateServer(self, settings : ServerParams):
        self.csServer =  CodeKnowledgeServerFactory._createServer(settings)
        self.csServer.Start()
        self.rpcServer = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
        server_pb2_grpc.add_PeachyServerServicer_to_server(self.csServer,self.rpcServer)
        self.rpcServer.add_insecure_port(LISTEN_IF_ADDR)
        logging.info(f"gRPC server started on {LISTEN_IF_ADDR}...")
        self.rpcServer.start()
        logging.info(f"gRPC server listening...")
        self.rpcServer.wait_for_termination()

if __name__ == "__main__":
    parser = argparse.ArgumentParser("CodeKnowledgeServer")
    parser.add_argument("--ollama", help="Use OLLama backend", action='store_true')
    args = parser.parse_args()
    st = ServerType.CODE_LLAMA_DIRECT
    if args.ollama:
        st = ServerType.CODE_LLAMA_OLLAMA
    logging.basicConfig(format='[%(asctime)s] %(levelname)s:%(message)s', level=logging.INFO)
    server_params = ServerParams(LLM_DIR=os.path.dirname(os.path.realpath(__file__)), server_type=st)
    logging.info(f"ServerParams -> {server_params}")
    factory = CodeKnowledgeServerFactory()
    factory.CreateServer(server_params)