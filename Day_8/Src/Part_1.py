from itertools import combinations
import re
from numpy import sqrt

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, value):
        if not isinstance(value, Vector):
            raise TypeError()
        return Vector(self.x-value.x, self.y - value.y)
    
    def __add__(self, value):
        if not isinstance(value, Vector):
            raise TypeError()
        return Vector(self.x + value.x, self.y + value.y)
    
    def __eq__(self, value) -> bool:
        if not isinstance(value, Vector):
            raise TypeError()
        return self.x == value.x and self.y == value.y
    
    def __lt__(self, value) -> bool:
        if not isinstance(value, Vector):
            raise TypeError()
        return self.Magnitude() < value.Magnitude()
    
    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"
    
    def Magnitude(self) -> float:
        return sqrt((self.x*self.x)+(self.y*self.y))
    
def ListContainsPoint(List:list[Vector], point:Vector) -> bool:
    for currPoint in List:
        if currPoint == point:
            return True
    return False
    
def ParseMapData(MapData:iter) -> list[str]:
    ParsedData:list[str] = []
    for y, MapLine in enumerate(MapData):
        ParsedData.append("")
        for MapChar in MapLine:
            if MapChar == "\n": continue
            ParsedData[y] += MapChar
    return ParsedData
    
class Map:
    def __init__(self, MapData:iter):
        self.MapData:list[str] = ParseMapData(MapData)
        self.Nodes:dict[str, list[Vector]] = self.GetNodeLocations()
    def __repr__(self):
        return f'{self.MapData}\n{self.Nodes}'
    
    
    def ContainsPoint(self, point:Vector):
        return (point.y >= 0 and
                point.x >= 0 and
                point.y < len(self.MapData) and
                point.x < len(self.MapData[point.y]))
    
    def GetNodeLocations(self) -> dict[str, list[Vector]]:
        nodes:dict[str, list[Vector]] = {}
        for y, MapRow in enumerate(self.MapData):
            for x, MapChar in enumerate(MapRow):
                if re.fullmatch(r"\w|\d", MapChar) is not None:
                    if MapChar not in nodes:
                        nodes[MapChar] = []
                    nodes[MapChar].append(Vector(x,y))
        return nodes
    
    def CalculateValidAntiNodes(self) -> list[Vector]:
        validAntiNodes: list[Vector] = []
        for NodeChar in self.Nodes:
            NodeList:list[Vector] = sorted(self.Nodes[NodeChar], reverse=True)
            for NodePair in combinations(NodeList, 2):
                DiffPoint:Vector = NodePair[0] - NodePair[1]
                NewPoint:Vector = NodePair[0] + DiffPoint
                if not ListContainsPoint(validAntiNodes, NewPoint) and self.ContainsPoint(NewPoint):
                    validAntiNodes.append(NewPoint)
                NewPoint = NodePair[1] - DiffPoint
                if not ListContainsPoint(validAntiNodes, NewPoint) and self.ContainsPoint(NewPoint):
                    validAntiNodes.append(NewPoint)
        return validAntiNodes


if __name__ == "__main__":
    with open("./Day_8/InputData/Input.txt") as file:
        NodeMap:Map = Map(file)
        print(NodeMap)
        validAntiNodes = NodeMap.CalculateValidAntiNodes()
        print(validAntiNodes)
        print(len(validAntiNodes))
