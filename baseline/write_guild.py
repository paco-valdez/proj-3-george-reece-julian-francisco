#!/usr/bin/env python
"""Extract events from kafka and write them to hdfs
"""
import json
from pyspark.sql import SparkSession, Row
# from pyspark.sql.functions import udf


def main():
    """main
    """
    spark = SparkSession \
        .builder \
        .appName("ExtractEventsJob") \
        .getOrCreate()

    raw_events = spark \
        .read \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:29092") \
        .option("subscribe", "guild") \
        .option("startingOffsets", "earliest") \
        .option("endingOffsets", "latest") \
        .load()

    guild_events = raw_events \
        .select(raw_events.value.cast('string').alias('raw'),
                raw_events.timestamp.cast('string'))

    extracted_guild_events = guild_events \
        .rdd \
        .map(lambda r: Row(timestamp=r.timestamp, **json.loads(r.raw))) \
        .toDF()
    extracted_guild_events.printSchema()
    extracted_guild_events.show()

    extracted_guild_events \
        .write \
        .mode('overwrite') \
        .parquet('/tmp/guild')


if __name__ == "__main__":
    main()
