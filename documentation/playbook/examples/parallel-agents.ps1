# parallel-agents.ps1
# Run several Claude agents in parallel, each in its own git worktree,
# then clean everything up automatically.
#
# Each task is read-only (analysis), so headless `claude -p` runs without
# permission prompts and makes no edits. To let agents WRITE code, add
# `--permission-mode acceptEdits` to the claude call AND collect the work
# (commit/merge or copy the diff) BEFORE the finally block deletes the branch.

$ErrorActionPreference = "Stop"
$repo = (git rev-parse --show-toplevel)
$lab  = Join-Path $HOME "wt-parallel"        # OUTSIDE OneDrive on purpose

# --- Define the parallel work: a short name + a prompt for each agent ---
$tasks = @(
  @{ name = "cli";     prompt = "In 3 bullets, summarize what src/cli.py does. Do not edit any files." },
  @{ name = "storage"; prompt = "List each function in src/storage.py and what it returns. Do not edit any files." },
  @{ name = "tests";   prompt = "In 3 bullets, summarize what the tests in tests/ cover. Do not edit any files." }
)

$created = @()
try {
  New-Item -ItemType Directory -Force -Path $lab | Out-Null

  # 1) One worktree per task; launch a headless Claude in each, in parallel.
  $jobs = foreach ($t in $tasks) {
    $dir    = Join-Path $lab $t.name
    $branch = "agent/$($t.name)"
    git -C $repo worktree add $dir -b $branch | Out-Null
    $created += @{ dir = $dir; branch = $branch }

    Start-Job -Name $t.name -ScriptBlock {
      param($dir, $prompt)
      Set-Location $dir
      claude -p $prompt 2>&1          # headless; remove "-p" args style if claude isn't on PATH in jobs
    } -ArgumentList $dir, $t.prompt
  }

  Write-Host "Launched $($jobs.Count) agents in parallel. Working..." -ForegroundColor Yellow

  # 2) Wait for all of them, then print each agent's result.
  $jobs | Wait-Job | Out-Null
  foreach ($j in $jobs) {
    Write-Host "`n===== AGENT: $($j.Name) =====" -ForegroundColor Cyan
    Receive-Job $j
  }
}
finally {
  # 3) Automatic cleanup — runs no matter what.
  Get-Job | Remove-Job -Force -ErrorAction SilentlyContinue
  foreach ($c in $created) {
    git -C $repo worktree remove --force $c.dir 2>$null
    git -C $repo branch -D $c.branch 2>$null
  }
  git -C $repo worktree prune
  Remove-Item -Recurse -Force $lab -ErrorAction SilentlyContinue
  Write-Host "`nCleaned up. Worktrees now:" -ForegroundColor Green
  git -C $repo worktree list
}
