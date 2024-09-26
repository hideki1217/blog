#!/bin/bash

if ! type uv > /dev/null; then
    echo "ERROR: 'uv' command is not found"
    exit 1
else 
    echo "INFO: 'uv' command is found"
fi

if [ -d .venv ]; then
    echo "INFO: './.venv' folder is found, and removing it."
    rm -rf .venv
fi

echo "INFO: It starts to create venv"
echo ""

uv venv .venv
uv pip install -r ./scripts/requirements.txt

echo ""
echo "INFO: Success"