# A-tempo

## Context

This module uses [A-workspace](https://github.com/Ron-RONZZ-org/A-workspace) as a **git submodule**:


```bash
# Clone with submodules
git clone --recurse-submodules https://github.com/Ron-RONZZ-org/A-tempo.git
# Or if already cloned:
git submodule update --init --recursive
```

**DO NOT edit workspace/ directly** - see [A-workspace](https://github.com/Ron-RONZZ-org/A-workspace) for master context.


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