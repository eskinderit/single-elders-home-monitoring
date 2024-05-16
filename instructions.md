## Getting started: install configuration
The steps that follow describe how to create and setup a Spark cluster using Vagrant and VirtualBox.
This is partially inspired by the guide [Spark Cluster with Virtual Box, Anaconda and Jupyter — The guide](https://blog.devgenius.io/spark-cluster-with-virtual-box-anaconda-and-jupyter-the-guide-dd0007cd5895)

### Prerequisites
virtualbox (tested with 7.0.16 r162802) and vagrant (tested with 2.4.1)

### Base setup
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
spark-submit --master spark://spark-master:7077 ./examples/src/main/python/pi.py 10
```

### To change configuration
- Follow and modify accordingly the procedure linked at the beginning of this section.
		

### Running PySpark on Jupyter Notebook
- to check that pyspark is correctly installed: launch `pyspark` and/or `spark-shell`
- to close ssh user session launch `exit` 
- to switch off VM launch `vagrant halt` 
