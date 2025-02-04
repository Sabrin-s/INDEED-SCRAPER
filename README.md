#  INDEED-SCRAPER web scraping 

**PROJECT DESCRIPTION:**
The Indeed Scraper is a Python-based web scraper designed to extract job listings from the Indeed
website. It gathers job details such as job title, company name, location, salary (if available), job
description, and the date posted. This tool is useful for job seekers, researchers, and recruiters
looking to collect job market data, analyze trends, or track specific job opportunities over time.

**Web Scraping Automation:**
Utilizes Selenium and BeautifulSoup for dynamic and static content extraction.
**Job Data Extraction:**
Collects job titles, companies, locations, salaries, posting dates, and application links.
**Pagination Support:**
Fetches multiple pages of job listings based on user input.
**Sorting Functionality:**
Allows sorting job results by posting date in ascending or descending order.
**Data Export:**
Saves the scraped job data to a CSV file (indeed_scraper.csv).

**Technologies Used**
Selenium:
Handles dynamic content and automates browser actions.
BeautifulSoup: Parses HTML content for data extraction.
Pandas: Manages and exports data to CSV.
Fake UserAgent: Generates random user agents to avoid detection.

**How It Works**
**User Input:**
The user provides the job title, location, and number of pages to scrape.
**Data Fetching:**
The scraper visits Indeed pages, fetches job data, and handles retries for robustness.
**Data Processing:**
Extracted data is cleaned and structured for storage.
**Sorting:**
Jobs are sorted by posting date based on user preference.
**Data Export:**
Results are saved in a CSV file for easy access.








