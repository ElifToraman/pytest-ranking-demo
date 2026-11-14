# Relationship to the LRTS paper (Cheng et al., ISSTA 2024)

LRTS is a historical *evaluation dataset*: 21,255 CI builds and 57,437 test-suite runs
from 10 large Apache projects, collected from Jenkins during 2020--2023.
The projects are predominantly Java / Scala, with TVM using Python and C++.
Its records describe test outcomes, durations and code changes; they are **not an
installable Python application with directly executable Pytest tests**.

The `pytest-ranking` plugin instead needs live tests that Pytest can collect and run,
plus a Pytest cache persisted between runs. Our self-contained shop project is the
*executable demonstration workload*. It does not claim to reproduce LRTS findings.

Research connection: LRTS compares 59 prioritization approaches and reports that a
simple combination of test speed and recent failure performed particularly well.
This motivates demonstrating both QTF and RecentFail, plus their hybrid.

LRTS dataset: https://zenodo.org/records/12662090
LRTS paper: https://doi.org/10.1145/3650212.3680307
pytest-ranking paper: https://doi.org/10.1145/3696630.3728587
