#!/usr/bin/env bash
# to use this script, cat the dataset text files and pipe to
# std input of this script
# cat chaucer.txt | word_count_mr_python.sh
./mapper.py | sort -k 1 | ./reducer.py 
