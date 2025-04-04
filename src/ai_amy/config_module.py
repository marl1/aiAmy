import os
from pydantic import ValidationError
import yaml
import random
import AmyUtils
from typing import List
from loguru import logger
import sys
from model.CharConfigModel import CharConfigIdleModel, CharConfigModel, CharConfigPictureModel

# Another approach at singleton, see below

class ConfigController:

    def __init__(self):
        pass

    def load_config(self):
        self.config =  []
        config_path = os.path.join(AmyUtils.get_base_path(),"config.yml")
        try:
            with open(config_path, "r") as yamlfile:
                self.config = yaml.load(yamlfile, Loader=yaml.FullLoader)
        except:
            logger.error(f"Couldn't read {config_path}. Make sure the file is at the root level and readable.")
            sys.exit(1)

        try:
            char_config_path = os.path.join(AmyUtils.get_base_path(),"chars",self.config['application']['current_character'],"charconfig.yml")
            with open(char_config_path, "r") as yamlfile:
                character_config_dict = yaml.load(yamlfile, Loader=yaml.FullLoader)
        except:
            logger.error(f"Couldn't read charconfig.yml file. Make sure the file is under {char_config_path} and readable.")
            sys.exit(1)

        try:
            self._char_config: CharConfigModel = CharConfigModel.model_validate(character_config_dict)
        except ValidationError as e:
            logger.error(f"Character configuration file {char_config_path} has invalid structure or data types:")
            logger.error(e)
            sys.exit(1)

    ########## Application
    def get_config_log_chat(self):
        return self.config['application']['record_all_chats']

    def get_config_current_character(self):
        return self.config['application']['current_character']

    def get_config_ai_text_model(self):
        model_path = self.config['application']['ai_text_model']
        if os.path.isabs(model_path):
            # The model path is an absolute path, he wants to use another model outside of amy's folder.
            return model_path
        else:
            return f"{AmyUtils.get_base_path()}/ai_models/{model_path}"

    ########### Character
    def get_config_personality(self):
        return self._char_config.personality

    def get_config_knowledge(self):
        return self._char_config.knowledge

    def get_config_appearance(self):
        return self._char_config.appearance

    def get_config_random_impulse(self):
        ponderated_impulses = []
        for impulse in self._char_config.impulses:
            ponderated_impulses.extend([impulse] * impulse.weight)
        return random.choice(ponderated_impulses).description

    def get_config_picture_from_mood(self, mood: str):
        ponderated_pictures_for_this_mood = []
        for picture in self._char_config.pictures:
            if picture.play_on_mood and picture.play_on_mood == mood:
                ponderated_pictures_for_this_mood.extend([picture] * picture.weight)
        return ponderated_pictures_for_this_mood

    def get_config_picture_from_name(self, picture_name: str) -> CharConfigPictureModel:
        for picture in self._char_config.pictures:
            if picture.name == picture_name:
                return picture
        return None

    def get_config_default_picture(self) -> CharConfigPictureModel:
        for picture in self._char_config.pictures:
            if picture.default == True:
                return picture
        return None
    
    def get_config_idle_from_idle_time(self, idle_time: str) -> List[CharConfigIdleModel]:
        idles: List[CharConfigIdleModel] = []
        print("a")
        for idle in self._char_config.idles:
            if idle.after and idle_time>=idle.after:
                if idle.never_after and idle_time<idle.never_after:
                    idles.append(idle)
                    break
            if not idle.never_after and idle.after and idle_time>=idle.after:
                idles.append(idle)
                break
            if not idle.after and idle.never_after and idle_time<idle.never_after:
                idles.append(idle)
                break
            if not idle.after and not idle.never_after:
                idles.append(idle)
                break
        return idles

# So, it's another approach at singleton: this var is defined at the MODULE level (not class level, not instance level).
_global_config_instance: ConfigController | None= None

def init_config_controller():
    global _global_config_instance
    _global_config_instance = ConfigController()
    _global_config_instance.load_config()


def get() -> ConfigController:
   return  _global_config_instance