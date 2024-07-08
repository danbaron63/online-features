from src.spark import spark
from pyspark.sql import types as T
from pyspark.sql import functions as F


def file_stream():
    schema = T.StructType([
        T.StructField("id", T.IntegerType()),
        T.StructField("uid", T.IntegerType()),
        T.StructField("firstname", T.StringType()),
        T.StructField("surname", T.StringType()),
        T.StructField("amount", T.FloatType()),
    ])
    sdf = spark.readStream.format("csv").option("header", "true").schema(schema).load("data")

    sdf = sdf.select("uid", "amount").groupBy("uid").sum("amount")

    query = sdf.writeStream.outputMode("complete").format("console").start()

    query.awaitTermination()


if __name__ == "__main__":
    file_stream()
