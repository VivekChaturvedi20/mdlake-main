CREATE PROCEDURE datalake.update_watermark @LastModifiedtime datetime, @TableName varchar(100)
AS

BEGIN
		UPDATE datalake.adfconf
		SET [Watermark_Value] = @LastModifiedtime

WHERE [Source_table] = @TableName

END