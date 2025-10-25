from .base import BaseFilter


class Split(BaseFilter):
    def __init__(self, n: int):
        super().__init__("split")
        self.output_count = n

    def _build(self) -> str:
        return f"{self.filter_name}={self.output_count}"