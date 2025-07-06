#!/bin/bash
cd ~/LocalBot || exit 1

VENV_PYTHON="$HOME/LocalBot/.venv/bin/python3"

echo "📬 Collecting SKUs from email..."
"$VENV_PYTHON" collect_skus_from_email.py

echo "📦 Processing catalog..."
"$VENV_PYTHON" filter_products.py

echo "... Uploading to Google Drive..."
"$VENV_PYTHON" upload_to_drive.py

