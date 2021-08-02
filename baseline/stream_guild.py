#!/usr/bin/env python
"""Extract events from kafka and write them to hdfs
"""
import json
from pyspark.sql import SparkSession, Row
from pyspark.sql import functions as F
from pyspark.sql.functions import udf, from_json
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType


def guild_event_schema():
    return StructType([
        StructField("user_id", IntegerType(), True),
        StructField("guild_id", IntegerType(), True),
        StructField("action", StringType(), True),
        StructField("api_string", StringType(), True),
        StructField("request_status", StringType(), True),
        StructField("Content-Length", StringType(), True),
        StructField("Content-Type", StringType(), True),
        StructField("Host", StringType(), True),
        StructField("User-Agent", StringType(), True),
        StructField("Accept", StringType(), True),
    ])

def main():
    """main
    """
    spark = SparkSession \
        .builder \
        .appName("ExtractGuildJob") \
        .getOrCreate()

    raw_events = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:29092") \
        .option("subscribe", "guild") \
        .load()

    purchases = raw_events \
        .select(raw_events.value.cast('string').alias('raw_event'),
                raw_events.timestamp.cast('string'),
                from_json(raw_events.value.cast('string'),
                          guild_event_schema()).alias('json')) \
        .select('raw_event', 'timestamp', 'json.*')

    sink = purchases \
        .writeStream \
        .format("parquet") \
        .option("checkpointLocation", "/tmp/checkpoints/guild") \
        .option("path", "/tmp/default/guild") \
        .trigger(processingTime="120 seconds") \
        .start()

    sink.awaitTermination()


if __name__ == "__main__":
    main()