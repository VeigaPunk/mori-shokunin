# Mo61MutC2a — C2 mutation probe

## Findings (frozen bytes; report only)

Axes: verdict discrimination, witness isolation, exact restoration.

**ROUTED DEFECT: all three mutants survive the frozen executable selftest oracle and entering-revision control.** Each arm is behavior-bearing: a new, isolated scratch hostile fixture kills its matching mutant. These new fixtures were committed only inside scratch; they are NOT witnesses committed in the frozen lane. No contract/counter amendment is proposed.

The selftest checks only `ok == want` (count-c2.py:276-283). Dropping an arm changes printed failure reasons but not the expected boolean:

| Mutant | Frozen selftest, --floor 6 | Entering control | Newly built isolated hostile | Verdict |
|---|---|---|---|---|
| delete span_small :140-142 | rc=0, pass=10 fail=0 | rc=1 entry_absent, unchanged | pristine rc=1 span_small; mutant rc=0 met | survives frozen oracle; routed coverage defect |
| delete quote_dup :143-145 | rc=0, pass=10 fail=0 | rc=1 entry_absent, unchanged | pristine rc=1 quote_dup; mutant rc=0 met | survives frozen oracle; routed coverage defect |
| :127-133 set equality -> rows>=pointers | rc=0, pass=10 fail=0 | rc=1 entry_absent, unchanged | pristine rc=1 missing+orphan; mutant rc=0 met | survives frozen oracle; routed coverage defect |

For M3 the replacement is `if len(anchor_list) < len(pset): res["failed"].append("rows_lt_pointers")`. The separate exact-count check at :185-186 stays intact. The new swap fixture keeps counts equal (47) and therefore isolates set identity.

An external exact-transcript comparison against evidence/selftest-c2.txt **would** distinguish all three via changed failure reasons. That is not the executable selftest's boolean oracle; no assertion of those reason strings appears at :277. Accordingly the finding is specifically missing verdict-discriminating witnesses, not that the transcripts are identical.

### Masking evidence

- :266 small-span uses `a a a a a a`, which is not located in a.rst:5-7. Removing span_small yields quote_missing instead; case still passes.
- :267 dup-quote copies the line-5 quote into anchor a.rst:9, where it is not located. Removing quote_dup yields quote_missing instead; case still passes.
- :264 row-missing also fails rows_ne_pointers; :265 orphan also fails quote_words (four words) and rows_ne_pointers. No frozen case swaps missing/orphan anchors while preserving count.

### Default selftest baseline is red (inconclusive mutation detector)

`--selftest --scratch <seat scratch>` with default floor 40 gives pristine rc=1, `case good: ok=False want=True FAIL failed=['pointer_floor:6<40']`, `C2_SELFTEST pass=9 fail=1`. All mutants and restored bytes give the same aggregate. This is a baseline failure, NOT a killed mutant. `--selftest --floor 6` reproduces the committed receipt exactly apart from its appended `rc=0` trailer. Floor 0 also reproduces it; the receipt alone does not establish which value was originally used. Live fixture/control runs below use default floor 40 throughout. See :38 (default floor), :205-206 (six deduplicated synthetic pointers), :291 and :296-297 (argument forwarded unchanged).

## Commands and fixture provenance

Freeze: 7370a731abcafc4c803111de7c22cd6264d63be1. Entering/control: 325f7e639916fcbc77fa2ec7475951a1b86bb1cb.

`S=/fast/scratch/hyaku/mori-r61/Mo61MutC2a`; all execution cwd/TMPDIR were under S after setup. The initial disk guard was green: rc=0, scratch free 371.2G, /tmp free 97.5G. No tools installed.

Commands (expanded per variant/fixture):

```sh
TMPDIR="$S" python3 "$S/<variant>.py" --selftest --scratch "$S/st-<variant>"
TMPDIR="$S" python3 "$S/<variant>.py" --selftest --floor 6 --scratch "$S/f6-<variant>"
TMPDIR="$S" python3 "$S/<variant>.py" 325f7e639916fcbc77fa2ec7475951a1b86bb1cb --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch "$S/run"
TMPDIR="$S" python3 "$S/<variant>.py" <fixture-rev> --repo "$S/fx/<fixture>" --scratch "$S/run"
```

