# Different playbooks to automate environment preparation and Hortonworks Data Platform (HDP) prerequisite tools installation

## Datanode preparation
<<<<<<< HEAD
 - Usage: ```ansible-playbook datanode-preparation.yml -i ./inventory```
 
=======
 - Usage: ansible-playbook datanode-preparation.yml -i ./inventory
>>>>>>> 4f35fd0b63bb0c6f9b9f4e9ac69a50ce2421b7d8
 The playbook will do the following:
* Install device mapper and perform a basic configuration
* Create blacklists for each datanode based on the desired number of hard-drives in order to exclude drives to be used by other datanodes
* Run basic healthcheck tests on the storage used by datanodes

## Prepare environment and install Ambari server
<<<<<<< HEAD
 - Usage: ```ansible-playbook install-ambari.yml -i ./inventory```

=======
 - Usage: ansible-playbook install-ambari.yml -i ./inventory
>>>>>>> 4f35fd0b63bb0c6f9b9f4e9ac69a50ce2421b7d8
 The playbook will do the following:
* Install and start NTP server on all nodes in the cluster
* Stop firewall and disable SELinux
* Set a suitable UMASK value
* Set repositories for Ambari
* Download and install Ambari
* Performing a basic setup of Ambari (using Oracle JDK 8.0 and Embedded PostgreSQL database)
* Configure a passwordless ssh between all nodes in the cluster
* Start the Ambari server


<<<<<<< HEAD
## Remove all HDP components and reset cluster nodes
 - Usage: ```ansible-playbook cleanup-hdp.yml -i ./inventory```
=======
>>>>>>> 4f35fd0b63bb0c6f9b9f4e9ac69a50ce2421b7d8

