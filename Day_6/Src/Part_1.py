class Point:
    def __init__(self, x, y):
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

DirChar = ["^",">","v","<"]

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

def HasPoint(PointList:list[Point], PointToFind:Point):
    for CurrentPoint in PointList:
        if PointToFind == CurrentPoint:
            return True
    return False

def PrintMapSection(MapData:list[str], startPos:Point = Point(0,0), range:Point = Point(2,2), WalkedPoints:list[Point] = [], dirChar:str = DirChar[0]) -> None:
    x:int = startPos.x - range.x
    y:int = startPos.y - range.y
    if y < 0: y = 0
    if x < 0: x = 0
    initialX:int = x
    printStr:str = ""
    while y <= startPos.y + range.y and y < len(MapData):
        MapRow = MapData[y]
        while x <= startPos.x + range.x and x < len(MapRow):
            MapChar = MapRow[x]
            if x == startPos.x and y == startPos.y:
                printStr += dirChar
            elif HasPoint(WalkedPoints, Point(x, y)):
                printStr += "X"
            else:
                printStr += MapChar
            x += 1
        printStr += "\n"
        x = initialX
        y += 1
    print(printStr)

def WalkPath(MapData:list[str], GuardPos:Point) -> int:
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
        
        #PrintMapSection(MapData, currentGuardPos, range=Point(4,4), WalkedPoints=WalkedPoints, dirChar=DirChar[DirIndex % len(DirChar)])
        #input('Press any key for next frame')

        if not HasPoint(WalkedPoints, currentGuardPos):
            WalkedPoints.append(Point(currentGuardPos.x, currentGuardPos.y))
    
    #PrintMapSection(MapData, startPos=GuardPos, range=Point(len(MapData[0]), len(MapData)), WalkedPoints=WalkedPoints)

    return len(WalkedPoints)


if __name__ == "__main__":
    with open("./Day_6/InputData/Input.txt") as file:
        InputData:tuple[list[str],Point] = ParseInput(file)
        print(WalkPath(InputData[0], InputData[1]))
