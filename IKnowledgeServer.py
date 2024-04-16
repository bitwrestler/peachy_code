import subprocess
import logging
import server_pb2_grpc
import server_pb2
from server_pb2 import PromptType, DiffRequest

"""
Abstract server class
"""
class IKnowledgeServer(server_pb2_grpc.PeachyServerServicer):
    DEFAULT_TEMPERATURE = 0.2

    def Start(self):
        raise NotImplementedError('Method not implemented!')
    
    def GPUStats(self, request : server_pb2.DiffRequest, context):
        logging.info("Received GPUStats request")
        statsargs = [args.Prompt for args in request.Request]
        statsargs.insert(0,'nvidia-smi')
        p = subprocess.Popen(statsargs, stdout=subprocess.PIPE)
        allines = [l for l in io.TextIOWrapper(p.stdout, encoding='utf-8')]
        return server_pb2.DiffResult(Result=allines)
    
    def Temperature(self):
        return IKnowledgeServer.DEFAULT_TEMPERATURE

    @staticmethod
    def ConvertRole(role : PromptType) -> str:
        if role == PromptType.PromptType_SYSTEM:
            return "system"
        else:
            return "user"
    
    def Submit(self, request : DiffRequest, context):
        logging.info(f"Recieved Prompt: {str(request)}")
        return None