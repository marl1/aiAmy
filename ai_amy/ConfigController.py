import configparser
import random
from loguru import logger

config = configparser.ConfigParser()
try:
    config.read('config.ini')
except:
    logger.error(f"Couldn't read config.ini file. Make sure the file is at the root level and readable.")

    

def get_config_personality():
    return config['CHARACTER']['Personnality']

def get_config_knowledge():
    return config['CHARACTER']['Knowledge']

def get_config_appearance():
    return config['CHARACTER']['Appearance']

def get_config_log_chat():
    return config['APPLICATION']['RecordAllChats']

def get_config_random_mood():
    moodsFromConfigFile = config['CHARACTER']['Moods']
    moodList = moodsFromConfigFile.splitlines()
    #"generate a list that consists of x for every element in strings if x actually contains something."
    #https://stackoverflow.com/questions/3845423
    moodWithoutBlank = [mood for mood in moodList if mood]
    return random.choice(moodWithoutBlank)