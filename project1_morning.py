"""
====================================================
  Daily Auto GitHub Project Generator - Project 1
  Runs at 7AM Pakistan Time
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
from google.genai import errors as genai_errors

# ============================================================
#  SETTINGS
# ============================================================
GITHUB_TOKEN  = os.environ.get("PERSONAL_TOKEN", "")
GITHUB_USER   = "HarisAhmed83"
GEMINI_KEY    = os.environ.get("GEMINI_API_KEY", "")

# ============================================================
#  MODEL FALLBACK CHAIN
#  gemini-2.0-flash is RETIRED March 3 2026 — DO NOT USE
#  Order: best → fastest → highest free quota
# ============================================================
MODELS = [
    "gemini-2.5-flash",        # Best quality, 10 RPM, 500 RPD free
    "gemini-2.5-flash-lite",   # Fastest, 15 RPM, 1000 RPD free
    "gemini-1.5-flash",        # Fallback, 15 RPM, 1500 RPD free
]

# ============================================================
#  60 PROFESSIONAL PROJECT TOPICS — MORNING (Project 1)
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
# Clean repo name from topic — remove filler words, take 3 meaningful words
_stop = {"with","that","and","for","the","a","an","of","to","in","by","on","using","from"}
_words = [w for w in topic.lower().split() if w not in _stop][:3]
repo_name = "-".join(_words).replace(",","").replace("(","").replace(")","").replace("/","-")

print(f"\n{'='*60}")
print(f"  PROJECT 1 — MORNING (7AM PKT)")
print(f"  Date    : {today}")
print(f"  Topic   : {topic}")
print(f"  Project : {topic_index + 1} of 60")
print(f"  Repo    : {repo_name}")
print(f"{'='*60}\n")

# ============================================================
#  GEMINI CALL WITH MODEL FALLBACK + RETRY
# ============================================================
def gemini_generate(client, prompt):
    """
    Try each model in MODELS list.
    On 429 quota error, wait 65s and retry once, then try next model.
    """
    for model in MODELS:
        print(f"  [Model] Trying {model}...")
        for attempt in range(1, 3):  # 2 attempts per model
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )
                print(f"  [OK] {model} succeeded.")
                return response
            except Exception as e:
                err = str(e)
                if "429" in err or "RESOURCE_EXHAUSTED" in err:
                    if attempt == 1:
                        print(f"  [Quota] {model} hit limit, waiting 65s...")
                        time.sleep(65)
                    else:
                        print(f"  [Skip] {model} quota exhausted, trying next model...")
                        break
                else:
                    # Non-quota error — raise immediately
                    raise
    raise RuntimeError("All models exhausted. Daily quota exceeded. Try again after 1 PM PKT (quota resets midnight Pacific).")

# ============================================================
#  GENERATE WITH GEMINI AI
# ============================================================
print("Generating with Gemini AI (Free)...\n")

client = genai.Client(api_key=GEMINI_KEY)

# Generate Python Code
print("  Writing Python code...")
code_prompt = (
    f"Write a professional, complete Python script for: {topic}\n\n"
    f"STRICT REQUIREMENTS:\n"
    f"1. Module docstring at top with title, description, author: HarisAhmed83\n"
    f"2. All functions must have docstrings\n"
    f"3. Full input validation on all user inputs\n"
    f"4. try/except error handling throughout\n"
    f"5. Clean terminal UI with dividers and clear prompts\n"
    f"6. Inline comments explaining logic\n"
    f"7. Main menu with exit option\n"
    f"8. if __name__ == '__main__': block at bottom\n\n"
    f"Return ONLY raw Python code. No markdown. No backticks. No explanation."
)
code_res = gemini_generate(client, code_prompt)
code = re.sub(r"^```(?:python)?\n?", "", code_res.text.strip())
code = re.sub(r"\n?```$", "", code.strip())

# Delay between API calls
print("  Waiting 15s between API calls...")
time.sleep(15)

# Generate README
print("  Writing README...")
readme_prompt = (
    f"Write a professional GitHub README.md for this Python project: {topic}\n\n"
    f"Include ALL these sections:\n"
    f"# Title with relevant emoji\n"
    f"## Description (2-3 sentences)\n"
    f"## Features (5-8 bullet points)\n"
    f"## Requirements\n"
    f"## Installation\n"
    f"## How to Run\n"
    f"## Example Output (short code block)\n"
    f"## Author\n"
    f"- Name: HarisAhmed83\n"
    f"- GitHub: https://github.com/HarisAhmed83\n\n"
    f"Return ONLY the markdown. No explanation. No backticks wrapping."
)
readme_res = gemini_generate(client, readme_prompt)
readme = re.sub(r"^```(?:markdown)?\n?", "", readme_res.text.strip())
readme = re.sub(r"\n?```$", "", readme.strip())

print("  Done generating!\n")

# ============================================================
#  CREATE GITHUB REPO
# ============================================================
print(f"Creating repo: {repo_name}...")

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

res = requests.post(
    "https://api.github.com/user/repos",
    headers=headers,
    json={
        "name": repo_name,
        "description": f"Daily Python Project #{topic_index + 1}/60: {topic[:80]} | {today}",
        "private": False,
        "auto_init": True,   # FIX: creates default branch so files can be pushed
        "has_issues": True
    }
)

if res.status_code == 201:
    print(f"  Repo created!")
    time.sleep(3)  # FIX: wait for GitHub to initialize the branch
elif res.status_code == 422:
    print(f"  Repo exists, pushing files...")
else:
    print(f"  Error {res.status_code}: {res.json().get('message')}")
    exit(1)

# ============================================================
#  PUSH FILES
# ============================================================
def push_file(filename, content, message):
    """Push a single file to GitHub repo (handles both new and existing files)."""
    url = f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}/contents/{filename}"
    body = {
        "message": message,
        "content": base64.b64encode(content.encode("utf-8")).decode("utf-8")
    }
    # FIX: always check for existing file sha (README.md now exists from auto_init)
    existing = requests.get(url, headers=headers)
    if existing.status_code == 200:
        body["sha"] = existing.json().get("sha")
    r = requests.put(url, headers=headers, json=body)
    if r.status_code not in [200, 201]:
        print(f"    [ERROR] {filename}: {r.status_code} — {r.json().get('message', '')}")
        return False
    return True

print("\nPushing files to GitHub...")

gitignore = "__pycache__/\n*.pyc\n*.pyo\n.env\n.venv/\nvenv/\n*.egg-info/\ndist/\nbuild/\n.DS_Store\n"

results = {
    "main.py":    push_file("main.py",    code,      f"Add project: {topic[:60]}"),
    "README.md":  push_file("README.md",  readme,    "Add README"),
    ".gitignore": push_file(".gitignore", gitignore, "Add .gitignore"),
}

for f, ok in results.items():
    print(f"  {'OK' if ok else 'FAILED'} — {f}")

print(f"\n{'='*60}")
print(f"  SUCCESS — Project {topic_index + 1}/60")
print(f"  https://github.com/{GITHUB_USER}/{repo_name}")
print(f"{'='*60}\n")
