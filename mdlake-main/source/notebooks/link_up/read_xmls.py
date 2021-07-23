# Databricks notebook source
storage_account_name = "dsmldevsa"
storage_account_access_key = dbutils.secrets.get(scope = "sqlmikeyvault", key = "storage-acc-dsmldevsa")
container_name = "dsml"
source = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net"
# spark.conf.set(f"fs.azure.account.key.{storage_account_name}.dfs.core.windows.net", storage_account_access_key)
xml_path = f"{source}/linkup_data/extracted_data/Kornferry/Diff/2021-06-07 11:03:33/2021-06-07 11:03:33_d_KornFerryFeed.xml"
xml_path = f"{source}/linkup_data/samplexml/d_KornFerryFeed.xml"
print(xml_path)
df = spark.read.format("com.databricks.spark.xml").option("rowTag", "job").load(xml_path)
df.show()

# df = spark.read .format("com.databricks.spark.xml").option("rowTag", "job").load("/FileStore/tables/2021_06_01_13_01_32_d_kornferry-2.xml")
# df.show()

# df=spark.read.format("xml").option("rowTag","Root").load(xml_path)
# df = spark.read .format("com.databricks.spark.xml") .option("rowTag", "book") .load("/FileStore/tables/books.xml")
# df.show()

# COMMAND ----------



# COMMAND ----------

# df = spark.read.format("com.databricks.spark.xml").option("rowTag", "job").load(xml_path)
# df = spark.read.format("com.databricks.spark.xml").option("rowTag", "job").load("/mnt/dsml/linkup_data/samplexml/d_KornFerryFeed.xml")


# COMMAND ----------

# dbutils.fs.ls('/mnt')

# COMMAND ----------

