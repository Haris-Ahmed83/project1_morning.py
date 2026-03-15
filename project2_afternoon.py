"""
====================================================
  Daily Auto GitHub Project Generator - Project 2
  Runs at 5:10 PM Pakistan Time (12:10 PM UTC)
  Uses Google Gemini API (FREE)
====================================================
"""

import os
import re
import time
import base64
import requests
from datetime import datetime
from google import genai

# ============================================================
#  SETTINGS
# ============================================================
GITHUB_TOKEN = os.environ.get("PERSONAL_TOKEN", "")
GITHUB_USER  = "HarisAhmed83"
GEMINI_KEY   = os.environ.get("GEMINI_API_KEY", "")

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

# ============================================================
#  MODEL FALLBACK CHAIN
# ============================================================
MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-8b",
    "gemini-1.5-flash",
]

# ============================================================
#  60 PROJECT TOPICS — PROJECT 2 (5:10 PM)
# ============================================================
TOPICS = [
    "Bank Account System using OOP with savings checking and transaction history",
    "Student Management System OOP with GPA calculator and report card generator",
    "Employee Payroll System OOP with salary tax deduction and payslip generator",
    "Hospital Patient Management OOP with appointments prescriptions and billing",
    "School Timetable Generator OOP with teacher subject and room assignment",
    "Online Shopping Cart OOP with products discount coupon and checkout",
    "Hotel Room Booking System OOP with availability calendar and invoice",
    "Parking Lot Management OOP with vehicle types hourly rates and receipt",
    "Restaurant Order System OOP with menu items total bill and kitchen queue",
    "Gym Membership Manager OOP with plans attendance and payment tracking",
    "Automated File Backup Script with timestamp versioning and restore option",
    "Batch Image Renamer with prefix suffix numbering and date-based naming",
    "Log File Analyzer with error warning info count and summary report",
    "System Health Monitor showing CPU RAM disk usage with alerts",
    "Automated Report Generator from CSV data with summary in terminal",
    "Email Template Generator with placeholders and batch personalization",
    "Config File Manager supporting INI JSON formats with validation",
    "Directory Tree Visualizer with file sizes dates and search filter",
    "Automated Test Runner for Python functions with pass fail summary",
    "Simple Task Automation Scheduler with cron-like syntax",
    "Personal Diary App with date entries search and password protection",
    "Recipe Manager with ingredients steps category search and shopping list",
    "Habit Tracker with daily streaks completion rate and progress bar",
    "Budget Planner with income expense savings goal and monthly report",
    "Flashcard Study App with spaced repetition and score tracking",
    "Travel Packing List Manager with categories checklist and trip profiles",
    "Movie Watchlist Manager with ratings reviews genre filter and stats",
    "Workout Log Tracker with exercises sets reps weight and progress chart",
    "Book Reading Tracker with progress notes rating and reading speed",
    "Music Playlist Manager with songs artist genre shuffle and export",
    "Student Survey Analyzer reading CSV calculating stats and generating report",
    "Sales Data Dashboard showing revenue by product region and time period",
    "Text Sentiment Analyzer using keyword scoring positive negative neutral",
    "Phone Number Formatter and Validator for international formats",
    "Email Address Validator and Cleaner with domain check and deduplication",
    "Data Cleaning Script for CSV removing duplicates nulls and formatting",
    "Grade Distribution Analyzer with histogram in terminal and statistics",
    "Sports League Table Generator from match results with sorting",
    "Election Results Analyzer with vote percentage bar chart and winner",
    "Weather Data Analyzer from CSV with monthly averages and trend",
    "Multi-threaded File Downloader with progress bar and retry logic",
    "Simple REST API Client with GET POST PUT DELETE and response formatter",
    "Web Scraper for job listings with title company location and export",
    "ZIP File Manager with compress extract list and password protection",
    "SQLite Todo App with priorities deadlines tags and completion stats",
    "Simple Chat Bot with pattern matching responses and conversation log",
    "Snake Game using curses library with score levels and high score",
    "Tetris Clone text-based with scoring levels and game over screen",
    "Cron Job Simulator running scheduled Python tasks with logging",
    "Plugin System demonstrating dynamic loading of Python modules",
    "ASCII Art Generator converting text to large ASCII font styles",
    "Random Story Generator with characters settings plot and twist",
    "Morse Code Encoder and Decoder with audio description output",
    "Number to Words Converter supporting up to trillions in English",
    "Joke of the Day App with categories ratings and local joke database",
    "Color Palette Generator showing RGB HEX HSL values with named colors",
    "Star Pattern Printer generating 10 different star patterns by size",
    "Calendar Printer with highlighted today events and navigation",
    "Simple Cipher Collection with 5 encryption methods encode decode",
    "Math Magic Tricks App demonstrating 10 number magic tricks with explanation",
]

# ============================================================
#  PICK TODAY'S TOPIC
# ============================================================
day_of_year = datetime.now().timetuple().tm_yday
topic_index = (day_of_year - 1) % len(TOPICS)
topic       = TOPICS[topic_index]
today       = datetime.now().strftime("%Y-%m-%d")

