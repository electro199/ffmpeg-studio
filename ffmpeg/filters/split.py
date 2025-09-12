from .base import BaseFilter


class Split(BaseFilter):
    def __init__(self, n: int):
        super().__init__("split")
        self.flags["n"] = n
        self.output_count = n
