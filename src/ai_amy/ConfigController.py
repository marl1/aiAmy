import os
from pydantic import ValidationError
import yaml
import random
import AmyUtils
from loguru import logger
import sys
from model.CharConfigModel import CharConfigModel, CharConfigPictureModel


config =  []
config_path = os.path.join(AmyUtils.get_base_path(),"config.yml")
try:
    with open(config_path, "r") as yamlfile:
        config = yaml.load(yamlfile, Loader=yaml.FullLoader)
except:
    logger.error(f"Couldn't read {config_path}. Make sure the file is at the root level and readable.")
    sys.exit(1)

try:
    char_config_path = os.path.join(AmyUtils.get_base_path(),"chars",config['application']['current_character'],"charconfig.yml")
    with open(char_config_path, "r") as yamlfile:
        character_config_dict = yaml.load(yamlfile, Loader=yaml.FullLoader)
except:
    logger.error(f"Couldn't read charconfig.yml file. Make sure the file is under {char_config_path} and readable.")
    sys.exit(1)

try:
    char_config_object: CharConfigModel = CharConfigModel.model_validate(character_config_dict)
except ValidationError as e:
    logger.error(f"Character configuration file {char_config_path} has invalid structure or data types:")
    logger.error(e)
    sys.exit(1)

########## Application
def get_config_log_chat():
    return config['application']['record_all_chats']

def get_config_current_character():
    return config['application']['current_character']

def get_config_ai_text_model():
    model_path = config['application']['ai_text_model']
    if os.path.isabs(model_path):
        # The model path is an absolute path, he wants to use another model outside of amy's folder.
        return model_path
    else:
        return f"{AmyUtils.get_base_path()}/ai_models/{model_path}"

########### Character
def get_config_personality():
    return char_config_object.personality

def get_config_knowledge():
    return char_config_object.knowledge

def get_config_appearance():
    return char_config_object.appearance

def get_config_random_impulse():
    ponderated_impulses = []
    for impulse in char_config_object.impulses:
        ponderated_impulses.extend([impulse] * impulse.weight)
    return random.choice(ponderated_impulses).description

def get_config_picture_from_mood(mood: str):
    ponderated_pictures_for_this_mood = []
    for picture in char_config_object.pictures:
        if picture.play_on_mood and picture.play_on_mood == mood:
            ponderated_pictures_for_this_mood.extend([picture] * picture.weight)
    return ponderated_pictures_for_this_mood

def get_config_picture_from_name(picture_name: str) -> CharConfigPictureModel:
    for picture in char_config_object.pictures:
        if picture.name == picture_name:
            return picture
    return None

def get_config_default_picture() -> CharConfigPictureModel:
    for picture in char_config_object.pictures:
        if picture.default == True:
            return picture
    return None