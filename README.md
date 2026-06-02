# Fashion Studio ETL Pipeline

This project is an **ETL (Extract, Transform, Load)** pipeline built with Python to scrape fashion product data, process and clean the data, and load it into multiple data repositories including a local CSV file, PostgreSQL database, and Google Sheets. This project is created as a final submission for the Dicoding Data Engineering curriculum.

## Features
- **Extract (Web Scraping):** Scrapes up to 1000 items (Title, Price, Rating, Colors, Size, Gender) from `fashion-studio.dicoding.dev` across 50 pages using `BeautifulSoup4`.
- **Transform (Data Cleaning):** Cleans invalid strings, filters out missing values, handles duplicates, and converts USD Prices to IDR (Rp16,000 exchange rate).
- **Load (Data Storage):** Uses modular loading functions to save data to `.csv`, `PostgreSQL` (via `SQLAlchemy`), and `Google Sheets` (via Google API).
- **Unit Testing:** Validates data processing logic using `pytest` and `unittest.mock` to ensure high quality and robust coverage (>80%).

## Architecture / Structure
```
submission-pemda/
├── utils/
│   ├── extract.py      # Web scraping module
│   ├── transform.py    # Data cleaning and formatting module
│   └── load.py         # Data storage handling (CSV, SQL, API)
├── tests/
│   ├── test_extract.py 
│   ├── test_transform.py
│   └── test_load.py    
├── main.py             # ETL Orchestrator
└── requirements.txt    # Python Dependencies
```

## How to Run
1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Enable Google Sheets API in GCP and place your `google-sheets-api.json` credential file in the root folder.
3. Ensure PostgreSQL is running on `localhost:5432` if you intend to use the database loader.
4. Run the ETL pipeline:
   ```bash
   python main.py
   ```
   
> **Note:** The `google-sheets-api.json` is safely excluded via `.gitignore` to prevent secret leakage.
