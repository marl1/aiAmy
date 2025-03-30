from pydantic import ValidationError
from MainWindow import MainWindow
from ai_amy.TextInference import *
from concurrent import futures
from model.ChatCompletion import *
import ast
from loguru import logger
from Memory import *
from ConfigController import *


thread_pool_executor = futures.ThreadPoolExecutor(max_workers=1)

class AmyController:
    IS_TEXT_INFERING=False
    def __init__(self):
        logger.add("AiAmy.log", level="INFO", rotation="50 MB")
        logger.info(f"Launching AiAmy...")
        # Launch the LLM
        self.text_inference = TextInference()
        # Create the short term memory that will hold the previous dialog.
        self.memory = Memory()
        # Create the Windows for the character
        self.main_window=MainWindow(self)
        self.main_window.start_mainloop()

    def send_text(self, text):
        print("received ", text)
        thread_pool_executor.submit(self.fetch_answer, text)

    def fetch_answer(self, text):
        """ Interrogate the text model. """
        if (self.IS_TEXT_INFERING):
            logger.error(f"Got {text} to infer but we were already infering.")
            return # We are alrealdy generating text so we exit.
        print("0")
        answer = self.text_inference.getAnswerToText(text, self.memory.getMessages())
        if(get_config_log_chat()):
            logger.info(f"USER: {text}")
        try:
            chat:ChatCompletion = ChatCompletion.model_validate(answer)
            self.memory.saveMessage(chat.choices[-1].message)
            if(get_config_log_chat()):
                logger.info(f"AMY: {chat.choices[0].message.content}")
            self.main_window.text_output.set_content(chat.choices[0].message.content)
            # If the answer is long the answer window may gets higher so we needs to update it.
            self.main_window.update_following_windows_position()
        except ValidationError as e:
            logger.error(f"Couldn't handle the following answer from the LLM: {answer}")
        self.IS_TEXT_INFERING = False
