# Expense Tracker

A lightweight command-line expense tracker with no external dependencies. Records are stored locally in a JSON file.

---

## Requirements

- Python 3.10+
- No third-party packages — standard library only

---

## Running Tests

```bash
pip install pytest
pytest tests/ -v
```

All tests use real file I/O via pytest's `tmp_path` — no mocks.

---

## Quick Start

```bash
python tracker.py add "Coffee" 4.50 Food
python tracker.py list
python tracker.py summary
```

---

## Commands

### `add` — Record an expense

```bash
python tracker.py add "<description>" <amount> <category>
```

| Argument | Type | Description |
|---|---|---|
| `description` | string | What you spent money on. Quote it if it contains spaces. |
| `amount` | float | Amount spent. Must be greater than zero. |
| `category` | string | Free-text label (e.g. `Food`, `Transport`, `Entertainment`). |

**Examples**

```bash
python tracker.py add "Morning coffee" 4.50 Food
python tracker.py add "Bus pass" 40 Transport
python tracker.py add "Netflix" 15.99 Entertainment
```

**Output**

```
Added: Morning coffee — $4.50 [Food]
```

---

### `list` — View all expenses

```bash
python tracker.py list [--category <name>]
```

| Flag | Description |
|---|---|
| `--category`, `-c` | Filter results to a single category (case-insensitive). |

**Examples**

```bash
python tracker.py list
python tracker.py list --category Food
python tracker.py list -c transport
```

**Output**

```
#     Date          Category            Amount  Description
─────────────────────────────────────────────────────────────────
1     2026-06-20    Food              $   4.50  Morning coffee
2     2026-06-20    Transport         $  40.00  Bus pass
3     2026-06-20    Entertainment     $  15.99  Netflix
─────────────────────────────────────────────────────────────────
                                        $  60.49  Total
```

---

### `summary` — Totals by category

```bash
python tracker.py summary
```

Groups all expenses by category and prints a sorted breakdown with a grand total.

**Output**

```
Category                   Total
─────────────────────────────────
Entertainment         $    15.99
Food                  $     4.50
Transport             $    40.00
─────────────────────────────────
TOTAL                 $    60.49
```

---

## Project Structure

```
expense-tracker/
├── src/
│   ├── models.py       # Expense TypedDict (data shape)
│   ├── storage.py      # load_expenses / save_expenses
│   └── cli.py          # command handlers and argument parsing
├── tests/
│   ├── test_cli.py     # tests for cmd_add, cmd_list, cmd_summary
│   └── test_storage.py # tests for load_expenses, save_expenses
├── data/
│   └── expenses.json   # auto-created on first add; not committed to source control
├── conftest.py         # adds src/ to sys.path for pytest
├── tracker.py          # entry point — adds src/ to path, delegates to cli.main
├── README.md
└── CLAUDE.md
```

### Module responsibilities

| File | Responsibility |
|---|---|
| `src/models.py` | Defines the `Expense` TypedDict: `date`, `description`, `amount`, `category`. |
| `src/storage.py` | `load_expenses()` and `save_expenses()` — full list read/write on every call. |
| `src/cli.py` | `cmd_add`, `cmd_list`, `cmd_summary`, and `main` — all user-facing logic. |
| `tracker.py` | Adds `src/` to `sys.path`, imports `main` from `cli`, and runs it. |

---

## Data Storage

Expenses are persisted in `data/expenses.json`. The file and directory are created automatically on the first `add`.

```json
[
  { "date": "2026-06-20", "description": "Morning coffee", "amount": 4.50, "category": "Food" },
  { "date": "2026-06-20", "description": "Bus pass",       "amount": 40.0, "category": "Transport" }
]
```

**Notes**

- Amounts are stored as floats, rounded to 2 decimal places.
- Categories are free-text with no validation. `Food` and `food` are treated as separate categories by `summary` (exact match), but `list --category` filtering is case-insensitive.
- The entire file is rewritten on every `add`. There is no partial update.

---

## Windows Note

The table separators use the Unicode box-drawing character `─` (U+2500). If your terminal shows encoding errors, set `PYTHONUTF8=1`:

```powershell
$env:PYTHONUTF8 = "1"
python tracker.py list
```
