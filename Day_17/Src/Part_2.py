
class Computer:
    def __init__(self, ARegister:int, BRegister:int, CRegister:int, Program:list[int]):
        self.A:int = ARegister
        self.B:int = BRegister
        self.C:int = CRegister
        self.Program:list[int] = Program
        self.InstructionPointer:int = 0
        self.Output:list[int] = []

    def __repr__(self):
        return fr'''A-Register: {self.A}
B-Register: {self.B}
C-Register: {self.C}

InstructionPointer: {self.InstructionPointer}

Program: {self.Program}
Output:{self.GetOutput()}'''
    
    def GetOutput(self) -> str:
        return ",".join(str(out) for out in self.Output)
    
    def GetProgramString(self) -> str:
        return ",".join(str(instruction) for instruction in self.Program)

    def GetNextLiteralValue(self) -> int:
        operand:int = self.Program[self.InstructionPointer]
        self.InstructionPointer +=1
        return operand

    def GetComboOperandValue(self) -> int:
        operand:int = self.Program[self.InstructionPointer]
        self.InstructionPointer +=1
        if operand <= 3:
            return operand
        elif operand == 4:
            return self.A
        elif operand == 5:
            return self.B
        elif operand == 6:
            return self.C
        else:
            raise Exception(f"Invalid Operand {operand} in program at {self.InstructionPointer-1}")

    def adv(self, operand:int) -> None:
        numerator:int = self.A
        denominator:int= 2**operand
        self.A = numerator // denominator
    
    def bxl(self, operand:int) -> None:
        self.B = self.B ^ operand
    
    def bst(self, operand:int) -> None:
        self.B = operand % 8

    def jnz(self, operand:int) -> None:
        if self.A == 0:
            return
        self.InstructionPointer = operand
    
    def bxc(self, operand:int) -> None:
        self.B = self.B ^ self.C

    def out(self, operand:int) -> None:
        self.Output.append(operand%8)
    
    def bdv(self, operand:int) -> None:
        numerator:int = self.A
        denominator:int= 2**operand
        self.B = numerator // denominator

    def cdv(self, operand:int) -> None:
        numerator:int = self.A
        denominator:int= 2**operand
        self.C = numerator // denominator

    def StepProgram(self) -> None:
        opCode = self.GetNextLiteralValue()
        match opCode:
            case 0: #adv
                self.adv(self.GetComboOperandValue())
            case 1: #bxl
                self.bxl(self.GetNextLiteralValue())
            case 2: #bst
                self.bst(self.GetComboOperandValue())
            case 3: #jnz
                self.jnz(self.GetNextLiteralValue())
            case 4: #bxc
                self.bxc(self.GetNextLiteralValue())
            case 5: #out
                self.out(self.GetComboOperandValue())
            case 6: #bdv
                self.bdv(self.GetComboOperandValue())
            case 7: #cdv
                self.cdv(self.GetComboOperandValue())
            case _:
                raise Exception(f"Unknown Opcode {opCode}!")
        
    def RunProgram(self) -> list[int]:
        while CurrentComputer.InstructionPointer < len(CurrentComputer.Program):
            CurrentComputer.StepProgram()
        return CurrentComputer.Output
            
def GetComputer(FileData:iter) -> Computer:
    ARegister:int = 0
    BRegister:int = 0
    CRegister:int = 0
    Program:list[int] = []
    for FileLine in FileData:
        SplitLine = FileLine.split(":")
        if(len(SplitLine) < 2):
            continue
        match SplitLine[0]:
            case "Register A":
                ARegister = int(SplitLine[1])
            case "Register B":
                BRegister = int(SplitLine[1])
            case "Register C":
                CRegister = int(SplitLine[1])
            case "Program":
                Program = [int(i) for i in SplitLine[1].split(",")]
            case _:
                raise Exception("Invalid File Data!")
    return Computer(ARegister, BRegister, CRegister, Program)

if __name__ == "__main__":
    with open("./Day_17/InputData/Input.txt") as file:
        currentAReg:int = -1
        BaseComputer:Computer = GetComputer(file)
        CurrentComputer = Computer(currentAReg, BaseComputer.B, BaseComputer.C, BaseComputer.Program)
        ComputerOutput:list[int] = []
        while BaseComputer.Program != ComputerOutput:
            currentAReg += 1
            #print(CurrentComputer)
            ComputerOutput = CurrentComputer.RunProgram()
            #print(ComputerOutput)
            CurrentComputer = Computer(currentAReg, BaseComputer.B, BaseComputer.C, BaseComputer.Program)
        print(f'CorrectAReg: {currentAReg}')
