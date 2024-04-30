# WORK in PROGRESS
# if the environment variable HADOOP_INSTALL
# is set, change the current directory to it
# pushd remembers the path of visited directories
pushd $HADOOP_INSTALL
# the bin folder in $HADOOP_INSTALL
# contains Hadoop programs
ls bin
# hdfs manages the distributed filesystem HDFS
bin/hdfs version
# list the content of the root directory
# of the HDFS distributed file system
bin/hdfs dfs -ls /
# show the contents of a file in hdfs
bin/hdfs dfs -cat /chaucer.txt
# copy a file from the local file system to
# the distributed file system
bin/hdfs dfs -put ~/chaucer.txt /chaucer.txt
# copy the contents of a file in HDFS to the local
# file system
bin/hdfs dfs -get /chaucer.txt ~
