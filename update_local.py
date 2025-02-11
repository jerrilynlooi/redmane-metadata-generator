import os
import json
from pathlib import Path
from params import *
from generate_html import generate_html_from_json

def get_ids(file, id):
    """
    Returns a list of patient/sample id from the given metadata file.

    Args:
        file (str): name of the metadata file in this directory
        id ("Patient ID" or "Sample ID")

        Returns:
            list: A list of patient/sample ids

    """
    if id not in {"Patient ID", "Sample ID"}:
        raise ValueError(f"Invalid value: {id}. Must be 'Patient ID' or 'Sample ID'.")
    with open(file, "r") as f:
        data = json.load(f)
        id_list = []
    for i in data:
        id_list.append(i[id])
    return id_list

def get_matching_files(directory, file_types):
    """
    Recursively find files in a directory that match the given file types.

    Args:
        directory (str): The directory to search.
        file_types (list): List of file extensions to match.

    Returns:
        list: A list of dictionaries with file details.
    """
    matching_files = []
    total_file_size = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in file_types):
                relative_path = os.path.relpath(os.path.join(root, file), directory)
                file_path = f'./{relative_path}'
                file_size = round(os.path.getsize(os.path.join(root, file))/CONVERT_FROM_BYTES)
                total_file_size += file_size
                file_object = {
                    "file_name": file,
                    "file_size": file_size,
                    "patient_id": '',
                    "sample_id": '',
                    "directory": file_path
                }
                print(f" | {file_path}  ~{file_size}{FILE_SIZE_UNIT}")
                matching_files.append(file_object)

    # Append the patient/sample ids found in the metadata (defined in params),
    # if it matches with the file name
    for id in get_ids(METADATA, "Patient ID"):
        for file in matching_files:
            if id in file["file_name"]:
                file["patient_id"] = id
    for id in get_ids(METADATA, "Sample ID"):
        for file in matching_files:
            if id in file["file_name"]:
                file["sample_id"] = id

    if not matching_files:
        print(f" | No files found")
    else:
        print(f" | \n | Total size of files is {total_file_size} {FILE_SIZE_UNIT}")
    return matching_files

def generate_json(directory, output_file):
    """
    Generate a JSON file summarizing files in the directory.

    Args:
        directory (str): The directory to analyze.
        output_file (str): Path to save the JSON output.

    Returns:
        None
    """
    if not os.path.isdir(directory):
        raise ValueError(f"The specified path '{directory}' is not a valid directory.")

    print(f"\nListing for raw files ({', '.join(RAW_FILE_TYPES)}) files")
    raw_files = get_matching_files(directory, RAW_FILE_TYPES)
    print(f"\nListing for processed files ({', '.join(PROCESSED_FILE_TYPES)}) files")
    processed_files = get_matching_files(directory, PROCESSED_FILE_TYPES)
    print(f"\nListing for summarised files ({', '.join(SUMMARISED_FILE_TYPES)}) files")
    summarised_files = get_matching_files(directory, SUMMARISED_FILE_TYPES)
    output_data = {
        "data": {
            "location": directory,
            "file_size_unit": FILE_SIZE_UNIT,
            "files": {
                "raw": raw_files,
                "processed": processed_files,
                "summarised": summarised_files,
            }
        }
    }

    with open(output_file, "w") as f:
        json.dump(output_data, f, indent=4)

    print(f"\nJSON file generated at: {output_file}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python update_local.py /path/to/directory")
        sys.exit(1)

    target_directory = sys.argv[1]
    print(f"\nSearching through /{target_directory} .........")

    # Define the output file path (in the same directory as the script)
    script_directory = Path(__file__).parent
    output_file_path = script_directory / OUTPUT_JSON_FILE_NAME
    output_html_path = script_directory / OUTPUT_HTML_FILE_NAME
    try:
        generate_json(target_directory, output_file_path)
        generate_html_from_json(output_file_path, output_html_path)
        print(f"")
    except Exception as e:
        print(f"Error: {e}")
