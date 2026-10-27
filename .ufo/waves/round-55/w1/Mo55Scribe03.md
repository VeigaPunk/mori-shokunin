# Mo55Scribe03 — round-55 C1/C2 scope and limits (report-only, non-voting)

Seat: Mo55Scribe03 (scribe, leaf). Lane `mori-shokunin`, wave `w1`, reportDir `.ufo/waves/round-55/w1`.
Measured: 2026-10-27, working-tree HEAD `b8a70adf93ebd9d1e4e95bef8627a220f2fa816b`, data commit
`b8b7064c2b54c8b6b22c288232a96c43fae1af47`, entering tip `ca52426ea496bc6592e3e867cc9d28843e45f196`,
frozen inputs `c9b908f0bb89974f30b927776ce2450ae4198b10`.
This seat holds no vote. This report contains no vote line and is not a voter report for either arm.

## Behavior

Read-only synthesis of committed evidence, plus re-execution of the frozen counters (documented as
read-only: `git show` / `git ls-tree` / `git rev-parse` only, count-c1.py:30-33, count-c2.py:28-29).
The working tree changed while this pass ran (see the drift finding under Findings); every counter result comes
from git objects at fixed revisions, so no count reported here is affected by that drift, and this seat wrote
none of those bytes.
Read: frozen `contract.md`; both counter predicates and their named limits; `evidence/c1-scope.txt`,
`c1-scope-count.txt`, `c1-at-data.txt`, `c2-at-data.txt`, `c2-claims.txt`, `selftest-c1.txt`,
`selftest-c2.txt`, `control-c1-do-nothing.txt`, `control-c2-do-nothing.txt`, `freeze-sha256.txt`,
`census-start.txt`, `census-end.txt`, `host-disk-snapshot.txt`; ledger `corpus/knowledge/kernel-v7.3-recheck-r55.md`;
entry `corpus/knowledge/disk-runway-enospc-r55.md` at the data commit; `corpus/SOURCES.md` rows S502,
S516, S526–S543; `w1-plan.json`, `w1/swarm-registry.json`; `assimilation/quarantine-verdicts.txt`.

No production edit, no git mutation, no host change, no install (pacman not invoked), no judge/commit.
Scratch `/fast/scratch/hyaku/mori-r55/Mo55Scribe03` used and removed.

## Gates measured

| # | gate | command | observed | exit |
|---|---|---|---|---|
| 1 | C1 at data commit | `python3 .ufo/waves/round-55/count-c1.py b8b7064c… --repo .` | `C1=unmet scope=78 rows=78 matched=78 status_ok=78 line_ok=78 source_rows=ok pins=ok provenance=ok same=69 moved=7 changed=2 broken=0 holds=78 stale=0 voted=0 dissent=0 rev=b8b7064c… failed=votes` | 1 |
| 2 | C2 at data commit | `python3 .ufo/waves/round-55/count-c2.py b8b7064c… --repo .` | `C2=unmet claims=23 located=23 quote_missing=0 bad_rows=0 sources=9 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=b8b7064c… failed=entailment` | 1 |
| 3 | C1 at HEAD | `count-c1.py HEAD` | identical counts, `rev=b8a70adf…` | 1 |
| 4 | C2 at HEAD | `count-c2.py HEAD` | identical counts, `rev=b8a70adf…` | 1 |
| 5 | C1 at correction 1 | `count-c1.py 51ebd3d3` | identical counts | 1 |
| 6 | both at receipt rev | `count-c1.py f70051dd`, `count-c2.py f70051dd` | identical counts (so the committed receipts are not stale in numbers) | 1 |
| 7 | frozen scope extraction | `count-c1.py --scope \| sort` vs `evidence/c1-scope.txt` | `diff` empty; `scope_identical`; 78 lines | 0 |
| 8 | C2 claim hashes | `count-c2.py --hashes b8b7064c` vs `evidence/c2-claims.txt` | `diff` empty; `claim_hashes_identical_at_data_commit` | 0 |
| 9 | frozen pins | `sha256sum -c .ufo/waves/round-55/evidence/freeze-sha256.txt` | 35/35 `OK`, no failures printed | 0 |
| 10 | counter selftests (receipt, not re-run) | `evidence/selftest-c1.txt`, `selftest-c2.txt` | `C1_SELFTEST pass=44 fail=0`, `C2_SELFTEST pass=10 fail=0`, `exit=0` | 0 |
| 11 | do-nothing controls (receipt) | `evidence/control-c1-do-nothing.txt`, `control-c2-do-nothing.txt` | `failed=ledger_absent,pins` / `failed=entry_absent,pins` | 1 |
| 12 | census | `evidence/census-start.txt:25`, `census-end.txt:25` | `exit=0` both | 0 |
| 13 | disk guard | `scripts/hyaku/disk-guard.sh status` | `use%` 34% / 26% / 3%; `/fast` free 594.6G | 0 |
| 14 | settlement state | `ls .ufo/waves/round-55/w1-results.json`; `git status --porcelain` | results file absent at both reads; `w1/*.md` count 20 at first read, 44 at 06:50Z, all untracked | — |

