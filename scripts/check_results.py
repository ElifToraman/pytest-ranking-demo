"""After uploading reports/cache, propagate unexpected test failures to CI."""
import json
import os
from pathlib import Path

folder = Path("reports")
statuses = {name: json.loads((folder / f"{name}.json").read_text())["exit_code"]
            for name in ("default", "ranked")}
print("Test results:", statuses)
if any(code != 0 for code in statuses.values()):
    if os.getenv("DEMO_BUG") == "1":
        print("The regression was deliberately enabled; a red CI job is expected.")
    raise SystemExit(1)
print("All tests passed.")
