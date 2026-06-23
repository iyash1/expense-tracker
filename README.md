# Expense Tracker

**Version: 1.0.0**

A lightweight command-line tool for recording and reviewing personal expenses. All data is stored locally in a single JSON file — no database, no dependencies beyond Python.

---

## Requirements

- Python 3.10+
- No third-party packages — standard library only

---

## Quick Start

```bash
python tracker.py add "Morning coffee" 4.50 Food
python tracker.py add "Bus pass" 40 Transport
python tracker.py add "Netflix" 15.99 Entertainment
python tracker.py list
python tracker.py summary
```

---

## Commands

### `add` — Record an expense

```bash
python tracker.py add "<description>" <amount> <category>
```

| Argument | Type | Notes |
|---|---|---|
| `description` | string | What you spent money on. Quote it if it contains spaces. |
| `amount` | float | Must be greater than zero. |
| `category` | string | Free-text label (e.g. `Food`, `Transport`, `Entertainment`). |

**Example**

```bash
python tracker.py add "Morning coffee" 4.50 Food
```

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
| `--category`, `-c` | Filter to a single category (case-insensitive). |

**Examples**

```bash
python tracker.py list
python tracker.py list --category Food
python tracker.py list -c transport
```

**Output**

```
#     Date          Category          Amount   Description
─────────────────────────────────────────────────────────────────
1     2026-06-20    Food               $  4.50  Morning coffee
2     2026-06-20    Transport          $ 40.00  Bus pass
3     2026-06-20    Entertainment      $ 15.99  Netflix
─────────────────────────────────────────────────────────────────
                                       $ 60.49  Total
```

The `--category` filter matches case-insensitively (`food`, `Food`, and `FOOD` all match), but the stored casing is displayed as-is.

---

### `summary` — Totals by category

```bash
python tracker.py summary
```

Groups all expenses by category, sorted alphabetically, with a grand total.

**Output**

```
Category              Total
─────────────────────────────────
Entertainment         $    15.99
Food                  $     4.50
Transport             $    40.00
─────────────────────────────────
TOTAL                 $    60.49
```

Note: category grouping is case-sensitive. `Food` and `food` appear as separate buckets.

---

## Data Storage

Expenses are written to `data/expenses.json`. The file and directory are created automatically on the first `add`.

```json
[
  { "date": "2026-06-20", "description": "Morning coffee", "amount": 4.50, "category": "Food" },
  { "date": "2026-06-20", "description": "Bus pass",       "amount": 40.0, "category": "Transport" }
]
```

The entire file is rewritten on every `add`. There is no partial update. The file is not committed to source control.

---

## Running Tests

```bash
pip install pytest
pytest tests/ -v
```

`conftest.py` adds `src/` to `sys.path`. Tests use `monkeypatch` and `tmp_path` for real file I/O — no mocks.

---

## Project Structure

```
expense-tracker/
├── src/
│   ├── models.py       # Expense TypedDict (date, description, amount, category)
│   ├── storage.py      # load_expenses / save_expenses
│   └── cli.py          # cmd_add, cmd_list, cmd_summary, main
├── tests/
│   ├── test_cli.py
│   └── test_storage.py
├── data/
│   └── expenses.json   # auto-created on first add; not committed
├── conftest.py         # adds src/ to sys.path for pytest
├── tracker.py          # entry point
├── README.md
└── CLAUDE.md
```

---

## Troubleshooting

**`ModuleNotFoundError: No module named 'storage'`**
Run the tracker via `tracker.py`, not directly via `src/cli.py`. Only `tracker.py` adds `src/` to `sys.path`.

```bash
# correct
python tracker.py list

# incorrect — will fail
python src/cli.py list
```

**Table separators show as `?` or boxes**
The table uses the Unicode box-drawing character `─` (U+2500). If your terminal displays garbage characters, set `PYTHONUTF8=1`:

```powershell
$env:PYTHONUTF8 = "1"
python tracker.py list
```

**`No expenses recorded yet`**
No `add` commands have been run yet, or `data/expenses.json` was deleted. Run an `add` to create the file and start tracking.

**Amount rejected**
`add` rejects amounts of zero or below. Pass a positive number:

```bash
python tracker.py add "Lunch" 12.50 Food
```
