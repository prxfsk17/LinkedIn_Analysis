"""XPath and CSS selectors for LinkedIn elements."""

from typing import List, Tuple
from selenium.webdriver.common.by import By


class LoginSelectors:
    """Selectors for login page and modal."""

    MODAL_BUTTONS: List[Tuple[str, str]] = [
        (By.CLASS_NAME, 'contextual-sign-in-modal__sign-in-with-email-cta'),
        (By.XPATH, '//*[@id="base-contextual-sign-in-modal"]/div/section/div/div/div[2]/button'),
    ]

    EMAIL_FIELDS: List[Tuple[str, str]] = [
        (By.ID, 'csm-v2_session_key'),
        (By.NAME, 'session_key'),
        (By.XPATH, '//*[@id="csm-v2_session_key"]'),
        (By.XPATH, "//input[@autocomplete='username']"),
    ]

    PASSWORD_FIELDS: List[Tuple[str, str]] = [
        (By.ID, 'csm-v2_session_password'),
        (By.NAME, 'session_password'),
        (By.XPATH, '//*[@id="csm-v2_session_password"]'),
        (By.XPATH, "//input[@autocomplete='current-password']"),
    ]

    SUBMIT_BUTTONS: List[Tuple[str, str]] = [
        (By.CLASS_NAME, 'sign-in-form__submit-btn--full-width'),
        (By.XPATH, '//*[@id="base-contextual-sign-in-modal"]/div/section/div/div/div[2]/form/div[2]/button'),
    ]


class JobListSelectors:
    """Selectors for job listing page."""

    CONTAINER: str = '//*[@id="main"]/div/div[2]/div[1]/div/ul'
    JOB_CARD_CLASS: str = 'job-card-container--clickable'

    NEXT_PAGE_BUTTONS: List[Tuple[str, str]] = [
        (By.CSS_SELECTOR, 'p #jobs-search-pagination__page-state button'),
        (By.XPATH, '/html/body/div[6]/div[3]/div[4]/div/div/main/div/div[2]/div[1]/div/div[3]/div[2]/button'),
        (By.XPATH, '/html/body/div[6]/div[3]/div[4]/div/div/main/div/div[2]/div[1]/div/div[2]/div[2]/button[2]'),
    ]


class JobDetailSelectors:
    """Selectors for job detail page."""

    CONTENT_CLASS: str = 'jobs-details__main-content'
    TITLE: str = 'h1'
    COMPANY_CLASS: str = 'job-details-jobs-unified-top-card__company-name'

    # Meta fields with dynamic indices
    META_BASE_XPATH: str = '//*[@id="main"]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/div/div[1]/div/div[1]/div/div[3]/div/span/span[{index}]'
    POSTED_INDEX: int = 3
    APPLICANTS_INDEX: int = 5

    DESCRIPTION_XPATH: str = '//*[@id="job-details"]/div/p'

    WORK_FORMAT_ELEMENTS: str = 'button span span strong'