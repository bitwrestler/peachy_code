import os
import grpc
import logging
from concurrent import futures
import server_pb2_grpc
import server_pb2_pyi_extensions
from ServerCommon import ServerParams, LISTEN_IF_ADDR
from CodeLLamaDirectServer import CodeLLamaDirectServer

"""
Server Factory for starting code server
"""
class CodeKnowledgeServerFactory:
    def CreateServer(self, settings : ServerParams):
        self.csServer = CodeLLamaDirectServer(settings)
        self.csServer.Start()
        self.rpcServer = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
        server_pb2_grpc.add_PeachyServerServicer_to_server(self.csServer,self.rpcServer)
        self.rpcServer.add_insecure_port(LISTEN_IF_ADDR)
        logging.info(f"gRPC server started on {LISTEN_IF_ADDR}...")
        self.rpcServer.start()
        logging.info(f"gRPC server listening...")
        self.rpcServer.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig(format='[%(asctime)s] %(levelname)s:%(message)s', level=logging.INFO)
    server_params = ServerParams(os.path.dirname(os.path.realpath(__file__)))
    logging.info(f"ServerParams -> {server_params}")
    factory = CodeKnowledgeServerFactory()
    factory.CreateServer(server_params)