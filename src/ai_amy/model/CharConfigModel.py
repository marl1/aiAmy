from pydantic import BaseModel, Field
from typing import List, Optional
import ast


class CharImpulseConfigModel(BaseModel):
    """Represents a character impulse to do something like jumping around or asking a question."""
    description: str
    weight: int
    model_config = {'extra': 'forbid'}

class CharConfigPictureModel(BaseModel):
    """Represents a picture or animation configuration."""
    name: str
    file: str
    default: Optional[bool] = Field(default=False)
    play_after_idle_time_min: Optional[int] = None
    play_after_idle_time_max: Optional[int] = None
    play_on_mood: Optional[str] = None
    add_to_memory: Optional[str] = None
    weight: Optional[int] = None
    playing_time_ms_min: Optional[int] = None
    playing_time_ms_max: Optional[int] = None
    followed_by_one_of_these_pictures: Optional[List[str]] = None
    model_config = {'extra': 'forbid'}

class CharConfigIdleModel(BaseModel):
    """Represent an action that will be launched after a specified amount of inactivity time."""
    name: str = None
    picture: Optional[str] = None
    after: Optional[int] = None
    never_after: Optional[int] = None
    weight: Optional[int] = 1 # How likely it will be picked up first to check the chance.
    per_thousand_chance: Optional[int] = 1000 # How likely the idle will play.
    text: Optional[List[str]] = None
    followed_by_one_of_these_idle: Optional[List[str]] = None
    summarize_and_reset_dialog: Optional[bool] = None

class CharConfigModel(BaseModel):
    """Configuration model for a desktop pet character."""
    output_window_y_offset: Optional[int] = 0
    prompt: str
    impulses: List[CharImpulseConfigModel]
    pictures: List[CharConfigPictureModel]
    idles: List[CharConfigIdleModel]
    model_config = {'extra': 'forbid'}