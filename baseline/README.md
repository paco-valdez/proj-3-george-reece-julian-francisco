#### Julian Hicks, Reece Koe, Paco Valdez and George Jiang
# Project 3: Understanding User Behavior

- You're a data scientist at a game development company  

- Your latest mobile game has two events you're interested in tracking: `buy a
  sword` & `join guild`

- Each has metadata characterstic of such events (i.e., sword type, guild name,
  etc)

## Troubleshooting Fix

There is an issue with one of the docker images used here. While replacement is always possible, a quicker fix may be to run the following code in ssh:

```
sudo -s
echo 'GRUB_CMDLINE_LINUX_DEFAULT="vsyscall=emulate"' >> /etc/default/grub
update-grub
reboot
```

This should fix any problems you may encounter. Since this issue is not necessarily reproducible, we recommend you run through the below first before trying the above. 

## Part 1: Create the Pipeline from Flask to Data Extraction

### Setup the project 3 folder

```
cd ~/w205/proj-3-george-reece-julian-francisco/baseline/
```
```
docker-compose up -d
```

### Install requirements for Rest API

```
docker-compose exec mids pip install -r \
 /w205/proj-3-george-reece-julian-francisco/baseline/requirements.txt
```

### Install kafkacat and Apache Bench
```
docker-compose exec mids apk add kafkacat
docker-compose exec mids apk add apache2-utils
```

### Setup a Hadoop folder in the cluster

```
docker-compose exec cloudera hadoop fs -ls /tmp/
```

### Create required kafka topics
<!-- 
```
docker-compose exec kafka \
  kafka-topics \
    --create \
    --topic events \
    --partitions 1 \
    --replication-factor 1 \
    --if-not-exists --zookeeper zookeeper:32181
``` -->
```
docker-compose exec kafka \
  kafka-topics \
    --create \
    --topic purchases \
    --partitions 1 \
    --replication-factor 1 \
    --if-not-exists --zookeeper zookeeper:32181
```
```
docker-compose exec kafka \
  kafka-topics \
    --create \
    --topic guild \
    --partitions 1 \
    --replication-factor 1 \
    --if-not-exists --zookeeper zookeeper:32181
```

### In a separate cmds, use kafkacat to continuously read from the topics
```
cd ~/w205/proj-3-george-reece-julian-francisco/baseline/
```
```
docker-compose exec mids \
  kafkacat -C -b kafka:29092 -t purchases -o beginning
```
```
docker-compose exec mids \
  kafkacat -C -b kafka:29092 -t guild -o beginning
```

### In a separate cmd, activate the api flask
```
cd ~/w205/proj-3-george-reece-julian-francisco/baseline/
```

```
docker-compose exec mids \
  env FLASK_APP=/w205/proj-3-george-reece-julian-francisco/baseline/game_api.py \
  flask run --host 0.0.0.0
```

### Back in original cmd, Extract test data from Kafka, land them into HDFS/parquet to make them available for analysis.

```
docker-compose exec spark spark-submit /w205/proj-3-george-reece-julian-francisco/baseline/stream_purchases.py
docker-compose exec spark spark-submit /w205/proj-3-george-reece-julian-francisco/baseline/stream_guild.py
```

###  Use Apache Bench to generate test data for your pipeline

```
docker-compose exec mids chmod 755 /w205/proj-3-george-reece-julian-francisco/baseline/scripts/create_test_data.sh
docker-compose exec mids /w205/proj-3-george-reece-julian-francisco/baseline/scripts/create_test_data.sh
```



## Part 2: Optional Extract the data from the HDFS/parquet to Spark SQL

### Add a hive metastore to the streaming tables

```
docker-compose exec cloudera hive
```

```sql
    create external table if not exists default.purchases (
        raw_event       string,
        timestamp       string,
        user_id         int,
        item_id         int,
        quantity        int,
        price_paid      double,
        vendor_id       int,
        api_string      string,
        request_status  string,
        content_length  string,
        content_type    string,
        host            string,
        user_agent      string,
        accept          string
        )
    stored as parquet 
    location '/tmp/default/purchases'
    tblproperties ("parquet.compress"="SNAPPY");
```

```sql
    create external table if not exists default.guild (
        raw_event       string,
        timestamp       string,
        user_id         int,
        guild_id        int,
        action          string,
        api_string      string,
        request_status  string,
        content_length  string,
        content_type    string,
        host            string,
        user_agent      string,
        accept          string
        )
    stored as parquet 
    location '/tmp/default/guild'
    tblproperties ("parquet.compress"="SNAPPY");
```

<!-- ### At the pyspark prompt, read from kafka

```
purchases = spark.read.parquet('/tmp/purchases')
purchases.show()
purchases.registerTempTable('purchases')
query = """
create external table default.purchases
  stored as parquet
  location '/tmp/default/purchases'
  as
  select * from purchases
"""
spark.sql(query)

guild = spark.read.parquet('/tmp/guild')
guild.show()
guild.registerTempTable('guild')
query = """
create external table default.guild
  stored as parquet
  location '/tmp/default/guild'
  as
  select * from guild
"""
spark.sql(query)
``` -->

## Part 3: Show Pipeline creates data table in Hadoop using Presto

### Launch Presto
```
docker-compose exec presto presto --server presto:8080 --catalog hive --schema default
```

### Using presto to show data table
```
presto:default> show tables;
```

```
presto:default> describe purchases;
presto:default> describe guild;
```

### Using presto to pull data
```
presto:default> select * from purchases;
presto:default> select * from guild;
```



