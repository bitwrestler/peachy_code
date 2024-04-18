import os
import copy
import logging
import server_pb2_grpc
from server_pb2 import PromptItem, PromptType, DiffRequest, DiffResult
import ServerCommon
from ServerCommon import ServerParams
from IKnowledgeServer import IKnowledgeServer
from llama import Llama

"""
Server that uses direct PyTorch CodeLLama
"""
class CodeLLamaDirectServer(IKnowledgeServer):
    DEFAULT_GEN_LEN = 512
    DEFAULT_THRESHOLD = 0.95

    def __init__(self,settings : ServerParams):
        super().__init__(settings)
        os.environ['LOCAL_WORLD_SIZE'] = str(settings.NUM_NODES)
        os.environ['WORLD_SIZE'] = os.environ['LOCAL_WORLD_SIZE']
        os.environ['LOCAL_RANK'] = str(0)
        os.environ['RANK'] = os.environ['LOCAL_RANK']
        os.environ['MASTER_ADDR'] = '127.0.0.1'
        os.environ['MASTER_PORT'] = '11002'
    
    def Start(self):
        path = self.settings.LLM_DIR
        self._single_generator = Llama.build(
            ckpt_dir=os.path.join(path, self.settings.LLM_RELATIVE_DIR),
            tokenizer_path=os.path.join(path, self.settings.LLM_RELATIVE_DIR, self.settings.TOKENIZER_MODEL_FILE),
            max_seq_len=self.settings.SEQ_LEN,
            max_batch_size=self.settings.MAX_BATCH_SIZE
        )

    def ConvertItem(self, item : PromptItem):
        p = item.Prompt
        if not p.endswith('.'):
            p = p + '.'
        return {"role" : IKnowledgeServer.ConvertRole(item.Type), "content" : p}

    def ConvertPromptsToInstructions(self, request : DiffRequest):
        currentList = []
        inSystem = 0
        for item in request.Request:
            currentList.append(self.ConvertItem(item))
            if item.Type == PromptType.PromptType_USER:
                yield currentList
                currentList = []
                inSystem=0
            elif inSystem > 0:
                raise Exception("System prompt types (if used at all) must alternate System and User. Detected mulitple System types back to back")
            else:
                inSystem+=1

    def _Submit(self, diff_request : DiffRequest, diff_result : DiffResult) -> None:
        if self._single_generator:
            generator = copy.deepcopy(self._single_generator)
            results = generator.chat_completion(
                list(self.ConvertPromptsToInstructions(diff_request)),
                max_gen_len=self.DEFAULT_GEN_LEN,
                temperature=self.Temperature(),
                top_p=self.DEFAULT_THRESHOLD
            )
            generator = None
            diff_result.Result.extend([result['generation']['content'] for result in results])

    def Shutdown(self, request, context):
        self._single_generator = None