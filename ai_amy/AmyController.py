from pydantic import ValidationError
from MainWindow import MainWindow
from ai_amy.TextAndVisionInference import *
from concurrent import futures
from model.ChatCompletion import *
import ast
from loguru import logger

thread_pool_executor = futures.ThreadPoolExecutor(max_workers=1)

class AmyController:
    def __init__(self):
        logger.add("AiAmy.log", level="INFO", rotation="50 MB")
        logger.info(f"Launching AiAmy...")

        # Launch the LLM
        self.text_inference = TextAndVisionInference()
        # Create the Windows for the character
        self.main_window=MainWindow(self)
        self.main_window.start_mainloop()

    def send_text(self, text):
        print("received ", text)
        thread_pool_executor.submit(self.fetch_answer, text)

    def fetch_answer(self, text):
        answer = self.text_inference.getAnswerTo(text)
        try:
            chat = ChatCompletion.model_validate(answer)
            self.main_window.text_output.set_content(chat.choices[0].message.content)
        except ValidationError as e:
            logger.error(f"Couldn't handle the following answer from the LLM: {answer}")
