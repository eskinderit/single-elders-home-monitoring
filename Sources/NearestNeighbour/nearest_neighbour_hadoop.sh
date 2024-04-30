#!/usr/bin/env bash
# Arguments can be passed to bash scripts by
# writing them, separated by spaces,
# after the script name and a space.
# They are referred to as $1, $2, ... .
# The $1 placeholder in the last line below
# is the value of the 1st argument to the script.
# Use it to pass an input file name, for example
# ./nearest_neighbour_set_hadoop.sh data.csv
rm -rf ./nearest_neighbour
$HADOOP_INSTALL/bin/hadoop jar \
$HADOOP_INSTALL/share/hadoop/tools/lib/hadoop-streaming-3.4.0.jar \
-files ./mapper.py,./reducer.py \
-mapper ./mapper.py \
-reducer ./reducer.py \
-input $1 -output ./nearest_neighbour
