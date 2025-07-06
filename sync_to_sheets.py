import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials

# === CONFIG ===
SHEET_ID = "1P1TZL510Ng57nIsktQs50s1Sq91L92QYE-SeQLfNiyc"
TAB_NAME = "Filtered Products"
CSV_FILE = "filtered_products.csv"
CREDS_FILE = "credentials.json"

# === AUTH ===
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
client = gspread.authorize(creds)

# === OPEN SHEET ===
spreadsheet = client.open_by_key(SHEET_ID)
worksheet = spreadsheet.worksheet(TAB_NAME)

# === LOAD & SYNC CSV DATA ===
df = pd.read_csv(CSV_FILE)

# Clear existing data (optional)
worksheet.clear()

# Write new data
set_with_dataframe(worksheet, df, include_column_header=True)

print(f"✅ Synced {len(df)} products to Google Sheet tab: {TAB_NAME}")
