import random
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

def getIdle() -> CharConfigIdleModel:
    """Returns the appropriate idle according to the time elapsed since last action. Should be called every second."""
    global last_action
    idle_time = int(time.time()-last_action)
    possible_idles: List[CharConfigIdleModel] = config_module.get().get_config_idle_from_idle_time(idle_time)
    idles_weight = [idle.weight for idle in possible_idles]
    while possible_idles:
        # First, pick one of the idle anim/text based on the weigth.
        idle_candidate: CharConfigIdleModel = random.choices(possible_idles, idles_weight)[0]
        # Then, throw the dice to see if the idle will play.
        if random.randint(1, 1000) <= idle_candidate.per_thousand_chance:
            print(idle_candidate, "was selected")
            last_action=time.time()
            return idle_candidate
        else:
            # Find the index of the failed candidate
            idx_to_remove = possible_idles.index(idle_candidate)
            # Remove it from both lists using the index
            possible_idles.pop(idx_to_remove)
            idles_weight.pop(idx_to_remove)
            if not possible_idles:
                return None
def reset():
    global last_action
    last_action = time.time()