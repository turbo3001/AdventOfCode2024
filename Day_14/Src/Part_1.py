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

if __name__ == "__main__":
    with open("./Day_14/InputData/Input.txt") as file:
        (MapSize, Robots) = ParseInput(file)
        MidX:int = MapSize.x // 2
        MidY:int = MapSize.y // 2
        TopLeftCount:int = 0
        TopRightCount:int = 0
        BottomLeftCount:int = 0
        BottomRightCount:int = 0
        for CurrentRobot in Robots:
            NewRobotPosition:Point = CurrentRobot.Position + (CurrentRobot.Velocity * 100)
            NewRobotPosition.x = NewRobotPosition.x % MapSize.x
            NewRobotPosition.y = NewRobotPosition.y % MapSize.y
            if NewRobotPosition.x < MidX:
                if NewRobotPosition.y < MidY:
                    TopLeftCount += 1
                elif NewRobotPosition.y > MidY:
                    BottomLeftCount += 1
            elif NewRobotPosition.x > MidX:
                if NewRobotPosition.y < MidY:
                    TopRightCount += 1
                elif NewRobotPosition.y > MidY:
                    BottomRightCount += 1
        print(TopLeftCount * TopRightCount * BottomLeftCount * BottomRightCount)

