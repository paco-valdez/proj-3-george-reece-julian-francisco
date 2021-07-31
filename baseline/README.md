# Project 3: Understanding User Behavior

- You're a data scientist at a game development company  

- Your latest mobile game has two events you're interested in tracking: `buy a
  sword` & `join guild`

- Each has metadata characterstic of such events (i.e., sword type, guild name,
  etc)
  
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

```
docker-compose exec kafka \
  kafka-topics \
    --create \
    --topic events \
    --partitions 1 \
    --replication-factor 1 \
    --if-not-exists --zookeeper zookeeper:32181
```
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
  kafkacat -C -b kafka:29092 -t events -o beginning
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

### Back in original cmd, use Apache Bench to generate test data for your pipeline

```
docker-compose exec mids chmod 755 /w205/proj-3-george-reece-julian-francisco/baseline/create_test_data.sh
docker-compose exec mids /w205/proj-3-george-reece-julian-francisco/baseline/create_test_data.sh
```


### Extract test data from Kafka, land them into HDFS/parquet to make them available for analysis.

```
docker-compose exec spark spark-submit /w205/proj-3-george-reece-julian-francisco/baseline/extract_events.py
docker-compose exec spark spark-submit /w205/proj-3-george-reece-julian-francisco/baseline/write_purchases.py
docker-compose exec spark spark-submit /w205/proj-3-george-reece-julian-francisco/baseline/write_guild.py
```

## Part 2: Optional Extract the data from the HDFS/parquet to Spark SQL

### Spin up a pyspark process using the `spark` container

```
docker-compose exec spark pyspark
```

### At the pyspark prompt, read from kafka

```
purchases = spark.read.parquet('/tmp/purchases')
purchases.show()
purchases.registerTempTable('purchases')
purchases_by_example2 = spark.sql("select * from purchases where host='user1.comcast.com'")
purchases_by_example2.show()
```

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
```

### Using presto to pull data
```
presto:default> select * from purchases;
```

