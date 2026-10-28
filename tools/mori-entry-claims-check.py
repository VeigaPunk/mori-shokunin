#!/usr/bin/env python3
"""Hardened quote-bound entry-claims verifier (round 60, C2 — depth capability).

Evaluates one knowledge entry of the r59 claim class under a materialized
root with the predicates the round-59 verifier spot-check routed as defects
(`corpus/lessons/round-59-verifier-spotcheck.md`, routed item 5; Mo59Critic22
D1-D4, Mo59Critic23 F1-F3, Mo59Critic25, Mo59Reviewer08 F1):

  H1  `grammar:` blocks the verdict. Any claim-shaped line that fails the
      frozen CLAIM regex makes the entry fail (r59: grammar reasons were
      orphaned and a met entry could carry unlimited malformed lines).
  H2  Distinct byte spans. Every claim resolves to a concrete byte span
      (line kind -> the line's byte range; offset kind -> [n, n+len(q))).
      Two claims may not cite the same byte span (line/offset aliasing on a
      one-line file collapses to the same span); each span carries at least
      MIN_SPAN bytes; whitespace-only quotes are rejected.
  H3  Non-degenerate claim texts. Claim texts are pairwise distinct and each
      at least MIN_TEXT characters (r59: nine claims of `x.` counted toward
      claims_min).
  H4  Per-copy row binding. Every cited copy must be covered by a registry
      row (status mined, used-by exactly this entry) whose source cell names
      that copy's .ufo artifact path (r59: one fabricated row could cover
      every copy).
  H5  (in the counter) drift-arm reason attribution; this tool does not scan.

Verdict JSON on stdout:
  {"schema": "mori-entry-claims-v2", "ok": bool, "reasons": [..],
   "stats": {"claims": N, "files": F, "spans": N, "min_span": N}}
Exit 0 iff ok.  Usage errors exit 2.

Usage:
  mori-entry-claims-check.py --root DIR --entry REL --copy-prefix DIR/
    --registry REL --artifacts-json FILE --min-claims N --min-files F
  mori-entry-claims-check.py --selftest [--scratch DIR]

Read-only over the root it is given; writes only inside its own selftest
scratch.  Honors TMPDIR; carries no absolute host path.
"""
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

SCHEMA = "mori-entry-claims-v2"
MIN_SPAN = 8     # H2: minimum distinct bytes per claim span
MIN_TEXT = 10    # H3: minimum characters of claim text

CLAIM = re.compile(
    r"^- \*\*K(\d+)\*\* — (.+?) Quote: `([^`]+)` "
    r"\((\S+?):(line|offset):(\d+); pin ([0-9a-f]{64})\)\s*$")
FRONTMATTER = ("source:", "verified-at:", "recheck:", "coverage-map:")
SID = re.compile(r"source:\s*(S\d+)")
ROW = re.compile(r"^\s{0,3}\|\s*(S\d{3,})\s*\|")


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def span_of(quote, cfile, kind, n, cache):
    """Resolve a claim to a concrete byte span.

    Returns (start, end) byte offsets inside the copy file, or None when the
    span does not exist (bad line number, offset past EOF)."""
    fb = cache.get(cfile)
    if fb is None:
        return None
    q = quote.encode("utf-8")
    if kind == "line":
        flines = fb.split(b"\n")
        if not (1 <= n <= len(flines)):
            return None
        start = sum(len(x) + 1 for x in flines[:n - 1])
        return (start, start + len(flines[n - 1]))
    if not (0 <= n <= len(fb)):
        return None
    return (n, n + len(q))


