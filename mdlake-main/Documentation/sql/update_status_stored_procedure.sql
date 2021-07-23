CREATE PROCEDURE datalake.update_watermark @Status varchar(100), @TableName varchar(100)
AS

BEGIN
		UPDATE datalake.adfconf
		SET [Status] = @Status

WHERE [Source_table] = @TableName

END