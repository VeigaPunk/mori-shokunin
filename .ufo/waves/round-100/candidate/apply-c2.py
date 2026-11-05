#!/usr/bin/env python3
"""Round-100 C2 transform: append the exact word-count correction to each mismatched SOURCES.md row.

Uses the frozen counter's own grammar (count-c2.py `stated`, `correction_text`) so the transform and the
counter read the same stated counts. The correction goes at the end of the row's anchor cell (cell 6),
preceded by one space; nothing else in the row changes. Usage: apply-c2.py DIR
"""
import importlib.util, pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("c2", HERE.parent / "count-c2.py")
c2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c2)


def main():
    p = pathlib.Path(sys.argv[1]) / "corpus/SOURCES.md"
    lines = p.read_text(encoding="utf-8").split("\n")
    changed = []
    for i, line in enumerate(lines):
        m = c2.ROW.match(line)
        if not m:
            continue
        mism = [(k, w) for k, w in c2.stated(line) if k != w]
        if not mism:
            continue
        parts = line.split("|")
        # parts[0] = leading spaces, parts[1] = id, ..., parts[6] = anchor cell
        if len(parts) != 13:
            sys.exit("apply-c2: %s has %d cells" % (m.group(1), len(parts) - 2))
        cell = parts[6]
        parts[6] = cell.rstrip(" ") + " " + c2.correction_text(mism) + " "
        lines[i] = "|".join(parts)
        changed.append("%s:%s" % (m.group(1), ",".join("%d->%d" % kw for kw in mism)))
    p.write_text("\n".join(lines), encoding="utf-8")
    print("apply-c2: corrected %d rows: %s" % (len(changed), " ".join(changed)))


if __name__ == "__main__":
    main()
