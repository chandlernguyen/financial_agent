import requests
import os
from datetime import datetime

# Constants
BASE_DIR = "/path/to/your/directory/filings"  # Change to the path where files should be saved
COMPANY_CIKS = {
    'Apple': '0000320193', 'Meta': '0001326801', 'Microsoft': '0000789019', 'Nvidia': '0001045810'
}

def download_filing(url, cik, form, date, file_extension):
    """
    This function downloads and saves a SEC filing from a specified URL.
    
    Args:
        url (str): URL to download the filing from.
        cik (str): Central Index Key (CIK) for the company.
        form (str): The type of SEC filing (e.g., 10-K, 10-Q).
        date (str): The filing date in YYYY-MM-DD format.
        file_extension (str): File extension for saved file (usually 'txt' or 'zip').
    """
    # Define request headers to simulate a browser visit
    headers = {'User-Agent': 'Company Filings Fetcher +http://yourwebsite.com'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        dir_name = f"{BASE_DIR}/{cik}"
        os.makedirs(dir_name, exist_ok=True)
        file_path = f"{dir_name}/{form}_{date}.{file_extension}"
        
        with open(file_path, 'wb') as file:
            file.write(response.content)
        
        print(f"Downloaded {form} for CIK {cik} on {date} to {file_path}")
    else:
        print(f"Failed to download {form} for CIK {cik} on {date}. Status code: {response.status_code}")

def fetch_filings(cik, form_types=['10-K', '10-Q'], years=5):
    """
    Fetch and download filings for a specified CIK from the SEC database.
    
    Args:
        cik (str): Central Index Key (CIK) of the company.
        form_types (list of str): Types of forms to fetch (default is 10-K and 10-Q).
        years (int): Number of past years to fetch filings from (default is 5 years).
    """
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    headers = {'User-Agent': 'Company Filings Fetcher +http://yourwebsite.com'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        current_year = datetime.now().year

        for filing_date, form, accession_number in zip(data['filings']['recent']['filingDate'], data['filings']['recent']['form'], data['filings']['recent']['accessionNumber']):
            if form in form_types and current_year - datetime.strptime(filing_date, '%Y-%m-%d').year <= years:
                download_filing(
                    f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_number.replace('-', '')}/{accession_number}-xbrl.zip",
                    cik, form, filing_date, 'zip'
                )
                download_filing(
                    f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_number.replace('-', '')}/{accession_number}.txt",
                    cik, form, filing_date, 'txt'
                )

for company_name, cik in COMPANY_CIKS.items():
    print(f"Fetching filings for {company_name}")
    fetch_filings(cik)

print("Completed downloading XBRL zip filings and txt filings for all companies.")