New scratch fixtures use the exact committed source-entry and all six pinned v7.3 copies from 7370a731. All six sha256s matched PINS. Synthetic registry rows are mined and used-by-bound. Good fixture has 47 unique pointers/rows, 31 same + 16 mechanically chosen moved rows, four cited files; it is a mechanics fixture, not an upstream semantic recheck claim.

- smallspan: replace psi.c:1268 row by moved/cgroup-v2.rst:596/`~~~~~~~~~~~~~ - C0 - C00` (five words, five distinct bytes, located).
- dup: quote from psi.c:1284-1288 is also used at psi.c:1282-1288, where the same quote is genuinely located.
- swap: replace anchor psi.rst:36-38 with psi.rst:1-188 and a unique located quote, retaining 47 rows.

Fixture repos were created under explicit scratch paths with `git -C <fixture> init -q`, then their top levels asserted equal to those paths before add/commit. Every fixture git operation named that fixture with `-C`; identity t/t@t was used only there. Lane/fleet git commands were read-only.

## Actual live-state matrix

```text
good / pristine-count-c2 rc=0
C2=met pointers=47 rows=47 same=31 moved=16 changed=0 quotes_ok=47 spans_ok=47 sources=4 failed=none rev=56bc371454cbf0ffc1c45187b55764bcaa8f4670

good / mut-span-small rc=0
C2=met pointers=47 rows=47 same=31 moved=16 changed=0 quotes_ok=47 spans_ok=47 sources=4 failed=none rev=56bc371454cbf0ffc1c45187b55764bcaa8f4670

good / mut-quote-dup rc=0
C2=met pointers=47 rows=47 same=31 moved=16 changed=0 quotes_ok=47 spans_ok=47 sources=4 failed=none rev=56bc371454cbf0ffc1c45187b55764bcaa8f4670

good / mut-anchor-set rc=0
C2=met pointers=47 rows=47 same=31 moved=16 changed=0 quotes_ok=47 spans_ok=47 sources=4 failed=none rev=56bc371454cbf0ffc1c45187b55764bcaa8f4670

smallspan / pristine-count-c2 rc=1
C2=unmet pointers=47 rows=47 same=31 moved=15 changed=0 quotes_ok=46 spans_ok=46 sources=4 failed=span_small:psi.c:1268 rev=b3d63d653b7c4181f04043d65e556760c3b3bb42

smallspan / mut-span-small rc=0
C2=met pointers=47 rows=47 same=31 moved=16 changed=0 quotes_ok=47 spans_ok=47 sources=4 failed=none rev=b3d63d653b7c4181f04043d65e556760c3b3bb42

smallspan / mut-quote-dup rc=1
C2=unmet pointers=47 rows=47 same=31 moved=15 changed=0 quotes_ok=46 spans_ok=46 sources=4 failed=span_small:psi.c:1268 rev=b3d63d653b7c4181f04043d65e556760c3b3bb42

smallspan / mut-anchor-set rc=1
C2=unmet pointers=47 rows=47 same=31 moved=15 changed=0 quotes_ok=46 spans_ok=46 sources=4 failed=span_small:psi.c:1268 rev=b3d63d653b7c4181f04043d65e556760c3b3bb42

dup / pristine-count-c2 rc=1
C2=unmet pointers=47 rows=47 same=30 moved=16 changed=0 quotes_ok=46 spans_ok=46 sources=4 failed=quote_dup:psi.c:1284-1288 rev=1c079f88d0c0afcd6ac4bc209939a7e55e2f7f59

dup / mut-span-small rc=1
C2=unmet pointers=47 rows=47 same=30 moved=16 changed=0 quotes_ok=46 spans_ok=46 sources=4 failed=quote_dup:psi.c:1284-1288 rev=1c079f88d0c0afcd6ac4bc209939a7e55e2f7f59

dup / mut-quote-dup rc=0
C2=met pointers=47 rows=47 same=31 moved=16 changed=0 quotes_ok=47 spans_ok=47 sources=4 failed=none rev=1c079f88d0c0afcd6ac4bc209939a7e55e2f7f59

dup / mut-anchor-set rc=1
C2=unmet pointers=47 rows=47 same=30 moved=16 changed=0 quotes_ok=46 spans_ok=46 sources=4 failed=quote_dup:psi.c:1284-1288 rev=1c079f88d0c0afcd6ac4bc209939a7e55e2f7f59

swap / pristine-count-c2 rc=1
C2=unmet pointers=47 rows=47 same=31 moved=16 changed=0 quotes_ok=47 spans_ok=47 sources=4 failed=rows_missing:psi.rst:36-38;rows_orphan:psi.rst:1-188 rev=dde7cff904234eca0cd58357135188a25a67e3da

swap / mut-span-small rc=1
C2=unmet pointers=47 rows=47 same=31 moved=16 changed=0 quotes_ok=47 spans_ok=47 sources=4 failed=rows_missing:psi.rst:36-38;rows_orphan:psi.rst:1-188 rev=dde7cff904234eca0cd58357135188a25a67e3da

swap / mut-quote-dup rc=1
C2=unmet pointers=47 rows=47 same=31 moved=16 changed=0 quotes_ok=47 spans_ok=47 sources=4 failed=rows_missing:psi.rst:36-38;rows_orphan:psi.rst:1-188 rev=dde7cff904234eca0cd58357135188a25a67e3da

swap / mut-anchor-set rc=0
C2=met pointers=47 rows=47 same=31 moved=16 changed=0 quotes_ok=47 spans_ok=47 sources=4 failed=none rev=dde7cff904234eca0cd58357135188a25a67e3da

committed-control / pristine-count-c2 rc=1
C2=unmet pointers=47 rows=0 same=0 moved=0 changed=0 quotes_ok=0 spans_ok=0 sources=0 failed=entry_absent rev=325f7e639916fcbc77fa2ec7475951a1b86bb1cb

committed-control / mut-span-small rc=1
C2=unmet pointers=47 rows=0 same=0 moved=0 changed=0 quotes_ok=0 spans_ok=0 sources=0 failed=entry_absent rev=325f7e639916fcbc77fa2ec7475951a1b86bb1cb

committed-control / mut-quote-dup rc=1
C2=unmet pointers=47 rows=0 same=0 moved=0 changed=0 quotes_ok=0 spans_ok=0 sources=0 failed=entry_absent rev=325f7e639916fcbc77fa2ec7475951a1b86bb1cb

committed-control / mut-anchor-set rc=1
C2=unmet pointers=47 rows=0 same=0 moved=0 changed=0 quotes_ok=0 spans_ok=0 sources=0 failed=entry_absent rev=325f7e639916fcbc77fa2ec7475951a1b86bb1cb

```

