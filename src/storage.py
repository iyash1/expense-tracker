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
