from src.spark import spark
from pyspark.sql import functions as F
from pyspark.sql import types as T


df = (
  spark
  .readStream
  .format("kafka")
  .option("kafka.bootstrap.servers", "localhost:9094,localhost:9094")
  .option("subscribe", "account")
  .option("startingOffsets", "earliest")
  .load()
)

# id,uid,firstname,surname,amount

df = (
  df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
  .withColumn("parsed", F.from_json(
    "value",
    schema=T.StructType([
        T.StructField("id", T.StringType()),
        T.StructField("uid", T.StringType()),
        T.StructField("firstname", T.StringType()),
        T.StructField("surname", T.StringType()),
        T.StructField("amount", T.StringType()),
    ])
  ))
  .select(
    F.col("key"),
    F.col("value").alias("raw"),
    F.col("parsed.id"),
    F.col("parsed.uid"),
    F.col("parsed.firstname"),
    F.col("parsed.surname"),
    F.col("parsed.amount").cast(T.FloatType()).alias("amount")
  )
  .groupBy("uid")
  .sum("amount")
)

query = df.writeStream.outputMode("complete").format("console").start()

query.awaitTermination()

