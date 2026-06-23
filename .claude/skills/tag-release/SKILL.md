---
name: tag-release
description: Tag and prepare a release of the expense tracker.
disable-model-invocation: true
---
# Release steps
1. Run the test suite; abort if anything fails.
2. Bump the version mentioned in README.md.
3. Show me the proposed `git tag` command — do NOT run it without confirmation.
