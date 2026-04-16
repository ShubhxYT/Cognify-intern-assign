# Cognify Internship – Software Development Program

A comprehensive Python project implementing 6 tasks across beginner, intermediate, and advanced levels. This submission showcases core programming concepts including game logic, data structures, CRUD operations, file persistence, and web scraping.

## 🎯 Project Overview

**Program:** Cognify Technologies Software Development Internship  
**Language:** Python 3.12  
**Package Manager:** UV  
**Status:** All 6 tasks implemented

## 📋 Tasks Completed

### Level 1: Beginner
- **Task 1:** Guessing Game – Random number game with hints and attempt tracking
- **Task 2:** Number Patterns – Multiple pattern generators (pyramid, diamond, Pascal's triangle)

### Level 2: Intermediate
- **Task 3:** CRUD Application – Task management with create, read, update, delete operations
- **Task 4:** Temperature Converter – Bidirectional conversion between °C, °F, and K

### Level 3: Advanced
- **Task 5:** File Persistence – Enhanced CRUD with JSON file storage for data persistence
- **Task 6:** Web Scraper – Multi-site interactive scraper (quotes.toscrape.com, books.toscrape.com, Hacker News)

## 🚀 Setup & Installation

```bash
# Install UV (if needed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone/navigate to project
git clone https://github.com/ShubhxYT/Cognify-intern-assign.git
cd Cognify-intern-assign

# Create virtual environment
uv sync
```

## ▶️ Running Each Task

```bash
uv run python task1/main.py          # Guessing Game
uv run python task2/main.py          # Number Patterns
uv run streamlit run task3_5/main.py # CRUD + Persistence
uv run python task4/main.py          # Temperature Converter
uv run streamlit run task6/main.py   # Web Scraper
```

## 📁 Project Structure

```
├── task1/main.py          # Guessing game (stdlib only)
├── task2/main.py          # Number pattern generator
├── task3_5/
│   ├── main.py            # Streamlit CRUD app
│   └── tasks.json         # Auto-created data file
├── task4/main.py          # Temperature converter
├── task6/main.py          # Streamlit web scraper
├── pyproject.toml         # UV project config
└── README.md              # This file
```

## 🛠 Key Features

- **Game Logic:** Conditional statements, input validation, game loop (Task 1)
- **Algorithms:** Loop-based pattern generation (Task 2)
- **CRUD Operations:** Full task lifecycle management with Streamlit UI (Task 3, 5)
- **Data Persistence:** JSON file I/O with error handling (Task 5)
- **Web Scraping:** Multi-source data aggregation with user-friendly display (Task 6)
- **Data Transformation:** Temperature conversion with input validation (Task 4)

## 📊 Dependencies

- `beautifulsoup4` – HTML parsing for web scraping
- `requests` – HTTP requests for scraping
- `streamlit` – Interactive UI for Tasks 3 & 6
- Standard Library – Tasks 1, 2, 4

## 👤 Author

Submitted for **Cognify Technologies Internship Program**
