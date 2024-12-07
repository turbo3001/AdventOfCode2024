
class LaunchManualUpdateData:
    def __init__(self):
        self.Orderings:list[tuple[int, int]] = []
        self.Pages:list[list[int]] = []

    def __str__(self) -> str:
        return f"""{self.Orderings}

{self.Pages}"""


def ParseOrdering(Line:str) -> tuple[int,int]:
    SplitLine:list[str] = Line.split("|", 1)
    return (int(SplitLine[0]), int(SplitLine[1]))

def ParsePages(Line:str) -> list[int]:
    return [int(item) for item in Line.split(",")]

def ParseInput(FileData:iter) -> LaunchManualUpdateData:
    inputData:LaunchManualUpdateData = LaunchManualUpdateData()
    for Line in FileData:
        if "|" in Line:
            inputData.Orderings.append(ParseOrdering(Line))
        elif "," in Line:
            inputData.Pages.append(ParsePages(Line))
    return inputData



def CorrectRow(PageData:list[int], Orderings:list[tuple[int,int]]) -> list[int]:
    correctedRow:list[int] = PageData.copy()
    isDirty:bool = True
    while isDirty:
        isDirty = False
        for Ordering in Orderings:
            try:
                HasPageIndex = correctedRow.index(Ordering[1])
                try:
                    MustHavePageIndex = correctedRow.index(Ordering[0])
                except ValueError:
                    continue
                else:
                    if HasPageIndex < MustHavePageIndex:
                        tempPage:int = correctedRow.pop(MustHavePageIndex)
                        correctedRow.insert(HasPageIndex, tempPage)
                        isDirty = True
            except:
                continue
    return correctedRow

def IsRowValid(PageData:list[int], Orderings:list[tuple[int, int]]) -> bool:
    for Ordering in Orderings:
        try:
            HasPageIndex = PageData.index(Ordering[1])
            try:
                MustHavePageIndex = PageData.index(Ordering[0])
            except ValueError:
                continue
            else:
                if HasPageIndex < MustHavePageIndex:
                    return False
        except:
            continue
    return True


def GetValidRowMiddleNumbers(InputData:LaunchManualUpdateData) -> list[int]:
    ValidRows:list[int] = []
    for PageData in InputData.Pages:
        if not IsRowValid(PageData, InputData.Orderings):
            middleIndex:int = int(len(PageData)/2)
            correctedRow:list[int] = CorrectRow(PageData, InputData.Orderings)
            print(correctedRow)
            ValidRows.append(correctedRow[middleIndex])
    return ValidRows

if __name__ == "__main__":
    with open("./Day_5/InputData/Input.txt") as file:
        InputData:LaunchManualUpdateData = ParseInput(file)
        middleNumbers:list[int] = GetValidRowMiddleNumbers(InputData)
        print(f'Middle Numbers: {middleNumbers}')
        print(sum(middleNumbers))