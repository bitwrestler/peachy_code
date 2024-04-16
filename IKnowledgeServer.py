import subprocess
import logging
import server_pb2_grpc
import server_pb2
from server_pb2 import PromptType

"""
Abstract server class
"""
class IKnowledgeServer(server_pb2_grpc.PeachyServerServicer):
    def Start(self):
        raise NotImplementedError('Method not implemented!')
    
    def GPUStats(self, request : server_pb2.DiffRequest, context):
        logging.info("Received GPUStats request")
        statsargs = [args.Prompt for args in request.Request]
        statsargs.insert(0,'nvidia-smi')
        p = subprocess.Popen(statsargs, stdout=subprocess.PIPE)
        allines = [l for l in io.TextIOWrapper(p.stdout, encoding='utf-8')]
        return server_pb2.DiffResult(Result=allines)
    
    @staticmethod
    def ConvertRole(role : PromptType) -> str:
        if role == PromptType.PromptType_SYSTEM:
            return "system"
        else:
            return "user"