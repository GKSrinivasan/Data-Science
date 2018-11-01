In terminal
> hbase shell



#Create a table 'peope' with Column family 'roles' and 'info'
create 'people','roles','info'

#Insert a data into table
put 'people','cutting','info:height','9ft'
put 'people','cutting','info:state','CA'
put 'people','cutting','info:ASF','Director'
put 'people','cutting','info:Hadoop','Founder'
put 'people','tlipcon','info:height','5ft'
put 'people','tlipcon','info:state','CA'
put 'people','tlipcon','info:Hadoop','Commiter'
put 'people','tlipcon','info:Hive','Contributor'

#Description about data
describe 'people'

#disable the table to drop
disable 'people'

#enable to table to use it
enable 'people'

#Alter the table versions
alter 'people' , {NAME=> 'roles', VERSION =>3}
 VERSIONS => '3'

describe 'people'

#Retreive the table with following condition
get 'people','tlipcon',{COLUMN =>'info:Hadoop' }


#Insert the data
put 'people','tlipcon','roles:state','TN'
put 'people','tlipcon','roles:Hadoop','Dev'
put 'people','tlipcon','roles:Hive','Coder'

#Get the data with condition
get 'people','tlipcon',{COLUMN =>'info:Hadoop',VERSIONS=>3 }

#Retreive all the data in the row key 'people'
get 'people','cutting'

#Retreive all data
scan 'people'

#delete particular column
delete 'people','tlipcon','info:Hive'


