# PreToolUse hook: blocks `git push` to the main branch.
# Wired to the Bash matcher in .claude/settings.json.
# Reads the tool call from stdin (JSON), and returns a deny decision as JSON
# rather than exit 2 so the reason surfaces cleanly to Claude.

$raw = [Console]::In.ReadToEnd()

try {
    $payload = $raw | ConvertFrom-Json
} catch {
    exit 0  # not JSON we understand — don't block
}

$command = $payload.tool_input.command
if (-not $command) { exit 0 }

# Only concerned with git push commands
if ($command -notmatch '\bgit\s+push\b') { exit 0 }

# Target is main if the command names it explicitly, or the current branch is main
$targets_main = $false
if ($command -match '\bmain\b') {
    $targets_main = $true
} else {
    $current = git rev-parse --abbrev-ref HEAD 2>$null
    if ($current -eq 'main') { $targets_main = $true }
}

if (-not $targets_main) { exit 0 }

$decision = @{
    hookSpecificOutput = @{
        hookEventName            = 'PreToolUse'
        permissionDecision       = 'deny'
        permissionDecisionReason = 'Pushing to main is blocked. Create a feature branch and open a pull request instead.'
    }
}
$decision | ConvertTo-Json -Depth 5 -Compress
exit 0
