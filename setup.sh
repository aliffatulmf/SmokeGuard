#!/bin/sh

if [ ! -d "hub" ]; then
    if ! command -v git &>/dev/null; then
        echo "git is not installed. Please install git before running this script."
        exit
    fi

    echo "Cloning to hub..."
    git clone https://github.com/ultralytics/yolov5.git hub
fi

if [ -d "utils" ]; then
    rm -rf utils
fi

if [ -d "models" ]; then
    rm -rf models
fi

if [ -f "export.py" ]; then
    rm export.py
fi

if [ ! -d "utils" ]; then
    cp -r hub/utils .
fi

if [ ! -d "models" ]; then
    cp -r hub/models .
fi

if [ ! -f "export.py" ]; then
    cp hub/export.py .
fi

echo "Done."
