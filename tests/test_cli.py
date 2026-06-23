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
