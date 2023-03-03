from interfaces.uobject import UObject
from mtypes.shape import Rect


class Space(UObject):

    def __init__(self, width: int = 800, height: int = 600, density: int = 10):
        self._width = width
        self._height = height
        self._density = density   # regions will be 80x60 by default

        region_w = int(width / density)
        region_h = int(height / density)

        # full map (k: v) of regions. key is region, value is list of objects in this region
        self._regions = {
            Rect(w, h, w + region_w, h + region_h): []
            for w in range(0, width, region_w)
            for h in range(0, height, region_h)
        }

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def density(self):
        return self._density

    @property
    def regions(self):
        return self._regions
