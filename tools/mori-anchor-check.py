#!/usr/bin/env python3
"""mori-anchor-check — mechanical located-line and word-count verification of
source-row quote anchors against a pinned copy (the QUALITY 162 check, made
runnable; fleet and host observability lane, detection and report only).

Round 72 (C3, operability + capability acquisition). The r71 closure routed
two defects in the lane's own S584 trail (D71-1: a located-line anchor drifted
:828->:829; D71-2: two recorded word-counts misstated, 22->26 and 17->15).
QUALITY 162 (round 71) already requires pin-verification of located-line
anchors by hand; this tool makes that check a runnable gate so the drift class
is caught mechanically instead of by eye:
  - a recorded (line, exact-quote) anchor LOCATES only if the exact quote text
    occurs on that line of the pinned copy (a line span A-B locates if the
    quote occurs on any one line of the span);
  - a recorded word-count MATCHES only if the recorded quote text's own
    whitespace-token count equals the recorded number — the same count
    `grep -o <quote> | wc -w` prints for one occurrence of the quote — so a
    recorded count that misstates its own recorded text fails even though the
    text locates, and a second sentence sharing the located line cannot skew
    the count.

What it is NOT: not a crawler, not a fetcher (the pin is a local file; live
byte-identity is a separate curl receipt, e.g.
.ufo/waves/round-72/evidence/source-s584-reopen-r72.txt), not a SOURCES.md
parser (the caller lists the anchors it wants verified, exactly as recorded),
and not a verdict on a row's tier, scope or teaches cells — citation hygiene
only.

Modes
  python tools/mori-anchor-check.py --pin PATH --check SPEC [--check SPEC ...]
  python tools/mori-anchor-check.py --selftest

SPEC format (single argument, fields separated by "|"):
  LABEL|LINE|WORDS|TEXT
  LABEL|A-B|WORDS|TEXT
  LABEL|LINE|-|TEXT        (WORDS "-" = no word-count check)
TEXT is the exact quote expected on the line (or on one line of the span).
LABEL is a short caller-chosen id echoed on the output line (numbers/shapes
only; TEXT is never echoed — output stays counts-only, the lane redaction
posture; the selftest's redaction arm pins that).

Output
  anchor item=<LABEL> span=<LINE or A-B> verdict=ok|mislocated|wordcount_mismatch located_on=<line|-> occurrences=<k|-> words_counted=<n|-> words_recorded=<m|->
  ANCHOR_CHECK: PASS items=N ok=N pin_sha256=<hex> pin_bytes=<n>
or
  ANCHOR_CHECK: FAIL items=N ok=N mislocated=N wordcount_mismatch=N pin_sha256=<hex> pin_bytes=<n>
Exit: 0 every anchor located and every recorded word-count matched · 1 any
mislocated or mismatched anchor · 2 unreadable pin or malformed SPEC (usage
errors are never a verification verdict).

Self-test: offline only — its own fixtures in one temp dir, written as bytes
and removed on exit; no network, no child processes, no live reads. Arms:
located ok; mislocated (recorded line is a heading, quote one line below);
word-count mismatch; line-span locate (quote on the span's second line);
span all-zero; mixed multi-item FAIL with per-verdict counts; redaction (a
marker token in the fixture never reaches stdout); missing pin rc 2;
malformed SPEC rc 2; WORDS "-" skips the count arm; a quote occurring twice
on one line still locates and counts words from the first occurrence.

v1 (round 72): initial shape. No baseline, no frozen predecessor.
"""

import argparse
import hashlib
import os
import shutil
import sys
import tempfile

USAGE_EXIT = 2


class AnchorError(Exception):
    """A verification that genuinely could not run (never a verdict)."""


def _load_pin(path):
    """Read the pinned copy as utf-8 text, keeping line structure."""
    try:
        with open(path, "rb") as fh:
            raw = fh.read()
    except OSError as exc:
        raise AnchorError("pin_unreadable:%s" % type(exc).__name__)
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise AnchorError("pin_not_utf8:%s" % type(exc).__name__)
    lines = text.split("\n")
    return lines, hashlib.sha256(raw).hexdigest(), len(raw)


def _parse_span(field):
    """'829' -> (829, 829); '826-827' -> (826, 827); else raise."""
    field = field.strip()
    if "-" in field:
        lo_s, hi_s = field.split("-", 1)
        try:
            lo, hi = int(lo_s), int(hi_s)
        except ValueError:
            raise AnchorError("spec_span_not_int")
        if lo < 1 or hi < lo:
            raise AnchorError("spec_span_order")
        return lo, hi
    try:
        line = int(field)
    except ValueError:
        raise AnchorError("spec_line_not_int")
    if line < 1:
        raise AnchorError("spec_line_negative")
    return line, line


