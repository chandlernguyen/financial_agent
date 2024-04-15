"""
This Python script efficiently cleans HTM financial filings from multiple companies, removing unnecessary content and formatting while preserving crucial metadata. 
The streamlined files facilitate easier analysis for financial analysis or regulatory compliance purposes. Here's the script's workflow:

1. Directory Setup: The script accesses a specific subdirectory for each company identified by its CIK number, containing their financial HTM filings.
2. Cleaning Process: Unnecessary content such as XBRL tags, encoded strings, and excessive whitespace is removed using regular expressions.
3. Metadata Preservation: Essential metadata within the HTM files is retained, ensuring that important information is not lost during the cleaning process.
4. Output: Cleaned files are stored in a designated directory for easy access and further analysis.
"""
import os
import re
from bs4 import BeautifulSoup

# Define the base directory for storing original filings (modify as per actual usage)
BASE_DIR = "/path/to/filings"

# Example CIKs for major companies
COMPANY_CIKS = {
    'Google': '0001652044',
    'Meta': '0001326801',
    'Microsoft': '0000789019',
    'Nvidia': '0001045810'
}

# Directory for storing cleaned filings
CLEANED_DIR = os.path.join(BASE_DIR, "cleaned_filings")
os.makedirs(CLEANED_DIR, exist_ok=True)

# Define regular expressions for various cleaning operations
re_patterns = {
    'xbrl_content': re.compile(r'<XBRL>.*?</XBRL>', flags=re.DOTALL),
    'encoded_strings': re.compile(r'\b[A-Za-z0-9+/]{10,}\b'),
    'html_tags': re.compile(r'<[^>]+>'),
    'tables': re.compile(r'\[Table:.*?\]'),
    'html_entities': re.compile(r'&[a-zA-Z0-9#]+;'),
    'ascii_blocks': re.compile(r'begin \d{3} .*?\nend', flags=re.DOTALL),
    'non_text_lines': re.compile(r'^[0-9\W]+$[\r\n]*', flags=re.MULTILINE),
    'whitespace': re.compile(r'\s+')
}

def clean_text(text):
    """Apply all regex cleaning operations to input text."""
    for regex in re_patterns.values():
        text = regex.sub('', text)
    return text.strip()

def preserve_metadata_and_clean_content(filepath):
    """Extract and preserve metadata, clean main content of HTM files."""
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'html.parser')
    metadata = {meta.get('name', ''): meta.get('content', '') for meta in soup.find_all('meta') if 'name' in meta.attrs and 'content' in meta.attrs}

    for tag in soup(["script", "style", "head"]):
        tag.decompose()
    
    main_content = soup.body.text if soup.body else ''
    cleaned_content = clean_text(main_content)
    cleaned_html = '<html><head>\n'
    for name, value in metadata.items():
        cleaned_html += f'<meta name="{name}" content="{value}">\n'
    cleaned_html += '</head>\n<body>\n' + cleaned_content + '\n</body></html>'

    cleaned_filename = os.path.basename(filepath).replace('.htm', '_cleaned.htm')
    cleaned_filepath = os.path.join(CLEANED_DIR, cleaned_filename)
    with open(cleaned_filepath, 'w', encoding='utf-8') as file:
        file.write(cleaned_html)

# Main execution loop
for company_name, cik in COMPANY_CIKS.items():
    filings_dir = os.path.join(BASE_DIR, cik)
    print(f"Processing and cleaning files for {company_name}")
    for filename in os.listdir(filings_dir):
        if filename.endswith('.htm'):
            filepath = os.path.join(filings_dir, filename)
            preserve_metadata_and_clean_content(filepath)

print("Cleaning completed. Cleaned files are saved in", CLEANED_DIR)
