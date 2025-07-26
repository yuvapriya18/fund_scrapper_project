# 📊 Mutual Fund Scraper

This Python script scrapes mutual fund details (fund name, category, launch date, and risk ratios) from Moneycontrol and updates them in a Google Sheet. It also compares risk ratios with category averages and assigns flags (R/G) based on performance.

---

## ✅ Features

* Scrapes **fund details, launch date, and risk ratios** from Moneycontrol.
* Updates data **directly into Google Sheets** using `gspread`.
* Flags metrics as **Red (R)** or **Green (G)** based on comparison with category averages.
* Skips already scraped rows to save API quota.
* Logs all activities and errors to both console and a log file.
* Configurable settings via `config.json`.

---

## 📂 Project Structure

```
📦 mutual-fund-scraper
 ┣ 📜 scraper.py           # Main script
 ┣ 📜 config.json          # Config file for credentials, URLs, and settings
 ┣ 📜 requirements.txt     # Required Python libraries
 ┣ 📜 scraper_log.txt      # Log file (auto-created)
 ┣ 📜 .gitignore           # Ignore sensitive files like credentials.json
 ┣ 📜 README.md            # Project documentation
```

---

## 🔧 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/mutual-fund-scraper.git
cd mutual-fund-scraper
```

### 2️⃣ Create a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### Create `config.json` file:

```json
{
  "google": {
    "credentials_path": "credentials.json",
    "spreadsheet_name": "Scrap",
    "worksheet_index": 0
  },
  "timing": {
    "sleep_seconds": 1.5
  },
  "flags": {
    "std_beta_high_is_bad": true,
    "others_high_is_good": true
  },
  "headers": {
    "user_agent": "Mozilla/5.0"
  },
  "urls": {
    "risk_template": "{base_url}/riskanalysis/{fund_code}",
    "launch_template": "{base_url}/investment-info/{fund_code}",
    "base_clean_pattern": "/nav/"
  },
  "logging": {
    "log_file": "scraper_log.txt"
  }
}
```

### 🔑 Google API Setup

#### **1️⃣ Go to Google Cloud Console**

Visit [Google Cloud Console](https://console.cloud.google.com/) to manage your Google Cloud resources.

#### **2️⃣ Create a Service Account and download the JSON key**

* Navigate to **IAM & Admin → Service Accounts**.
* Create a **new service account** (give it a name and grant access to Google Sheets API).
* After creating, go to **Keys → Add Key → Create New Key → JSON**.
* A JSON key file will be downloaded containing authentication credentials.

#### **3️⃣ Rename the key file and place it in the project folder**

* Rename the downloaded file to **`credentials.json`**.
* Place it in the same folder as `scraper.py` (or specify a custom path in `config.json`).

#### **4️⃣ Share your Google Sheet with the Service Account email**

* Open the `credentials.json` file and find the **`client_email`** field.
* Open your Google Sheet → Click **Share** → Paste the email.
* Give **Editor** access so the script can update the sheet.

---

## ▶️ Running the Script

```bash
python scraper.py
```

Logs will be stored in **scraper\_log.txt** as well as shown in the terminal.

---

## 📜 Requirements

Install all dependencies with:

```bash
pip install -r requirements.txt
```

Contents of `requirements.txt`:

```
gspread
oauth2client
requests
beautifulsoup4
```

---

## 🚀 Uploading to GitHub

### 1️⃣ Initialize Git

```bash
git init
git branch -M main
git remote add origin https://github.com/<your-username>/mutual-fund-scraper.git
```

### 2️⃣ Create `.gitignore`

Create a file named `.gitignore` with:

```
credentials.json
__pycache__/
venv/
```

### 3️⃣ Add and Commit Files

```bash
git add .
git commit -m "Initial commit"
```

### 4️⃣ Push to GitHub

```bash
git push -u origin main
```

✅ Now your project is live on GitHub!

---

### 👨‍💻 Author

Developed by **Yuvapriya Nanjappan** ✨
