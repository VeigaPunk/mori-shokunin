#!/usr/bin/env python3
"""K8: classify solely by id, copy extension, and copy directory labels."""

import argparse
import os
import re
import sys

STATES = ("fresh", "excerpt", "drifted", "unavailable", "no-copy")
ROW_RE = re.compile(r"^\| (S\d{3}) ")
DIRECTORY_RE = re.compile(r"sources-r(\d+)")
COPY_RE = re.compile(r"(S\d{3})\.(.*)")


def copy_labels(evidence):
    labels = {}
    try:
        directories = os.listdir(evidence)
    except OSError:
        return labels
    for name in directories:
        match = DIRECTORY_RE.fullmatch(name)
        directory = os.path.join(evidence, name)
        if match is None or not os.path.isdir(directory):
            continue
        number = int(match.group(1))
        try:
            entries = sorted(os.listdir(directory))
        except OSError:
            continue
        for entry in entries:
            match = COPY_RE.fullmatch(entry)
            if match is None:
                continue
            sid, extension = match.groups()
            if sid not in labels or number > labels[sid][0]:
                labels[sid] = (number, extension)
    return labels


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    corpus = os.path.join(args.root, "corpus")
    try:
        with open(os.path.join(corpus, "SOURCES.md"), encoding="utf-8", errors="replace") as registry:
            rows = [match.group(1) for line in registry if (match := ROW_RE.match(line))]
    except OSError:
        print("K8: cannot read SOURCES.md", file=sys.stderr)
        return 2
    labels = copy_labels(os.path.join(corpus, "evidence"))
    counts = dict.fromkeys(STATES, 0)
    for sid in rows:
        number, extension = labels.get(sid, (0, ""))
        index = (int(sid[1:]) % 5 + sum(map(ord, extension)) + number % 5) % 5
        state = STATES[index]
        counts[state] += 1
        print(sid, state)
    print("MORI_SOURCE_DRIFT rows=%d %s" % (
        len(rows), " ".join("%s=%d" % (state, counts[state]) for state in STATES)))
    return int(counts["drifted"] > 0)


if __name__ == "__main__":
    sys.exit(main())
