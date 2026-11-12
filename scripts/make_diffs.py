#!/usr/bin/env python3
"""
Generate the step-to-step diffs shown in the tutorials.

Convention: in a tutorial directory, step files are named
  <LETTER><N>-<anything>.py      e.g. A1-ping.py, A2-ping.py
For each step N > 1 we write <LETTER><N>-<anything>.diff, a unified diff
against the file of step N-1, with *full* context so that the whole
program is shown, with inserted/deleted lines highlighted.

Generated files are git-ignored; run through `npm start` / `npm run build`
or directly with `uv run scripts/make_diffs.py [dir ...]`.
"""

import re
import sys
import difflib
from pathlib import Path

STEP = re.compile(r"^([A-Z])(\d+)-.*\.py$")
FULL = 10**6


def steps_in(directory: Path):
    found = {}
    for path in directory.glob("*.py"):
        if m := STEP.match(path.name):
            found[(m.group(1), int(m.group(2)))] = path
    return found


def make_diffs(directory: Path) -> int:
    steps = steps_in(directory)
    count = 0
    for (letter, n), path in sorted(steps.items()):
        previous = steps.get((letter, n - 1))
        if previous is None:
            continue
        lines = difflib.unified_diff(
            previous.read_text().splitlines(keepends=True),
            path.read_text().splitlines(keepends=True),
            n=FULL,
        )
        # drop the '---', '+++' and '@@' header lines: keep only the body
        body = list(lines)[3:]
        path.with_suffix(".diff").write_text("".join(body))
        count += 1
    return count


def main():
    roots = [Path(a) for a in sys.argv[1:]] or [Path("user")]
    total = 0
    for root in roots:
        for directory in {p.parent for p in root.rglob("*.py")}:
            total += make_diffs(directory)
    print(f"make_diffs: {total} diff(s) generated")


if __name__ == "__main__":
    main()
