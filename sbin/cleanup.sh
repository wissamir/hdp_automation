#!/bin/bash
# Reference: https://community.hortonworks.com/articles/97489/completely-uninstall-hdp-and-ambari.html

# Stop all services in Ambari or kill them.
ps fax | grep hdfs | awk '{print $1}' | xargs kill -9

# Run python script on all cluster nodes
python /usr/lib/python2.6/site-packages/ambari_agent/HostCleanup.py --silent --skip=users

# Remove Hadoop packages on all nodes
yum remove -y hive\*
yum remove -y oozie\*
yum remove -y pig\*
yum remove -y zookeeper\*
yum remove -y tez\*
yum remove -y hbase\*
yum remove -y ranger\*
yum remove -y knox\*
yum remove -y storm\*
yum remove -y accumulo\*
yum remove -y falcon\*
yum remove -y ambari-metrics-hadoop-sink 
yum remove -y smartsense-hst
yum remove -y slider_2_4_2_0_258
yum remove -y ambari-metrics-monitor
yum remove -y spark2_2_5_3_0_37-yarn-shuffle
yum remove -y spark_2_5_3_0_37-yarn-shuffle
yum remove -y ambari-infra-solr-client

# Remove ambari-server (on ambari host) and ambari-agent (on all nodes) - if run with ansible, remember to add ignore_errors as ambari-server does exist on datanodes
ambari-server stop
ambari-agent stop
yum erase -y ambari-server
yum erase -y ambari-agent

# Remove repositories on all nodes
rm -rf /etc/yum.repos.d/ambari* /etc/yum.repos.d/HDP*
yum clean all

# Remove log folders on all nodes
rm -rf /var/log/ambari-agent
rm -rf /var/log/ambari-metrics-grafana
rm -rf /var/log/ambari-metrics-monitor
rm -rf /var/log/ambari-server/
rm -rf /var/log/falcon
rm -rf /var/log/flume
rm -rf /var/log/hadoop
rm -rf /var/log/hadoop-mapreduce
rm -rf /var/log/hadoop-yarn
rm -rf /var/log/hive
rm -rf /var/log/hive-hcatalog
rm -rf /var/log/hive2
rm -rf /var/log/hst
rm -rf /var/log/knox
rm -rf /var/log/oozie
rm -rf /var/log/solr
rm -rf /var/log/zookeeper

