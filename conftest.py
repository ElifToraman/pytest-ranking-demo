"""Record *observed* test order and time to first failing test.

The JSON trace does not rank tests. pytest-ranking does the ranking.
"""

import json
import os
import time
from pathlib import Path

_started = None
_observed = []


def pytest_sessionstart(session):
    global _started
    _started = time.perf_counter()
    _observed.clear()


def pytest_runtest_logreport(report):
    # This demo's failures all occur in the test call phase.
    if report.when == "call":
        _observed.append({
            "test": report.nodeid,
            "outcome": report.outcome,
            "duration_s": round(report.duration, 4),
            "elapsed_s": round(time.perf_counter() - _started, 4),
        })


def pytest_sessionfinish(session, exitstatus):
    path = os.getenv("DEMO_TRACE_FILE")
    if not path:
        return
    record = {
        "bug_enabled": os.getenv("DEMO_BUG", "0") == "1",
        "exit_code": int(exitstatus),
        "test_count": len(_observed),
        "first_failure_s": next(
            (entry["elapsed_s"] for entry in _observed if entry["outcome"] == "failed"),
            None,
        ),
        "total_elapsed_s": round(time.perf_counter() - _started, 4),
        "tests": _observed,
    }
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
