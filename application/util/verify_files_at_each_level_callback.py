from typing import Protocol, List

from application.objects.image import Image


class VerifyFilesAtEachLevelCallback(Protocol):
    def __call__(self, *, dir: str, images: List[Image]) -> None:
        ...
