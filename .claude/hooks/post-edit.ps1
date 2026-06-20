# Runs after Claude edits any Python file
# Checks for syntax errors immediately

$editedFile = $env:CLAUDE_HOOK_FILE

if ($editedFile -like "*.py") {
    Write-Host "Checking syntax of $editedFile..."
    python -m py_compile $editedFile
    if ($LASTEXITCODE -ne 0) {
        Write-Host "SYNTAX ERROR in $editedFile — Claude will be notified"
        exit 1
    }
    Write-Host "Syntax OK"
}