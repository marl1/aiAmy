import re
import TextInference
from Memory import Memory
from pydantic import ValidationError
from MainWindow import MainWindow
from concurrent import futures
from model.ChatCompletion import *
from loguru import logger
from ConfigController import *


thread_pool_executor = futures.ThreadPoolExecutor(max_workers=1)

class AmyController:
    IS_TEXT_INFERING=False
    def __init__(self):
        logger.add("AiAmy.log", level="INFO", rotation="50 MB")
        logger.info(f"Launching AiAmy...")
        # Launch the LLM
        self.text_inference = TextInference.TextInference()
        # Create the Windows for the character
        self.main_window=MainWindow(self)
        self.main_window.root.after(0, lambda: self.main_window.amy_animation.changePicture(get_config_default_picture().file))
        self.main_window.start_mainloop()

    def send_text(self, text):
        print("received ", text)
        thread_pool_executor.submit(self.fetch_answer, text)

    def fetch_answer(self, text):
        """ Interrogate the text model. """
        if (self.IS_TEXT_INFERING):
            logger.error(f"Got {text} to infer but we were already infering.")
            return # We are alrealdy generating text so we exit.
        answer = self.text_inference.getAnswerToText(text)
        if(get_config_log_chat()):
            logger.info(f"USER: {text}")
        try:
            chat:ChatCompletion = ChatCompletion.model_validate(answer)
            amy_answer = chat.choices[0].message.content
            self.main_window.root.after(0, self.handle_answer, amy_answer)
            if(get_config_log_chat()):
                logger.info(f"AMY: {amy_answer}")
            # If the answer is long the answer window may gets higher so we needs to update it.
            self.main_window.update_following_windows_position()
        except ValidationError as e:
            logger.error(f"Couldn't handle the following answer from the LLM: {answer}")
        self.IS_TEXT_INFERING = False

    def handle_answer(self, amy_answer):
        """ Operations done upon Amy answering. """
        self.main_window.text_output.set_content(re.sub(r"\[.*?\]", "", amy_answer))
        picture :CharConfigPictureModel = self.main_window.amy_animation.changePictureAccordingToMood(amy_answer)
        message_to_add_in_memory = amy_answer
        if picture and picture.add_to_memory:
            message_to_add_in_memory = " " + picture.add_to_memory
        Memory.saveMessage(Message(role="assistant", content=message_to_add_in_memory))