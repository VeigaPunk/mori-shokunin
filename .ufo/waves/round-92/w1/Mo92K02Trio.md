# Mo92K02Trio — round 92 wave w1: C1 provenance trio on nine `corpus/knowledge/` entries

Entering revision: `f63d1ab030d4179576e494342f48ef8718e497a5`. Patch: `.ufo/waves/round-92/w1/patches/Mo92K02Trio.patch`
(9 files, +39 / −23, `corpus/knowledge/` only). Scratch clone verified (`rev-parse --show-toplevel` = scratch repo) and
removed before this report. No tools installed or upgraded. No git mutation against the lane; lane reads were
`git log --diff-filter=A` and `ls` only.

## Deviation the L1 must know about: out-of-window keys were moved, not duplicated

Four files already carried provenance keys below line 12, so the counter's window (lines 1–12) missed them.
Adding a second copy would duplicate a key (contract rule), so the existing lines were cut and pasted, byte-identical,
into the head. No body text changed.

- `rotation-series-r75.md`: existing `verified-at:` (:13–17) and `recheck:` (:18–20) moved to :1–8.
- `selftest-flake-r9.md`: existing `verified-at:` (:13–19) moved to :2–8; new `recheck:` at :9.
- `surfaces-r8.md`: existing `recheck:` (:20–22) moved to :2–4 (`verified-at:` now at :12, still in window).
- `workstate-win-r71.md`: existing `verified-at:` (:11–13, already in window) and `recheck:` (:14–15) moved to :1–5,
  so that `source:` stays in window at :6.

Check: for all nine files the removed-line multiset against `f63d1ab0` is empty (`removed_lines=0`); the only
additions are the new key lines listed below. Existing key values were kept verbatim, including the four
non-admission-form `verified-at:` values (for example `2026-10-15T21:05–21:35Z — …`); only missing keys get the
admission-commit form.

## Per-file table

Admission commit = `git -C <lane> log --diff-filter=A --format=%h%x20%cs -- corpus/knowledge/<file>` (one add per file).
"new" = added by this patch; "moved" = existing line relocated into the window.

| file | keys | source | verified-at | recheck | body line giving the recheck |
|---|---|---|---|---|---|
| rotation-series-r75.md | moved verified-at, recheck (existing `source:` at :9) | existing `S590 (docs.aws.amazon.com — CAPTCHA …` | existing `2026-11-02 (round 75; …)` (not admission form, kept) | existing `180d, or when a fresh session …` (kept) | **none**: body gives no command; anchor receipt cited at :8–9 (`.ufo/waves/round-75/evidence/s590-anchor-check-r75.txt`) |
| selftest-flake-r9.md | new recheck; moved verified-at (existing `source:` at :11) | existing `tools/mori-census.sh before sha256` | existing `2026-10-15T21:05–21:35Z — …` (kept) | new: `awk 'NR>=1571' tools/mori-census.sh \| grep -nE '…' ` (static race-class scan) | :225–228 (§6 item 1) |
| silence-cutover-r3.md | new source, verified-at, recheck | new: `tools/mori-census.sh; tools/mori-silence-cases.sh; corpus/evidence/cutover-r3-20261015T165712Z-selftest.log; corpus/evidence/cutover-r3-20261015T164140Z-before.log` | new: `1439c473 (2026-10-15), admission commit` | new: `manual, corpus/knowledge/silence-cutover-r3.md:121 (selftest receipt …)` | **none**: body gives no command; manual pointer to the primary evidence line :121 |
| silence-grading-r2.md | new source, verified-at, recheck | new: `corpus/knowledge/lane-silence-r2.md; tools/mori-silence-cases.sh; PROTOCOL.md:153-168; .ufo/watchdog.log` | new: `3da84149 (2026-10-15), admission commit` | new: `date -u -d '2026-10-15T01:50:57-03:00' +%s` (expect 1792039857) | :75 (also :243) |
| surfaces-r8.md | moved recheck (existing `source:` at :6, `verified-at:` at :12) | existing `tools/mori-census.sh sha256` | existing `2026-10-15T20:17–20:39Z — …` (kept) | existing 3-line command block (kept) | :20–22 (the block itself is the command set) |
| verdict-machine-r4.md | new source, verified-at, recheck | new: `tools/mori-silence-cases.sh; tools/mori-census.sh; corpus/evidence/verdict-r4-20261015T173551Z-live.log` | new: `5b62c897 (2026-10-15), admission commit` | new: `bash tools/mori-silence-cases.sh` (expect matched=28 total=28, exit 0) | :98–99 |
| verdict-machine-r5.md | new source, verified-at, recheck | new: `tools/mori-silence-cases.sh; tools/mori-census.sh; corpus/evidence/order-r5-20261015T180431Z-*.log` | new: `a420deb7 (2026-10-15), admission commit` | new: `bash tools/mori-silence-cases.sh` (expect matched=28 total=28, exit 0) | :248–252 (re-run recipe; command at :250) |
| verdict-machine-r6.md | new source, verified-at, recheck | new: `tools/mori-silence-cases.sh; tools/mori-census.sh` | new: `92b2e427 (2026-10-15), admission commit` | new: `bash tools/mori-silence-cases.sh` (expect exit 0, matched=28 total=28) | :242–246 (re-run recipe; command at :244) |
| workstate-win-r71.md | moved verified-at, recheck (existing `source:` at :6) | existing `S584 (learn.microsoft.com — QueryUnbiasedInterruptTime …; S582 …` | existing `2026-11-01 (round 71; …)` (kept) | existing `180d, or when a re-fetch of either page changes its sha256 …` (kept) | **none**: body gives no command; live receipt cited at :11–13 (`.ufo/waves/round-71/evidence/workstate-live-r71.txt`) |

