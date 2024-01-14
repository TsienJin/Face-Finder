from typing import Optional

import pydantic


class FaceInImage(pydantic.BaseModel):
    id: Optional[int] = None
    image_id: Optional[int] = None
    face_id: Optional[int] = None
    