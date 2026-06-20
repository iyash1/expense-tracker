# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running tests

```bash
pip install pytest
pytest tests/ -v
```

`conftest.py` at the project root adds `src/` to `sys.path` so test files can import `storage`, `cli`, and `models` directly. Tests use `monkeypatch` + `tmp_path` to redirect `storage.DATA_FILE` — real file I/O, no mocks.

## Running the tracker

```bash
python tracker.py add "Description" 9.99 Category
python tracker.py list
python tracker.py summary
```

No dependencies beyond the Python standard library. No install step needed.

## Project structure

```
expense-tracker/
├── src/
│   ├── models.py       # Expense TypedDict
│   ├── storage.py      # load_expenses / save_expenses
│   └── cli.py          # command handlers + main
├── tests/
│   ├── test_cli.py     # tests for cmd_add, cmd_list, cmd_summary
│   └── test_storage.py # tests for load_expenses, save_expenses
├── data/
│   └── expenses.json   # runtime data, not committed
├── conftest.py         # adds src/ to sys.path for pytest
├── tracker.py          # entry point: adds src/ to sys.path, imports cli.main
├── README.md
└── CLAUDE.md
```

## Architecture

- **`src/models.py`**: `Expense` TypedDict — the shape of a single expense record.
- **`src/storage.py`**: `load_expenses` / `save_expenses` — full read/write of `data/expenses.json` on every operation. No partial updates; the whole list is always rewritten.
- **`src/cli.py`**: `cmd_add`, `cmd_list`, `cmd_summary`, and `main` — all command logic and argument parsing.
- **`tracker.py`**: Inserts `src/` into `sys.path` then calls `cli.main`. This is the only entry point.

## Data format

```json
[
  { "date": "2026-06-20", "description": "Coffee", "amount": 3.50, "category": "Food" }
]
```

Categories are free-text — no validation or enum. The summary command groups by exact string match, so casing matters (`Food` vs `food` are separate buckets).

## Conventions
- All functions must have a docstring explaining what they do
- Use snake_case for all variable and function names
- Keep all user-facing messages in a consistent format: "[ACTION] description (amount)"
- Never use global variables — pass data through function parameters
- Python version: 3.10+
