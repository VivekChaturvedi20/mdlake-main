## AryaProfiles- ADF pipeline for extraction of zip data

### How to run
- Copy the new zip files to aryaprofiles storageaccount under sampledata/profiles/ directory
- Run the zipextraction pipeline from Azure data factory (adf.azure.com )
- Pipeline processes all the zip files in the profiles directory, extracts them to the storage account dsmldevsa in path dsml/aryaprofiles/extracted_zip_data
- Once a zip file is successfully extracted, the pipeline moves the source zip file present in the storage account aryaprofiles to the path sampledata/adfprocessedzips, so that it doesn't get processed in the future again

### ADF - Pipeline Data Sources
There are 4 data sources defined for ADF pipeline for Aryaprofiles : -
- AryaDatalakeSink - Specifies the destination Data lake gen 2 path - dsml/aryaprofiles/extracted_zip_data
- AryaProfilesSource - Specifies the source path but with ZIPDeflate option (for extraction)
- AryaProfilesMoveZIPSource - Specifies source zip folder path path without Zipdeflate option (for moving after extraction is complete)
- AryaProfilesMoveZIPSink - Specifies destination directory path where the source zip file is to be moved once the extraction finishes.

### ADF - Pipeline Activities
There are total 4 activities in the pipeline
- Get Metadata Activity - to obtain the list of zip files available in the source directory
- For Each Activity - to run copy operation for all zip files (Operations are performed parallely)
- Extract (Copy Data Activity)- For extraction of each zip file (present inside For Each)
- Move (Copy Data Activity) -  For moving source zip files once extraction finishes successfully (present inside For Each)