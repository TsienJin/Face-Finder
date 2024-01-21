import pydantic
from typing import Optional
import numpy as np


class Face(pydantic.BaseModel):
    id: Optional[int] = None
    person_id: Optional[int] = None
    encoding: np.ndarray


