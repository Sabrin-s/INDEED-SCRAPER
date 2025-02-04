from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd
import random
import re
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class IndeedScraper:
    def __init__(self):
        self.base_url = "https://in.indeed.com/jobs?q={query}&l={location}&start={page}"
        self.results = []
        options = webdriver.ChromeOptions()
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument('--headless')

        self.driver = webdriver.Chrome(service=Service(
            r"C:\chromedriver\chromedriver.exe"),
            options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def fetch_page(self, query, location, page):
        url = self.base_url.format(query=query, location=location, page=page * 10)

        retries = 3
        for attempt in range(retries):
            try:
                print(f"Fetching page {page} (Attempt {attempt + 1})...")
                self.driver.get(url)
                self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "job_seen_beacon")))
                time.sleep(random.uniform(3, 7))  # Randomized delay to mimic human behavior
                return self.driver.page_source
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(5)

        print(f"Failed to fetch page {page} after {retries} retries.")
        return None

    def extract_job_details(self, soup):
        jobs = []
        for job in soup.find_all("div", {"class": "job_seen_beacon"}):
            try:
                title_tag = job.find("h2", class_="jobTitle")
                title = title_tag.text.strip() if title_tag else "No title"

                company_tag = job.find("span", {"data-testid": "company-name"})
                company = company_tag.text.strip() if company_tag else "No company"

                location_tag = job.find("div", {"data-testid": "text-location"})
                location = location_tag.text.strip() if location_tag else "No location"

                salary_tag = job.find("div", class_="css-18z4q2i eu4oa1w0")  # Verify this class name
                if salary_tag:
                    salary_text = salary_tag.text.strip()
                    salary_numbers = re.findall(r"\d+[\.,]?\d*", salary_text)  # Extract numbers
                    salary = float(salary_numbers[0].replace(",", "")) if salary_numbers else 0.0  # Convert to float
                else:
                    salary = 0.0

                link_tag = job.find("a", {"class": "jcs-JobTitle"})
                link = "https://www.indeed.com" + link_tag["href"] if link_tag else "URL not available"

                date_tag = job.find("span", class_="css-1yxm164 eu4oa1w0")  # Verify this class name
                date_posted = date_tag.text.strip() if date_tag else "Not specified"

                jobs.append({
                    "Title": title,
                    "Company": company,
                    "Location": location,
                    "Salary": salary,
                    "Date Posted": date_posted,
                    "Link": link,
                })
            except Exception as e:
                print(f"Error extracting job details: {e}")
        return jobs

    def scrape(self, query, location, pages=1):
        for page in range(1, pages + 1):
            html = self.fetch_page(query, location, page)
            if not html:
                continue

            soup = BeautifulSoup(html, "html.parser")
            jobs = self.extract_job_details(soup)
            self.results.extend(jobs)

    def sort_by_date_posted(self, order="ascending"):
        """Sort jobs by date posted in ascending or descending order."""
        self.results = sorted(
            self.results,
            key=lambda x: pd.to_datetime(x["Date Posted"], errors='coerce'),  # Convert to datetime for sorting
            reverse=(order == "descending")  # Reverse order if descending
        )

    def save_results(self):
        df = pd.DataFrame(self.results)
        filename = "indeed_scraper.csv"

        df.to_csv(filename, index=False)
        print("Sorted results saved to indeed_scraper.csv")

    def close(self):
        self.driver.quit()


if __name__ == "__main__":
    scraper = IndeedScraper()
    try:
        search_query = input("Enter job title: ").replace(" ", "+")
        job_location = input("Enter location: ").replace(" ", "+")
        pages = int(input("Enter number of pages: "))

        scraper.scrape(search_query, job_location, pages)

        order = input("Sort order (ascending/descending): ").lower()
        scraper.sort_by_date_posted(order)
        scraper.save_results()
    finally:
        scraper.close()