# Remove Hadoop folders including HDFS data on all nodes
rm -rf /hadoop/*
rm -rf /hdfs/hadoop
rm -rf /hdfs/lost+found
rm -rf /hdfs/var
rm -rf /local/opt/hadoop
rm -rf /tmp/hadoop
rm -rf /usr/bin/hadoop
rm -rf /usr/hdp
rm -rf /var/hadoop

# Remove config folders on all nodes
rm -rf /etc/ambari-agent
rm -rf /etc/ambari-metrics-grafana
rm -rf /etc/ambari-server
rm -rf /etc/ambari-infra-solr
rm -rf /etc/ambari-metrics-grafana
rm -rf /etc/ams-hbase
rm -rf /etc/falcon
rm -rf /etc/flume
rm -rf /etc/hadoop
rm -rf /etc/hadoop-httpfs
rm -rf /etc/hbase
rm -rf /etc/hive 
rm -rf /etc/hive-hcatalog
rm -rf /etc/hive-webhcat
rm -rf /etc/hive2
rm -rf /etc/hst
rm -rf /etc/knox 
rm -rf /etc/livy
rm -rf /etc/livy2
rm -rf /etc/mahout 
rm -rf /etc/oozie
rm -rf /etc/phoenix
rm -rf /etc/pig 
rm -rf /etc/ranger-admin
rm -rf /etc/ranger-usersync
rm -rf /etc/spark2
rm -rf /etc/tez
rm -rf /etc/tez_hive2
rm -rf /etc/zookeeper

# Remove PIDs on all nodes
rm -rf /var/run/ambari-agent
rm -rf /var/run/ambari-metrics-grafana
rm -rf /var/run/ambari-server
rm -rf /var/run/falcon
rm -rf /var/run/flume
rm -rf /var/run/hadoop 
rm -rf /var/run/hadoop-mapreduce
rm -rf /var/run/hadoop-yarn
rm -rf /var/run/hbase
rm -rf /var/run/hive
rm -rf /var/run/hive-hcatalog
rm -rf /var/run/hive2
rm -rf /var/run/hst
rm -rf /var/run/knox
rm -rf /var/run/oozie 
rm -rf /var/run/webhcat
rm -rf /var/run/zookeeper

# Remove library folders on all nodes
rm -rf /usr/lib/ambari-agent
rm -rf /usr/lib/ambari-infra-solr-client
rm -rf /usr/lib/ambari-metrics-hadoop-sink
rm -rf /usr/lib/ambari-metrics-kafka-sink
rm -rf /usr/lib/ambari-server-backups
rm -rf /usr/lib/ams-hbase
rm -rf /usr/lib/mysql
rm -rf /var/lib/ambari-agent
rm -rf /var/lib/ambari-metrics-grafana
rm -rf /var/lib/ambari-server
rm -rf /var/lib/flume
rm -rf /var/lib/hadoop-hdfs
rm -rf /var/lib/hadoop-mapreduce
rm -rf /var/lib/hadoop-yarn 
rm -rf /var/lib/hive2
rm -rf /var/lib/knox
rm -rf /var/lib/smartsense
rm -rf /var/lib/storm

# Clean folder /var/tmp/* on all nodes
rm -rf /var/tmp/*

# Delete HST from cron on all nodes (in the meanwhile you're using crontab -r to delete all cron jobs)
# 0 * * * * /usr/hdp/share/hst/bin/hst-scheduled-capture.sh sync
# 0 2 * * 0 /usr/hdp/share/hst/bin/hst-scheduled-capture.sh
crontab -r

#  Remove databases. I remove the instances of MySQL and Postgres so that Ambari installed and configured fresh databases.
yum remove -y mysql mysql-server
yum erase -y postgresql
rm -rf /var/lib/pgsql
rm -rf /var/lib/mysql

# Remove symlinks on all nodes. Especially check folders /usr/sbin and /usr/lib/python2.6/site-packages
cd /usr/bin
which accumulo | xargs rm -rf
which atlas-start | xargs rm -rf
which atlas-stop | xargs rm -rf

which beeline | xargs rm -rf
which falcon | xargs rm -rf
which flume-ng | xargs rm -rf
which hbase | xargs rm -rf
which hcat | xargs rm -rf
which hdfs | xargs rm -rf
which hive | xargs rm -rf
which hiveserver2 | xargs rm -rf
which kafka | xargs rm -rf
which mahout | xargs rm -rf
which mapred | xargs rm -rf
which oozie | xargs rm -rf
which oozied.sh | xargs rm -rf
which phoenix-psql | xargs rm -rf
which phoenix-queryserver | xargs rm -rf
which phoenix-sqlline | xargs rm -rf
which phoenix-sqlline-thin | xargs rm -rf
which pig | xargs rm -rf
which python-wrap | xargs rm -rf
which ranger-admin | xargs rm -rf
which ranger-admin-start | xargs rm -rf
which ranger-admin-stop | xargs rm -rf
which ranger-kms | xargs rm -rf
which ranger-usersync | xargs rm -rf
which ranger-usersync-start | xargs rm -rf
which ranger-usersync-stop | xargs rm -rf
which slider | xargs rm -rf
which sqoop | xargs rm -rf
which sqoop-codegen | xargs rm -rf
which sqoop-create-hive-table | xargs rm -rf
which sqoop-eval | xargs rm -rf
which sqoop-export | xargs rm -rf
which sqoop-help | xargs rm -rf
which sqoop-import | xargs rm -rf
which sqoop-import-all-tables | xargs rm -rf
which sqoop-job | xargs rm -rf
which sqoop-list-databases | xargs rm -rf
which sqoop-list-tables | xargs rm -rf
which sqoop-merge | xargs rm -rf
which sqoop-metastore | xargs rm -rf
which sqoop-version | xargs rm -rf
which storm | xargs rm -rf
which storm-slider | xargs rm -rf
which worker-lanucher | xargs rm -rf
which yarn | xargs rm -rf
which zookeeper-client | xargs rm -rf
which zookeeper-server | xargs rm -rf
which zookeeper-server-cleanup | xargs rm -rf

# Remove service users on all nodes
userdel -r accumulo
userdel -r ambari-qa
userdel -r ams
userdel -r falcon
userdel -r flume
userdel -r hbase
userdel -r hcat
userdel -r hdfs
userdel -r hive
userdel -r kafka
userdel -r knox
userdel -r mapred
userdel -r oozie
userdel -r ranger
userdel -r spark
userdel -r sqoop
userdel -r storm
userdel -r tez
userdel -r yarn
userdel -r zeppelin
userdel -r zookeeper

# Run find / -name ** on all nodes. You will definitely find several more files/folders. Remove them.
find / -name "*ambari*" | xargs rm -rf
find / -name "*accumulo*" | xargs rm -rf
find / -name "*atlas*" | xargs rm -rf
find / -name "*beeline*" | xargs rm -rf
find / -name "*falcon*" | xargs rm -rf
find / -name "*flume*" | xargs rm -rf
find / -name "*hadoop*" | xargs rm -rf
find / -name "*hbase*" | xargs rm -rf
find / -name "*hcat*" | xargs rm -rf
find / -name "*hdfs*" | xargs rm -rf
find / -name "*hdp*" | xargs rm -rf
find / -name "*hive*" | xargs rm -rf
find / -name "*hiveserver2*" | xargs rm -rf
find / -name "*kafka*" | xargs rm -rf
find / -name "*mahout*" | xargs rm -rf
find / -name "*mapred*" | xargs rm -rf
find / -name "*oozie*" | xargs rm -rf
find / -name "*phoenix*" | xargs rm -rf
find / -name "*pig*" | xargs rm -rf
find / -name "*ranger*" | xargs rm -rf
find / -name "*slider*" | xargs rm -rf
find / -name "*sqoop*" | xargs rm -rf
find / -name "*storm*" | xargs rm -rf
find / -name "*yarn*" | xargs rm -rf
find / -name "*zookeeper*" | xargs rm -rf

# Reboot all nodes
reboot