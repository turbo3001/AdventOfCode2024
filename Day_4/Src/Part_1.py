from enum import Enum, auto

def GetWordSearch(FileData:iter) -> list[list[str]]:
    WordSearch = []
    for Line in FileData:
        LineData = []
        for Char in Line:
            if(Char == "\n"): continue
            LineData.append(Char)
        WordSearch.append(LineData)
    return WordSearch


def CheckDir(XDir:int, YDir:int, WordSearch:list[list[str]], x:int, y:int, WordToFind:str) -> bool:
    WordLength:int = len(WordToFind)-1
    if ((XDir < 0 and x < WordLength) or
        (YDir < 0 and y < WordLength)):
        return False
    
    for i, FindChar in enumerate(WordToFind):
        NewX = x + (i * XDir)
        NewY = y + (i * YDir)
        if NewY > len(WordSearch)-1 or NewX > len(WordSearch[NewY])-1:
            return False
        if WordSearch[NewY][NewX] != FindChar:
            return False
    return True

def GetDirName(xDir:int, yDir:int) -> str:
    Name:str = ""
    if(yDir < 0):
        Name = "Up"
    elif(yDir > 0):
        Name = "Down"
    
    if xDir != 0 and len(Name) > 0:
        Name += " and "

    if(xDir < 0):
        Name += "to the Left"
    elif(xDir > 0):
        Name += "to the Right"
    
    return Name


def CountWords(WordSearch:list[list[str]], WordToFind:str) -> int:
    count = 0
    for y, Row in enumerate(WordSearch):
        for x, char in enumerate(Row):
            if char == WordToFind[0]:
                #print(f"First Char ({WordToFind[0]}) found at {x}, {y}")
                for yDir in range(-1,2):
                    for xDir in range(-1,2):
                        if yDir == 0 and xDir == 0:
                            continue
                        if(CheckDir(xDir, yDir, WordSearch, x, y, WordToFind)):
                            print(f"Word Found at {x}, {y} Heading {GetDirName(xDir, yDir)}")
                            count += 1
    return count

if __name__ == "__main__":
    with open("./Day_4/InputData/Input.txt") as file:
        print(CountWords(GetWordSearch(file), "XMAS"))
