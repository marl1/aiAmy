from llama_cpp import Llama
from sklearn import get_config
from ConfigController import *
from Memory import Memory
from model.ChatCompletion import Message
from typing import List
import json
import AmyUtils



class TextInference:
    def __init__(self):
        self.llm = Llama(
        model_path=AmyUtils.get_base_path() + "/ai_models/gemma-3-4b-it-Q4_K_M.gguf",
        verbose=True,
        n_ctx=4096,
        )

    def getAnswerToText(self, text):
        print("here received", text)
        Memory.saveMessage(Message(role="user", content=text))
        messages_to_send = Memory.getMessages()
        print("1")
        system_content = get_config_personality() + " " + get_config_appearance() + " " + get_config_knowledge() + " " + get_config_random_impulse() + " "
        print("2")
        system_content = system_content + "At the end of your sentence write your current mood in brackets choosing only from [neutral], [curious], [happy], [sad], [angry], [surprised], [lovey]."
        print("3")
        messages_to_send.insert(0, Message(role="system", content=system_content))
        print("4")
        messagesListJson = json.dumps([message.__dict__ for message in messages_to_send])

        print("we are sending the json:", messagesListJson)

        answer = self.llm.create_chat_completion(
            messages = messages_to_send,
            temperature=0.01,
            max_tokens=512
        )
        print("answer", answer)
        print("all messages before exiting the function", Memory.getMessages())

        return answer