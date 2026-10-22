Seat: `MoriR24.MineMistake` (scribe/drafter, leaf — no subagents dispatched).
Lane: `mori-shokunin`, repo `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Date: 2026-10-22. Round: 24 (attempt 2), wave 1.
Assignment: mine one real mistake from round 23 or earlier into the draft `## Mistakes`
section of `corpus/lessons/round-24.md`. **Draft only — the L1 (MoriR24) integrates.**

## Sources read

- `corpus/lessons/round-23-verifier-spotcheck.md` (full).
- `corpus/lessons/round-23.md` (full).
- `SCORECARD.md` from line 1413 (the round-23 declaration, measured disposition and
  measured-withdrawal-revision sections) at committed tip
  `c725aa37aa3c9ec4f34e3c2abc8ca1b616c7c130`.
- `corpus/QUALITY.md`, `corpus/lessons/round-12.md` (M18), `corpus/lessons/round-22.md`,
  the committed round-23 evidence JSONs, and the fleet/sibling records of the same
  class (cited below).

## The mined mistake

**Class: record-side lexical boundary loss — a label and its measured value fused into
one token in committed prose.** The label and the value are written with no separator:
`exit0`, `operability7`, `original25/26→26/26`, `remains95raw/86allowlisted/…`,
`90scanner`, `permission11/12red`.

**Severity, stated honestly: this is writer degradation and auditability loss, not a
wrong number.** I re-derived every numeric claim of the round-23 SCORECARD section that
has a committed receipt and **all of them match** (evidence table below). The defect is
that the record is hard to re-check mechanically, not that it states a false value. The
drafted row says exactly that, so it cannot be read as a claim-integrity accusation it
cannot support.

### Evidence pointers (committed bytes at `c725aa37`)

| Path:line | Text as committed |
|---|---|
| `SCORECARD.md:1423` | `sealed independent fixture cases capability_absent → all match; real host exit0 \`QUOTA_DISABLED\` as frozen` |
| `SCORECARD.md:1425` | `Targets, not results. Other scores held operability7/depth5/freshness5/adjacency6.` |
| `SCORECARD.md:1434` | `C1 calibration \| original25/26→26/26; alias-bearing outputs8/18→0/18; schema-v2 outputs0/18→18/18` |
| `SCORECARD.md:1435` | `absent at1bfe708a; strict29/30 atf3dc07c0 (26/27 primary+3/3 supplemental);274/274 supplementary output predicates` |
| `SCORECARD.md:1445-1446` | `The real accounting remains95raw/86allowlisted/5non-author/` / `90scanner/4in-scope-unallowlisted/9raw-complement, red, privacy_clearance=false.` |
| `SCORECARD.md:1447` | `R01–R26 are26 requirement IDs over18 cached invocations, not26 independent detections.` |
| `SCORECARD.md:1452` | `Operability7/depth5/freshness5/adjacency6 held. Original permission11/12red,` |
| `SCORECARD.md:1472` | `Full driver exit1 remains RED:` |
| `SCORECARD.md:1474-1475` | `Current C2 buckets are30capability_absent/0pass … unmet0 is an absence bucket, NOT a pass.` |
| `SCORECARD.md:1482` | `actually exits1 RETENTION_FINDINGS, metric4, raw95/allowlisted86/non-author5.` |

### Counting command and output

Command (narrow, grep over the committed file, as requested):

```
git -C /home/vgpnk/Projects/shokunin/mori-shokunin show c725aa37:SCORECARD.md \
  | grep -cE 'exit[01]|exits1|[Oo]perability[0-9]|depth[0-9]|freshness[0-9]|adjacency[0-9]|original[0-9]|[0-9]+raw|[0-9]+allowlisted|[0-9]+scanner|[0-9]+pass|[0-9]+capability|[0-9]+non|[0-9]+red'
```

Output: `34` (lines in the whole committed file).
Same grep restricted to the round-23 section (`sed -n '1413,1493p'`): `11`.

