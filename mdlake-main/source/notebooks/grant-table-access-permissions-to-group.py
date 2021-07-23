# Databricks notebook source
# MAGIC %sql
# MAGIC 
# MAGIC GRANT USAGE ON DATABASE aryaprofiles TO dsml;
# MAGIC GRANT SELECT ON DATABASE aryaprofiles TO dsml;
# MAGIC GRANT READ_METADATA ON DATABASE aryaprofiles TO dsml;

# COMMAND ----------

# MAGIC %sql
# MAGIC 
# MAGIC GRANT USAGE ON DATABASE datawarehouse TO dsml;
# MAGIC GRANT SELECT ON DATABASE datawarehouse TO dsml;
# MAGIC GRANT READ_METADATA ON DATABASE datawarehouse TO dsml;

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW GRANT dsml ON DATABASE datawarehouse

# COMMAND ----------

# MAGIC %sql
# MAGIC 
# MAGIC GRANT USAGE ON DATABASE uam TO dsml;
# MAGIC GRANT SELECT ON DATABASE uam TO dsml;
# MAGIC GRANT READ_METADATA ON DATABASE uam TO dsml;

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW GRANT dsml ON DATABASE uam

# COMMAND ----------

