#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate

# Pre-flight check
python3 src/check_dependencies.py
if [ $? -ne 0 ]; then
  echo "❌ Dependencies were just installed. Please re-run the script."
  exit 1
fi

# Main pipeline
python3 src/grab_current_LDB_data.py
python3 src/email_parser.py
python3 src/product_filter.py
python3 src/sync_to_sheets.py