# Mo53ScribeReadme — round-53 w1 scribe: the `corpus/README.md` coverage additions

Seat: Mo53ScribeReadme (leaf, no subagents). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Scope: draft only — the `## Round-53 coverage additions` block for `corpus/README.md`, in the house
shape of the round-52 block (`corpus/README.md:736-747`). Nothing under `corpus/`, `SKILL.md`,
`tools/` or `.ufo/waves/round-53/` was written except this report. Scratch
`/fast/scratch/hyaku/mori-r53/Mo53ScribeReadme/` was created for `TMPDIR` and removed at the end
(`rm -rf` before exit; nothing cited depends on it).

## Reads (absolute paths)

- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-53/contract.md` — C1/C2, the
  vote-line rule for the twelve voter reports (no other seat starts such a line), the
  frozen-counter rule.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/README.md` — coverage map, `## Frontier`
  table (FR8 at `:348`), the round-49/50/51 dated notes, the round-52 block at `:736-747`
  (last line 747, file ends with a newline).
- `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/knowledge/commit-runway-read-r53.md` (56 lines),
  `.../kernel-v7.3-recheck-r53.md` (111 lines).
- `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md:281-292` (S502–S513), `:344`
  (round-53 bounded search), `:351` (the v7.3 panic lead).
- `/home/vgpnk/Projects/shokunin/mori-shokunin/SKILL.md:1178-1215` (`## Round53`, its registry row).
- `/home/vgpnk/Projects/shokunin/mori-shokunin/PROVINCE.md:42-60` (Frontier rows, FR8 at `:51`).
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-53/evidence/sweeps.txt`,
  `c1-at-data.txt`, `c2-at-data.txt`, `census-start.txt` (tail).
- `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r53/vm.rst.v7.3:920-935,998-1006`.

## Observed checks (command → output → exit)

1. `cd /home/vgpnk/Projects/shokunin/mori-shokunin && python3 -I -B tools/mori-commit-runway.py`
   → one JSON line, `schema: mori-commit-runway-v1`, `verdict: COMMIT_HEURISTIC`, `mode: 0`,
   `cpus_present: 32`, `commit_limit_kb: 47583772`, `committed_as_kb: 38334788`,
   `headroom_kb: 9248984`, `single_request_cap_kb: 63444672`, `reserve_kb: null`,
   `band_kb: null`, `batch_pages: null`, `limit_recomputed_kb: 47583772`,
   `limit_consistent: true`, `findings: []`, `enforced: false` → exit 0.
2. Same tool `--selftest` (with `TMPDIR=/fast/scratch/hyaku/mori-r53/Mo53ScribeReadme/tmp`)
   → `MATCHER: rejected 23/23 corrupted expectations` then
   `MORI_COMMIT_RUNWAY_SELFTEST: PASS 23/23` → exit 0.
3. `python3 .ufo/waves/round-53/count-c1.py 2a4213bf8da72f7cd78189baa5bb9be825dca1df`
   → `C1=unmet scope=46 rows=46 matched=46 status_ok=46 quote_ok=46 source_rows=ok pins=ok
   provenance=ok held=44 absent=2 holds=46 changed=0 voted=0 dissent=0
   rev=2a4213bf8da72f7cd78189baa5bb9be825dca1df failed=votes` → exit 1; byte-identical to
   `evidence/c1-at-data.txt`.
4. Ledger row counts by `grep -c`: `^| [0-9a-f]{12} |` = 46, `| held |` = 44, `| absent |` = 2
   (`kernel-v7.3-recheck-r53.md`).
5. `git diff --stat 20edafa5 2a4213bf -- tools/mori-census.sh` → empty, exit 0;
   `grep -c 'CommitLimit\|Committed_AS\|commit-runway' tools/mori-census.sh` → `0`, exit 1.
6. `git diff --stat 20edafa5 2a4213bf` → 40 files, `corpus/README.md` is **not** among them, so the
   block below is the first landing of round-53 coverage text in the README.
7. `grep -n "panic_on_unrecoverable_memory_failure" corpus/evidence/sources-r53/vm.rst.v7.3`
   → `67`, `926` (section heading), `1002` (the `echo 1 > …` example). The section reads: "When a
   hardware memory error (e.g. multi-bit ECC) hits a kernel page that cannot be recovered by the
   memory failure handler, the default behaviour is to ignore the error and continue operation."
8. `recheck:` pins: `oom-tracepoints-r47.md` → `on-release`; `oom-memcg-stat-r50.md` → `90d`
   (three sha256 pins).
9. `grep -c` of the commit-ledger names in `tools/` at the entering tip: `sweeps.txt:2-3` shows
   `git grep -c … -- tools/` → `exit=1 (1 = no match)`; v7.3 hits in `corpus/knowledge`,
   `corpus/SOURCES.md`, `SKILL.md` at the tip → `exit=1`; `refs/tags/v7.3^{}` →
   `c03c1a14507dfaf8b856c2608f9ac216021fc222`.
10. `scripts/hyaku/disk-guard.sh status`: `/fast/scratch/hyaku` 25 % used, 609.3 G free — no
    ENOSPC condition; `uname -r` → `7.2.11-arch1-1` (the host is still the v7.2 line).

No tool was installed or upgraded; no pacman transaction; no git/jj mutation; no census/journal read
beyond the evidence files listed (no kernel-log MESSAGE text was grepped).

## Draft — `## Round-53 coverage additions` (append at the end of `corpus/README.md`, after line 747)