_stop = {"with","that","and","for","the","a","an","of","to","in","by","on","using","from"}
_words = [w for w in topic.lower().split() if w not in _stop][:3]
repo_name = "-".join(_words).replace(",","").replace("(","").replace(")","").replace("/","-")

print(f"\n{'='*60}")
print(f"  PROJECT 2  —  5:10 PM PKT")
print(f"  Date    : {today}")
print(f"  Topic   : {topic}")
print(f"  Project : {topic_index + 1} of {len(TOPICS)}")
print(f"  Repo    : {repo_name}")
print(f"{'='*60}\n")

# ============================================================
#  GEMINI — MODEL FALLBACK + RETRY
# ============================================================
def gemini_generate(client, prompt):
    """Try each model. On 429 wait 65s and retry once, then try next model."""
    for model in MODELS:
        print(f"  [Model] Trying {model} ...")
        for attempt in range(1, 3):
            try:
                response = client.models.generate_content(model=model, contents=prompt)
                print(f"  [OK]    {model} succeeded.")
                return response.text.strip()
            except Exception as e:
                err = str(e)
                if "429" in err or "RESOURCE_EXHAUSTED" in err:
                    if attempt == 1:
                        print(f"  [Wait]  {model} quota — retrying in 65s...")
                        time.sleep(65)
                    else:
                        print(f"  [Skip]  {model} exhausted, trying next...")
                        break
                else:
                    raise
    raise RuntimeError("All Gemini models exhausted. Quota resets ~1 PM PKT.")

def strip_fences(text, lang=""):
    """Remove markdown code fences from AI output."""
    text = re.sub(rf"^```{lang}\n?", "", text.strip())
    text = re.sub(r"\n?```$", "", text.strip())
    return text.strip()

# ============================================================
#  GENERATE FILES WITH GEMINI
# ============================================================
print("Generating project files with Gemini...\n")
client = genai.Client(api_key=GEMINI_KEY)

print("  [1/3] Generating src/main.py ...")
code = strip_fences(gemini_generate(client, (
    f"Write a professional, complete Python script for: {topic}\n\n"
    f"STRICT REQUIREMENTS:\n"
    f"1. Module docstring at top: title, description, author HarisAhmed83\n"
    f"2. Every function must have a docstring\n"
    f"3. Full input validation on ALL user inputs\n"
    f"4. try/except error handling throughout\n"
    f"5. Clean terminal UI with dividers (===) and clear prompts\n"
    f"6. Inline comments explaining key logic\n"
    f"7. Main menu with numbered options and an exit option\n"
    f"8. if __name__ == '__main__': block at the bottom\n\n"
    f"Return ONLY raw Python code. No markdown. No backticks. No explanation."
)), "python")

if len(code) < 200:
    print(f"  [ERROR] Code too short ({len(code)} chars). Aborting.")
    exit(1)
print(f"  [OK]    src/main.py — {len(code)} chars\n")
time.sleep(15)

print("  [2/3] Generating README.md ...")
readme = strip_fences(gemini_generate(client, (
    f"Write a professional GitHub README.md for this Python project: {topic}\n\n"
    f"Include ALL these sections:\n"
    f"# [emoji] Project Title\n"
    f"## Description (2-3 sentences)\n"
    f"## Features (6-8 bullet points)\n"
    f"## Project Structure (show: src/main.py, requirements.txt, .gitignore)\n"
    f"## Requirements\n"
    f"## Installation (git clone, cd, pip install -r requirements.txt)\n"
    f"## How to Run (python src/main.py)\n"
    f"## Example Output (short terminal snippet in a code block)\n"
    f"## Author\n"
    f"  - **HarisAhmed83** — https://github.com/HarisAhmed83\n\n"
    f"Return ONLY the markdown. No wrapping backticks. No explanation."
)), "markdown")
print(f"  [OK]    README.md — {len(readme)} chars\n")
time.sleep(15)

print("  [3/3] Generating requirements.txt ...")
requirements = strip_fences(gemini_generate(client, (
    f"List ONLY the third-party pip packages needed for: {topic}\n"
    f"One package per line, lowercase. No stdlib modules.\n"
    f"If none needed, return exactly: # no external dependencies\n"
    f"Return ONLY the list. No explanation. No backticks."
)))
print(f"  [OK]    requirements.txt — {len(requirements)} chars\n")

GITIGNORE = (
    "__pycache__/\n*.pyc\n*.pyo\n.env\n.venv/\nvenv/\n"
    "*.egg-info/\ndist/\nbuild/\n.DS_Store\n*.log\n"
)

print("  All files generated!\n")

# ============================================================
#  CREATE GITHUB REPO  (auto_init=False — we push manually)
# ============================================================
description = (
    f"Daily Python Project #{topic_index + 1}/{len(TOPICS)}: "
    f"{topic[:80]} | {today} | by HarisAhmed83"
)

print(f"Creating repo '{repo_name}' on GitHub...")
res = requests.post(
    "https://api.github.com/user/repos",
    headers=HEADERS,
    json={
        "name":        repo_name,
        "description": description,
        "private":     False,
        "auto_init":   False,   # we handle the first commit ourselves
        "has_issues":  True,
    }
)

