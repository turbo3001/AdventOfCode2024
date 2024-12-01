def ParseLists(inputData:iter) -> tuple[list[int], list[int]]:
    leftList = []
    rightList = []
    for inputLine in inputData:
        splitLine = inputLine.split()
        leftList.append(int(splitLine[0]))
        rightList.append(int(splitLine[1]))
    return (leftList, rightList)

def GetDiffs(locationLists:tuple[list[int], list[int]]) -> list[int]:
    outputList: list[int] = []
    sortedLeft:list[int] = sorted(locationLists[0])
    sortedRight:list[int] = sorted(locationLists[1])
    for i in range(len(sortedLeft)):
        outputList.append(abs(sortedLeft[i]-sortedRight[i]))
    return outputList


if __name__ == "__main__":
    with open("./Day_1/InputData/Input.txt") as file:
        print(sum(GetDiffs(ParseLists(file))))