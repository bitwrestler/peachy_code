from collections import namedtuple
from enum import Enum

LISTEN_IF_PORT="50301"
LISTEN_IF_ADDR=f"0.0.0.0:{LISTEN_IF_PORT}"
DEFAULT_MAX_LEN=512
DEFAULT_BATCH_SIZE=4
DEFAULT_NODES_COUNT=1
DEFAULT_TEMPERATURE=.2 

class ServerType(Enum):
    CODE_LLAMA_DIRECT = 1
    CODE_LLAMA_OLLAMA = 2

DEFAULT_SERVER_TYPE = ServerType.CODE_LLAMA_DIRECT
    
ServerParams = namedtuple('ServerParams',['LLM_DIR','server_type','server_arg','LLM_RELATIVE_DIR','TOKENIZER_MODEL_FILE','SEQ_LEN','MAX_BATCH_SIZE','NUM_NODES','TEMPERATURE'], 
                          defaults=[None,DEFAULT_SERVER_TYPE,None,'llm_model','tokenizer.model',DEFAULT_MAX_LEN,DEFAULT_BATCH_SIZE,DEFAULT_NODES_COUNT,DEFAULT_TEMPERATURE])
