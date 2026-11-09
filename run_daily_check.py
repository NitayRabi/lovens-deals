import urllib.request
import json
import subprocess
import os
import datetime

# 1. Run scraper script to refresh deals.json
scraper_path = os.path.expanduser("~/projects/lovens-deals/scraper.py")
subprocess.run(["python3", scraper_path], check=True)

# 2. Check git diff for deals.json
deals_path = os.path.expanduser("~/projects/lovens-deals/deals.json")
with open(deals_path) as f:
    data = json.load(f)

# 3. Commit and push changes to update live Dokploy deployment
repo_dir = os.path.expanduser("~/projects/lovens-deals")
git_status = subprocess.run(["git", "status", "--porcelain"], cwd=repo_dir, capture_output=True, text=True).stdout

if "deals.json" in git_status or "index.html" in git_status:
    subprocess.run(["git", "add", "."], cwd=repo_dir)
    subprocess.run(["git", "commit", "-m", f"Daily deal refresh: {datetime.date.today()}"], cwd=repo_dir)
    subprocess.run(["git", "push"], cwd=repo_dir)
    print("Pushed update to GitHub & Dokploy.")
else:
    print("No price changes detected.")

# 4. Summary output for Telegram notification
print(f"CHECK_DONE: Lovens Bakfiets Deal Radar checked {len(data['dealers'])} Amsterdam dealers.")