def _parse_spec(spec):
    """LABEL|LINE|WORDS|TEXT -> (label, lo, hi, words_or_None, text)."""
    parts = spec.split("|", 3)
    if len(parts) != 4:
        raise AnchorError("spec_fields")
    label, span_s, words_s, text = parts[0].strip(), parts[1].strip(), parts[2].strip(), parts[3]
    if not label or not text:
        raise AnchorError("spec_empty_label_or_text")
    lo, hi = _parse_span(span_s)
    words = None
    if words_s != "-":
        try:
            words = int(words_s)
        except ValueError:
            raise AnchorError("spec_words_not_int")
        if words < 0:
            raise AnchorError("spec_words_negative")
    return label, lo, hi, words, text


def check_item(lines, lo, hi, words, text):
    """One anchor check -> verdict dict (counts and shapes only).

    The word-count arm recomputes the count from the recorded TEXT itself
    (the whitespace-token count one occurrence of the quote produces — the
    same number `grep -o <quote> | wc -w` prints for that occurrence), so a
    recorded count that misstates the recorded text fails even though the
    text locates, and extra sentences sharing the located line cannot skew
    the count.
    """
    occurrences_at = {}
    for line_no in range(lo, hi + 1):
        if line_no - 1 < len(lines):
            occurrences_at[line_no] = lines[line_no - 1].count(text)
    located_on = next((n for n in sorted(occurrences_at) if occurrences_at[n] > 0), None)
    if located_on is None:
        return {"verdict": "mislocated", "located_on": "-", "occurrences": 0,
                "words_counted": "-",
                "words_recorded": words if words is not None else "-"}
    words_counted = len(text.split())
    verdict = "ok"
    if words is not None and words_counted != words:
        verdict = "wordcount_mismatch"
    return {"verdict": verdict, "located_on": located_on,
            "occurrences": occurrences_at[located_on],
            "words_counted": words_counted, "words_recorded": words if words is not None else "-"}


# ------------------------------------------------------------------ selftest

FIXTURE = (
    "<h2 id=\"remarks\">Remarks</h2>\n"
    "<p>The interrupt-time count begins at zero when the system starts.</p>\n"
    "<p>If the function succeeds, the return value is nonzero. MARKER-TOKEN-VALUE.</p>\n"
)

Q_ZERO = "The interrupt-time count begins at zero when the system starts."
Q_FAIL = "If the function succeeds, the return value is nonzero. MARKER-TOKEN-VALUE."


def _fixture(tmpdir):
    path = os.path.join(tmpdir, "fixture.html")
    with open(path, "wb") as fh:
        fh.write(FIXTURE.encode("utf-8"))
    return path


