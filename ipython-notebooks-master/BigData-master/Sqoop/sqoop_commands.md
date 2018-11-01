#Sqoop version
[cloudera@quickstart conf]$ sqoop-version
Warning: /usr/lib/sqoop/../accumulo does not exist! Accumulo imports will fail.
Please set $ACCUMULO_HOME to the root of your Accumulo installation.
18/02/28 12:07:17 INFO sqoop.Sqoop: Running Sqoop version: 1.4.6-cdh5.12.0
Sqoop 1.4.6-cdh5.12.0
git commit id 
Compiled by jenkins on Thu Jun 29 04:30:40 PDT 2017

--------------------------------------------------------------

Importing a Table

Sqoop tool ‘import’ is used to import table data from the table to the Hadoop file system as a text file or a binary file.

Checking the table in mysql

Connectiong mysql

mysql -uroot -pcloudera

mysql>


mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| cm                 |
| firehose           |
| hue                |
| metastore          |
| mysql              |
| nav                |
| navms              |
| oozie              |
| retail_db          |
| rman               |
| sentry             |
+--------------------+
12 rows in set (0.02 sec)

mysql> use retail_db
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed

mysql> show tables;
+---------------------+
| Tables_in_retail_db |
+---------------------+
| categories          |
| customers           |
| departments         |
| order_items         |
| orders              |
| products            |
+---------------------+
6 rows in set (0.00 sec)

mysql> desc customers;
+-------------------+--------------+------+-----+---------+----------------+
| Field             | Type         | Null | Key | Default | Extra          |
+-------------------+--------------+------+-----+---------+----------------+
| customer_id       | int(11)      | NO   | PRI | NULL    | auto_increment |
| customer_fname    | varchar(45)  | NO   |     | NULL    |                |
| customer_lname    | varchar(45)  | NO   |     | NULL    |                |
| customer_email    | varchar(45)  | NO   |     | NULL    |                |
| customer_password | varchar(45)  | NO   |     | NULL    |                |
| customer_street   | varchar(255) | NO   |     | NULL    |                |
| customer_city     | varchar(45)  | NO   |     | NULL    |                |
| customer_state    | varchar(45)  | NO   |     | NULL    |                |
| customer_zipcode  | varchar(45)  | NO   |     | NULL    |                |
+-------------------+--------------+------+-----+---------+----------------+
9 rows in set (0.00 sec)



[cloudera@quickstart conf]$ sqoop import --connect jdbc:mysql://localhost/retail_db --username root --password cloudera --table customers --m 1


[cloudera@quickstart conf]$ hadoop fs -cat customers/part-m-00000


Importing into Target Directory


[cloudera@quickstart conf]$ sqoop import --connect jdbc:mysql://localhost/retail_db --username root --password cloudera --table customers --m 1 --target-dir /queryresult

Import Subset of Table Data


[cloudera@quickstart conf]$ sqoop import --connect jdbc:mysql://localhost/retail_db --username root --password cloudera --table customers --m 1 --where "customer_city ='Chicago'" --target-dir queryresult

Incremental Import

Incremental import is a technique that imports only the newly added rows in a table. It is required to add ‘incremental’, ‘check-column’, and ‘last-value’ options to perform the incremental import.

 
[cloudera@quickstart conf]$ sqoop import --connect jdbc:mysql://localhost/retail_db --username root --password cloudera --table customers --m 1 --incremental append --check-column customer_id --last-value 12299


Import All tables

[cloudera@quickstart conf]$ sqoop import-all-tables --connect jdbc:mysql://localhost/retail_db --username root --password cloudera


------------------------------------------------------------------------

Sqoop Export


sqoop export --connect jdbc:mysql://localhost/retail_db --username root --password cloudera --table noor --export-dir customers/part-m-00001

----------------------------------------------------------------------------

Sqoop job


sqoop job --create incremental_import_job -- import --connect jdbc:mysql://localhost/retail_db --username root     --password cloudera     --table noor     --target-dir /data/newemployee     --incremental append     --check-column id     --last-value 7    --m 1

Verify Job (--list)

[cloudera@quickstart log]$ sqoop job --list
Warning: /usr/lib/sqoop/../accumulo does not exist! Accumulo imports will fail.
Please set $ACCUMULO_HOME to the root of your Accumulo installation.
18/02/28 12:42:03 INFO sqoop.Sqoop: Running Sqoop version: 1.4.6-cdh5.12.0
Available jobs:
  incremental_import_job


Inspect Job (--show)

[cloudera@quickstart log]$ sqoop job --show myjob

Execute Job (--exec)

[cloudera@quickstart log]$ sqoop job --exec myjob


--------------------------------------------

Sqoop Evaluation

sqoop eval \
--connect jdbc:mysql://localhost/retail_db \
--username root \ 
--password cloudera \
--query “SELECT * FROM noor LIMIT 3”


List Databases

sqoop list-databases \
--connect jdbc:mysql://localhost/ \
--username root \
--password cloudera 

List Tables

sqoop list-tables \
--connect jdbc:mysql://localhost/retail_db \
--username root \
--password cloudera 

-----------------------------------------------------------------------

Sqoop: Import Data From MySQL to Hive


sqoop import --connect jdbc:mysql://localhost:3306/retail_db \
--username root \
-P \
--split-by customer_id \
--columns customer_id,customer_fname \
--table customers  \
--target-dir /user/cloudera/ingest/raw/customers \ 
--fields-terminated-by "," \
--hive-import \
--create-hive-table \
--hive-table noor.customers 

hive> use noor
hive> show create table customers;
