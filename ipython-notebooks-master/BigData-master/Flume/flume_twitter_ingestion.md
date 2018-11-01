Twitter flume data ingestion

flume-ng agent -n TwitterAgent -c conf -f /etc/flume-ng/conf/twitter.conf



#twitter.conf

# Naming the components on the current agent.
TwitterAgent.sources = Twitter
TwitterAgent.channels = MemChannel
TwitterAgent.sinks = HDFS

# Describing/Configuring the source
TwitterAgent.sources.Twitter.type = org.apache.flume.source.twitter.TwitterSource


TwitterAgent.sources.Twitter.consumerKey = XRihcUg1U5JtNewEZqbH89eB2
TwitterAgent.sources.Twitter.consumerSecret = vLUGt1QKnmh7aT3NYpCcKEUAUdxODgH9lAAEG4ezbdjvm1bInf
TwitterAgent.sources.Twitter.accessToken = 103894086-RDjAeQp9ZhZ2WQh9HnzVKKKfBcYhCLxRPuyNy3Jw
TwitterAgent.sources.Twitter.accessTokenSecret = l4TzgkGdkaJimpJGVwNHK0WqGtxPOWDzAAIQVDOtpzXhc
TwitterAgent.sources.Twitter.keywords = hadoop

# Describing/Configuring the sink

TwitterAgent.sinks.HDFS.type = hdfs
TwitterAgent.sinks.HDFS.hdfs.path = hdfs://quickstart.cloudera:8020/tmp/Hadoop/twitter_data/
TwitterAgent.sinks.HDFS.hdfs.fileType = DataStream
TwitterAgent.sinks.HDFS.hdfs.writeFormat = Text
TwitterAgent.sinks.HDFS.hdfs.batchSize = 1000
TwitterAgent.sinks.HDFS.hdfs.rollSize = 0
TwitterAgent.sinks.HDFS.hdfs.rollCount = 10000

# Describing/Configuring the channel
TwitterAgent.channels.MemChannel.type = memory
TwitterAgent.channels.MemChannel.capacity = 10000
TwitterAgent.channels.MemChannel.transactionCapacity = 100

# Binding the source and sink to the channel
TwitterAgent.sources.Twitter.channels = MemChannel
TwitterAgent.sinks.HDFS.channel = MemChannel




