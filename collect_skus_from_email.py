from datetime import datetime, timedelta
from imap_tools import MailBox, AND
import re

# === CONFIGURATION ===
EMAIL = "localbot850@gmail.com"
PASSWORD = "jtrh ajjx jmkn sjwh"
IMAP_SERVER = "imap.gmail.com"
FOLDER = "INBOX"
SENDER_FILTER = "tim@localcannabisco.ca"
SUBJECT_KEYWORDS = ["Your BC Cannabis Wholesale order"]
SKU_PATTERN = r"\b\d{7}\b"  # 7-digit SKUs
OUTPUT_FILE = "skus.txt"
found_skus = set()

# === Calculate date range: last Wednesday 00:00 → now ===
now = datetime.now()
weekday = now.weekday()  # Monday=0, Sunday=6
days_since_wed = (weekday - 2) % 7  # Wednesday is day 2
last_wednesday = now - timedelta(days=days_since_wed)
last_wednesday = last_wednesday.replace(hour=0, minute=0, second=0, microsecond=0)

# === CONNECT AND SEARCH ===
with MailBox(IMAP_SERVER).login(EMAIL, PASSWORD, FOLDER) as mailbox:
    for msg in mailbox.fetch(AND(from_=SENDER_FILTER, date_gte=last_wednesday.date())):
        if any(keyword.lower() in msg.subject.lower() for keyword in SUBJECT_KEYWORDS):
            body = msg.html or msg.text or ""
            if not body and msg.obj:
                for part in msg.obj.walk():
                    if part.get_content_type() == "text/html":
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        break
            skus = re.findall(SKU_PATTERN, body)
            found_skus.update(skus)

# === SAVE TO FILE ===
with open(OUTPUT_FILE, "w") as f:
    for sku in sorted(found_skus):
        f.write(f"{sku}\n")

print(f"✅ Found and saved {len(found_skus)} SKUs to {OUTPUT_FILE}")
print(f"🗓️ Checking messages from: {last_wednesday.date()} to {now.date()}")