Command (per-token, python regex over the same committed bytes; the check script is in
the "Fix" section below):

```
git -C /home/vgpnk/Projects/shokunin/mori-shokunin show c725aa37:SCORECARD.md \
  | python3 -I /fast/scratch/hyaku/mori-r24-a2/mori-prose-fused.py --file /dev/stdin
```

Output (tail): `PROSE_FUSED: FAIL hits=256`, exit `1`.
Round-23 section only (`sed -n '1413,1493p'` piped the same way):
`PROSE_FUSED: FAIL hits=53`, exit `1`.
Of the 53, 40 have an all-lowercase word side (`exit0`, `operability7`, `original25`,
`raw95`, `90scanner`, `permission11`, …); the other 13 are identifier-shaped
(`Round23`, `MadoR22`, `QUALITY70`, `CriticContractC2`, …) and would be allowlisted by
a landed version. The class therefore survives identifier filtering.

### The class is a drift, not a typo

Per-section counts of fused tokens in the same committed file (checker output, one
line per section):

| Section | hits | Section | hits |
|---|---|---|---|
| Round 5 | 1 | Round 16 | 24 |
| Round 7 | 1 | Round 17 | 37 |
| Round 8 | 1 | Round 19 | 26 |
| Round 10 | 1 | Round 20 | 1 |
| Round 13 | 3 | Round21 | 57 |
| Round 14 | 3 | Round22 | 39 |
| Round 15 | 9 | Round23 | 53 |

And the spaced form disappears exactly where the fused form appears. Counting
`exit 0` / `exit 1` (spaced) and `exit0` / `exit1` / `exits1` (fused) per section:
rounds 2–14 write the spaced form (13 sections, 0 fused hits, e.g. Round 11 has
2 spaced and 0 fused); from Round 15 onward the spaced count is **0** and only fused
forms remain (Round 15: 2 fused, Round 16: 5, Round 19: 1, Round21: 2, Round22: 1,
Round 23: 4). This is the drift sentinel's degraded-writer signal, and round 23 is the
worst-affected recent section.

The class is lane-wide, not confined to the SCORECARD. Checker over committed bytes at
`c725aa37` (all default surfaces, `--all-surfaces`): `PROSE_FUSED: FAIL hits=682`,
exit 1. The nine default surfaces are `SCORECARD.md`, `PROVINCE.md`, `LOG.md`,
`SKILL.md`, `README.md`, `corpus/QUALITY.md`, `corpus/README.md`, `corpus/lessons/**`
and `corpus/knowledge/**`. Per file: `LOG.md` 326 tokens, `corpus/lessons/round-23.md` 72,
`corpus/lessons/round-22.md` 39, `SKILL.md` 40, `corpus/README.md` 30,
`PROVINCE.md` 19, `corpus/QUALITY.md` 11, `corpus/lessons/round-23-verifier-spotcheck.md` 4,
`README.md` 0.

### What it costs (concrete)

Grep over the round-23 section of the committed file:

| Spaced phrase | hits | Fused form | hits |
|---|---|---|---|
| `exit 0` | 0 | `exit0` | 2 |
| `exit 1` | 0 | `exit1` / `exits1` | 1 / 1 |
| `operability 7` | 0 | `operability7` | 1 |
| `depth 5` | 0 | `depth5` | 2 |
| `90 scanner` | 0 | `90scanner` | 1 |
| `raw 95` | 0 | `raw95` | 1 |

A boundary-aware re-check finds nothing: `\bexit\b` cannot match `exit0`, exactly the
round-12 M18 failure mode (`bare \`cursor\` matched 3 files; \`\bcursor\b\` matched 0`),
with the missing boundary on the **record** side instead of the regex side. The parent
(hyaku) re-verifies a lane by grepping its records; the round-23 record no longer
carries the canonical phrases, so "the driver still exits 1" cannot be re-found by
string match in the surface the parent cites.

