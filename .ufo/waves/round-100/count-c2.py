#!/usr/bin/env python3
"""Round-100 C2 counter (calibration): stated quote word counts in corpus/SOURCES.md match their quotes.

Predicate P2 (frozen; same sentence in contract.md and in the receipt label):
  C2=met iff, in the tree --root DIR,
   (mismatch) every stated quote word count in a registry row of DIR/corpus/SOURCES.md either equals the
              whitespace word count of its quote or is answered, in the same row, by the exact correction
              text `[r100 word-count correction: K→W, ...; counted by whitespace]` listing every mismatch of
              that row in order (a W over 25 written `K→W (over the 25-word cap)`);
   (spurious) no row carries an `r100 word-count correction` that is not that exact text;
   (altered)  every row that carried a stated count at --base is byte-identical to its --base text once
              its correction text (with the one space before it) is removed;
   (census)   `sources-census.sh validate --file DIR/corpus/SOURCES.md` exits 0.
A stated count is `"QUOTE" (N words` or `"QUOTE" (LOCATOR, N words` (pattern A), or `(N words): "QUOTE"` /
`(LOCATOR, N words): "QUOTE"` (pattern B); QUOTE is a double-quoted span that may hold `\\"` escapes; LOCATOR
holds no parenthesis or double quote and is at most 80 characters. Exit 0 met, 1 unmet, 2 setup.
Usage: count-c2.py --root DIR [--base REV] [--repo LANE] [--census PATH]
"""
import argparse, pathlib, re, subprocess, sys

ROW = re.compile(r"^ {0,3}\| *(S\d{3,}) *\|")
Q = r'"((?:[^"\\]|\\.)+)"'
PA = re.compile(Q + r' \((?:[^()"]{0,80}?, )?(\d+) words')
PB = re.compile(r'\((?:[^()"]{0,80}?, )?(\d+) words\): ' + Q)
TAG = "r100 word-count correction"
CAP = 25
BASE = "d1bd1b339b894de0249b0f60702dff9962da88d9"


def stated(line):
    out = []
    for m in PA.finditer(line):
        out.append((m.start(), int(m.group(2)), len(m.group(1).split())))
    for m in PB.finditer(line):
        out.append((m.start(), int(m.group(1)), len(m.group(2).split())))
    out.sort()
    return [(k, w) for _p, k, w in out]


def correction_text(mism):
    items = ["%d→%d%s" % (k, w, " (over the 25-word cap)" if w > CAP else "") for k, w in mism]
    return "[%s: %s; counted by whitespace]" % (TAG, ", ".join(items))


def rows(text):
    d = {}
    for line in text.split("\n"):
        m = ROW.match(line)
        if m:
            d.setdefault(m.group(1), []).append(line)
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--base", default=BASE)
    ap.add_argument("--repo", default=str(pathlib.Path(__file__).resolve().parents[3]))
    ap.add_argument("--census", default="/home/vgpnk/Projects/shokunin/scripts/sources-census.sh")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    src = pathlib.Path(a.root) / "corpus/SOURCES.md"
    if not src.is_file():
        print("C2=setup reason=no-sources"); return 2
    after = src.read_text(encoding="utf-8")
    try:
        before = subprocess.run(["git", "-C", a.repo, "show", "%s:corpus/SOURCES.md" % a.base],
                                capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError:
        print("C2=setup reason=base-unreadable"); return 2
    ra, rb = rows(after), rows(before)
    n_stated = mism_total = uncorrected = spurious = altered = 0
    detail = []
    for sid, lines in ra.items():
        for line in lines:
            ss = stated(line)
            n_stated += len(ss)
            mism = [(k, w) for k, w in ss if k != w]
            mism_total += len(mism)
            want = correction_text(mism) if mism else None
            has_tag = TAG in line
            if mism:
                if line.count(want) != 1:
                    uncorrected += len(mism)
                    detail.append("uncorrected %s %s" % (sid, ",".join("%d->%d" % kw for kw in mism)))
                elif line.count(TAG) != 1:
                    spurious += 1
                    detail.append("spurious %s extra-tag" % sid)
            elif has_tag:
                spurious += 1
                detail.append("spurious %s no-mismatch" % sid)
    for sid, blines in rb.items():
        for bl in blines:
            if not stated(bl):
                continue
            alines = ra.get(sid, [])
            stripped = []
            for al in alines:
                m = re.search(r" \[" + re.escape(TAG) + r": [^\]]*\]", al)
                stripped.append(al[:m.start()] + al[m.end():] if m else al)
            if bl not in stripped:
                altered += 1
                detail.append("altered %s" % sid)
    try:
        c = subprocess.run(["bash", a.census, "validate", "--file", str(src)], capture_output=True,
                           text=True, timeout=300)
        census = "ok" if c.returncode == 0 else "rc%d" % c.returncode
    except (OSError, subprocess.TimeoutExpired):
        census = "unrun"
    failed = [n for n, v in (("mismatch", uncorrected == 0), ("spurious", spurious == 0),
                             ("altered", altered == 0), ("census", census == "ok")) if not v]
    print("C2=%s stated=%d mismatches=%d uncorrected=%d spurious=%d altered=%d census=%s checks_failed=%s base=%s" % (
        "met" if not failed else "unmet", n_stated, mism_total, uncorrected, spurious, altered, census,
        ",".join(failed) or "-", a.base[:8]))
    for d in detail if a.list else detail[:20]:
        print("  " + d)
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
