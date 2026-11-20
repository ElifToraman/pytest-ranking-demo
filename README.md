# pytest-ranking demo: live test prioritization in GitHub Actions

A small commerce application with 16 Pytest tests. Twelve tests deliberately
simulate slower operations (0.35--0.45 s each); four payment tests finish quickly.
A controlled regression (`DEMO_BUG=1`) makes `test_discounted_total` fail. Because
that test is in `test_zz_payment.py`, Pytest's default order executes it late.
After one clean run populates pytest-ranking's cache, Quickest-Test-First can
schedule short tests earlier and potentially detect the regression faster.

This is a **teaching demonstration**, not a benchmark on the LRTS dataset.

## Setup

Requires Python 3.11 (recommended) and Git.

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
```

## Local demo: first failure under different orders

Start with an empty ranking cache:

```bash
python -m pytest --cache-clear --rank --rank-weight=1-0-0 -q
```

This clean run teaches the plugin the durations of all tests. Then compare default
order to QTF on the same intentionally buggy application:

```bash
# macOS/Linux, commands from the repository root
DEMO_BUG=1 DEMO_TRACE_FILE=reports/default.json python -m pytest -vv
DEMO_BUG=1 DEMO_TRACE_FILE=reports/ranked.json python -m pytest --rank --rank-weight=1-0-0 --rank-level=function -vv
python scripts/compare_traces.py reports
```

Both failing test commands return exit code 1 **as expected**; run them separately.
The JSON traces record real test order, test durations, and wall-clock time to the
first failed test. `compare_traces.py` prints a Markdown summary.

For Windows PowerShell, set the environment values before each command:

```powershell
$env:DEMO_BUG = '1'
$env:DEMO_TRACE_FILE = 'reports/default.json'
python -m pytest -vv
$env:DEMO_TRACE_FILE = 'reports/ranked.json'
python -m pytest --rank --rank-weight=1-0-0 --rank-level=function -vv
python scripts/compare_traces.py reports
```

## Explore other strategies

| Strategy | Command option | Interpretation |
| --- | --- | --- |
| QTF | `--rank-weight=1-0-0` | Most recently fast tests first |
| RecentFail | `--rank-weight=0-1-0` | More recently failing tests first |
| SimChgPath | `--rank-weight=0-0-1` | Test identifiers most similar to changed Python file paths |
| Hybrid | `--rank-weight=1-1-1` | Equal relative weight to the three normalized heuristic scores |
| Random | `--rank-weight=0-0-0 --rank-seed=42` | Reproducible random baseline |

**RecentFail demonstration:** execute a failing run *with `--rank` enabled* first
so that a previous failure is recorded. Execute the same command again; the
formerly failing test should be favored. A new repository without failure
history cannot demonstrate this on its first run.

**SimChgPath demonstration:** execute a clean ranked run to cache file checksums,
modify `shop/payment.py`, and run with `--rank-weight=0-0-1`. The tool computes
textual similarity with changed `.py` paths; it does **not** compute coverage or
require Git history to identify the file changes. Match depends on path names.

At module granularity (`--rank-level=module`), whole test files are ranked while
tests *within* each file retain their default relative order. With `function`,
each test function can move on its own.

## References

- [pytest-ranking source](https://github.com/softwareTestingResearch/pytest-ranking)
- [pytest-ranking paper, FSE Companion 2025](https://doi.org/10.1145/3696630.3728587)
- [LRTS paper, ISSTA 2024](https://doi.org/10.1145/3650212.3680307)
- [LRTS dataset archive](https://zenodo.org/records/12662090)
