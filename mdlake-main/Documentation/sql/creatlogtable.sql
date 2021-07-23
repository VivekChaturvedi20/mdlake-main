Use DataLake
SET ANSI_NULLS ON
GO
 
SET QUOTED_IDENTIFIER ON
GO
 
CREATE TABLE [datalake].[pipeline_log](
   [DataFactory_Name] [nvarchar](500) NULL,
   [Pipeline_Name] [nvarchar](500) NULL,
   [RunId] [nvarchar](500) NULL,
   [Source] [nvarchar](500) NULL,
   [Destination] [nvarchar](500) NULL,
   [LoadType] [nvarchar](500) NULL,
   [Status] [nvarchar](500) NULL,
   [TriggerType] [nvarchar](500) NULL,
   [TriggerId] [nvarchar](500) NULL,
   [TriggerName] [nvarchar](500) NULL,
   [TriggerTime] [nvarchar](500) NULL,
   [rowsCopied] [nvarchar](500) NULL,
   [RowsRead] [int] NULL,
   [No_ParallelCopies] [int] NULL,
   [copyDuration_in_secs] [nvarchar](500) NULL,
   [effectiveIntegrationRuntime] [nvarchar](500) NULL,
   [Source_Type] [nvarchar](500) NULL,
   [Sink_Type] [nvarchar](500) NULL,
   [Execution_Status] [nvarchar](500) NULL,
   [CopyActivity_Start_Time] [datetime] NULL,
   [CopyActivity_End_Time] [datetime] NULL,
   [CopyActivity_queuingDuration_in_secs] [nvarchar](500) NULL,
   [CopyActivity_timeToFirstByte_in_secs] [nvarchar](500) NULL,
   [CopyActivity_transferDuration_in_secs] [nvarchar](500) NULL
) ON [PRIMARY]
GO