from enum import Enum,auto
from itertools import product

class Operators(Enum):
    PLUS = auto()
    MULTIPLY = auto()
    CONCAT = auto()
    def __repr__(self):
        match self:
            case Operators.PLUS:
                return "+"
            case Operators.MULTIPLY:
                return "*"
            case Operators.CONCAT:
                return "||"
            case _:
                return "UNKNOWN OPERATOR"

class EquationInputs:
    def __init__(self, result:int, operands:list[int]):
        self.result:int = result
        self.operands:list[int] = operands
        self.validCount:None|int = None
    def __repr__(self) -> str:
        return f'[{self.result}: {" ".join([str(x) for x in self.operands])}]'
    def CalculateValidity(self):
        #print(f"Calculating Validity for {self}")
        self.validCount = 0
        for operatorList in product(Operators, repeat=len(self.operands)-1):
            #print(f'{self} - {operatorList}')
            result = self.operands[0]
            for i in range(0, len(operatorList)):
                if result > self.result:
                    break
                match operatorList[i]:
                    case Operators.PLUS:
                        result += self.operands[i+1]
                    case Operators.MULTIPLY:
                        result *= self.operands[i+1]
                    case Operators.CONCAT:
                        result = int(str(result) + str(self.operands[i+1]))
            if result == self.result:
                print(f'{self} - Valid result found {operatorList}')
                self.validCount += 1
        return self.validCount
    def ValidCount(self) -> int:
        if self.validCount != None:
            return self.validCount
        else:
            return self.CalculateValidity()

def ParseInput(FileData:iter) -> list[EquationInputs]:
    inputs:list[EquationInputs] = []
    for FileLine in FileData:
        splitLine = FileLine.split(":")
        result:int = int(splitLine[0])
        operands:list[int] = [int(item) for item in splitLine[1].split()]
        inputs.append(EquationInputs(result, operands))
    return inputs
        
def GetEquationsSum(Equations:list[EquationInputs]) -> int:
    sum:int = 0
    for Equation in Equations:
        if Equation.ValidCount() > 0:
            sum += Equation.result
    return sum

if __name__ == "__main__":
    with open("./Day_7/InputData/Input.txt") as file:
        print(GetEquationsSum(ParseInput(file)))
