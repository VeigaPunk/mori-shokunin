#!/usr/bin/env python3
"""Conformance fixture: prints the published summary line, flushes, then hangs.

A counter that keys on the summary text alone scores this tool "pass" on the arm it
runs; the round-38 counter must map the expiry to `tool_timeout` and score the arm
FAIL (r37 LabTimeoutBoundary measured the same class as a false pass at exit 124).
"""
import sys
import time

print("appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,"
      "S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] "
      "superseded=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,"
      "S185,S186,S188,S189,S190,S193] round_changed=[S182,S193]")
sys.stdout.flush()
time.sleep(120)
