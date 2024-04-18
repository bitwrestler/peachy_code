import io
import subprocess
import logging
import uuid
import server_pb2_grpc
import server_pb2
from server_pb2 import PromptType, ResponseType ,DiffRequest, DiffResult, Empty
from ServerCommon import ServerParams

"""
Abstract server class
"""
class IKnowledgeServer(server_pb2_grpc.PeachyServerServicer):

    def __init__(self,settings : ServerParams):
        self.settings = settings

    def Start(self):
        raise NotImplementedError('Method not implemented!')
    
    def GPUStats(self, request : server_pb2.DiffRequest, context):
        logging.info("Received GPUStats request")
        statsargs = [args.Prompt for args in request.Request]
        statsargs.insert(0,'nvidia-smi')
        p = subprocess.Popen(statsargs, stdout=subprocess.PIPE)
        allines = [l for l in io.TextIOWrapper(p.stdout, encoding='utf-8')]
        return server_pb2.DiffResult(Result=allines)
    
    def Temperature(self) -> float:
        return self.settings.TEMPERATURE

    @staticmethod
    def ConvertRole(role : PromptType) -> str:
        if role == PromptType.PromptType_SYSTEM:
            return "system"
        else:
            return "user"
    
    def Submit(self, request : DiffRequest, context) -> DiffResult:
        logging.info(f"Recieved Prompt: {str(request)}")
        return DiffResult(ResultID=uuid.uuid4(), ResultType=ResponseType.ResponseType_COMPLETE)
    
    def ChangeSettings(self, request : server_pb2.Settings, context):
        logging.info(f"Caught change in settings -> {request}")
        self.settings.TEMPERATURE = request.Temperature
        return Empty()