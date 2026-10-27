#!/usr/bin/env python3
"""Copy-on-change amendment of the frozen `build-w1-spec.py` (round-51 closure routed defect 6: a frozen file is
never edited in place). The validator refused the frozen spec: `items[39].role "labrat" is not a swarm role`
(evidence/w1-validate-refused.txt). This wrapper imports the frozen builder unchanged and moves that one item
(Mo52LabLaneWrites, a falsification probe that runs code) to the executor role; nothing else changes.
Usage: build-w1-spec-amend.py <freeze> <data>."""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("frozen_builder", os.path.join(HERE, "build-w1-spec.py"))
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)
n = 0
for it in b.items:
    if it["name"] == "Mo52LabLaneWrites" and it["role"] == "labrat":
        it["role"] = "executor"
        n += 1
if n != 1:
    raise SystemExit("amend: expected exactly one labrat item, found %d" % n)
b.main()
