# Running Mapreduce SalesReport Data 

This tutorial is developed on Linux - Ubuntu operating System.
You should have Hadoop (version 2.2.0 used for this tutorial) already installed.
You should have Java (version 1.8.0 used for this tutorial) already installed on the system.

Steps: 1

Create a new directory with name MapReduceTutorial

sudo mkdir MapReduceTutorial

Give permissions

sudo chmod -R 777 MapReduceTutorial

Steps: 2

pull the src data

Steps: 3

Copy the File SalesJan2009.csv into ~/inputMapReduce

Now Use below command to copy ~/inputMapReduce to HDFS.

hadoop dfs -copyFromLocal ~/inputMapReduce /

Step 4:

Load the project to Eclipse and Export the jar

or

copy the jar from github folder SalesCountry.jar

Step 5:

Run the MapReduce job

hadoop jar SalesCountry.jar SalesCountry.SalesCountryDriver /SalesJan2009.csv /output
