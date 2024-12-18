import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.cdp.net/en/responses?queries%5Bname%5D=")
time.sleep(random.uniform(15, 25))  # Random wait on startup to avoid detection

# Input and output files
input_file = "security_type.txt"
output_file = "cdp_esg_reports.csv"

data = []
with open(input_file, "r") as file:
    for line in file:
        line = line.strip()
        if line and "|" in line:
            parts = line.split("|")
            security = parts[0].strip()
            sector = parts[1].strip()  # Industry
            sub_sector = parts[2].strip()  # Sub-Industry
            city_state = parts[3].strip()  # City/State combined
            data.append((security, sector, sub_sector, city_state))

results = []
missing_data = []
total_entries = len(data)

# Start timer
start_time = time.time()

for idx, (security, sector, sub_sector, city_state) in enumerate(data):
    try:
        print(f"Searching for: {security}")

        # Search the security name on the website
        search_box = driver.find_element(By.XPATH, '//input[@placeholder="Search for a city or company name"]')
        search_box.clear()
        search_box.send_keys(security)
        search_box.send_keys(Keys.RETURN)
        time.sleep(random.uniform(8, 15))  # Randomized wait after searching

        # Extract rows from the results table
        rows = driver.find_elements(By.CSS_SELECTOR, "tr")

        if len(rows) > 1:  # Skip header
            first_valid_row = None
            for row in rows[1:]:
                columns = row.find_elements(By.TAG_NAME, "td")
                if len(columns) >= 5:
                    first_valid_row = {
                        "Security": security,
                        "Sector": sector,
                        "Sub-Sector": sub_sector,
                        "City/State": city_state,
                        "Year": columns[2].text.strip(),
                        "Submission": columns[3].text.strip(),
                        "Score": columns[4].text.strip(),
                    }
                    break  # Take only the first valid row and stop

            if first_valid_row:
                results.append(first_valid_row)
            else:
                missing_data.append([security, sector, sub_sector, city_state])

        else:
            missing_data.append([security, sector, sub_sector, city_state])

        # Progress status
        completion_percent = ((idx + 1) / total_entries) * 100
        #.24 min per entry is around what I got when running sandp500 multiple times, rememeber there is a random search time so expect a little varation +/- 10 min
        print(f"Progress: {idx + 1}/{total_entries} ({completion_percent:.2f}%) Time left: {(total_entries-(idx+1))*.24} Minutes left")

    except Exception as e:
        print(f"Error scraping {security}: {e}")
        missing_data.append([security, sector, sub_sector, city_state])

    finally:
        time.sleep(random.uniform(5, 10))  # Random wait between searches

# Timer end
end_time = time.time()
total_time = (end_time - start_time) / 60

# Save results
if results:
    df = pd.DataFrame(results)
    df.to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")

if missing_data:
    missing_df = pd.DataFrame(missing_data, columns=["Security", "Sector", "Sub-Sector", "City/State"])
    missing_df.to_csv("missing_data.csv", index=False)
    print("Missing data saved to 'missing_data.csv'")

print(f"Scraping completed in {total_time:.2f} minutes.")
driver.quit()
