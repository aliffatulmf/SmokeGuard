@echo off

if not exist hub (
    echo Cloning to hub...
    git clone https://github.com/ultralytics/yolov5.git hub
)

if exist utils (
    rd /s /q utils
)

if exist models (
    rd /s /q models
)

if exist export.py (
    del export.py
)

if not exist utils (
    move /Y hub\utils .
)

if not exist models (
    move /Y hub\models .
)

if not exist export.py (
    move /Y hub\export.py .
)

echo Done.
