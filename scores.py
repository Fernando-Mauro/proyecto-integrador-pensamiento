"""
scores.py

Simple utilities to persist and retrieve high scores for the memorama game.
"""
from __future__ import annotations

from typing import Dict
import sys
import ast
import os

SCORES_FILE = "scores.json"

# Try to import stdlib json; if shadowed by local json.py, fall back to a tiny parser
try:
    import json as _json  # type: ignore
    if not (hasattr(_json, "load") and hasattr(_json, "dump")):
        raise ImportError("shadowed json module")
except Exception:
    _json = None  # type: ignore


def _load_scores(path: str = SCORES_FILE) -> Dict[str, int]:
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            if _json:
                data = _json.load(f)
            else:
                # safe parse for simple dicts {"name": 1}
                txt = f.read()
                data = ast.literal_eval(txt or "{}")
            # ensure correct types
            return {str(k): int(v) for k, v in dict(data).items()}
    except Exception:
        # if file is corrupted, start fresh instead of crashing
        return {}


def _save_scores(data: Dict[str, int], path: str = SCORES_FILE) -> None:
    with open(path, "w", encoding="utf-8") as f:
        if _json:
            _json.dump(data, f, indent=2, ensure_ascii=False)
        else:
            # minimal JSON-like writer (sufficient for str->int mapping)
            items = ",\n".join([f'  "{k}": {int(v)}' for k, v in data.items()])
            f.write("{\n" + items + "\n}")


def write_score(name: str, score: int, path: str = SCORES_FILE) -> None:
    """Write a score for a player.

    - If the player already has a score, keep the highest.
    - File is created if missing.
    """
    if not name:
        return
    data = _load_scores(path)
    prev = data.get(name)
    if prev is None or score > prev:
        data[name] = int(score)
        _save_scores(data, path)


def read_scores(path: str = SCORES_FILE) -> Dict[str, int]:
    """Return scores sorted by value desc as an ordered dict-like (regular dict in 3.7+ preserves insertion order)."""
    data = _load_scores(path)
    # sort by score desc
    items = sorted(data.items(), key=lambda x: x[1], reverse=True)
    return {k: v for k, v in items}
