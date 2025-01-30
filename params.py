'''
Set parameters here!
'''

OUTPUT_JSON_FILE_NAME = "output.json"
OUTPUT_HTML_FILE_NAME = "output.html"

CONVERT_FROM_BYTES, FILE_SIZE_UNIT = 1024, "KB"

RAW_FILE_TYPES = ['.fastq', '.fasta']
PROCESSED_FILE_TYPES = ['.cram', '.bam']
SUMMARISED_FILE_TYPES = ['.vcf', '.maf']

METADATA = "sampled_clinical_data.json"
PATIENT_ID = "Patient ID" #what the Patient ID column is named in the file above
SAMPLE_ID = "Sample ID" #What the Sample Id column is named in the file above
