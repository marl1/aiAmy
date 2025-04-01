import random
import threading
from tkinter import Tk
from typing import List
import ImageLabel
import AmyUtils
from ConfigController import get_config_current_character, get_config_default_picture, get_config_picture_from_mood, get_config_picture_from_name
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
        mood = amy_answer[amy_answer.rfind("[")+1:amy_answer.rfind("]")]
        pictures_from_mood: List[CharConfigPictureModel] = get_config_picture_from_mood(mood)
        if pictures_from_mood:
            self.loadAnimation(random.choice(pictures_from_mood))

    
    def loadAnimation(self, picture_to_load: CharConfigPictureModel):
            """ Load the specified animation and prepare the next one. """
            self.changePicture(picture_to_load.file)
            # Load the next animation if there's a time limit for the current one
            if picture_to_load.playing_time_min and not picture_to_load.playing_time_max:
                picture_to_load.playing_time_max = picture_to_load.playing_time_min
            if picture_to_load.playing_time_min and not picture_to_load.playing_time_min:
                picture_to_load.playing_time_min = picture_to_load.playing_time_max
            if picture_to_load.playing_time_min and picture_to_load.playing_time_max:       
                stop_anim_after = random.randint(picture_to_load.playing_time_min*1000, picture_to_load.playing_time_min*1000)
                print("stop_anim_after", stop_anim_after)
                next_picture :CharConfigPictureModel=get_config_picture_from_name(picture_to_load.followed_by_picture)
                if next_picture:
                    self._rootWindow.after(stop_anim_after, lambda: self.loadAnimation(next_picture))
                else:
                    self._rootWindow.after(stop_anim_after, lambda: self.loadAnimation(get_config_default_picture()))