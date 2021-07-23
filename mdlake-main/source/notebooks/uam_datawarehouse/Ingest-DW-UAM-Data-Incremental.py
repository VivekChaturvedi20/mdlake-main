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

# Primary keys required for dw and uam can be obtained by running below sql query in the managed instance for DataWarehouse and UAM databases separately and the exporting the results as csv files dw_primarykeys.csv and uam_primarykeys.csv
"""
select schema_name(tab.schema_id) as [schema_name], 
    pk.[name] as pk_name,
    ic.index_column_id as column_id,
    col.[name] as column_name, 
    tab.[name] as table_name
from sys.tables tab
    inner join sys.indexes pk
        on tab.object_id = pk.object_id 
        and pk.is_primary_key = 1
    inner join sys.index_columns ic
        on ic.object_id = pk.object_id
        and ic.index_id = pk.index_id
    inner join sys.columns col
        on pk.object_id = col.object_id
        and col.column_id = ic.column_id
order by schema_name(tab.schema_id),
    pk.[name],
    ic.index_column_id

"""


primarykeyspath = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net/mi_data/primarykeysdata/"
dwprimarykeycsvpath = primarykeyspath + "dw_primarykeys.csv"
uamprimarykeyscsvpath = primarykeyspath + "uam_primarykeys.csv"
dwprimarydf = spark.read.option("header", "false").option("inferSchema", "true").csv(dwprimarykeycsvpath)
uamprimarydf = spark.read.option("header", "false").option("inferSchema", "true").csv(uamprimarykeyscsvpath)
dwprimarypdf = dwprimarydf.toPandas()
uamprimarypdf = uamprimarydf.toPandas()
cols = ['schema','pk_name','col_id','keycol','tablename']
dwprimarypdf.columns = cols
uamprimarypdf.columns =cols
dwprimarypdf['fulltablename'] = dwprimarypdf['schema'] +"_" +dwprimarypdf['tablename']
uamprimarypdf['fulltablename'] = uamprimarypdf['schema'] +"_" +uamprimarypdf['tablename']

# COMMAND ----------

# uamprimarypdf

# COMMAND ----------

def mergeall(fulltablepath,mergetabname,condition):
#   condition = fulltablepath +".jobid = " + mergetabname +".jobid"

  mergequery = """

  MERGE INTO {fulltablepath}
  USING {mergedifftable}
  ON {Condition}
  WHEN MATCHED THEN
    UPDATE SET *
  WHEN NOT MATCHED
    THEN INSERT *

            """.format(fulltablepath=fulltablepath,mergedifftable= mergetabname,Condition=condition)
  
  print("Running query ",mergequery)
  spark.sql(mergequery)
  
  
  print("Merge Done sucessfully!!")
  pass

# COMMAND ----------

# For UAM DB

uam_db = f"{source}/mi_data/uam_db"
uam_db_processed_folder = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net/mi_data/processed_data/uam"
uam_database_name = "uam"

# for child_path in dbutils.fs.ls(uam_db)[:5]:
for child_path in dbutils.fs.ls(uam_db):
  file_path = child_path.path
  table_name = child_path.path.split("/")[-1].replace(".", "_")
  table_name_with_DB = f'{uam_database_name}.{table_name}'
  processed_folder = f"{uam_db_processed_folder}/{table_name}"
  print("---",file_path)
  print(f"Step 1: Starting process for --> {table_name}")
  df = spark.read.option("header", "true").option("inferSchema", "true").csv(file_path)
  print("Step 2: CSV read sucessfully!!")
  
  resultdf = uamprimarypdf[uamprimarypdf["fulltablename"]==table_name]
  if (resultdf.shape[0]==0):
    print("initiating merge using all columns..")
    keyvalues= df.columns
    fulltablepath = table_name_with_DB    
    mergetabname="mergetable"    
    mergecondition = fulltablepath +"." + keyvalues[0] + " = " + mergetabname + "." + keyvalues[0]
    df.createOrReplaceTempView(mergetabname)
    if resultdf['keycol'].shape[0]>1:
      for keyv in resultdf['keycol'].values[1:]:
        mergecondition = mergecondition + " AND " + fulltablepath +"." + keyv + " = " + mergetabname + "." + keyv
        
    try:
      mergeall(fulltablepath,mergetabname,mergecondition)
    except:
      import traceback
      traceback.print_exc()
        
  if resultdf.shape[0]!=0:
    print("initiating merge using primary key columns..")
    keyvalues = resultdf['keycol'].values
    fulltablepath = table_name_with_DB    
    mergetabname="mergetable"    
    
    initkeyval = resultdf['keycol'].values[0]
