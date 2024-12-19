from functools import cache

@cache
def IsPatternPossible(Pattern:str, TowelsStr:str) -> bool:
    Towels = TowelsStr.split(",")
    for Towel in Towels:
        if Pattern.startswith(Towel):
            subPattern = Pattern[len(Towel):]
            if len(subPattern) == 0 or IsPatternPossible(subPattern, TowelsStr):
                return True
    return False


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
            if IsPatternPossible(Pattern, TowelsStr):
                count += 1
        print(count)

