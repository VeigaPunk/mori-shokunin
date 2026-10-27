# Round 54 lesson

Entering tip `39dcf4d7e410d362781a47e8365ca23b5c807598` (round-53 closure, admitted); freeze
`6830f3af992d906bfa1e17e3743e631ab834f67c` (contract, two counters, controls and frozen receipts); data
`1116c092ddf39819bb5b23093814552936cf224f`; pre-wave correction `78295c764093ff1f6cee08d7246679900bde7265`;
wave spec/data receipt commit `2d0347a32b6befd7fd946a83319e04f6d8f004b9`; post-wave claim correction
`782c6e7dabdb913ab01119707aaf57bf064a50fe`; C2 row-4 correction `c71d088a94b5992d74c2780fde1a7ac267a9b732`.
L1 MoriR54, attempt 1. Claims: C1 freshness — the 31 remaining Linux-v7.2-pinned `claim|source|quote` rows at v7.3,
with the v7.3 quote-start line and RECHECK dispositions; C2 depth — hardware memory-failure kills and their
observable counters/tracepoint, a kill-event class outside the OOM-victim path. One v2 wave `w1` (74 seats) ran
after the data commit; its `w1-results.json` records all 74 outputs. Claim receipts are under
`.ufo/waves/round-54/evidence/`.

## Gate

### New SOURCES rows (opened this round; rule 1)

S515–S524 are ten tier-A rows, opened 2026-10-27, status `mined`, `on-release`, used by one or both round-54
entries; S525 is an opened tier-A code row with status `rejected`. The six C1 release copies are under
`corpus/evidence/sources-r54/` (the two reused v7.3 copies S508/S514 remain under `sources-r53/`); the four new C2
copies are there too. Full hashes, exact line ranges, and current registry values are in `corpus/SOURCES.md`.
Quotes below were located in those committed copies with a whitespace-collapsed substring check; date is the
L1's access date, not a seat/package date.

| id | URL / locator | accessed | ≤25-word located quote | decision |
|---|---|---|---|---|
| S515 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/mm/memcontrol.c?h=v7.3 — copy `sources-r54/memcontrol.c.v7.3` | 2026-10-27 | `pr_info("memory: usage %llukB, limit %llukB, failcnt %lu\n",` (7 words; line 1819) | admit, tier A code |
| S516 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/mm/oom_kill.c?h=v7.3 — copy `sources-r54/oom_kill.c.v7.3` | 2026-10-27 | `/* one line summary of the oom killer context. */` (10 words; line 446) | admit, tier A code |
| S517 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/lib/percpu_counter.c?h=v7.3 — copy `sources-r54/percpu_counter.c.v7.3` | 2026-10-27 | `if (unlikely(abs(count + amount) >= batch)) {` (7 words; line 100) | admit, tier A code |
| S518 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/linux/percpu_counter.h?h=v7.3 — copy `sources-r54/percpu_counter.h.v7.3` | 2026-10-27 | `static inline s64 percpu_counter_read_positive(struct percpu_counter *fbc)` (6 words; line 118) | admit, tier A code |
| S519 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/uapi/asm-generic/errno.h?h=v7.3 — copy `sources-r54/errno.h.v7.3` | 2026-10-27 | `#define EDQUOT 122 /* Quota exceeded */` (7 words; line 107) | admit, tier A code |
| S520 | https://docs.kernel.org/7.3/admin-guide/cgroup-v2.html — copy `sources-r54/cgroup-v2.7.3.html` | 2026-10-27 | `The number of processes belonging to this cgroup killed by any kind of OOM killer.` (15 words; rendered text, line 1225) | admit, tier A docs; release-pinned path, footer fact is the sidebar blurb, not the footer |
| S521 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/mm/memory-failure.c?h=v7.3 — copy `sources-r54/memory-failure.c.v7.3` | 2026-10-27 | `pr_err("%#lx: Sending SIGBUS to %s:%d due to hardware memory corruption\\n",` (10 words; line 292) | admit, tier A code |
| S522 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/mm/hwpoison.rst?h=v7.3 — copy `sources-r54/hwpoison.rst.v7.3` | 2026-10-27 | `Send SIGBUS when the application runs into the corrupted page.` (10 words; line 68) | admit, tier A docs |
| S523 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/ABI/stable/sysfs-devices-node?h=v7.3 — copy `sources-r54/sysfs-devices-node.v7.3` | 2026-10-27 | `The total number of raw poisoned pages (pages containing corrupted data due to memory errors) on a NUMA node.` (19 words; line 196) | admit, tier A docs |
| S524 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/trace/events/memory-failure.h?h=v7.3 — copy `sources-r54/memory-failure-trace.h.v7.3` | 2026-10-27 | `For historical versions, memory_failure_event is in ras subsystem,` (8 words; line 4) | admit, tier A code |
| S525 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/ras/ras_event.h?h=v7.3 — copy `sources-r54/ras_event.h.v7.3` | 2026-10-27 | `#define TRACE_SYSTEM ras` (3 words; line 7) | reject: `memory_failure_event` is not defined in this file at v7.3; it lives at S524. Flip if the v7.3 file defines the event. `grep -c` receipt: `evidence/gate-rejects.txt` |

