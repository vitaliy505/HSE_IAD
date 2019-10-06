# How install Hadoop in a single node mode
Note: Instruction contains information how to install Hadoop 3.1.2 on Ubuntu 16.04
### Steps:
1. [Install Java](#install_java)
2. [Install and configure Hadoop](#install_hadoop)
3. [Check correct work of Hadoop](#check_hadoop)
___
1. <a name="install_java"></a> Install Java:
   * Check either Java is already installed ($ means command in bash):
        ```
        $ java -version
     ```
    * If Java is installed, go to [Install and configure Hadoop](#install_hadoop)
    * To install default Java, do the next:
        ```
        $ sudo apt-get update
        $ sudo apt-get upgrade
        $ sudo apt-get install default-jre
      ``` 
      JDK can be additionally installed:
       ```
        $ sudo apt-get install default-jdk
      ``` 
      To install Oracle Java, refer to https://tecadmin.net/install-oracle-java-11-on-ubuntu-16-04-xenial/
     * Check Java version:
        ```
        $ java -version
       ```
     For additional information about Java installation, refer to https://www.digitalocean.com/community/tutorials/java-apt-get-ubuntu-16-04-ru

2. <a name="install_hadoop"></a> Install and configure Hadoop:
    * Download, extract and deploy Hadoop binaries:
        ```
        $ wget http://apache-mirror.rbc.ru/pub/apache/hadoop/common/hadoop-3.1.2/hadoop-3.1.2.tar.gz
        $ tar -xzvf hadoop-3.1.2.tar.gz
        $ sudo mv hadoop-3.1.2 /usr/local/hadoop
      ``` 
     * Configure Hadoop - add `export JAVA_HOME=$(readlink -f /usr/bin/java | sed "s:bin/java::")` in /usr/local/hadoop/etc/hadoop/hadoop-env.sh
3. Run Hadoop sample to check correct work:
     ```
     $ mkdir ~/input
     $ cp /usr/local/hadoop/etc/hadoop/*.xml ~/input
     $ /usr/local/hadoop/bin/hadoop jar /usr/local/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.1.2.jar grep ~/input ~/grep_example 'a[d]*'
     $ cat ~/grep_example/*
    ```
For additional information about Hadoop installation, refer to https://www.digitalocean.com/community/tutorials/how-to-install-hadoop-in-stand-alone-mode-on-ubuntu-16-04 or 
https://poweruphosting.com/blog/install-hadoop-ubuntu/
