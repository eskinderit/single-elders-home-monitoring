## Getting started: install configuration
The steps that follow describe how to create and setup a Spark cluster using Vagrant and VirtualBox.
This is partially inspired by the guide [Spark Cluster with Virtual Box, Anaconda and Jupyter — The guide](https://blog.devgenius.io/spark-cluster-with-virtual-box-anaconda-and-jupyter-the-guide-dd0007cd5895)

### Prerequisites
1. virtualbox (tested with 7.0.16 r162802) and vagrant (tested with 2.4.1)
2. our vms with bootloaders [Download latest release here](https://github.com/eskinderit/single-elders-home-monitoring/releases)

# Base setup
In the following procedure we setup 3 nodes: 1(master,slave), 2(slave), 3(slave)
#### **For each node**
both *master* and *slaves*, follow the stesps below:

1. open the unix terminal or windows powershell in the VM vagrant folder (that is `spark-master`, `spark-slave-2` or `spark-slave-3`)
2. launch the VM: `vagrant up --provision`
3. login with ssh to the VM `vagrant ssh`. For the `spark-master` use also the command to simultaneously open the ports of the VM
to the host machine: `vagrant ssh -- -L 8888:localhost:8888 -L 18080:localhost:18080 -L 7077:localhost:7077 -L 8080:localhost:8080`
4. to test the connection between VMs, try to ssh each other, for instance we can launch `ssh spark-slave-2` from `spark-master` using the default password `vagrant`

#### On the `spark-master`
also follow the steps below:

1. Modify the slaves configuration:
```
cd $SPARK_HOME/conf 
sudo nano slaves 
#notice the 's' # add slave name from our network settings here 
spark-master 
spark-slave-2
spark-slave-3
```

2. Configure SSH connection between VMs
```
ssh-keygen

ssh-copy-id spark-master 
ssh-copy-id spark-slave-2
ssh-copy-id spark-slave-3
```
3. Create spark-logs folder to visualize the tasks dashboard:
``` 
sudo mkdir /spark-logs
sudo chmod -R 777 /spark-logs
```
4. Specify the position of the spark-logs folder to the general config of spark:
```
cd $SPARK_HOME/conf 
cp spark-defaults.conf.template spark-defaults.conf 
sudo nano spark-defaults.conf
 
# add these lines 
spark.eventLog.enabled true 
spark.eventLog.dir file:///spark-logs 
spark.history.fs.logDirectory file:///spark-logs
```
5. Try the configuration just set by running a sample py file:

Start the dashboard (you should be able to see it in the host machine at http://localhost:18080)
```
start-history-server.sh
```
Starting all the nodes:
```
start-all.sh
```
Submitting a sample job to the cluster just set:
```
cd $SPARK_HOME
spark-submit --master spark://spark-master:7077 ./examples/src/main/python/pi.py 10
```

# Set up HDFS

### Slaves (Datanodes) setup
This procedure has to be followed on the spark-slave-2 and spark-slave-3 VMs:

1. Copy as the content of the file `hdfs-site.xml` located in `/usr/local/hadoop-3.4.0/etc/hadoop`:
```
<configuration>
  <property>
    <name>dfs.replication</name>
    <value>2</value>
  </property>
  <property>
    <name>dfs.namenode.rpc-address</name>
    <value>spark-master:8020</value>
  </property>
  <property>
    <name>dfs.datanode.data.dir</name>
    <value>file:/hdfs/datanode</value>
  </property>
</configuration>
```
2. Copy as the content of the file `core-site.xml` located in `/usr/local/hadoop-3.4.0/etc/hadoop`:
```
<configuration>
  <property>
    <name>fs.defaultFS</name>
    <value>hdfs://spark-master:8020</value>
  </property>
</configuration>
```
3. create namenode and datanode hdfs directories
```
sudo mkdir -p /hdfs/datanode
sudo chmod -R 777 /hdfs/datanode
```
4. format namenode
```
sudo $HADOOP_HOME/bin/hadoop datanode -format
```
5. start namenode and datanode daemons, check status
```
sudo $HADOOP_HOME/bin/hdfs --daemon start datanode
sudo $HADOOP_HOME/bin/hdfs --daemon status datanode
```
### Master (Namenode + Datanode) setup
This procedure has to be followed on the spark-master VM:

1. Copy as the content of the file `hdfs-site.xml` located in `/usr/local/hadoop-3.4.0/etc/hadoop`:
```
<configuration>
  <property>
    <name>dfs.replication</name>
    <value>2</value>
  </property>
  <property>
    <name>dfs.namenode.rpc-address</name>
    <value>spark-master:8020</value>
  </property>
  <property>
    <name>dfs.namenode.name.dir</name>
    <value>file:/hdfs/namenode</value>
  </property>
  <property>
    <name>dfs.datanode.data.dir</name>
    <value>file:/hdfs/datanode</value>
  </property>
</configuration>
```
2. Copy as the content of the file `core-site.xml` located in `/usr/local/hadoop-3.4.0/etc/hadoop`:
```
<configuration>
  <property>
    <name>fs.defaultFS</name>
    <value>hdfs://spark-master:8020</value>
  </property>
</configuration>
```
3. create namenode and datanode hdfs directories
```
sudo mkdir -p /hdfs/datanode
sudo chmod -R 777 /hdfs/datanode

sudo mkdir -p /hdfs/namenode
sudo chmod -R 777 /hdfs/namenode
```
4. format namenode
```
sudo $HADOOP_HOME/bin/hadoop namenode -format
sudo $HADOOP_HOME/bin/hadoop datanode -format
```
5. start namenode and datanode daemons, check status
```
sudo $HADOOP_HOME/bin/hdfs --daemon start datanode
sudo $HADOOP_HOME/bin/hdfs --daemon status datanode
sudo $HADOOP_HOME/bin/hdfs --daemon start namenode
sudo $HADOOP_HOME/bin/hdfs --daemon status namenode
```
# Set up YARN
### Master (Resourcemanager + Nodemanager) setup
1. Modify the `yarn-site.xml` file located in `` to this:
```
<configuration>
  <property>
    <name>yarn.resourcemanager.hostname</name>
    <value>spark-master</value>
  </property>
  <property>
    <name>yarn.log-aggregation-enable</name>
    <value>true</value>
  </property>
</configuration>
```
2. run clustermanager and nodemanager daemons, check status
```
$HADOOP_HOME/bin/yarn --daemon start resourcemanager
$HADOOP_HOME/bin/yarn --daemon status resourcemanager

$HADOOP_HOME/bin/yarn --daemon start nodemanager
$HADOOP_HOME/bin/yarn --daemon status nodemanager
```
### Slaves (Nodemanager) setup
1. Modify the `yarn-site.xml` file located in `` to this:
```
<configuration>
  <property>
    <name>yarn.resourcemanager.hostname</name>
    <value>spark-master</value>
  </property>
  <property>
    <name>yarn.log-aggregation-enable</name>
    <value>true</value>
  </property>
</configuration>
```
2. run nodemanager daemons, check status
```
$HADOOP_HOME/bin/yarn --daemon start nodemanager
$HADOOP_HOME/bin/yarn --daemon status nodemanager
```

# Execute our pipeline
1. create a user folder on distributed file system
```
sudo $HADOOP_HOME/bin/hdfs dfs -mkdir -p /user/root/vagrant
```
2. grant access to the distributed filesystem to vagrant user:
```
sudo $HADOOP_HOME/bin/hdfs dfs -chown -R vagrant /
sudo $HADOOP_HOME/bin/hdfs dfs -chmod -R 700 /
```
3. move input csv to namenode hdfs
```
sudo $HADOOP_HOME/bin/hdfs dfs -put /vagrant/single-elders-home-monitoring/data/database_gas.csv /user/root/vagrant/database_gas.csv
```
4. move noise PCAModel to namenode hdfs
```
sudo $HADOOP_HOME/bin/hdfs dfs -put /vagrant/single-elders-home-monitoring/models/noisePCA /user/root/vagrant/noisePCA
```
5. submit our project pipeline 
```
spark-submit --master yarn /vagrant/single-elders-home-monitoring/event-recognition-pipeline.py 10
```

### To change configuration
- Follow and modify accordingly the procedure linked at the beginning of this section.
		

### Running PySpark on Jupyter Notebook
- to check that pyspark is correctly installed: launch `pyspark` and/or `spark-shell`
- to check what hdfs datanodes/namenodes are running: `$HADOOP_HOME/bin/hdfs dfsadmin -report`
- to close ssh user session launch `exit` 
- to switch off VM launch `vagrant halt` 
