import subprocess

print("📬 Collecting SKUs from email...")
subprocess.run(["python", "collect_skus_from_email.py"], check=True)

print("\n📦 Filtering product catalog...")
subprocess.run(["python", "filter_products.py"], check=True)

print("\n✅ All done! Check 'filtered_products.csv' for results.")
input("🔍 Press Enter to exit...")
