"""Pytest configuration for the book-4 companion scripts.

Putting this file at the code/ root tells pytest to use that as the
rootdir, so test modules under tests/ can import the sibling scripts
(four_property_test, beta_gating_sanity_check) without sys.path tricks
and without packaging the directory.
"""
import sys
from pathlib import Path

# pytest discovers this conftest before collecting tests; prepending the
# code/ directory to sys.path makes `from four_property_test import ...`
# resolve naturally inside tests/.
sys.path.insert(0, str(Path(__file__).resolve().parent))
