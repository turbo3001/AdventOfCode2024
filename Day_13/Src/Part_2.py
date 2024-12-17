from itertools import product
from enum import Enum, auto
from functools import cache

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
    
    def __hash__(self) -> int:
        return hash(str(self.x) + str(self.y))
    
    def __repr__(self):
        return f"({self.x}, {self.y})"
    
class ComboState(Enum):
    SHORT = auto()
    EXACT = auto()
    TOO_FAR = auto()
    
@cache
def GetCombosForNumPresses(NumPresses:int) -> list[tuple[int,int]]:
    Combos:list[tuple[int,int]] = []
    for i in range(NumPresses):
        Combos.append((i, NumPresses - i))
    return Combos

class Machine:
    def __init__(self, ButtonA:Point, ButtonB:Point, Prize:Point):
        self.ButtonA = ButtonA
        self.ButtonB = ButtonB
        self.Prize = Prize

    def __repr__(self):
        return f'<Button A: {self.ButtonA}\tButton B: {self.ButtonB}\tPrize: {self.Prize}>'
    
    @cache
    def isValidButtonCombo(self, ButtonCombo:tuple[int, int]) -> ComboState:
        currentPos:Point = Point(0,0) + (self.ButtonA * ButtonCombo[0]) + (self.ButtonB * ButtonCombo[1])
        if (currentPos.x > self.Prize.x or currentPos.y > self.Prize.y):
            return ComboState.TOO_FAR
        elif (currentPos == self.Prize):
            return ComboState.EXACT
        return ComboState.SHORT

    def GetMinCost(self) -> int:
        cost:int = -1
        numPresses:int = 1
        comboResults:list[bool] = [True]
        while cost < 0 and any(comboResults):
            comboResults.clear()
            for combination in GetCombosForNumPresses(numPresses):
                comboResult:ComboState = self.isValidButtonCombo(combination)
                comboResults.append(comboResult != ComboState.TOO_FAR)
                if comboResult == ComboState.EXACT:
                    cost = (combination[0] * 3) + combination[1]
                    break
            numPresses+=1
        return cost

        
def GetButtonPos(PosStr:str) -> Point:
    ButtonPos:Point = Point(0,0)
    SplitPosStr:list[str] = PosStr.split(",")
    for PosPart in SplitPosStr:
        SplitPosPart = PosPart.split("+")
        if SplitPosPart[0].strip() == "X":
            ButtonPos.x = int(SplitPosPart[1])
        else:
            ButtonPos.y = int(SplitPosPart[1])
    return ButtonPos

def GetPrizePos(PosStr:str) -> Point: #Why are these formatted differently :/
    PrizePos:Point = Point(0,0)
    SplitPosStr:list[str] = PosStr.split(",")
    for PosPart in SplitPosStr:
        SplitPosPart = PosPart.split("=")
        if SplitPosPart[0].strip() == "X":
            PrizePos.x = int(SplitPosPart[1]) + 10000000000000
        else:
            PrizePos.y = int(SplitPosPart[1]) + 10000000000000
    return PrizePos


def GetMachines(FileData:iter) -> list[Machine]:
    Machines:list[Machine] = []
    ButtonA:Point
    ButtonB:Point
    Prize:Point
    for Line in FileData:
        if Line == "\n":
            Machines.append(Machine(ButtonA, ButtonB, Prize))
            continue
        
        SplitLine:list[str] = Line.split(":")
        Type = SplitLine[0]
        Position = SplitLine[1]
        if Type.startswith("Button"):
            if Type.endswith("A"):
                ButtonA = GetButtonPos(Position)
            else:
                ButtonB = GetButtonPos(Position)
        else:
            Prize = GetPrizePos(Position)
    return Machines


if __name__ == "__main__":
    with open("./Day_13/InputData/Example.txt") as file:
        costSum = 0
        for CurrentMachine in GetMachines(file):
            print(f'Checking {CurrentMachine}')
            currentCost = CurrentMachine.GetMinCost()
            if currentCost > 0:
                costSum += currentCost
        print(costSum)
