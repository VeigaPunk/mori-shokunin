#!/usr/bin/env python3
"""C2 J1 control: accept the CLI but skip all history inspection."""

import argparse


parser = argparse.ArgumentParser()
parser.add_argument("rev")
parser.add_argument("--repo", default=".")
parser.add_argument("--round-base")
parser.add_argument("--path", default="corpus/SOURCES.md")
parser.parse_args()
print("appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]")