### What it does not cost (checked — the numbers are right)

| SCORECARD round-23 text | Committed receipt | Verdict |
|---|---|---|
| `95raw/86allowlisted/5non-author/4in-scope-unallowlisted` | `.ufo/waves/round-23/evidence/retention-floor-final.json` (rev `4994c0df`): `hits` 95, `allowlisted_hits` 86, `non_author` 5, `unallowlisted_hits` 4, `metric` 4 | matches |
| `90scanner` | 86 + 4 = 90, i.e. `hits` 95 − `non_author` 5 | matches (arithmetic) |
| `9raw-complement` | `.ufo/waves/round-23/evidence/count-lineage.json` → `debt.raw_not_allowlisted: 9` | matches |
| `selftest4/4` | `evidence/measure-withdrawal/c1-selftest-measured.json` → `passed 4`, `total 4` | matches |
| `alias-bearing outputs8/18→0/18` | `c1-before-observed.json`: `parsed_runs 18`, `misleading_alias_runs 8`; `c1-after-observed.json`: `misleading_alias_runs 0` | matches |
| `schema-v2 outputs0/18→18/18` | `c1-before-observed.json`: `schema_v2_runs 0`; `c1-after-observed.json`: `schema_v2_runs 18`, `parsed_runs 18`; `summary.json` `checks[21]` `C20.c1_schema_v2_after` `schema_v2_runs 18` | matches |
| `same source4599ee1a` | `c1-after-observed.json` `tool_sha256` `4599ee1a…` | matches |
| `mode100755` | `git ls-tree 0d8f2d50eb85e0d4349b1045f01c04e57318cc1b tools/mori-retention-reconcile.py` → `100755 blob 78c676e…` | matches |
| `strict29/30 (26/27 primary+3/3 supplemental)` | `count-lineage.json`: `frozen_cases 30`, `original_derived 27`, `source_review_discovery 3`, `original_match 29` | matches |
| `274/274 supplementary` | `count-lineage.json`: `supplementary_output_checks 274` | matches |

So the mined mistake is: **the round-23 record is not wrong, but it is no longer
mechanically re-checkable.** That distinction is the lesson.

### Captured-by

- **Nothing in this lane.** The nearest existing criterion is Q19
  (`corpus/QUALITY.md:41-42`): *"A sweep's nonzero hits are inspected before the count
  is cited; regexes use word boundaries. ← lessons/round-12.md#M18"*. Q19 bounds the
  **checker** side of exactly this boundary defect; no criterion covers the **record**
  side. Q61 (`corpus/QUALITY.md:212-215`) is about transport rendering versus source
  bytes and does not apply: the fused tokens are in the committed source bytes.
- The only prose capture is the seat instruction *"Plain English, no run-together words"*
  in the wave dispatch text — prose with no mechanism.
