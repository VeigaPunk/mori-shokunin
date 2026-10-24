#!/usr/bin/env python3
"""K1: accept the C1 interface, then deliberately do no work."""

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--root", required=True)
parser.parse_args()