Files where the body gives no re-verification command: `rotation-series-r75.md` and `workstate-win-r71.md` (existing
recheck values retained; they are durations/conditions, not commands) and `silence-cutover-r3.md` (recheck is `manual`).

## Source-path checks (`test -e` in the scratch clone at `f63d1ab0`)

- Present: `corpus/knowledge/lane-silence-r2.md`, `tools/mori-silence-cases.sh`, `tools/mori-census.sh`,
  `corpus/evidence/cutover-r3-20261015T165712Z-selftest.log`, `corpus/evidence/cutover-r3-20261015T164140Z-before.log`,
  `corpus/evidence/verdict-r4-20261015T173551Z-live.log`, `corpus/evidence/order-r5-20261015T180431Z-*.log` (glob, 6 files).
- **Absent from the lane tree**: `PROTOCOL.md` and `.ufo/watchdog.log` (cited in `silence-grading-r2.md` :54, :73 — fleet-root
  artifacts). Kept in `source:` because the body cites them; flagged.
- **Body cites receipts that do not exist**: `verdict-machine-r6.md` :19–20 cites
  `corpus/evidence/backchannel-r6-20261015T{190229,190453}Z-*.log`; the lane holds only the `T191216Z` set. Not used as
  `source:`; `source:` cites the two tools only. Flagged.

## Per-file check output

Python check in scratch (same rule as `count-c1.py`: `^key:` within the first 12 lines, each key once, body lines preserved):

```
rotation-series-r75: within12={'source': True, 'verified-at': True, 'recheck': True} keycount={'source': 1, 'verified-at': 1, 'recheck': 1} removed_lines=0 OK
selftest-flake-r9:   within12={'source': True, 'verified-at': True, 'recheck': True} keycount={'source': 1, 'verified-at': 1, 'recheck': 1} removed_lines=0 OK
silence-cutover-r3:  within12={'source': True, 'verified-at': True, 'recheck': True} keycount={'source': 1, 'verified-at': 1, 'recheck': 1} removed_lines=0 OK
silence-grading-r2:  within12={'source': True, 'verified-at': True, 'recheck': True} keycount={'source': 1, 'verified-at': 1, 'recheck': 1} removed_lines=0 OK
surfaces-r8:         within12={'source': True, 'verified-at': True, 'recheck': True} keycount={'source': 1, 'verified-at': 1, 'recheck': 1} removed_lines=0 OK
verdict-machine-r4:  within12={'source': True, 'verified-at': True, 'recheck': True} keycount={'source': 1, 'verified-at': 1, 'recheck': 1} removed_lines=0 OK
verdict-machine-r5:  within12={'source': True, 'verified-at': True, 'recheck': True} keycount={'source': 1, 'verified-at': 1, 'recheck': 1} removed_lines=0 OK
verdict-machine-r6:  within12={'source': True, 'verified-at': True, 'recheck': True} keycount={'source': 1, 'verified-at': 1, 'recheck': 1} removed_lines=0 OK
workstate-win-r71:   within12={'source': True, 'verified-at': True, 'recheck': True} keycount={'source': 1, 'verified-at': 1, 'recheck': 1} removed_lines=0 OK
FAILS 0   (exit 0)
```

Patch applied to a fresh clone detached at `f63d1ab0` (`git clone --shared`, `rev-parse --show-toplevel` checked):
`git apply --check` exit 0; `git apply` exit 0; the same python check on the applied tree: `PYCHECK pass` (exit 0);
`git status --short` lists the nine files only.

Recheck command runs (read-only, scratch):

- `date -u -d '2026-10-15T01:50:57-03:00' +%s` → `1792039857`, exit 0 (matches `silence-grading-r2.md:75`).
- `awk 'NR>=1571' tools/mori-census.sh | grep -cnE '…'` (selftest-flake-r9 recheck) → `2`, grep exit 0. **The body's
  "must be empty" (:228) does not hold at `f63d1ab0`.** Both hits are comment lines at `tools/mori-census.sh:2449`
  (`# F01 (audit-r11 §4 …`) and `:3300` (`# The replaced idiom …`), not live pipelines. The recheck line in the
  patch says so explicitly; the body text was not changed.

Not run: the oracle `bash tools/mori-silence-cases.sh`, `bash tools/mori-census.sh --selftest`, and `count-c1.py`
(the counter is not to be run on the lane; my check mirrors its rule on the scratch tree).

## Dead ends

- None blocking. The out-of-window move (above) was the only structural decision; the recheck-command mismatch and the
  two absent/unresolvable source citations are reported, not papered over.
