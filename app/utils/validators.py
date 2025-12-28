# app/utils/validators.py

from datetime import date
from typing import List


def validate_budget(amount: int):
    if amount < 500:
        raise ValueError("Budget must be at least $5.00 (500 cents)")


def validate_dates(start: date, end: date):
    if end <= start:
        raise ValueError("End date must be after start date")


def validate_age_range(min_age: int, max_age: int):
    if min_age < 13:
        raise ValueError("Minimum age must be 13+")
    if max_age < min_age:
        raise ValueError("Max age must be greater than min age")


def validate_countries(countries: List[str]):
    if not countries:
        raise ValueError("At least one country must be selected")

    for c in countries:
        if len(c) != 2:
            raise ValueError(f"Invalid country code: {c}")