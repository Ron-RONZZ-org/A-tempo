# AGENTS.md — Rules for A-tempo
This file extends [A-workspace](./workspace/AGENTS.md).

This file extends root A-core AGENTS.md for the A-tempo plugin.

## Project Overview

A-tempo is a CLI plugin that shows the current local time.

## Relationship to A-core

**A-tempo depends on A-core** for:
- `A` package for i18n (`tr()`), output (`error()`, `info()`), and subprocess (`run()`)
- Plugin discovery via entry points
- SQLite utilities when needed
- **API Reference**: See [A-core AGENTS.md](https://github.com/Ron-RONZZ-org/A-core/blob/main/AGENTS.md#api-reference)

All source code must import from `A`, not duplicate utilities.

## Architecture

```
src/A_tempo/
├── __init__.py       # Plugin exports
├── cli.py            # Typer app (depends on A)
├── service.py        # Business logic (depends on A)
└── data/
    └── storage.py    # SQLite (depends on A.data)
```

**Rule:** Service layer uses A-core, CLI layer uses Typer + A output utils.

## Code Standards

1. Import from `A` — never duplicate utilities
2. Use `tr()` for all user-facing strings
3. Use `error()` for errors, `info()` for info
4. Type hints on all public functions
5. Docstrings on all public functions
6. Tests required (pytest-mock for subprocess)

## Testing

```bash
poetry run pytest tests/
```

## What to Avoid

- Don't duplicate A-core utilities
- Don't skip i18n (use `tr()`)
- Don't use `print()` — use `A.utils.output`