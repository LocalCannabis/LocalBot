import gspread
from gspread_dataframe import set_with_dataframe
import pandas as pd
import json

# === CONFIGURATION ===
CREDS_FILE = "creds/localbot-automation-df16ee94ce73.json"
SHEET_ID = "108Xpz87730dPY23NCXUCkLhnAOYuh1iwXyDy65DAkPg"  # Replace with your actual Sheet ID
SHEET_NAME = "Filtered_Products"       # Name of the sheet tab

# === Load Data (replace with your actual data loading logic) ===
df = pd.read_csv("filtered_products.csv")

# === Authenticate with Google Sheets ===
gc = gspread.service_account(filename=CREDS_FILE)
sh = gc.open_by_key(SHEET_ID)
worksheet = sh.worksheet(SHEET_NAME)

# === Clear existing content (optional) ===
worksheet.clear()

# === Send DataFrame to sheet ===
set_with_dataframe(worksheet, df)

print("✅ Synced data to Google Sheets")
