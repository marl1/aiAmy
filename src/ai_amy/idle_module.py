import time
from typing import List
from loguru import logger
from model.CharConfigModel import CharConfigIdleModel
import config_module


# Since when the character was idling.
last_action: int=0

def init():
    global last_action
    last_action = time.time()

def getIdle():
    idle_time = int(time.time()-last_action)
    possible_idles: List[CharConfigIdleModel] = config_module.get().get_config_idle_from_idle_time(idle_time)
    print(possible_idles)
    # I'll need to pick from the list according to probabilities : https://stackoverflow.com/questions/22722079