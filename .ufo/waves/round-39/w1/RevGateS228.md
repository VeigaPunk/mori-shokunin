# RevGateS228 — S228 supersede verification (round 39, wave 1)

Scored tip `13bfba23b7ca063c76d3504a2ff6eb7b6a294932`; entering tip `13f3db7e5c7163e7ef300259ff597a42a79f81f1`.
Verdict: **4 of 5 target checks PASS; check 4 FAILS.**

| # | Check | Result |
|---|-------|--------|
| 1 | row opens `supersedes S226` | PASS |
| 2 | quote verbatim at `S228.src:657-659`, ≤25 words | PASS (24 words) |
| 3 | S228 landing descends from S226 landing | PASS |
| 4 | gate at `13bfba2` lists S226 in `superseded_as_of` | **FAIL** |
| 5 | S226 row at `13f3db7` still prints `:657-658` | PASS |

## Checks

### 1. Supersede cell — PASS
`corpus/SOURCES.md:234` (present at `13bfba2`), `teaches` cell (colmap from the gate's own parser, `tools/mori-sources-appendonly.py:parse_registry`):

```
S228 teaches: supersedes S226 — same sentence and teaching; the located qu
SUPERSEDES_RE match: S226
```

Literal cell text (field 8 of the row): `supersedes S226 — same sentence and teaching; the located quote runs to line 659 (the r38 closure routed the :657-658 correction; the anchor cell is immutable, so the fix rides this row).` The gate's regex `^supersedes\s+(S\d{3})\b` (line 69) matches it, so the row is registered as a superseder of S226.

### 2. Located quote — PASS
Quote extracted from the committed `anchor` cell at `13bfba2`, then searched in the committed blob `13bfba2:corpus/evidence/sources-r39/S228.src`:

```
anchor quote words: 24
range: 657 659
verbatim at range: True
verbatim at 657-658: False
quote tail: y are supported by the operating system)
```

Source lines: 657 `<dd><p>Return the canonical path of the specified filename, eliminating any symbolic`, 658 `links encountered in the path (if they are supported by the operating`, 659 `system). On Windows, this function will also resolve MS-DOS (also called 8.3)`. The quote is a strict substring of the raw joined lines (the trailing `.` of the sentence is excluded); it does **not** fit in 657-658, so the correction is substantive, not cosmetic.

### 3. Landing-commit ancestry — PASS
Landing commits found by pickaxe and confirmed by the addition hunks:

```
git log -S'| S228 |' -- corpus/SOURCES.md  -> f920eaf7dbe85372a20b6710f1f4848c74d06c47 (only)
git log -S'| S226 |' -- corpus/SOURCES.md  -> daa1d4d (only)
git show daa1d4d -- corpus/SOURCES.md | grep -c '^+| S226 |'  -> 1
git show f920eaf  -- corpus/SOURCES.md | grep -c '^+| S228 |'  -> 1
git merge-base --is-ancestor daa1d4d f920eaf7   -> exit 0
git merge-base --is-ancestor f920eaf7 daa1d4d   -> exit 1  (negative control)
git merge-base --is-ancestor daa1d4d 13bfba2    -> exit 0
git merge-base --is-ancestor f920eaf7 13bfba2   -> exit 0
```

`f920eaf` changes `corpus/SOURCES.md` by +4 lines and adds `corpus/evidence/sources-r39/S227.src`, `S228.src`.

### 4. Gate `superseded_as_of` at the scored tip — FAIL
```
$ python3 tools/mori-sources-appendonly.py 13bfba23b7ca063c76d3504a2ff6eb7b6a294932
exit=1
supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] stale_supersede=[]
appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[...same 18...] round_changed=[]
changed S069 superseded_by=S226
```

S226 appears nowhere in `superseded_as_of`, `stale_supersede`, `superseded`, `ids`, or any `changed` line. Direct call into `analyze()` at the same rev:

```
sup_map S226 -> S228
S226 in ids: False
ids count: 18
S226 in superseded_as_of: False
S226 in stale_supersede: False
```

The supersede link **is** registered (`superseded_by["S226"] == "S228"`, built at `tools/mori-sources-appendonly.py:299-301,338-342`), but it is never dispositioned. The gate output at the scored tip is byte-identical to the output at the entering tip (`diff /tmp/gate-enter.out /tmp/gate-tip.out` → exit 0), and the same holds at the S228 landing commit `f920eaf`; the round's own `evidence/c9-after-lane.txt` records exactly this ("diff tip (v2 f920eaf7 vs r38 gate-after.txt): identical, exit 0"), whose as_of line has the same 18 ids.

Root cause is structural, not a bad run:
- `:343` `superseded = sorted(cid for cid in ids if cid in sup_map)` — the disposition universe is `ids`.
- `:334` `ids` = rows whose **immutable cells** differ from their first appearance. S226's row is byte-identical at every commit from `daa1d4d` to the scored tip (per-commit `grep '^| S226 |' | sha256sum` yields one live hash, `bfb985ad…`; pre-add commits hash the empty string), so `S226 ∉ ids`.
- `:344-347` `last_edit` is populated only for changed rows, and `:350-357` iterates `superseded`; S226 is never reached.

Consequence: `contract.md:148`'s declared after-state `superseded_as_of=[18 ids + S226 once S228 lands]` is unachievable under the shipped v2 predicate as written. P-C9 itself says "descendant … of the commit of the id's last immutable-cell edit" — S226 has no such edit commit, so the predicate has no subject for S226; a superseding row can only be dispositioned for an id that already needed no superseding row. S228 therefore discharges the `:657-658` → `:657-659` correction only at the documentation layer (SOURCES row, `corpus/lessons/round-39.md:8,12,19`); the gate never shows it. C3's "plus S226 once S228 lands" observable is refuted by the shipped instrument and by the round's own receipt.

### 5. S226 suffix at the entering tip — PASS
```
$ git show 13f3db7e5c7163e7ef300259ff597a42a79f81f1:corpus/SOURCES.md | grep '| S226 |'
| S226 | Python `os.path.realpath` documentation — … | docs | A | … | `os.path.realpath` paragraph "Return the canonical path of the specified filename, eliminating any symbolic links encountered in the path (if they are supported by the operating system)":657-658; page fetched 2026-10-23 | supersedes S069 — … | mined | 2026-10-23 | on-release | corpus/knowledge/containment-timed-supersede-r38.md |
```
Identical at `13bfba2` (anchor cell untouched — the immutable-cell rule held).

## Supporting observations
- `corpus/evidence/sources-r39/S228.src` vs `corpus/evidence/sources-r38/S226.src`: a single differing line, 1019 (`Last updated on Oct 23, 2026 (20:21 UTC).` → `Oct 24, 2026 (00:13 UTC).`). The "re-open; differs only in the docs build footer" statement is accurate.
- S228 row absent at `13f3db7` (`count=0`), present at `f920eaf` and `13bfba2` (`count=1`).
- Working tree bytes for `tools/mori-sources-appendonly.py`, `corpus/SOURCES.md`, `corpus/evidence/sources-r39/` equal `13bfba2` (`git diff --stat` empty). HEAD is two commits past the scored tip (`5561819`, `20260b0`, dispatch records), and `git rev-list --count 13bfba2..HEAD -- corpus/SOURCES.md` = 0, so in-place runs are equivalent to the scored tip; all gate runs above pass the revision explicitly.
- Gate exit 1 at the tip is the gate's normal nonzero-on-changes behavior (18 changed ids), not a claim failure.

## Residual risk and verification gaps
- **No `lsp` device in this seat's tool inventory** (available: read/bash/edit/eval/glob/grep/task/wait/web_search/write), so server-based `references`/`definition`/`diagnostics` were impossible. Caller/definition checks were done with the gate's own parser and committed blobs (semantic extraction), not grep over source alone. Recorded as unavailability.
- Contract/receipt mismatch outside this target: `contract.md:147` declares `MORI_SOURCES_APPENDONLY_SELFTEST pass=11 fail=0`, while `evidence/gate-selftest-after.txt` prints `pass=12 fail=0` (and the round context repeats 12). Not adjudicated here (C3 seat's scope); the frozen contract's after-state text is stale on that number.
- Severity: **HIGH** for check 4 (a declared, receipt-checkable after-state is false and structurally unreachable under the frozen predicate); **LOW** for the pass=11/12 text mismatch.
- No tools installed or upgraded; no lane file touched other than this report.
