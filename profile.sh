#!/bin/sh
python3.4 -m cProfile -o cli.prof cli.py /Users/andre/git/MPAndroidChart 100 method
snakeviz cli.prof
