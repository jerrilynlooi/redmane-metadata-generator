# REDMANE Metadata Generator
by Data Ingestion Team

### 1 - Set parameters in `params.py`
- This would be replaced by calling of REDMANE Data Registry API.
- Tells the script what filetypes to look for.

### 2 - To run:
- `python update_local.py /path/to/directory`
- --> generates `output.json` and `output.html`

Output:
- searches directory and subdirectories for files with matching filetype for raw/processed/summarised
- maps to matching sampleId and patient based on filename (to replace with API)
- generates summary of files found to output.json
- allows user to double check data using table generated in output.html

## Files
- `update_local.py` - script to create json
- `generate_html.py` - script with function to generate html
- `params.py` - set parameters here
- `template.json` - example of what `output.json` should be formatted
- `template.html` - example of what `output.html` should be formatted based on `template.json`
- `sampled_clinical_data.json`
- `/sample_files`
- `.gitignore`
