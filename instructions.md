# Spark VM Tutorial Steps (Standalone mode)
## initial setup
0. set virtualization on by BIOS and launch on unix terminal ```bcdedit /set hypervisorlaunchtype off```
1. install vagrant and virtualbox last versions
2. create a dedicated folder: ```mkdir BDAVM```

## initial-setup + everyday launch
3. mount the donwloaded setup: ```vagrant up --provision```
4. open port for jupyter notebook display: ```vagrant ssh -- -L 8888:localhost:8888```
5. launch jupyter notebook (with spark pre-enabled): ```/usr/local/spark-3.3.1-bin-hadoop3/bin/pyspark```
6. to close everything launch ```exit``` to switch off VM and ```vagrant halt``` to shutdown vagrant 

# Notes
- all 'mr' python files are prebuilt pipelines, run command example: 'cat ncdc | ./weather?mr?python.sh'
- all hadoop scripts specify inside what to use as a mapper and reducer (python), as input and as output. we call these scripts like ```./word_count_hadoop.sh```
- sometimes hadoop files need external arguments (such as the name of an external file, in the .sh $1$ is the first arg), we call these scripts like ``````

# other commands

- ```vagrant ssh``` to login to ubuntu-jammy
- ```exit``` to exit VM and ```vagrant halt``` to exit vagrant
- to restore sessions ```vagrant reload --provision```
- ```mc``` for file manager
