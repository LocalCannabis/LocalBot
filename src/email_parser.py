from datetime import datetime, timedelta
from imap_tools import MailBox, AND
from dotenv import load_dotenv
import os, re

# === LOAD CONFIG ===
load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.gmail.com")
FOLDER = "INBOX"
SENDER_FILTER = os.getenv("SENDER_FILTER", "tim@localcannabisco.ca")
SUBJECT_KEYWORDS = ["Your BC Cannabis Wholesale order"]
SKU_PATTERN = r"\b\d{7}\b"
DATA_DIR = os.getenv("DATA_DIR", "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "skus.txt")
DEBUG = True
found_skus = set()

# === DATE RANGE ===
now = datetime.now()
days_since_wed = (now.weekday() - 2) % 7
last_wednesday = now - timedelta(days=days_since_wed)
last_wednesday = last_wednesday.replace(hour=0, minute=0, second=0, microsecond=0)

# === FETCH EMAILS ===
with MailBox(IMAP_SERVER).login(EMAIL, PASSWORD, FOLDER) as mailbox:
    for idx, msg in enumerate(mailbox.fetch(AND(from_=SENDER_FILTER, date_gte=last_wednesday.date()))):
        if any(keyword.lower() in msg.subject.lower() for keyword in SUBJECT_KEYWORDS):
            body = msg.html or msg.text or ""
            if not body and msg.obj:
                for part in msg.obj.walk():
                    if part.get_content_type() == "text/html":
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        break
            if DEBUG:
                with open(os.path.join(DATA_DIR, f"debug_email_{idx + 1}.html"), "w", encoding="utf-8") as dbg:
                    dbg.write(body)
            skus = re.findall(SKU_PATTERN, body)
            found_skus.update(skus)

# === SAVE SKUs ===
os.makedirs(DATA_DIR, exist_ok=True)
with open(OUTPUT_FILE, "w") as f:
    for sku in sorted(found_skus):
        f.write(f"{sku}\n")

print(f"✅ Found and saved {len(found_skus)} SKUs to {OUTPUT_FILE}")
print(f"🗓️ Checking messages from: {last_wednesday.date()} to {now.date()}")