- The same class was caught by hand elsewhere in this session, which is why the L1
  saw it: tabi `.ufo/waves/round-22/w1/Semantic12.md:26,156`; kama
  `.ufo/waves/round-24/falsify/advice/DocQuality.md:658`; tameshi
  `.ufo/waves/round-17/w2/CR49.md:100`; and the parent routed it as a defect class in
  fleet `.ufo/waves/hyaku/PHASE3.md:132` ("Routed defects D1–D5 include run-together
  words").

## Drafted row for `corpus/lessons/round-24.md` → `## Mistakes`

Table shape follows `corpus/lessons/round-22.md` and `corpus/lessons/round-23.md`:
`| ID | Class | Evidence pointer | Captured-by | Fix / fail-capability |`. The row ID
below is provisional (`M1` is free in a new round-24 file; the L1 renumbers if the file
already carries rows).

> **M1** | record-side lexical boundary loss: a label and its measured value fused into
> one token (`exit0`, `operability7`, `original25/26→26/26`, `remains95raw/…`,
> `90scanner`, `permission11/12red`) | `SCORECARD.md` at `c725aa37`: `:1423` `exit0`,
> `:1425` `operability7/depth5/freshness5/adjacency6`, `:1434`
> `original25/26→26/26`, `:1445-1446` `remains95raw/86allowlisted/5non-author/90scanner/…`,
> `:1447` `are26 … over18 … not26`, `:1452` `permission11/12red`, `:1472` `exit1`,
> `:1482` `exits1`; per-section counts 1/1/1/1/3/3/9/24/37/26/1/57/39/**53** for
> r5,r7,r8,r10,r13,r14,r15,r16,r17,r19,r20,r21,r22,r23 and 256 tokens in the whole
> file at `c725aa37` (682 across the nine parent-facing surfaces `SCORECARD.md`,
> `PROVINCE.md`, `LOG.md`, `SKILL.md`, `README.md`, `corpus/QUALITY.md`,
> `corpus/README.md`, `corpus/lessons/**`, `corpus/knowledge/**`); over the round-23
> section the spaced forms `exit 0`, `exit 1`,
> `operability 7`, `depth 5`, `90 scanner`, `raw 95` have **0** hits each | none.
> Nearest existing criterion is Q19 (`corpus/QUALITY.md:41-42`, lessons/round-12.md#M18:
> "bare `cursor` matched 3 files; `\bcursor\b` matched 0"), which bounds the *regex*
> side of the same boundary defect; no criterion and no lane tool covers the *record*
> side. The seat prose rule "Plain English, no run-together words" has no mechanism | A
> byte-level prose boundary check over the lane's parent-facing surfaces
> (`SCORECARD.md`, `PROVINCE.md`, `LOG.md`, `SKILL.md`, `README.md`, `corpus/**`) that
> flags a word/number join and exits 1 when it finds one, run as a **ratchet on added
> lines** since the round-24 tip (the same added-line shape the round-24 C1 R2
> predicate already uses), so the 256 legacy tokens in `SCORECARD.md` and 682 lane-wide
> stay visible as named debt and no round-23 byte is rewritten. **Fail-capability:**
> exit 1 with 53 hits on the committed round-23 section; exit 0 with 0 hits on the same
> text after a mechanical de-fusion; exit 1 with 1 hit on a single injected `exit1`.
> Add a `QUALITY.md` criterion line tagged `r24 prose-boundary` citing this row. Do not
> de-fuse the round-23 `SCORECARD.md` text in round 24: the parent has already read
> those bytes, and rewriting them is not this round's business. Landing a new tool is a
> new claim, so this row is a lesson for the next round, not a round-24 claim — only
> the L1 may declare it.

## Fix — the check, and its red/green demonstration

The check is a draft artifact. It lives in scratch (outside the lane repo) and is
reproduced here in full so the L1 can land it as `tools/mori-prose-check.py`:

```python
#!/usr/bin/env python3
"""Prose boundary check (draft for round 24): flags word/number joins in the
lane's parent-facing prose surfaces.

Reads committed bytes (git object) or a local file. Read-only; writes nothing.
Exit 1 when at least one fused token is found, 0 when none, 2 on usage/IO error.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys

WORD_NUM = re.compile(r"[A-Za-z]{3,}[0-9]+")
NUM_WORD = re.compile(r"[0-9]+[A-Za-z]{3,}")
HEX_RUN = re.compile(r"[0-9a-f]{8,}")
CODE_SPAN = re.compile(r"`[^`]*`")
URL = re.compile(r"https?://\S+")

DEFAULT_SURFACES = (
    "SCORECARD.md",
    "PROVINCE.md",
    "LOG.md",
    "SKILL.md",
    "README.md",
    "corpus/QUALITY.md",
    "corpus/README.md",
    "corpus/lessons",
    "corpus/knowledge",
)


def fused_tokens(text: str):
    """Return [(lineno, token)] for word/number joins in prose lines."""
    hits = []
    for lineno, line in enumerate(text.split("\n"), 1):
        prose = CODE_SPAN.sub(" ", line)
        prose = URL.sub(" ", prose)
        for tok in re.split(r"\s+", prose):
            if not tok:
                continue
            if HEX_RUN.search(tok):              # commit id or digest fragment
                continue
            if tok.lower().startswith("sha"):    # sha256 style
                continue
            for rx in (WORD_NUM, NUM_WORD):
                for m in rx.finditer(tok):
                    hits.append((lineno, m.group(0)))
    return hits


def git_show(repo: str, rev: str, path: str):
    out = subprocess.run(
        ["git", "-C", repo, "show", f"{rev}:{path}"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if out.returncode != 0:
        return None
    return out.stdout.decode("utf-8", "replace")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file")
    ap.add_argument("--repo")
    ap.add_argument("--rev")
    ap.add_argument("--surface", default="SCORECARD.md")
    ap.add_argument("--all-surfaces", action="store_true")
    ap.add_argument("--section-from", help="count only from this heading on")
    args = ap.parse_args()

    if not args.file and not (args.repo and args.rev):
        sys.stderr.write("usage: --file PATH | --repo PATH --rev REV\n")
        return 2

    total = 0
    if args.file:
        try:
            with open(args.file, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError as exc:
            sys.stderr.write(f"PROSE_FUSED_UNAVAILABLE: {exc}\n")
            return 2
        if args.section_from:
            idx = text.find(args.section_from)
            if idx < 0:
                sys.stderr.write("PROSE_FUSED_UNAVAILABLE: section not found\n")
                return 2
            text = text[idx:]
        hits = fused_tokens(text)
        for lineno, tok in hits:
            print(f"{args.file}:{lineno}: FUSED_TOKEN {tok}")
        total = len(hits)
        print(f"PROSE_FUSED: {'FAIL' if total else 'PASS'} hits={total}")
        return 1 if total else 0

    surfaces = DEFAULT_SURFACES if args.all_surfaces else (args.surface,)
    for surface in surfaces:
        text = git_show(args.repo, args.rev, surface)
        if text is None:
            continue
        if args.section_from:
            idx = text.find(args.section_from)
            if idx < 0:
                continue
            text = text[idx:]
        hits = fused_tokens(text)
        for lineno, tok in hits:
            print(f"{args.rev}:{surface}:{lineno}: FUSED_TOKEN {tok}")
        total += len(hits)
    print(f"PROSE_FUSED: {'FAIL' if total else 'PASS'} hits={total}")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### Exercised red / green (all runs read-only; scratch only)

```
$ cd /fast/scratch/hyaku/mori-r24-a2
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin show c725aa37:SCORECARD.md \
    | python3 -I mori-prose-fused.py --file /dev/stdin > whole.txt
$ echo $?                      # → 1
$ tail -1 whole.txt            # → PROSE_FUSED: FAIL hits=256

$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin show c725aa37:SCORECARD.md \
    | sed -n '1413,1493p' | python3 -I mori-prose-fused.py --file /dev/stdin > r23.txt
$ echo $?                      # → 1
$ tail -1 r23.txt              # → PROSE_FUSED: FAIL hits=53
$ head -6 r23.txt
  /dev/stdin:1: FUSED_TOKEN Round23
  /dev/stdin:3: FUSED_TOKEN MadoR22
  /dev/stdin:11: FUSED_TOKEN exit0
  /dev/stdin:13: FUSED_TOKEN operability7
  /dev/stdin:13: FUSED_TOKEN depth5
  /dev/stdin:13: FUSED_TOKEN freshness5
  (… 53 lines; absolute line numbers in the committed file: 1413, 1415, 1423, 1425×4,
   1430, 1434×4, 1435×3, 1444, 1445×4, 1446×2, 1447×3, 1452×6, 1465, 1470×3, 1472,
   1474×3, 1475×2, 1477×2, 1478×3, 1482×5, 1483×2)

$ python3 -I mori-prose-fused.py --file SCORECARD.c725aa37.defused.md
  PROSE_FUSED: PASS hits=0
$ echo $?                      # → 0

$ printf 'The driver exit1 remains RED.\n' > inject.txt
$ python3 -I mori-prose-fused.py --file inject.txt
  inject.txt:1: FUSED_TOKEN exit1
  PROSE_FUSED: FAIL hits=1
$ echo $?                      # → 1

$ python3 -I mori-prose-fused.py --repo /home/vgpnk/Projects/shokunin/mori-shokunin \
    --rev c725aa37 --all-surfaces | tail -1
  PROSE_FUSED: FAIL hits=682
$ echo ${PIPESTATUS[0]}        # → 1
```

`SCORECARD.c725aa37.defused.md` is a scratch copy of the committed bytes with a
mechanical space inserted at every flagged join (script: insert a space between an
alphabetic run of 3+ letters and an adjacent digit run, skipping tokens that contain an
8+ character hexadecimal run or start with `sha`). It exists only to show the check
discriminates; it is **not** a proposed rewrite of the committed file, and nothing was
written inside the lane repo except this report.

## Alternatives weighed, and why they are not mined

1. **The CaseEscapedSpace frozen rule versus its frozen expected row** (round-23
   lessons, "Frozen rule versus inconsistent expected topology"; evidence
   `frozen-contradiction.json`; spot-check "Frozen C2 contradiction and rejection").
   Stronger in substance: it cost the round its C2 claim. But it is already covered by
   an existing criterion and already handled correctly — Q55
   (`corpus/QUALITY.md:176-179`, "the frozen rule wins when they disagree … the
   executor reports the conflict") and round 23 reports the conflict, keeps the rule
   and the expected bytes, and preserves the red case. Round 24 additionally pins the
   frozen tree unchanged (C1 R1/R3). Re-mining it would duplicate a criterion and a
   correctly handled case.
2. **M13, the receipt filename overwriting the raw command wrapper**
   (`evidence/harness-receipt-overwrite.json`). Already a row in round 23's own mistakes
   table and already routed as round 24's R3 preservation guard. Duplicative.
3. **The "90 scanner" figure**, disputed in round 22 by
   `.ufo/waves/round-22/build/AttackR06.md:75` (91 under the policy-path-only
   definition). Not a round-23 mistake: it is round-22-era receipt metadata, it is
   arithmetically consistent with the round-23 receipt (86 + 4 = 90), and round 22
   already recorded the disagreement
   (`corpus/knowledge/retention-reconciliation-r22.md:25`). Not mined.

The L1's candidate therefore stands as the one mistake that is real, byte-checkable,
uncovered by any existing criterion or check in this lane, and closable with a check
that fails. Its severity is auditability, not correctness, and the drafted row says so.

## Bounds observed

- Only file created inside the lane repo: this report,
  `.ufo/waves/round-24/w1/MineMistake.md`. No production file, tool, corpus file or
  lesson file was edited.
- No `git add/commit/stash/checkout/reset/pull/push` and no mutating `jj` command in
  the lane repo. Read-only git only: `show`, `ls-tree`, `log`, `status`.
- Scratch artifacts (outside the repo): `/fast/scratch/hyaku/mori-r24-a2/` —
  `mori-prose-fused.py`, `SCORECARD.c725aa37.md`, `SCORECARD.c725aa37.defused.md`,
  `whole.txt`, `r23.txt`, `defused.txt`, `inject.txt`.
- Detection only: no writes to `/proc`, `/sys` or cgroup files, no PSI trigger
  registration, no service restart, no host configuration change.
- No tools installed or updated (none needed; `python3` and `git` already present).
- Unrun checks are not claimed as passing. The de-fusion discriminator is a scratch
  demonstration, not a proposed edit to committed bytes.

Report: .ufo/waves/round-24/w1/MineMistake.md
