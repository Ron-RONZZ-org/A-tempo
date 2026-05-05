"""Test isolation for A-tempo — minimal, no persistent storage used."""

from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def isolate_tempo(monkeypatch, tmp_path):
    """Isolate any config or keyring access.

    A-tempo is a simple time/clock module with no database. Mock
    keyring access for safety in case A-core utilities are used.
    """
    monkeypatch.setattr("A.core.ai.save_api_key", lambda key, **kw: True)
    monkeypatch.setattr("A.core.ai.get_api_key", lambda **kw: "mock-key")
