# Financial Agent

## Overview
This repository contains a suite of Python scripts designed to automate the downloading, processing, and cleaning of financial filings from the U.S. Securities and Exchange Commission (SEC) database. 
These tools are intended for anyone interested in performing detailed analyses of corporate financial statements, especially through the use of Large language models.

### Scripts Included
- **SEC Filings Downloader (`sec-filings-downloader.py`)**: Downloads XBRL and TXT filings using company CIKs.
- **SEC Metadata Processor (`sec-metadata-processor.py`)**: Extracts and processes financial statements and metadata from filings.
- **HTML Filings Cleaner (`financial_filings_htm_cleaner.py`)**: Cleans and prepares HTM financial filings for analysis.

## Features
- **Comprehensive Data Handling**: From downloading to cleaning, handle all aspects of SEC filings management.
- **Flexibility**: Download and process filings based on form type and date range.
- **Customization**: Easy to modify to fit specific needs for different companies' filings.

## Usage
1. Clone this repository to your local machine.
2. Modify the `BASE_DIR` in the scripts to the path where you want to save the filings.
3. Optionally, update the `COMPANY_CIKS` dictionary in each script to include the CIKs of the companies you're interested in.
4. Run the desired script using Python 3.11.

### Quick Start

python sec-filings-downloader.py  # Download filings
python sec-metadata-processor.py  # Process and extract data
python financial_filings_htm_cleaner.py  # Clean HTML filings

### Requirements
python = "^3.11"
langchain = "^0.1.11"
langchain-openai = "^0.0.8"
langchain-core = "^0.1.29"
langchain-community = "^0.0.26"
fastapi = "^0.110.0"
python-dotenv = "^1.0.1"
langchain-anthropic = "^0.1.3"
beautifulsoup4 = "^4.12.3"
lark = "^1.1.9"
chromadb = "^0.4.24"
langchain-elasticsearch = "^0.1.2"

## Contributing
Contributions to financial_agent are welcome! Here are some ways you can contribute:

Submit pull requests with improvements to the scripts or documentation.
Report any issues you encounter using the scripts.
Suggest new features or enhancements.
Feel free to fork this repository and submit your contributions via pull requests.

## License
This project is open source under the MIT license. See the [LICENSE](LICENSE) file for more information.

