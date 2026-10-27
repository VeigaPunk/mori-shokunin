# Mo52RevNoHarm — no-harm audit, round 52 wave w1 (C1 + C2 data lands)

Seat: Mo52RevNoHarm (leaf; no subagents). Scope: the round-52 data commit
`8524904adb25e44f24d9f25aac7eae909625c18c` against the entering tip
`4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d`, audited across all six axes
(coverage, operability, depth, freshness, calibration, adjacency). Verdict per
axis: harmed / not harmed, with evidence. All reads and runs below used absolute
paths; all temp work sat under `/fast/scratch/hyaku/mori-r52/Mo52RevNoHarm/`.
Nothing was written inside the lane except this report.

## What changed (the 33 tracked files)

`git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --stat 4f266ef2 8524904`
→ 33 files, +7933 −3:

- 22 new `.ufo/waves/round-52/` round artifacts (contract, both counters,
  controls, build-w1-spec.py, receipts, w1-spec.json). All additions; no
  pre-existing round-52 file overwritten (the round-52 directory did not exist
  at the entering tip).
- `SCORECARD.md`: exactly 3 lines rewritten (operability, depth, freshness rows
  of the Axes table).
- `corpus/QUALITY.md`: +21 lines appended (criteria 141, 142).
- `corpus/README.md`: +13 lines appended (round-52 corrections section).
- `corpus/SOURCES.md`: +5 rows (S497–S501).
- `corpus/evidence/sources-r52/`: 5 new kernel source copies.
- `corpus/knowledge/overcommit-commit-limit-r52.md`: new entry (75 lines).

No tracked file was deleted, no existing row/cell edited in place except the
three SCORECARD cells; SHONEN.md, LOG.md, SKILL.md, PROVINCE.md, `merge/mori/`
and all sibling lanes are untouched by the round's data (only the wave's own
untracked `w1/*` report files exist in `git status`, all written by wave seats).

## Reproducibility evidence (run in a `--no-local` clone in scratch)

- `python3 .ufo/waves/round-52/count-c1.py 8524904… --repo <clone> --fleet-repo /home/vgpnk/Projects/shokunin --scratch <scratch>` →
  `C1=met items=42 axes=6 pins=2 boxes=4 living=7 superseded=4 locators=27 mismatches=0 errors=0 hidden=0 lane_writes=0 manifest=6209bdb8e400 rev=8524904…`, exit 0 — byte-identical to `evidence/c1-at-data.txt`.
- `python3 .ufo/waves/round-52/count-c2.py 8524904…` →
  `C2=unmet claims=28 located=28 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 … failed=entailment`, exit 1 — byte-identical to `evidence/c2-at-data.txt`.
- `count-c1.py --selftest` → `C1_SELFTEST pass=42 fail=0`, exit 0 (matches `evidence/selftest-c1.txt`).
- `count-c2.py --selftest` → `C2_SELFTEST pass=45 fail=0`, exit 0 (matches `evidence/selftest-c2.txt`).
- `git status --short` of the clone after all runs: clean (no instrument wrote into the repo it read).
- Source copies: `sha256sum` of the five `sources-r52/` files equals the hashes in the SOURCES rows, the entry's `recheck:` line, and `evidence/freeze-sha256.txt` (767ab881…, bf8ca026…, e702754c…, d7bf787c…, 449b8583…).

## Axis verdicts

### coverage — not harmed
All changes are additive; the only −3 lines are the replaced tails of three
SCORECARD cells (verified by `git diff --word-diff`). The new entry fills
confirmed-blank ground: the pre-data sweep (`evidence/sweep-overcommit.txt` at
`4f266ef2`) reports 0 occurrences of every overcommit ledger term in
`SOURCES.md`, `corpus/knowledge/`, `SKILL.md`, and 0 `merge/mori/` staged
files. The entry's `coverage-map:` line ("resource runway … no FR row held it")
matches the FR registry (`corpus/README.md:348`, FR8 open; FR1/FR10–FR12 rows
do not hold runway). S497–S501 URLs are new (they do not appear in the 23 W04
duplicate-URL census rows; `evidence/census-start.txt`). No new surface claimed
outside the mori lane.

### operability — not harmed
Counters are new instruments, not replacements: no frozen instrument verdict
changed (round-51 counters untouched; nothing in the diff touches
`tools/`). The round-52 selftest receipts record literal commands including the
checkout hash (`evidence/selftests/mori-pin-check.txt` line 1: `cd <lane
checkout at d3a8ea5957…> && python3 tools/mori-pin-check.py --selftest`),
satisfying the round-51 closure item 7. Both counters' selftests re-run green,
and both counters reproduce their data-commit receipts verbatim from a scratch
clone (`lane_writes=0`). The two SHONEN instrument pins (`python3
tools/mori-pin-check.py --selftest` → 125/125; `python3
tools/mori-unlanded-check.py --selftest` → 17/17) were red at the entering tip
with `_receipt_missing` and are green at data with the new round-52 receipts
present. No runtime config, sysctl, cgroup or service was touched.

