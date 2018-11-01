nano custs.txt

custno,fname,lname,profession
101,43,56,7
102,4,34,76
103,3,6,65


hbase> create 'customers','c_data'


grunt> raw_data = LOAD 'custs.txt' USING PigStorage(',') AS (custno:chararray,fname:int,lname:int,age:int,profession:int);



grunt> store raw_data into 'hbase://customers' USING org.apache.pig.backend.hadoop.hbase.HBaseStorage('c_data:fname,c_data:lname,c_data:age,c_data:profession');
