import threading
import uuid
from server_pb2 import DiffRequest, DiffResult, ResponseType
import server_pb2_pyi_extensions
from dataclasses import dataclass

#@dataclass
#class QueueItem:
#    Request : DiffRequest
#    Result : DiffResult

class KnowledgeServerQueue:
    def __init__(self, queue_size : int):
        self.size = queue_size
        self.lock = threading.Lock()
        self.q = {}

    def canRun(self):
        return len(self.q) < self.size
    
    def isQueued(self, id : str) -> bool:
        return id in self.q
    def removeQueued(self, id :str):
        del self.q[id]

    @staticmethod
    def _newID() -> str:
        return str(uuid.uuid4())

    @staticmethod
    def initResult(id : str = None, t : ResponseType = ResponseType.ResponseType_COMPLETE):
        id = id or KnowledgeServerQueue._newID()
        return DiffResult(ResultID=id, ResultType=t)
    
    def queueIt(self, request : DiffRequest) -> DiffResult:
        id = request.ResultID or KnowledgeServerQueue._newID()
        request.ResultID = id
        self.q[id] = request
        return KnowledgeServerQueue.initResult(id=id, t=ResponseType.ResponseType_QUEUED)
    
    def TryQueue(self, request : DiffRequest):
        with self.lock:
            if request.IsStatusCheck():
                if self.isQueued(request.ResultID):
                    if self.canRun():
                        self.removeQueued(request.ResultID)
                        return (False, KnowledgeServerQueue.initResult(id=request.ResultID))
                    else:
                        e = self.q[request.ResultID]
                        return (True, KnowledgeServerQueue.initResult(id=request.ResultID, t = ResponseType.ResponseType_QUEUED))
                else:
                    return (False, KnowledgeServerQueue.initResult(id=request.ResultID))
            else:
                if self.canRun():
                    return(False, KnowledgeServerQueue.initResult())
                else:
                    return (True,self.queueIt(request))