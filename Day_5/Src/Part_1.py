
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
        if IsRowValid(PageData, InputData.Orderings):
            middleIndex = int(len(PageData)/2)
            ValidRows.append(PageData[middleIndex])
    return ValidRows

if __name__ == "__main__":
    with open("./Day_5/InputData/Input.txt") as file:
        InputData = ParseInput(file)
        print(sum(GetValidRowMiddleNumbers(InputData)))