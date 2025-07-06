#!/bin/bash
# Ensure script always runs from project root
cd "$(dirname "$0")"

# Optional: load virtualenv
# source venv/bin/activate

# Run the email parser
python3 src/email_parser.py
