#!/usr/bin/env bash
rm -rf output
$SPARK_INSTALL/bin/spark-submit --master local word_count.py
