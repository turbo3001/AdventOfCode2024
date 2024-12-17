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
    
    def __mul__(self, value):
        if not str(value).isnumeric():
            raise TypeError()
        return Point(self.x * value, self.y * value)
    
    def __repr__(self):
        return f"({self.x}, {self.y})"

class Robot:
    def __init__(self, Position:Point, Velocity:Point):
        self.Position:Point = Position
        self.Velocity:Point = Velocity

    def __repr__(self):
        return f'p={self.Position} v={self.Velocity}'
        
def GetPointFromStr(PointStr:str) -> Point:
    SplitStr:list[str] = PointStr.split(",")
    x:int = int(SplitStr[0][2:])
    y:int = int(SplitStr[1])
    return Point(x,y)


def ParseInput(FileData:iter) -> tuple[Point, list[Robot]]:
    MapSize:Point = Point(0,0)
    Robots:list[Robot] = []
    for i, FileRow in enumerate(FileData):
        if i == 0: #MY_MOD: Prepended Map Size as first row
            SplitLine = FileRow.split(",")
            MapSize.y = int(SplitLine[0])
            MapSize.x = int(SplitLine[1])
            continue
        SplitLine = FileRow.split()
        Position:Point = GetPointFromStr(SplitLine[0])
        Velocity:Point = GetPointFromStr(SplitLine[1])
        Robots.append(Robot(Position, Velocity))      
    return(MapSize, Robots)

def ListHasRobotAtPoint(Location:Point, RobotList:list[Robot]) -> bool:
    for CurrentRobot in RobotList:
        if CurrentRobot.Position == Location:
            return True
    return False

def HasChristmasTree(MapSize:Point, RobotList:list[Robot]) -> bool:
    MidX:int = MapSize.x // 2
    for y in range(MapSize.y):
        
        for x in range(y+1):
            XOffset = x - (y//2)
            XPos = MidX + XOffset
            Location:Point = Point(XPos,y)
            if not ListHasRobotAtPoint(Location, RobotList):
                return False
    return True

def PrintMap(MapSize:Point, RobotList:list[Robot]) -> None:
    outputStr:str = ""
    for y in range(MapSize.y):
        for x in range(MapSize.x):
            if ListHasRobotAtPoint(Point(x,y), RobotList):
                outputStr += "X"
            else:
                outputStr += "."
        outputStr += "\n"
    print(outputStr)


if __name__ == "__main__":
    with open("./Day_14/InputData/Example.txt") as file:
        (MapSize, Robots) = ParseInput(file)
        treeFound:bool = False
        time:int = 0
        while not treeFound:
            time += 1
            for CurrentRobot in Robots:
                CurrentRobot.Position += CurrentRobot.Velocity
                CurrentRobot.Position.x %= MapSize.x
                CurrentRobot.Position.y %= MapSize.y
            PrintMap(MapSize, Robots)
            treeFound = HasChristmasTree(MapSize, Robots)
        print(time)

