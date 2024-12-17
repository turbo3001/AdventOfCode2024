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
    
    def __mul__(self, value):
        if not str(value).isnumeric():
            raise TypeError()
        return Point(self.x * value, self.y * value)
    
    def __repr__(self):
        return f"({self.x}, {self.y})"

class MapObject(Enum):
    WALL = auto()
    BOX = auto()
    AIR = auto()

class Robot:
    def __init__(self, Location:Point = Point(0,0), Program:str = ""):
        self.Location = Location
        self.Program = Program
        
class Warehouse:
    def __init__(self, WarehouseMap:list[list[MapObject]], WarehouseRobot:Robot):
        self.Map:list[list[MapObject]] = WarehouseMap
        self.Robot:Robot = WarehouseRobot    
    def __repr__(self):
        outputStr:str = ""
        for y, MapRow in enumerate(self.Map):
            for x, MapObject in enumerate(MapRow):
                if self.Robot.Location == Point(x,y):
                    outputStr += "@"
                else:
                    match MapObject:
                        case MapObject.WALL:
                            outputStr += "#"
                        case MapObject.BOX:
                            outputStr += "O"
                        case MapObject.AIR:
                            outputStr += "."
            outputStr += "\n"
        outputStr += f"\n{self.Robot.Program}"
        return outputStr
    
    def RunRobotProgram(self):
        MoveDirs:dict[str,Point] = {
            "<": Point(-1, 0),
            "^": Point( 0,-1),
            ">": Point( 1, 0),
            "v": Point( 0, 1)
        }
        for ProgramAction in self.Robot.Program:
            MoveDir = MoveDirs[ProgramAction]
            NewRobotPosition = self.Robot.Location + MoveDir
            NextMapObject:MapObject  = self.Map[NewRobotPosition.y][NewRobotPosition.x]
            if NextMapObject == MapObject.AIR:
                self.Robot.Location = NewRobotPosition
                continue
            if NextMapObject == MapObject.WALL:
                continue
            boxCount:int = 0
            NewBoxPosition = NewRobotPosition
            while NextMapObject == MapObject.BOX:
                NewBoxPosition += MoveDir
                NextMapObject = self.Map[NewBoxPosition.y][NewBoxPosition.x]
                boxCount += 1
            
            if NextMapObject == MapObject.AIR:
                self.Map[NewBoxPosition.y][NewBoxPosition.x] = MapObject.BOX
                self.Map[NewRobotPosition.y][NewRobotPosition.x] = MapObject.AIR
                self.Robot.Location = NewRobotPosition
            #print(self)
    
    def GetBoxGPS(self) -> list[int]:
        BoxGPS:list[int] = []
        for y, MapRow in enumerate(self.Map):
            for x, CurrentMapObject in enumerate(MapRow):
                if CurrentMapObject == MapObject.BOX:
                    BoxGPS.append((100*y)+x)
        return BoxGPS
        
def GetWarehouse(fileData:iter) -> Warehouse:
    WarehouseMap:list[list[MapObject]] = []
    WarehouseRobot:Robot = Robot()
    processingMap: bool = True
    for y, FileLine in enumerate(fileData):
        if FileLine == "\n":
            processingMap = False
            continue
        if processingMap:
            WarehouseMap.append([])
            for x, FileChar in enumerate(FileLine[:-1]): #exclude newline
                match FileChar:
                    case "@":
                        WarehouseRobot.Location.x = x
                        WarehouseRobot.Location.y = y
                        WarehouseMap[y].append(MapObject.AIR)
                    case "#":
                        WarehouseMap[y].append(MapObject.WALL)
                    case "O":
                        WarehouseMap[y].append(MapObject.BOX)
                    case ".":
                        WarehouseMap[y].append(MapObject.AIR)
                    case _:
                        raise Exception(f"Unknown Map Char {FileChar}")
        else:
            WarehouseRobot.Program += FileLine[:-1] #exclude newline
    return Warehouse(WarehouseMap, WarehouseRobot)

if __name__ == "__main__":
    with open("./Day_15/InputData/Input.txt") as file:
        CurrentWarehouse:Warehouse = GetWarehouse(file)
        #print(CurrentWarehouse)
        CurrentWarehouse.RunRobotProgram()
        print(sum(CurrentWarehouse.GetBoxGPS()))
