#!/bin/bash

folders=("hub" "utils" "models")

for folder in "${folders[@]}"; do
  if [ -d "$folder" ]; then
    echo "Delete $folder"
    rm -rf "$folder"
  fi
done


file="export.py"
if [ -f "$file" ]; then
  echo "Delete export.py"
  rm "$file"
fi
