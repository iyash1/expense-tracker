import json

import pytest

import storage


@pytest.fixture(autouse=True)
def isolated_data_file(tmp_path, monkeypatch):
    """Redirect DATA_FILE to a temp path so tests never touch the real data file."""
    monkeypatch.setattr(storage, "DATA_FILE", tmp_path / "expenses.json")


def test_load_returns_empty_list_when_file_absent():
    """load_expenses returns [] when expenses.json does not exist yet."""
    assert storage.load_expenses() == []


def test_load_returns_empty_list_when_file_is_empty_array(tmp_path, monkeypatch):
    """load_expenses returns [] when expenses.json contains an empty array."""
    f = tmp_path / "expenses.json"
    f.write_text("[]")
    monkeypatch.setattr(storage, "DATA_FILE", f)
    assert storage.load_expenses() == []


def test_save_and_load_roundtrip():
    """Data written by save_expenses is returned unchanged by load_expenses."""
    expenses = [
        {"date": "2026-06-20", "description": "Coffee", "amount": 4.50, "category": "Food"}
    ]
    storage.save_expenses(expenses)
    assert storage.load_expenses() == expenses


def test_save_persists_multiple_records():
    """All records in the list are persisted and returned in order."""
    expenses = [
        {"date": "2026-06-20", "description": "Coffee", "amount": 4.50, "category": "Food"},
        {"date": "2026-06-20", "description": "Bus pass", "amount": 40.00, "category": "Transport"},
    ]
    storage.save_expenses(expenses)
    result = storage.load_expenses()
    assert len(result) == 2
    assert result[1]["description"] == "Bus pass"


def test_save_overwrites_previous_data():
    """A second save replaces the entire file rather than appending."""
    storage.save_expenses([{"date": "2026-06-20", "description": "Old", "amount": 1.00, "category": "X"}])
    storage.save_expenses([{"date": "2026-06-20", "description": "New", "amount": 2.00, "category": "Y"}])
    result = storage.load_expenses()
    assert len(result) == 1
    assert result[0]["description"] == "New"


def test_save_creates_parent_directory(tmp_path, monkeypatch):
    """save_expenses creates missing parent directories before writing."""
    nested = tmp_path / "nested" / "dir" / "expenses.json"
    monkeypatch.setattr(storage, "DATA_FILE", nested)
    storage.save_expenses([])
    assert nested.exists()


def test_save_writes_valid_json(tmp_path, monkeypatch):
    """The file on disk is valid JSON with the correct structure."""
    data_file = tmp_path / "expenses.json"
    monkeypatch.setattr(storage, "DATA_FILE", data_file)
    storage.save_expenses([{"date": "2026-06-20", "description": "Coffee", "amount": 4.50, "category": "Food"}])
    parsed = json.loads(data_file.read_text())
    assert isinstance(parsed, list)
    assert parsed[0]["amount"] == 4.50
