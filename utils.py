"""Utility functions for the LinkedIn scraper."""

import csv
import random
import time
from typing import List, Dict, Any, Optional


def random_delay(min_seconds: float = 1, max_seconds: float = 3) -> None:
    """
    Add random delay between actions to avoid detection.

    Args:
        min_seconds: Minimum delay in seconds
        max_seconds: Maximum delay in seconds
    """
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)


def save_to_csv(jobs_data: List[Dict[str, Any]], filename: str = "vacancies_warsaw.csv") -> str:
    """
    Save jobs data to CSV file with dynamic columns for skills.

    Args:
        jobs_data: List of job dictionaries
        filename: Output filename

    Returns:
        Path to saved file
    """
    if not jobs_data:
        print("No data to save")
        return filename

    all_keys: set = set()
    for job in jobs_data:
        all_keys.update(job.keys())

    base_fields: List[str] = ['title', 'company', 'work_format', 'employment_type',
                              'posted', 'applicants', 'seniority_level', 'skills']
    other_fields: List[str] = sorted([k for k in all_keys if k not in base_fields])
    fieldnames: List[str] = [f for f in base_fields if f in all_keys] + other_fields

    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for job in jobs_data:
            row = job.copy()
            if 'skills' in row and isinstance(row['skills'], list):
                row['skills'] = ', '.join(row['skills'])
            writer.writerow(row)

    print(f"Saved {len(jobs_data)} vacancies to {filename}")
    return filename