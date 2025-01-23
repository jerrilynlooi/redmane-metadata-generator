import json

def generate_html_from_json(json_file, output_html):
    """
    Generate an HTML file displaying the data from a JSON file in a table format.

    Args:
        json_file (str): Path to the input JSON file.
        output_html (str): Path to save the generated HTML file.

    Returns:
        None
    """
    with open(json_file, "r") as f:
        data = json.load(f)

    location = data["data"]["location"]
    files = data["data"]["files"]

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>File Summary</title>
        <style>
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                font-size: 18px;
                text-align: left;
            }}
            th, td {{
                padding: 12px;
                border: 1px solid #ddd;
            }}
            th {{
                background-color: #f4f4f4;
            }}
        </style>
    </head>
    <body>
        <h1>File Summary</h1>
        <h2>Location: {location}</h2>
    """

    for category, file_list in files.items():
        html_content += f"<h3>{category.capitalize()} Files</h3>"
        html_content += "<table><thead><tr><th>File Name</th><th>File Size</th><th>Patient ID</th><th>Sample ID</th><th>Directory</th></tr></thead><tbody>"
        for file in file_list:
            html_content += f"""
            <tr>
                <td>{file['file_name']}</td>
                <td>{file['file_size']}</td>
                <td>{file['patient_id']}</td>
                <td>{file['sample_id']}</td>
                <td>{file['directory']}</td>
            </tr>
            """
        html_content += "</tbody></table>"

    html_content += "</body></html>"

    with open(output_html, "w") as f:
        f.write(html_content)

    print(f"HTML file generated at: {output_html}")