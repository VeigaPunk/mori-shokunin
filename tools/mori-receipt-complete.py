#!/usr/bin/env python3
"""mori-receipt-complete — guard: a counter receipt's `failed=` anchor list is
complete and untruncated.

Round 63 (C2, calibration). Mechanizes routed nit 1 of
`corpus/lessons/round-62-verifier-spotcheck.md`: the r61-counter spot-check
receipt committed at r62 (`.ufo/waves/round-62/evidence/r61-counter-spotcheck.txt`)
truncated its `failed=quote_words:` list mid-token at a 200-character line cut
(4 of 14 anchors fully visible), while the counter's own stdout was complete —
the truncation happened at receipt capture, after the counter printed the full
list. Lane rule enforced here: a receipt's failed-anchor list carries the
complete list, or the guard is red.

Predicate
  Every line of the receipt that contains `failed=` is checked. The `failed=`
  value runs to the token's end (`;`-separated; the value ends at the first
  whitespace after `failed=` — the counters print `failed=a;b;c rev=…`, so the
  whitespace ends the list). Each token must be non-empty and built only from
  `[A-Za-z0-9_.:/+-]` (the shape family the lane's counters emit: full anchors
  like `quote_words:psi.c:1268-1270`, class-qualified details like
  `refused:tool_absent`, and bare continuation details like `live_absent` —
  one shared charset). `failed=none` is complete. Findings:
    malformed:<token>       a token is empty or carries a character outside the
                            receipt-safe charset (junk; the last token failing
                            this is reported as truncated_tail instead — the
                            signature of a width cut that ended the line)
    count_mismatch          the fully-listed anchor count disagrees with the
                            expected count — the primary truncation detector.
                            Expected = --expect N when given (the operator's
                            assertion wins), else rows - quotes_ok derived from
                            the same line when both counters parse (the r61/r62
                            C2 counter family's arithmetic: one quote span per
                            row). Applied only when no malformed/truncated_tail
                            finding already exists on the line.

Named limits: a cut exactly at a `;` token boundary leaves only well-formed
tokens — undetectable from the receipt bytes alone when the line carries
neither `rows=`/`quotes_ok=` nor a matching --expect (the selftest pins this
limit as a named case, `boundary_cut_without_counters_undetected`); the r62
receipt itself is caught because its line carries both counters. The guard
reads one file and executes nothing.

Modes
  python tools/mori-receipt-complete.py <receipt-path> [--expect N]

Output: one `finding …` line per finding, then
  `RECEIPT_COMPLETE=complete|unmet failed_lines=N anchors=N truncated_tail=N
  malformed=N count_mismatch=N receipt=<basename>`
Exit: 0 complete · 1 unmet · 2 setup (unreadable path)

Self-test: builds synthetic receipts in one temp dir — fixture bytes written in
binary mode (the r62 lesson Mistakes 1 routed fix, so the selftest is
host-portable: no CRLF translation, no gitconfig dependence) — and checks the
predicate against them: the r62 truncation shape (caught by the derived
count), the boundary-cut named limit, failed=none, the r62 control's
class/detail token shapes, a malformed mid-token, an --expect mismatch, a
complete list, and a missing file. No subprocess, no interpreter words.

v1.1 (round 63, pre-landing self-correction): the first draft's token grammar
invented a class prefix on every `;` token; the r62 control receipt's real
shape (`refused:tool_absent;live_absent;entry_absent`) has bare continuation
details, so the draft false-flagged legitimate receipts — caught by this
selftest before any receipt was scored, predicate rewritten to the shared
charset, --expect made to outrank the derived count, and the boundary-cut
limit pinned as a named arm.
v1 (round 63): initial shape. No baseline, no frozen predecessor.
"""

import argparse
import os
import re
import shutil
import sys
import tempfile

TOKEN_RE = re.compile(r"^[A-Za-z0-9_.:/+-]+$")
FAILED_RE = re.compile(r"failed=(\S*)")
ROWS_RE = re.compile(r"\brows=(\d+)\b")
QUOTES_OK_RE = re.compile(r"\bquotes_ok=(\d+)\b")


def check_receipt(text, expect=None):
    """Return (findings, counters). findings is a list of strings."""
    findings = []
    failed_lines = 0
    anchors = 0
    truncated_tail = 0
    malformed = 0
    count_mismatch = 0
    for raw in text.splitlines():
        m = FAILED_RE.search(raw)
        if not m:
            continue
        failed_lines += 1
        value = m.group(1)
        if value == "none":
            continue
        toks = value.split(";")
        listed = 0
        for i, tok in enumerate(toks):
            if TOKEN_RE.match(tok):
                listed += 1
            elif i == len(toks) - 1:
                findings.append("finding truncated_tail:%s" % tok)
                truncated_tail += 1
            else:
                findings.append("finding malformed:%s" % tok)
                malformed += 1
        anchors += listed
        if not any(f.startswith("finding truncated_tail") or
                   f.startswith("finding malformed") for f in findings):
            if expect is not None:
                expected = expect
                src = "--expect %d" % expect
            else:
                rm = ROWS_RE.search(raw)
                qm = QUOTES_OK_RE.search(raw)
                expected = (int(rm.group(1)) - int(qm.group(1))) if (rm and qm) else None
                src = "derived rows-quotes_ok=%s" % expected
            if expected is not None and listed != expected:
                findings.append("finding count_mismatch:listed=%d %s" % (listed, src))
                count_mismatch += 1
    verdict = "complete" if not findings else "unmet"
    return findings, {"failed_lines": failed_lines, "anchors": anchors,
                      "truncated_tail": truncated_tail, "malformed": malformed,
                      "count_mismatch": count_mismatch}


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("receipt")
    ap.add_argument("--expect", type=int, default=None)
    args = ap.parse_args(argv)
    try:
        with open(args.receipt, "rb") as f:
            text = f.read().decode("utf-8", "replace")
    except OSError as exc:
        print("RECEIPT_COMPLETE_SETUP unreadable: %s" % exc)
        return 2
    findings, c = check_receipt(text, args.expect)
    for f in findings:
        print(f)
    print("RECEIPT_COMPLETE=%s failed_lines=%d anchors=%d truncated_tail=%d "
          "malformed=%d count_mismatch=%d receipt=%s"
          % ("complete" if not findings else "unmet", c["failed_lines"],
             c["anchors"], c["truncated_tail"], c["malformed"],
             c["count_mismatch"], os.path.basename(args.receipt)))
    return 0 if not findings else 1


