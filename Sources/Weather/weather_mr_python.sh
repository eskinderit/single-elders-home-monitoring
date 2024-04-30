#!/usr/bin/env bash
# to use this script, cat the dataset text files and pipe to
# std input of this script
# cat ncdc | weather_mr_python.sh
./mapper.py | sort | ./reducer.py | sort 