def run_selftest():
    """11 offline arms; every fixture written as bytes in one temp dir.
    Expected counts are DERIVED from the fixture sentences (len(text.split())),
    never recalled — the r71 fixture-arithmetic lesson, applied."""
    arms = []
    tmpdir = tempfile.mkdtemp(prefix="mori-anchor-check-selftest-")
    try:
        pin = _fixture(tmpdir)
        q_zero_n = len(Q_ZERO.split())
        q_fail_n = len(Q_FAIL.split())

        # 1. located ok (quote one line below the heading; derived word count)
        res = check_item(FIXTURE.split("\n"), 2, 2, q_zero_n, Q_ZERO)
        arms.append(("located_ok", res["verdict"] == "ok" and res["words_counted"] == q_zero_n))

        # 2. mislocated: recorded line is the heading, quote is one line below
        res = check_item(FIXTURE.split("\n"), 1, 1, q_zero_n, Q_ZERO)
        arms.append(("mislocated", res["verdict"] == "mislocated"))

        # 3. word-count mismatch: located, recorded count wrong (derived - 1)
        res = check_item(FIXTURE.split("\n"), 2, 2, q_zero_n - 1, Q_ZERO)
        arms.append(("wordcount_mismatch", res["verdict"] == "wordcount_mismatch"))

        # 4. span locate: quote on the span's second line
        res = check_item(FIXTURE.split("\n"), 1, 2, q_zero_n, Q_ZERO)
        arms.append(("span_located", res["verdict"] == "ok" and res["located_on"] == 2))

        # 5. span all-zero: quote nowhere in the span
        res = check_item(FIXTURE.split("\n"), 1, 1, None, Q_FAIL)
        arms.append(("span_all_zero", res["verdict"] == "mislocated"))

        # 6. mixed multi-item: one ok + one mislocated + one mismatch
        lines = FIXTURE.split("\n")
        r1 = check_item(lines, 2, 2, q_zero_n, Q_ZERO)
        r2 = check_item(lines, 1, 1, q_zero_n, Q_ZERO)
        r3 = check_item(lines, 3, 3, q_fail_n - 1, Q_FAIL)
        mixed = (r1["verdict"] == "ok" and r2["verdict"] == "mislocated"
                 and r3["verdict"] == "wordcount_mismatch")
        arms.append(("mixed_multi_item", mixed))

        # 7. redaction: the marker token in the fixture text must not leak
        #    through a rendered item line (render() emits counts/labels only)
        res = check_item(lines, 3, 3, q_fail_n, Q_FAIL)
        rendered = render_item("redact", "3", res)
        arms.append(("redaction", "MARKER-TOKEN-VALUE" not in rendered))

        # 8. missing pin -> AnchorError (rc 2 path), never a fake verdict
        try:
            _load_pin(os.path.join(tmpdir, "absent.html"))
            arms.append(("missing_pin", False))
        except AnchorError as exc:
            arms.append(("missing_pin", "pin_unreadable" in str(exc)))

        # 9. malformed SPEC fields (all six bad shapes must raise)
        bad_specs_raise = True
        for bad in ("only-two|fields", "label|notanint|-|text",
                    "label|3|notanint|text", "label|0|-|text",
                    "label|5-3|-|text", "|3|-|text"):
            try:
                _parse_spec(bad)
                bad_specs_raise = False
                break
            except AnchorError:
                continue
        arms.append(("malformed_spec", bad_specs_raise))

        # 10. WORDS "-" skips the count arm (located, no count check)
        label, lo, hi, words, text = _parse_spec("skip|2|-|%s" % Q_ZERO)
        res = check_item(FIXTURE.split("\n"), lo, hi, words, text)
        arms.append(("words_skipped", res["verdict"] == "ok" and res["words_recorded"] == "-"))

        # 11. quote occurring twice on one line still locates; the word-count
        #     arm counts ONE occurrence's tokens, occurrences reported
        double = "<p>Alpha beta gamma. Alpha beta gamma.</p>\n"
        res = check_item(double.split("\n"), 1, 1, 3, "Alpha beta gamma.")
        arms.append(("double_locate", res["verdict"] == "ok" and res["occurrences"] == 2
                     and res["words_counted"] == 3))
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    for name, ok in arms:
        print("selftest %-16s %s" % (name, "PASS" if ok else "FAIL"))
    failed = [n for n, ok in arms if not ok]
    if failed:
        print("ANCHOR_CHECK_SELFTEST: FAIL (%d cases)" % len(arms))
        return 1
    print("ANCHOR_CHECK_SELFTEST: PASS (%d cases)" % len(arms))
    return 0


def render_item(label, span, res):
    return ("anchor item=%s span=%s verdict=%s located_on=%s occurrences=%s "
            "words_counted=%s words_recorded=%s" % (
                label, span, res["verdict"], res["located_on"],
                res["occurrences"], res["words_counted"], res["words_recorded"]))


# ------------------------------------------------------------------ main

def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="mori-anchor-check",
        description="Verify recorded quote anchors (line + word count) against a pinned copy.")
    parser.add_argument("--pin", help="path to the pinned copy (required unless --selftest)")
    parser.add_argument("--check", action="append", default=[],
                        help="LABEL|LINE|WORDS|TEXT  (WORDS '-' skips the count arm; repeatable)")
    parser.add_argument("--selftest", action="store_true",
                        help="run the offline selftest and exit")
    args = parser.parse_args(argv)

    if args.selftest:
        return run_selftest()
    if not args.pin:
        parser.error("--pin is required unless --selftest")
    if not args.check:
        parser.error("no --check anchors given (nothing to verify)")

    try:
        specs = [_parse_spec(spec) for spec in args.check]
        lines, sha_hex, nbytes = _load_pin(args.pin)
    except AnchorError as exc:
        print("ANCHOR_CHECK: UNREADABLE reason=%s" % str(exc).lstrip("AnchorError(").rstrip(")"))
        return USAGE_EXIT

    ok = mislocated = mismatch = 0
    for label, lo, hi, words, text in specs:
        span = str(lo) if lo == hi else "%d-%d" % (lo, hi)
        res = check_item(lines, lo, hi, words, text)
        print(render_item(label, span, res))
        if res["verdict"] == "ok":
            ok += 1
        elif res["verdict"] == "mislocated":
            mislocated += 1
        else:
            mismatch += 1

    items = len(specs)
    if mislocated or mismatch:
        print("ANCHOR_CHECK: FAIL items=%d ok=%d mislocated=%d wordcount_mismatch=%d "
              "pin_sha256=%s pin_bytes=%d" % (items, ok, mislocated, mismatch, sha_hex, nbytes))
        return 1
    print("ANCHOR_CHECK: PASS items=%d ok=%d pin_sha256=%s pin_bytes=%d"
          % (items, ok, sha_hex, nbytes))
    return 0


if __name__ == "__main__":
    sys.exit(main())
