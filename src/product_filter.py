import pandas as pd
import os
from dotenv import load_dotenv
from tqdm import tqdm

# === Load environment configuration ===
load_dotenv()
USE_GPT = os.getenv("USE_GPT", "false").lower() == "true"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if USE_GPT and OPENAI_API_KEY:
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)


# === GPT summarizer function ===
def summarize_description(product_name, description):
    prompt = (
        f"Summarize the following cannabis product description in 25 words or fewer. "
        f"Keep it casual and clear. Emphasize flavour, effect, or unique traits:\n\n"
        f"Product: {product_name}\nDescription: {description}"
    )
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=60,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[ERROR: {e}]"


# === Configuration ===
SKU_FILE = "skus.txt"
CSV_FILE = "data/latest_catalog.csv"
OUTPUT_FILE = "filtered_products.csv"

COLUMNS_TO_KEEP = [
    "SKU",
    "PRODUCT_NAME",
    "BRAND_NAME",
    "SUBCATEGORY",
    "CLASS",
    "SU_PRODUCT_NET_SIZE",
    "SU_PRODUCT_NET_SIZE_UOM",
    "SPECIES",
    "PER_RETAIL_UNIT_CBD_MAX",
    "PER_RETAIL_UNIT_CBD_MIN",
    "PER_RETAIL_UNIT_CBD_UOM",
    "PER_RETAIL_UNIT_THC_MAX",
    "PER_RETAIL_UNIT_THC_MIN",
    "PER_RETAIL_UNIT_THC_UOM",
    "ECOMM_SHORT_DESCRIPTION",
    "ECOMM_LONG_DESCRIPTION"
]

UOM_MAP = {
    "GRAM": "g",
    "MG/G": "mg/g",
    "MG": "mg",
    "EACH": "each",
    "ML": "mL"
}

def format_range(min_val, max_val, uom):
    if pd.isna(min_val) and pd.isna(max_val):
        return ""
    is_percent = str(uom).upper() == "MG/G"

    def format_val(val):
        if pd.isna(val):
            return "?"
        if is_percent:
            return str(round(float(val) / 10, 1)).rstrip('0').rstrip('.')
        return str(val).rstrip('0').rstrip('.')

    min_str = format_val(min_val)
    max_str = format_val(max_val)
    unit = "%" if is_percent else UOM_MAP.get(str(uom).upper(), uom.lower() if uom else "")

    return f"{min_str}{unit}" if min_str == max_str else f"{min_str}–{max_str}{unit}"

# === Load SKUs ===
with open(SKU_FILE, 'r') as f:
    skus = {line.strip() for line in f if line.strip()}

# === Load and filter catalog ===
df = pd.read_csv(CSV_FILE, encoding='utf-16', sep='\t')
df = df[COLUMNS_TO_KEEP]
df = df[df['SKU'].astype(str).isin(skus)]

# === Normalize units and format potency ranges ===
df["PRODUCT_SIZE"] = df["SU_PRODUCT_NET_SIZE"].astype(str).str.rstrip('0').str.rstrip('.') + \
                     df["SU_PRODUCT_NET_SIZE_UOM"].map(UOM_MAP).fillna("")

df["CBD_RANGE"] = [
    format_range(minv, maxv, uom)
    for minv, maxv, uom in zip(
        df["PER_RETAIL_UNIT_CBD_MIN"],
        df["PER_RETAIL_UNIT_CBD_MAX"],
        df["PER_RETAIL_UNIT_CBD_UOM"]
    )
]

df["THC_RANGE"] = [
    format_range(minv, maxv, uom)
    for minv, maxv, uom in zip(
        df["PER_RETAIL_UNIT_THC_MIN"],
        df["PER_RETAIL_UNIT_THC_MAX"],
        df["PER_RETAIL_UNIT_THC_UOM"]
    )
]

# === Drop raw columns ===
df = df.drop(columns=[
    "SU_PRODUCT_NET_SIZE", "SU_PRODUCT_NET_SIZE_UOM",
    "PER_RETAIL_UNIT_CBD_MIN", "PER_RETAIL_UNIT_CBD_MAX", "PER_RETAIL_UNIT_CBD_UOM",
    "PER_RETAIL_UNIT_THC_MIN", "PER_RETAIL_UNIT_THC_MAX", "PER_RETAIL_UNIT_THC_UOM"
])

# === Optional: LLM-generated short descriptions ===
if USE_GPT and OPENAI_API_KEY:
    print("🧠 Generating AI descriptions...")
    df["LLM_MENU_DESCRIPTION"] = [
        summarize_description(row["PRODUCT_NAME"], row["ECOMM_SHORT_DESCRIPTION"])
        for _, row in tqdm(df.iterrows(), total=len(df))
    ]

# === Save output ===
df.to_csv(OUTPUT_FILE, index=False)
print(f"✅ Saved {len(df)} products to {OUTPUT_FILE}")
if USE_GPT:
    print("🧠 GPT-generated menu descriptions included.")
else:
    print("✏️ GPT summarizer is disabled (USE_GPT=false).")
