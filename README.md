# Peachy Code - The Code Review assistant
This is a research project to explore the possiblity of using a local code-specific LLM to assist with code reviews. 

It is a client-server architecture that supports direct loading of a codellama via PyTorch or can act as a proxy for Ollama.
The codellama model is not included and must be obtained separately. The same is true of Ollama.

# Server
## Run in standard direct mode
Usage: python PeachyServer.py

## Run in ollama mode
Usage: python PeachyServer.py --ollama [--arg optional host/port of ollama server]


# Client
* Usage: python PeachyCodeClient.py [--ip optional host/port of PeachyCodeServer] | stdin
* Usage: python PeachyCodeClient.py --prompt [--ip optional host/port of PeachyCodeServer]
* Usage: python PeachyCodeClient.py --stats (NVIDIA GPU stats)

---


Powered by Code LLama
https://ai.meta.com/blog/code-llama-large-language-model-coding/
with support for Ollama
https://ollama.com/