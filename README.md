# A-tempo

## Context

For architecture and API reference, see [A-workspace](./workspace/).

A-tempo - Print current local time and day of week

## Install

```bash
pip install A-tempo
```

Requires **A-core** (automatically installed as dependency).

## Usage

```bash
A tempo           # Show current local time
A tempo -z       # Show all UTC offsets
A tempo --horzono 9  # Show time for UTC+9
```

## About

A-tempo is a plugin for the [A](https://github.com/Ron-RONZZ-org/A-core/) framework.

**A-tempo depends on A-core** for:
- Plugin discovery via entry points
- i18n (tr() for multilingual support)
- SQLite with WAL mode when needed
- Shared utilities (error(), info(), run())

See the [A-core documentation](https://github.com/Ron-RONZZ-org/A-core/) for more on the framework.

## License

GPL-3.0-only