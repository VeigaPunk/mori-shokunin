# Mo92K01Trio — round 92 w1, C1 provenance trio on ten corpus/knowledge entries

Seat: Mo92K01Trio (leaf, no subagents, no model pass). Entering revision `f63d1ab030d4179576e494342f48ef8718e497a5`.
Scratch: clone `<scratch>/repo` at f63d1ab0, `rev-parse --show-toplevel` verified before any change; scratch removed at yield.
Patch: `.ufo/waves/round-92/w1/patches/Mo92K01Trio.patch` (213 lines, 10 files, all under `corpus/knowledge/`; `git diff f63d1ab0 -- corpus/knowledge/`).
Lane tree, fleet root, siblings: not written. Only `git log --diff-filter=A` (read) ran against the lane.

## Result

All ten files now carry `source:`, `verified-at:` and `recheck:` each at least once within their first 12 lines (per-file check in §2, rc 0). Two files gained a full new trio (audit-r11, progressing-weak-r2), one gained only a `recheck:` (drift-pin-r10), and seven gained no new line: each already had its key(s) in the body beyond line 12, and those lines were moved verbatim into the head. Body text is unchanged: the line multiset of each file equals the entering file, except the added lines listed in §2 and one blank line removed in each of lane-silence-r2 and drift-pin-r10 (formatting only).

**Deviation the L1 must decide (see §3):** a key already present in a file was moved, not duplicated, because the brief forbids duplicates and forbids body edits. For the eight files that had a pre-existing `verified-at:`, that value is an observation date or window, not the admission-commit form the brief gives for new lines.

## 1. Per-file table

Line numbers in the "body line" column are the **entering** (f63d1ab0) file's line numbers. "now" gives the post-edit line.

| file | keys added (new lines) | source value | verified-at value | recheck value | body line that gave the recheck |
|---|---|---|---|---|---|
| audit-r11.md | source, verified-at, recheck (lines 2–4) | `tools/mori-census.sh; tools/mori-silence-cases.sh; corpus/evidence/baseline-r10-20261015T2231Z.json (hashes at audit-r11.md:50-52)` | `e4855e8c (2026-10-15), admission commit` | `bash tools/mori-census.sh --selftest; bash tools/mori-silence-cases.sh (audit-r11.md:118-121)` | 118 (`bash tools/mori-silence-cases.sh`), 120 (`bash tools/mori-census.sh --selftest`), §3 table |
| progressing-weak-r2.md | source, verified-at, recheck (lines 2–4) | `PROTOCOL.md:157-168 (fleet tree); corpus/knowledge/lane-silence-r2.md; corpus/knowledge/silence-grading-r2.md:224-229` | `3da84149 (2026-10-15), admission commit` | `progressing-weak-r2.md:48-53` — awk-extract the `###CHECK-BEGIN…###CHECK-END` block, run with bash; expect `MORI_AUTHORSHIP_CHECK: matched=10 total=10` | 48–53 (awk at 49, `bash` at 52) |
| drift-pin-r10.md | recheck (line 3). `verified-at` moved, not added (see §3) | existing `source:` line (orig 3, now line 5) | existing body line 20 moved to line 2: `2026-10-15T22:06:01–22:17Z, two arms, one per revision:` | `MORI_SHOKUNIN_ROOT=<fleet root> bash tools/mori-census.sh --drift corpus/evidence/baseline-r10-20261015T2231Z.json` | Erratum 297–298. The body records this command reads red (exit 1) on 2026-10-19; the trio line names the command, it does not assert a pass |
| counter-semantics-r78.md | none new; verified-at (15–17) and recheck (18) moved to lines 1–4 | existing `source: S593 …` (now line 5) | existing `2026-11-02 (round 78; …)` | existing `180d` (no command in body) | n/a — see §3 |
| counter-win-r77.md | none new; verified-at (16–22) moved to lines 1–7, recheck (23) to line 8 | existing `source: S592 …` (now line 9) | existing `2026-11-02 (round 77; …)` | existing `180d` (no command) | n/a — see §3 |
| rotation-receipt-grammar-r76.md | none new; verified-at (15–18) to lines 1–4, recheck (19) to line 5 | existing `source: S591 …` (now line 6) | existing `2026-11-02 (round 76; …)` | existing `180d` (no command) | n/a — see §3 |
| rotation-schedule-r74.md | none new; recheck (17–18) to lines 1–2 | existing `source: S589 …` (now line 3) | existing `2026-11-02 (round 74; …)` (orig line 10, still in head at 12) | existing `180d, or when a re-fetch of the page changes its sha256 against the pinned copy` (no command) | n/a — see §3 |
| execution-binding-r89.md | none new; recheck (15) moved to line 2 | existing `source: S611 …` (now line 4) | existing `2026-11-04 (round 89; …)` (now line 11) | existing `on-release` (no command) | n/a — see §3 |
| kernel-v7.3-recheck-r53.md | none new; verified-at (12) and recheck (13) moved to lines 2–3 | existing `source: S502 …` (now line 5; nine `source:` lines in the file, pre-existing) | existing `2026-10-26` | existing `on-release — python3 .ufo/waves/round-53/count-c1.py <rev> …` (command present in body line 13) | body line 13 |
| lane-silence-r2.md | none new; verified-at (11–14) to lines 2–5, recheck (15–20) to lines 6–11, source (3–10) to lines 12–19; blank line 2 removed | existing `source: PROTOCOL.md:157-168 …` (now line 12) | existing `2026-10-15T04:56Z — read-only recon …` | existing `the per-row commands below, then bash tools/mori-census.sh (live) and bash tools/mori-silence-cases.sh …` | body lines 15–17 (commands present) |