## C1 scope (measured, data commit)

- 78 unique `(entry, path, lines)` groups; hash = first 12 hex of `sha256("<entry>|<v7.2 path>|<lines>")`
  (count-c1.py docstring; `matched=78` proves the derivation).
- Per entry: `system-pressure-r24.md` 51, `oom-victim-selection-r27.md` 14, `oom-tracepoints-r47.md` 13,
  `watchdog-identity-r31.md` 0 (its v7.2 kernel citations are S-id-only, so the extractor sees no pointer —
  contract.md:18).
- Status: 69 `same`, 7 `moved`, 2 `changed`; all 78 dispositions `holds`, 0 `stale`; 0 votes.
- The nine non-`same` rows (hash, entry, v7.2 pointer → v7.3 lines):

| status | hash | entry | pointer → v7.3 lines |
|---|---|---|---|
| moved | `b50f210b822a` | oom-tracepoints-r47.md | `mm/page_alloc.c:4630` → 4689 |
| moved | `db108c1ad61c` | oom-tracepoints-r47.md | `mm/page_alloc.c:4265` → 4311 |
| moved | `eee4454705c0` | system-pressure-r24.md | `kernel-parameters.txt:5505-5507` → 5540-5542 |
| moved | `edd8b8c361b4` | system-pressure-r24.md | `cgroup-v2.rst:1215-1221` → 1240-1246 |
| changed | `02b8d2d11094` | system-pressure-r24.md | `cgroup-v2.rst:1911-1915` → 1938-1942 |
| changed | `77bd396cffd3` | system-pressure-r24.md | `cgroup-v2.rst:2171-2175` → 2202-2206 |
| moved | `9a8d29e96280` | oom-victim-selection-r27.md | `proc.rst:1811-1812` → 1812-1813 |
| moved | `07a985363937` | oom-victim-selection-r27.md | `cgroup-v2.rst:1450-1466` → 1477-1493 |
| moved | `4eea9d9f5ae5` | oom-victim-selection-r27.md | `kernel/fork.c:1768-1769,1949-1966` → 1795-1796,1976-1993 |

- Ledger: 88 lines, 78 data rows, header `source:` = S526–S534 + S516 + S502 (11 ids), `verified-at: 2026-10-27`,
  `recheck: on-release` (kernel-v7.3-recheck-r55.md:3-5, 78 rows).
- Seats that count: `Mo55Rc01`–`Mo55Rc16` only (count-c1.py:56); 2 distinct bound agreeers per row and zero
  dissent (count-c1.py:385-388, 402). Minimum 156 vote instances for 78 rows.

## C2 scope (measured, data commit)

- 23 claim rows, 9 sources S535–S543 (entry lines 3, 9-33), header cited exactly in the table (`provenance=ok`).
- Per-source claim counts: S538 5, S537 4, S540 4, S536 2, S539 2, S541 2, S542 2, S535 1, S543 1.
  Contract floor is 16 rows / 6 sources (contract.md:37), so 7 rows and 3 sources of headroom.
- Claim lengths 18–30 words; backticked quotes 6–22 words (median 11, 6 of the 23 quotes ≤8 words) — all inside
  the predicate's 6–25-word window and all located in the pinned copies (`located=23`).
- Entry structure: `source:`/`verified-at:`/`recheck:` at lines 3-5; claim table 9-33; decision table 35-47;
  host paragraph 48-50; boundaries 52-54; captured-snapshot note 56-58.
