1. Create a file
#emp.txt
nano emp.txt

101,abc,20000
102,asd,30000
103,pqr,25000
104,qwe,30000
105,edc,20020


--Internal table

create table emp (eid int, ename string, esal double)
row format delimited
fields terminated by ','
lines terminated by '\n'
stored as textfile;


--External table

create external table emp2 (eid int, ename string, esal double)
row format delimited
fields terminated by ','
lines terminated by '\n'
stored as textfile;

local data local inpath 'emp.txt' into table emp;

local data local inpath 'emp2.txt' into table emp2;

--to see the file in hdfs
hadoop fs -lsr /user/hive/warehouse/


drop table emp;
drop table emp2;

nano createEx.hql

		create table emp (eid int, ename string, esal double)
		row format delimited
		fields terminated by ','
		lines terminated by '\n'
		stored as textfile;


hive -f createEx.hql

alter table emp rename to employee;

--------------------------------------------------------------------

#PARTITION

nano createExPartemp.hql

create table partemp(eid int, ename string, esal double)
partitioned by (loc string)
row format delimited
fields terminated by ','
lines terminated by '\n'
stored as textfile;


hive -f createExPartemp.hql

nano emp.txt

101,abc,200
102,asd,300
103,qaz,400

load data local inpath 'emp.txt' into table partemp partition(loc = 'HYD');
load data local inpath 'emp.txt' into table partemp partition(loc = 'BAN');


#View the files
hadoop fs -lsr /user/warehouse/hivedb/partemp/


show partitions partemp;

select * from partemp where loc = 'HYD';

------------------------------------------------------------------------------

#BUCKETTING

set hive.enforce.bucketing = true;

create table buckemp(eid int, ename string, esal double)
clustered by (eid) into 3 buckets;
row format delimited
fields terminated by ','
lines terminated by '\n'
stored as textfile;

desc bucktemp;

insert overwrite table bucktemp
select * from employee;

#View the files
hadoop fs -lsr /user/warehouse/buckemp


create table buckemp2(eid int, ename string, esal double)
row format delimited
fields terminated by ','
lines terminated by '\n'
stored as textfile;

insert overwrite table bucktemp2
select * from employee;

select * from buckemp2 TABLESAMPLE( BUCKET 2 OUT OF 3 ON eid);

select * from buckemp2 TABLESAMPLE( BUCKET 1 OUT OF 3 ON eid);


show functions;



---------------------------------------------------------------------------------

#UDF

nano trail.txt
#trail.txt
RAVi,KUMAR
ANISH,Kumar
Rakesh,JHA
MOHAMed,NoorDeen


nano createtable.hql
CREATE table mytab(
fname STRING,
lname STRING)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
STORED AS TEXTFILE;

LOAD DATA LOCAL INPATH 'trail.txt' OVERWRITE INTO TABLE mytab;

select * from mytab;


hive -f createtable.hql


nano my.py
#my.py
import sys

import datetime

for line in sys.stdin:

     line = line.strip()

     fname , lname = line.split('\t')

     l_name = lname.lower()

     print '\t'.join([fname, str(l_name)])




# Go inside hive shell

add FILE my.py;


SELECT TRANSFORM(fname, lname) USING 'python my.py' AS (fname, l_name) FROM mytab;










