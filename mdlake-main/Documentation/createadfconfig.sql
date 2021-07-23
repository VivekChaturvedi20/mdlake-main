
Create Schema datalake

CREATE TABLE datalake.adfconf(  
	[Source] [nvarchar](100) NULL,  
	[Source_table] [nvarchar](100) NULL,  
	[Dest_table] [nvarchar](100) NOT NULL,  
	[Columns] [nvarchar](100) NOT NULL,  
	[Watermark_Column] [varchar](100) NULL,  
	[Watermark_Value] [datetime] NULL,  
	[Enabled] [int] NOT NULL,  
	[Load_Flag] [nvarchar](100) NULL,  
	[Status] [nvarchar](50) NULL,  
	[Comment] [varchar](255) NULL  
)