## Actual selftests at receipt floor

### pristine-count-c2 (rc=0)

```text
case good: ok=True want=True pass failed=[]
case quote-missing: ok=False want=False pass failed=['quote_missing:a.rst:5-7']
case row-missing: ok=False want=False pass failed=['rows_missing:a.rst:5-7', 'rows_ne_pointers']
case orphan: ok=False want=False pass failed=['rows_orphan:b.c:25', 'quote_words:b.c:25', 'rows_ne_pointers']
case small-span: ok=False want=False pass failed=['span_small:a.rst:5-7']
case dup-quote: ok=False want=False pass failed=['quote_dup:a.rst:9']
case not-mined: ok=False want=False pass failed=['rows_src:a.rst', 'rows_src:b.c', 'rows_src:c.txt', 'rows_src:d.h']
case usedby-miss: ok=False want=False pass failed=['rows_src:a.rst', 'rows_src:b.c', 'rows_src:c.txt', 'rows_src:d.h']
case tampered-copy: ok=False want=False pass failed=['copy_pin:a.rst', 'loc_bad:a.rst:5-7', 'loc_bad:a.rst:9', 'sources_floor']
case no-prov: ok=False want=False pass failed=['provenance']
C2_SELFTEST pass=10 fail=0
```

### mut-span-small (rc=0)

