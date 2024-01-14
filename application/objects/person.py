from typing import Optional

import pydantic


class Person(pydantic.BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
