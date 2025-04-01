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
        try:
            self.llm = Llama(
            model_path=get_config_ai_text_model(),
            verbose=True,
            n_ctx=4096,
            )
        except:
            logger.error(f"Couldn't read {get_config_ai_text_model()}. Make sure the file is at the root level and readable.")
            sys.exit(1)

    def getAnswerToText(self, text):
        print("here received", text)
        Memory.saveMessage(Message(role="user", content=text))
        messages_to_send = Memory.getMessages()
        system_content = get_config_personality() + " " + get_config_appearance() + " " + get_config_knowledge() + " " + get_config_random_impulse() + " "
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
        print("all messages before exiting the function", Memory.getMessages())

        return answer