```text
case good: ok=True want=True pass failed=[]
case quote-missing: ok=False want=False pass failed=['quote_missing:a.rst:5-7']
case row-missing: ok=False want=False pass failed=['rows_missing:a.rst:5-7', 'rows_ne_pointers']
case orphan: ok=False want=False pass failed=['rows_orphan:b.c:25', 'quote_words:b.c:25', 'rows_ne_pointers']
case small-span: ok=False want=False pass failed=['quote_missing:a.rst:5-7']
case dup-quote: ok=False want=False pass failed=['quote_dup:a.rst:9']
case not-mined: ok=False want=False pass failed=['rows_src:a.rst', 'rows_src:b.c', 'rows_src:c.txt', 'rows_src:d.h']
case usedby-miss: ok=False want=False pass failed=['rows_src:a.rst', 'rows_src:b.c', 'rows_src:c.txt', 'rows_src:d.h']
case tampered-copy: ok=False want=False pass failed=['copy_pin:a.rst', 'loc_bad:a.rst:5-7', 'loc_bad:a.rst:9', 'sources_floor']
case no-prov: ok=False want=False pass failed=['provenance']
C2_SELFTEST pass=10 fail=0
```

### mut-quote-dup (rc=0)

```text
case good: ok=True want=True pass failed=[]
case quote-missing: ok=False want=False pass failed=['quote_missing:a.rst:5-7']
case row-missing: ok=False want=False pass failed=['rows_missing:a.rst:5-7', 'rows_ne_pointers']
case orphan: ok=False want=False pass failed=['rows_orphan:b.c:25', 'quote_words:b.c:25', 'rows_ne_pointers']
case small-span: ok=False want=False pass failed=['span_small:a.rst:5-7']
case dup-quote: ok=False want=False pass failed=['quote_missing:a.rst:9']
case not-mined: ok=False want=False pass failed=['rows_src:a.rst', 'rows_src:b.c', 'rows_src:c.txt', 'rows_src:d.h']
case usedby-miss: ok=False want=False pass failed=['rows_src:a.rst', 'rows_src:b.c', 'rows_src:c.txt', 'rows_src:d.h']
case tampered-copy: ok=False want=False pass failed=['copy_pin:a.rst', 'loc_bad:a.rst:5-7', 'loc_bad:a.rst:9', 'sources_floor']
case no-prov: ok=False want=False pass failed=['provenance']
C2_SELFTEST pass=10 fail=0
```

### mut-anchor-set (rc=0)

```text
case good: ok=True want=True pass failed=[]
case quote-missing: ok=False want=False pass failed=['quote_missing:a.rst:5-7']
case row-missing: ok=False want=False pass failed=['rows_lt_pointers', 'rows_ne_pointers']
case orphan: ok=False want=False pass failed=['quote_words:b.c:25', 'rows_ne_pointers']
case small-span: ok=False want=False pass failed=['span_small:a.rst:5-7']
case dup-quote: ok=False want=False pass failed=['quote_dup:a.rst:9']
case not-mined: ok=False want=False pass failed=['rows_src:a.rst', 'rows_src:b.c', 'rows_src:c.txt', 'rows_src:d.h']
case usedby-miss: ok=False want=False pass failed=['rows_src:a.rst', 'rows_src:b.c', 'rows_src:c.txt', 'rows_src:d.h']
case tampered-copy: ok=False want=False pass failed=['copy_pin:a.rst', 'loc_bad:a.rst:5-7', 'loc_bad:a.rst:9', 'sources_floor']
case no-prov: ok=False want=False pass failed=['provenance']
C2_SELFTEST pass=10 fail=0
```

## Restoration evidence

Before mutation / pristine sha256: `82d0fee6124685f8a50f93550f3665703a33dce644948958db642a77d5aec2d8`.

Mutation hashes:
- mut-span-small: `da59d6357909149d146a97bbf0aecd86824c2abdb2203eb307dc1d9c57f286a9`
- mut-quote-dup: `5e273eddb509b7c4cbc8dcd14397f55e4cdb89c5096f8db7eab72dc377451f7e`
- mut-anchor-set: `d9b8165d6bb7461347346fa799f9b6afd2ff74505aeab7a7052365eeb8a22b4c`

Restored each scratch mutant with the exact pristine bytes, then reran the identical selftest (default and floor 6), all four committed scratch fixtures, and the entering control. Lane file remained the pristine hash. Actual restored outputs:

