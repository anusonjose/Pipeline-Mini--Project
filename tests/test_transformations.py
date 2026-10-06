from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def test_net_amount():
    spark = (
        SparkSession.builder
        .master("local[2]")
        .appName("retail-tests")
        .getOrCreate()
    )

    data = [("O1", 2, 100.0), ("O2", 3, 50.0)]
    df = spark.createDataFrame(data, ["order_id", "quantity", "unit_price"])

    result = df.withColumn("net_amount", F.col("quantity") * F.col("unit_price"))
    values = [r.net_amount for r in result.orderBy("order_id").collect()]

    assert values == [200.0, 150.0]
    spark.stop()


def test_invalid_quantity_is_filtered():
    spark = (
        SparkSession.builder
        .master("local[2]")
        .appName("retail-tests")
        .getOrCreate()
    )

    data = [("O1", 2), ("O2", 0), ("O3", -1)]
    df = spark.createDataFrame(data, ["order_id", "quantity"])

    result = df.filter(F.col("quantity") > 0)

    assert result.count() == 1
    spark.stop()
