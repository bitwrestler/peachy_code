# Peachy Code - The Code Review assistant

**WORK IN PROGRESS - DOES NOT DO A WHOLE LOT YET**

This is a research project to explore the possiblity of using a local code-specific LLM to assist with code reviews.
Specifically, I am trying to determine the feasiblity that an LLM can explain the high level differences present in a unified-diff formmatted code review in order to help the reviewer:
* Get a high-level summary of the differences
* Get a better clue on which file to start with and a preferred order of files while performing the review
* Eventually, can the model make helpful suggestions regarding code style, duplicative code detection, library usage?  
* Can prompt engineering without fine tuning or training the model meet these goals?

Peachy Code Server is a client-server architecture that supports direct loading of a codellama via PyTorch or can act as a proxy for Ollama.
The codellama model is not included and must be obtained separately. The same is true of Ollama.

Note: This client-server architecture is independent of the goals above. With a little adaptation, it could be used with any model and any prompts.


## Server
### Run in standard direct mode
Usage: python PeachyCodeServer.py
### Run in ollama mode
Usage: python PeachyCodeServer.py --ollama [--arg optional host/port of ollama server]

## Client
* Usage: python PeachyCodeClient.py [--ip optional host/port of PeachyCodeServer] | stdin
* Usage: python PeachyCodeClient.py --prompt [string prompt] [--ip optional host/port of PeachyCodeServer]
* Usage: python PeachyCodeClient.py --stats (NVIDIA GPU stats)

## Prompt File Format
* One line per prompt
* Line continuation with '\'
* Comments with lines starting with '#'
* System prompts start with '~'; all others are User prompts

---

Powered by Code LLama
https://ai.meta.com/blog/code-llama-large-language-model-coding/
with support for Ollama
https://ollama.com/
