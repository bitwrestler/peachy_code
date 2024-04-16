import IOLLamaServer

"""
Impl of COdeLLamaServer using OLLama
"""
class CodeLLamaOLLamaServer(IOLLamaServer.IOLLamaServer):
    def ModelName(self) -> str:
        return 'codellama:7b-instruct'