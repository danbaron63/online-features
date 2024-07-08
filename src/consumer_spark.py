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

# id,uid,firstname,surname,amount

transaction_df = (
  transaction_df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
  .withColumn("parsed", F.from_json(
    "value",
    schema=T.StructType([
        T.StructField("id", T.StringType()),
        T.StructField("uid", T.StringType()),
        T.StructField("amount", T.StringType()),
    ])
  ))
  .select(
    F.col("key"),
    F.col("value").alias("raw"),
    F.col("parsed.id"),
    F.col("parsed.uid"),
    F.col("parsed.amount").cast(T.FloatType()).alias("amount")
  )
  .groupBy("uid")
  .sum("amount").alias("total")
  .join(user_df, F.col("id") == F.col("uid"))
)

query = transaction_df.writeStream.outputMode("update").format("console").start()

query.awaitTermination()

