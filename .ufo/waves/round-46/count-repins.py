#!/usr/bin/env python3
"""Count stale round-45 registry pins in a SKILL.md snapshot."""
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROWS = {
    "r44 gate registry (C2)": ("GATE_REGISTRY_SELFTEST pass=15 fail=0",),
    "r45 ledger counter (C1)": ("C1_SELFTEST pass=16 fail=0", "5f2deea0b35c5e1346229d265aa0c07bf7f365bf6c5acda87648045bce658d23"),
    "r45 gate conformance (C2)": (
        "C2_SELFTEST pass=14 fail=0", "153423c48ca90466e85b02707828f5c6b2cf39c87c68ee67e3f9abee956baf93",
        "9850b3fcc8885456c3e71458b34184d716d54880a91ae5b29c7d003f26708703",
        "8b82ac999091ebe65e765ed69f759910a57049ff0e7c5c4aa56df9c7168f5832", "743 lines",
    ),
    "r44 gate registry (C2) — write scope superseded": (
        "GATE_REGISTRY_SELFTEST pass=15 fail=0", "8b82ac999091ebe65e765ed69f759910a57049ff0e7c5c4aa56df9c7168f5832", "743 lines",
    ),
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("skill", nargs="?", default="SKILL.md")
    args = parser.parse_args()
    lines = Path(args.skill).read_text().splitlines()
    errors = []
    for row, needles in ROWS.items():
        matches = [line for line in lines if line.startswith("| " + row + " |")]
        if len(matches) != 1:
            errors.append(f"{row}: expected one row, found {len(matches)}")
            continue
        missing = [needle for needle in needles if needle not in matches[0]]
        if missing:
            errors.append(f"{row}: stale/missing {len(missing)} pin(s)")
    print(f"MORI_R45_REPINS mismatches={len(errors)} rows={len(ROWS)}")
    for error in errors:
        print(error)
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