Entering head state (lines 1–12), for the record: audit-r11 and progressing-weak-r2 had no trio key; counter-semantics-r78, counter-win-r77, rotation-receipt-grammar-r76 and drift-pin-r10 had only `source:`; execution-binding-r89, kernel-v7.3-recheck-r53, lane-silence-r2 and rotation-schedule-r74 had `source:` and `verified-at:` and lacked `recheck:` in the head. The table is the post-edit state.

## 2. Per-file check output

Checker: scratch `check_trio.py` (regex `^key:` over the first 12 lines, the same predicate as `count-c1.py`; also a line-multiset comparison against `git show f63d1ab0:<path>`). Run on the scratch clone and on a fresh clone with the patch applied.

```
audit-r11:                    head source=1 verified-at=1 recheck=1  PASS  lines 426->429  added 3
counter-semantics-r78:        head source=1 verified-at=1 recheck=1  PASS  lines 69->69    moved only
counter-win-r77:              head source=1 verified-at=1 recheck=1  PASS  lines 119->119  moved only
drift-pin-r10:                head source=1 verified-at=1 recheck=1  PASS  lines 301->301  added 1 (recheck), removed 1 blank
execution-binding-r89:        head source=1 verified-at=1 recheck=1  PASS  lines 125->125  moved only
kernel-v7.3-recheck-r53:      head source=8 verified-at=1 recheck=1  PASS  lines 115->115  moved only (source count 8 in head; 9 in file, pre-existing)
lane-silence-r2:              head source=1 verified-at=1 recheck=1  PASS  lines 236->235  moved only, removed 1 blank
progressing-weak-r2:          head source=1 verified-at=1 recheck=1  PASS  lines 434->437  added 3
rotation-receipt-grammar-r76: head source=1 verified-at=1 recheck=1  PASS  lines 67->67    moved only
rotation-schedule-r74:        head source=1 verified-at=1 recheck=1  PASS  lines 50->50     moved only
FAILED_FILES 0   (check rc 0 on the scratch clone; rc 0 on a fresh clone with the patch applied)
```

Full-file uniqueness: `verified-at:` and `recheck:` each occur exactly once in all ten files; `source:` occurs once in nine files and nine times in kernel-v7.3-recheck-r53 (all pre-existing).

