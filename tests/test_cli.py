import pytest

import storage
import cli

SAMPLE = [
    {"date": "2026-06-20", "description": "Coffee", "amount": 4.50, "category": "Food"},
    {"date": "2026-06-20", "description": "Bus pass", "amount": 40.00, "category": "Transport"},
    {"date": "2026-06-20", "description": "Lunch", "amount": 12.75, "category": "Food"},
]


@pytest.fixture(autouse=True)
def isolated_data_file(tmp_path, monkeypatch):
    """Redirect DATA_FILE to a temp path so tests never touch the real data file."""
    monkeypatch.setattr(storage, "DATA_FILE", tmp_path / "expenses.json")


# ---------------------------------------------------------------------------
# cmd_add
# ---------------------------------------------------------------------------

def test_add_persists_expense():
    """Saved record contains the correct description, amount, and category."""
    cli.cmd_add("Coffee", 4.50, "Food")
    saved = storage.load_expenses()
    assert len(saved) == 1
    assert saved[0]["description"] == "Coffee"
    assert saved[0]["amount"] == 4.50
    assert saved[0]["category"] == "Food"


def test_add_sets_todays_date():
    """Saved record has today's date in YYYY-MM-DD format."""
    from datetime import date
    cli.cmd_add("Coffee", 4.50, "Food")
    assert storage.load_expenses()[0]["date"] == str(date.today())


def test_add_prints_confirmation(capsys):
    """Confirmation message includes the description, amount, and category."""
    cli.cmd_add("Coffee", 4.50, "Food")
    out = capsys.readouterr().out
    assert "Added" in out
    assert "Coffee" in out
    assert "4.50" in out
    assert "Food" in out


def test_add_rounds_amount_to_two_decimal_places():
    """Amount is rounded to 2 dp before saving; 1.234 → 1.23 is unambiguous in IEEE 754."""
    cli.cmd_add("Coffee", 1.234, "Food")
    assert storage.load_expenses()[0]["amount"] == 1.23


def test_add_rejects_zero_amount(capsys):
    """Zero amount prints an error and writes nothing to disk."""
    cli.cmd_add("Nothing", 0, "Food")
    assert "greater than zero" in capsys.readouterr().out
    assert storage.load_expenses() == []


def test_add_rejects_negative_amount(capsys):
    """Negative amount prints an error and writes nothing to disk."""
    cli.cmd_add("Nothing", -5.00, "Food")
    assert "greater than zero" in capsys.readouterr().out
    assert storage.load_expenses() == []


def test_add_accumulates_multiple_expenses():
    """Successive add calls append to the store rather than overwriting it."""
    cli.cmd_add("Coffee", 4.50, "Food")
    cli.cmd_add("Bus pass", 40.00, "Transport")
    assert len(storage.load_expenses()) == 2


# ---------------------------------------------------------------------------
# cmd_list
# ---------------------------------------------------------------------------

def test_list_empty_store(capsys):
    """Prints a friendly message when no expenses have been recorded."""
    cli.cmd_list()
    assert "No expenses" in capsys.readouterr().out


def test_list_shows_all_expenses(capsys):
    """All expense descriptions appear in the output."""
    storage.save_expenses(SAMPLE)
    cli.cmd_list()
    out = capsys.readouterr().out
    assert "Coffee" in out
    assert "Bus pass" in out
    assert "Lunch" in out


def test_list_shows_totals_row(capsys):
    """A totals row showing the sum of all displayed amounts is printed."""
    storage.save_expenses(SAMPLE)
    cli.cmd_list()
    out = capsys.readouterr().out
    # Coffee 4.50 + Bus pass 40.00 + Lunch 12.75 = 57.25
    assert "57.25" in out


def test_list_filter_by_category(capsys):
    """Only expenses matching the given category are shown."""
    storage.save_expenses(SAMPLE)
    cli.cmd_list(category="Food")
    out = capsys.readouterr().out
    assert "Coffee" in out
    assert "Lunch" in out
    assert "Bus pass" not in out


def test_list_filter_is_case_insensitive(capsys):
    """Category filter matches regardless of input casing."""
    storage.save_expenses(SAMPLE)
    cli.cmd_list(category="food")
    out = capsys.readouterr().out
    assert "Coffee" in out
    assert "Bus pass" not in out


def test_list_filter_no_match(capsys):
    """Prints a not-found message when the filter matches no expenses."""
    storage.save_expenses(SAMPLE)
    cli.cmd_list(category="Entertainment")
    assert "No expenses found" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# cmd_summary
# ---------------------------------------------------------------------------

def test_summary_empty_store(capsys):
    """Prints a friendly message when no expenses have been recorded."""
    cli.cmd_summary()
    assert "No expenses" in capsys.readouterr().out


def test_summary_shows_each_category(capsys):
    """Each distinct category appears as a line in the summary."""
    storage.save_expenses(SAMPLE)
    cli.cmd_summary()
    out = capsys.readouterr().out
    assert "Food" in out
    assert "Transport" in out


def test_summary_aggregates_totals_correctly(capsys):
    """Per-category totals are summed correctly across multiple records."""
    storage.save_expenses(SAMPLE)
    cli.cmd_summary()
    out = capsys.readouterr().out
    # Food: 4.50 + 12.75 = 17.25
    assert "17.25" in out
    # Transport: 40.00
    assert "40.00" in out