def eval_root(root, entry_rel, copy_prefix, registry_rel, artifacts, min_claims,
              min_files):
    """Evaluate one entry under root.  Returns (ok, reasons, stats)."""
    root = Path(root)
    reasons = []
    stats = {"claims": 0, "files": 0, "spans": 0, "min_span": 0}
    ep = root / entry_rel
    try:
        text = ep.read_text(encoding="utf-8")
    except OSError:
        return False, ["entry_absent"], stats
    lines = text.splitlines()
    head = lines[:10]
    for k in FRONTMATTER:
        if not any(l.startswith(k) for l in head):
            reasons.append("frontmatter:%s" % k.rstrip(":"))

    cache = {}
    for copy_rel in artifacts:
        p = root / copy_rel
        try:
            cache[copy_rel] = p.read_bytes()
        except OSError:
            cache[copy_rel] = None

    claims = []
    seen_kids = set()
    for ln in lines:
        m = CLAIM.match(ln)
        if not m:
            if "**K" in ln or (ln.lstrip().startswith("-") and "Quote:" in ln):
                # H1: any malformed claim-shaped line fails the entry.
                reasons.append("grammar:%.40s" % ln.strip()[:40])
            continue
        kid, ctext, quote, cfile, kind, n, pin = m.groups()
        if kid in seen_kids:
            reasons.append("distinct:dup_kid=K%s" % kid)
        seen_kids.add(kid)
        claims.append((kid, ctext, quote, cfile, kind, int(n), pin))

    # H3: non-degenerate claim texts.
    texts = {}
    for kid, ctext, *_ in claims:
        t = ctext.strip()
        if len(t) < MIN_TEXT:
            reasons.append("text:short=K%s" % kid)
        if t in texts:
            reasons.append("text:dup=K%s=K%s" % (texts[t], kid))
        else:
            texts[t] = kid

    stats["claims"] = len(claims)
    if len(claims) < min_claims:
        reasons.append("claims_min:%d" % len(claims))
    files = sorted({c[3] for c in claims})
    stats["files"] = len(files)
    if len(files) < min_files:
        reasons.append("files_min:%d" % len(files))
    for f in files:
        if f not in artifacts:
            reasons.append("files:outside=%s" % f)

    # H2: distinct byte spans; minimum span size; no blank quotes.
    spans = {}
    span_lens = []
    for kid, _t, quote, cfile, kind, n, pin in claims:
        if cfile not in artifacts:
            continue
        q = quote.encode("utf-8")
        if not q.strip():
            reasons.append("span:blank=K%s" % kid)
            continue
        sp = span_of(quote, cfile, kind, n, cache)
        if sp is None:
            reasons.append("span:%s" % kid)
            continue
        start, end = sp
        span_lens.append(end - start)
        key = (cfile, start, end)
        if key in spans:
            # H2: line/offset aliasing collapses to one span -> duplicate.
            reasons.append("distinct:dup_span=K%s=K%s" % (spans[key], kid))
        else:
            spans[key] = kid
        if end - start < MIN_SPAN:
            reasons.append("span:short=K%s" % kid)
    stats["spans"] = len(spans)
    stats["min_span"] = min(span_lens) if span_lens else 0

    # pins + byte-exact spans
    for kid, _t, quote, cfile, kind, n, pin in claims:
        if cfile not in artifacts:
            continue
        fb = cache.get(cfile)
        if fb is None:
            reasons.append("pin:copy_absent=%s" % cfile)
            continue
        if sha256(fb) != pin:
            reasons.append("pin:%s" % kid)
        q = quote.encode("utf-8")
        sp = span_of(quote, cfile, kind, n, cache)
        if sp is not None and fb[sp[0]:sp[1]] != q:
            reasons.append("span:%s" % kid)

    # H4: per-copy row binding + mined/used-by (as r59) + source-cell naming.
    sids = set()
    for l in head:
        sids.update(SID.findall(l))
    if not sids:
        reasons.append("rows:no_source_ids")
    try:
        reg = (root / registry_rel).read_text(encoding="utf-8")
    except OSError:
        reg = None
        reasons.append("rows:sources_absent")
    reg_rows = {}
    if reg is not None:
        for sid in sorted(sids):
            hit = None
            for ln in reg.splitlines():
                m = ROW.match(ln)
                if m and m.group(1) == sid:
                    hit = ln
                    break
            if hit is None:
                reasons.append("rows:missing=%s" % sid)
                continue
            cells = [c.strip() for c in hit.strip().strip("|").split("|")]
            if len(cells) != 11:
                reasons.append("rows:bad_row=%s" % sid)
                continue
            if cells[7] != "mined":
                reasons.append("rows:status=%s" % sid)
            if cells[10] != entry_rel:
                reasons.append("rows:usedby=%s" % sid)
            # source cell names artifacts: keep the row's source cell text
            reg_rows[sid] = cells[1]
    # H4: per-copy row binding. A copy is bound when some registry row that
    # is mined, used-by exactly this entry, and 11 cells wide names that
    # copy's .ufo artifact path in its source cell.
    binders = []
    if reg is not None:
        for ln in reg.splitlines():
            m = ROW.match(ln)
            if not m:
                continue
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) == 11 and cells[7] == "mined" \
                    and cells[10] == entry_rel:
                binders.append(cells[1])
    cited_copies = sorted({c[3] for c in claims if c[3] in artifacts})
    for copy_rel in cited_copies:
        art = artifacts[copy_rel]
        if binders and not any(art in b for b in binders):
            reasons.append("rows:binding=%s" % copy_rel)
    return (len(reasons) == 0), reasons, stats