```markdown
## Round-53 coverage additions

| Ground | Entry | Bounded advance |
|---|---|---|
| Resource runway — the commit ledger as a verdict (knowledge → tool) | `knowledge/commit-runway-read-r53.md` (S511–S513); `tools/mori-commit-runway.py`, its fixtures and the `## Round53` registry row | Round 52 said what `CommitLimit` and `Committed_AS` are; the tool reads them under the mode that decides enforcement and, under mode 2, prints `usable_kb` against `band_kb` = batch × present CPUs × page — the lag the per-CPU counter's global-only read leaves in `Committed_AS` (`COMMIT_LOW`, exit 1, when the room is inside the band) — while modes 0/1 print the ledger and never read it as a limit (`COMMIT_HEURISTIC` / `COMMIT_UNLIMITED`, exit 0). `python3 -I -B tools/mori-commit-runway.py --selftest` → `MORI_COMMIT_RUNWAY_SELFTEST: PASS 23/23` with `MATCHER: rejected 23/23 corrupted expectations`; the frozen counter agrees 80/80, no disagreement (`C2=met … agree=80 disagree=0 registry=ok live=ok`, `.ufo/waves/round-53/evidence/c2-at-data.txt`); the live read on this host (2026-10-26, mode 0, 32 present CPUs) printed `COMMIT_HEURISTIC` with `limit_consistent: true`, exit 0. Bounded: `COMMIT_LOW` is "inside the counter's own error band", not a calibrated alarm (FR8 stays open); the band is an upper bound from the batch rule with present CPUs and today's totalram, not a measured deviation; the counter's REF and the tool share one author, so a shared misreading of the kernel passes both; the tool reads no cgroup-level commit and gives no alert threshold. |
| Freshness — the round-51/52 claim rows rechecked at tag v7.3 | `knowledge/kernel-v7.3-recheck-r53.md` (S502–S510; its own `coverage-map:` files it under resource runway, no new ground) | The release trigger is answered for the two entries' tables: 46 v7.2-pinned rows re-read at v7.3 (44 `held`, 2 `absent` — both `MAP_NORESERVE` quotes, respelled `vma_flags_set(&vma_flags, VMA_NORESERVE_BIT)`), every row's disposition `holds`. `python3 .ufo/waves/round-53/count-c1.py 2a4213bf8da72f7cd78189baa5bb9be825dca1df` → `C1=unmet scope=46 rows=46 matched=46 status_ok=46 quote_ok=46 source_rows=ok pins=ok provenance=ok held=44 absent=2 holds=46 changed=0 voted=0 dissent=0 … failed=votes`, exit 1 (`.ufo/waves/round-53/evidence/c1-at-data.txt`; the vote arm is the twelve RECHECK seats', and its landed line is the round-53 report's). Bounded: `held` proves the words still occur somewhere in the v7.3 file, not at the same place or with the same meaning — the disposition and its two votes carry that; the recheck covers the two tables only, so `oom-tracepoints-r47.md`, the round-50 memcg entry (`recheck: 90d`), the prose outside the tables and the anchors of S492–S501 stay unrechecked at v7.3; the pins prove the bytes are what the L1 fetched from cgit, not that cgit served the tag. |

