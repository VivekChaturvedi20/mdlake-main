# Databricks notebook source
# Intalizing all the variables
storage_account_name = "dsmldevsa"
storage_account_access_key = dbutils.secrets.get(scope = "sqlmikeyvault", key = "storage-acc-dsmldevsa")
container_name = "dsml"
source = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net"

# spark.conf.set(f"fs.azure.account.key.{storage_account_name}.dfs.core.windows.net", storage_account_access_key)

parent_folder = f"{source}/s3datafiles/s3paydata"

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE DATABASE IF NOT EXISTS  aws_country_data;
# MAGIC -- DROP DATABASE IF EXISTS aws_country_data CASCADE;

# COMMAND ----------

import re
from pyspark.sql.functions import col


for country_folder in dbutils.fs.ls(parent_folder):
  print("=====================",country_folder.path,"==============================")
  country_name = country_folder.name.replace("/","")
  print("COUNTRY NAME", country_name)
  df = None
  for country_folder_file in dbutils.fs.ls(country_folder.path):
    if country_folder_file.name != "log.txt":
      if ".xlsx" in country_folder_file.name:
        print(country_folder_file.path)
        print(country_folder_file.name)
        sparkDF = spark.read.format("com.crealytics.spark.excel").option("header", "true").option("inferSchema", True).load(country_folder_file.path)

      elif ".csv" in country_folder_file.name:
        print(country_folder_file.path)
        print(country_folder_file.name)
        sparkDF = spark.read.option("header", "true").option("inferSchema", True).csv(country_folder_file.path)
      # Updating Col names
      old_col = sparkDF.columns
      print("OLD COL --> ",old_col)
      new_col = [re.sub('\W+','_', i) for i in sparkDF.columns]
      mapping = dict(zip(old_col, new_col))
      sparkDF = sparkDF.select([col(c).alias(mapping.get(c, c)) for c in sparkDF.columns])
      print("NEW COL --> ",sparkDF.columns)    
      # Making Table Name as per the convention
      table_name = re.sub('\W+','_', country_folder_file.name)
      table_name = f'aws_country_data.{country_name}_{table_name}'
      print("FINAL TABLE --> ",table_name)
      sparkDF.write.format("delta").saveAsTable(table_name)
      print("Yheeeeeeeah!! Table is created")
      print()
  print()



# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLE aws