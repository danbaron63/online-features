from src.utils.spark import spark
from pyspark.sql import functions as F
from pyspark.sql import types as T


user_df = (
    spark
    .read
    .option("header", "true")
    .csv("data/user")
)

transaction_df = (
    spark
    .readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9094,localhost:9094")
    .option("subscribe", "transactions")
    .option("startingOffsets", "earliest")
    .load()
)

transaction_df = (
    transaction_df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
    .withColumn("parsed", F.from_json(
        "value",
        schema=T.StructType([
            T.StructField("id", T.StringType()),
            T.StructField("uid", T.StringType()),
            T.StructField("amount", T.StringType()),
            T.StructField("timestamp", T.StringType())
        ])
    ))
    .select(
        F.col("key"),
        F.col("value").alias("raw"),
        F.col("parsed.id"),
        F.col("parsed.uid"),
        F.col("parsed.amount").cast(T.FloatType()).alias("amount"),
        F.col("parsed.timestamp"),
    )
    .groupBy(
        F.window(F.col("timestamp"), "10 minutes", "5 minutes"),
        "uid"
    )
    .sum("amount").alias("total")
    .join(user_df, F.col("id") == F.col("uid"))
    .select(
        "*",
        F.col("window.start").alias("window_start"),
        F.col("window.end").alias("window_end"),
    )
    .drop("window")
)

# query = transaction_df.writeStream.outputMode("update").format("console").start()


def write_to_postgres(df, epoch_id):
    (
        df.write
        .format("jdbc").mode("append")
        .option("driver", "org.postgresql.Driver")
        .option("url", "jdbc:postgresql://localhost:5433/offline_store")
        .option("user", "user")
        .option("password", "password")
        .option("dbtable", "transaction")
        .save()
    )


db_query = (
    transaction_df
    .writeStream
    .outputMode("update")
    .foreachBatch(write_to_postgres)
    .start()
)

db_query.awaitTermination()
# query.awaitTermination()
