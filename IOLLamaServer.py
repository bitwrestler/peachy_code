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
    DEFUALT_OLLAMA_HOST = '127.0.0.1:11434'
    DEFAULT_OLLAMA_CONTEXT = 65536
    CONST_VALID_DONE='done'

    def __init__(self, settings : ServerParams):
        super().__init__(settings)
        ollama_host = settings.server_arg or IOLLamaServer.DEFUALT_OLLAMA_HOST
        self.ollama_url = f'http://{ollama_host}/api/'

    @staticmethod
    def toJSON(data : dict) -> str:
        return json.dumps(data)
    
    @staticmethod
    def fromJSON(data : str):
        return json.loads(data)

    def getGenerateUrl(self):
        return self.ollama_url + "generate"

    @staticmethod
    def assertResponse(res):
        resDict = IOLLamaServer.fromJSON(res.text)
        if (not IOLLamaServer.CONST_VALID_DONE in resDict) or (not resDict[IOLLamaServer.CONST_VALID_DONE]):
            raise Exception(f"Ollama response invalid -> '{res.text}'")     
        return resDict

    def Start(self):
        logging.info("Starting OLLama CodeKnowledge Proxy...")
        IOLLamaServer.assertResponse(requests.post( url=self.getGenerateUrl(), data = IOLLamaServer.toJSON(self.initRequest()) ))
    
    def ModelName(self) -> str:
        raise NotImplementedError('ModelName required')

    def initRequest(self):
        d = {'model' : self.ModelName() }
        return d

    def _makeRequest(self, request : DiffRequest) -> dict:
        system = '.'.join([rp.Prompt for rp in request.Request if rp.Type == PromptType.PromptType_SYSTEM])
        prompt = "\n".join([rp.Prompt for rp in request.Request if rp.Type == PromptType.PromptType_USER])
        data = self.initRequest()
        data['prompt'] = prompt
        data['stream'] = False
        data['options'] = {'temperature' : self.Temperature(), 'num_ctx' : IOLLamaServer.DEFAULT_OLLAMA_CONTEXT}
        if system:
            data['system'] = system
        return data
    
    def makeRequest(self, request : DiffRequest) -> str:
        s = self._makeRequest(request)
        return IOLLamaServer.toJSON(s)

    def _Submit(self, diff_request : DiffRequest, diff_result : DiffResult):
        res = IOLLamaServer.assertResponse(requests.post(url=self.getGenerateUrl(), data=self.makeRequest(diff_request)))
        diff_result.Result.extend([res['response']])
