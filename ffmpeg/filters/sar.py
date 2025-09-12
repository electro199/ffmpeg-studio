from .base import BaseFilter


class SetSampleAspectRatio(BaseFilter):
    def __init__(self, expression: str | float = "1"):
        """
        Set the Sample (or Pixel) Aspect Ratio (SAR or PAR) of the input video to the specified value.
        
        The expression can be a float (e.g., 1.0, 1.3333) or a string representing a ratio (e.g., "4:3", "16:9").
        """
        super().__init__("setsar")
        self.flags = {"sar": expression}
