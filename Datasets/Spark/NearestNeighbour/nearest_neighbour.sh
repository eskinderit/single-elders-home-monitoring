#!/usr/bin/env bash
rm -rf output
$SPARK_INSTALL/bin/spark-submit --master local nearest_neighbour.py
