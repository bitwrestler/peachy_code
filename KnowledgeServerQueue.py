import threading
import uuid
from collections import deque
from server_pb2 import DiffRequest, DiffResult, ResponseType
import server_pb2_pyi_extensions
from dataclasses import dataclass

@dataclass
class QueueItem:
    Request : DiffRequest
    Result : DiffResult

class KnowledgeServerQueue:
    def __init__(self, queue_size : int):
        self.size = queue_size
        self.lock = threading.Lock()
        self.q = deque()
        self.running = 0

    def shouldQueue(self):
        return self.running >= self.size
    
    def checkStatus(self, id : str):
        f = filter(lambda e: e.Result and e.Result.ResultID == id, self.q)
        try:
            return next(f)
        except StopIteration:
            return None

    def TryQueue(self, request : DiffRequest, response : DiffResult = None):
        with self.lock:
            if request.IsCheckStatus() and :
                
            if self.shouldQueue():
                response = DiffResult(ResultID=str(uuid.uuid4()), ResultType=ResponseType.ResponseType_COMPLETE)

    def RecordCompletion(self, isQueued : bool):
        if isQueued:
            with self.lock:
                self.running = self.running - 1