Rejected access route (not a registry row): jsDelivr `@v7.3` returned HTTP 403 on some files and 200 on others; this is path-scoped, not a site-wide rejection. The unpinned `docs.kernel.org/.../latest` page still renders 7.3.0, but is mutable; S520 uses the release-pinned URL. Round-53's lead about `panic_on_unrecoverable_memory_failure` is opened as S507/S521 and admitted through the C2 entry.

### Rows touched old→new

- S502 used-by: `kernel-v7.3-recheck-r53.md` → that path plus `memory-failure-kills-r54.md`.
- S507 used-by: `kernel-v7.3-recheck-r53.md` → that path plus `memory-failure-kills-r54.md`.
- S508 used-by: `kernel-v7.3-recheck-r53.md` → that path plus `kernel-v7.3-recheck-r54.md`.
- S514 used-by: `commit-runway-read-r53.md` → that path plus `kernel-v7.3-recheck-r54.md`.

Other row corrections from wave review are **not** written in place (SOURCES contract v1 append-only): S520's opened
row still says its version marker is in the footer (the 7.3.0 blurb is in the sidebar), its quote-lines list omits
the second S520 occurrence at 1636; S508's original anchor omits the newly used `vm_memory_committed` line 937.
These are routed to round 55 as superseding rows if still needed; the existing first-published cells are unchanged.

### Assimilation and quarantine

Assimilation: none — `merge/mori/` has no files on the C1 kernel-v7.3 claim ground or the C2 hardware-memory-failure ground. The freeze broad sweep recorded 0, but re-running it found three quota/EDQUOT files; the narrowed C1/C2-topic sweep found 0. See `evidence/assimilation-sweep-correction.txt`: the discrepancy is disclosed, and no package file was adopted.

The full mori absent-defect slice was 3 rows (`assimilation/quarantine-slice`). S244 remains **unverifiable**, not fabrication: the DOI/Crossref metadata opened, the ACM page returned 403, and the register had no quote/locator to compare. S262 and S268 are **present** in the publisher's ROMA PDF, fetched 2026-10-27 with a browser User-Agent (2,357,114 bytes, sha256 `1603404dd25b3a0dff93f2dcb23c75b671d4e2d78da3cce8f461e87ebde6add2`): S262's abstract sentence is at printed page 3015, extracted lines 17–22; S268's tracepoint example is at printed page 3016, extracted lines 121–126. Full adjudication and quotes are in `assimilation/quarantine-verdicts.txt`. No campaign file was edited.

### Spot-check

Pending independent non-author closure. The wave seats are the lane and do not count as an outside spot-check. Candidate decisions: admit S521 (the SIGBUS/recovery handler code) and reject S525 (the v7.3 `ras_event.h` header has no `memory_failure_event`).

## Mistakes

