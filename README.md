# Different playbooks to automate environment preparation and Hortonworks Data Platform (HDP) prerequisite tools installation

## Datanode preparation
 - Usage: ```ansible-playbook datanode-preparation.yml -i ./inventory```
 
 The playbook will do the following:
* Install device mapper and perform a basic configuration
* Create blacklists for each datanode based on the desired number of hard-drives in order to exclude drives to be used by other datanodes
  (Use the ```jbod_hdds``` variable in the inventory file to setup the desired number of hard-drives for each single datanode)
* Run basic Healthcheck tests on the storage used by datanodes

## Prepare environment and install Ambari server
 - Usage: ```ansible-playbook install-ambari.yml -i ./inventory```

 The playbook will do the following:
* Install and start NTP server on all nodes in the cluster
* Stop firewall and disable SELinux
* Set a suitable UMASK value
* Set repositories for Ambari
* Download and install Ambari
* Performing a basic setup of Ambari (using Oracle JDK 8.0 and Embedded PostgreSQL database)
* Configure a passwordless ssh between all nodes in the cluster
* Start the Ambari server


## Remove all HDP components and reset cluster nodes
 - Usage: ```ansible-playbook cleanup-hdp.yml -i ./inventory```



# Hortonworks Data Platform (HDP) cluster installation using Ambari
Before proceeding with HDP cluster deployment, refer to the documents
* [Cluster Planning](https://docs.hortonworks.com/HDPDocuments/HDP2/HDP-2.6.4/bk_cluster-planning/bk_cluster-planning.pdf)
* [Apache Ambari Installation](https://docs.hortonworks.com/HDPDocuments/Ambari-2.6.1.0/bk_ambari-installation/bk_ambari-installation.pdf)
* [Apache Ambari Administration](https://docs.hortonworks.com/HDPDocuments/Ambari-2.6.1.0/bk_ambari-administration/bk_ambari-administration.pdf)


# Critical issues to consider (subject to further investigation)
Below are some of the critical issues that require careful planning
* Configuring Ambari in HA
* Planning a clean and safe procedure for node maintenance, service migration, services shutdown and cluster reboot
* Database selection for Ambari/ Hive/ Oozie
   - Ambari, Hive and Oozie need a database to operate (metastore). 
     - Ambari comes with its own built-in database (a PostgreSQL one), 
     - For Hive, the default database is MySQL that will be downloaded automatically by Ambari during cluster deployment
       - [JDBC connector must be configured](https://docs.hortonworks.com/HDPDocuments/Ambari-2.6.1.0/bk_ambari-administration/content/using_hive_with_mysql.html)
     - For Oozie, the default database is Derby that has an already integrated JDBC connector and need no further operations
   - For production grade HDP cluster, it is highly recommended to use external databases for the above services 
     that are configured in HA in order to guarantee business continuity 
* Service distribution between namenodes and datanodes. Frameworks such Hive, HBase, Spark, Kafka are resource-intensive and might
  require a careful planning while deployment (services to deploy on dedicated nodes, and other services to deploy on the same nodes in order to make 
  a better use of data-locality)



Refer to the [Apache Ambari Administration](https://docs.hortonworks.com/HDPDocuments/Ambari-2.6.1.0/bk_ambari-administration/bk_ambari-administration.pdf) for
further considerations to take into account in order to have a production grade HDP cluster 