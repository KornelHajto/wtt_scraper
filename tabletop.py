import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Set up headless Firefox (you can switch to Chrome if you want)
options = webdriver.FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)

url = "https://www.ittf.com/wp-content/uploads/2025/05/2025_20_SEN_MS.html"
driver.get(url)
time.sleep(5)  # Wait for page load

# Find all rows in the table (both visible and hidden)
rows = driver.find_elements(By.CSS_SELECTOR, 'tr.rrow, tr.drow')

data = []
i = 0
while i < len(rows):
    row = rows[i]
    if 'rrow' in row.get_attribute('class'):
        # Extract visible row data
        try:
            rank = row.find_element(By.CSS_SELECTOR, 'span.rank').text.strip()
            name = row.find_elements(By.TAG_NAME, 'td')[1].text.strip()
            assoc = row.find_element(By.CSS_SELECTOR, 'td.assoc').text.strip().split()[-1]
            rcellcs = row.find_elements(By.CSS_SELECTOR, 'td.rcellc')
            if len(rcellcs) < 2:
                i += 1
                continue
            rcellc_val = int(rcellcs[1].text.strip())

            pid = None  # default if no drow

            # Check next row for hidden details
            if i + 1 < len(rows):
                next_row = rows[i + 1]
                if 'drow' in next_row.get_attribute('class'):
                    # Look for data-pid attribute inside this hidden row's inner table rows
                    detail_rows = next_row.find_elements(By.CSS_SELECTOR, 'tbody tr[data-pid]')
                    if detail_rows:
                        # Assuming the pid is the same for all detail rows,
                        # get the data-pid of the first one
                        pid = detail_rows[0].get_attribute('data-pid')

            if rcellc_val > 10:
                data.append([rank, name, assoc, rcellc_val, pid])

        except Exception as e:
            # Just skip any problematic row
            pass

        i += 2  # skip to the next visible row after the hidden row
    else:
        i += 1  # just move on if somehow hitting a drow unexpectedly

driver.quit()

# Save to CSV
csv_filename = 'scraped_data_with_pid.csv'
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Rank', 'Name', 'Association', 'Rcellc', 'PID'])
    writer.writerows(data)

print(f"Saved {len(data)} entries to {csv_filename}")
