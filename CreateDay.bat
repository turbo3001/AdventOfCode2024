REM @echo off
set FolderName=Day_%1
set FolderPath=.\%FolderName%\
if exist %FolderPath% (
    echo Folder %FolderName% already exists
    exit
)

xcopy /s .\TemplateDay\ %FolderPath%
cd %FolderPath%Src
powershell -Command "(gc ./Part_1.py) -replace 'Day_X', '%FolderName%' | Out-File -encoding ASCII Part_1.py"