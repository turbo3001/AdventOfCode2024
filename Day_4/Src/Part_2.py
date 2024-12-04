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


def FindXMAS(WordSearch:list[list[str]], x:int, y:int) -> bool:
    if (y < 1 or 
        x < 1 or 
        y+1 >= len(WordSearch) or
        x+1 >= len(WordSearch[y-1]) or
        x+1 >= len(WordSearch[y+1])):
        return False
    
    if (
        ((WordSearch[y-1][x-1] == "M" and WordSearch[y+1][x+1] == "S") or
        (WordSearch[y-1][x-1] == "S" and WordSearch[y+1][x+1] == "M")) and
        ((WordSearch[y-1][x+1] == "M" and WordSearch[y+1][x-1] == "S") or
        (WordSearch[y-1][x+1] == "S" and WordSearch[y+1][x-1] == "M"))
        ):
        return True



def CountWords(WordSearch:list[list[str]]) -> int:
    count = 0
    for y, Row in enumerate(WordSearch):
        for x, char in enumerate(Row):
            if char == "A":
                #print(f"A found at {y}, {x}")
                if(FindXMAS(WordSearch, x, y)):
                    print(f"X-MAS Found at {y}, {x}")
                    count += 1
    return count

if __name__ == "__main__":
    with open("./Day_4/InputData/Input.txt") as file:
        print(CountWords(GetWordSearch(file)))
