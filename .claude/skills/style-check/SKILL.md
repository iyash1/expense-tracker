---
name: style-check
description: Review code for style issues specific to this project's conventions
user-invocable: false
---

# Style review checklist for expense-tracker

Check every Python file for these specific issues:
1. Every function must have a docstring — flag any that don't
2. All variable names must be snake_case — flag camelCase or PascalCase variables
3. User-facing messages must follow format: "[ACTION] description (amount)" — flag deviations
4. No global variables — flag any found at module level (excluding constants in ALL_CAPS)
5. All amounts must be validated as positive floats before use

For each issue found, show the file name, line number, the problem, and the fix.