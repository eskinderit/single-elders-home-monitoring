#!/usr/bin/env bash

apt-get update
apt-get install -y python3 default-jre python3-pip
alias python=python3
add-apt-repository ppa:openjdk-r/ppa
apt-get update
apt-get install openjdk-11-jdk
# a simple two-panel file commander
apt-get install -y mc
# uncomment one of the following for graphical desktops
# NOTE: the graphical desktop is accessible through
# the main VirtualBox window (Show button)
#
# - minimal: wm & graphical server
# apt-get install -y icewm xinit xterm python3-tk
#
# - minimal desktop env: lxqt
# apt-get install -y xinit lxqt
#
# cd to the shared  directory
cd /vagrant
# python packages
pip3 install matplotlib pandas seaborn scikit-learn plotly scipy
# jupyter
pip3 install jupyter
# uncomment and modify to remove a previously installed Spark version
# rm -rf /usr/local/spark-3.0.0-preview2-bin-hadoop2.7
# remove any previously downloaded file
rm -rf spark-3.*-bin-hadoop*.tgz*
if ! [ -d /usr/local/spark-3.5.0-bin-hadoop3 ]; then
# current link as of 2023-11-24:
  wget https://archive.apache.org/dist/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz
  tar -C /usr/local -xvzf spark-3.5.0-bin-hadoop3.tgz
  rm spark-3.5.0-bin-hadoop3.tgz
fi

if ! [ -d /usr/local/hadoop-3.4.0 ]; then
  wget https://downloads.apache.org/hadoop/common/hadoop-3.4.0/hadoop-3.4.0.tar.gz
  tar -C /usr/local -xvzf hadoop-3.4.0.tar.gz
  rm hadoop-3.4.0.tar.gz
fi

if ! grep "export HADOOP_INSTALL=/usr/local/hadoop-3.4.0" /home/vagrant/.bashrc; then
  echo "export HADOOP_INSTALL=/usr/local/hadoop-3.4.0" >>  /home/vagrant/.bashrc
fi
if ! grep "export HADOOP_HOME=/usr/local/hadoop-3.4.0" /home/vagrant/.bashrc; then
  echo "export HADOOP_HOME=/usr/local/hadoop-3.4.0" >>  /home/vagrant/.bashrc
fi
if ! grep "export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64/" /home/vagrant/.bashrc; then
  echo "export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64/" >>  /home/vagrant/.bashrc
  echo "export PATH=$PATH:$JAVA_HOME/jre/bin" >>  /home/vagrant/.bashrc
fi
if ! grep "export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64/" /usr/local/hadoop-3.4.0/etc/hadoop/hadoop-env.sh; then
  echo "export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64/" >>  /usr/local/hadoop-3.4.0/etc/hadoop/hadoop-env.sh
fi
if ! grep "export HADOOP_MAPRED_HOME=/usr/local/hadoop-3.4.0" /home/vagrant/.bashrc; then
  echo "export HADOOP_MAPRED_HOME=/usr/local/hadoop-3.4.0" >>  /home/vagrant/.bashrc
fi
if ! grep "export PYSPARK_PYTHON=/usr/bin/python3" /home/vagrant/.bashrc; then
  echo "export PYSPARK_PYTHON=/usr/bin/python3" >>  /home/vagrant/.bashrc
fi
if ! grep "export PYSPARK_DRIVER_PYTHON=/usr/bin/python3" /home/vagrant/.bashrc; then
  echo "export PYSPARK_DRIVER_PYTHON=/usr/bin/python3" >>  /home/vagrant/.bashrc
fi
if ! grep "export SPARK_HOME=/usr/local/spark-3.5.0-bin-hadoop3" /home/vagrant/.bashrc; then
  echo "export SPARK_HOME=/usr/local/spark-3.5.0-bin-hadoop3" >>  /home/vagrant/.bashrc
  echo "export PATH=$PATH:/usr/local/spark-3.5.0-bin-hadoop3/bin:/usr/local/spark-3.5.0-bin-hadoop3/sbin" >>  /home/vagrant/.bashrc
fi


# setting up hostnames
echo "127.0.0.1 localhost
192.168.56.0 spark-master
192.168.56.1 spark-slave-2
192.168.56.2 spark-slave-3" > /etc/hosts

echo "## VM configuration completed ##"