if res.status_code == 201:
    print(f"  [OK]  Repo created fresh!")
elif res.status_code == 422:
    print(f"  [OK]  Repo already exists.")
else:
    print(f"  [ERROR] {res.status_code}: {res.json().get('message')}")
    exit(1)

time.sleep(2)

# ============================================================
#  DETECT: does the repo have a default branch yet?
# ============================================================
repo_info      = requests.get(
    f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}",
    headers=HEADERS
).json()
default_branch = repo_info.get("default_branch", "main")

branch_check   = requests.get(
    f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}/git/ref/heads/{default_branch}",
    headers=HEADERS
)
repo_is_empty  = (branch_check.status_code == 404)
print(f"  [Info] Empty repo: {repo_is_empty} | Branch: {default_branch}\n")

# ============================================================
#  STRATEGY A — Empty repo: Git Data API (one atomic commit)
# ============================================================
def push_initial_commit(files: dict) -> bool:
    """
    Push all files as the very first commit on an empty repo.
    Uses the low-level Git Data API:
      create blobs → create tree → create commit → create ref
    """
    base = f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}/git"

    # Step 1 — blob for each file
    tree_items = []
    for filepath, content in files.items():
        r = requests.post(f"{base}/blobs", headers=HEADERS, json={
            "content":  base64.b64encode(content.encode("utf-8")).decode("utf-8"),
            "encoding": "base64",
        })
        if r.status_code != 201:
            print(f"  [ERROR] blob {filepath}: {r.status_code} {r.json()}")
            return False
        tree_items.append({
            "path": filepath,
            "mode": "100644",
            "type": "blob",
            "sha":  r.json()["sha"],
        })
        print(f"  [blob]   {filepath}")

    # Step 2 — tree
    r = requests.post(f"{base}/trees", headers=HEADERS, json={"tree": tree_items})
    if r.status_code != 201:
        print(f"  [ERROR] tree: {r.status_code} {r.json()}")
        return False
    tree_sha = r.json()["sha"]
    print(f"  [tree]   {tree_sha[:10]}...")

    # Step 3 — commit (no parents = first commit)
    r = requests.post(f"{base}/commits", headers=HEADERS, json={
        "message": f"Initial commit: {topic[:60]}",
        "tree":    tree_sha,
        "parents": [],
    })
    if r.status_code != 201:
        print(f"  [ERROR] commit: {r.status_code} {r.json()}")
        return False
    commit_sha = r.json()["sha"]
    print(f"  [commit] {commit_sha[:10]}...")

    # Step 4 — create the branch ref
    r = requests.post(f"{base}/refs", headers=HEADERS, json={
        "ref": f"refs/heads/{default_branch}",
        "sha": commit_sha,
    })
    if r.status_code not in (200, 201):
        print(f"  [ERROR] ref: {r.status_code} {r.json()}")
        return False
    print(f"  [ref]    refs/heads/{default_branch} created ✅")
    return True


# ============================================================
#  STRATEGY B — Existing repo: Contents API (file by file)
# ============================================================
def push_file(filepath, content, commit_msg) -> bool:
    """Update or create a single file using the Contents API."""
    url = f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}/contents/{filepath}"
    body = {
        "message": commit_msg,
        "content": base64.b64encode(content.encode("utf-8")).decode("utf-8"),
    }
    existing = requests.get(url, headers=HEADERS)
    if existing.status_code == 200:
        body["sha"] = existing.json().get("sha")
    r = requests.put(url, headers=HEADERS, json=body)
    if r.status_code in (200, 201):
        return True
    print(f"  [ERROR] {filepath}: HTTP {r.status_code} — {r.json().get('message','')}")
    return False


# ============================================================
#  PUSH FILES
# ============================================================
all_files = {
    "src/main.py":      code,
    "README.md":        readme,
    "requirements.txt": requirements,
    ".gitignore":       GITIGNORE,
}

print("Pushing files to GitHub...")

if repo_is_empty:
    print("  [Strategy] Empty repo — Git Data API (initial commit)\n")
    success = push_initial_commit(all_files)
    results = {f: success for f in all_files}
    if success:
        for f in all_files:
            print(f"  ✅  {f}")
else:
    print("  [Strategy] Existing repo — Contents API\n")
    results = {}
    for filepath, content in all_files.items():
        ok = push_file(filepath, content, f"Update: {filepath}")
        results[filepath] = ok
        print(f"  {'✅' if ok else '❌'}  {filepath}")
        time.sleep(1)

# ============================================================
#  FINAL STATUS
# ============================================================
failed = [f for f, ok in results.items() if not ok]
print(f"\n{'='*60}")
if not failed:
    print(f"  ✅ SUCCESS — Project {topic_index + 1}/{len(TOPICS)}")
    print(f"  🔗 https://github.com/{GITHUB_USER}/{repo_name}")
else:
    print(f"  ❌ PARTIAL FAILURE — files NOT pushed:")
    for f in failed:
        print(f"     • {f}")
    print(f"  🔗 https://github.com/{GITHUB_USER}/{repo_name}")
    exit(1)
print(f"{'='*60}\n")
