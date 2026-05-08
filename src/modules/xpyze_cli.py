#!/usr/bin/env python3
"""
Console entry point for xpyze.
"""

from __future__ import annotations

import runpy


def main() -> None:
    # Keep this shim so pyproject console_scripts can expose an `xpyze`
    # command without refactoring xpyze.py, whose CLI currently lives in
    # its `if __name__ == "__main__":` block rather than a callable main().
    runpy.run_module("xpyze", run_name="__main__")


if __name__ == "__main__":
    main()
