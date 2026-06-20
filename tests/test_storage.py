import json

import pytest

import storage


@pytest.fixture(autouse=True)
def isolated_data_file(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DATA_FILE", tmp_path / "expenses.json")


def test_load_returns_empty_list_when_file_absent():
    assert storage.load_expenses() == []


def test_load_returns_empty_list_when_file_is_empty_array(tmp_path, monkeypatch):
    f = tmp_path / "expenses.json"
    f.write_text("[]")
    monkeypatch.setattr(storage, "DATA_FILE", f)
    assert storage.load_expenses() == []


def test_save_and_load_roundtrip():
    expenses = [
        {"date": "2026-06-20", "description": "Coffee", "amount": 4.50, "category": "Food"}
    ]
    storage.save_expenses(expenses)
    assert storage.load_expenses() == expenses


def test_save_persists_multiple_records():
    expenses = [
        {"date": "2026-06-20", "description": "Coffee", "amount": 4.50, "category": "Food"},
        {"date": "2026-06-20", "description": "Bus pass", "amount": 40.00, "category": "Transport"},
    ]
    storage.save_expenses(expenses)
    result = storage.load_expenses()
    assert len(result) == 2
    assert result[1]["description"] == "Bus pass"


def test_save_overwrites_previous_data():
    storage.save_expenses([{"date": "2026-06-20", "description": "Old", "amount": 1.00, "category": "X"}])
    storage.save_expenses([{"date": "2026-06-20", "description": "New", "amount": 2.00, "category": "Y"}])
    result = storage.load_expenses()
    assert len(result) == 1
    assert result[0]["description"] == "New"


def test_save_creates_parent_directory(tmp_path, monkeypatch):
    nested = tmp_path / "nested" / "dir" / "expenses.json"
    monkeypatch.setattr(storage, "DATA_FILE", nested)
    storage.save_expenses([])
    assert nested.exists()


def test_save_writes_valid_json(tmp_path, monkeypatch):
    data_file = tmp_path / "expenses.json"
    monkeypatch.setattr(storage, "DATA_FILE", data_file)
    storage.save_expenses([{"date": "2026-06-20", "description": "Coffee", "amount": 4.50, "category": "Food"}])
    parsed = json.loads(data_file.read_text())
    assert isinstance(parsed, list)
    assert parsed[0]["amount"] == 4.50
