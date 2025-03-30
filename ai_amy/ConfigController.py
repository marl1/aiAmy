import yaml
import random
from loguru import logger


config =  []
try:
    with open("config.yml", "r") as yamlfile:
        config = yaml.load(yamlfile, Loader=yaml.FullLoader)
except:
    config.error(f"Couldn't read config.yml file. Make sure the file is at the root level and readable.")
print(config)

    

def get_config_personality():
    return config['character']['personnality']

def get_config_knowledge():
    return config['character']['knowledge']

def get_config_appearance():
    return config['character']['appearance']

def get_config_log_chat():
    return config['application']['record_all_chats']

def get_config_random_impulse():
    ponderated_impulses = []
    for impulse in config['character']['impulses']:
        ponderated_impulses.extend([impulse] * impulse['weight'])
    return random.choice(ponderated_impulses)['description']