#     df = df.dropDuplicates(keyvalues)
    df.createOrReplaceTempView(mergetabname)
    mergecondition = fulltablepath +"." + initkeyval + " = " + mergetabname + "." + initkeyval
    if resultdf['keycol'].shape[0]>1:
      for keyv in resultdf['keycol'].values[1:]:
        mergecondition = mergecondition + " AND " + fulltablepath +"." + keyv + " = " + mergetabname + "." + keyv
    try:
      mergeall(fulltablepath,mergetabname,mergecondition)
    except:
      import traceback
#       traceback.print_exc()
      print("duplicates found, dropping duplicates and retrying...")
      df = df.dropDuplicates(keyvalues)
      df.createOrReplaceTempView(mergetabname)
      mergeall(fulltablepath,mergetabname,mergecondition)
  print("-------------------------------")


# COMMAND ----------

# For DATAWAREHOUSE DB

datawarehouse_db = f"{source}/mi_data/datawarehouse_db"
datawarehouse_db_processed_folder = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net/mi_data/processed_data/datawarehouse_db"
datawarehouse_database_name = "datawarehouse"

# for child_path in dbutils.fs.ls(datawarehouse_db)[1:2]:
for child_path in dbutils.fs.ls(datawarehouse_db):
  file_path = child_path.path
  table_name = child_path.path.split("/")[-1].replace(".", "_")
  table_name_with_DB = f'{datawarehouse_database_name}.{table_name}'
  processed_folder = f"{datawarehouse_db_processed_folder}/{table_name}"
  print(file_path)
  print(f"Step 1: Starting process for --> {table_name}")
  df = spark.read.option("header", "true").option("inferSchema", "true").csv(file_path)
  print("Step 2: CSV readed sucessfully!!")
  resultdf = dwprimarypdf[dwprimarypdf["fulltablename"]==table_name]
  
  if (resultdf.shape[0]==0):
    print("initiating merge using all columns..")
    keyvalues= df.columns
    fulltablepath = table_name_with_DB    
    mergetabname="mergetable"    
    mergecondition = fulltablepath +"." + keyvalues[0] + " = " + mergetabname + "." + keyvalues[0]
    df.createOrReplaceTempView(mergetabname)
    if resultdf['keycol'].shape[0]>1:
      for keyv in resultdf['keycol'].values[1:]:
        mergecondition = mergecondition + " AND " + fulltablepath +"." + keyv + " = " + mergetabname + "." + keyv
        
    try:
      mergeall(fulltablepath,mergetabname,mergecondition)
    except:
      import traceback
      traceback.print_exc()
  
  if resultdf.shape[0]!=0:
    print("initiating merge using primary key columns..")
    keyvalues = resultdf['keycol'].values
    fulltablepath = table_name_with_DB    
    mergetabname="mergetable"    
    
    initkeyval = resultdf['keycol'].values[0]
#     df = df.dropDuplicates(keyvalues)
    df.createOrReplaceTempView(mergetabname)
    mergecondition = fulltablepath +"." + initkeyval + " = " + mergetabname + "." + initkeyval
    if resultdf['keycol'].shape[0]>1:
      for keyv in resultdf['keycol'].values[1:]:
        mergecondition = mergecondition + " AND " + fulltablepath +"." + keyv + " = " + mergetabname + "." + keyv
    try:
      mergeall(fulltablepath,mergetabname,mergecondition)
      
    except:
      import traceback
#       traceback.print_exc()
      print("duplicates found, dropping duplicates and retrying...")      
      df = df.dropDuplicates(keyvalues)
      df.createOrReplaceTempView(mergetabname)
      mergeall(fulltablepath,mergetabname,mergecondition)
     
    
  print("-------------------------------")
  

# COMMAND ----------

# testdf = spark.table("mergetable")
# clientkvalues = [x['ClientKey'] for x in testdf.select("ClientKey").collect()]
# len(clientkvalues)
# len(set(clientkvalues))



# COMMAND ----------

# %sql
# SELECT ClientKey, COUNT(*)
# FROM mergetable
# GROUP BY ClientKey
# HAVING COUNT(*) > 1


# COMMAND ----------