### depth — not harmed, two accuracy nits (MED/LOW below)
Entry shape matches the round-51 entry convention (`source:` lines, `verified-at:`,
`recheck:` with curl+sha256, `coverage-map:`, Claims table, reading rules,
Boundaries). All 28 claim quotes are verified present in the copies
(`located=28 quote_missing=0`), and the five source copies hash to the pinned
shas. I independently spot-checked the load-bearing rows against the copies:
row 4 (meminfo prints both lines — `meminfo.c.v7.2:125-126`), rows 14–21
(`util.c.v7.2:904-1003`), row 23/24 (`mman.h.v7.2:76-84`), rows 25/26
(`mmap.c.v7.2:550-558`), rows 1–13 (both .rst copies). The entry's anchor to
round-51 data (`fs/proc/meminfo.c:125-126` as S494) is correct. Two wording
problems are in Findings 1 and 2.

### freshness — not harmed
The only freshness-cell change is a pointer correction: `SCORECARD.md:1771`
→ `:1781` (line 1771 holds the round-28 amendment A1 paragraph; line 1781 holds
the round-28 measured-outcome row "freshness 5 → 6 proposed" — verified by
`grep -n "5 → 6" SCORECARD.md`). Stale pins are superseded, never rewritten:
append-only notes in README (lines 727-728) and QUALITY (141 supersedes 112's
check cell only), matching the frozen house rule. All pins the counter enumerates
pass at data (living=7, superseded=4); the new pins (QUALITY:1360, README:727-728)
are current (MORI_SOURCES_APPENDONLY_SELFTEST pass=22 rc=0; CONFORM_SELFTEST
pass=9 rc=0). The appended notes are dated 2026-10-26. The README bullet pins
the entering-tip rev `4f266ef2` in its runnable conform command; that is a
deliberate absolute rev and runs correctly today (it will need a future
supersession like any pin — not a current harm).

### calibration — not harmed
The frozen C1 control matrix and the landed data agree: the do-nothing receipt's
eight mismatches map one-to-one onto landed fixes — (1)(2) operability/depth
last-change cells now cite the round-51 closure (`round-51-verifier-spotcheck.md:130`
and `:131`, verified to contain the quoted verdicts and scores); (3)(4) the two
SHONEN pins now have round-52 receipts; (5)(6)(7) the three stale living pins are
superseded; (8) the `SCORECARD.md:1771` locator pair is corrected to `:1781`.
The disclosed witness control and the landed data produce identical counter
output (items=42, living=7, superseded=4, locators=27, mismatches=0), so the
data commit applies exactly the four disclosed parts. `C1=met` at data, exit 0.

### adjacency — not harmed
Only mori-lane files changed; no sibling lane or fleet-root file is in the diff.
The new entry's boundary citation `../tsukuroi-shokunin/PROVINCE.md:8-14,28`
resolves (lines 8-14 = read-only owned surfaces; line 28 = "Detection and
report; the operator remediates."), and is cross-consistent with tsukuroi's
own PROVINCE (lines 30-33) delegating fleet correlation to mori, and with mori
PROVINCE.md:6-16 (resource runway ownership, OS-state refusal). The entry
explicitly disclaims sysctl ownership (task is the operator's), so no scope
crosses into tsukuroi's ground.

## Findings

1. **MED** — `corpus/knowledge/overcommit-commit-limit-r52.md` rows 27/28 and
   `corpus/SOURCES.md` S501 summary state the boot-time caps as "128 MiB" and
   "8 MiB", but the quoted v7.2 bytes are `SZ_128K` and `SZ_8K`
   (`mmap.c.v7.2:1595`, `:1616`), which `include/linux/sizes.h` at v7.2
   defines as `0x00020000` (128 KiB) and `0x00002000` (8 KiB). The kernel's own
   comment (`mmap.c.v7.2:1586-1587`, `1624-1625`) and `vm.rst` state the
   intended 128 MB / 8 MB (and `util.c.v7.2:785-786` uses `1UL << 17` / `1UL <<
   13` for the sysctl defaults), so the claim conflates documented intent with
   the literal boot-time constant. Recommended data correction: word the rows
   from the literal ("capped at min(free_kbytes/32, SZ_128K), i.e. 128 KiB by
   the byte constant; the docs and sysctl default state 128 MiB") or add the
   gap to Boundaries.
2. **LOW** — entry "Reading rules" row 2 cites `util.c.v7.2:969-977` for the
   mode-2 request-time refusal; those lines are the OVERCOMMIT_ALWAYS/GUESS
   branches, and the never-overcommit test is at `:994` (range 978-995). The
   sentence's substance is correct; only the line anchor is off.
3. **LOW** — `corpus/QUALITY.md:1359` (criterion 141 rationale) cites "(QUALITY
   128)" for "the committed tool has printed 22 since the round-41 freeze
   d72ac167"; the pass=22 statement actually lives in criterion 123
   (`QUALITY.md:1033-1034`). Criterion 128 is about located quotes. Reference
   should read 123.
4. **LOW** — `evidence/freeze-sha256.txt` lists the frozen contract/counters/
   controls/selftest receipts but omits `evidence/selftests/mori-pin-check.txt`
   and `evidence/selftests/mori-unlanded-check.txt`, which the C1 arm-B pins
   gate on at R. Governance note only: the files are committed with the data and
   reproduce, so no current harm.

## Verification gap
No live host reads were needed or performed for this audit (host port is
read-only and the claims are v7.2-byte claims). The C2 entailment votes and the
wave's attack seats will land after this report; the data-commit state
(`C2=unmet … failed=entailment`) is the expected pre-vote state and was
reproduced.
