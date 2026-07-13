#!/usr/bin/env bash
# PreToolUse hook: blocks `git push` to the main branch.
# Wired to the Bash matcher in .claude/settings.json.
# Reads the tool call from stdin (JSON), and returns a deny decision as JSON
# rather than exit 2 so the reason surfaces cleanly to Claude.

raw="$(cat)"

# Only concerned with git push commands
printf '%s' "$raw" | grep -Eq 'git[[:space:]]+push' || exit 0

# Target is main if the command names it explicitly, or the current branch is main
targets_main=0
if printf '%s' "$raw" | grep -qw main; then
    targets_main=1
else
    current=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
    [ "$current" = "main" ] && targets_main=1
fi
[ "$targets_main" -eq 0 ] && exit 0

cat <<'JSON'
{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"Pushing to main is blocked. Create a feature branch and open a pull request instead."}}
JSON
exit 0
