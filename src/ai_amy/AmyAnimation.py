import random
import threading
from tkinter import Tk
from typing import List
import ImageLabel
import AmyUtils
from ConfigController import get_config_current_character, get_config_picture_from_mood
from model.CharConfigModel import CharConfigPictureModel

#https://medium.com/analytics-vidhya/how-to-create-a-thread-safe-singleton-class-in-python-822e1170a7f6
#https://stackoverflow.com/questions/50566934
class AmyAnimation:
    """ Singleton class that handle the animations. """
    _instance = None
    _lock = threading.Lock()
    _imageLabel :ImageLabel = None
    _rootWindow :Tk = None

    def __new__(cls, imageLabel :ImageLabel, rootWindow :Tk):
        if cls._instance is None: 
            with cls._lock:
                # Another thread could have created the instance before we
                # acquired the lock. So check that the instance is still nonexistent.
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._imageLabel = imageLabel
                    cls._rootWindow = imageLabel
        return cls._instance

    def changePicture(self, new_picture):
        """ Thread safe. Change the picture of Amy. """
        with self._lock:
            self._imageLabel.unload()
            self._imageLabel.load(AmyUtils.get_base_path() + "/chars/" + get_config_current_character() + "/img/" + new_picture)

    def changePictureAccordingToMood(self, amy_answer):
        """ Get the part between bracket in Amy's answer that represent a feeling and play the picture accordingly, for the specified delay. """
        # Get "happy" from the string Hello! [happy].
        amy_answer[amy_answer.rfind("[")+1:amy_answer.rfind("]")]
        print("amy_answer", amy_answer)
        pictures_from_mood: List[CharConfigPictureModel] = get_config_picture_from_mood("amy_answer")
        selected_picture_for_current_mood: CharConfigPictureModel = random.choice(pictures_from_mood)
        self._imageLabel.load(AmyUtils.get_base_path() + "/chars/" + get_config_current_character() + "/img/" + selected_picture_for_current_mood.file)
        stop_anim_after = random.randint(selected_picture_for_current_mood.playing_time_min*1000, selected_picture_for_current_mood.playing_time_min*1000)
        self._rootWindow.after(stop_anim_after, lambda: self.changePicture("stony.png"))