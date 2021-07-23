# Databricks notebook source
dbutils.fs.ls("/mnt/dsml/s3datafiles/s3paydata/Angola")

# COMMAND ----------

filepath = "abfss://dsml@dsmldevsa.dfs.core.windows.net/s3datafiles/s3paydata/Angola/Angola Dictionary 14-20.xlsx"

# COMMAND ----------

sparkDF = spark.read.format("com.crealytics.spark.excel").option("header", "true").option("inferSchema", True).load(filepath)

# COMMAND ----------

display(sparkDF)

# COMMAND ----------

df1 = spark.table("aws_country_data.afghanistan_afghanistan2020eu")

# COMMAND ----------

df1.show()

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from aws_country_data.afghanistan_afghanistan2020eu

# COMMAND ----------

