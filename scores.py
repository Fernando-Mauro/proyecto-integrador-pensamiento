"""
scores.py

Simple utilities to persist and retrieve high scores for the memorama game.
"""
from __future__ import annotations

from typing import Dict, List, TypedDict, Any
import sys
import ast
import os

SCORES_FILE = "scores.json"


class ScoreEntry(TypedDict):
    name: str
    score: int
    difficulty: str  # 'facil' | 'medio' | 'dificil'

# Try to import stdlib json; if shadowed by local json.py, fall back to a tiny parser
try:
    import json as _json  # type: ignore
    if not (hasattr(_json, "load") and hasattr(_json, "dump")):
        raise ImportError("shadowed json module")
except Exception:
    _json = None  # type: ignore


def _load_scores(path: str = SCORES_FILE) -> List[ScoreEntry]:
    """Load scores from disk.

    Supports two formats for backward compatibility:
    - Legacy: {"Alice": 120, ...}  (assumed 'dificil')
    - New: [{"name": "Alice", "score": 120, "difficulty": "facil"}, ...]
    """
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            if _json:
                data = _json.load(f)
            else:
                # safe parse for simple dicts {"name": 1}
                txt = f.read()
                data = ast.literal_eval(txt or "{}")

            # normalize to list[ScoreEntry]
            if isinstance(data, list):
                out: List[ScoreEntry] = []
                for item in data:
                    try:
                        name = str(item.get("name"))
                        score = int(item.get("score"))
                        diff = str(item.get("difficulty") or "dificil")
                        if name:
                            out.append({"name": name, "score": score, "difficulty": diff})
                    except Exception:
                        continue
                return out
            elif isinstance(data, dict):
                # legacy dict -> convert assuming 'dificil'
                return [
                    {"name": str(k), "score": int(v), "difficulty": "dificil"}
                    for k, v in dict(data).items()
                    if str(k)
                ]
            else:
                return []
    except Exception:
        # if file is corrupted, start fresh instead of crashing
        return []


def _save_scores(data: List[ScoreEntry], path: str = SCORES_FILE) -> None:
    with open(path, "w", encoding="utf-8") as f:
        if _json:
            _json.dump(data, f, indent=2, ensure_ascii=False)
        else:
            # minimal JSON-like writer (sufficient for our simple list of dicts)
            def _esc(s: str) -> str:
                return s.replace('"', '\\"')
            items = []
            for it in data:
                items.append(
                    "  {\n" +
                    f"    \"name\": \"{_esc(it['name'])}\",\n" +
                    f"    \"score\": {int(it['score'])},\n" +
                    f"    \"difficulty\": \"{_esc(it['difficulty'])}\"\n" +
                    "  }"
                )
            f.write("[\n" + ",\n".join(items) + "\n]")


def write_score(name: str, score: int, difficulty: str = "dificil", path: str = SCORES_FILE) -> None:
    """Write a score for a player.

    - Keep the highest per (player, difficulty).
    - File is created if missing.
    """
    if not name:
        return
    difficulty = (difficulty or "dificil").strip().lower()
    if difficulty not in {"facil", "medio", "dificil"}:
        # normalize common inputs
        if difficulty in {"easy", "e", "4x4"}:
            difficulty = "facil"
        elif difficulty in {"medium", "m", "5x5"}:
            difficulty = "medio"
        elif difficulty in {"hard", "h", "6x6"}:
            difficulty = "dificil"
        else:
            difficulty = "dificil"

    data = _load_scores(path)
    # find existing entry for same (name, difficulty)
    found_idx = None
    for i, it in enumerate(data):
        if it["name"] == name and it["difficulty"] == difficulty:
            found_idx = i
            break
    if found_idx is None:
        data.append({"name": name, "score": int(score), "difficulty": difficulty})
    else:
        if int(score) > int(data[found_idx]["score"]):
            data[found_idx]["score"] = int(score)
    _save_scores(data, path)


def read_scores(path: str = SCORES_FILE) -> List[ScoreEntry]:
    """Return a list of score entries sorted by score desc.

    Each entry has: {"name": str, "score": int, "difficulty": str}
    """
    data = _load_scores(path)
    data.sort(key=lambda it: it.get("score", 0), reverse=True)
    return data
