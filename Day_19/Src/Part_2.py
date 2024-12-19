from functools import cache

@cache
def GetPossibleCombinations(Pattern:str, TowelsStr:str) -> int:
    count = 0
    Towels = TowelsStr.split(",")
    for Towel in Towels:
        if Pattern == Towel:
            count += 1
        elif Pattern.startswith(Towel):
            subPattern = Pattern[len(Towel):]
            count += GetPossibleCombinations(subPattern, TowelsStr)
    return count


def ParseInput(FileData:iter) -> tuple[list[str], list[str]]:
    Towels:list[str] = []
    TowelPatterns:list[str] = []
    for FileLine in FileData:
        LineData:str = FileLine.strip()
        if len(LineData) == 0:
            continue

        if "," in LineData:
            Towels += [ Towel.strip() for Towel in LineData.split(",")]
            continue
        TowelPatterns.append(LineData)
    return (Towels, TowelPatterns)


if __name__ == "__main__":
    with open("./Day_19/InputData/Input.txt") as file:
        Towels, Patterns = ParseInput(file)
        Towels.sort(key=lambda Towel: len(Towel))
        Patterns.sort(key=lambda Pattern: len(Pattern))
        TowelsStr = ','.join(Towels)
        count:int = 0
        for Pattern in Patterns:
            count += GetPossibleCombinations(Pattern, TowelsStr)
        print(count)

