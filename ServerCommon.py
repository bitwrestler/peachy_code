from dataclasses import dataclass
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
    
@dataclass
class ServerParams:
    LLM_DIR : str = None
    server_type : ServerType = DEFAULT_SERVER_TYPE
    server_arg : str = None
    LLM_RELATIVE_DIR : str = 'llm_model'
    TOKENIZER_MODEL_FILE : str = 'tokenizer.model'
    SEQ_LEN : int = DEFAULT_MAX_LEN
    MAX_BATCH_SIZE : int = DEFAULT_BATCH_SIZE
    NUM_NODES : int = DEFAULT_NODES_COUNT
    TEMPERATURE : float = DEFAULT_TEMPERATURE