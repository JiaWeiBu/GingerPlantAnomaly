
class Size:
    def __init__(self, width: int | None, height: int | None):
        self.width : int = width # type: ignore
        self.height : int = height # type: ignore

    def ClassValidation(self):
        assert isinstance(self.width, int), "Width must be an integer"
        assert isinstance(self.height, int), "Height must be an integer"

    def SetWidth(self, width: int):
        self.width = width

    def SetHeight(self, height: int):
        self.height = height

class Point:
    def __init__(self, x: int | None, y: int | None):
        self.x : int = x # type: ignore
        self.y : int = y # type: ignore

    def ClassValidation(self):
        assert isinstance(self.x, int), "X must be an integer"
        assert isinstance(self.y, int), "Y must be an integer"

    def SetX(self, x: int):
        self.x = x

    def SetY(self, y: int):
        self.y = y

class Rect:
    def __init__(self, size: Size, point: Point):
        self.size : Size = size
        self.point : Point = point

    def ClassValidation(self):
        self.size.ClassValidation()
        self.point.ClassValidation()

    def SetSize(self, size: Size):
        self.size = size

    def SetPoint(self, point: Point):
        self.point = point