```text
mut-span-small restored_sha256=82d0fee6124685f8a50f93550f3665703a33dce644948958db642a77d5aec2d8
selftest floor=40 rc=1 C2_SELFTEST pass=9 fail=1
selftest floor=6 rc=0 C2_SELFTEST pass=10 fail=0
good rc=0 C2=met pointers=47 rows=47 same=31 moved=16 changed=0 quotes_ok=47 spans_ok=47 sources=4 failed=none rev=56bc371454cbf0ffc1c45187b55764bcaa8f4670
smallspan rc=1 C2=unmet pointers=47 rows=47 same=31 moved=15 changed=0 quotes_ok=46 spans_ok=46 sources=4 failed=span_small:psi.c:1268 rev=b3d63d653b7c4181f04043d65e556760c3b3bb42
dup rc=1 C2=unmet pointers=47 rows=47 same=30 moved=16 changed=0 quotes_ok=46 spans_ok=46 sources=4 failed=quote_dup:psi.c:1284-1288 rev=1c079f88d0c0afcd6ac4bc209939a7e55e2f7f59
swap rc=1 C2=unmet pointers=47 rows=47 same=31 moved=16 changed=0 quotes_ok=47 spans_ok=47 sources=4 failed=rows_missing:psi.rst:36-38;rows_orphan:psi.rst:1-188 rev=dde7cff904234eca0cd58357135188a25a67e3da
control rc=1 C2=unmet pointers=47 rows=0 same=0 moved=0 changed=0 quotes_ok=0 spans_ok=0 sources=0 failed=entry_absent rev=325f7e639916fcbc77fa2ec7475951a1b86bb1cb
mut-quote-dup restored_sha256=82d0fee6124685f8a50f93550f3665703a33dce644948958db642a77d5aec2d8
selftest floor=40 rc=1 C2_SELFTEST pass=9 fail=1
selftest floor=6 rc=0 C2_SELFTEST pass=10 fail=0
good rc=0 C2=met pointers=47 rows=47 same=31 moved=16 changed=0 quotes_ok=47 spans_ok=47 sources=4 failed=none rev=56bc371454cbf0ffc1c45187b55764bcaa8f4670
smallspan rc=1 C2=unmet pointers=47 rows=47 same=31 moved=15 changed=0 quotes_ok=46 spans_ok=46 sources=4 failed=span_small:psi.c:1268 rev=b3d63d653b7c4181f04043d65e556760c3b3bb42
dup rc=1 C2=unmet pointers=47 rows=47 same=30 moved=16 changed=0 quotes_ok=46 spans_ok=46 sources=4 failed=quote_dup:psi.c:1284-1288 rev=1c079f88d0c0afcd6ac4bc209939a7e55e2f7f59
swap rc=1 C2=unmet pointers=47 rows=47 same=31 moved=16 changed=0 quotes_ok=47 spans_ok=47 sources=4 failed=rows_missing:psi.rst:36-38;rows_orphan:psi.rst:1-188 rev=dde7cff904234eca0cd58357135188a25a67e3da
control rc=1 C2=unmet pointers=47 rows=0 same=0 moved=0 changed=0 quotes_ok=0 spans_ok=0 sources=0 failed=entry_absent rev=325f7e639916fcbc77fa2ec7475951a1b86bb1cb
mut-anchor-set restored_sha256=82d0fee6124685f8a50f93550f3665703a33dce644948958db642a77d5aec2d8
selftest floor=40 rc=1 C2_SELFTEST pass=9 fail=1
selftest floor=6 rc=0 C2_SELFTEST pass=10 fail=0
good rc=0 C2=met pointers=47 rows=47 same=31 moved=16 changed=0 quotes_ok=47 spans_ok=47 sources=4 failed=none rev=56bc371454cbf0ffc1c45187b55764bcaa8f4670
smallspan rc=1 C2=unmet pointers=47 rows=47 same=31 moved=15 changed=0 quotes_ok=46 spans_ok=46 sources=4 failed=span_small:psi.c:1268 rev=b3d63d653b7c4181f04043d65e556760c3b3bb42
dup rc=1 C2=unmet pointers=47 rows=47 same=30 moved=16 changed=0 quotes_ok=46 spans_ok=46 sources=4 failed=quote_dup:psi.c:1284-1288 rev=1c079f88d0c0afcd6ac4bc209939a7e55e2f7f59
swap rc=1 C2=unmet pointers=47 rows=47 same=31 moved=16 changed=0 quotes_ok=47 spans_ok=47 sources=4 failed=rows_missing:psi.rst:36-38;rows_orphan:psi.rst:1-188 rev=dde7cff904234eca0cd58357135188a25a67e3da
control rc=1 C2=unmet pointers=47 rows=0 same=0 moved=0 changed=0 quotes_ok=0 spans_ok=0 sources=0 failed=entry_absent rev=325f7e639916fcbc77fa2ec7475951a1b86bb1cb
```

