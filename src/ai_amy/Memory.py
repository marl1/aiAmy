import threading
from .ConfigController import *
from .model.ChatCompletion import Message
from typing import List


class Memory:
    """ Singleton class that hold the list of previous messages."""
    # Shared class variable
    _messages: List[Message] = []
    # Class-level lock
    _lock = threading.Lock()

    @classmethod
    def saveMessage(cls, message: Message):
        with cls._lock:
            cls._messages.append(message)

    @classmethod
    def getMessages(cls) -> List[Message]:
        with cls._lock:
            return list(cls._messages) # Return a copy
