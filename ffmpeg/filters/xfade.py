from .base import BaseFilter


class XFade(BaseFilter):
    all_transitions = (
        "custom",
        "fade",
        "wipeleft",
        "wiperight",
        "wipeup",
        "wipedown",
        "slideleft",
        "slideright",
        "slideup",
        "slidedown",
        "circlecrop",
        "rectcrop",
        "distance",
        "fadeblack",
        "fadewhite",
        "radial",
        "smoothleft",
        "smoothright",
        "smoothup",
        "smoothdown",
        "circleopen",
        "circleclose",
        "vertopen",
        "vertclose",
        "horzopen",
        "horzclose",
        "dissolve",
        "pixelize",
        "diagtl",
        "diagtr",
        "diagbl",
        "diagbr",
        "hlslice",
        "hrslice",
        "vuslice",
        "vdslice",
        "hblur",
        "fadegrays",
        "wipetl",
        "wipetr",
        "wipebl",
        "wipebr",
        "squeezeh",
        "squeezev",
        "zoomin",
        "fadefast",
        "fadeslow",
        "hlwind",
        "hrwind",
        "vuwind",
        "vdwind",
        "coverleft",
        "coverright",
        "coverup",
        "coverdown",
        "revealleft",
        "revealright",
        "revealup",
        "revealdown",
    )

    def __init__(
        self, name: str, offset: float = 0, duration: float = 1, expression=None
    ):
        """
        Combine two videos with transition.
        
        Note: 
            Requires same size and fps and aspect ratio.
        """
        super().__init__("xfade")

        if name == "custom" and not isinstance(expression, str):
            raise TypeError("Expression must be a string")

        if name not in self.all_transitions:
            raise TypeError("Transtion name should ", self.all_transitions)

        self.flags = {"transition": name, "offset": offset, "duration": duration}
