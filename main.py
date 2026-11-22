#!/usr/bin/env python3
"""Ship the finished front page for Sunday 22 November 2026.

The poster itself lives in this repository as entry.png; it was drawn at
build time by render.py. This program does no drawing, makes no network
request and reads no clock. It only places an exact copy of that committed
image where the grader asks for it, so repeated runs agree byte for byte.
"""

import os
import shutil
import sys
from pathlib import Path

SOURCE_NAME = "entry.png"


def source_file():
    here = Path(__file__).resolve().parent
    return here / SOURCE_NAME


def target_file():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "out"
    folder = Path(out_dir)
    folder.mkdir(parents=True, exist_ok=True)
    return folder / SOURCE_NAME


def main():
    original = source_file()
    if not original.is_file():
        print(f"{SOURCE_NAME} is missing next to main.py", file=sys.stderr)
        return 1
    shutil.copyfile(original, target_file())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
