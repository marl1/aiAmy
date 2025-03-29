from nexa.gguf import NexaTextInference

class TextInference:
    def __init__(self):
        self.inference = NexaTextInference(
        model_path=None,
        local_path="./ai_amy/ai_models/llava-phi-3-mini-int4.gguf",
        stop_words=[],
        temperature=0.7,
        max_new_tokens=512,
        top_k=50,
        top_p=0.9,
        profiling=True
    )

    def getAnswerTo(self, text):
        answer = self.inference.create_chat_completion(
            messages=[{"role": "user", "content": "write a long 1000 word story about a detective"}]
        )
        print("la réponse=",answer)
        return answer
