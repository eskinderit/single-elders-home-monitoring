#!/usr/bin/env bash
rm -rf ./nearest_neighbour_set
$HADOOP_INSTALL/bin/hadoop jar \
$HADOOP_INSTALL/share/hadoop/tools/lib/hadoop-streaming-3.4.0.jar \
-files ./mapper.py,./reducer.py \
-mapper 'python3 ./mapper.py ./query_points.csv' \
-reducer ./reducer.py \
-input ./spline_boundary_enum_inputs.csv -output ./nearest_neighbour_set
