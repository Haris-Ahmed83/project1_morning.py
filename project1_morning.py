"""
====================================================
  Daily Auto GitHub Project Generator - Project 1
  Runs at 4:10 PM Pakistan Time (11:10 AM UTC)
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
#  STEP 0 — VALIDATE TOKEN BEFORE DOING ANYTHING
# ============================================================
print("\nValidating GitHub token...")
token_check = requests.get("https://api.github.com/user", headers=HEADERS)
if token_check.status_code != 200:
    print(f"  [ERROR] Token invalid or missing! HTTP {token_check.status_code}")
    print(f"  Fix: Go to GitHub → Settings → Developer settings → Personal access tokens")
    print(f"       Create a CLASSIC token with 'repo' (full) scope checked.")
    exit(1)

# Check scopes — classic token must have 'repo' scope
scopes = token_check.headers.get("X-OAuth-Scopes", "")
print(f"  [OK]  Token valid. Scopes: '{scopes}'")
if "repo" not in scopes:
    print(f"  [ERROR] Token is missing 'repo' scope!")
    print(f"  Your token scopes: {scopes}")
    print(f"  Fix: Create a new CLASSIC token and check the 'repo' checkbox.")
    exit(1)
print(f"  [OK]  Token has 'repo' scope.\n")

# ============================================================
#  MODEL FALLBACK CHAIN
# ============================================================
MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-8b",
    "gemini-1.5-flash",
]

# ============================================================
#  60 PROJECT TOPICS — PROJECT 1 (4:10 PM)
# ============================================================
TOPICS = [
    "Number Guessing Game with 3 difficulty levels easy medium hard and live score tracker",
    "Simple Calculator with full operation history log and memory functions",
    "Rock Paper Scissors game with win loss draw statistics and replay option",
    "Dice Rolling Simulator with probability stats and multi-dice support",
    "Prime Number Checker and Generator with Sieve of Eratosthenes",
    "Fibonacci Sequence Generator with memoization and execution time display",
    "Palindrome Checker for words sentences and numbers with clean output",
    "ATM Machine Simulator with PIN login balance check deposit and withdraw",
    "Roman Numeral Converter bidirectional with validation",
    "Temperature Converter supporting Celsius Fahrenheit and Kelvin",
    "CSV File Reader Analyzer with column stats min max average and export",
    "JSON Data Parser Formatter and Validator with pretty print output",
    "File Organizer that sorts files into folders by extension automatically",
    "Duplicate File Finder using MD5 hashing with delete confirmation",
    "Text File Word Frequency Counter with top 10 words display",
    "Student Grade Manager with file storage average calculator and pass fail",
    "Personal Expense Tracker with category budget and CSV monthly export",
    "Contact Book CLI with add search update delete and persistent JSON storage",
    "Inventory Management System with stock alerts and reorder notifications",
    "Library Book Manager with borrow return overdue tracking and fine calculator",
    "Hangman Word Game with 5 categories and ASCII art gallows",
    "Quiz Game with 3 categories score tracking timer and leaderboard",
    "Typing Speed Test with WPM accuracy score and difficulty levels",
    "Tic Tac Toe 2 player with win detection draw detection and replay",
    "Slot Machine Simulator with bet system balance and jackpot feature",
    "Blackjack Card Game with betting chips dealer AI and full rules",
    "Word Scramble Game with hints timer and category selection",
    "Trivia Quiz with 10 questions timer score and difficulty selector",
    "Math Quiz Generator with adaptive difficulty and performance tracking",
    "Text Adventure Game with rooms inventory and multiple endings",
    "Password Generator with length symbols uppercase options and strength meter",
    "Password Strength Analyzer with detailed feedback and improvement tips",
    "Countdown Timer with multiple timers alarm and pause resume",
    "Pomodoro Timer CLI with work break cycles session counter and stats",
    "Unit Converter for length weight volume area and temperature",
    "Currency Converter with 20 static exchange rates and conversion history",
    "Random Quote Generator by category with save favorites feature",
    "Simple Alarm Clock with multiple alarms snooze and label support",
    "Text Encryption Decryption tool using Caesar cipher and Vigenere cipher",
    "Markdown to Plain Text Converter with formatting cleanup",
    "Weather App using OpenWeatherMap API with 5 day forecast",
    "News Headline Fetcher using RSS feeds with category filter",
    "GitHub Profile Fetcher showing repos followers stats using GitHub API",
    "Dictionary App using Free Dictionary API with synonyms antonyms examples",
    "IP Address Lookup Tool with geolocation and ISP info",
    "URL Status Checker with HTTP response codes and redirect tracking",
    "Random Joke Fetcher with category filter and save favorites",
    "Currency Rate Fetcher with live rates and comparison",
    "Public Holiday Checker using Nager Date API for any country and year",
    "Chuck Norris Joke and Trivia Fetcher with category and search",
    "Stack Implementation with real world use cases like undo redo browser history",
    "Queue Implementation with print spooler and ticket system simulation",
    "Linked List with full CRUD insert delete search traverse and reverse",
    "Binary Search implementation with step by step visualization in terminal",
    "Bubble Sort Visualizer showing each swap step in terminal",
    "Merge Sort with step by step output comparison count and time tracking",
    "Simple Hash Map from scratch with collision handling and load factor",
    "Binary Tree with insert delete and all traversal methods",
    "Graph Representation with adjacency list BFS DFS and path finding",
    "LRU Cache implementation using OrderedDict with get put eviction demo",
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

print(f"{'='*60}")
print(f"  PROJECT 1  —  4:10 PM PKT")
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
#  DELETE EMPTY REPO IF IT EXISTS (clean slate)
# ============================================================
def repo_exists() -> bool:
    r = requests.get(
        f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}",
        headers=HEADERS
    )
    return r.status_code == 200

def repo_is_empty_check() -> bool:
    """Returns True if repo exists but has no commits yet."""
    r = requests.get(
        f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}/git/refs",
        headers=HEADERS
    )
    # Empty list [] means no refs = no commits
    return r.status_code == 200 and r.json() == []

def delete_repo():
    r = requests.delete(
        f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}",
        headers=HEADERS
    )
    return r.status_code == 204

# If the repo exists but is empty (broken state), delete it for a clean start
if repo_exists():
    if repo_is_empty_check():
        print(f"  [Fix] Repo '{repo_name}' exists but is empty (broken state).")
        print(f"  [Fix] Deleting it for a clean start...")
        if delete_repo():
            print(f"  [OK]  Deleted. Recreating fresh...\n")
            time.sleep(2)
        else:
            print(f"  [ERROR] Could not delete repo. Check token has 'delete_repo' scope.")
            exit(1)
    else:
        print(f"  [Info] Repo exists and has commits — will update files.\n")

# ============================================================
#  CREATE GITHUB REPO
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
        "auto_init":   False,   # we push the first commit ourselves
        "has_issues":  True,
    }
)

if res.status_code == 201:
    print(f"  [OK]  Repo created fresh!")
elif res.status_code == 422:
    print(f"  [OK]  Repo already exists with commits — will update files.")
else:
    print(f"  [ERROR] {res.status_code}: {res.json().get('message')}")
    exit(1)

time.sleep(2)

# ============================================================
#  DETECT DEFAULT BRANCH
# ============================================================
repo_info      = requests.get(
    f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}",
    headers=HEADERS
).json()
default_branch = repo_info.get("default_branch", "main")

branch_check  = requests.get(
    f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}/git/ref/heads/{default_branch}",
    headers=HEADERS
)
is_empty = (branch_check.status_code == 404)
print(f"  [Info] Empty: {is_empty} | Branch: {default_branch}\n")

# ============================================================
#  PUSH — Git Data API (first commit on empty repo)
# ============================================================
def push_initial_commit(files: dict) -> bool:
    """One atomic commit with all files using the Git Data API."""
    base = f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}/git"

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
            "path": filepath, "mode": "100644",
            "type": "blob",   "sha":  r.json()["sha"],
        })
        print(f"  [blob]   {filepath}")

    r = requests.post(f"{base}/trees", headers=HEADERS, json={"tree": tree_items})
    if r.status_code != 201:
        print(f"  [ERROR] tree: {r.status_code} {r.json()}")
        return False
    tree_sha = r.json()["sha"]
    print(f"  [tree]   {tree_sha[:10]}...")

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

    r = requests.post(f"{base}/refs", headers=HEADERS, json={
        "ref": f"refs/heads/{default_branch}",
        "sha": commit_sha,
    })
    if r.status_code not in (200, 201):
        print(f"  [ERROR] ref: {r.status_code} {r.json()}")
        return False
    print(f"  [ref]    refs/heads/{default_branch} ✅")
    return True

# ============================================================
#  PUSH — Contents API (update existing repo)
# ============================================================
def push_file(filepath, content, commit_msg) -> bool:
    """Update or create a single file via the Contents API."""
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
#  RUN THE RIGHT PUSH STRATEGY
# ============================================================
all_files = {
    "src/main.py":      code,
    "README.md":        readme,
    "requirements.txt": requirements,
    ".gitignore":       GITIGNORE,
}

print("Pushing files to GitHub...")

if is_empty:
    print("  [Strategy] Git Data API — initial commit\n")
    success = push_initial_commit(all_files)
    results = {f: success for f in all_files}
    if success:
        for f in all_files:
            print(f"  ✅  {f}")
else:
    print("  [Strategy] Contents API — updating files\n")
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