def selftest(scratch=None):
    passed = failed = 0

    def chk(name, cond):
        nonlocal passed, failed
        if cond:
            passed += 1
        else:
            failed += 1
            print("FAIL " + name, file=sys.stderr)

    base = Path(tempfile.mkdtemp(prefix="mori-r60-ecst-",
                                 dir=os.environ.get("TMPDIR") or None))
    try:
        entry = "corpus/knowledge/e.md"
        regf = "corpus/SOURCES.md"
        copies = {
            "corpus/evidence/c1.json": ".ufo/waves/round-54/w1-results.json",
            "corpus/evidence/c2.json": ".ufo/waves/round-55/w1-results.json",
        }
        art = base / "corpus/evidence"
        art.mkdir(parents=True)
        blobs = {}
        # each copy: 4 lines; lines 2 and 3 carry distinct 12-byte quotes
        for i, rel in enumerate(sorted(copies)):
            b = (b'{\n "seats": 64-AAAA,\n "seats": 64-BBBB,\n "n": %d\n}\n'
                 % i)
            (base / rel).write_bytes(b)
            blobs[rel] = b
        c1rel, c2rel = sorted(copies)

        def pin(rel):
            return sha256(blobs[rel])

        def write_entry(claim_lines, front=True):
            p = base / entry
            p.parent.mkdir(parents=True, exist_ok=True)
            head = ("source: S901 — artifact %s\n"
                    "source: S902 — artifact %s\n"
                    "verified-at: 2026-10-28\n"
                    "recheck: 90d\n"
                    "coverage-map: t\n\n"
                    % (copies[c1rel], copies[c2rel])) if front else ""
            p.write_text(head + "\n".join(claim_lines) + "\n")

        def write_reg(rows):
            src = base / regf
            src.parent.mkdir(parents=True, exist_ok=True)
            src.write_text("\n".join(rows) + "\n")

        def good_rows():
            rows = []
            for sid, rel in zip(("S901", "S902"), sorted(copies)):
                rows.append(
                    "| %s | artifact %s captured | own-work | A | scope | "
                    "anchor | teaches | mined | 2026-10-28 | 90d | %s |"
                    % (sid, copies[rel], entry))
            return rows

        def cl(kid, rel, line, quote):
            return ('- **K%d** — claim %s checks seats. Quote: `%s` '
                    '(%s:line:%d; pin %s)' % (kid, kid, quote, rel, line,
                                              pin(rel)))

        def run():
            return eval_root(base, entry, "corpus/evidence/", regf, copies,
                             4, 2)

        # 1: good entry — 4 claims on 4 distinct line spans
        write_entry([cl(1, c1rel, 2, ' "seats": 64-AAAA,'),
                     cl(2, c1rel, 3, ' "seats": 64-BBBB,'),
                     cl(3, c2rel, 2, ' "seats": 64-AAAA,'),
                     cl(4, c2rel, 3, ' "seats": 64-BBBB,')])
        write_reg(good_rows())
        ok, reasons, st = run()
        chk("good_ok", ok and st["claims"] == 4 and st["spans"] == 4
            and st["min_span"] >= MIN_SPAN)
        chk("good_no_reasons", ok and reasons == [])

        # 2 (H1): one malformed claim-shaped line blocks the verdict
        write_entry([cl(1, c1rel, 2, ' "seats": 64-AAAA,'),
                     cl(2, c1rel, 3, ' "seats": 64-BBBB,'),
                     cl(3, c2rel, 2, ' "seats": 64-AAAA,'),
                     cl(4, c2rel, 3, ' "seats": 64-BBBB,'),
                     '- **K99** — dangling claim with no pin or span'])
        ok2, r2, _ = run()
        chk("grammar_blocks", not ok2
            and any(r.startswith("grammar:") for r in r2))

        # 3 (H2): line:2 and offset:N aliasing to the same byte span
        off = blobs[c1rel].split(b"\n")[1]
        start = blobs[c1rel].index(off)
        write_entry([cl(1, c1rel, 2, ' "seats": 64-AAAA,'),
                     '- **K2** — offset alias same span here. Quote: `%s` '
                     '(%s:offset:%d; pin %s)' % (off.decode(), c1rel, start,
                                                 pin(c1rel)),
                     cl(3, c2rel, 2, ' "seats": 64-AAAA,'),
                     cl(4, c2rel, 3, ' "seats": 64-BBBB,')])
        ok3, r3, st3 = run()
        chk("alias_dup_span", not ok3 and st3["spans"] == 3
            and any(r.startswith("distinct:dup_span") for r in r3))

        # 4 (H2): whitespace-only quote
        (base / c1rel).write_bytes(
            b'{\n        \n "seats": 64-BBBB,\n "n": 0\n}\n')
        blobs[c1rel] = (base / c1rel).read_bytes()
        write_entry([cl(1, c1rel, 2, '        '),
                     cl(2, c1rel, 3, ' "seats": 64-BBBB,'),
                     cl(3, c2rel, 2, ' "seats": 64-AAAA,'),
                     cl(4, c2rel, 3, ' "seats": 64-BBBB,')])
        ok4, r4, _ = run()
        chk("blank_quote", not ok4
            and any(r.startswith("span:blank") for r in r4))
        (base / c1rel).write_bytes(
            b'{\n "seats": 64-AAAA,\n "seats": 64-BBBB,\n "n": 0\n}\n')
        blobs[c1rel] = (base / c1rel).read_bytes()

        # 5 (H2): 2-byte quotes on a short-line fixture are too short
        (base / c1rel).write_bytes(b'aa\nbb\ncc\ndd\n')
        blobs[c1rel] = (base / c1rel).read_bytes()
        write_entry([cl(1, c1rel, 1, 'aa'),
                     cl(2, c1rel, 2, 'bb'),
                     cl(3, c1rel, 3, 'cc'),
                     cl(4, c1rel, 4, 'dd')])
        ok5, r5, _ = run()
        chk("short_span", not ok5
            and sum(1 for r in r5 if r.startswith("span:short")) == 4)
        (base / c1rel).write_bytes(
            b'{\n "seats": 64-AAAA,\n "seats": 64-BBBB,\n "n": 0\n}\n')
        blobs[c1rel] = (base / c1rel).read_bytes()

        # 6 (H3): degenerate claim texts
        def clx(kid, rel, line, quote, text):
            return ('- **K%d** — %s Quote: `%s` (%s:line:%d; pin %s)'
                    % (kid, text, quote, rel, line, pin(rel)))

        write_entry([clx(1, c1rel, 2, ' "seats": 64-AAAA,', 'x.'),
                     clx(2, c1rel, 3, ' "seats": 64-BBBB,', 'x.'),
                     clx(3, c2rel, 2, ' "seats": 64-AAAA,', 'y.'),
                     clx(4, c2rel, 3, ' "seats": 64-BBBB,', 'y.')])
        ok6, r6, _ = run()
        chk("degenerate_text", not ok6
            and any(r.startswith("text:short") for r in r6)
            and any(r.startswith("text:dup") for r in r6))

        # 7 (H4): a single row whose source cell names only one artifact
        write_entry([cl(1, c1rel, 2, ' "seats": 64-AAAA,'),
                     cl(2, c1rel, 3, ' "seats": 64-BBBB,'),
                     cl(3, c2rel, 2, ' "seats": 64-AAAA,'),
                     cl(4, c2rel, 3, ' "seats": 64-BBBB,')])
        write_reg(good_rows()[:1])
        ok7, r7, _ = run()
        chk("binding_missing", not ok7
            and any(r.startswith("rows:binding=%s" % c2rel) for r in r7))
        write_reg(good_rows())

        # 8: row status not mined
        write_reg([r.replace("| mined |", "| queued |")
                   for r in good_rows()])
        ok8, r8, _ = run()
        chk("row_status", not ok8
            and sum(1 for r in r8 if r.startswith("rows:status")) == 2)
        write_reg(good_rows())

        # 9: stale pin
        write_entry([cl(1, c1rel, 2, ' "seats": 64-AAAA,'),
                     cl(2, c1rel, 3, ' "seats": 64-BBBB,'),
                     cl(3, c2rel, 2, ' "seats": 64-AAAA,'),
                     cl(4, c2rel, 3, ' "seats": 64-BBBB,')
                     .replace(pin(c2rel), "b" * 64)])
        ok9, r9, _ = run()
        chk("stale_pin", not ok9 and any(r.startswith("pin:") for r in r9))

        # 10: byte-mismatched span (quote not on the cited line)
        write_entry([cl(1, c1rel, 2, ' "seats": 64-AAAA,'),
                     cl(2, c1rel, 3, ' "seats": 64-BBBB,'),
                     cl(3, c2rel, 2, ' "seats": 64-AAAA,'),
                     '- **K4** — wrong line content here. Quote: ` "nope": 1,`'
                     ' (%s:line:3; pin %s)' % (c2rel, pin(c2rel))])
        ok10, r10, _ = run()
        chk("span_mismatch", not ok10
            and any(r == "span:4" for r in r10))

        # 11: frontmatter-less body fails
        write_entry([cl(1, c1rel, 2, ' "seats": 64-AAAA,')], front=False)
        ok11, r11, _ = run()
        chk("no_frontmatter", not ok11
            and any(r.startswith("frontmatter") for r in r11))

        # 12: absent entry
        (base / entry).unlink()
        ok12, r12, _ = run()
        chk("entry_absent", not ok12 and r12 == ["entry_absent"])
        return 0 if failed == 0 else 1
    finally:
        shutil.rmtree(base, ignore_errors=True)


def main(argv):
    if "--selftest" in argv:
        scratch = None
        i = argv.index("--selftest")
        if "--scratch" in argv:
            scratch = argv[argv.index("--scratch") + 1]
        return selftest(scratch)
    opts = {"--root": None, "--entry": None, "--copy-prefix": None,
            "--registry": None, "--artifacts-json": None,
            "--min-claims": "10", "--min-files": "3"}
    i = 0
    while i < len(argv):
        if argv[i] in opts:
            opts[argv[i]] = argv[i + 1]
            i += 2
        else:
            i += 1
    if not all([opts["--root"], opts["--entry"], opts["--registry"],
                opts["--artifacts-json"]]):
        print(__doc__)
        return 2
    try:
        artifacts = json.loads(Path(opts["--artifacts-json"]).read_text())
    except (OSError, ValueError):
        print("artifacts_json unreadable")
        return 2
    ok, reasons, stats = eval_root(
        opts["--root"], opts["--entry"], opts["--copy-prefix"] or "",
        opts["--registry"], artifacts, int(opts["--min-claims"]),
        int(opts["--min-files"]))
    stats["files"] = stats.get("files", 0)
    print(json.dumps({"schema": SCHEMA, "ok": ok, "reasons": reasons,
                      "stats": stats}))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
