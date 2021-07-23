# Databricks notebook source
jdbcHostname = "use-ic-da-dlmi.public.6897cae55f64.database.windows.net"
jdbcDatabase = "UAM"
jdbcPort = 3342

jdbcUrl = "jdbc:sqlserver://{0}:{1};database={2}".format(jdbcHostname, jdbcPort, jdbcDatabase)
connectionProperties = {
  "user" : "DFUser01",
  "password" : dbutils.secrets.get(scope = "sqlmikeyvault-him", key = "dfuser01-sqlmanagedinstance"),
  "driver" : "com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

# COMMAND ----------

createTableQuery = """
CREATE TABLE dw.adfconfig(  
	[Source] [nvarchar](max) NULL,  
	[Source_table] [nvarchar](max) NULL,  
	[Dest_table] [nvarchar](max) NOT NULL,  
	[Columns] [nvarchar](max) NOT NULL,  
	[Watermark_Column] [varchar](max) NULL,  
	[Watermark_Value] [datetime] NULL,  
	[Enabled] [bit] NOT NULL,  
	[Load_Flag] [nvarchar] NULL,  
	[Status] [nvarchar](max) NULL,  
	[Comment] [varchar](255) NULL  
)
"""

# COMMAND ----------

pushdown_query = "select TOP 100 * from UAM.uam.Survey"
df = spark.read.jdbc(url=jdbcUrl, table=pushdown_query, properties=connectionProperties)
display(df)

# COMMAND ----------

# df = spark.read.jdbc(url=jdbcUrl, table="employees", column="emp_no", lowerBound=1, upperBound=100000, numPartitions=100)
# display(df)