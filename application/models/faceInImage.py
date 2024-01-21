from typing import Optional, Annotated, Literal
import numpy as np
import numpy.typing as npt
import pydantic
from pydantic import Field


class FaceInImage(pydantic.BaseModel):
    id: Optional[int] = None
    image_id: Optional[int] = None
    img_x_pos: int
    img_y_pos: int
    img_width: int
    img_height: int
    encoding: np.ndarray = Field(default_factory=lambda: np.zeros(4096, dtype=np.float32))

    class Config:
        arbitrary_types_allowed = True


    def __str__(self):
        return f"[FaceInImage] id: {self.id}, image_id: {self} | ({self.img_x_pos}, {self.img_y_pos}, {self.img_width}, {self.img_height})"
