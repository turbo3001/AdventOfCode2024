def ParseFloors(FloorData:iter) -> list[list[int]]:
    outputFloors = []
    for RawFloor in FloorData:
        currentFloor = [int(item) for item in RawFloor.split()]
        outputFloors.append(currentFloor)
    return outputFloors

def CompareLevels(currentLevel, LastLevel, lastDiff = 0) -> tuple[bool, int]:
    diff = currentLevel - LastLevel
    absDiff = abs(diff)
    if (diff * lastDiff) < 0:
        return (False, diff)
    if absDiff < 1 or absDiff > 3:
        return (False, diff)
    return (True, diff)

def IsFloorSafe(Floor:list[int], depth = 0) -> bool:
    if depth == 0 and not CompareLevels(Floor[0], Floor[1])[0]:
        return IsFloorSafe(Floor[1:])
    lastDigit = Floor[0]
    lastDiff = 0
    for i, currentDigit in enumerate(Floor):
        if i == 0: #skip the first element
            continue
        UnsafeLevel, lastDiff = CompareLevels(currentDigit, lastDigit, lastDiff)
        if not UnsafeLevel:
            if depth == 0:
                NewLevel = [digit for j, digit in enumerate(Floor) if j is not i]
                return IsFloorSafe(NewLevel, depth+1)
            else:
                return False
        lastDigit = currentDigit
    return True

def GetSafeFloorsCount(FloorData:list[list[int]]) -> int:
    count = 0
    for i, CurrentFloor in enumerate(FloorData):
        print(f'Checking Floor {i} ({CurrentFloor}):')
        if IsFloorSafe(CurrentFloor):
            #print(f'Floor {CurrentFloor} is safe')
            count += 1
        else:
            print(f'Floor {i} ({CurrentFloor}) is unsafe')
    return count

if __name__ == "__main__":
    with open("./Day_2/InputData/Input.txt") as file:
        print(GetSafeFloorsCount(ParseFloors(file)))
