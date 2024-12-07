from concurrent.futures import ThreadPoolExecutor

class Point:
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y

    def __sub__(self, value):
        if not isinstance(value, Point):
            raise TypeError()
        self.x -= value.x
        self.y -= value.y
        return self
    
    def __add__(self, value):
        if not isinstance(value, Point):
            raise TypeError()
        self.x += value.x
        self.y += value.y
        return self
    
    def __eq__(self, value):
        if not isinstance(value, Point):
            raise TypeError()
        return self.x == value.x and self.y == value.y
    
    def __repr__(self):
        return f"({self.x}, {self.y})"

Dirs = [
    Point(0,-1),
    Point(1,0),
    Point(0,1),
    Point(-1,0)
]

GuardDirChar:str = "^>v<"
LoopDirChar:str = "|-|-"

class LoopPoint:
    def __init__(self, Position:Point, Direction:int):
        self.position = Position
        self.direction = Direction
    def dirChar(self) -> str:
        return GuardDirChar[self.direction % len(GuardDirChar)]
    def loopDirChar(self) -> str:
        return LoopDirChar[self.direction % len(LoopDirChar)]
    def __repr__(self):
        return f"{self.position} {self.dirChar()}"
    
    def __eq__(self, value):
        if isinstance(value, Point):
            return self.position == value
        elif isinstance(value, LoopPoint):
            return self.position == value.position and self.direction == value.direction
        else:
            raise TypeError()


def ParseInput(FileData:iter) -> tuple[list[str],Point]:
    MapData:list[str] = []
    GuardPoint:Point = Point(0,0)
    for y, MapLine in enumerate(FileData):
        MapData.append(MapLine)
        for x, Char in enumerate(MapLine):
            if Char == "^":
                GuardPoint.x = x
                GuardPoint.y = y
    return (MapData, GuardPoint)

def GetPointIndex(PointList:list[LoopPoint], PointToFind:Point|LoopPoint) -> int:
    listCopy = PointList.copy()
    listCopy.reverse()
    for i, CurrentPoint in enumerate(listCopy):
        if CurrentPoint == PointToFind:
            return i
    return -1


def PrintMapSection(MapData:list[str], startPos:Point = Point(0,0), range:Point = Point(2,2), WalkedPoints:list[LoopPoint] = [], dirChar:str = GuardDirChar[0], NewObstaclePos:Point = Point(-1,-1)) -> None:
    x:int = startPos.x - range.x
    y:int = startPos.y - range.y
    if y < 0: y = 0
    if x < 0: x = 0
    initialX:int = x
    printStr:str = ""
    while y <= startPos.y + range.y and y < len(MapData):
        MapRow = MapData[y]
        while x <= startPos.x + range.x and x < len(MapRow)-1:
            MapChar = MapRow[x]
            pointIndex = GetPointIndex(WalkedPoints, Point(x, y))
            if(x == NewObstaclePos.x and y == NewObstaclePos.y):
                printStr += "0"
            elif x == startPos.x and y == startPos.y:
                printStr += dirChar
            elif len(WalkedPoints) > 0 and pointIndex >= 0:
                printStr += WalkedPoints[pointIndex].loopDirChar()
            else:
                printStr += MapChar
            x += 1
        printStr+="\n"
        x = initialX
        y += 1
    print(printStr)

def PathLoops(MapData:list[str], GuardPos:Point, NewObstaclePos:Point) -> bool:
    print(NewObstaclePos)
    WalkedPoints:list[LoopPoint] = []
    currentGuardPos:Point = Point(GuardPos.x, GuardPos.y)
    DirIndex:int = 0
    FoundLoop:bool = False
    while True:
        currentDir = Dirs[DirIndex % len(Dirs)]
        currentGuardPos += currentDir
        if (currentGuardPos.y < 0 or
            currentGuardPos.x < 0 or
            currentGuardPos.y >= len(MapData) or
            currentGuardPos.x >= len(MapData[currentGuardPos.y])
            ):
            break

        nextSpace:str = MapData[currentGuardPos.y][currentGuardPos.x]
        if nextSpace == "#":
            #print(f"Hit wall at {currentGuardPos}")
            currentGuardPos -= currentDir
            DirIndex = (DirIndex + 1) % len(Dirs)
            continue
        elif NewObstaclePos == currentGuardPos:
            if len(WalkedPoints) == 0:
                DirIndex = (DirIndex + 1) % len(Dirs)
                WalkedPoints.append(LoopPoint(Point(currentGuardPos.x, currentGuardPos.y), DirIndex))
                currentGuardPos -= currentDir
                continue
            loopPointIndex = GetPointIndex(WalkedPoints, LoopPoint(Point(currentGuardPos.x, currentGuardPos.y), DirIndex))
            if loopPointIndex >= 0 and WalkedPoints[loopPointIndex].direction == DirIndex:
                FoundLoop = True
                break

        
        if len(WalkedPoints) > 0:
            WalkedPoints.append(LoopPoint(Point(currentGuardPos.x, currentGuardPos.y), DirIndex))
        
        #if(NewObstaclePos == Point(3,6)):
            #PrintMapSection(MapData, currentGuardPos, range=Point(len(MapData[0]), len(MapData)), WalkedPoints=WalkedPoints, dirChar=DirChar[DirIndex], NewObstaclePos=NewObstaclePos)
        #PrintMapSection(MapData, currentGuardPos, range=Point(4,4), WalkedPoints=WalkedPoints, dirChar=DirChar[DirIndex % len(DirChar)])
        #input('Press any key for next frame')
    
    PrintMapSection(MapData, startPos=GuardPos, range=Point(len(MapData[0]), len(MapData)), WalkedPoints=WalkedPoints, NewObstaclePos=NewObstaclePos)
    return FoundLoop

def CountLoopingPaths(MapData:list[str], GuardPos:Point) -> int:
    count = 0
    for y, MapRow in enumerate(MapData):
        for x, MapChar in enumerate(MapRow):
            if MapChar == "#" or MapChar == "^" or MapChar == "\n": #Skip existing obstacles and start pos
                continue
            if PathLoops(MapData, GuardPos, Point(x,y)):    
                count += 1
    return count


if __name__ == "__main__":
    with open("./Day_6/InputData/Example.txt") as file:
        InputData:tuple[list[str],Point] = ParseInput(file)
        print(CountLoopingPaths(InputData[0], InputData[1]))
