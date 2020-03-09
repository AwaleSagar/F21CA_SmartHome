#!/bin/bash
echo "Please wait..."
eval "$(conda shell.bash hook)"
conda activate Alana
python bot.py
