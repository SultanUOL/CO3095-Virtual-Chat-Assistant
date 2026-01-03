# Test file for User Story 35
# Testing Type: whitebox
# Technique: branch_coverage
# Team Member: sa1068
# Original file: test_user_story_35.py

from __future__ import annotations
from pathlib import Path
from vca.core.intents import IntentClassifier
from vca.storage.history_store import HistoryStore
def _write_turns_jsonl(path: Path, turns: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    for i in range(turns):
        lines.append(f'{{"ts":"t{i}u","role":"user","content":"u{i}"}}')
        lines.append(f'{{"ts":"t{i}a","role":"assistant","content":"a{i}"}}')
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

def test_user_story_35_intent_classifier_initialises_compiled_groups() -> None:
    c = IntentClassifier()
    r = c.classify_result("help")
    assert r.intent is not None
    assert c.last_result is not None
