#!/usr/bin/env python3
"""Control: a tool that never reads the registry. It answers `unmet` when the harness hands it
a round-48-style variant name (`variant-J1.md`, `variant-N1.md`, a `c1-J*` scratch directory) and
`met` otherwise — the leak round 48's w1/CritC1Counter.md F1 found. Under the round-49 counter's
opaque handles it must score junk_met > 0."""
import os
import re
import sys
blob = " ".join(sys.argv) + " " + os.environ.get("TMPDIR", "")
if re.search(r"variant-[JN]\d|c1-[JN]\d", blob):
    print("PIN_CHECK=unmet mismatches=1 stub=filename-sniffer")
    sys.exit(1)
print("PIN_CHECK=met tally_pins=99 stub=filename-sniffer")
