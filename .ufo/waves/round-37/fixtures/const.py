#!/usr/bin/env python3
"""Constant-printer fixture — round-37 C1 negative arm.

Prints the published real-arm constant unconditionally, never reading a history.
The blind arm must reject it (round-36 N2 behaviour); kept as a control that the
challenge arm did not replace the blind witness.
"""
import sys

CONSTANT = (
    "appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,"
    "S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] "
    "round_changed=[S182,S193]")


def main(argv):
    print("changed S041 superseded_by=-")
    print("deleted S069")
    print(CONSTANT)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
