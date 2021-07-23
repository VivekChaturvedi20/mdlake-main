# Databricks notebook source
# DBTITLE 1,Mounting Adls gen 2 to dbfs
### Below example shows the process for Mounting the container dsml from the storage account dsmldevsa to the dbfs directory /mnt/dsml
### Note- This requires a High Concurrency Cluster with AD credentials Passthrough enabled under advanced options

# COMMAND ----------

configs = {
  "fs.azure.account.auth.type": "CustomAccessToken",
  "fs.azure.account.custom.token.provider.class": spark.conf.get("spark.databricks.passthrough.adls.gen2.tokenProviderClassName")
}

# Optionally, you can add <directory-name> to the source URI of your mount point.
dbutils.fs.mount(
  source = "abfss://dsml@dsmldevsa.dfs.core.windows.net/",
  mount_point = "/mnt/dsml",
  extra_configs = configs)

# COMMAND ----------

dbutils.fs.ls("/mnt/dsml")

# COMMAND ----------

import pandas as pd

df = pd.DataFrame({'num_legs': [2, 4, 8, 0],

                   'num_wings': [2, 0, 0, 0],

                   'num_specimen_seen': [10, 2, 1, 8],

                  'animal':['falcon', 'dog', 'spider', 'fish']},)

sparkdf = spark.createDataFrame(df)
sparkdf.createOrReplaceTempView("test_table") # Crating Temp table


# COMMAND ----------

dbutils.fs.mkdirs("/mnt/dsml/testfolder/testdbhc")

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE DATABASE IF NOT EXISTS testdbhc

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS TestDBhc.testtable
# MAGIC USING DELTA
# MAGIC LOCATION "abfss://dsml@dsmldevsa.dfs.core.windows.net/testfolder/TestDBhc"
# MAGIC -- LOCATION "/mnt/dsml/testfolder/TestDBhc"
# MAGIC AS SELECT * FROM test_table

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM TestDBhc.testtable

# COMMAND ----------

dbutils.fs.ls("/mnt/dsml")

# COMMAND ----------

storage_account_name = "dsmldevsa"
# storage_account_access_key = dbutils.secrets.get(scope = "sqlmikeyvault", key = "storage-acc-dsmldevsa")
container_name = "dsml"
source = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net"

# spark.conf.set(f"fs.azure.account.key.{storage_account_name}.dfs.core.windows.net", storage_account_access_key)
# xml_path = "/mnt/dsml/linkup_data/extracted_data/Kornferry/Diff/2021-06-07 11:03:33/2021-06-07 11:03:33_d_KornFerryFeed.xml"
xml_path = "/mnt/dsml/linkup_data/samplexml/d_KornFerryFeed.xml"

# COMMAND ----------


print(xml_path)
df = spark.read.format("com.databricks.spark.xml").option("rowTag", "job").load(xml_path)
df.show()

# df = spark.read .format("com.databricks.spark.xml").option("rowTag", "job").load("/FileStore/tables/2021_06_01_13_01_32_d_kornferry-2.xml")
# df.show()

# df=spark.read.format("xml").option("rowTag","Root").load(xml_path)
# df = spark.read .format("com.databricks.spark.xml") .option("rowTag", "book") .load("/FileStore/tables/books.xml")
# df.show()

# COMMAND ----------