| class | evidence pointer | captured-by | fix / shown able to fail |
|---|---|---|---|
| number-drift | Round-53 closure D2: SCORECARD After cells cited at-salvage while report measured at-landed; round-50 rows had the same stage mismatch (`SCORECARD.md` correction paragraphs; `w1/Mo54RevengerD2.md`) | QUALITY 148 | `receipt-stage.py 39dcf4d7` flags 5 intermediate citations; after appended correction paragraphs it must print `flagged=0` (receipt committed with the report) |
| landing / stale strays | Round-53 closure D3; eight files were relocated to lane-root paths by r28/r38, then stayed there (`evidence/d3-relocation.txt`) | QUALITY 149 | byte-exact copies and `cmp` receipts moved the 8 files under `round-28/misroot-lane-root/` and `round-38/misroot-lane-root/`; `git ls-tree` before lists 8, after lists 0; empty untracked `--repo/` removed |
| overclaim / reference drift | Initial C2 rows 1, 4, 5, 7, 10, 11, 12, 16, 20, 21 received reviewer/critic overclaim votes (`w1/Mo54En*.md`); row 4 required a second re-vote after “only” was still too broad | QUALITY 128 (location is not entailment) | The L1 narrowed claims and re-ran the exact hashes; every final row received ≥2 distinct entailed votes and zero final overclaim votes at the committed w1 reports. The original wrong wording is retained in vote reports; the frozen counter's count/source arms stayed unchanged. |
| wrong locator / rejected header | L1 first selected `include/ras/ras_event.h` for the event; memory-failure.c includes `include/trace/events/memory-failure.h` (`evidence/gate-rejects.txt`) | SOURCES rejection S525 | `grep -c 'TRACE_EVENT(memory_failure_event' ras_event.h.v7.3` → 0; same check on the correct S524 header → 1. S525 remains rejected, no wrong row admitted. |
| stale quarantine disposition | `absent-defect-register.md` classified S262/S268 “could not be fetched” (`assimilation/quarantine-slice`); later publisher PDF S478 existed but the quarantine slice had not been re-opened | none | Round-54 re-fetched the PDF and located both quotes; S244 remains unverifiable. The old register was not edited; the round lesson/report holds the verdicts. |

## Wave w1 — integrated findings

One v2 wave, 74 seats: reviewer 19, critic 18, executor 15, scribe 9, scout 4, sentinel 3, mutation-tester 2, connector 2, revenger 1, simplifier 1. Attack seats: 39/74 (reviewer+critic+mutation-tester), above the 25% floor. Voters: 12 RECHECK + 12 ENTAILMENT. `w1-results.json` has 74 outputs; one output (`Mo54RevC1Counter`) is malformed coordinator text and has no report file; four other seats also lack report files but have structured output in results. No seat was re-spawned. The dispatcher result contains no status or last-error field, so the round does not infer a provider death from those omissions. No tool installs or upgrades; pacman stayed paused. No LSP server was available to the seats (text/source review only).

- C1: all 31 scoped rows held at v7.3; line-start checks match 31/31; six new/reused source rows pass provenance/pins; 31/31 dispositions have two+ distinct settled voters, zero dissent. Four other release-triggered artefacts remain outside the exact `claim|source|quote` scope: `oom-tracepoints-r47.md`, `system-pressure-r24.md`, `watchdog-identity-r31.md`, `oom-victim-selection-r27.md`; the report names this boundary. Ten rows rest on byte-identical copies; status/disposition is not discriminating on those rows.
- C2: 21/21 located rows over six sources; ≥2 settled entailment voters per final hash; no dissent. Ten initial row hashes changed after overclaim votes; a second row-4 hash was judged before landing. The counter's own result binding checks only the orchestrator result `name` and committed report filename; it does not cryptographically prove which seat wrote those bytes. A malicious fixture results file can fabricate distinct voter names — a named counter limit for round 55. No memory-failure event was observed live; host counters are all zero.
- Controls: do-nothing/copies-only, no-vote, unsettled, no-line, v7.2-copy, quote-echo, unlocated, two-source and synthetic witness receipts were measured before data. They were generated in throwaway clones, but the clones/commits were removed by the runner; 12/14 control clone revisions cannot be resolved later (`w1/Mo54SentReceipts.md` F2). The committed first-run receipts remain recorded observations, not re-creatable revision proofs. Do not overstate this control evidence.
- Main independently replayed the frozen counters/selftests at the final measured revision (receipts named in the report). Selftests: C1 57/57, C2 54/54. Sources census at start: exit 0, 23 W04; at end: exit 0, 23 W04. The broad assimilation sweep discrepancy is in `evidence/assimilation-sweep-correction.txt`.
- No-harm reviewer: coverage, operability, depth, freshness, calibration and adjacency not harmed; only one low ledger-prose concern (S491 anchors in `oom_kill.c` did not move) was checked and corrected in the movement table.

