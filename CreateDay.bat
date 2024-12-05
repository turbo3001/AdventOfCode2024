@echo off
set FolderName=.\Day_%1\
if exist %FolderName% (
    echo Folder %FolderName% already exists
    exit
)

xcopy /s .\TemplateDay\ %FolderName%