"""Shared utilities for lightweight test execution without pytest."""
from __future__ import annotations

from dataclasses import dataclass
import math
import time


@dataclass(frozen=True)
class _Approx:
    """Simple numeric comparator similar to pytest.approx."""
    expected: float
    rel: float = 1e-12
    abs_tol: float = 0.0

    def __eq__(self, other):
        return math.isclose(float(other), float(self.expected), rel_tol=self.rel, abs_tol=self.abs_tol)

    def __repr__(self):
        return f"approx(expected={self.expected}, rel={self.rel}, abs={self.abs_tol})"


def approx(expected, rel=1e-12, abs=0.0):
    """Return an approximate matcher for numeric assertions."""
    return _Approx(expected=float(expected), rel=float(rel), abs_tol=float(abs))


def run_module_tests(module_globals):
    """Run test functions (test_*) in a module and print a compact report."""
    test_functions = [
        (name, fn)
        for name, fn in module_globals.items()
        if name.startswith("test_") and callable(fn)
    ]
    test_functions.sort(key=lambda item: item[0])

    passed = 0
    failed = 0
    started = time.perf_counter()

    for name, fn in test_functions:
        try:
            fn()
            passed += 1
            print(f"PASS {name}")
        except Exception as exc:
            failed += 1
            print(f"FAIL {name}: {exc}")

    elapsed = time.perf_counter() - started
    total = passed + failed
    print(f"\n{total} run, {passed} passed, {failed} failed in {elapsed:.2f}s")
    return 0 if failed == 0 else 1
