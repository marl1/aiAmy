import base64
from llama_cpp import Llama
from sklearn import get_config
from ConfigController import *



class TextInference:
    def __init__(self):
        self.llm = Llama(
        model_path="./ai_amy/ai_models/gemma-3-4b-it-Q4_K_M.gguf",
        verbose=True,
        n_ctx=2048, # n_ctx should be increased to accommodate the image embedding
        )

    def getAnswerToText(self, text):
        print("here received", text)
        answer = self.llm.create_chat_completion(
            messages = [
                {"role": "system", "content": get_config_personality() + " " + get_config_random_mood()},
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0.01,
            max_tokens=512
        )
        print("answer", answer)
        return answer