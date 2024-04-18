import io
import subprocess
import logging
import server_pb2_grpc
import server_pb2
from KnowledgeServerQueue import KnowledgeServerQueue
from server_pb2 import PromptType,DiffRequest, DiffResult, Empty
from ServerCommon import ServerParams
import server_pb2_pyi_extensions

"""
Abstract server class
"""
class IKnowledgeServer(server_pb2_grpc.PeachyServerServicer):

    def __init__(self,settings : ServerParams):
        self.settings = settings
        self.q = KnowledgeServerQueue(queue_size=settings.NUM_NODES)

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
    
    def _Submit(self, request : DiffRequest, result : DiffResult) -> None:
        raise NotImplementedError("_Submit is an abstract method")

    def Submit(self, request : DiffRequest, context) -> DiffResult:
        logging.info(f"Recieved Prompt (IsStatusCheck->{request.IsStatusCheck()}): {str(request)}")
        qstruct = self.q.TryQueue(request)
        res = qstruct[1]
        if qstruct[0]: #if can run immediately, run it now
            #TODO this isn't working on queued client, returns no response
            try:
                self._Submit(request, res)
            finally:
                self.q.RemoveQueued(res.ResultID)
        logging.info(f"Result -> {res}")
        return res

    def ChangeSettings(self, request : server_pb2.Settings, context):
        logging.info(f"Caught change in settings -> {request}")
        self.settings.TEMPERATURE = request.Temperature
        return Empty()