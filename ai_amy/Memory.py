import base64
from llama_cpp import Llama
from llama_cpp.llama_chat_format import Llava15ChatHandler
from ConfigController import *
from model.ChatCompletion import Message
from typing import List


class Memory:
    messages:List[Message] = []
    
    def __init__(self):
        pass

    def saveMessage(self, message:Message):
        self.messages.append(message)

    def getMessages(self) -> List[Message]:
        return self.messages
