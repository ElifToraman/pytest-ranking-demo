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

## Run in GitHub Actions

1. Create an **empty** GitHub repository named `pytest-ranking-demo` (do not add
   an initial README in GitHub).
2. From this folder:

   ```bash
   git init
   git add .
   git commit -m "Add Pytest regression prioritization demo"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/pytest-ranking-demo.git
   git push -u origin main
   ```

3. Open the GitHub repository > **Actions** > **Pytest ranking demonstration**.
4. The automatic `push` run should pass. It initializes and saves plugin history.
5. Select **Run workflow** with `strategy=qtf` and `inject_bug=true`.
6. Open the resulting run, expand the two test steps, and read the **Summary**.
   The failure is intentionally injected, so the final job status will be red.
7. Repeat a manual run with `strategy=recentfail` and `inject_bug=true` to show
   how previously failing tests are favored. For `simchgpath`, select that strategy
   in a manual run: the workflow appends a harmless comment to `shop/payment.py`
   **after restoring the previous cache**, demonstrating checksum-based detection
   of changed Python files. You can separately demonstrate a real committed change.

The workflow restores `.pytest_cache/v/pytest_ranking_data` by a cache-key prefix,
then saves updated data under a new key containing `github.run_id`. This prevents
immutable-cache reuse from freezing the history. It uploads test traces as a CI
artifact and gives a quick comparison in the Actions step summary.

## Important points for a class presentation

- Reordering does **not** necessarily make the full suite faster; compare **time
  to first failure**, not just total duration.
- The first run is a cold start. QTF/RecentFail require historical measurements.
- File-path similarity is a heuristic and can be wrong even when code changed.
- Test order changes may expose order-dependent (flaky) tests. This project has
  no intentionally order-dependent tests.
- An intentionally broken run is expected to produce a **failed CI status**.

## References

- [pytest-ranking source](https://github.com/softwareTestingResearch/pytest-ranking)
- [pytest-ranking paper, FSE Companion 2025](https://doi.org/10.1145/3696630.3728587)
- [LRTS paper, ISSTA 2024](https://doi.org/10.1145/3650212.3680307)
- [LRTS dataset archive](https://zenodo.org/records/12662090)
