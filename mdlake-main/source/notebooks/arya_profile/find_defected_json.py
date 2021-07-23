# Databricks notebook source
storage_account_name = "dsmldevsa"
storage_account_access_key = dbutils.secrets.get(scope = "sqlmikeyvault", key = "storage-acc-dsmldevsa")
container_name = "dsml"
source = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net"
parent_folder_location = f"{source}/aryaprofiles/extracted_zip_data/batch-5.zip/"
processed_folder = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net/aryaprofiles/processed_zip_data/batch_5"

spark.conf.set(f"fs.azure.account.key.{storage_account_name}.dfs.core.windows.net", storage_account_access_key)

# COMMAND ----------

from pyspark.sql.functions import explode
###

storage_account_name = "dsmldevsa"
storage_account_access_key = dbutils.secrets.get(scope = "sqlmikeyvault", key = "storage-acc-dsmldevsa")
container_name = "dsml"
source = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net"
parent_folder_location = f"{source}/aryaprofiles/extracted_zip_data/batch-5.zip/"
processed_folder = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net/aryaprofiles/processed_zip_data/batch_5"

spark.conf.set(f"fs.azure.account.key.{storage_account_name}.dfs.core.windows.net", storage_account_access_key)
  
dbutils.fs.mkdirs(processed_folder)

list_of_dfs = list()
for i in dbutils.fs.ls(parent_folder_location):
  print(f"Reading JSON File {i.path}")
  try:
      df = spark.read.json(i.path)
      profile_data_df = df.select("Profiles", explode("Profiles").alias("Profilesexplode")).select("Profilesexplode.*")
      profile_data_df.write.format("delta").mode("append").save(processed_folder) # Writing table in asd file storage
      profile_data_df.write.format("delta").mode("append").saveAsTable("aryaprofiles.batch_5")
  except Exception as err:
    print(err)
    pass



# COMMAND ----------

from pyspark.sql.functions import explode


  
dbutils.fs.mkdirs(processed_folder)


df = spark.read.json("abfss://dsml@dsmldevsa.dfs.core.windows.net/aryaprofiles/extracted_zip_data/batch-5.zip/DataFile-2147.json")
profile_data_df = df.select("Profiles", explode("Profiles").alias("Profilesexplode")).select("Profilesexplode.*")
profile_data_df.write.format("delta").mode("append").option("mergeSchema", "true").save(processed_folder)
profile_data_df.write.format("delta").mode("append").option("mergeSchema", "true").saveAsTable("aryaprofiles.batch_5")


# COMMAND ----------

