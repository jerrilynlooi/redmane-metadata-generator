import os
import json
from pathlib import Path
from params import * 
from generate_html import generate_html_from_json

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
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in file_types):
                relative_path = os.path.relpath(os.path.join(root, file), directory)
                file_size = os.path.getsize(os.path.join(root, file))
                matching_files.append({
                    "file_name": file,
                    "file_size": f'{round(file_size/CONVERT_FROM_BYTES)}{FILE_SIZE_UNIT}',
                    "patient_id": '', # still need to implement
                    "sample_id": '', # still need to implement
                    "directory": f'./{relative_path}'
                })
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

    raw_files = get_matching_files(directory, RAW_FILE_TYPES)
    processed_files = get_matching_files(directory, PROCESSED_FILE_TYPES)
    summarised_files = get_matching_files(directory, SUMMARISED_FILE_TYPES)
    output_data = {
        "data": {
            "location": directory, 
            "files": {
                "raw": raw_files,
                "processed": processed_files,
                "summarised": summarised_files,
            }
        }
    }

    with open(output_file, "w") as f:
        json.dump(output_data, f, indent=4)

    print(f"JSON file generated at: {output_file}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python update_local.py /path/to/directory")
        sys.exit(1)

    target_directory = sys.argv[1]

    # Define the output file path (in the same directory as the script)
    script_directory = Path(__file__).parent
    output_file_path = script_directory / OUTPUT_JSON_FILE_NAME
    output_html_path = script_directory / OUTPUT_HTML_FILE_NAME

    try:
        generate_json(target_directory, output_file_path)
        generate_html_from_json(output_file_path, output_html_path)
    except Exception as e:
        print(f"Error: {e}")