- Seats that count: `Mo55En01`–`Mo55En12` only (count-c2.py:50); 2 distinct bound entailers per claim, zero
  overclaim (count-c2.py:265-267, 271). Minimum 46 vote instances.

## Limits (named in the frozen evidence, not re-litigated here)

C1 (count-c1.py:34-41):
- The status arm proves where cited v7.2 lines now sit, or that they no longer occur verbatim; it does not prove
  the citing sentence still means the same thing. Disposition and its votes carry the meaning.
- The results binding proves the orchestrator recorded a seat of that name whose output repeats the vote line —
  not who wrote the report bytes.
- The extractor sees line pointers only; S-id-only citations are outside scope, so 78 is a floor for those four
  entries, not a census of their v7.2 reliance.
- Pins prove the bytes are what the L1 fetched; wave seats re-fetch independently.
- `changed` means the v7.2 block occurs nowhere in the v7.3 copy (count-c1.py docstring); it is a textual
  relation, not a semantic verdict.
- 26 of 78 rows (33%) cite paths whose pinned v7.2 and v7.3 copies are byte-identical (see the forced-`same`
  finding under Findings): their status is forced to `same` by construction.
- Votes are read at the measured revision only (`git show` / `git ls-tree`, count-c1.py:424-439), so uncommitted
  reports and an uncommitted settlement record count as zero.

C2 (count-c2.py:30-36):
- A located quote proves the quoted words exist in the copy; entailment is seat judgment.
- A voter's `entailed` line counts only if the voter is named in the settlement record and the exact line appears
  in the captured output (count-c2.py:154-170); an `overclaim` line needs the voter listed but not the output line.
- Authorship signal is only a correction line naming the old hash; a row's author cannot self-entail.
- No ENOSPC was observed firing; every filesystem read had free blocks and inodes; v7.3 bytes say nothing about
  this host's 7.2.11 kernel beyond a live observation.
- Quotes are 6–22-word fragments, so "located" is weaker than sentence-level support for the claim text.
- One overclaim from any listed En seat blocks that row even with two entailed votes (strict kill).

Cross-cutting:
- Nothing is met until votes are committed: `w1-results.json` is absent and every seat report in `w1/` is
  untracked (20 at first read, 44 at 06:50Z), so both counters read `voted=0` / `entailed=0` at every tested
  revision.
- Feasibility arithmetic: 156 bound C1 vote instances from 16 Rc seats (≈10 rows each) and 46 from 12 En seats
  (≈2 claims each), with zero dissent tolerance.

## Out of scope / not done

- No vote cast (scribe seat), no production edit, no git/jj mutation, no commit/push, no judge invocation.
- Counter selftests not re-run (pinned receipts, `freeze-sha256.txt:1-2`); sources not re-fetched (wave seats do).
- Working-tree changes listed in the drift finding under Findings were not made by this seat and were left
  untouched; two of them were restored by another actor during the pass.
- No host change: no sysctl/mount/cgroup write, no ENOSPC/OOM forcing, no install; pacman not invoked.

## Touched surfaces

- Wrote: this report only (`.ufo/waves/round-55/w1/Mo55Scribe03.md`).
- Scratch (removed): `/fast/scratch/hyaku/mori-r55/Mo55Scribe03` (`scope.out`, `hashes-b8b7064c.txt`).
- Read-only: contract, counters, checks, controls, evidence, ledger, entry, `corpus/SOURCES.md`, wave plan,
  registry, quarantine register, `scripts/hyaku/disk-guard.sh`.

## Findings

