import importlib
import subprocess
import sys

# Module name → pip install name (in case they differ)
REQUIRED_MODULES = {
    "pandas": "pandas",
    "imap_tools": "imap-tools",
    "dotenv": "python-dotenv",
    "openai": "openai",
    "tqdm": "tqdm",
    "gspread": "gspread",
    "google.auth": "google-auth",
    "googleapiclient.discovery": "google-api-python-client",
    "httplib2": "httplib2",
    "oauth2client": "oauth2client"
}

missing = []

for module, pip_name in REQUIRED_MODULES.items():
    try:
        importlib.import_module(module)
    except ImportError:
        missing.append((module, pip_name))

if missing:
    print("🚨 Missing packages detected. Installing:")
    for module, pip_name in missing:
        print(f"  - {module} (via pip install {pip_name})")
        subprocess.run([sys.executable, "-m", "pip", "install", pip_name])

    print("\n🔁 Re-run your command to continue.")
    sys.exit(1)
else:
    print("✅ All dependencies are satisfied.")
