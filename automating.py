"""LinkedIn driver for job scraping."""

import os
import random
import time
from typing import List, Dict, Any, Optional, Tuple
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from dotenv import load_dotenv

from config import Config
from css_selectors import LoginSelectors, JobListSelectors, JobDetailSelectors
from extractors import extract_work_details, extract_seniority_from_text, extract_tech_skills
from utils import random_delay, save_to_csv


class Driver:
    """LinkedIn job scraper for Warsaw Python-related positions."""

    def __init__(self) -> None:
        """Initialize the driver with Chrome options and load environment variables."""
        load_dotenv()
        self.url: str = os.getenv("URL", Config.LINKEDIN_LOGIN_URL)
        self.email: Optional[str] = os.getenv("EMAIL")
        self.password: Optional[str] = os.getenv("PASSWORD")

        options = Options()
        options.add_argument(f'--window-size={Config.WINDOW_SIZE}')
        options.add_argument(f'--user-agent={Config.USER_AGENT}')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("detach", True)

        self.driver: webdriver.Chrome = webdriver.Chrome(options=options)
        self.driver.get(self.url)
        self.all_jobs: List[Dict[str, Any]] = []
        self.seen_urls: set = set()

    def _random_delay(self, min_sec: float = 1, max_sec: float = 3) -> None:
        """
        Add random delay between actions.

        Args:
            min_sec: Minimum delay in seconds
            max_sec: Maximum delay in seconds
        """
        time.sleep(random.uniform(min_sec, max_sec))

    def _find_element_with_selectors(self, selectors: List[Tuple[str, str]],
                                     timeout: int = Config.SHORT_TIMEOUT) -> Optional[WebElement]:
        """
        Try multiple selectors and return first matching element.

        Args:
            selectors: List of (by, selector) tuples
            timeout: Timeout in seconds

        Returns:
            Found WebElement or None
        """
        for by, selector in selectors:
            try:
                return self.wait_for_clickable(by, selector, timeout)
            except Exception:
                continue
        return None

    def _get_meta_value(self, index: int) -> str:
        """
        Get meta field value by index from job detail page.

        Args:
            index: Index of the meta field (3=posted, 5=applicants)

        Returns:
            Meta field text or empty string
        """
        try:
            xpath: str = JobDetailSelectors.META_BASE_XPATH.format(index=index)
            element: WebElement = self.driver.find_element(By.XPATH, xpath)
            return element.text
        except Exception:
            return ""

    def wait_for_element(self, by: str, value: str,
                         timeout: int = Config.DEFAULT_TIMEOUT) -> WebElement:
        """
        Wait for element to be present in DOM.

        Args:
            by: Selenium By strategy
            value: Selector value
            timeout: Timeout in seconds

        Returns:
            Found WebElement
        """
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def wait_for_clickable(self, by: str, value: str,
                           timeout: int = Config.DEFAULT_TIMEOUT) -> WebElement:
        """
        Wait for element to be clickable.

        Args:
            by: Selenium By strategy
            value: Selector value
            timeout: Timeout in seconds

        Returns:
            Found WebElement
        """
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )

    def login(self) -> Optional[str]:
        """
        Login to LinkedIn using credentials from .env file.

        Returns:
            None on success, 'err' on failure
        """
        if not self.email or not self.password:
            print("Missing credentials in .env file")
            return "err"

        login_button = self._find_element_with_selectors(LoginSelectors.MODAL_BUTTONS)

        if login_button:
            login_button.click()
        else:
            print("Not found button to login.")
            return

        email_field = self._find_element_with_selectors(LoginSelectors.EMAIL_FIELDS)
        password_field = self._find_element_with_selectors(LoginSelectors.PASSWORD_FIELDS)

        if email_field and password_field:
            self._random_delay(*Config.RANDOM_DELAY_RANGE)
            email_field.send_keys(self.email)
            password_field.send_keys(self.password)
        else:
            print("Not found input fields to login.")
            return "err"

        submit_button = self._find_element_with_selectors(LoginSelectors.SUBMIT_BUTTONS)

        if submit_button:
            submit_button.click()
        else:
            print("Not found submit button to login.")
            return

        self.driver.get(self.url)
        self._random_delay(*Config.RANDOM_DELAY_RANGE)
        return

    def analyze_pages(self, pages_quantity: int = 1) -> int:
        """
        Parse multiple pages of job listings.

        Args:
            pages_quantity: Number of pages to parse

        Returns:
            Total number of vacancies parsed
        """
        total_vac: int = 0
        for i in range(pages_quantity):
            total_vac += self.analyze_page()

            next_button = self._find_element_with_selectors(JobListSelectors.NEXT_PAGE_BUTTONS)

            if next_button:
                next_button.click()
            else:
                print("Not found button to next page.")

        save_to_csv(self.all_jobs, Config.OUTPUT_FILENAME)
        return total_vac

    def analyze_page(self) -> int:
        """
        Parse a single page of job listings.

        Returns:
            Number of jobs parsed on this page
        """
        container = self.wait_for_element(By.XPATH, JobListSelectors.CONTAINER, Config.LONG_TIMEOUT)
        all_li: List[WebElement] = container.find_elements(By.CSS_SELECTOR, 'li')
        vacancies: int = 0

        for job in all_li:
            try:
                job.click()
                job.find_element(By.CLASS_NAME, JobListSelectors.JOB_CARD_CLASS)
            except Exception:
                continue
            else:
                job_url: str = self.driver.current_url

                if job_url in self.seen_urls:
                    print(f"Duplicate skipped: {job_url}")
                    continue

                self.seen_urls.add(job_url)
                vacancies += 1
                print(f"\n--- Vacancy {vacancies} ---")

                content: WebElement = self.wait_for_element(
                    By.CLASS_NAME, JobDetailSelectors.CONTENT_CLASS
                )

                # Title
                title_text: str = ""
                try:
                    title = content.find_element(By.CSS_SELECTOR, JobDetailSelectors.TITLE)
                    title_text = title.text
                    print(f"Title: {title_text}")
                except Exception:
                    print("Title not found")

                # Company
                company_text: str = ""
                try:
                    company = content.find_element(By.CLASS_NAME, JobDetailSelectors.COMPANY_CLASS)
                    company_text = company.text
                    print(f"Company: {company_text}")
                except Exception:
                    print("Company not found")

                # Work format and employment type
                work_format, employment_type = extract_work_details(content)
                print(f"Work format: {work_format}")
                print(f"Employment type: {employment_type}")

                # Posted date and applicants
                posted_text: str = self._get_meta_value(JobDetailSelectors.POSTED_INDEX)
                if posted_text:
                    print(f"Posted: {posted_text}")
                else:
                    print("Posted info not found")

                applicants_text: str = self._get_meta_value(JobDetailSelectors.APPLICANTS_INDEX)
                if applicants_text:
                    print(f"Applicants: {applicants_text}")
                else:
                    print("Applicants info not found")

                # Description and skills
                description_text: str = ""
                skills_dict: Dict[str, bool] = {}
                try:
                    description = content.find_element(By.XPATH, JobDetailSelectors.DESCRIPTION_XPATH)
                    description_text = description.text
                except Exception:
                    print("Description not found")
                else:
                    skills_dict = extract_tech_skills(description_text)
                    found_skills = [skill for skill, exists in skills_dict.items() if exists]
                    print(f"Found skills: {found_skills}")

                # Seniority level
                seniority_level: Optional[str] = extract_seniority_from_text(title_text)
                if not seniority_level and description_text:
                    seniority_level = extract_seniority_from_text(description_text)

                if seniority_level:
                    print(f"Seniority level: {seniority_level}")
                else:
                    print("Seniority level not found")

                # Build job data
                job_data: Dict[str, Any] = {
                    'title': title_text,
                    'company': company_text,
                    'work_format': work_format,
                    'employment_type': employment_type,
                    'posted': posted_text,
                    'applicants': applicants_text,
                    'seniority_level': seniority_level
                }

                for key, value in skills_dict.items():
                    job_data[key] = value

                self.all_jobs.append(job_data)

            self._random_delay(*Config.DELAY_RANGE)

        print(f"\n--- Found vacancies on this page: {vacancies} ---")
        return vacancies

    def quit(self) -> None:
        """Close the browser."""
        self.driver.quit()