- **Medium (High while it existed) — a frozen-evidence input was transiently edited in the working tree.**
  First `git status --porcelain` (≈06:41Z, HEAD `b8a70adf`) showed ` M SCORECARD.md`, ` M corpus/QUALITY.md`,
  ` M corpus/lessons/round-55.md`, ` M corpus/knowledge/disk-runway-enospc-r55.md`. The C2 entry edit at
  `corpus/knowledge/disk-runway-enospc-r55.md:14` rewrote row 4's claim cell and replaced its quote (claim and
  quote both reworded), hashing to `45120996891a` instead of the committed row's `22a23e3fb849` (reproduced from
  `evidence/c2-claims.txt` row=4 and from `count-c2.py --hashes b8b7064c`). Had that text been committed inside
  the measured revision, every row-4 vote bound to `22a23e3fb849` would become unbound and the claim list would
  diverge from `evidence/c2-claims.txt`. Re-read at 06:50Z: that entry and `corpus/lessons/round-55.md` are back
  at their committed bytes, while ` M SCORECARD.md`, ` M corpus/QUALITY.md`, ` M corpus/lessons/round-54.md`
  remain modified. HEAD did not move and `git diff b8b7064c..HEAD` touches only `w1-dispatch.json`,
  `w1-input.json`, `w1-plan.json`, `w1.ready`, so no C2 damage landed; the finding is the transient edit of a
  frozen-evidence input by an actor that is not this seat.
- **Medium — C2 prose host numbers are not reproducible from the captured snapshot.** Entry
  `corpus/knowledge/disk-runway-enospc-r55.md:50` states `/tmp` free 32,795,798 / free inodes 67,005,211,
  `/fast` free 147,466,003 / free inodes 417,090,444, `/` free 164,023,017 / available 154,680,289; line 58
  calls the captured snapshot "the immediately reproducible point-in-time values", but
  `evidence/host-disk-snapshot.txt:3-6` records `/tmp` 32,795,553 / 67,004,121, `/fast` 155,927,507 /
  418,617,687, `/` 164,012,985 / 154,665,001. All three differ (the `/fast` gap is ≈8.4M blocks). These numbers
  are prose, not counted subclaims (contract.md:34-35), so no vote is affected, but the stated reproduction
  claim does not hold against the committed capture.
- **Medium — a third of C1 rows are structurally forced to `same`.** 26 of 78 rows cite paths whose pinned
  v7.2 and v7.3 copies are byte-identical: `mm/oom_kill.c` (14 rows, sha
  `452f1348…` == `452f1348…`, `corpus/evidence/sources-r50/oom_kill.c.v7.2` vs
  `corpus/evidence/sources-r54/oom_kill.c.v7.3`), `Documentation/accounting/psi.rst` (9 rows, `11c6b712…`,
  `freeze-sha256.txt`), `include/trace/events/oom.h` (2 rows, `82f04ad4…`), `include/linux/psi_types.h`
  (1 row, `483269b2…`). For those rows the status arm cannot detect drift; their `same` disposition rests
  entirely on the Rc seats' meaning judgment and on the pins being the true v7.3 bytes.
- **Medium — vote arms are asymmetric and settlement-coupled.** C1: a differing final word from any listed voter
  counts as dissent from the report alone, while agreement counts only when the same line is bound into
  `w1-results.json` output (count-c1.py:284-305, 385-388). C2: any `overclaim` from a listed voter blocks a row
  even against two `entailed` votes (count-c2.py:265-271). All vote material is read through `git show` at the
  measured revision (count-c1.py:424-439, count-c2.py:297-312), so reports and the settlement record must be
  committed at that revision; seat reports remain untracked (20 at first read, 44 at 06:50Z) and
  `w1-results.json` is absent, hence `voted=0` / `entailed=0`.
- **Low — committed "at data" receipts name an older revision.** `evidence/c1-at-data.txt:1` and
  `evidence/c2-at-data.txt:1` carry `rev=f70051ddcb903dc6c4393c410f8bab054951af82`, not the data commit
  `b8b7064c`. Re-running both counters at `b8b7064c`, `51ebd3d3`, `f70051dd` and HEAD yields byte-identical
  count fields (only `rev=` differs), so the numbers stand; the label is what is stale.
- **Low — C2 evidence density is uneven.** Two of the nine sources carry one claim each (S535, S543) and 6 of 23
  quotes are ≤8 words (entry lines 9-33). Inside the predicate, but a reader should not treat one-claim sources
  or fragment quotes as independent corroboration.
- **Info — gate surfaces are clean at measurement.** 35/35 frozen pins `OK`; `--scope` extraction reproduces
  `evidence/c1-scope.txt` exactly; claim-hash list reproduces `evidence/c2-claims.txt` exactly; census start and
  end both `exit=0`; disk guard `exit=0` with 594.6G free on `/fast`, so no ENOSPC condition was approached.
