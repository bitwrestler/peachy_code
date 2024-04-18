import threading
import uuid
import logging
from server_pb2 import DiffRequest, DiffResult, ResponseType
import server_pb2_pyi_extensions

class KnowledgeServerQueue:
    def __init__(self, queue_size : int):
        self.size = queue_size
        self.lock = threading.Lock()
        self.running_count = 0
        self.q = {}

    def canRun(self):
        return self.running_count < self.size
    
    def isQueued(self, id : str) -> bool:
        return id in self.q
    
    def _removeQueued(self, id :str):
        self.q.pop(id, None)

    def RemoveQueued(self, id : str):
        with self.lock:
            self._removeQueued(id)
            self.running_count = self.running_count - 1

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
                logging.info("QUEUE: IsStatusCheck")
                if self.isQueued(request.ResultID):
                    logging.info("QUEUE: isQueued on IsStatusCheck")
                    if self.canRun():
                        logging.info("QUEUE: canRun on isQueued on IsStatusCheck")
                        self.running_count = self.running_count + 1
                        return (True, KnowledgeServerQueue.initResult(id=request.ResultID))
                    else:
                        logging.info("QUEUE: not canRun on isQueued on IsStatusCheck")
                        e = self.q[request.ResultID]
                        return (False, KnowledgeServerQueue.initResult(id=request.ResultID, t = ResponseType.ResponseType_QUEUED))
                else:
                    logging.info("QUEUE: not id queued on IsStatusCheck")
                    #this should not impact running_count and COULD be an exception
                    return (True, KnowledgeServerQueue.initResult(id=request.ResultID))
            else:
                logging.info("QUEUE: not IsStatusCheck")
                if self.canRun():
                    logging.info("QUEUE: canRun")
                    tmpres = self.queueIt(request)
                    self.running_count = self.running_count + 1
                    return(True, KnowledgeServerQueue.initResult(id=tmpres.ResultID))
                else:
                    logging.info("QUEUE: not canRun -> queued")
                    return (False,self.queueIt(request))