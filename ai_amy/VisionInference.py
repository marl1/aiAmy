import base64
from llama_cpp import Llama
from llama_cpp.llama_chat_format import Llava15ChatHandler
from ConfigController import *


class VisionInference:
    def __init__(self):
        chat_handler = Llava15ChatHandler(clip_model_path="./ai_amy/ai_models/moondream2-mmproj-f16.gguf")
        self.llm = Llama(
        model_path="./ai_amy/ai_models/moondream2-text-model-f16.gguf",
        chat_handler=chat_handler,
            verbose=True,
        n_ctx=2048, # n_ctx should be increased to accommodate the image embedding
        )

    def getAnswerToImage(self, text):
        print("here received", text)
        data_uri = self.image_to_base64_data_uri("./ai_amy/img/stony.png")
        print("encoded to",data_uri)
        answer = self.llm.create_chat_completion(
            messages = [
                {"role": "system", "content": "You are an assistant who perfectly describes images."},
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": data_uri }},
                        {"type" : "text", "text": "Describe this image in detail please."}
                    ]
                }
            ],
            temperature=0.7,
            max_tokens=512
        )
        print("answer", answer)
        return answer

    def image_to_base64_data_uri(self, file_path):
        with open(file_path, "rb") as img_file:
            base64_data = base64.b64encode(img_file.read()).decode('utf-8')
            return f"data:image/png;base64,{base64_data}"