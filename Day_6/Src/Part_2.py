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
        return self.dirChar()#LoopDirChar[self.direction % len(LoopDirChar)]
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

def ListHasPoint(PointList:list[Point], PointToFind:Point) -> bool:
    for CurrentPoint in PointList:
        if CurrentPoint == PointToFind:
            return True
    return False

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
            if(x == NewObstaclePos.x and y == NewObstaclePos.y):
                printStr += "0"
            elif x == startPos.x and y == startPos.y:
                printStr += dirChar
            elif ListHasPoint(WalkedPoints, Point(x,y)):
                printStr += "X"
            else:
                printStr += MapChar
            x += 1
        printStr+="\n"
        x = initialX
        y += 1
    print(printStr)

def GetGuardPath(MapData:list[str], GuardPos:Point) -> list[Point]:
    WalkedPoints:list[Point] = [Point(GuardPos.x, GuardPos.y)]
    currentGuardPos:Point = Point(GuardPos.x, GuardPos.y)
    DirIndex:int = 0
    while True:
        currentDir = Dirs[DirIndex % len(Dirs)]
        currentGuardPos += currentDir
        if (currentGuardPos.y < 0 or
            currentGuardPos.x < 0 or
            currentGuardPos.y >= len(MapData) or
            currentGuardPos.x >= len(MapData[currentGuardPos.y])
            ):
            print(f"Exited at {currentGuardPos}")
            break

        if MapData[currentGuardPos.y][currentGuardPos.x] == "#":
            print(f"Hit wall at {currentGuardPos}")
            currentGuardPos -= currentDir
            DirIndex += 1
            continue

        if not ListHasPoint(WalkedPoints, currentGuardPos):
            WalkedPoints.append(Point(currentGuardPos.x, currentGuardPos.y))

    return WalkedPoints

def PathLoops(MapData:list[str], GuardPos:Point, NewObstaclePos:Point) -> bool:
    print(NewObstaclePos)
    WalkedPoints:list[Point] = []
    LoopPoints:list[LoopPoint] = []
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
            currentGuardPos -= currentDir
            DirIndex = (DirIndex + 1) % len(Dirs)
            if len(LoopPoints) == 0:
                LoopPoints.append(LoopPoint(Point(currentGuardPos.x, currentGuardPos.y), DirIndex))
                continue
        
        if len(LoopPoints) > 0:
            loopPointIndex = GetPointIndex(LoopPoints, LoopPoint(Point(currentGuardPos.x, currentGuardPos.y), DirIndex))
            if loopPointIndex >= 0:
                FoundLoop = True
                break
            LoopPoints.append(LoopPoint(Point(currentGuardPos.x, currentGuardPos.y), DirIndex))

        WalkedPoints.append(Point(currentGuardPos.x, currentGuardPos.y))
        
        # if(NewObstaclePos == Point(3,6)):
        #     PrintMapSection(MapData, currentGuardPos, range=Point(len(MapData[0]), len(MapData)), WalkedPoints=WalkedPoints, dirChar=GuardDirChar[DirIndex], NewObstaclePos=NewObstaclePos)
        #     input('Press any key for next frame')
        #PrintMapSection(MapData, currentGuardPos, range=Point(4,4), WalkedPoints=WalkedPoints, dirChar=DirChar[DirIndex % len(DirChar)])
    
    #PrintMapSection(MapData, startPos=GuardPos, range=Point(len(MapData[0]), len(MapData)), WalkedPoints=WalkedPoints, NewObstaclePos=NewObstaclePos)
    return FoundLoop

def CountLoopingPaths(MapData:list[str], GuardPos:Point) -> int:
    count = 0
    GuardPath:list[Point] = GetGuardPath(MapData, GuardPos)
    for Position in GuardPath[1:]:
        #print(f'Checking {Position}')
        if PathLoops(MapData, GuardPos, Position):
            count += 1
    return count


if __name__ == "__main__":
    with open("./Day_6/InputData/Input.txt") as file:
        InputData:tuple[list[str],Point] = ParseInput(file)
        print(CountLoopingPaths(InputData[0], InputData[1]))