Patch verification:
- `git -C <scratch>/repo diff f63d1ab0 -- corpus/knowledge/` → `Mo92K01Trio.patch`, 10 files, rc 0.
- Fresh clone of the lane (`git clone --shared`), `checkout --detach f63d1ab0`, `rev-parse --show-toplevel` = the clone, `git apply --check <patch>` → rc 0.
- `git apply` in that fresh clone, then `corpus/knowledge/` compared with scratch → identical (`diff -r`, rc 0).

## 3. Decisions and deviations for the L1

1. **Moved, not duplicated.** Eight files had a key outside lines 1–12 (counter-semantics-r78, counter-win-r77, rotation-receipt-grammar-r76, rotation-schedule-r74, execution-binding-r89, kernel-v7.3-recheck-r53, lane-silence-r2, drift-pin-r10). Adding a second key would duplicate it; editing the body is forbidden. The lines were moved verbatim. These same eight files carry a pre-existing `verified-at:` whose value is **not** the admission-commit form the brief gives for new lines (e.g. `2026-11-02 (round 78; …)`, `2026-10-26`, `2026-10-15T04:56Z — …`, `2026-10-15T22:06:01–22:17Z, two arms …`). Counter-presence is met; the "verified-at names the admission commit" wording of C1 is not met for these eight. L1 decides whether to rewrite those values (a provenance-only edit) or accept the observation-date form.
2. **drift-pin-r10 readability.** Its `verified-at:` line (orig line 20) was the lead-in to eight bullets (orig 22–29). Moving the line leaves those bullets directly under the `source:` block without their lead-in. Text is intact; context is weaker. Same decision as 1.
3. **Existing recheck values are not commands** in counter-semantics-r78, counter-win-r77, rotation-receipt-grammar-r76, rotation-schedule-r74 (`180d` cadence) and execution-binding-r89 (`on-release`). The brief's rule (`manual, <path:line>` when the body gives no command) would rewrite them; they are existing values, so I kept them. Under that rule these five would be `manual`. No added recheck line is `manual`: all three added rechecks cite a command the body gives (audit-r11 lines 118/120; progressing-weak-r2 lines 49–52; drift-pin-r10 Erratum 297–298).
4. **drift-pin-r10 recheck command reads red.** Its Erratum records `--drift` exit 1 at 2026-10-19 (classification in `corpus/evidence/drift-r12-20261019T2204Z-classification.md`). The recheck line names the command; it does not assert a pass.
5. **Admission commits used for new verified-at lines** come from `git -C <lane> log --diff-filter=A --format='%h %cs'`: audit-r11 `e4855e8c` (2026-10-15); progressing-weak-r2 `3da84149` (2026-10-15). First lines, as the brief says.
6. Counter run: not run. The brief allows counters on scratch only when the task says so, and the scratch commit that the git-object-based counter would need is forbidden. The predicate was reproduced by the per-file check in §2.
7. Entering control: the ten files are all in `evidence/c1-missing-entering.txt` (confirmed).

## 4. Tooling and dead ends

- Tools installed or upgraded: none. No pacman, no uv, no npm.
- Dead end (no effect): the first edit batch was rejected by the editor because two anchored ranges had not been displayed (rotation-schedule 17–18, kernel 12–13). I displayed them and re-issued the identical batch. The rejected batch applied nothing.
- Host guard: writes only to scratch, to this report and to `patches/Mo92K01Trio.patch` under the wave `w1/` directory; no lane-tree write; no git mutation against the lane.

## 5. Checks the main agent should run

- After landing the full 19-file set: `python3 -I .ufo/waves/round-92/count-c1.py <landing rev> --repo <clone>`. `C1=met knowledge=98 missing=0 floor=98` requires all 19 listed files to carry the trio; these ten are a subset.
- `git apply --check .ufo/waves/round-92/w1/patches/Mo92K01Trio.patch` at f63d1ab0 (rc 0 here).
