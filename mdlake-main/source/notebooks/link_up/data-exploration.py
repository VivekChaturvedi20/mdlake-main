# Databricks notebook source
# storage_account_name = "dsmldevsa"
# storage_account_access_key = dbutils.secrets.get(scope = "sqlmikeyvault", key = "storage-acc-dsmldevsa")
# container_name = "dsml"
# source = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net"
# spark.conf.set(f"fs.azure.account.key.{storage_account_name}.dfs.core.windows.net", storage_account_access_key)
# # xml_path = f"{source}/linkup_data/extracted_data/Kornferry/Diff/2021-06-01 13:01:32_d_kornferry.xml"

# COMMAND ----------

diffmetadf = spark.sql("show tables from jobs_diff")
fullmetadf = spark.sql("show tables from jobs_full")
diffmetadf.show()


# COMMAND ----------

fullmetadf.show()

# COMMAND ----------

alldifftables = [x['tableName'] for x in diffmetadf.select("tableName").collect()]
allfulltables = [x['tableName'] for x in  fullmetadf.select("tableName").collect()]

# COMMAND ----------


indexlistfull = ["_".join(x.split("_")[0:3]) for x in allfulltables]
indexlistdiff = ["_".join(x.split("_")[0:3]) for x in alldifftables]

# COMMAND ----------

indexlistfull==indexlistdiff

# COMMAND ----------

alldifftables

# COMMAND ----------

allfulltables

# COMMAND ----------

fulldflist =[]
diffdflist =[]
insertdifflist=[]
deldifflist=[]
upddifflist=[]

for fulltab in allfulltables:
  fulldflist.append(spark.table("jobs_full."+fulltab))

for difftab in alldifftables:
  diffdflist.append(spark.table("jobs_diff."+difftab))
  
for difftab in alldifftables:
  insertdifflist.append(spark.sql("select * from " +"jobs_diff."+difftab + " where status= 'I'"))
  deldifflist.append(spark.sql("select * from " +"jobs_diff."+difftab + " where status= 'D'"))
  upddifflist.append(spark.sql("select * from " +"jobs_diff."+difftab + " where status= 'U'"))

# COMMAND ----------

fulldflist[0]

# COMMAND ----------

# set([x['status'] for x in diffdflist[0].select("status").collect()])
# 'D, 'I', 'U'

# COMMAND ----------

# diffdflist

# COMMAND ----------

fullcounts = []
diffcounts =[]
insdiffcounts =[]
deldiffcounts =[]
upddiffcounts =[]

for df in fulldflist:
  fullcounts.append(df.count())
  
for df in diffdflist:
  diffcounts.append(df.count())
  
for df in insertdifflist:
  insdiffcounts.append(df.count())

for df in deldifflist:
  deldiffcounts.append(df.count())
  
for df in upddifflist:
  upddiffcounts.append(df.count())

# COMMAND ----------

fullcounts

# COMMAND ----------

diffcounts

# COMMAND ----------

insdiffcounts

# COMMAND ----------

import numpy as np
import pandas as pd
statsdftrans = pd.DataFrame(np.array([fullcounts, diffcounts, insdiffcounts,deldiffcounts,upddiffcounts]))

statsdf = statsdftrans.T
statsdf.columns = ["fullcounts","diffcounts","insdiffcounts","deletediffcounts","upddiffcounts"]
statsdf.index = indexlistfull

# COMMAND ----------

statsdf

# COMMAND ----------

statsdf['nextdaycountcompare'] = statsdf['fullcounts'] - (statsdf['deletediffcounts']) + statsdf['insdiffcounts']
# statsdf['nextdaycountcompare2'] = statsdf['fullcounts'] + statsdf['insdiffcounts']
# statsdf = statsdf.drop(['nextdaycountcompare2'],axis=1)

# COMMAND ----------



# COMMAND ----------

# spark.conf.set("fs.azure.account.key.dsmldevsa.dfs.core.windows.net",dbutils.secrets.get(scope = "sqlmikeyvault", key = "storage-acc-dsmldevsa"))

# statsdfspark = spark.createDataFrame(statsdf)
# statsdfspark.write.format("com.databricks.spark.csv").option("header", "true").mode("overwrite").save("abfss://dsml@dsmldevsa.dfs.core.windows.net/testfolder2/statsdf.csv")

# COMMAND ----------

selectioncolumns = fulldflist[0].columns
selectioncolumns

# COMMAND ----------

distinctjobidfull =[]
distinctjobiddiff = []

for i in range(len(fulldflist)):
  distinctjobidfull.append(fulldflist[i].select("job_id").distinct().count())
  distinctjobiddiff.append(diffdflist[i].select("job_id").distinct().count())


# COMMAND ----------

uniondflist = []
uniondistinctcounts =[]
for i in range(len(fulldflist)):
    undf = fulldflist[i].select(selectioncolumns).union(diffdflist[i].select(selectioncolumns))
    uniondflist.append(undf)
    uniondistinctcounts.append(undf.select("job_id").distinct().count())

# COMMAND ----------

# uniondflist[3].select("job_id").distinct().count()

# COMMAND ----------



# COMMAND ----------

statsdf['distinct_job_ids_full']=distinctjobidfull
statsdf['distinct_job_ids_diff']=distinctjobiddiff
statsdf['distinct_job_ids_union_full_diff']=uniondistinctcounts

# COMMAND ----------

statsdf

# COMMAND ----------

# dfdiffcols = df_diff.columns
# set(dfdiffcols).difference(set(dffullcols))
# dfdifffiltered = df_diff.select(dffullcols)
# df_subtracted = df_full.exceptAll(dfdifffiltered)
# df_subtracted.count()
# # 4534439 - 4426887
# dfdiff_subtracted = dfdifffiltered.exceptAll(df_full)
# dfdiff_subtracted.count()
# # 198754 - 91202

# COMMAND ----------

fulldflist[0].createOrReplaceTempView("linkupdata") # Crating Temp table


# COMMAND ----------

difftab = diffdflist[0].select("status")
indf = diffdflist[0].filter(diffdflist[0].status == "I")

# COMMAND ----------

indf

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from linkupdata

# COMMAND ----------

