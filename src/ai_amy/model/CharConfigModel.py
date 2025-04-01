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
    file: str
    default: Optional[bool] = Field(default=False)
    play_after_idle_time_min: Optional[int] = None
    play_after_idle_time_max: Optional[int] = None
    play_on_mood: Optional[str] = None
    weight: Optional[int] = None
    loop_min: Optional[int] = None
    loop_max: Optional[int] = None
    model_config = {'extra': 'forbid'}

class CharConfigModel(BaseModel):
    """Configuration model for a desktop pet character."""
    personality: str
    appearance: str
    knowledge: str
    impulses: List[CharImpulseConfigModel]
    pictures: List[CharConfigPictureModel]
    model_config = {'extra': 'forbid'}