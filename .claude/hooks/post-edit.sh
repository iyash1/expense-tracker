#!/usr/bin/env bash
# Runs after Claude edits any Python file
# Checks for syntax errors immediately

edited_file="$CLAUDE_HOOK_FILE"

if [[ "$edited_file" == *.py ]]; then
    echo "Checking syntax of $edited_file..."
    python3 -m py_compile "$edited_file"
    if [ $? -ne 0 ]; then
        echo "SYNTAX ERROR in $edited_file — Claude will be notified"
        exit 1
    fi
    echo "Syntax OK"
fi
