from functools import cache

def GetNextStone(Stone:int) -> list[int]:
    NewStones:list[int] = []
    if Stone == 0:
        NewStones.append(1)
        return NewStones
    StrStone:str = str(Stone)
    if len(StrStone) % 2 == 0:
        midPoint:int = len(StrStone)//2
        NewStones.append(int(StrStone[:midPoint]))
        NewStones.append(int(StrStone[midPoint:]))
        return NewStones
    NewStones.append(Stone * 2024)
    return NewStones

@cache
def GetStoneCount(Stone:int, depth:int) -> int:
    if depth == 0:
        return 1
    count:int = 0
    NextStonesStep:list[int] = GetNextStone(Stone)
    for NextStone in NextStonesStep:
        count += GetStoneCount(NextStone, depth-1)
    return count

if __name__ == "__main__":
    with open("./Day_11/InputData/Input.txt") as file:
        Stones:list[int] = [int(Stone) for Stone in file.readline().split()]
        StoneCount = 0
        for Stone in Stones:
            StoneCount += GetStoneCount(Stone, 75)
        print(StoneCount)
        
