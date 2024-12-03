import re

def GetMultiplyPairs(ProgramData:iter) -> tuple[list[int],list[int]]:
    regexStr = r"mul\((\d*,\d*)\)"
    xList = []
    yList = []
    for Line in ProgramData:
        for Match in re.findall(regexStr, Line):
            SplitMatch = Match.split(',')
            xList.append(int(SplitMatch[0]))
            yList.append(int(SplitMatch[1]))
    return(xList, yList)

if __name__ == "__main__":
    total = 0
    with open("./Day_3/InputData/Input.txt") as file:
        xList, yList = GetMultiplyPairs(file)
        for x,y in zip(xList, yList):
            total += x * y
    print(total)