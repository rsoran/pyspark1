from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("HelloPySpark").master("local[*]").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
print("Spark version:", spark.version)

df = spark.createDataFrame(
    [("Alice", "Math", 90), ("Bob", "Math", 75), ("Alice", "Physics", 85), ("Bob", "Physics", 95)],
    ["name", "subject", "marks"],
)
df.show()
df.groupBy("name").agg(F.avg("marks").alias("avg_marks")).show()

spark.stop()
