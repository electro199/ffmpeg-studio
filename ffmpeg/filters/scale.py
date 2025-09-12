from enum import IntEnum, StrEnum
from typing import Self
from .base import BaseFilter


class EvalMode(StrEnum):
    INIT = "init"
    FRAME = "frame"


class InterlacingMode(IntEnum):
    ENABLED = 1
    DISABLED = 0
    AUTO = -1


class Intent(StrEnum):
    PERCEPTUAL = "perceptual"
    RELATIVE_COLORIMETRIC = "relative_colorimetric"
    ABSOLUTE_COLORIMETRIC = "absolute_colorimetric"
    SATURATION = "saturation"


class ColorMatrix(StrEnum):
    AUTO = "auto"
    BT709 = "bt709"
    FCC = "fcc"
    BT601 = "bt601"
    BT470 = "bt470"
    SMPTE170M = "smpte170m"
    SMPTE240M = "smpte240m"
    BT2020 = "bt2020"


class IORange(StrEnum):
    AUTO = "auto"
    JPEG = "jpeg"
    MPEG = "mpeg"


class IOChromaLocation(StrEnum):
    AUTO = "auto"
    UNKNOWN = "unknown"
    LEFT = "left"
    CENTER = "center"
    TOPLEFT = "topleft"
    TOP = "top"
    BOTTOMLEFT = "bottomleft"
    BOTTOM = "bottom"


class IOPrimaries(StrEnum):
    AUTO = "auto"
    BT709 = "bt709"
    BT470M = "bt470m"
    BT470BG = "bt470bg"
    SMPTE170M = "smpte170m"
    SMPTE240M = "smpte240m"
    FILM = "film"
    BT2020 = "bt2020"
    SMPTE428 = "smpte428"
    SMPTE431 = "smpte431"
    SMPTE432 = "smpte432"
    JEDEC_P22 = "jedec-p22"
    EBU3213 = "ebu3213"


class AspectRatioMode(StrEnum):
    DISABLE = "disable"
    DECREASE = "decrease"
    INCREASE = "increase"


class Scale(BaseFilter):
    """
    Represents the FFmpeg scale filter.

    Args:
        width: The width of the output video.
        height: The height of the output video.
    """
    def __init__(self, width: float, height: float):
        super().__init__("scale")
        self.flags: dict[str, float | int | str | bool] = {"width": width, "height": height}

    # --- helper methods for each option ---

    def set_eval(self, mode: EvalMode) -> Self:
        """
        Set the evaluation mode. Useful for dynamic scaling.

        Args:
            mode: The evaluation mode.

        Returns:
            Self: The current Scale instance.
        """
        self.flags["eval"] = mode
        return self

    def set_interlacing(self, mode: InterlacingMode) -> Self:
        """
        Set the interlacing mode. 

        Args:
            mode: The interlacing mode.

        Returns:
            Self: The current Scale instance.
        """
        self.flags["interl"] = mode
        return self

    def set_intent(self, intent: Intent) -> Self:
        """
        Set the color intent.

        Args:
            intent: The color intent.

        Returns:
            Self: The current Scale instance.
        """
        self.flags["intent"] = intent
        return self

    def set_in_color_matrix(self, matrix: ColorMatrix) -> Self:
        """
        Set the input color matrix.

        Args:
            matrix: The input color matrix.

        Returns:
            Self: The current Scale instance.
        """
        self.flags["in_color_matrix"] = matrix
        return self

    def set_out_color_matrix(self, matrix: ColorMatrix) -> Self:
        """
        Set the output color matrix.

        Args:
            matrix: The output color matrix.

        Returns:
            Self: The current Scale instance.
        """
        self.flags["out_color_matrix"] = matrix
        return self

    def set_in_range(self, rng: IORange) -> Self:
        """
        Set the input range.

        Args:
            rng: The input range.

        Returns:
            Self: The current Scale instance.
        """
        self.flags["in_range"] = rng
        return self

    def set_out_range(self, rng: IORange) -> Self:
        """
        Set the output range.

        Args:
            rng: The output range.

        Returns:
            Self: The current Scale instance.
        """
        self.flags["out_range"] = rng
        return self

    def set_in_chroma_location(self, loc: IOChromaLocation) -> Self:
        """
        Set the input chroma location.

        Args:
            loc: The input chroma location.

        Returns:
            Self: The current Scale instance.
        """
        self.flags["in_chroma_loc"] = loc
        return self

    def set_out_chroma_location(self, loc: IOChromaLocation) -> Self:
        """
        Set the output chroma location.

        Args:
            loc: The output chroma location.

        Returns:
            Self: The current Scale instance.
        """
        self.flags["out_chroma_loc"] = loc
        return self

    def set_in_primaries(self, primaries: IOPrimaries) -> Self:
        """
        Set the input color primaries.

        Args:
            primaries: The input color primaries.

        Returns:
            Self: The current Scale instance.
        """
        self.flags["in_primaries"] = primaries
        return self

    def set_out_primaries(self, primaries: IOPrimaries) -> Self:
        """
        Set the output color primaries.

        Args:
            primaries: The output color primaries.

        Returns:
            Self: The current Scale instance.
        """
        self.flags["out_primaries"] = primaries
        return self

    def set_aspect_ratio_mode(self, mode: AspectRatioMode) -> Self:
        """
        Set the aspect ratio mode.

        Args:
            mode: The aspect ratio mode.

        Returns:
            Self: The current Scale instance.
        """
        self.flags["force_original_aspect_ratio"] = mode
        return self

    def set_force_divisible_by(self, n: int) -> Self:
        """
        Set the force divisible by value.

        Args:
            n: The value to force divisibility by.

        Returns:
            Self: The current Scale instance.
        """
        self.flags["force_divisible_by"] = n
        return self

    def reset_sar(self, enable: bool = True) -> Self:
        """
        Reset the sample aspect ratio.

        Args:
            enable: Whether to enable resetting SAR.

        Returns:
            Self: The current Scale instance.
        """
        self.flags["reset_sar"] = enable
        return self
