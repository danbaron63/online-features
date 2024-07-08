from src.utils.spark import spark
from pyspark.sql import types as T


def file_stream():
    schema = T.StructType([
        T.StructField("id", T.IntegerType()),
        T.StructField("uid", T.IntegerType()),
        T.StructField("amount", T.FloatType()),
    ])
    sdf = spark.readStream.format("csv").option("header", "true").schema(schema).load("data/transactions")

    sdf = sdf.select("uid", "amount").groupBy("uid").sum("amount")

    query = sdf.writeStream.outputMode("complete").format("console").start()

    query.awaitTermination()


if __name__ == "__main__":
    file_stream()
