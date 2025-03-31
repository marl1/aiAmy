import os
import yaml
import random
import AmyUtils
from loguru import logger


config =  []
character_config =  []
try:
    with open("config.yml", "r") as yamlfile:
        config = yaml.load(yamlfile, Loader=yaml.FullLoader)
except:
    logger.error(f"Couldn't read config.yml file. Make sure the file is at the root level and readable.")
    exit(1)

try:
    char_config_path = AmyUtils.get_base_path() + "/chars/" + config['application']['current_character'] + "/charconfig.yml"
    with open(char_config_path, "r") as yamlfile:
        character_config = yaml.load(yamlfile, Loader=yaml.FullLoader)
except:
    logger.error(f"Couldn't read charconfig.yml file. Make sure the file is under {char_config_path} and readable.")
    exit(1)


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
    return character_config['personnality']

def get_config_knowledge():
    return character_config['knowledge']

def get_config_appearance():
    return character_config['appearance']

def get_config_random_impulse():
    ponderated_impulses = []
    for impulse in character_config['impulses']:
        ponderated_impulses.extend([impulse] * impulse['weight'])
    return random.choice(ponderated_impulses)['description']