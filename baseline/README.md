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
cp ~/w205/course-content/12-Querying-Data-II/docker-compose.yml .
```

::: notes
Get the necessary docker-compose for project 3
:::

### Spin up the cluster

```
docker-compose up -d
```

### Setup a Hadoop folder in the cluster

```
docker-compose exec cloudera hadoop fs -ls /tmp/
```

### Create a topic `events`

```
docker-compose exec kafka \
  kafka-topics \
    --create \
    --topic events \
    --partitions 1 \
    --replication-factor 0 \
    --if-not-exists --zookeeper zookeeper:32181
```

### In a separate cmd,  use kafkacat to continuously read from `events` topic

```
docker-compose exec mids \
  kafkacat -C -b kafka:29092 -t events -o beginning
```

### In a separate cmd, activate the api flask

```
docker-compose exec mids \
  env FLASK_APP=/w205/proj-3-george-reece-julian-francisco/baseline/game_api.py \
  flask run --host 0.0.0.0
```

### Use Apache Bench to generate test data for your pipeline

```
docker-compose exec mids create_test_data.sh
```

create_test_data.sh
```
ab -n 10 -H "Host: user1.comcast.com" http://localhost:5000/
ab -n 10 -H "Host: user1.comcast.com" http://localhost:5000/purchase_a_sword
```


### Extract test data from Kafka, land them into HDFS/parquet to make them available for analysis using Spark.

```
docker-compose exec spark spark-submit /w205/proj-3-george-reece-julian-francisco/baseline/extract_events.py
docker-compose exec spark spark-submit /w205/proj-3-george-reece-julian-francisco/baseline/filtered_writes.py
```

## Part 2: Extract the data from the HDFS/parquet to Spark SQL for analysis

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

## Part 3: Answer business questions using dataframe

#### Potential Business Questions
1. How many purchases are being made by host?
  - `	SELECT count(user_id) FROM purchases WHERE host='user1.comcast.com'" `
2. How many purchases did each user name?
  - `	SELECT count(user_id) FROM purchases WHERE host='user1.comcast.com'" `
3. How many users both buy a sword and join a guild?
  - `SELECT user_id, count(user_id) FROM purchases, guildaction WHERE EXISTS (Select user_id from purchases, guildaction WHERE purchases.user_id = guildaction.user_id AND guildaction.action = 'Join')`
4. What’s the most common vendor for sword buying?
  - `	1. SELECT vendor_id, count(vendor_id) as count FROM purchases ORDER BY count`

5. Do users tend to buy swords first or join guilds first?
6. What guilds do users leave the most?
  - `SELECT guild_id FROM guildaction WHERE action=leave GROUP BY action=leave ORDER BY count(guild_id)`

7. What swords are purchased most at a discount?

