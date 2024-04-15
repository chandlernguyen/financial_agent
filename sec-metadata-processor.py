"""
This Python script automates the process of extracting financial statements and their associated metadata from the filings of multiple companies. 
It is designed to handle the files downloaded from the SEC EDGAR database, which includes both .zip and .txt files. Here is the workflow of the script:

1. **Directory Setup**: Each company has its own designated subdirectory under the base directory, where their respective filing archives are stored.
2. **Unzip Files**: The script scans each company's directory for .zip files, each containing HTML documents of the company's financial filings. 
These files are then extracted into corresponding subdirectories for further processing.
3. **Metadata Extraction**: For each unzipped directory, a corresponding .txt file is sought. 
This file contains crucial metadata about the filing. 
The script extracts metadata such as the document type and reporting period from the .txt file using regular expressions.
4. **Content Processing**: The script identifies the largest HTML file in each unzipped directory, which typically represents the main financial statement. 
It then combines the extracted metadata with the HTML content of this file, embedding the metadata as meta tags in the HTML header.
5. **File Renaming and Saving**: The combined HTML content is saved in a new file named according to the company's CIK number, 
the type of the filing, and the reporting period, facilitating easy identification and access.

This automated process ensures consistency
"""

import os
import re
import zipfile

# Define the base directory for filing storage, replace with a path relevant to your setup
BASE_DIR = "path/to/filings"

# Example CIKs for major companies
COMPANY_CIKS = {
    'Google': '0001652044',
    'Meta': '0001326801',
    'Microsoft': '0000789019',
    'Nvidia': '0001045810'
}

def extract_metadata_from_txt(filepath):
    """
    Extract metadata from the .txt file using regex to find relevant sections.

    Args:
        filepath (str): Full path to the .txt file.
        
    Returns:
        dict: A dictionary containing extracted metadata.
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()

    metadata_pattern = r'(<SEC-DOCUMENT>.*?</SEC-HEADER>)'
    metadata_matches = re.findall(metadata_pattern, content, re.DOTALL)
    metadata_text = metadata_matches[0] if metadata_matches else ""

    metadata = {}
    for line in metadata_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            metadata[key.strip()] = value.strip()
    return metadata

def combine_metadata_and_content(metadata, htm_content):
    """
    Embed extracted metadata as meta tags in the HTML content.

    Args:
        metadata (dict): Metadata to embed.
        htm_content (str): Original HTML content.

    Returns:
        str: HTML content with embedded metadata.
    """
    combined_content = "<html><head>\n"
    for key, value in metadata.items():
        combined_content += f'<meta name="{key.lower().replace(" ", "_")}" content="{value}">\n'
    combined_content += "</head>\n<body>\n" + htm_content + "\n</body></html>"
    return combined_content

def find_corresponding_txt_file(directory, item):
    """
    Attempt to locate a .txt file corresponding to a .zip file in the same directory.

    Args:
        directory (str): Directory to search in.
        item (str): The name of the .zip file.

    Returns:
        str or None: Filename of the corresponding .txt file, if found.
    """
    possible_txt_filename = item.replace('.zip', '') + '.txt'
    possible_txt_filepath = os.path.join(directory, possible_txt_filename)
    
    if os.path.exists(possible_txt_filepath):
        return possible_txt_filename
    else:
        for txt_file in os.listdir(directory):
            if txt_file.endswith('.txt') and item.split('_')[0] in txt_file:
                return txt_file
        return None

def unzip_files(directory):
    """
    Unzip all .zip files in a given directory into subdirectories.

    Args:
        directory (str): Directory containing .zip files to be unzipped.
    """
    for item in os.listdir(directory):
        if item.endswith('.zip'):
            file_path = os.path.join(directory, item)
            unzip_dir = os.path.join(directory, item[:-4])
            os.makedirs(unzip_dir, exist_ok=True)
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(unzip_dir)
            print(f"Unzipped {item}")

def process_unzipped_folders(directory, cik):
    """
    Process all unzipped folders in a directory, extracting content and metadata.

    Args:
        directory (str): Base directory to process.
        cik (str): CIK number of the company (for naming purposes).
    """
    for item in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, item)) and not item.endswith('.zip'):
            txt_filename = find_corresponding_txt_file(directory, item)
            if txt_filename:
                metadata = extract_metadata_from_txt(os.path.join(directory, txt_filename))
                largest_file = None
                max_size = 0
                for file in os.listdir(os.path.join(directory, item)):
                    if file.endswith('.htm') or file.endswith('.html'):
                        file_path = os.path.join(directory, item, file)
                        size = os.path.getsize(file_path)
                        if size > max_size:
                            max_size = size
                            largest_file = file_path
                if largest_file:
                    with open(largest_file, 'r', encoding='utf-8') as file:
                        htm_content = file.read()
                    combined_content = combine_metadata_and_content(metadata, htm_content)
                    new_name = f"{cik}_{item}_{metadata.get('CONFORMED SUBMISSION TYPE', '')}_{metadata.get('CONFORMED PERIOD OF REPORT', '')}.htm"
                    new_filepath = os.path.join(directory, new_name)
                    with open(new_filepath, 'w', encoding='utf-8') as file:
                        file.write(combined_content)
                    print(f"Created {new_name} in {directory}")

# Process each company's filings
for company_name, cik in COMPANY_CIKS.items():
    company_dir = f"{BASE_DIR}/{cik}"
    print(f"Processing files for {company_name}")
    unzip_files(company_dir)
    process_unzipped_folders(company_dir, cik)

print("Completed processing for all companies.")
