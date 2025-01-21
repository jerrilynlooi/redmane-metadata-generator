# REDMANE Metadata Generator
### Data Ingestion Team

1. Set parameters in **params.py**
This would be replaced by calling of REDMANE Data Registry API.
Tells the script what filetypes to look for.

2. To run:
`python update_local.py /path/to/directory`
--> generates **output.json**

Currently:
- lists filenames of matching filetypes for raw/processed/summarised
To Implement:
- mapping of sampleId and patientId (likely using another constants file - to replace with API)
- generating of file object for JSON
- searching of subdirectories for files

## Files
**update_local.py** script
**params.py** set parameters here
**template.json** example of what output.json should be formatted like
**.gitignore**