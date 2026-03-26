"""Configuration constants for LinkedIn scraper."""

from typing import Tuple


class Config:
    """Application configuration."""

    # Timeouts (seconds)
    DEFAULT_TIMEOUT: int = 10
    LONG_TIMEOUT: int = 30
    SHORT_TIMEOUT: int = 3

    # Delay ranges (seconds)
    DELAY_RANGE: Tuple[float, float] = (1, 2.6)
    RANDOM_DELAY_RANGE: Tuple[float, float] = (1, 3)

    # Output file
    OUTPUT_FILENAME: str = "vacancies_warsaw.csv"

    # URLs
    LINKEDIN_LOGIN_URL: str = "https://www.linkedin.com/login"
    LINKEDIN_FEED_URL: str = "https://www.linkedin.com/feed/"

    # Browser options
    USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
    WINDOW_SIZE: str = "1920,1080"