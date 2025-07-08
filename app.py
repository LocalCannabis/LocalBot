from flask import Flask, request, render_template, redirect
import subprocess
import threading
from functools import wraps
import os

app = Flask(__name__)
PASSWORD = os.getenv("LOCALBOT_PASSWORD", "fallback")


# Auth decorator
def check_auth(password):
    return password == PASSWORD

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.method == "POST":
            auth = request.form.get("password")
            if not check_auth(auth):
                return "Unauthorized", 401
        return f(*args, **kwargs)
    return decorated

# Home route with password protection
@app.route("/", methods=["GET", "POST"])
@requires_auth
def home():
    if request.method == "POST":
        use_ai = request.form.get("use_ai") == "on"
        thread = threading.Thread(target=run_localbot, args=(use_ai,))
        thread.start()
        return redirect("https://docs.google.com/spreadsheets/d/108Xpz87730dPY23NCXUCkLhnAOYuh1iwXyDy65DAkPg")
    return render_template("index.html")

@app.route("/done")
def done():
    return "<h2>Bot started! Check back soon for results.</h2>"

def run_localbot(use_ai=False):
    subprocess.run([
        "python3", "LocalBot/main.py",
        "--use-ai", str(use_ai).lower()
    ])

if __name__ == "__main__":
    app.run(debug=True)