Dated note (append-only, 2026-10-26): the commit-runway entry supersedes the round-52 note's "no instrument reads
the ledger yet" — the ledger has a read-only reader, and under mode 2 that reader states its own error band instead
of a headroom number; the routed commit-ledger census line is answered by that tool, not by a census arm (the
census carries 0 hits of the commit-ledger names at the entering tip and `tools/mori-census.sh` is unchanged
through the data commit, `evidence/sweeps.txt`); no frontier row is rewritten. Still frontier: FR8 —
`COMMIT_LOW` is "inside the counter's own error band", not a calibrated threshold, and no workload window
prices it (`knowledge/commit-runway-read-r53.md` §Boundaries); the v7.3
`panic_on_unrecoverable_memory_failure` section (S507 copy line 926) names a panic surface for an unrecoverable
hardware memory error — a lead for mori's kill-event frontier, not a claim of this round, and `mm/memory-failure.c`
at v7.3 was not opened (`SOURCES.md:351`); and the recheck is bounded to the round-51/52 tables, so
`knowledge/oom-tracepoints-r47.md` (its own pin is `recheck: on-release`, and the v7.3 tag fires it too) and
`knowledge/oom-memcg-stat-r50.md` (`recheck: 90d`) are unrechecked at v7.3
(`knowledge/kernel-v7.3-recheck-r53.md` §Boundaries).
```

## Integration notes for the L1

- Insert exactly one block, appended after `corpus/README.md:747`; the round-52 block above it stays
  byte-identical, and no row of `## Frontier` (`:336-352`) is edited — the FR8 row `:348` is only
  referenced.
- Row 2's Ground label is "Freshness" per the seat assignment; the ledger's own `coverage-map:` line
  (`kernel-v7.3-recheck-r53.md:14`) says resource runway, no new ground, and the row states that
  parenthetically so the two do not read as a conflict.
- Row 1 cites the tool's verdict class and `limit_consistent: true` from my own live read, not the
  over-limit instance the entry records at `commit-runway-read-r53.md:44-45` (see F1).
- Row 2 cites the at-data counter line (exit 1, `failed=votes`) because the votes were not landed at
  this seat's clock; swap in the landed line from `.ufo/waves/round-53/evidence/c1-at-landed.txt` and
  the round-53 report when the wave closes, if the house style wants the landed reading in the README.
- Nothing here is a command-tally pin in the round-52 sense (arm C reads `QUALITY.md`/`README.md`
  pins; `.ufo/waves/round-52/count-c1.py`): the two pin-shaped strings are the identical selftest and
  counter commands above, both re-run by this seat (observations 2 and 3).

## Findings

- **MED — `corpus/knowledge/commit-runway-read-r53.md:44-45`.** The host sentence reads "the
  recomputed limit equals the printed 47583772 kB and Committed_AS exceeds it — `COMMIT_HEURISTIC`
  with `over_limit_not_enforced`, exit 0". My live read of the same tool on 2026-10-26 prints
  `committed_as_kb: 38334788` against `commit_limit_kb: 47583772` (`headroom_kb: 9248984`,
  `findings: []`, exit 0): the over-limit state is not reproducible at the scribe's clock. The dated
  capture may be true for its moment, but the sentence is the kind of host instance a README row
  would copy; the draft above therefore cites only `COMMIT_HEURISTIC` and `limit_consistent: true`.
  The L1 decides whether the entry keeps the instance as a dated capture or re-reads it.
- **LOW — `corpus/knowledge/oom-tracepoints-r47.md:5`.** Its pin is `recheck: on-release`, so the
  v7.3 tag fires that entry's trigger as well, but the C1 scope D covers only the round-51/52
  tables (`kernel-v7.3-recheck-r53.md:107`), so a third `on-release` entry stands unanswered at
  v7.3. Named in the contract as a C1 limit; routed item for round 54, not a counter change.
- **LOW — `corpus/knowledge/commit-runway-read-r53.md:9` vs `corpus/knowledge/kernel-v7.3-recheck-r53.md:14`.**
  The two `coverage-map:` lines both file under "resource runway", while the seat assignment and the
  drafted row label the recheck row "Freshness" (the freshness axis, no new ground). Both readings
  are true; if the L1 wants one label, the entry line is the one to align — no counter reads a
  `coverage-map:` line for C1 (checked: `count-c1.py` and `count-c2.py` contain no `README` or
  `coverage-map` reference).
- **LOW — `corpus/README.md:745-746` (round-52 note, superseded clause only).** "no instrument reads
  the ledger yet … a commit-ledger census line is routed to round 53" is answered by a tool, not by
  a census line: `tools/mori-census.sh` still prints 0 hits of `CommitLimit`/`Committed_AS`/
  `commit-runway` and is byte-unchanged between `20edafa5` and `2a4213bf`. The drafted note says so
  explicitly; a census arm, if wanted, is round-54 work.
