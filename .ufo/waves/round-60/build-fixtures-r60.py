#!/usr/bin/env python3
"""Build the round-60 hostile entry trees (trees-c2h/) deterministically.

Each tree is a materialized root for tools/mori-entry-claims-check.py:
corpus/knowledge/wave-settlement-artifacts-r59.md (entry variant),
corpus/SOURCES.md (registry variant), corpus/evidence/<copy> files with
synthetic bytes, and expect.txt (the reason prefixes the hardened verifier
MUST emit; empty = the tree must verify).  h00-good-control is the
no-false-negative control; h01-h12 each encode one routed met-flip or
grammar class from the round-59 verifier spot-check (Mo59Critic22 D1-D4,
Mo59Critic23 F1-F3, Mo59Reviewer08 F1, Mo59Sentinel58 F2).

Writes trees under .ufo/waves/round-60/trees-c2h/ and the frozen expect
table to .ufo/waves/round-60/trees-c2h-expects.json (the counter embeds the
same table; a committed expect.txt that disagrees is expect_tamper).

Run from the lane repo root:  python3 .ufo/waves/round-60/build-fixtures-r60.py
"""
import hashlib
import json
import sys
from pathlib import Path

OUT = Path(".ufo/waves/round-60/trees-c2h")
EXPECTS = {}
ENTRY = "corpus/knowledge/wave-settlement-artifacts-r59.md"
SOURCES = "corpus/SOURCES.md"
C1 = "corpus/evidence/sources-r59/w1-results-r54.json"
C2 = "corpus/evidence/sources-r59/w1-results-r55.json"
ART = {
    C1: ".ufo/waves/round-54/w1-results.json",
    C2: ".ufo/waves/round-55/w1-results.json",
    "corpus/evidence/sources-r59/w1-results-r56.json":
        ".ufo/waves/round-56/w1-results.json",
    "corpus/evidence/sources-r59/w1-results-r57.json":
        ".ufo/waves/round-57/w1-results.json",
    "corpus/evidence/sources-r59/w1-results-r58.json":
        ".ufo/waves/round-58/w1-results.json",
    "corpus/evidence/sources-r59/w1-settlement-r58.json":
        ".ufo/waves/round-58/evidence/w1-settlement.json",
}

BLOBS = {
    C1: (b'{\n "lane": "mori", "round": 54, "wave": "w1",\n'
         b' "seats": 74,\n "members": 74,\n "results": []\n}\n'),
    C2: (b'{\n "lane": "mori", "round": 55, "wave": "w1",\n'
         b' "seats": 64,\n "members": 64,\n "results": []\n}\n'),
    "corpus/evidence/sources-r59/w1-results-r56.json":
        (b'{\n "lane": "mori", "round": 56, "wave": "w1",\n'
         b' "seats": 64,\n "members": 64,\n "results": []\n}\n'),
    "corpus/evidence/sources-r59/w1-results-r57.json":
        (b'{\n "lane": "mori", "round": 57, "wave": "w1",\n'
         b' "seats": 64,\n "members": 64,\n "results": []\n}\n'),
    "corpus/evidence/sources-r59/w1-results-r58.json":
        (b'{\n "lane": "mori", "round": 58, "wave": "w1",\n'
         b' "seats": 64,\n "members": 64,\n "results": []\n}\n'),
    "corpus/evidence/sources-r59/w1-settlement-r58.json":
        (b'{"schema": "mori-wave-settlement-v1", "settled": 36,'
         b' "partial": 26, "empty": 2}\n'),
}

REG_COPIES = (
    ("S901", C1), ("S902", C2),
    ("S903", "corpus/evidence/sources-r59/w1-results-r56.json"),
    ("S904", "corpus/evidence/sources-r59/w1-results-r57.json"),
)


HEAD_OK = "".join(
    "source: %s — committed artifact `%s` (copy `%s`)\n" % (sid, ART[rel], rel)
    for sid, rel in REG_COPIES) \
    + ("verified-at: 2026-10-28\n"
       "recheck: 90d\n"
       "coverage-map: Core — wave settlement artifact shape\n\n")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def claim(kid, text, quote, copy_rel, kind, n, pinv):
    return ('- **K%d** — %s Quote: `%s` (%s:%s:%d; pin %s)'
            % (kid, text, quote, copy_rel, kind, n, pinv))


