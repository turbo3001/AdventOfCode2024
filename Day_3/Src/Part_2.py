import re

def GetMultiplyPairs(ProgramData:iter) -> tuple[list[int],list[int]]:
    regexStr = r"mul\((\d*,\d*)\)|(do\(\))|(don\'t\(\))"
    xList = []
    yList = []
    enabled = True
    for Line in ProgramData:
        for Match in re.findall(regexStr, Line):
            if Match[1] == "do()" or Match[2] == "don't()":
                enabled = Match[1] == "do()"
            elif enabled:
                SplitMatch = Match[0].split(',')
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