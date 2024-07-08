from pyspark.sql import SparkSession


spark = (
    SparkSession
    .builder
    .config("spark.jars", "jars/build/libs/spark-sql-kafka-build-all.jar")
    .getOrCreate()
)
