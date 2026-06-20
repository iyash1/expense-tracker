from typing import TypedDict


class Expense(TypedDict):
    """Shape of a single expense record as stored in expenses.json."""
    date: str
    description: str
    amount: float
    category: str
