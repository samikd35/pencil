"""Run with python3 test_journal.py; does not change the real journal."""
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from journal import append_event


with TemporaryDirectory() as folder:
    root = Path(folder)
    asset = root / "pose.txt"
    asset.write_text("pose one", encoding="utf-8")
    fields = dict(stage="design", status="pending_review", intent="Review pose", method="test", result="Line one\nline two")
    first = append_event(root, inputs=["pose.txt"], **fields)
    asset.write_text("pose two", encoding="utf-8")
    second = append_event(root, outputs=["pose.txt"], **fields)
    lines = (root / "events.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert json.loads(lines[0])["result"] == "Line one\nline two"
    assert first["inputs"][0]["sha256"] == hashlib.sha256(b"pose one").hexdigest()
    assert first["inputs"][0]["sha256"] != second["outputs"][0]["sha256"]
    assert first["id"] != second["id"]
    for bad in (dict(inputs=["missing.png"]), dict(outputs=["../outside.png"]), dict(seconds=float("nan")), dict(status="approved_without_review")):
        try:
            append_event(root, **(fields | bad))
        except (OSError, ValueError):
            pass
        else:
            raise AssertionError(f"Invalid entry accepted: {bad}")
    assert (root / "events.jsonl").read_text(encoding="utf-8").splitlines() == lines
print("Journal checks passed: append, hashes, multiline text, and invalid-input rejection.")
