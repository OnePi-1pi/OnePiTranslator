#!/bin/bash
SCRIPT_DIR="./src"


SCRIPT_FILE=$(find "$SCRIPT_DIR" -name 'onepitranslator.py*' | head -n 1)

if [ -z "$SCRIPT_FILE" ]; then
    echo "no such file"
    echo $SCRIPT_FILE
    exit 1
fi


python3 "$SCRIPT_FILE"&

exit 0
