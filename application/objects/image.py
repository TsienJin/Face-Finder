import pydantic
from typing import Optional


class Image(pydantic.BaseModel):
    id: Optional[int]
    dir: str
    filename: str

    def __str__(self):
        return f'[ID: {self.id}]\t{self.dir}\t{self.filename}'

    def __repr__(self):
        return self.__str__()

    def toTuple(self):
        return self.id, self.dir
