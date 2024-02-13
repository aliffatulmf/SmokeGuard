@echo off
setlocal enabledelayedexpansion

set "folders[0]=hub"
set "folders[1]=utils"
set "folders[2]=models"

for /L %%i in (0,1,2) do (
  set "folder=!folders[%%i]!"
  if exist "!folder!" (
    @REM echo Deleting !folder!
    echo remove !folder!
    rmdir /S /Q "!folder!"
  ) else (
    echo folder !folder! not found.
  )
)

set "file=export.py"
if exist "!file!" (
  echo remove !folder!
  del /F /Q "!file!"
) else (
  echo file !file! not found.
)

endlocal
