import io
import subprocess
import logging
import server_pb2_grpc
import server_pb2
import abc
from KnowledgeServerQueue import KnowledgeServerQueue
from server_pb2 import PromptType,DiffRequest, DiffResult, Empty
from ServerCommon import ServerParams
import server_pb2_pyi_extensions

"""
Abstract server class
"""
class IKnowledgeServer(server_pb2_grpc.PeachyServerServicer, metaclass=abc.ABCMeta):

    def __init__(self,settings : ServerParams):
        self.settings = settings
        self.q = KnowledgeServerQueue(queue_size=settings.NUM_NODES)

    @abc.abstractmethod
    def Start(self):
        pass
    
    def GPUStats(self, request : server_pb2.DiffRequest, context):
        logging.info("Received GPUStats request")
        statsargs = [args.Prompt for args in request.Request]
        statsargs.insert(0,'nvidia-smi')
        p = subprocess.Popen(statsargs, stdout=subprocess.PIPE)
        allines = [l for l in io.TextIOWrapper(p.stdout, encoding='utf-8')]
        return server_pb2.DiffResult(Result=allines)
    
    def Temperature(self) -> float:
        return self.settings.TEMPERATURE
    
    @abc.abstractmethod
    def _Submit(self, request : DiffRequest, result : DiffResult) -> None:
        pass

    def Submit(self, request : DiffRequest, context) -> DiffResult:
        logging.info(f"Recieved Prompt (IsStatusCheck->{request.IsStatusCheck()}): {str(request)}")
        qstruct = self.q.TryQueue(request)
        res = qstruct[1]
        if qstruct[0]: #if can run immediately, run it now
            try:
                self._Submit(qstruct[0], res)
            finally:
                self.q.RemoveQueued(res.ResultID)
        logging.info(f"Result -> {res}")
        return res

    def Shutdown(self, request, context):
        pass 

    def ChangeSettings(self, request : server_pb2.Settings, context):
        logging.info(f"Caught change in settings -> {request}")
        self.settings.TEMPERATURE = request.Temperature
        return Empty()