## Per-axis and learning verdicts (L1; outside admission pending)

| item | verdict | evidence |
|---|---|---|
| freshness (C1; one lowest axis) | improved | 31 remaining v7.2 claim-table rows re-derived at v7.3; 31 line-starts, 31/31 final votes, source pins all valid; `count-c1.py` receipt |
| depth (C2; lowest axis) | improved | a new decision-table entry for the previously unheld non-OOM memory-failure kill class, 21 located claims over six sources, 21/21 final entailment |
| coverage | unchanged | new knowledge entry, no tool/core coverage surface claimed |
| operability | unchanged | no new executable capability claimed |
| calibration | unchanged | no scalar self-assessment score changed; remaining counter identity limit disclosed |
| adjacency | unchanged | read-only boundary preserved; host repair and MCE/EDAC remain outside the entry |
| expansion | improved | new admitted knowledge ground and 10 new mined sources; no package adoption |
| quality | improved | 31 old-tag claims rechecked, line movement documented; C2 overclaims corrected before score and no known false claim left unmarked |
| discernment | unchanged | independent admit/reject spot-check is still pending; wave voters are the lane |

Assimilation: none. Tool installs: none. L0 questions: none. Stale-lane: respawn-per-round driver; no other mission is open.

## Round-55 append-only errata (outside spot-check D1–D6)

### M1 — number-drift (QUALITY 148)

The round-54 `Mistakes` row at original line 67 is the number-drift mistake cited by QUALITY 148; the prior `#M1` locator did not exist. Its check and result remain as written: `receipt-stage.py 39dcf4d7` flagged 5 intermediate receipts before correction and `flagged=0` afterward.

### M2 — landing / misroot strays (QUALITY 149)

The round-54 `Mistakes` row at original line 68 is the misroot mistake cited by QUALITY 149; the prior `#M2` locator did not exist. The byte-exact relocation and root-list check remain the evidence; QUALITY 149's pointer now resolves to this heading.

### Gate locator corrections (D2)

The original Gate table lines are retained, but these four locations were wrong: S515's quote starts at `sources-r54/memcontrol.c.v7.3:1850` (not 1819); S520's quote is at rendered line 1409 (not 1225); S522's quote starts at `sources-r54/hwpoison.rst.v7.3:70` (not 68); S525's quote starts at `sources-r54/ras_event.h.v7.3:3` (not 7). S524 is the distinct row at line 7.

### Remaining routed corrections (D1, D3, D5)

- D1: `evidence/census-end.txt` is a transcription, not the validator's captured bytes; its S349 URL is also wrong. The source file and live validator use `...%E6%8A%80%E6%9C%AF%E7%99%BD%E7%9A%AE%E4%B9%A6.pdf`, not `...%E7%99%BD%E6%96%87%E6%9C%AC.pdf`. Round 55 captures its own census stdout/stderr and exit code mechanically; the old receipt is not rewritten.
- D3: the Round 54 limits paragraph at original line 87 says “Ten control clone revisions”; the measured observation is 12/14 unavailable. The scorecard correction is appended in Round 55; this historical line is retained.
- D5: round-54 `w1-results.json` has 74 results and the committed `w1/` directory has 73 `.md` reports; only `Mo54RevC1Counter` lacks one. The previous “four other seat reports are absent” statement is incorrect.

### Gate observation

The outside review found the four locator defects above and the decision-table panic overclaim (corrected append-only in `memory-failure-kills-r54.md` and `SKILL.md`). Round-54's historical source decisions remain as filed; this erratum does not rewrite them.
