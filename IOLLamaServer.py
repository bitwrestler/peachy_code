import requests
import json
import IKnowledgeServer
from server_pb2 import DiffRequest, PromptType

class IOLLamaServer(IKnowledgeServer.IKnowledgeServer):
    DEFUALT_OLLAMA_HOST = '127.0.0.1'
    DEFAULT_OLLAMA_PORT = 11434
    DEFAULT_OLLAMA_CONTEXT = 65536
    
    def __init__(self, ollama_host : str = DEFUALT_OLLAMA_HOST, ollama_port : int = DEFAULT_OLLAMA_PORT):
        self.ollama_url = f'http://{ollama_host}:{ollama_port}/api/'

    def getGenerateUrl(self):
        return self.ollama_url + "generate"

    def Start(self):
        requests.post( url=self.getGenerateUrl(), data  )

    def Shutdown(self, request, context):
        pass
    
    def ModelName(self):
        raise NotImplementedError('ModelName required')

    def initRequest(self):
        return {'model' : self.ModelName(), 'stream' : 'false'}

    def makeRequest(self, request : DiffRequest) -> dict:
        model = self.ModelName()
        system = '.'.join([rp.Prompt for rp in request.Request if rp.Type == PromptType.PromptType_SYSTEM])
        prompt = "\n".join([rp.Prompt for rp in request.Request if rp.Type == PromptType.PromptType_USER])
        data = self.initRequest()
        data['prompt'] = prompt
        data['options'] = {'temperature' : self.Temperature, 'num_ctx' : IOLLamaServer.DEFAULT_OLLAMA_CONTEXT}
        if system:
            data['system'] = system
        return data

    def Submit(self, request : DiffRequest, context):
        data = json.dumps(self.makeRequest(request))
        requests.post()