def good_claims(min_n=10):
    """Distinct spans (lines 2..4 across C1/C2 and r56/r57 copies) with
    distinct >=10-char texts."""
    lines = {C1: [b' "seats": 74,', b' "members": 74,', b' "results": []'],
             C2: [b' "seats": 64,', b' "members": 64,', b' "results": []'],
             "corpus/evidence/sources-r59/w1-results-r56.json":
                 [b' "seats": 64,', b' "members": 64,', b' "results": []'],
             "corpus/evidence/sources-r59/w1-results-r57.json":
                 [b' "seats": 64,', b' "members": 64,', b' "results": []']}
    texts = ["seats equals members count", "wave name is present",
             "round number is recorded", "lane identity is recorded",
             "results list is present", "seat total is an integer",
             "member total is an integer", "artifact line shape holds",
             "settlement shape is stable", "counts agree per artifact",
             "lane field is nonempty", "wave field is nonempty"]
    out = []
    i = 0
    for rel in (C1, C2, "corpus/evidence/sources-r59/w1-results-r56.json",
                "corpus/evidence/sources-r59/w1-results-r57.json"):
        for ln, q in enumerate(lines[rel], start=3):
            out.append(claim(i + 1, texts[i], q.decode(), rel, "line", ln,
                             sha(BLOBS[rel])))
            i += 1
    return out[:min_n]


def good_registry(entry=ENTRY, mined=True, usedby=True, full=True):
    rows = []
    for sid, rel in REG_COPIES:
        cells = [sid, "artifact %s captured" % ART[rel], "own-work", "A",
                 "scope", "anchor", "teaches",
                 "mined" if mined else "queued",
                 "2026-10-28", "90d",
                 entry if usedby else "corpus/knowledge/other-r1.md"]
        if not full:
            cells = cells[:9]
        rows.append("| " + " | ".join(cells) + " |")
    return "\n".join(rows) + "\n"


def write_tree(name, entry_text, registry_text, extra_copies=None,
               expect=(), blobs=None):
    d = OUT / name
    d.mkdir(parents=True, exist_ok=True)
    ep = d / ENTRY
    ep.parent.mkdir(parents=True, exist_ok=True)
    ep.write_text(entry_text)
    (d / SOURCES).parent.mkdir(parents=True, exist_ok=True)
    (d / SOURCES).write_text(registry_text)
    use = blobs if blobs is not None else BLOBS
    for rel, b in use.items():
        p = d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b)
    (d / "expect.txt").write_text(",".join(EXPECTS.get(name, expect))
                                  + "\n")
    return name


