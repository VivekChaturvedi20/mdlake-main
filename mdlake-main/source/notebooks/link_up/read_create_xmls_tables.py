# Databricks notebook source
# Intalizing all the variables
storage_account_name = "dsmldevsa"
storage_account_access_key = dbutils.secrets.get(scope = "sqlmikeyvault", key = "storage-acc-dsmldevsa")
container_name = "dsml"
source = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net"

spark.conf.set(f"fs.azure.account.key.{storage_account_name}.dfs.core.windows.net", storage_account_access_key)

linkup_data_path = f"{source}/linkup_data/extracted_data/Kornferry/"
dbfs_data_path = "/mnt/Kornferry/"
dbutils.fs.mkdirs(dbfs_data_path)

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE DATABASE IF NOT EXISTS  jobs_full;
# MAGIC CREATE DATABASE IF NOT EXISTS  jobs_diff;

# COMMAND ----------

# Fteching all the dir form adls for full and diff
linkup_data_full_path = None
linkup_data_diff_path = None

for i in dbutils.fs.ls(linkup_data_path):
  if i.name == 'Full/':
    linkup_data_full_path = dbutils.fs.ls(i.path)
  elif i.name == 'Diff/':
    linkup_data_diff_path = dbutils.fs.ls(i.path)

# Creating seprate dir in dbfs in full and diff
dbfs_full_data_path = f"{dbfs_data_path}/full"
dbfs_diff_data_path = f"{dbfs_data_path}/diff"
dbutils.fs.mkdirs(dbfs_full_data_path)
dbutils.fs.mkdirs(dbfs_diff_data_path)

# # Copying all the files (DIFF and FULL) from adls --> dbfs
# print("============ FULL PATH ===================")
# for i in linkup_data_full_path:
#   print(f"Step 1: Initating process for --> {i.path}")
#   file_path = f'{dbfs_full_data_path}/{i.name.replace(" ", "_").replace(":", "_").replace("-", "_")}'
#   dbutils.fs.mkdirs(file_path)
#   print(f"Step 2: Directory is create in DBFS --> {file_path}")
#   print("Step 3: Start making copies and creating Delta tables")
#   for j in dbutils.fs.ls(i.path):
#     file_name = j.name.replace(" ", "_").replace(":", "_").replace("-", "_")
#     dbfs_file_path = f"{file_path}{file_name}"
#     dbutils.fs.cp(j.path, dbfs_file_path)
#     print(f"file is copy from --> {j.path} to --> {dbfs_file_path}")
#     df = spark.read .format("com.databricks.spark.xml").option("rowTag", "job").load(dbfs_file_path)
#     print(f"Data is readed sucessfully for {dbfs_file_path}")
#     df.write.format("delta").saveAsTable(f'jobs_full.{file_name.replace(".xml", "")}')
#     print(f'DF is written sucessfully in delta table {file_name.replace(".xml", "")}')
#     print("=============================================")
#   print()
    

# print("============ DIFF PATH ===================")
# for i in linkup_data_diff_path:
#   print(f"Step 1: Initating process for --> {i.path}")
#   file_path = f'{dbfs_diff_data_path}/{i.name.replace(" ", "_").replace(":", "_").replace("-", "_")}'
#   dbutils.fs.mkdirs(file_path)
#   print(f"Step 2: Directory is create in DBFS --> {file_path}")
#   print("Step 3: Start making copies and creating Delta tables")
#   for j in dbutils.fs.ls(i.path):
#     file_name = j.name.replace(" ", "_").replace(":", "_").replace("-", "_")
#     dbfs_file_path = f"{file_path}{file_name}"
#     dbutils.fs.cp(j.path, dbfs_file_path)
#     print(f"file is copy from --> {j.path} to --> {dbfs_file_path}")
#     df = spark.read .format("com.databricks.spark.xml").option("rowTag", "job").load(dbfs_file_path)
#     print(f"Data is readed sucessfully for {dbfs_file_path}")
#     df.write.format("delta").saveAsTable(f'jobs_diff.{file_name.replace(".xml", "")}')
#     print(f'DF is written sucessfully in delta tables {file_name.replace(".xml", "")}')
#     print("=============================================")
#   print()

# COMMAND ----------

dbfs_diff = "/mnt/Kornferry/diff"
dbfs_full = "/mnt/Kornferry/full"
# diff_30 = f"{source}/linkup_data/extracted_data/Kornferry/Diff/2021-05-30 10:48:20/2021-05-30 10:48:20_d_KornFerryFeed.xml"
# diff_31 = f"{source}/linkup_data/extracted_data/Kornferry/Diff/2021-05-31 11:02:19/2021-05-31 11:02:19_d_KornFerryFeed.xml"
# full_30 = f"{source}/linkup_data/extracted_data/Kornferry/Full/2021-05-30 10:48:20/2021-05-30 10:48:20_KornFerryFeed.xml"
# full_31 = f"{source}/linkup_data/extracted_data/Kornferry/Full/2021-05-31 11:02:19/2021-05-31 11:02:19_KornFerryFeed.xml"
# dbutils.fs.cp(diff_30, f"{dbfs_diff}/2021_05_30_10_48_20_d_KornFerryFeed.xml")
# dbutils.fs.cp(diff_31, f"{dbfs_diff}/2021_05_31_11_02_19_d_KornFerryFeed.xml")
# dbutils.fs.cp(full_30, f"{dbfs_full}/2021_05_30_10_48_20_KornFerryFeed.xml")
# dbutils.fs.cp(full_31, f"{dbfs_full}/2021_05_31_11_02_19_KornFerryFeed.xml")

# df = spark.read .format("com.databricks.spark.xml").option("rowTag", "job").load(diff_30)
# df.show()

# COMMAND ----------

# for i in dbutils.fs.ls(dbfs_diff):
#   df = spark.read .format("com.databricks.spark.xml").option("rowTag", "job").load(i.path)
#   df.write.format("delta").saveAsTable(f'jobs_diff.{i.name.replace(".xml", "")}')

for i in dbutils.fs.ls(dbfs_full):
  df = spark.read .format("com.databricks.spark.xml").option("rowTag", "job").load(i.path)
  df.write.format("delta").saveAsTable(f'jobs_full.{i.name.replace(".xml", "")}')


# COMMAND ----------

dbutils.fs.rm(dbfs_data_path, recurse=True)

# COMMAND ----------

