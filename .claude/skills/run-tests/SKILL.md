---
name: run-tests
description: Run the project's test suite and interpret the results
---

# How to run and interpret tests for this project

1. Check if a tests/ folder exists. If not, create test_tracker.py with basic tests first.
2. Run: python -m pytest test_tracker.py -v
3. If pytest is not installed, run: pip install pytest
4. After running, summarize:
   - How many tests passed / failed
   - For each failure, explain what broke and why in plain English
   - Suggest a fix for each failing test