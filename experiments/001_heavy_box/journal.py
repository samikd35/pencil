"""Append one production event, with verified local artifact references."""
import argparse
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import math
from pathlib import Path
import uuid

ROOT = Path(__file__).resolve().parent
STATUSES = ("started", "completed", "passed", "failed", "pending_review", "selected", "rejected")


def artifact(root, name):
    path = (root / name).resolve()
    relative = path.relative_to(root.resolve())
    data = path.read_bytes()
    return {"path": relative.as_posix(), "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}


def append_event(root, *, stage, status, intent, method, result, decision="", inputs=(), outputs=(), sources=(), seconds=None, reviewer=None):
    if status not in STATUSES:
        raise ValueError("Unknown event status")
    if not all(isinstance(value, str) and value.strip() for value in (stage, intent, method, result)):
        raise ValueError("Stage, intent, method, and result must be nonempty text")
    if seconds is not None and (not math.isfinite(seconds) or seconds < 0):
        raise ValueError("Duration must be finite and nonnegative")
    if reviewer is not None and (not isinstance(reviewer, str) or not reviewer.strip()):
        raise ValueError("Reviewer must identify who actually reviewed the artifact")
    event = {
        "schema_version": 1, "id": str(uuid.uuid4()),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "stage": stage, "status": status, "intent": intent, "method": method,
        "inputs": [artifact(root, name) for name in inputs],
        "outputs": [artifact(root, name) for name in outputs],
        "result": result, "decision": decision, "sources": list(sources), "duration_seconds": seconds,
    }
    if reviewer is not None:
        event["reviewer"] = reviewer
    with (root / "events.jsonl").open("a", encoding="utf-8") as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        stream.write(json.dumps(event, ensure_ascii=False, allow_nan=False) + "\n")
        stream.flush()
    return event


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for field in ("stage", "intent", "method", "result"):
        parser.add_argument("--" + field, required=True)
    parser.add_argument("--status", choices=STATUSES, required=True)
    parser.add_argument("--decision", default="")
    parser.add_argument("--input", dest="inputs", action="append", default=[])
    parser.add_argument("--output", dest="outputs", action="append", default=[])
    parser.add_argument("--source", dest="sources", action="append", default=[])
    parser.add_argument("--seconds", type=float)
    parser.add_argument("--reviewer")
    args = parser.parse_args()
    try:
        event = append_event(ROOT, **vars(args))
    except (OSError, ValueError) as error:
        parser.exit(1, f"Journal entry not written: {error}\n")
    print(f"Recorded {event['stage']}: {event['status']}")