def selftest():
    base = tempfile.mkdtemp(prefix="receipt-selftest-")
    results = []

    def w(name, text):
        # r62 lesson Mistakes 1 routed fix: fixture bytes are written in binary
        # mode, so no host performs newline translation on them.
        p = os.path.join(base, name)
        with open(p, "wb") as f:
            f.write(text.encode("utf-8"))
        return p

    anchors14 = ";".join("quote_words:psi.c:%d" % n for n in
                         (1268, 1712, 1017, 1540, 1686, 1710, 1268, 1269,
                          228, 1717, 1257, 240, 1711, 1596))
    full = ("C2=unmet pointers=47 rows=47 quotes_ok=33 failed=%s rev=986d4b46\nrc=1\n"
            % anchors14)
    cut = ("C2=unmet pointers=47 rows=47 quotes_ok=33 failed=quote_words:psi.c:1268;"
           "quote_words:psi.c:1712;quote_words:psi.c:1017;quote_words:psi.c:1540;quote_\n"
           "rc=1\n")
    cut_nocount = ("C9=unmet failed=quote_words:psi.c:12;quote_words:psi.c:34;quote_\n"
                   "rc=1\n")
    none = "C1=met pointers=47 rows=47 failed=none rev=8327bdfc\nrc=0\n"
    refused = ("CX=unmet failed=refused:tool_absent;live_absent;entry_absent "
               "rev=2f5b0626\nrc=1\n")
    malformed = ("CZ=unmet rows=2 failed=quote_words:ok_a:1;quote_w…x;quote_words:ok_b:2 "
                 "rev=deadbeef\nrc=1\n")
    short = ("C2=unmet rows=47 quotes_ok=34 failed=%s rev=986d4b46\nrc=1\n"
             % ";".join("quote_words:psi.c:%d" % n for n in range(1000, 1013)))

    # 1: complete 14-anchor list, --expect met -> complete rc 0
    p = w("full.txt", full)
    rc = main([p, "--expect", "14"])
    results.append(("complete_list_expect_met", rc == 0, "rc=%d" % rc))
    # 2: the r62 truncation shape -> caught by the derived count (14 vs 4), rc 1
    p = w("cut.txt", cut)
    rc = main([p])
    results.append(("r62_truncation_caught_by_derived_count", rc == 1, "rc=%d" % rc))
    # 3: named limit — a cut at a token boundary with no counters and no
    # --expect is undetectable from the receipt bytes alone (documented limit;
    # this arm pins it so a future "fix" is a conscious predicate change)
    p = w("cut_nocount.txt", cut_nocount)
    rc = main([p])
    results.append(("boundary_cut_without_counters_undetected", rc == 0, "rc=%d" % rc))
    # 4: failed=none -> complete rc 0
    p = w("none.txt", none)
    rc = main([p])
    results.append(("failed_none_complete", rc == 0, "rc=%d" % rc))
    # 5: the r62 control's class/detail token shapes -> complete rc 0
    p = w("refused.txt", refused)
    rc = main([p])
    results.append(("class_and_bare_detail_tokens_ok", rc == 0, "rc=%d" % rc))
    # 6: malformed mid-token -> unmet rc 1
    p = w("malformed.txt", malformed)
    rc = main([p])
    results.append(("malformed_mid_token", rc == 1, "rc=%d" % rc))
    # 7: --expect outranks the derived count -> mismatch fires, rc 1
    p = w("short.txt", short)
    rc = main([p, "--expect", "14"])
    results.append(("expect_outranks_derived_count", rc == 1, "rc=%d" % rc))
    # 8: missing file -> setup rc 2
    rc = main([os.path.join(base, "absent.txt")])
    results.append(("missing_file_setup", rc == 2, "rc=%d" % rc))

    shutil.rmtree(base, ignore_errors=True)
    fails = 0
    for name, ok, last in results:
        print("%s %s  %s" % ("PASS" if ok else "FAIL", name, last))
        fails += 0 if ok else 1
    print("RECEIPT_COMPLETE_SELFTEST pass=%d fail=%d" % (len(results) - fails, fails))
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.exit(selftest())
    sys.exit(main(sys.argv[1:]))
