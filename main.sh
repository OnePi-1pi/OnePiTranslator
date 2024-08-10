#!/bin/bash


SCRIPT_DIR="./scripts"


SCRIPT_FILE=$(find "$SCRIPT_DIR" -name 'onepitranslator.py*' | head -n 1)

if [ -z "$SCRIPT_FILE" ]; then
    echo "no such file"
    exit 1
fi


pythonw "$SCRIPT_FILE"&

exit 0
