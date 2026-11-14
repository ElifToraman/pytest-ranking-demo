"""Print a compact summary of real test execution traces."""
import json
import os
import sys
from pathlib import Path


def main():
    folder = Path(sys.argv[1] if len(sys.argv) > 1 else "reports")
    records = []
    for name in ("default", "ranked"):
        path = folder / f"{name}.json"
        if not path.exists():
            raise SystemExit(f"Missing {path}; run both test commands first.")
        records.append((name, json.loads(path.read_text(encoding="utf-8"))))

    lines = ["## Observed test execution (not a simulation)", ""]
    lines += ["| Run | Tests | First failure | Test session | First executed test |", "|---|---:|---:|---:|---|"]
    for name, record in records:
        first = record["tests"][0]["test"] if record["tests"] else "(none)"
        first_failure = (
            f'{record["first_failure_s"]:.3f} s'
            if record["first_failure_s"] is not None else "none"
        )
        lines.append(
            f'| {name} | {record["test_count"]} | {first_failure} | '
            f'{record["total_elapsed_s"]:.3f} s | `{first}` |'
        )
    default = records[0][1]["first_failure_s"]
    ranked = records[1][1]["first_failure_s"]
    if default is not None and ranked is not None:
        lines.extend(["", f"**Observed first-failure improvement:** {default - ranked:+.3f} seconds "
                             "(positive means ranked detected the failure sooner)."])
    lines.extend(["", "Test run exit statuses: " + ", ".join(
        f'{name}={record["exit_code"]}' for name, record in records
    )])
    summary = "\n".join(lines) + "\n"
    print(summary)
    output = os.getenv("GITHUB_STEP_SUMMARY")
    if output:
        with open(output, "a", encoding="utf-8") as stream:
            stream.write(summary)


if __name__ == "__main__":
    main()
