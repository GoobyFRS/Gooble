# Patching plan for Gooble quality review

## Goal
Improve the bot so it follows the repository standards in AGENTS.md without changing the current behavior or breaking the Mumble integration.

## Review summary
The current bot works, but it violates several quality constraints:
- hardcoded connection settings instead of environment-driven configuration
- use of module-level global state (`bot`, `SERVER`, `PORT`, `NICKNAME`, `PASSWORD`)
- callback bound to a global instead of a constructed closure
- no defensive handling for the alternative `pymumble` import name
- logging and command logic are harder to test and maintain than necessary

## Planned changes

### 1. Configuration cleanup
- Move runtime connection values to `load_settings()`.
- Read from environment variables: `GOOBLE_SERVER`, `GOOBLE_PORT`, `GOOBLE_NICKNAME`, and `GOOBLE_PASSWORD`.
- Keep sensible defaults for local development.
- Preserve existing default behavior when environment vars are unset.

### 2. Eliminate global-state coupling
- Remove the implicit module-level `bot` state.
- Create a `build_on_text_message(bot, nickname)` closure so the callback is scoped to the active bot instance.
- Keep the event handler logic functionally identical for user messages and self-ignoring rules.

### 3. Keep the runtime contract stable
- Preserve the `!hello` reply behavior.
- Preserve the `COMMAND_PREFIX`/`g!` concept and compatibility with the original message trigger.
- Keep the bot start loop and keyboard interrupt shutdown path intact.

### 4. Make imports robust
- Support both `pymumble_py3` and `pymumble` package names.
- Raise a clear error if neither package is available.
- Keep the fix intentionally minimal and non-invasive.

### 5. Improve maintainability and testability
- Add small unit tests for configuration loading and the self-message guard.
- Keep functions small and descriptive, with docstrings and explicit type hints.
- Use structured logging instead of raw print statements where it improves maintainability without altering behavior.

## Implementation notes
- The refactor should be incremental and localized to [main.py](../main.py).
- The patch should avoid adding frameworks or dependencies.
- The code should remain compatible with the existing instructions in AGENTS.md: Python 3, readability first, no unnecessary async complexity.

## Verification checklist
- `python -m unittest tests/test_main.py -q` should pass after the patch.
- The bot should still start with the default values when no env vars are present.
- The `!hello` path should still send a direct reply to the original sender.
- Self-messages should be ignored exactly as before.

## Review status
Planned; patch is staged to preserve function while improving maintainability and compliance with AGENTS.md.
