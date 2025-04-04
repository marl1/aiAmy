import random
import threading
from tkinter import Tk
from typing import List
import ImageLabel
import AmyUtils
import config_module as config
from model.CharConfigModel import CharConfigPictureModel

#https://medium.com/analytics-vidhya/how-to-create-a-thread-safe-singleton-class-in-python-822e1170a7f6
#https://stackoverflow.com/questions/50566934
class AmyAnimation:
    """ Singleton class that handle the animations. """
    _instance = None
    _lock = threading.Lock()
    _imageLabel :ImageLabel = None
    _rootWindow :Tk = None
    _tkinter_waiting_process_ids :List[str]=[]

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
            self._imageLabel.load(AmyUtils.get_base_path() + "/chars/" + config.get().get_config_current_character() + "/img/" + new_picture)

    def changePictureAccordingToMood(self, amy_answer):
        """ Get the part between bracket in Amy's answer that represent a feeling and play the picture accordingly, for the specified delay. """
        # Get "happy" from the string Hello! [happy].
        chosen_picture :CharConfigPictureModel = None
        mood = amy_answer[amy_answer.rfind("[")+1:amy_answer.rfind("]")]
        pictures_from_mood: List[CharConfigPictureModel] = config.get().get_config_picture_from_mood(mood)
        if pictures_from_mood:
            # A mood is coming right from the LLM, adapted to the text.
            # The animation have the highest priority so we cancel if some were waiting to be chained.
            for waiting_process in self._tkinter_waiting_process_ids:
                self._rootWindow.after_cancel(waiting_process)
            self._tkinter_waiting_process_ids.clear()
            chosen_picture = random.choice(pictures_from_mood)
            self.loadAnimation(chosen_picture)
        return chosen_picture

    
    def loadAnimation(self, picture_to_load: CharConfigPictureModel):
            """ Load the specified animation and prepare the next animation. """
            self.changePicture(picture_to_load.file)
            # Load the next animation if there's a time limit for the current one
            if picture_to_load.playing_time_ms_min and not picture_to_load.playing_time_ms_max:
                picture_to_load.playing_time_ms_max = picture_to_load.playing_time_ms_min
            if picture_to_load.playing_time_ms_min and not picture_to_load.playing_time_ms_min:
                picture_to_load.playing_time_ms_min = picture_to_load.playing_time_ms_max
            if picture_to_load.playing_time_ms_min and picture_to_load.playing_time_ms_max:       
                stop_anim_after = random.randint(picture_to_load.playing_time_ms_min, picture_to_load.playing_time_ms_min)
                if picture_to_load.followed_by_one_of_these_pictures:
                    next_picture :CharConfigPictureModel=config.get().get_config_picture_from_name(random.choice(picture_to_load.followed_by_one_of_these_pictures))
                    if next_picture:
                        self._tkinter_waiting_process_ids.append(
                            self._rootWindow.after(stop_anim_after, lambda: self.loadAnimation(next_picture))
                        )
                else:
                    self._tkinter_waiting_process_ids.append(
                        self._rootWindow.after(stop_anim_after, lambda: self.loadAnimation(config.get().get_config_default_picture()))
                    )