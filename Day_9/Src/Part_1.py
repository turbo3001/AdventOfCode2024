from itertools import repeat

def PrintBlocks(Blocks:list[list[int]]) -> None:
    outputStr:str = ""
    for Block in Blocks:
        if len(Block) <= 0:
            continue
        for Data in Block:
            if Data < 0:
                outputStr += "."
            else:
                outputStr += str(Data)            
    print(outputStr)

def ParseBlocks(FileData:iter) -> list[list[int]]:
    BlockData = []
    for i in range(0,len(FileData),2):
        FileSize = int(FileData[i])
        BlockData.append([i//2 for j in range(FileSize)])
        if i+1 < len(FileData):
            SpaceSize = int(FileData[i+1])
            BlockData.append([-1 for j in range(SpaceSize)])
    return BlockData

def OrganiseBlocks(Blocks:list[list[int]]) -> None:
    writeBlockHead:int = 0
    for i in range(len(Blocks)-1, -1, -1):
        CurrentBlock:list[int] = Blocks[i]
        BlockSize:int = len(CurrentBlock)
        ReadHead:int = BlockSize-1
        if BlockSize <= 0: #skip 0-sized blocks
            continue
        if CurrentBlock[0] == -1: #skip empty blocks
            continue
        while ReadHead >= 0 and writeBlockHead < i:
            WriteBlock:list[int] = Blocks[writeBlockHead]
            if len(WriteBlock) <= 0: #skip 0-sized blocks
                writeBlockHead += 1
                continue
            for j, Data in enumerate(WriteBlock):
                if Data == -1:
                    WriteBlock[j] = CurrentBlock[ReadHead]
                    CurrentBlock[ReadHead] = -1
                    ReadHead -= 1
                    if ReadHead < 0:
                        writeBlockHead -= 1
                        break
            writeBlockHead += 1        


def CalculateChecksum(Blocks:list[list[int]]) -> int:
    sum:int = 0
    currentIndex:int = 0
    for Block in Blocks:
        for Data in Block:
            if Data == -1:
                continue
            sum += currentIndex * Data
            currentIndex +=1
    return sum

if __name__ == "__main__":
    with open("./Day_9/InputData/Input.txt") as file:
        Blocks = ParseBlocks(file.readline())
        OrganiseBlocks(Blocks)
        PrintBlocks(Blocks)
        print(CalculateChecksum(Blocks))