def main():
    if OUT.exists():
        print("refusing to overwrite existing %s" % OUT, file=sys.stderr)
        return 2
    # h00: good control — must verify (empty expect)
    EXPECTS["h00-good-control"] = []
    write_tree("h00-good-control", HEAD_OK + "\n".join(good_claims()) + "\n",
               good_registry())

    # h01 (Critic22 D1/D2): semantically empty — ten `x.` claims on one span
    q = '"lane"'
    pin1 = sha(BLOBS[C1])
    em = [claim(i + 1, "x." if i != 8 else
                "The artifact encodes waveform audio in YAML form.",
                q, C1, "offset", 3, pin1) for i in range(10)]
    em.append("- **K99** — dangling claim with no pin or span")
    EXPECTS["h01-semantically-empty"] = ["distinct:dup_span", "text:short"]
    write_tree("h01-semantically-empty", HEAD_OK + "\n".join(em) + "\n",
               good_registry())

    # h02 (Reviewer08 F1): clean entry + one malformed claim line
    g = good_claims()
    g.append("- **K77** — malformed claim line missing quote and pin")
    EXPECTS["h02-malformed-claim"] = ["grammar"]
    write_tree("h02-malformed-claim", HEAD_OK + "\n".join(g) + "\n",
               good_registry())

    # h03 (Critic23 F1): line/offset aliasing to one byte span
    off = BLOBS[C1].split(b"\n")[1]
    start = BLOBS[C1].index(off)
    al = good_claims(9)
    al.append(claim(10, "offset alias of the same span here", off.decode(),
                    C1, "offset", start, pin1))
    al[0] = claim(1, "seats equals members count", off.decode(), C1, "line",
                  2, pin1)
    EXPECTS["h03-line-offset-alias"] = ["distinct:dup_span"]
    write_tree("h03-line-offset-alias", HEAD_OK + "\n".join(al) + "\n",
               good_registry())

    # h04 (Critic23 F3): whitespace-only quote
    bl = [claim(1, "blank line quote is vacuous", "        ", C1, "line", 7,
                pin1)]
    bl += good_claims()[1:10]
    blobs4 = dict(BLOBS)
    blobs4[C1] = BLOBS[C1] + b'        \n'
    # ^ appended blank line is line 7 of the extended blob
    EXPECTS["h04-blank-quote"] = ["span:blank"]
    write_tree("h04-blank-quote", HEAD_OK + "\n".join(bl) + "\n",
               good_registry(), blobs=blobs4)
    # rebuild claims with the extended blob's pin
    d = OUT / "h04-blank-quote"
    ep = (d / ENTRY).read_text().splitlines()
    ep = [ln.replace(pin1, sha(blobs4[C1])) if "`pin" not in ln else ln
          for ln in ep]
    # (pins in claims must match the extended blob)
    fixed = []
    for ln in ep:
        fixed.append(ln.replace(pin1, sha(blobs4[C1])))
    (d / ENTRY).write_text("\n".join(fixed))

    # h05 (Critic23 F2): distinct but 2-byte spans
    blobs5 = {C1: b'aa\nbb\ncc\ndd\n'}
    sh = [claim(i + 1, "short span claim %d here" % (i + 1),
                ['aa', 'bb', 'cc', 'dd'][i % 4], C1, "line", i + 1,
                sha(blobs5[C1])) for i in range(4)]
    EXPECTS["h05-short-quotes"] = ["span:short"]
    write_tree("h05-short-quotes", HEAD_OK + "\n".join(sh) + "\n",
               good_registry(),
               blobs=dict(blobs5, **{k: v for k, v in BLOBS.items()
                                     if k != C1}))

    # h06 (Critic22 D1): degenerate distinct-span claims, `x.` texts
    dg = [claim(i + 1, "x." if i % 2 else "y.",
                (b' "members": 74,' if i % 2 else b' "seats": 64,').decode(),
                C1 if i % 2 else C2, "line", 2,
                sha(BLOBS[C1 if i % 2 else C2])) for i in range(10)]
    EXPECTS["h06-degenerate-text"] = ["text:short"]
    write_tree("h06-degenerate-text", HEAD_OK + "\n".join(dg) + "\n",
               good_registry())

    # h07 (Critic22 D4): one fabricated row covering both copies
    one_row = ("| S901 | artifact %s captured | own-work | A | scope | "
               "anchor | teaches | mined | 2026-10-28 | 90d | %s |\n"
               % (ART[C1], ENTRY))
    EXPECTS["h07-single-row"] = ["rows:binding"]
    write_tree("h07-single-row", HEAD_OK + "\n".join(good_claims()) + "\n",
               one_row)

    # h08: rows not mined
    EXPECTS["h08-row-not-mined"] = ["rows:status"]
    write_tree("h08-row-not-mined", HEAD_OK + "\n".join(good_claims()) + "\n",
               good_registry(mined=False))

    # h09: used-by another entry
    EXPECTS["h09-usedby-other"] = ["rows:usedby"]
    write_tree("h09-usedby-other", HEAD_OK + "\n".join(good_claims()) + "\n",
               good_registry(usedby=False))

    # h10: stale pin
    st = [ln.replace(sha(BLOBS[C1]), "b" * 64)
          for ln in (HEAD_OK + "\n".join(good_claims()) + "\n")
          .splitlines()]
    EXPECTS["h10-stale-pin"] = ["pin:"]
    write_tree("h10-stale-pin", "\n".join(st) + "\n", good_registry())

    # h11: quote not on the cited line (byte mismatch)
    wm = good_claims()
    wm[0] = claim(1, "wrong line content claimed here", ' "nope": 1,', C1,
                  "line", 2, sha(BLOBS[C1]))
    EXPECTS["h11-wrong-line"] = ["span:"]
    write_tree("h11-wrong-line", HEAD_OK + "\n".join(wm) + "\n",
               good_registry())

    # h12: frontmatter-less body
    body = "\n".join(good_claims()) + "\n"
    EXPECTS["h12-no-frontmatter"] = ["frontmatter"]
    write_tree("h12-no-frontmatter", body, good_registry())

    (OUT.parent / "trees-c2h-expects.json").write_text(
        json.dumps(EXPECTS, indent=1, sort_keys=True) + "\n")
    print("trees=%d expects=%d" % (len(EXPECTS), len(EXPECTS)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
