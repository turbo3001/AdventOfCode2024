
def StepStones(Stones:list[int]) -> list[int]:
    NewStones:list[int] = []
    for Stone in Stones:
        if Stone == 0:
            NewStones.append(1)
            continue
        StrStone:str = str(Stone)
        if len(StrStone) % 2 == 0:
            midPoint:int = len(StrStone)//2
            NewStones.append(int(StrStone[:midPoint]))
            NewStones.append(int(StrStone[midPoint:]))
            continue
        NewStones.append(Stone * 2024)
    return NewStones
        
        


if __name__ == "__main__":
    with open("./Day_11/InputData/Input.txt") as file:
        Stones:list[int] = [int(Stone) for Stone in file.readline().split()]
        #print(Stones)
        for i in range(25):
            Stones = StepStones(Stones)
            #print(Stones)
        print(len(Stones))
        
