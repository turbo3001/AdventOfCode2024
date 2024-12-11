from enum import Enum, auto

class NodeDir(Enum):
    NORTH = auto(),
    EAST = auto(),
    SOUTH = auto(),
    WEST = auto()


class PathNode:
    def __init__(self, Number:int):
        self.Number:int = Number
        self.NextNodes:dict[NodeDir, PathNode|None] = {
            NodeDir.NORTH: None,
            NodeDir.EAST: None,
            NodeDir.SOUTH: None,
            NodeDir.WEST: None
        }
        self.CachedScore:None|int = None

    def __repr__(self):
        return f'<{self.Number} {self.NextNodes}>'

    def SetNextNode(self, Dir:NodeDir, NextNode) -> None:
        if not isinstance(NextNode, PathNode):
            raise TypeError()
        self.NextNodes[Dir] = NextNode

    def CalculateScore(self) -> int:
        if self.CachedScore is None:
            if self.Number == 9:
                self.CachedScore = 1
            else:
                self.CachedScore = 0
            for Dir in NodeDir:
                NextNode:PathNode|None = self.NextNodes[Dir]
                if NextNode is not None:
                    self.CachedScore += NextNode.CalculateScore()

        return self.CachedScore

def GetTrailMap(MapData:iter) -> list[list[PathNode]]:
    trailMap:list[list[PathNode]] = []
    for y, MapRow in enumerate(MapData):
        trailMap.append([])
        for x, TrailChar in enumerate(MapRow):
            if TrailChar == "\n":
                break
            TrailValue:int = int(TrailChar)
            NewNode = PathNode(TrailValue)
            if y > 0:
                NorthNode:PathNode = trailMap[y-1][x]
                NodeDiff = NorthNode.Number - TrailValue
                if NodeDiff == -1:
                    NorthNode.SetNextNode(NodeDir.SOUTH, NewNode)
                elif NodeDiff == 1:
                    NewNode.SetNextNode(NodeDir.NORTH, NorthNode)
            if x > 0:
                LeftNode:PathNode = trailMap[y][x-1]
                NodeDiff = LeftNode.Number - TrailValue
                if NodeDiff == -1:
                    LeftNode.SetNextNode(NodeDir.EAST, NewNode)
                elif NodeDiff == 1:
                    NewNode.SetNextNode(NodeDir.WEST, LeftNode)
            trailMap[y].append(NewNode)
    return trailMap

if __name__ == "__main__":
    with open("./Day_10/InputData/Input.txt") as file:
        TrailMap:list[list[PathNode]] = GetTrailMap(file)
        sum:int = 0
        for MapRow in TrailMap:
            for MapNode in MapRow:
                if MapNode.Number == 0:
                    NodeScore:int = MapNode.CalculateScore()
                    print(NodeScore)
                    sum += NodeScore
        print(sum)

