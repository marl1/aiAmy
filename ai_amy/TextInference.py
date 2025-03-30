import base64
from llama_cpp import Llama
from sklearn import get_config
from ConfigController import *
from model.ChatCompletion import Message
from typing import List
import json



class TextInference:
    def __init__(self):
        self.llm = Llama(
        model_path="./ai_amy/ai_models/gemma-3-4b-it-Q4_K_M.gguf",
        verbose=True,
        n_ctx=4096,
        )

    def getAnswerToText(self, text, previousMessages:List[Message]):
        print("here received", text)
        print(previousMessages)
        previousMessages.append(Message(role="user", content=text))
        messages_to_send = previousMessages.copy()        
        system_content = get_config_personality() + " " + get_config_appearance() + " " + get_config_random_impulse() + " "
        system_content = system_content + "At the end of your sentence write your current mood in brackets choosing only from [neutral], [curious], [happy], [sad], [angry], [surprised], [lovey]."
        messages_to_send.insert(0, Message(role="system", content=system_content))
        messagesListJson = json.dumps([message.__dict__ for message in messages_to_send])

        print("we are sending the json:", messagesListJson)

        answer = self.llm.create_chat_completion(
            messages = messages_to_send,
            temperature=0.01,
            max_tokens=512
        )
        print("answer", answer)
        return answer