oozie admin --oozie http://localhost:11000/oozie -status

go to the particular jog folder 

say for example  
cd $your_path_where_you_installed/apps/java-main

oozie job -oozie http://localhost:11000/oozie/ -config job.properties -run
This will prompt a status with job id

copy that job id and check for status

myjob id was 0000002-180301215901161-oozie-oozi-W

oozie job -oozie http://localhost:11000/oozie/ -info 0000002-180301215901161-oozie-oozi-W
