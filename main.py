import json
import gspread
import requests
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials
import time
import re
import logging

# Load config
with open("config.json") as f:
    config = json.load(f)

#log file
log_file = config["logging"]["log_file"]

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(config["google"]["credentials_path"], scope)
client = gspread.authorize(creds)
spreadsheet = client.open(config["google"]["spreadsheet_name"])
sheet = spreadsheet.get_worksheet(config["google"]["worksheet_index"])

SLEEP_TIME = config["timing"]["sleep_seconds"]
USER_AGENT = config["headers"]["user_agent"]

# Helper functions
def extract_fund_name_and_category(url):
    response = requests.get(url, headers={"User-Agent": USER_AGENT})
    soup = BeautifulSoup(response.text, 'html.parser')
    name_tag = soup.select_one('h1.pcstname, h1.page_heading')
    category_tag = soup.select_one('div.category_text span.sub_category_text a')

    fund_name = name_tag.text.strip() if name_tag else "N/A"
    category = category_tag.text.strip() if category_tag else "N/A"
    return fund_name, category

def extract_launch_date(url):
    response = requests.get(url, headers={"User-Agent": USER_AGENT})
    soup = BeautifulSoup(response.text, 'html.parser')
    for li in soup.select('ul.schemedetails_list li'):
        if 'Launch date' in li.text:
            parts = li.text.split('–')
            if len(parts) == 2:
                return parts[1].strip()
    return "N/A"

def get_risk_ratios_with_avg(url):
    response = requests.get(url, headers={"User-Agent": USER_AGENT})
    soup = BeautifulSoup(response.text, 'html.parser')
    values = []
    averages = []

    blocks = soup.find_all("div", class_="percentage")
    for i in range(5):
        try:
            spans = blocks[i].find_all("span")
            val = spans[0].text.strip() if len(spans) > 0 else "N/A"
            avg = spans[2].text.strip() if len(spans) > 1 else "N/A"
        except Exception as e:
            logging.warning(f"⚠️ Could not extract risk ratio index {i}: {e}")
            val = "N/A"
            avg = "N/A"
        values.append(val)
        averages.append(avg)
    return values, averages

def clean_number(text):
    try:
        return float(re.sub(r"[^\d.-]", "", text))
    except Exception as e:
        logging.warning(f"⚠️ Could not parse number from '{text}': {e}")
        return None

# Start processing from second row
data = sheet.get_all_values()
for i in range(1, len(data)):
    row = data[i]
    base_url = row[2].strip() if len(row) > 2 else ""
    if not base_url:
        continue

    fund_name_cell = row[1].strip() if len(row) > 1 else ""
    std_dev_cell = row[7].strip() if len(row) > 7 else ""

    if fund_name_cell and std_dev_cell:
        logging.info(f"⏭️ Skipping row {i+1}: Already scraped.")
        continue

    fund_code = base_url.split("/")[-1]
    base_cleaned = base_url.replace(config["urls"]["base_clean_pattern"], "/").rstrip("/")
    risk_url = config["urls"]["risk_template"].format(base_url=base_cleaned, fund_code=fund_code)
    launch_url = config["urls"]["launch_template"].format(base_url=base_cleaned, fund_code=fund_code)

    logging.info(f"\n⏳ Processing row {i+1}...")

    try:
        fund_name, category = extract_fund_name_and_category(base_url)
        launch_date = extract_launch_date(launch_url)
        risk_values, cat_averages = get_risk_ratios_with_avg(risk_url)

        v = [clean_number(x) for x in risk_values]
        c = [clean_number(x) for x in cat_averages]

        flags = []
        for j in range(5):
            if v[j] is None or c[j] is None:
                flags.append("")
            elif j <= 1:
                flags.append("R" if v[j] > c[j] else "G")
            else:
                flags.append("G" if v[j] > c[j] else "R")

        sheet.update_cell(i + 1, 2, fund_name)
        sheet.update_cell(i + 1, 4, category)
        sheet.update_cell(i + 1, 5, launch_date)

        sheet.update_cell(i + 1, 6, risk_values[0])
        sheet.update_cell(i + 1, 7, cat_averages[0])
        sheet.update_cell(i + 1, 8, flags[0])

        sheet.update_cell(i + 1, 9, risk_values[1])
        sheet.update_cell(i + 1,10, cat_averages[1])
        sheet.update_cell(i + 1,11, flags[1])

        sheet.update_cell(i + 1,12, risk_values[2])
        sheet.update_cell(i + 1,13, cat_averages[2])
        sheet.update_cell(i + 1,14, flags[2])

        sheet.update_cell(i + 1,15, risk_values[3])
        sheet.update_cell(i + 1,16, cat_averages[3])
        sheet.update_cell(i + 1,17, flags[3])

        sheet.update_cell(i + 1,18, risk_values[4])
        sheet.update_cell(i + 1,19, cat_averages[4])
        sheet.update_cell(i + 1,20, flags[4])

        logging.info(f"✅ Row {i+1} updated")

    except requests.exceptions.RequestException as e:
        logging.error(f"🔌 Network error in row {i+1} ({row}): {e}")
    except Exception as e:
        logging.error(f"❌ General error in row {i+1} ({row}): {e}")

    time.sleep(SLEEP_TIME)

logging.info("\n✅ All done!")
