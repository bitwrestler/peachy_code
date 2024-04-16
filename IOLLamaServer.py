import requests
import json
import logging
import IKnowledgeServer
from server_pb2 import DiffRequest, DiffResult, PromptType
from ServerCommon import ServerParams

"""
Abstract class for an OLLama server proxy
"""
class IOLLamaServer(IKnowledgeServer.IKnowledgeServer):
    DEFUALT_OLLAMA_HOST = '127.0.0.1'
    DEFAULT_OLLAMA_PORT = 11434
    DEFAULT_OLLAMA_CONTEXT = 65536
    
    def __init__(self, settings : ServerParams,  ollama_host : str = DEFUALT_OLLAMA_HOST, ollama_port : int = DEFAULT_OLLAMA_PORT):
        self.ollama_url = f'http://{ollama_host}:{ollama_port}/api/'

    @staticmethod
    def toJSON(data) -> str:
        return json.dumps(data)
    
    @staticmethod
    def fromJSON(data : str):
        return json.loads(data)

    def getGenerateUrl(self):
        return self.ollama_url + "generate"

    @staticmethod
    def assertResponse(res):
        resDict = IOLLamaServer.fromJSON(res.text)
        if not resDict['done']:
            raise Exception("Starting model failed")        
        return resDict

    def Start(self):
        logging.info("Starting OLLama CodeKnowledge Proxy...")
        IOLLamaServer.assertResponse(requests.post( url=self.getGenerateUrl(), data = IOLLamaServer.toJSON(self.initRequest()) ))

    def Shutdown(self, request, context):
        pass
    
    def ModelName(self):
        raise NotImplementedError('ModelName required')

    def initRequest(self):
        return {'model' : self.ModelName() }

    def makeRequest(self, request : DiffRequest) -> dict:
        model = self.ModelName()
        system = '.'.join([rp.Prompt for rp in request.Request if rp.Type == PromptType.PromptType_SYSTEM])
        prompt = "\n".join([rp.Prompt for rp in request.Request if rp.Type == PromptType.PromptType_USER])
        data = self.initRequest()
        data['prompt'] = prompt
        data['stream'] = 'false'
        data['options'] = {'temperature' : self.Temperature, 'num_ctx' : IOLLamaServer.DEFAULT_OLLAMA_CONTEXT}
        if system:
            data['system'] = system
        return data

    def Submit(self, request : DiffRequest, context):
        super().Submit(request, context)
        data = IOLLamaServer.toJSON(self.makeRequest(request))
        res = IOLLamaServer.assertResponse(requests.post(url=self.getGenerateUrl(), data=data))
        logging.info(f"Result -> {res}")
        return DiffResult(Result=[res['response']])