import requests
from datetime import datetime, timedelta

def get_last_monday():
    today = datetime.today()
    # Always go back to the previous Monday
    days_since_monday = (today.weekday() + 7) % 7  # 0 (Mon) to 6 (Sun)
    last_monday = today - timedelta(days=days_since_monday or 7)
    return last_monday.strftime("%Y-%m-%d")

def download_catalog():
    base_url = "https://cdn.shopify.com/s/files/1/0007/0267/8860/files"
    date_str = get_last_monday()
    filename = f"Central_Delivery_Product_Catalog_-en-ca-{date_str}.csv"
    url = f"{base_url}/{filename}"

    # Optional: check if file exists before downloading
    head = requests.head(url)
    if head.status_code == 200:
        print(f"Downloading file for {date_str}...")
        response = requests.get(url)
        with open("latest_catalog.csv", "wb") as f:
            f.write(response.content)
        print("Download complete.")
        return True
    else:
        print(f"File not found: {url}")
        return False

if __name__ == "__main__":
    download_catalog()
