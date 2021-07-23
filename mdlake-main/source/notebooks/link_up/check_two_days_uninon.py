# Databricks notebook source
diff_df = spark.sql("SELECT State, city, company_name, country, description, direct_url, job_id, naics_code, naics_description, onet_occupation_code, onet_occupation_name, postedDate, title FROM jobs_diff.2021_06_10_10_58_11_d_kornferryfeed where status='I' or status='U'")

full_df = spark.sql("SELECT * FROM jobs_full.2021_06_10_10_58_11_kornferryfeed")

print(diff_df.count())
print(full_df.count())

# COMMAND ----------

intersect_df = full_df.intersect(diff_df)
print(intersect_df.count())

# COMMAND ----------

print(4605573-286672)

# COMMAND ----------

left_join = full_df.join(diff_df, full_df.job_id == diff_df.job_id)
print(left_join.count())

# COMMAND ----------

full_df_nine = spark.sql("SELECT * FROM jobs_full.2021_06_09_10_48_07_kornferryfeed")
print(full_df_nine.count())
full_full_join = full_df.join(full_df_nine, full_df.job_id == full_df_nine.job_id)
print(full_full_join.count())


# COMMAND ----------

print(4571127-4398219)

# COMMAND ----------

diff_df_a = spark.sql("SELECT State, city, company_name, country, description, direct_url, job_id, naics_code, naics_description, onet_occupation_code, onet_occupation_name, postedDate, title FROM jobs_diff.2021_06_10_10_58_11_d_kornferryfeed where status='I'")
print(diff_df_a.count())

# COMMAND ----------

print(286672-206462)

# COMMAND ----------

