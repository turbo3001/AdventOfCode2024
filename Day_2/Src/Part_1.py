def ParseFloors(FloorData:iter) -> list[list[int]]:
    outputFloors = []
    for RawFloor in FloorData:
        currentFloor = [int(item) for item in RawFloor.split()]
        outputFloors.append(currentFloor)
    return outputFloors

def GetSafeFloorsCount(FloorData:list[list[int]]) -> int:
    count = 0
    for CurrentFloor in FloorData:
        lastDigit = CurrentFloor[0]
        lastDiff = 0
        isSafe = True
        for i in range(1,len(CurrentFloor)):
            currentDigit = CurrentFloor[i]
            diff = currentDigit - lastDigit
            absDiff = abs(diff)
            if absDiff < 1 or absDiff > 3:
                isSafe = False
                break
            if (diff * lastDiff) < 0:
                isSafe = False
                break
            lastDigit = currentDigit
            lastDiff = diff
        if isSafe:
            count += 1
    return count

if __name__ == "__main__":
    with open("./Day_2/InputData/Input.txt") as file:
        print(GetSafeFloorsCount(ParseFloors(file)))
