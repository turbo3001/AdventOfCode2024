from enum import Enum, auto

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, value):
        if not isinstance(value, Point):
            raise TypeError()
        return Point(self.x - value.x, self.y - value.y)
    
    def __add__(self, value):
        if not isinstance(value, Point):
            raise TypeError()
        return Point(self.x + value.x, self.y + value.y)
    
    def __eq__(self, value):
        if not isinstance(value, Point):
            raise TypeError()
        return self.x == value.x and self.y == value.y
    
    def __repr__(self):
        return f"({self.x}, {self.y})"

class PlotDir(Enum):
    NORTH = auto(),
    EAST = auto(),
    SOUTH = auto(),
    WEST = auto()


class Region:
    def __init__(self, StartPos:Point, RegionChar:str):
        self.StartPos:Point = StartPos
        self.RegionChar:str = RegionChar
        self.ConnectedNodes:dict[PlotDir, Region]
    def __repr__(self):
        return f''

        
def GetRegions(MapData:iter) -> list[Region]:
    Regions:list[Region] = []
    # for y, MapRow in enumerate(MapData):
    #     for x, MapChar in enumerate(MapRow):
    #         if MapChar not in MappedRegions:
    #             MappedRegions[MapChar] = []
    #         PlotPos:Point = Point(x,y)
    #         FoundRegion:bool = False
    #         for ExistingRegion in MappedRegions[MapChar]:
    #             if ExistingRegion.TryAddPlot(PlotPos):
    #                 FoundRegion = True
    #                 break
    #         if not FoundRegion:
    #             MappedRegions[MapChar].append(Region(PlotPos))
    
    # for Char in MappedRegions:
    #     Regions += MappedRegions[Char]
    return Regions


if __name__ == "__main__":
    with open("./Day_12/InputData/Example.txt") as file:
        print(GetRegions(file))