All receipts were copied into this report before scratch cleanup. Production/registry/VCS state unchanged by this seat; only this report survives. No remediation or service/config changes.

## Reproduction appendix: scratch fixture builder used

This code is a receipt, not a proposed production change. It assumes S/copies contains the six files extracted with `git -C <lane> show 7370a731:corpus/evidence/sources-r61/<file>` and S/pristine-count-c2.py is the frozen counter. Its scratch paths are disposable.

```python
#!/usr/bin/env python3
"""Scratch-only fixture builder for Mo61MutC2a (C2 mutant drive).

Builds throwaway git fixture repos at explicit scratch paths from the committed
7370a731 bytes (system-pressure-r24.md + pinned v7.3 copies), with a synthetic
ledger + synthetic SOURCES.md rows. Never touches the lane or fleet.
"""
import importlib.util
import json
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
SCR = "/fast/scratch/hyaku/mori-r61/Mo61MutC2a"
COUNTER = f"{SCR}/pristine-count-c2.py"
spec = importlib.util.spec_from_file_location("c2p", COUNTER)
c2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c2)

FX = f"{SCR}/fx"
os.makedirs(FX, exist_ok=True)
WORD = re.compile(r"\S+")

src_text = subprocess.run(
    ["git", "-C", LANE, "show", "7370a731:corpus/knowledge/system-pressure-r24.md"],
    capture_output=True, check=True).stdout.decode("utf-8", "replace")
pointers = c2.enumerate_pointers(src_text)
copies_bytes = {f: open(f"{SCR}/copies/{f}", "rb").read() for f in c2.FILES}
copies_txt = {f: b.decode("utf-8", "replace") for f, b in copies_bytes.items()}


def candidates(lines):
    out = []
    for ln in lines:
        toks = list(WORD.finditer(ln))
        for a in range(len(toks)):
            for b in range(a + 5, min(a + 26, len(toks)) + 1):
                s = ln[toks[a].start():toks[b - 1].end()]
                if ("`" in s or "|" in s):
                    continue
                if 5 <= len(s.split()) <= 25 and len(set(s.encode())) >= 8:
                    out.append(s)
    return out


def base_rows():
    """Good ledger: one row per pointer; same if a quote fits its span, else moved."""
    used, rows = set(), []
    for p in pointers:
        fn, lo, hi = c2.span_of(p)
        hi = max(hi, lo)
        lines = copies_txt[fn].splitlines()
        q = next((c for c in candidates(lines[lo - 1:hi]) if c not in used), None)
        if q is not None:
            used.add(q)
            rows.append((p, "same", "-", q))
            continue
        found = None
        for f in c2.FILES:
            for i, ln in enumerate(copies_txt[f].splitlines(), 1):
                for c in candidates([ln]):
                    if c not in used:
                        found = (f"{f}:{i}", c)
                        break
                if found:
                    break
            if found:
                break
        assert found, p
        used.add(found[1])
        rows.append((p, "moved", found[0], found[1]))
    return rows


HEAD = ("source: S090-S095, S145 (Linux v7.3 pinned copies, corpus/evidence/sources-r61)\n"
        "verified-at: 2026-10-30 (fixture, Mo61MutC2a scratch)\n"
        "recheck: python3 -I .ufo/waves/round-61/count-c2.py <rev>\n\n")


def render(rows):
    body = ["| anchor | status | loc | quote |", "|---|---|---|---|"]
    for a, s, l, q in rows:
        body.append(f"| {a} | {s} | {l} | `{q}` |")
    return HEAD + "\n".join(body) + "\n"


