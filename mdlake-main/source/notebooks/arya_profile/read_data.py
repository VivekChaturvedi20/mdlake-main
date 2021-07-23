# Databricks notebook source
# MAGIC %sql
# MAGIC SET spark.databricks.delta.formatCheck.enabled=false

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE DATABASE IF NOT EXISTS  aryaprofiles

# COMMAND ----------

from pyspark.sql.functions import explode


storage_account_name = "dsmldevsa"
storage_account_access_key = dbutils.secrets.get(scope = "sqlmikeyvault", key = "storage-acc-dsmldevsa")
container_name = "dsml"
source = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net"
parent_folder_location = f"{source}/aryaprofiles/extracted_zip_data"
processed_folder = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net/aryaprofiles/processed_zip_data/"
db_name = "aryaprofiles"


spark.conf.set(f"fs.azure.account.key.{storage_account_name}.dfs.core.windows.net", storage_account_access_key)

# COMMAND ----------



for child_path in dbutils.fs.ls(parent_folder_location): # Loading all the parent folder
  folder_path = child_path.path # Getting JSON file path
  folder_name = folder_path.split("/")[-2].split(".")[0].replace("-","_") # extracting table name
  print(f"Starting process for batch {folder_name}")
  df = spark.read.json(f"{folder_path}/*.json") # Reading Dataframe for the all the files in the directory
  print(f"Step 1: Dataframe for {folder_name} is readed scuessfully!!")
  profile_data_df = df.select("Profiles", explode("Profiles").alias("Profilesexplode")).select("Profilesexplode.*") # Exploding the profile from the JSON
  print(f"Step 2: Dataframe for {folder_name} Profile exploded scuessfully!!")
  profile_data_df.createOrReplaceTempView(folder_name) # Crating Temp table
  table = spark.table(folder_name) # Create spark table
  writing_folder = f"{processed_folder}{folder_name}" 
  print("Step 3: Dataframe is converted into delta table sucessfully")
  dbutils.fs.mkdirs(writing_folder) # Making the dirs according 
  table.write.format("delta").save(writing_folder) # Writing table in asd file storage
  print(f"Step 4: Delta Table is written sucessfully on path {writing_folder}")
  table.write.format("delta").saveAsTable(f"{db_name}.{folder_name}")
  print(f"Step 5: Delta Table is created sucessfully in DBFS --> {db_name}.{folder_name})
  print("==========================================================================")
  print()

# COMMAND ----------

# from pyspark.sql.functions import explode


# storage_account_name = "dsmldevsa"
# storage_account_access_key = "LMbJexHtqCPh16CaNhNAT9v4LD1cZhaGd2tGRbS4+SyAgy5z+Embf/DsC/a5VMZOcfQAAEqRJ5s8GNERWr1ywA=="
# container_name = "dsml"
# source = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net"
# parent_folder_location = f"{source}/aryaprofiles/extracted_zip_data"
# processed_folder = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net/aryaprofiles/processed_zip_data/"

# spark.conf.set(f"fs.azure.account.key.{storage_account_name}.dfs.core.windows.net", storage_account_access_key)


# for child_path in dbutils.fs.ls(processed_folder):
#   delta_table_path = child_path.path
#   print(f"Step 1: Starting Process for --> {delta_table_path}")
#   table_name = "aryaprofiles."+delta_table_path.split("/")[-2]
#   print(f"Step 2: Table name for {table_name}")
#   asdl_delta_table = spark.read.format("delta").load(delta_table_path)
#   print(f"Step 3: Dataframe is readed sucessfully!!")
#   asdl_delta_table.write.format("delta").saveAsTable(table_name)
#   print(f"Step 4: Table is write is sucessfully!!")
#   print("=====================================================================")
#   print()

# COMMAND ----------

df = spark.read.csv("abfss://dsml@dsmldevsa.dfs.core.windows.net/mi_data/datawarehouse_db/dw.Currency")

# COMMAND ----------

df.show()

# COMMAND ----------

