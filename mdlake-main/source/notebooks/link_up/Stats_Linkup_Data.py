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

# MAGIC %sql
# MAGIC -- CREATE DATABASE linkup_data_stats;

# COMMAND ----------

all_diff_tables_name = dict()
all_full_tables_name = dict()
for i in alldifftables:
  all_diff_tables_name[i[0:19]] = {"table_name": f"jobs_diff.{i}", "df":spark.sql(f"select * from jobs_diff.{i}")}
print(all_diff_tables_name)
print("=======================")
for i in allfulltables:
  all_full_tables_name[i[0:19]] = {"table_name": f"jobs_full.{i}", "df":spark.sql(f"select * from jobs_full.{i}")}
print(all_full_tables_name)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- CREATE TABLE linkup_data_stats.linkup_data_stats (table_name STRING, table_date STRING, total_count INT, insert_count INT, update_count INT, delete_count STRING)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) FROM jobs_diff.2021_05_30_10_48_20_d_kornferryfeed where status="D"

# COMMAND ----------

insert_query = "INSERT INTO linkup_data_stats.linkup_data_stats VALUES ('{table_name}','{table_date}', {total_count}, {insert_count}, {update_count}, {delete_count});"

for key, value in all_diff_tables_name.items():
  table_name = value["table_name"]
  table_date = key
  df = value["df"]
  total_count = df.count()
  insert_count = df.filter(df.status == "I").count()
  update_count = df.filter(df.status == "U").count()
  delete_count = df.filter(df.status == "D").count()
  query = insert_query.format(table_name=table_name, table_date=table_date, total_count=total_count, insert_count=insert_count, update_count=update_count, delete_count=delete_count)
  print(query)
#   spark.sql(query)


for key, value in all_full_tables_name.items():
  table_name = value["table_name"]
  table_date = key
  df = value["df"]
  total_count = df.count()
  insert_count = 0
  update_count = 0
  delete_count = 0
  query = insert_query.format(table_name=table_name, table_date=table_date, total_count=total_count, insert_count=insert_count, update_count=update_count, delete_count=delete_count)
  print(query)
#   spark.sql(query)

# COMMAND ----------

diff_df = all_diff_tables_name["2021_05_31_11_02_19"]["df"]
print("DIFF TOTAL COUNT",diff_df.count())

diff_delete_df = diff_df.filter(diff_df.status == "D")
print("DIFF DELETE COUNT",diff_delete_df.count())

diff_insert_df = diff_df.filter(diff_df.status == "I")
print("DIFF Insert COUNT",diff_insert_df.count())

diff_update_df = diff_df.filter(diff_df.status == "U")
print("DIFF update COUNT",diff_update_df.count())

full_df = all_full_tables_name["2021_05_31_11_02_19"]["df"]
print("TOTAL FULL COUNT", full_df.count())

display(diff_insert_df)


# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM jobs_diff.2021_05_30_10_48_20_d_kornferryfeed where status='D';
# MAGIC SELECT COUNT(*) FROM jobs_diff.2021_05_30_10_48_20_d_kornferryfeed where status='D';

# COMMAND ----------

th_diff_df = all_diff_tables_name["2021_05_30_10_48_20"]["df"]
print("DIFF TOTAL COUNT",diff_df.count())

diff_delete_df = th_diff_df.filter(diff_df.status == "D")
print("DIFF DELETE COUNT",diff_delete_df.count())

diff_insert_df = th_diff_df.filter(diff_df.status == "I")
print("DIFF Insert COUNT",diff_insert_df.count())

diff_update_df = th_diff_df.filter(diff_df.status == "U")
print("DIFF update COUNT",diff_update_df.count())

# COMMAND ----------

full_linkup_stats = spark.sql("SELECT * FROM linkup_data_stats.linkup_data_stats WHERE table_name LIKE 'jobs_full%' ORDER BY table_date")
diff_linkup_stats = spark.sql("SELECT * FROM linkup_data_stats.linkup_data_stats WHERE table_name  LIKE 'jobs_diff%' ORDER BY table_date")
display(full_linkup_stats)
display(diff_linkup_stats)

# COMMAND ----------

4574369
print(102937+69977)

# COMMAND ----------

for i, j in all_diff_tables_name.items():
all_full_tables_name