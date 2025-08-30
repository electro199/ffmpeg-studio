from .base import BaseFilter


class Crop(BaseFilter):
    def __init__(
        self,
        x: str | int,
        y: str | int,
        w: str | int,
        h: str | int,
        keep_aspect: bool = False,
        **kwargs,
    ):
        super().__init__("crop")
        self.flags = {
            "x": x,
            "y": y,
            "w": w,
            "h": h,
            "keep_aspect": keep_aspect,
        }
        self.flags.update(kwargs)
