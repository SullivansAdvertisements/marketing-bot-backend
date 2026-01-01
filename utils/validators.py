from typing import List

def validate_non_empty(value: str, field_name: str):
    if not value or not value.strip():
        raise ValueError(f"{field_name} cannot be empty")


def validate_budget(amount: float):
    if amount <= 0:
        raise ValueError("Budget must be greater than 0")


def validate_countries(countries: List[str]):
    if not countries:
        raise ValueError("At least one country must be selected")


def validate_age_range(age_min: int, age_max: int):
    if age_min < 13:
        raise ValueError("Minimum age must be at least 13")
    if age_min >= age_max:
        raise ValueError("age_min must be less than age_max")


def validate_url(url: str):
    if not url.startswith("http"):
        raise ValueError("URL must start with http or https")
