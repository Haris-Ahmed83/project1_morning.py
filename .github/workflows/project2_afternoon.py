"""
====================================================
  Daily Auto GitHub Project Generator - Project 2
  Runs at 10AM Pakistan Time
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
#  60 PROFESSIONAL PROJECT TOPICS — AFTERNOON (Project 2)
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
    "Morse Code Encoder and Decoder with description output",
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
repo_name   = f"project-afternoon-{today}"

print(f"\n{'='*60}")
print(f"  PROJECT 2 — AFTERNOON (10AM PKT)")
print(f"  Date    : {today}")
print(f"  Topic   : {topic}")
print(f"  Project : {topic_index + 1} of 60")
print(f"  Repo    : {repo_name}")
print(f"{'='*60}\n")

# ============================================================
#  GEMINI CALL WITH AUTO-RETRY (handles 429 quota errors)
# ============================================================
def gemini_generate(client, prompt, retries=5, wait=65):
    """Call Gemini with automatic retry on rate limit / quota errors."""
    for attempt in range(1, retries + 1):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            return response
        except genai_errors.ClientError as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                if attempt < retries:
                    print(f"  [Rate limit] Waiting {wait}s... (retry {attempt}/{retries - 1})")
                    time.sleep(wait)
                else:
                    print("  [FAILED] Quota exhausted after all retries.")
                    raise
            else:
                raise

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

# Small delay between API calls to avoid per-minute limit
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
        "auto_init": False,
        "has_issues": True
    }
)

if res.status_code == 201:
    print(f"  Repo created!")
elif res.status_code == 422:
    print(f"  Repo exists, pushing files...")
else:
    print(f"  Error {res.status_code}: {res.json().get('message')}")
    exit(1)

# ============================================================
#  PUSH FILES
# ============================================================
def push_file(filename, content, message):
    """Push a single file to GitHub repo."""
    url = f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}/contents/{filename}"
    body = {
        "message": message,
        "content": base64.b64encode(content.encode("utf-8")).decode("utf-8")
    }
    existing = requests.get(url, headers=headers)
    if existing.status_code == 200:
        body["sha"] = existing.json().get("sha")
    r = requests.put(url, headers=headers, json=body)
    return r.status_code in [200, 201]

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
