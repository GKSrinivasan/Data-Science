1.2. Environment

    Apache Flume 1.6.0 (installed on Linux CentOS is prefered)
    Hadoop 2.6.0


which flume-ng
[cloudera@quickstart ~]$ cd /etc
[cloudera@quickstart etc]$ tree flume*
flume-ng
├── conf -> /etc/alternatives/flume-ng-conf
├── conf.dist -> conf.empty
└── conf.empty
    ├── flume.conf
    ├── flume-conf.properties.template
    ├── flume-env.ps1.template
    ├── flume-env.sh.template
    └── log4j.properties

3 directories, 5 files


You can use Cloudera Quickstart VMs. The current version is CDH 5.7. It already has Apache Hadoop ecosystems including Apache Flume installed.
1.3. Create a configuration for Flume Agent

Create a file flume-hdfs-sink.conf at the folder: /usr/lib/flume-ng/conf with following content:
agent1.channels.memory-channel.type=memory
agent1.sources.tail-source.type=exec
agent1.sources.tail-source.command=tail -F /var/log/messages
agent1.sources.tail-source.channels=memory-channel

#hdfs sink
agent1.sinks.hdfs-sink.channel=memory-channel
agent1.sinks.hdfs-sink.type=hdfs
agent1.sinks.hdfs-sink.hdfs.path=hdfs://quickstart.cloudera:8020/tmp/system.log
agent1.sinks.hdfs-sink.hdfs.fileType=DataStream
agent1.channels=memory-channel
agent1.sources=tail-source
agent1.sinks=log-sink hdfs-sink

	
agent1.channels.memory-channel.type=memory
agent1.sources.tail-source.type=exec
agent1.sources.tail-source.command=tail -F /var/log/messages
agent1.sources.tail-source.channels=memory-channel
 
#hdfs sink
agent1.sinks.hdfs-sink.channel=memory-channel
agent1.sinks.hdfs-sink.type=hdfs
agent1.sinks.hdfs-sink.hdfs.path=hdfs://quickstart.cloudera:8020/tmp/system.log
agent1.sinks.hdfs-sink.hdfs.fileType=DataStream
agent1.channels=memory-channel
agent1.sources=tail-source
agent1.sinks=log-sink hdfs-sink

We named the agent: agent1

We will use the exec source type which will  executes the tail command on the file /var/log/messages.

We use the hdfs sink, specify the path of file which the log file will be written on the hdfs:hdfs://quickstart.cloudera:8020/tmp/system.log

And finally we connect the tail source and the hdfs sink by the memory-channel.
2. Run the Apache Flume HDFS Sink example
2.1. Start the Agent

Go to the folder where Apache Flume is installed. In my Cloudera, it is: /usr/lib/flume-ng
cd /usr/lib/flume-ng

	
cd /usr/lib/flume-ng

Start the agent by issuing following command:
./bin/flume-ng agent --conf conf -conf-file conf/flume-hdfs-sink.conf --name agent1

	
./bin/flume-ng agent --conf conf -conf-file conf/flume-hdfs-sink.conf --name agent1

We have specified the configuration file is the file we have just created above and the agent1 as agent name.

2.2. Verify the result.

We can verify the result by check the directory: hdfs://quickstart.cloudera:8020/tmp/system.log on the HDFS. You can do that by issuing below command:
hadoop fs -cat hdfs://quickstart.cloudera:8020/tmp/system.log/*

	
hadoop fs -cat hdfs://quickstart.cloudera:8020/tmp/system.log/*

The output on my console:
Aug  1 06:38:18 quickstart ntpd[4832]: 0.0.0.0 c614 04 freq_mode
Aug  1 06:38:18 quickstart ntpd_intres[4846]: DNS 3.centos.pool.ntp.org -> 118.102.5.136
Aug  1 06:38:19 quickstart ntpd[4832]: 0.0.0.0 c618 08 no_sys_peer
Aug  1 06:39:51 quickstart kernel: fuse init (API version 7.14)
	
Aug  1 06:38:18 quickstart ntpd[4832]: 0.0.0.0 c614 04 freq_mode
Aug  1 06:38:18 quickstart ntpd_intres[4846]: DNS 3.centos.pool.ntp.org -> 118.102.5.136
Aug  1 06:38:19 quickstart ntpd[4832]: 0.0.0.0 c618 08 no_sys_peer
Aug  1 06:39:51 quickstart kernel: fuse init (API version 7.14)

Or simply open Hue or any tool that can view HDFS content.
