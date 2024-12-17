from enum import Enum, auto
class Point:
    def __init__(self, x:int, y:int):
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
    
    def copy(other):
        if not isinstance(other, Point):
            raise TypeError()
        return Point(other.x, other.y)

class MapObject(Enum):
    WALL = auto()
    BOX_LEFT_SIDE = auto()
    BOX_RIGHT_SIDE = auto()
    AIR = auto()

def IsBox(Value:MapObject) -> bool:
    return Value == MapObject.BOX_LEFT_SIDE or Value == MapObject.BOX_RIGHT_SIDE

class Robot:
    def __init__(self, Location:Point = Point(0,0), Program:str = ""):
        self.Location = Location
        self.Program = Program
        
class Warehouse:
    def __init__(self, WarehouseMap:list[list[MapObject]], WarehouseRobot:Robot):
        self.Map:list[list[MapObject]] = WarehouseMap
        self.Robot:Robot = WarehouseRobot
        self.MoveDirs:dict[str,Point] = {
            "<": Point(-1, 0),
            "^": Point( 0,-1),
            ">": Point( 1, 0),
            "v": Point( 0, 1)
        } 
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
                        case MapObject.BOX_LEFT_SIDE:
                            outputStr += "["
                        case MapObject.BOX_RIGHT_SIDE:
                            outputStr += "]"
                        case MapObject.AIR:
                            outputStr += "."
            outputStr += "\n"
        outputStr += f"\n{self.Robot.Program}"
        return outputStr
    
    def pushBox(self, BoxPosition:Point, ProgramAction:str) -> Point:
        NextMapObject:MapObject  = self.Map[BoxPosition.y][BoxPosition.x]
        if ProgramAction == "<" or ProgramAction == ">":
            if IsBox(NextMapObject):
                if ProgramAction == "<":
                    BoxPosition.x -= 1
                else:
                    BoxPosition.x += 1
                return self.pushBox(BoxPosition, ProgramAction)
            elif NextMapObject == MapObject.AIR:
                if ProgramAction == "<":
                    AirDistance = self.Robot.Location.x - BoxPosition.x
                else:
                    AirDistance = BoxPosition.x - self.Robot.Location.x
                
                NextBoxPos = Point.copy(BoxPosition)
                while AirDistance > 1:
                    NextBoxPos.x += 1 if ProgramAction == "<" else -1
                    self.Map[BoxPosition.y][BoxPosition.x] = self.Map[NextBoxPos.y][NextBoxPos.x]
                    BoxPosition.x += 1 if ProgramAction == "<" else -1
                    AirDistance -= 1
                self.Map[BoxPosition.y][BoxPosition.x] = MapObject.AIR
                return BoxPosition
        else: # ^ or v
            BoxOtherHalf:Point = Point.copy(BoxPosition)
            if NextMapObject == MapObject.BOX_LEFT_SIDE:
                BoxOtherHalf.x += 1
            else:
                BoxOtherHalf.x -= 1
            if self.pushBox(BoxOtherHalf, ProgramAction) == self.Robot.Location:
                return self.Robot.Location

            if IsBox(NextMapObject):
                if ProgramAction == "^":
                    BoxPosition.y -= 1
                else:
                    BoxPosition.y += 1
                return self.pushBox(BoxPosition, ProgramAction)
            elif NextMapObject == MapObject.AIR:
                if ProgramAction == "v":
                    AirDistance = self.Robot.Location.y - BoxPosition.y
                    WriteOrder = [MapObject.BOX_RIGHT_SIDE, MapObject.BOX_LEFT_SIDE]
                else:
                    AirDistance = BoxPosition.y - self.Robot.Location.y
                    WriteOrder = [MapObject.BOX_LEFT_SIDE, MapObject.BOX_RIGHT_SIDE]
                
                while AirDistance > 1:
                    self.Map[BoxPosition.y][BoxPosition.x] = WriteOrder[AirDistance%2]
                    if ProgramAction == "v":
                        BoxPosition.x += 1
                    else:
                        BoxPosition.x -= 1
                    AirDistance -= 1
                self.Map[BoxPosition.y][BoxPosition.x] = MapObject.AIR
                return BoxPosition
                

        # NewBoxPosition = NewRobotPosition
        # if ProgramAction == "<" or ProgramAction == ">":        
        #     boxCount:int = 0
        #     while NextMapObject == MapObject.BOX_LEFT_SIDE or NextMapObject == MapObject.BOX_RIGHT_SIDE:
        #         NewBoxPosition += MoveDir * 2
        #         NextMapObject = self.Map[NewBoxPosition.y][NewBoxPosition.x]
        #         boxCount += 1
            
        #     if NextMapObject == MapObject.AIR:
        #         while boxCount > 0:
        #             boxLeft = NewBoxPosition.x
        #             boxRight = NewBoxPosition.x
        #             if ProgramAction == "<":
        #                 boxLeft -= boxCount*2
        #                 boxRight = boxLeft + 1
        #             else:
        #                 boxRight += boxCount*2
        #                 boxLeft = boxRight - 1

        #             self.Map[NewBoxPosition.y][boxLeft] = MapObject.BOX_LEFT_SIDE
        #             self.Map[NewBoxPosition.y][boxRight] = MapObject.BOX_RIGHT_SIDE
        #             boxCount -= 1

        #         self.Map[NewRobotPosition.y][NewRobotPosition.x] = MapObject.AIR
        #         self.Robot.Location = NewRobotPosition
        #     return

        # foundBoxes:list[Point] = []
        return self.Robot.Location

    def stepProgram(self, ProgramCounter:int):
        ProgramAction:str = self.Robot.Program[ProgramCounter]
        MoveDir = self.MoveDirs[ProgramAction]
        NewRobotPosition = self.Robot.Location + MoveDir
        NextMapObject:MapObject  = self.Map[NewRobotPosition.y][NewRobotPosition.x]
        if NextMapObject == MapObject.AIR:
            self.Robot.Location = NewRobotPosition
            return
        if NextMapObject == MapObject.WALL:
            return
        if IsBox(NextMapObject):
            self.Robot.Location = self.pushBox(NewRobotPosition, ProgramAction)


    def RunRobotProgram(self):
        for i in range(len(self.Robot.Program)):
            self.stepProgram(i)
            print(self)
            input()
    
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
                        WarehouseRobot.Location.x = x*2
                        WarehouseRobot.Location.y = y
                        WarehouseMap[y].append(MapObject.AIR)
                        WarehouseMap[y].append(MapObject.AIR)
                    case "#":
                        WarehouseMap[y].append(MapObject.WALL)
                        WarehouseMap[y].append(MapObject.WALL)
                    case "O":
                        WarehouseMap[y].append(MapObject.BOX_LEFT_SIDE)
                        WarehouseMap[y].append(MapObject.BOX_RIGHT_SIDE)
                    case ".":
                        WarehouseMap[y].append(MapObject.AIR)
                        WarehouseMap[y].append(MapObject.AIR)
                    case _:
                        raise Exception(f"Unknown Map Char {FileChar}")
        else:
            WarehouseRobot.Program += FileLine[:-1] #exclude newline
    return Warehouse(WarehouseMap, WarehouseRobot)

if __name__ == "__main__":
    with open("./Day_15/InputData/Example3.txt") as file:
        CurrentWarehouse:Warehouse = GetWarehouse(file)
        print(CurrentWarehouse)
        CurrentWarehouse.RunRobotProgram()
        #print(sum(CurrentWarehouse.GetBoxGPS()))