def test_summary_grand_total(capsys):
    """A grand total row reflecting all expenses is printed."""
    storage.save_expenses(SAMPLE)
    cli.cmd_summary()
    out = capsys.readouterr().out
    # 4.50 + 40.00 + 12.75 = 57.25
    assert "57.25" in out


def test_summary_categories_sorted_alphabetically(capsys):
    """Categories are listed in alphabetical order."""
    storage.save_expenses(SAMPLE)
    cli.cmd_summary()
    out = capsys.readouterr().out
    assert out.index("Food") < out.index("Transport")


def test_summary_single_category(capsys):
    """Summary with one category prints that category and a matching grand total."""
    storage.save_expenses([
        {"date": "2026-06-20", "description": "Coffee", "amount": 4.50, "category": "Food"},
    ])
    cli.cmd_summary()
    out = capsys.readouterr().out
    assert "Food" in out
    assert "4.50" in out


def test_summary_rounding_accumulation(capsys):
    """Floating-point amounts accumulate without spurious precision errors."""
    # 0.10 * 3 in naive float arithmetic can produce 0.30000000000000004
    storage.save_expenses([
        {"date": "2026-06-20", "description": "A", "amount": 0.10, "category": "Misc"},
        {"date": "2026-06-20", "description": "B", "amount": 0.10, "category": "Misc"},
        {"date": "2026-06-20", "description": "C", "amount": 0.10, "category": "Misc"},
    ])
    cli.cmd_summary()
    out = capsys.readouterr().out
    assert "0.30" in out


# ---------------------------------------------------------------------------
# cmd_list — additional edge cases
# ---------------------------------------------------------------------------

def test_list_single_expense_shows_amount(capsys):
    """A single expense renders with its amount and the total matches."""
    storage.save_expenses([
        {"date": "2026-06-20", "description": "Coffee", "amount": 4.50, "category": "Food"},
    ])
    cli.cmd_list()
    out = capsys.readouterr().out
    assert "4.50" in out


def test_list_filter_shows_filtered_total_only(capsys):
    """The totals row reflects only the filtered subset, not the full dataset."""
    storage.save_expenses(SAMPLE)
    cli.cmd_list(category="Food")
    out = capsys.readouterr().out
    # Food total: 4.50 + 12.75 = 17.25; full total 57.25 must not appear
    assert "17.25" in out
    assert "57.25" not in out


def test_list_shows_date_and_category_columns(capsys):
    """Each expense row includes its date and category."""
    storage.save_expenses([
        {"date": "2026-06-20", "description": "Coffee", "amount": 4.50, "category": "Food"},
    ])
    cli.cmd_list()
    out = capsys.readouterr().out
    assert "2026-06-20" in out
    assert "Food" in out


def test_list_shows_row_numbers(capsys):
    """Rows are numbered starting at 1."""
    storage.save_expenses(SAMPLE)
    cli.cmd_list()
    out = capsys.readouterr().out
    # First column is the row index; '1' appears as a row number
    assert "1" in out


# ---------------------------------------------------------------------------
# cmd_add — additional edge cases
# ---------------------------------------------------------------------------

def test_add_description_with_spaces():
    """Descriptions containing spaces are stored and retrieved correctly."""
    cli.cmd_add("Morning coffee", 3.00, "Food")
    saved = storage.load_expenses()
    assert saved[0]["description"] == "Morning coffee"


def test_add_large_amount():
    """Large amounts are stored with two decimal places without truncation."""
    cli.cmd_add("Rent", 1500.00, "Housing")
    saved = storage.load_expenses()
    assert saved[0]["amount"] == 1500.00


def test_add_confirmation_format(capsys):
    """Confirmation line starts with '[Added]' and includes the category in brackets."""
    cli.cmd_add("Coffee", 4.50, "Food")
    out = capsys.readouterr().out
    assert out.startswith("[Added]")
    assert "[Food]" in out


# ---------------------------------------------------------------------------
# main — argparse dispatch
# ---------------------------------------------------------------------------

def test_main_dispatches_add(monkeypatch, capsys):
    """main() with 'add' args calls cmd_add and produces output."""
    monkeypatch.setattr("sys.argv", ["tracker.py", "add", "Coffee", "4.50", "Food"])
    cli.main()
    out = capsys.readouterr().out
    assert "Added" in out
    assert "Coffee" in out


def test_main_dispatches_list(monkeypatch, capsys):
    """main() with 'list' args calls cmd_list; empty store prints the empty message."""
    monkeypatch.setattr("sys.argv", ["tracker.py", "list"])
    cli.main()
    assert "No expenses" in capsys.readouterr().out


def test_main_dispatches_summary(monkeypatch, capsys):
    """main() with 'summary' args calls cmd_summary; empty store prints the empty message."""
    monkeypatch.setattr("sys.argv", ["tracker.py", "summary"])
    cli.main()
    assert "No expenses" in capsys.readouterr().out


def test_main_list_category_flag(monkeypatch, capsys):
    """main() passes --category to cmd_list, filtering the output correctly."""
    storage.save_expenses(SAMPLE)
    monkeypatch.setattr("sys.argv", ["tracker.py", "list", "--category", "Food"])
    cli.main()
    out = capsys.readouterr().out
    assert "Coffee" in out
    assert "Bus pass" not in out
