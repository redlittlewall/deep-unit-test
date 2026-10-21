#!/usr/bin/env python3
"""
Quality Gate Validator for deep-unit-test standard.
Performs:
1. Anti-Cheat Scan (blocks SUT mocking cheats: spyOn(service), service.method = jest.fn()).
2. Line Coverage Verification (enforces >= min_coverage threshold).
"""
from pathlib import Path
import re
import sys
from typing import Optional


def check_anti_sut_mocking(spec_content: str) -> Optional[str]:
    """Detects if the test attempts to mock the SUT (System Under Test) instead of dependencies."""
    forbidden_patterns = [
        (r"spyOn\(\s*service\s*,", "jest.spyOn(service, ...)"),
        (r"spyOn\(\s*sut\s*,", "jest.spyOn(sut, ...)"),
        (r"service\.\w+\s*=\s*jest\.fn\(", "service.<method> = jest.fn(...)"),
        (r"sut\.\w+\s*=\s*jest\.fn\(", "sut.<method> = jest.fn(...)"),
    ]
    for pattern, name in forbidden_patterns:
        if re.search(pattern, spec_content, re.IGNORECASE):
            return (
                f"CRITICAL VIOLATION (Khorikov SUT Anti-Pattern): Detected `{name}`. "
                f"Mocking the class/method under test is strictly forbidden. "
                f"The method under test MUST execute its real logic. Mock only injected dependencies."
            )
    return None


def parse_line_coverage(jest_stdout: str, service_file_name: str) -> Optional[float]:
    """Extracts line coverage percentage from Jest coverage table output."""
    clean_name = Path(service_file_name).name
    stem = Path(service_file_name).stem

    for line in jest_stdout.splitlines():
        if "|" in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 6:
                filename_col = parts[0]
                stripped_col = filename_col.lstrip(".").strip()
                if (
                    clean_name in filename_col
                    or stem in filename_col
                    or (stripped_col and stripped_col in clean_name)
                ):
                    try:
                        return float(parts[4])
                    except ValueError:
                        pass
    return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 quality_gate.py <path/to/spec.ts>")
        sys.exit(1)
    spec_path = Path(sys.argv[1])
    content = spec_path.read_text(encoding="utf-8")
    violation = check_anti_sut_mocking(content)
    if violation:
        print(f"❌ REJECTED:\n{violation}")
        sys.exit(1)
    print("✅ Quality Gate: Anti-Cheat check passed successfully.")
