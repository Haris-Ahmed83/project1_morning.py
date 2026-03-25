"""
====================================================
  Daily Auto GitHub Project Generator - Project 1
  Runs at 5:00 PM Pakistan Time (12:00 PM UTC)
  Uses Google Gemini API (FREE)
====================================================
"""

import os
import re
import sys
import time
import subprocess
import requests
import tempfile
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
#  STEP 0 — VALIDATE TOKEN
# ============================================================
print("\nValidating GitHub token...")
token_check = requests.get("https://api.github.com/user", headers=HEADERS)
if token_check.status_code != 200:
    print(f"  [ERROR] Token invalid! HTTP {token_check.status_code}")
    sys.exit(1)

scopes = token_check.headers.get("X-OAuth-Scopes", "")
print(f"  [OK]  Token valid. Scopes: '{scopes}'")
if "repo" not in scopes:
    print(f"  [ERROR] Token missing 'repo' scope!")
    sys.exit(1)
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
#  60 PROJECT TOPICS
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
print(f"  PROJECT 1  ---  5:00 PM PKT")
print(f"  Date    : {today}")
print(f"  Topic   : {topic}")
print(f"  Project : {topic_index + 1} of {len(TOPICS)}")
print(f"  Repo    : {repo_name}")
print(f"{'='*60}\n")

# ============================================================
#  GEMINI GENERATION
# ============================================================
def gemini_generate(client, prompt):
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
    raise RuntimeError("All Gemini models exhausted.")

def strip_fences(text, lang=""):
    text = re.sub(rf"^```{lang}\n?", "", text.strip())
    text = re.sub(r"\n?```$", "", text.strip())
    return text.strip()

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
    sys.exit(1)
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

GITIGNORE = "__pycache__/\n*.pyc\n*.pyo\n.env\n.venv/\nvenv/\n*.egg-info/\ndist/\nbuild/\n.DS_Store\n*.log\n"
print("  All files generated!\n")

# ============================================================
#  HELPER: Run shell command
# ============================================================
def run(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    return result.returncode == 0, result.stdout.strip(), result.stderr.strip()

# ============================================================
#  STEP 1: Ensure repo exists on GitHub
# ============================================================
description = (
    f"Daily Python Project #{topic_index + 1}/{len(TOPICS)}: "
    f"{topic[:80]} | {today} | by HarisAhmed83"
)

repo_check = requests.get(
    f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}",
    headers=HEADERS
)
repo_exists = (repo_check.status_code == 200)

if repo_exists:
    # Check if empty
    refs = requests.get(
        f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}/git/refs",
        headers=HEADERS
    )
    is_empty = (refs.status_code != 200) or (refs.json() == []) or isinstance(refs.json(), dict)
    if is_empty:
        print(f"  [Fix]  Repo '{repo_name}' exists but empty — deleting...")
        requests.delete(f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}", headers=HEADERS)
        time.sleep(5)
        repo_exists = False
        print(f"  [OK]   Deleted.\n")
    else:
        print(f"  [Info] Repo '{repo_name}' exists with commits — will update.\n")

if not repo_exists:
    print(f"  Creating repo '{repo_name}' on GitHub...")
    res = requests.post(
        "https://api.github.com/user/repos",
        headers=HEADERS,
        json={
            "name": repo_name,
            "description": description,
            "private": False,
            "auto_init": False,
            "has_issues": True,
        }
    )
    if res.status_code in (201, 422):
        print(f"  [OK]   Repo ready on GitHub.\n")
    else:
        print(f"  [ERROR] Create failed: {res.status_code} {res.json().get('message')}")
        sys.exit(1)
    time.sleep(3)

# ============================================================
#  STEP 2: Build project locally in temp dir
# ============================================================
work_dir = tempfile.mkdtemp()
remote_url = f"https://x-access-token:{GITHUB_TOKEN}@github.com/{GITHUB_USER}/{repo_name}.git"

# Check if repo has existing commits
refs_check = requests.get(
    f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}/git/refs",
    headers=HEADERS
)
has_commits = (
    refs_check.status_code == 200
    and isinstance(refs_check.json(), list)
    and len(refs_check.json()) > 0
)

if has_commits:
    print(f"  [Git] Cloning existing repo...")
    ok, out, err = run(f'git clone "{remote_url}" project', cwd=work_dir)
    if not ok:
        print(f"  [ERROR] Clone failed: {err}")
        sys.exit(1)
    project_dir = os.path.join(work_dir, "project")
else:
    print(f"  [Git] Initializing fresh local repo...")
    project_dir = os.path.join(work_dir, "project")
    os.makedirs(project_dir)
    run("git init", cwd=project_dir)
    run("git branch -M main", cwd=project_dir)
    run(f'git remote add origin "{remote_url}"', cwd=project_dir)

run('git config user.email "harisahmed83@users.noreply.github.com"', cwd=project_dir)
run('git config user.name "HarisAhmed83"', cwd=project_dir)

# ============================================================
#  STEP 3: Write files to disk
# ============================================================
print(f"  Writing project files...")

files_to_write = {
    "src/main.py":      code,
    "README.md":        readme,
    "requirements.txt": requirements,
    ".gitignore":       GITIGNORE,
}

for filepath, content in files_to_write.items():
    full_path = os.path.join(project_dir, filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"    {filepath} — {len(content)} chars")

# ============================================================
#  STEP 4: Git add + commit + push
# ============================================================
print(f"\n  Committing...")
run("git add -A", cwd=project_dir)

commit_msg = f"Project {topic_index + 1}: {topic[:60]}"
ok, out, err = run(f'git commit -m "{commit_msg}"', cwd=project_dir)
if not ok:
    if "nothing to commit" in (out + err):
        print(f"  [OK]  No changes to commit.")
    else:
        print(f"  [ERROR] Commit failed: {err}")
        sys.exit(1)
else:
    print(f"  [OK]  Committed.")

# Ensure branch is named 'main' AFTER the commit exists
run("git branch -M main", cwd=project_dir)

print(f"  Pushing to GitHub...")
ok, out, err = run("git push -u origin main --force", cwd=project_dir)
if not ok:
    print(f"  [ERROR] Push failed: {err}")
    print(f"  [DEBUG] stdout: {out}")
    sys.exit(1)

print(f"  [OK]  Pushed successfully!\n")

# Update description
requests.patch(
    f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}",
    headers=HEADERS,
    json={"description": description}
)

# ============================================================
#  DONE
# ============================================================
print(f"{'='*60}")
print(f"  SUCCESS — Project {topic_index + 1}/{len(TOPICS)}")
print(f"  https://github.com/{GITHUB_USER}/{repo_name}")
print(f"{'='*60}\n")
