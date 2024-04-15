# SEC Filings Downloader

## Overview
This repository contains a Python script for automatically downloading XBRL and TXT filings from the U.S. Securities and Exchange Commission (SEC) database. It is designed to fetch recent filings for specified companies using their Central Index Key (CIK).

## Features
- Download filings for multiple companies.
- Handles both XBRL (zipped) and plain text formats.
- Filters filings by form type (e.g., 10-K, 10-Q) and date range.

## Usage
1. Clone this repository to your local machine.
2. Modify the `BASE_DIR` in the script to the path where you want to save the downloaded filings.
3. Optionally, update the `COMPANY_CIKS` dictionary to include the CIKs of the companies you're interested in.
4. Run the script using Python 3.x.

## Requirements
- Python 3.x
- Requests (`pip install requests`)

## Contributing
Contributions are welcome! Please feel free to submit pull requests or create issues for any bugs you encounter or enhancements you think would be beneficial.

## License
This project is open source under the MIT license. See the [LICENSE](LICENSE) file for more information.

