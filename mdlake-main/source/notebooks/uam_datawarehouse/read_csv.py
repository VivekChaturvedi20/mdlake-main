# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE DATABASE IF NOT EXISTS uam;
# MAGIC CREATE DATABASE IF NOT EXISTS datawarehouse;

# COMMAND ----------

storage_account_name = "dsmldevsa"
storage_account_access_key = dbutils.secrets.get(scope = "sqlmikeyvault", key = "storage-acc-dsmldevsa")
container_name = "dsml"
source = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net"
spark.conf.set(f"fs.azure.account.key.{storage_account_name}.dfs.core.windows.net", storage_account_access_key)


# COMMAND ----------

# For UAM DB

uam_db = f"{source}/mi_data/uam_db"
uam_db_processed_folder = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net/mi_data/processed_data/uam"
uam_database_name = "uam"

for child_path in dbutils.fs.ls(uam_db):
  file_path = child_path.path
  table_name = child_path.path.split("/")[-1].replace(".", "_")
  table_name_with_DB = f'{uam_database_name}.{table_name}'
  processed_folder = f"{uam_db_processed_folder}/{table_name}"
  print(file_path)
  print(f"Step 1: Starting process for --> {table_name}")
  df = spark.read.option("header", "true").option("inferSchema", "true").csv(file_path)
  print("Step 2: CSV readed sucessfully!!")
  df.createOrReplaceTempView(table_name) # Crating Temp table
  table = spark.table(table_name) # Create spark table
  print("Step 4: Making table is successfully!!")
  dbutils.fs.mkdirs(processed_folder)
  print("Step 4: Making directory sucessfully!!")
  table.write.format("delta").save(processed_folder) # Writing table in asd file storage
  print("Step 5: Writing data into adls storage")
  table.write.format("delta").saveAsTable(table_name_with_DB)
  print("Step 5: Table is saved into the delta table sucessfully!!")
  print("ALl DONE SUCESSFULLY")
  print()

  

# COMMAND ----------

# For DATAWAREHOUSE DB

datawarehouse_db = f"{source}/mi_data/datawarehouse_db"
datawarehouse_db_processed_folder = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net/mi_data/processed_data/datawarehouse_db"
datawarehouse_database_name = "datawarehouse"

for child_path in dbutils.fs.ls(datawarehouse_db):
  file_path = child_path.path
  table_name = child_path.path.split("/")[-1].replace(".", "_")
  table_name_with_DB = f'{datawarehouse_database_name}.{table_name}'
  processed_folder = f"{datawarehouse_db_processed_folder}/{table_name}"
  print(file_path)
  print(f"Step 1: Starting process for --> {table_name}")
  df = spark.read.option("header", "true").option("inferSchema", "true").csv(file_path)
  print("Step 2: CSV readed sucessfully!!")
  df.createOrReplaceTempView(table_name) # Crating Temp table
  table = spark.table(table_name) # Create spark table
  print("Step 4: Making table is successfully!!")
  dbutils.fs.mkdirs(processed_folder)
  print("Step 4: Making directory sucessfully!!")
  table.write.format("delta").save(processed_folder) # Writing table in asd file storage
  print("Step 5: Writing data into adls storage")
  table.write.format("delta").saveAsTable(table_name_with_DB)
  print("Step 5: Table is saved into the delta table sucessfully!!")
  print("ALl DONE SUCESSFULLY")
  print()
  

# COMMAND ----------

