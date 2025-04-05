import random
import re
import sys
import TextInference
import idle_module
from model.CharConfigModel import CharConfigIdleModel, CharConfigPictureModel
import config_module as config
from Memory import Memory
from pydantic import ValidationError
from MainWindow import MainWindow
from concurrent import futures
from model.ChatCompletion import *
from loguru import logger


thread_pool_executor = futures.ThreadPoolExecutor(max_workers=1)

class AmyController:
    IS_TEXT_INFERING=False
    def __init__(self):
        logger.add("AiAmy.log", level="INFO", rotation="50 MB")
        logger.info(f"Launching AiAmy...")
        config.init_config_controller()
        idle_module.init()
        # Launch the LLM
        self.text_inference = TextInference.TextInference()
        # Create the Windows for the character
        self.main_window=MainWindow(self)
        self.main_window.root.after(0, lambda: self.main_window.amy_animation.changePicture(config.get().get_config_default_picture().file))
        self.main_window.root.after(1000, self.handle_idle)
        self.main_window.start_mainloop()

    def send_text(self, text):
        print("received ", text)
        if not self.IS_TEXT_INFERING:
            thread_pool_executor.submit(self.fetch_answer, text)

    def fetch_answer(self, text):
        """ Interrogate the text model. """
        if (self.IS_TEXT_INFERING):
            logger.error(f"Got {text} to infer but we were already infering.")
            return # We are alrealdy generating text so we exit.
        self.IS_TEXT_INFERING = True
        answer = self.text_inference.getAnswerToText(text)
        if(config.get().get_config_log_chat()):
            logger.info(f"USER: {text}")
        try:
            chat:ChatCompletion = ChatCompletion.model_validate(answer)
            amy_answer = chat.choices[0].message.content
            self.main_window.root.after(0, self.handle_answer, amy_answer)
            if(config.get().get_config_log_chat()):
                logger.info(f"AMY: {amy_answer}")
            # If the answer is long the answer window may gets higher so we needs to update it.
            self.main_window.update_following_windows_position()
        except ValidationError as e:
            logger.error(f"Couldn't handle the following answer from the LLM: {answer}")
        self.IS_TEXT_INFERING = False

    def handle_answer(self, amy_answer: str):
        """ Operations done upon Amy answering. """
        idle_module.reset()
        self.main_window.text_output_window.set_text(re.sub(r"\[.*?\]", "", amy_answer))
        picture :CharConfigPictureModel = self.main_window.amy_animation.changePictureAccordingToMood(amy_answer)
        message_to_add_in_memory = amy_answer
        if picture and picture.add_to_memory:
            message_to_add_in_memory = " " + picture.add_to_memory
        Memory.saveMessage(Message(role="assistant", content=message_to_add_in_memory))

    def handle_idle(self):
        idle_to_play: CharConfigIdleModel = idle_module.getIdle()
        self.main_window.root.after(1000, self.handle_idle)
        if idle_to_play and not self.IS_TEXT_INFERING:
            if idle_to_play.picture:
                self.main_window.root.after(0, lambda: self.main_window.amy_animation.loadAnimation(config.get().get_config_picture_from_name(idle_to_play.picture)))
            if idle_to_play.text:
                # A dummy message necessary to have the alternance user/bot/user/bot, if not the server is not happy.
                Memory.saveMessage(Message(role="user", content=""))
                self.main_window.root.after(0, self.handle_answer, random.choice(idle_to_play.text))