def registry():
    head = ("| id | source | kind | tier | scope | anchor | teaches | status"
            " | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n")
    rows = []
    for i, f in enumerate(c2.FILES, 1):
        rows.append(f"| S9{i:02d} | fixture copy corpus/evidence/sources-r61/{f} | code | A | psi"
                    f" | anchor | teaches | mined | 2026-10-30 | on-release"
                    f" | corpus/knowledge/psi-v73-recheck-r61.md |")
    return head + "\n".join(rows) + "\n"


def build(name, rows):
    d = os.path.join(FX, name)
    subprocess.run(["rm", "-rf", d], check=True)
    os.makedirs(d)
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True, check=True).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(d), (top, d)
    os.makedirs(f"{d}/corpus/knowledge", exist_ok=True)
    os.makedirs(f"{d}/corpus/evidence/sources-r61", exist_ok=True)
    open(f"{d}/corpus/knowledge/system-pressure-r24.md", "w", encoding="utf-8").write(src_text)
    for f, b in copies_bytes.items():
        open(f"{d}/corpus/evidence/sources-r61/{f}", "wb").write(b)
    open(f"{d}/corpus/SOURCES.md", "w", encoding="utf-8").write(registry())
    open(f"{d}/corpus/knowledge/psi-v73-recheck-r61.md", "w", encoding="utf-8").write(render(rows))
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "-c", "user.name=t", "-c", "user.email=t@t",
                    "commit", "-qm", f"fixture {name}"], check=True)
    rev = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"], capture_output=True,
                         text=True, check=True).stdout.strip()
    return d, rev


if __name__ == "__main__":
    base = base_rows()
    rows_by_anchor = {r[0]: r for r in base}
    fixtures = {}

    fixtures["good"] = base

    # H-smallspan: moved row whose quote is a 5-word, 5-distinct-byte span from cgroup-v2.rst:596
    lowb = "~~~~~~~~~~~~~ - C0 - C00"
    assert "~~~~~~~~~~~~~ - C0 - C00" in copies_txt["cgroup-v2.rst"].splitlines()[595]
    fixtures["smallspan"] = [
        (a, "moved", "cgroup-v2.rst:596", lowb) if a == "psi.c:1268" else r
        for a, _s, _l, _q in [(x[0], x[1], x[2], x[3]) for x in base]
        for r in [(a, _s, _l, _q)]
    ]
    fixtures["smallspan"] = [("psi.c:1268", "moved", "cgroup-v2.rst:596", lowb) if r[0] == "psi.c:1268"
                             else r for r in base]

    # H-dup: give psi.c:1282-1288 the same quote as psi.c:1284-1288 (both spans contain it)
    q_inner = rows_by_anchor["psi.c:1284-1288"][3]
    assert q_inner in "\n".join(copies_txt["psi.c"].splitlines()[1281:1288])
    fixtures["dup"] = [("psi.c:1282-1288", "same", "-", q_inner) if r[0] == "psi.c:1282-1288"
                       else r for r in base]

    # H-swap: equal row count, one pointer missing and one orphan anchor added
    orphan_anchor = "psi.rst:1-188"
    orphan_q = next(c for c in candidates(copies_txt["psi.rst"].splitlines())
                    if c not in {r[3] for r in base})
    fixtures["swap"] = [(orphan_anchor, "same", "-", orphan_q) if r[0] == "psi.rst:36-38"
                        else r for r in base]

    # Sanity: orphan quote is located in its wide anchor range.
    assert orphan_q in copies_txt["psi.rst"]

    out = {}
    for name, rows in fixtures.items():
        d, rev = build(name, rows)
        out[name] = {"dir": d, "rev": rev, "rows": len(rows)}
        print(f"{name}\t{d}\t{rev}\trows={len(rows)}")
    json.dump(out, open(f"{SCR}/fixtures.json", "w"), indent=2)

```

## Self-evaluation

Accuracy 4: observed receipts, hashes, baseline failure and reason-string distinction retained; fixture upstream semantics are intentionally not asserted. Completeness 4: all three probes and restored replay done; frozen lane has no met ledger state. Clarity 4: separates default-red, frozen-survival and new-witness kills. Actionability 4: exact edits, commands, outputs and builder included. Conciseness 3: full receipts/builder retained to survive required cleanup. Overall 3.8. Improvement applied: preserved exact receipts rather than treating the red baseline as a kill. User agreement: expected on scope/evidence; integration remains L1's decision.
