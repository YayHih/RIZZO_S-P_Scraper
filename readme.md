README
Created by Martin Oka, 12/18/2024

Overview

This project contains two Python scripts designed to work together:

Data Extraction Script: Extracts specific fields (security type, industry, sub-industry, and state/city) from tabular data, typically copied from websites like Wikipedia.

Data Scraping Script: Uses the extracted data to search for ESG (Environmental, Social, and Governance) reports on the CDP (Carbon Disclosure Project) website and compiles the results into a CSV file.

For Non-CS Users

What This Does

First Script:

Takes a table you copy (works best with Wikipedia tables).

Extracts information about security types, industries, sub-industries, and states.

Saves the information in a simpler format in a text file (security_type.txt).

Second Script:

Searches the CDP website for ESG reports using the data from the first script.

CDP is an organization that collects and scores sustainability-related data from companies and cities.

Saves the results, including the year, submission type, and ESG score, into a CSV file (cdp_esg_reports.csv).

Tracks entries where data is missing and saves them in another file (missing_data.csv).

How to Use

Copy a table from a website (preferably Wikipedia) and save it to a file (e.g., sandptest.txt).

Run the first script to process the table and generate security_type.txt.

Run the second script to search for ESG reports and save the results in cdp_esg_reports.csv.

Use the CSV file to analyze ESG performance data.

For CS Users

First Script: create_security_type_file

This script processes tab-delimited input data (e.g., copied tables) and extracts:

Security Name: From the second column.

Industry: From the third column.

Sub-Industry: From the fourth column.

State: From the fifth column.

Usage:

Input: sandptest.txt (tab-delimited file).

Output: security_type.txt (pipe-delimited file with a header row).

Method: Parses each line, splits by tab, and writes selected columns to the output file.

create_security_type_file(input_filepath, output_filepath)

Second Script: CDP ESG Data Scraper

This script uses Selenium to automate ESG report searches on the CDP website.

Key Components:

Input: security_type.txt (output from the first script).

Search Logic: Automates search for each security in the CDP search box.

Output:

cdp_esg_reports.csv: Contains security, sector, sub-sector, city/state, year, submission type, and score.

missing_data.csv: Lists entries with no data found.

Web Scraping: Randomized wait times (5-15 seconds) between actions to avoid detection.

CDP Overview:

CDP is a platform that collects ESG data and scores companies/cities based on their sustainability performance. Scores are derived from self-reported data and represent a company’s transparency and impact.

Usage:

Install dependencies using pip install selenium pandas webdriver-manager.

Run the script. It initializes a browser (Chrome) and navigates to the CDP search page.

Extracts the ESG data into structured rows.

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.cdp.net/en/responses?queries%5Bname%5D=")

Considerations:

Performance: Each entry takes ~0.24 minutes on average due to random wait times.

Error Handling: Logs errors for individual entries and saves incomplete results to missing_data.csv.

Ethics: Ensure the use of this tool complies with CDP’s terms of service and ethical guidelines for web scraping.

Dependencies

Python 3.8+

Required libraries:

selenium

pandas

webdriver-manager

Execution Flow

Prepare the input file (e.g., sandptest.txt).

Run the first script to generate security_type.txt.

Run the second script to scrape ESG data from CDP and generate output files.

Output Files

security_type.txt: Pipe-delimited file with extracted data.

cdp_esg_reports.csv: CSV file containing ESG report data.

missing_data.csv: CSV file listing entries with no results.

