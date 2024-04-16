from collections import namedtuple

LISTEN_IF_PORT="50301"
LISTEN_IF_ADDR=f"0.0.0.0:{LISTEN_IF_PORT}"
DEFAULT_MAX_LEN=512
DEFAULT_BATCH_SIZE=4
DEFAULT_NODES_COUNT=1

"""
Server Params
"""
class ServerParams:
    def __init__(self, llm_dir):
        self.LLM_DIR = llm_dir
    @property
    def LLM_DIR(self):
        return self.llm_dir
    @LLM_DIR.setter
    def LLM_DIR(self,val):
        self.llm_dir = val
    @property
    def LLM_RELATIVE_DIR(self):
        return 'llm_model'
    @property
    def TOKENIZER_MODEL_FILE(self):
        return 'tokenizer.model'
    @property
    def SEQ_LEN(self):
        return DEFAULT_MAX_LEN
    @property
    def MAX_BATCH_SIZE(self):
        return DEFAULT_BATCH_SIZE
    @property
    def NUM_NODES(self):
        return DEFAULT_NODES_COUNT

#namedtuple('ServerParams',['LLM_DIR','LLM_RELATIVE_DIR','TOKENIZER_MODEL_FILE','SEQ_LEN','MAX_BATCH_SIZE','NUM_NODES'], 
#                          defaults=[None,'llm_model','tokenizer.model',DEFAULT_MAX_LEN,DEFAULT_BATCH_SIZE,DEFAULT_NODES_COUNT])