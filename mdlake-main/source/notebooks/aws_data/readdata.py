# Databricks notebook source
# MAGIC %pip install xlrd==2.0.1
# MAGIC %pip install fsspec

# COMMAND ----------

import pandas as pd

# COMMAND ----------

dbutils.fs.ls("/mnt/dsml/s3datafiles/s3paydata/UK")

# COMMAND ----------

pdf1 = pd.read_excel("abfss://dsml@dsmldevsa.dfs.core.windows.net/s3datafiles/s3paydata/Afghanistan/Afghanistan 2020.EU.xlsx")

# COMMAND ----------

sDF = spark.read.format("com.crealytics.spark.excel").option("header", "true").option("inferSchema", True).load("dbfs:/mnt/dsml/s3datafiles/s3paydata/UK/United Kingdom 2019_part 1.xlsx")

# COMMAND ----------

