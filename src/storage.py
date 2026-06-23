"""
Persistence layer for expense records.

Reads and writes the full expenses list to ``data/expenses.json`` on every
operation — no partial updates. ``DATA_FILE`` can be monkey-patched in tests
to redirect I/O to a temporary path without touching the real data file.
"""

import json
from pathlib import Path

from models import Expense

# expenses.json lives in data/ at the project root, one level above src/
DATA_FILE = Path(__file__).parent.parent / "data" / "expenses.json"


def load_expenses() -> list[Expense]:
    """Read expenses from disk, returning an empty list if the file doesn't exist yet."""
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open() as f:
        return json.load(f)


def save_expenses(expenses: list[Expense]) -> None:
    """Write the full expenses list back to disk."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w") as f:
        json.dump(expenses, f, indent=2)
