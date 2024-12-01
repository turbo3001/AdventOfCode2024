def ParseLists(inputData:iter) -> tuple[list[int], list[int]]:
    leftList = []
    rightList = []
    for inputLine in inputData:
        splitLine = inputLine.split()
        leftList.append(int(splitLine[0]))
        rightList.append(int(splitLine[1]))
    return (leftList, rightList)

def GetSimilarityScores(locationLists:tuple[list[int], list[int]]) -> list[int]:
    outputList: list[int] = []
    sortedLeft:list[int] = sorted(locationLists[0])
    sortedRight:list[int] = sorted(locationLists[1])
    for leftID in sortedLeft:
        similarityScore = 0
        for rightID in sortedRight:
            if(rightID == leftID):
                similarityScore += leftID
        outputList.append(similarityScore)
    return outputList


if __name__ == "__main__":
    with open("./Day_1/InputData/Input.txt") as file:
        print(sum(GetSimilarityScores(ParseLists(file))))