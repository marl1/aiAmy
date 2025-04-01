import threading
import ImageLabel
import AmyUtils
from ConfigController import *
from model.CharConfigModel import CharConfigPictureModel

#https://medium.com/analytics-vidhya/how-to-create-a-thread-safe-singleton-class-in-python-822e1170a7f6
#https://stackoverflow.com/questions/50566934
class AmyAnimation:
    """ Singleton class that handle the animations. """
    _instance = None
    _lock = threading.Lock()
    _imageLabel :ImageLabel = None

    def __new__(cls, imageLabel :ImageLabel):
        if cls._instance is None: 
            with cls._lock:
                # Another thread could have created the instance before we
                # acquired the lock. So check that the instance is still nonexistent.
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._imageLabel = imageLabel
        return cls._instance

    def changePicture(self, new_picture):
        """ Thread safe. Change the picture of Amy. """
        with self._lock:
            self._imageLabel.unload()
            self._imageLabel.load(AmyUtils.get_base_path() + "/chars/" + get_config_current_character() + "/img/" + new_picture)

    def changePictureAccordingToMood(self, amy_answer):
        """ """
        # Get "happy" from the string Hello! [happy].
        amy_answer[amy_answer.rfind("[")+1:amy_answer.rfind("]")]
        print("amy_answer", amy_answer)
        pictures_from_mood: CharConfigPictureModel = get_config_picture_from_mood("amy_answer")
        self._imageLabel.load(AmyUtils.get_base_path() + "/chars/" + get_config_current_character() + "/img/" + random.choice(pictures_from_mood).file)
