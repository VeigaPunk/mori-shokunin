# Round 12 — mistakes mined since round 11

date: 2026-10-19 · lane: mori-shokunin · lane base: `20e2255` (2026-10-17T00:28:33-03:00)
· record: the round-12 LOG block `## 2026-10-19 — round 12: named corrections owed since round 11`
appended with this lesson; L1 (W2RoundMori) appends the round's main entry.

Method: mined from `mori-state.md` §4 (M1–M17) and `mori-art.md` §7 (M1–M6), deduplicated;
then re-mined `LOG.md`, `SCORECARD.md`, `corpus/knowledge/audit-r11.md` and the reports for
classes the dossiers did not carry. Every LANE pointer was re-resolved on 2026-10-19 at
`20e2255` plus L1's in-flight round-12 working-tree edit; corrected pointers are marked in
the evidence column and listed in **Pointer re-verification** below. Dossier-only pointers
(§-anchored rows in the read-only dossiers, and source rows S001–S030) were re-read at their
dossier lines; web sources were not re-fetched, and those cells say so.

`captured-by` names the QUALITY.md criterion number that exists **after** this round's
append, a SKILL.md row, or `none` with the reason in `fix`. `SKILL.md:<n>` pointers in this
lesson are line numbers at base `20e2255`; round 12's own SKILL edits moved some of them
(e.g. the `unavailable` checklist rule `:51` → `:54`, the credential rule `:46` → `:49`).

## Mistakes

| # | class | evidence pointer (path:line or command → output) | captured-by (QUALITY criterion number, SKILL.md row, or none) | fix |
|---|---|---|---|---|
| M1 | A claim was over-stated and then narrowed at admission (5 of 10 rounds) | `SCORECARD.md:229-235` (r4), `:265-273` (r5), `:310-318` (r6: "at the first revision the claim did NOT hold"), `:413-422` (r8), `:546-560` (r11); `grep -cE '^\*\*Verdicts\.\*\* ADMIT-with-correction' LOG.md` → 5 | 25 | Admit at the measured scope; record the narrowing as a named correction, not a silent edit. |
| M2 | A crash exit code equals the DRIFT verdict code under errexit/pipefail | `LOG.md:212`; `tools/mori-census.sh:1366-1374` still pipes `printf … sed … grep -Fxq` (F01, open); lesson `2026-10-15-errexit-pipefail-silent-crash.md:24-25` | 6 | Every probe pipeline rc-gated; a reserved setup code; an unreadable-input canary per probe. |
| M3 | A producer killed by SIGPIPE is scored as "no match" | `LOG.md:438-442` (harness flake 1/8–25%); lesson `2026-10-15-selftest-grep-sigpipe-race.md:202-203` (141 ≠ 1); r10 acceptance also read drift through a pipe (`SCORECARD.md:556-560`) | 7 | Capture once, then match (here-string); no live producer pipe into `grep -q`. |
| M4 | An oracle the SUT can observe or replay is forgeable | lesson `2026-10-15-forgeable-oracle-visible-fixtures.md:32-38` (sniffer 27/27); current F02 `corpus/knowledge/audit-r11.md:157` (BANANA wrapper 28/28). The state dossier's `LOG.md:315-320,346-351,376-382` pointers are r4–r6 verdict paragraphs, not this evidence — corrected here | 8 | "Cannot fake" claims list the channels tested; untested classes are named residuals; keep a forgery probe. |
| M5 | Pointers rot and corrections are not swept | At `20e2255`: `SKILL.md:75` "56 → 65" (receipts: `grep -ohE 'PASS \(66 cases' corpus/evidence/*.log` → 2 lines), `:78` `…T2210Z.json` (`test -e corpus/evidence/baseline-r10-20261015T2210Z.json` → absent), `:107-108` `tsukuroi/PROVINCE.md:16-17` and `kama/PROVINCE.md:22-26` (quotes now at `:19` and `:45-47`); F04: `ls corpus/evidence` counts 190229 → 0, 190453 → 0, 191216 → 7 | 9 | Resolve every pointer at the carrying commit; land replacements with a sweep of every mention; a report names its delivered commit. |
| M6 | Cited tallies disagree with the delivered artifacts | `SCORECARD.md:429` says "eight r8 receipts"; the delivered r8 count is 7 (`ls corpus/evidence`); `:511` "seven receipts + the baseline" vs 6 r10 files (5 logs + 1 baseline); `:410-411` "exactly the 4 new names" vs fixture diff 9 / live diff 4 (`corpus/knowledge/surfaces-r8.md:203-204`) | 20 | Recompute every count from the delivered set at the carrying commit. |
| M7 | A fifth verdict value ("improved narrowly") | `grep -c 'improved narrowly' SCORECARD.md` → 9 (cells `:114,115,173,226,281,327,377,427,429`); admitted vocabulary `AXES.md:79` | 21 | Put qualifications in the evidence cell; verdict cells use the four admitted values. |
| M8 | Admission timestamps are later than their carrying commits | `SCORECARD.md:211,258-259,350-351` labels 17:55Z/18:30Z/20:10Z vs commit clocks 17:53:05Z/18:28:43Z/20:06:34Z (`git show -s --format='%h %cI' 7a3629a 848b3a6 ed9de46`); r9 report `:26` 21:50Z vs `6a549b9` 21:48:43Z | 22 | Timestamp ≤ carrying commit; rounded labels are marked estimates. |
| M9 | Scratch (/tmp) evidence cannot be recreated | `SCORECARD.md:550-554` 140/275 fingerprints not recomputable; `find . -name 'expected*.json' -not -path './.git/*'` → 0; F14 `corpus/knowledge/audit-r11.md:169` | 23 | Commit the fixture generator plus a digest; a `/tmp` path is never evidence. |
| M10 | Discernment was self-attested | `SCORECARD.md:573-575` "externally probed by the critic-of-the-audit seat" vs `LEARNING.md:42-43` "A subagent the lane dispatched is still the lane."; `grep -lE 'spot[- ]check' corpus/lessons/*.md` → no output, rc 1 (0 files) | none | Protocol-level: the named non-author spot-check belongs in the `## Gate` section L1 appends; same-seat attestation cannot move the trend. |
| M11 | A change landed with no LOG entry | `git show --numstat --format='%h %s' 20e2255` → `.gitignore 1/0`, `SKILL.md 70/4`, no LOG.md hunk; rule `AGENTS.md:4`; F10 inherited dirty SKILL (last commit `1439c47`) | none | Protocol-level: every commit carries its LOG hunk; this round's block records `20e2255`. |
| M12 | Seat status ≠ artifact | `LOG.md:61-65` (status failed while a 19 KB report landed); `:250-255` (8 seats lost to a content-filter 400); F13 `corpus/knowledge/audit-r11.md:168` | none | Protocol-level/domain knowledge: settlement = artifact + status (candidate K5); the SKILL rows at `:16,27` cover wave settlement, not seat status, so no criterion exists and none is invented. |
| M13 | A journal class was counted from text instead of a structured field | `LOG.md:38-44`: text grep 0 segfaults vs `COREDUMP_SIGNAL` 656; `:67-71`: signal 5 vs 11; art M2 (OneUptime recipe repeats it) | 15 | Count by `MESSAGE_ID` or another trusted field when one exists; never message text. |
| M14 | An unknown was collapsed into a negative | `LOG.md:46-53` (missing `pgrep` read as a dead daemon); `SKILL.md:51`; D05/D06 `corpus/knowledge/audit-r11.md:200-201` | SKILL.md:51 | A missing surface is `unavailable`, never unhealthy. |
| M15 | Baseline aging was realized; re-pin is not a recorded act | `LOG.md:490-493` named the risk; today `bash tools/mori-census.sh --drift corpus/evidence/baseline-r10-20261015T2231Z.json` → `MORI_DRIFT: …` rc 1 (11 tokens); baseline `:3` pinned 2026-10-15T22:26:29Z; `uptime -s` → 2026-10-19 08:11:44 -03:00 | 10 | A baseline declares its volatile set and window, host and gate SHA; re-pin is recorded with a reason, never to turn red green. |
| M16 | A blocked attempt (honest stop) must not earn credit | `LOG.md:100-178` round-2 blocked attempt; `SCORECARD.md:32-95` "Verified lane rounds remain 1", "one blocked attempt" | none | Protocol-level: no artifact, no score movement; recorded as evidence of taste. |
| M17 | Sibling hygiene empties the observation surface | `git -C /home/vgpnk/Projects/shokunin show --stat e20f4fa` → 17 `waves/aggregator-r10*` paths deleted; baseline `:26-27` counts both as unsettled; live counts them `empty` | 24 | Disclose an emptied surface as empty-by-removal, never as never-written. |
| M18 | A lexical sweep false positive without word boundaries | bare `cursor` matched 3 files; `\bcursor\b` matched 0 (`grep -rliE … corpus --include='*.md'`, art M1) | 19 | Inspect nonzero hits before citing the count; use word boundaries. |
| M19 | Notice ≠ event, and scopes were summed | host fact `mori-art.md:20`: 5 kernel kills vs 7 user + 9 system `fe6faa94…` notices, same boot | 16 | A kill count names its unit (kill vs notice) and scope; scopes are never summed. |
| M20 | Doc wording was read wider than the increment site | S002: "any kind of OOM killer" (`mori-art.md:96`) vs S003 `:935-936`, the single increment site (`mori-art.md:97`) | 14 | Counter semantics cite the increment site, not only the doc line. |
| M21 | A detection recipe was silent about delivery paths it cannot see | S020 probes only `kill/tkill/tgkill` syscalls (`mori-art.md:114`); S011 `:274` kills through `cg_kill_kernel_sigkill` with a `kill()` fallback (`mori-art.md:105`); eBPF terms in the corpus → 0 (§1b) | 17 | Every detection recipe states which delivery paths it cannot observe. |
| M22 | Post-hoc attribution by re-reading a dead cgroup | `corpus/knowledge/observability-census-r1.md:143-144` "cgroup path now `ENOENT`"; art M6 | 18 | Attribute from records written at event time, never from the victim's re-read cgroup. |
| M23 | A delivery report cites the entering baseline, not its own work | `.ufo/reports/round-2/mori-goalwave.md:5` names `e30b2e3`; the work lands at `3da8414` (`git log --diff-filter=A --format='%H %cI' -- .ufo/reports/round-2/mori-goalwave.md`) | 9 | A report names the commit that carries the reported work; entering state is labeled separately. |
| M24 | SHENON box lines were collapsed | F06 `corpus/knowledge/audit-r11.md:161`; awk box count: r2 4, r3 4, r4 4, r5–r10 1 each (6/9 affected); e.g. `.ufo/reports/round-10/mori-goalwave.md:45-47` | none | Protocol-level report format: one `- [ ]` line per box. |
| M25 | An environmental abort was tallied as a case result | F13 `corpus/knowledge/audit-r11.md:168`: exit 1, 44 PASS, no tally, `printf: write error: Disk quota exceeded`; D21 | 6 | A setup abort never borrows a verdict code (exit 2) and is neither a case PASS nor FAIL. |
| M26 | "Malformed baseline is rejected" was claimed beyond the validator | F09 `corpus/knowledge/audit-r11.md:164`; today: control drift rc 1 with tokens, headerless copy rc 1 with the same tokens, junk rc 2 `baseline malformed (canonical marker absent)` | 8 | Negative guarantees name the inputs tested; a format contract precedes the claim. |

### Notes on rows

- **Rows without a dossier parent.** M23 (F07), M24 (F06) and M25 (F13) are re-mined from
  `audit-r11.md` §4; the two dossiers' mistake tables do not carry them. M1 and M16 are the
  named "narrowed claims" and "honest-stop r2" classes; they are present in `mori-state.md`
  §4 and are kept here because the ART dossier's §7 omits both.
- **Deduplications.** `mori-art.md` M2 (text grep vs structured field) merges into state M13;
  state M1 absorbs "narrowed claims"; state M16 absorbs "honest-stop r2". All other state
  M1–M17 and art M1–M6 rows appear once.
- **Open defects referenced, not relabelled as fixed.** F01 (`tools/mori-census.sh:1366-1374`)
  and F02 (oracle verdict-line validation) remain open at the audited bytes; the row says so.

## Pointer re-verification (2026-10-19, lane base `20e2255`)

Re-resolved every LANE pointer cited above. Drifted or wrong pointers, with the correction
used in the table:

| dossier pointer | observed at `20e2255` | corrected pointer / value |
|---|---|---|
| state M4: `LOG.md:315-320,346-351,376-382` | r4/r5/r6 `**Verdicts.**` paragraphs; no forgeability detail | `2026-10-15-forgeable-oracle-visible-fixtures.md:32-38`; F02 `audit-r11.md:157` |
| state M5: `SKILL.md:75` "56 → 65 cases" | `git show HEAD:SKILL.md:75` reads "56 → 65"; committed receipts: `grep -ohE 'PASS \(66 cases' corpus/evidence/*.log` → 2 | 66 cases; L1's in-flight round-12 edit reads "56 → 66" (measured working tree) |
| state M5: `SKILL.md:78` `baseline-r10-20261015T2210Z.json` | `test -e …2210Z` → absent; `sha256sum …2231Z` → `0993b235…` | `baseline-r10-20261015T2231Z.json`; L1's edit names it (working tree) |
| state M5: `SKILL.md:107-108` `tsukuroi/PROVINCE.md:16-17`, `kama/PROVINCE.md:22-26` | tsukuroi quote at `PROVINCE.md:19`; kama write boundary at `:45-47` (main checkouts, 2026-10-19) | `:19` and `:45-47`; L1's edit carries them (working tree) |
| state §3: "9 lanes graded" and 9 `SURFACE lane.*` rows | live-census claim of 2026-10-19T21:05Z, not re-run in this seat | left as the dossier's measured value; the roster seat owns the live count |
| state M6: `SCORECARD.md:429` "eight r8 receipts" | confirmed verbatim; `ls corpus/evidence` r8 count 7 | seven; F05 |
| state M7: audit F08 cell list | `grep -c 'improved narrowly' SCORECARD.md` → 9; cells confirmed at the listed lines; exact-cell recount today: improved 24 / improved narrowly 9 / unchanged 27 | nine cells; the audit's 22/23 recount used a narrower exact-cell match — the violation count (9) is unchanged [INFERENCE on the regex difference] |
| state M8: `SCORECARD.md:211,258-259,350-351` | 17:55Z / 18:30Z / 20:10Z confirmed; commits 17:53:05Z / 18:28:43Z / 20:06:34Z | labels are estimates; commit clocks are the correct times |
| state M15: `LOG.md:490-493` | confirmed: "red drift may be baseline aging; re-pin policy documented" | today's drift read is red: 11 tokens, rc 1 |
| state M17: souji `e20f4fa` | `git show --stat` → 17 `waves/aggregator-r10*` paths deleted | confirmed |
| state M12: `SKILL.md:16,27` as capture | those rows cover wave settlement (registry present / no results) | not a capture of seat-status semantics; row M12 records `none` with the protocol-level reason |
| state M14: `SKILL.md:51` | confirmed: "A missing surface is reported as `unavailable`, never as unhealthy." | unchanged |
| art S002/S003/S011/S019/S020 rows | `mori-art.md:96,97,105,113,114` confirmed | unchanged (dossier-measured; sources not re-fetched) |
| art M1 lexical sweep | bare `cursor` → 3 files; `\bcursor\b` → 0 | confirmed |

Sweep for the dead baseline name: `grep -rl '2210Z' --exclude-dir=.git .` → 11 files. Four are
active or index-bearing (`corpus/knowledge/drift-pin-r10.md`, `corpus/README.md`,
`corpus/knowledge/audit-r11.md`, this lesson's parent lesson); seven are historical round-10/11
seat drafts. `drift-pin-r10.md` and `corpus/README.md` are outside this seat's write scope and
are routed through the LOG correction block; historical drafts are left as history.

## Gate

Round-12 admission gate (lane L1, 2026-10-19). Bar: `corpus/QUALITY.md` criteria 1–25.
Discernment check: **pending** — the lane's own reviewer/critic seats are the lane; the
non-author spot-check (≥1 admit, ≥1 reject) is the orchestrator's after landing and is recorded
here by the next round as `agree`/`disagree` with a reason.

### Candidates → decision

| candidate | origin | decision | reason (criterion) |
|---|---|---|---|
| oom-kill counter is kernel-only | ART K1 | **admitted** → `knowledge/oom-kill-counter-kernel-only-r12.md` | increment site re-derived (S003 :935-936, S004 :4966) — Q14; delivery paths named — Q17 |
| kill classes by MESSAGE_ID; notice ≠ kill | ART K3 | **admitted** → `knowledge/kill-classes-by-message-id-r12.md` | catalog ids re-derived (S013 :66/:604/:884); 5 kills vs 7+9 notices re-measured — Q15, Q16 |
| kernel OOM record carries attribution | ART K2 | **admitted** → `knowledge/kernel-oom-line-attribution-r12.md` | S003 :447/:452/:945, S004 :1820/:1825; 5 records dated 2026-10-18 MESSAGE-free — Q18 |
| userspace killers bypass the counters | ART K4 + earlyoom | **admitted** → `knowledge/userspace-oom-killers-r12.md` | S011 :269/:306; inactive → `unavailable (inactive)`; tsukuroi overlap cited, OS state deferred — Q17 |
| roster = declared lanes ∪ driver counters | STATE K2 | **admitted** → `knowledge/roster-truth-r12.md` | three sets measured (9 / 20 / 21 → union 23); census change gated by selftest 77/77 + oracle 28/28; critic-found over-broad parse fixed before admission (rows only inside `LANES="…"`) |
| journal cursor new-since-pin counts | ART K5 | **rejected (deferred to Frontier FR11)** | rotation/vacuum behaviour of a stored cursor is [UNKNOWN] (lead sd_journal_get_seqnum(3) unopened); admitting it would assert an untested channel — Q8 |
| CI/CD result vocabulary for settlement | ART K6 | **rejected (Frontier FR14)** | the mapping "OOM-killed lane → `error`" is opinion; the fact (S022, six values) is kept as a `queued` row, not an entry — Q1 |
| wave-settlement hygiene interference (souji) | STATE K1 | **rejected this round (Frontier FR3; QUALITY 24)** | needs a reading rule over souji's receipts (`souji-shokunin/census/operator-sweep-20261018/approval-list.tsv`); not yet measured by the census |
| counter-namespace desync (state 2 vs ledger 11) | STATE K3 | **rejected this round (Frontier FR4)** | a census reconciliation against MANIFEST is unbuilt; fact recorded in the dossier only |
| drift aging after reboot | STATE K4 | **rejected as an entry; kept as evidence** | the classification is a dated receipt (`evidence/drift-r12-20261019T2204Z-classification.md`), not a durable claim |
| seat status ≠ artifact | STATE K5 | **rejected as an entry** | lesson row M12 only; no new measurement this round |
| eBPF kill tracing in the census (R1) · PSI trigger watcher (R2) · windowed memory.peak via reset (R3) · OTel hostmetrics as runway (R4) · learned thresholds (R5) · pidfd liveness (R6) | ART §6 | **rejected** | resident/privileged/writing instruments break "one process, no resident sampler, … live mode writes nothing" (free-lunch lesson :22-23); R5 contradicts the SKILL decision-table `Never` cell "tuning a labeled-local threshold to fit one observation" (`SKILL.md:18`) |
| OneUptime systemd-oomd blog (S030) | ART R7 | **rejected row** | tier C restatement; greps MESSAGE text where `d989611b…` is the stable key; remediation how-to — Q15 |

### SOURCES rows (contract v1 rule 1)

33 new rows (S001–S033, contiguous; the seat first filed the three extra rows as S032–S034 with S031
held by the unreachable Bash manual lead — the L1 renumbered them S031–S033 before filing, since a
lead is never a row; critic-seat finding).
Tiers A=30 B=2 C=1; status mined=11 queued=21 rejected=1. Rows touched old→new: none (all new).
Every row was re-opened on 2026-10-19 by seat R12SourcesB; digest = first 16 hex of
`curl -fsSL '<url>' | sha256sum` at access.

| id | URL | accessed | SHA256 prefix | Verbatim quote (≤25 words) | location |
|---|---|---|---|---|---|
| S001 | https://docs.kernel.org/accounting/psi.html | 2026-10-19 | `f752c8d5447760a3` | “The total absolute stall time (in us) is tracked and exported as well” | Pressure interface |
| S002 | https://docs.kernel.org/admin-guide/cgroup-v2.html | 2026-10-19 | `b478c1bae99899df` | “The number of processes belonging to this cgroup killed by any kind of OOM killer.” | `memory.events` → `oom_kill` |
| S003 | https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c | 2026-10-19 | `452f1348e79c252e` | `count_vm_event(OOM_KILL);` | `mm/oom_kill.c:935`, tag `v7.2` |
| S004 | https://raw.githubusercontent.com/torvalds/linux/c03c1a14507dfaf8b856c2608f9ac216021fc222/mm/memcontrol.c | 2026-10-19 | `bdb6159cc2378c44` | `pr_cont(",task_memcg=");` | `mm/memcontrol.c:1825`, commit `c03c1a14507dfaf8b856c2608f9ac216021fc222` |
| S005 | https://raw.githubusercontent.com/torvalds/linux/c03c1a14507dfaf8b856c2608f9ac216021fc222/include/trace/events/oom.h | 2026-10-19 | `82f04ad4108ba949` | `TRACE_EVENT(mark_victim,` | `include/trace/events/oom.h:76`, same commit |
| S006 | https://raw.githubusercontent.com/torvalds/linux/c03c1a14507dfaf8b856c2608f9ac216021fc222/include/trace/events/signal.h | 2026-10-19 | `0b6fe2f241b547b4` | “signal_generate - called when a signal is generated” | `include/trace/events/signal.h:37`, same commit |
| S007 | https://www.freedesktop.org/software/systemd/man/latest/systemd-oomd.service.html | 2026-10-19 | `56460ffb24d7ea3c` | “select a cgroup to terminate, and send `SIGKILL` to all processes in it.” | Description; systemd 262 |
| S008 | https://www.freedesktop.org/software/systemd/man/latest/oomd.conf.html | 2026-10-19 | `7b4a2c24dab78dd2` | “The hook is not intended as a way to avoid the kill, but rather as a notification mechanism.” | Prekill event; systemd 262 |
| S009 | https://www.freedesktop.org/software/systemd/man/latest/oomctl.html | 2026-10-19 | `9e31fc49328b01b1` | “Show the current state of the cgroups and system contexts stored by systemd-oomd.” | Commands → `dump`; systemd 262 |
| S010 | https://systemd.io/PRESSURE/ | 2026-10-19 | `edb10d38c4e82df0` | “Regardless of which of the three types of inodes this absolute path refers to, all three are `poll()`-able for pressure events.” | Pressure Service Protocol |
| S011 | https://raw.githubusercontent.com/systemd/systemd/v261/src/oom/oomd-util.c | 2026-10-19 | `2e94450aa337dd7d` | `r = increment_oomd_xattr(ctx->path, "user.oomd_ooms", 1);` | `oomd-util.c:269`, tag `v261` |
| S012 | https://github.com/systemd/systemd/security/advisories/GHSA-652q-wxr6-h5j6 | 2026-10-19 | `94ca1710cbaadf10` | “Local unprivileged users can terminate arbitrary local processes via a systemd-oomd IPC API due to a missing path traversal validation.” | Impact; published 2026-08-10 |
| S013 | https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in | 2026-10-19 | `e53707db7e6963b2` | “Subject: A process of @UNIT@ unit has been killed by the OOM killer.” | `systemd.catalog.in:604-605`, commit `cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af` |
| S014 | https://www.freedesktop.org/software/systemd/man/latest/journalctl.html | 2026-10-19 | `75440570fb1f7185` | “Start showing entries from the location in the journal after the location specified by the passed cursor.” | Filtering Options → `--after-cursor=`; systemd 262 |
| S015 | https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html | 2026-10-19 | `906e5d34b38913dd` | “not supposed to be parsed for metadata.” | User Journal Fields → `MESSAGE=`; systemd 262 |
| S016 | https://raw.githubusercontent.com/rfjakob/earlyoom/8477c902fce09be26e5668acba05df216871e7ae/README.md | 2026-10-19 | `b2a34e354d122fd7` | “earlyoom checks the amount of available memory and free swap up to 10 times a second” | README → What does it do; commit `8477c902fce09be26e5668acba05df216871e7ae` |
| S017 | https://raw.githubusercontent.com/bpftrace/bpftrace/59810b1b6c97ead1cdcb19de26d5a60dd9046a52/README.md | 2026-10-19 | `40e9851c90871422` | “bpftrace is a general purpose tracing tool and language for Linux.” | README introduction; commit `59810b1b6c97ead1cdcb19de26d5a60dd9046a52` |
| S018 | https://github.com/bpftrace/bpftrace/releases | 2026-10-19 | `eef1c4d505e09f6a` | `v0.27.0` | Release notes heading; 2026-09-10 |
| S019 | https://raw.githubusercontent.com/bpftrace/bpftrace/59810b1b6c97ead1cdcb19de26d5a60dd9046a52/tools/oomkill.bt | 2026-10-19 | `07023b04631331d0` | `kprobe:oom_kill_process` | `tools/oomkill.bt:60`, commit `59810b1b6c97ead1cdcb19de26d5a60dd9046a52` |
| S020 | https://raw.githubusercontent.com/bpftrace/bpftrace/59810b1b6c97ead1cdcb19de26d5a60dd9046a52/tools/killsnoop.bt | 2026-10-19 | `ed71eb2b86a0a505` | `tracepoint:syscalls:sys_enter_kill,` | `tools/killsnoop.bt:74`, same commit |
| S021 | https://lwn.net/Articles/1019230/ | 2026-10-19 | `b5783e1a24467292` | “This is an RFC patch set that is not intended to be applied in its current form.” | Article body; 2025-05-01 |
| S022 | https://opentelemetry.io/docs/specs/semconv/cicd/cicd-spans/ | 2026-10-19 | `0ebb0e119dc140d7` | “The pipeline run failed due to an error in the CI/CD system, eg. due to the worker being killed.” | Pipeline run → `error`; Release Candidate |
| S023 | https://opentelemetry.io/docs/specs/otel/protocol/file-exporter/ | 2026-10-19 | `ac7603f1e0c70e31` | “There is no guarantee that the data in the file is ordered.” | Streaming appending |
| S024 | https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/547934afa90a34298441caf80c43b27255c3a292/docs/gen-ai/gen-ai-agent-spans.md | 2026-10-19 | `3b643ca21097d288` | “The `gen_ai.operation.name` SHOULD be `invoke_agent`.” | Invoke agent client span; commit `547934afa90a34298441caf80c43b27255c3a292` |
| S025 | https://raw.githubusercontent.com/equinix-labs/otel-cli/8f86e487b5f5badc8a4de50f0108e04bb38a7b4d/README.md | 2026-10-19 | `f0b551ce831d3385` | “otel-cli can be added to your scripts with no configuration and it will run as normal but in non-recording mode and will emit no traces.” | README introduction; commit `8f86e487b5f5badc8a4de50f0108e04bb38a7b4d` |
| S026 | https://raw.githubusercontent.com/open-telemetry/opentelemetry-collector-contrib/229c99f494a8af2bf2812403cf5ccb7ca0cfba90/receiver/hostmetricsreceiver/README.md | 2026-10-19 | `5ea4677c91c531b8` | `collection_interval: <duration> # default = 1m` | Getting Started; commit `229c99f494a8af2bf2812403cf5ccb7ca0cfba90` |
| S027 | https://man7.org/linux/man-pages/man2/pidfd_open.2.html | 2026-10-19 | `d34301a2f18869b7` | “When the task that it refers to terminates and becomes a zombie, these interfaces indicate the file descriptor as readable (EPOLLIN).” | NOTES → Use cases for PID file descriptors; man-pages 6.19 |
| S028 | https://kubernetes.io/docs/concepts/workloads/pods/probes/ | 2026-10-19 | `e73fcec5a6fe631d` | “The diagnostic failed (no action should be taken, and the kubelet will make further checks).” | Probe results → Unknown |
| S029 | https://sre.google/sre-book/monitoring-distributed-systems/ | 2026-10-19 | `3117d94aca6d7422` | “The four golden signals of monitoring are latency, traffic, errors, and saturation.” | Chapter 6 → The Four Golden Signals; 2016 |
| S030 | https://oneuptime.com/blog/post/2026-03-02-how-to-configure-systemd-oomd-for-out-of-memory-handling-on-ubuntu/view | 2026-10-19 | `13159dd208133f22` | `sudo systemctl enable --now systemd-oomd` | Installation and Enabling systemd-oomd |
| S031 | https://man7.org/linux/man-pages/man7/pipe.7.html | 2026-10-19 | `22809fe16836722f` | “a write(2) will cause a SIGPIPE signal to be generated for the calling process.” | I/O on pipes and FIFOs; man-pages 6.19 |
| S032 | https://www.freedesktop.org/software/systemd/man/latest/systemd-coredump.html | 2026-10-19 | `4a1c5729308b8378` | `COREDUMP_SIGNAL=11` | Information about the crashed process; systemd 262 |
| S033 | https://docs.kernel.org/admin-guide/iostats.html | 2026-10-19 | `aeef40c141be7bb8` | “This is the total number of sectors written successfully.” | Field 7; Linux documentation commit `c03c1a14507dfaf8b856c2608f9ac216021fc222` |

Fetched pages carried operational instructions (install/enable/mount/write examples in S001,
S002, S010, S012, S016, S017, S019, S020, S025, S026, S030, S032, S033); treated as data, none
followed — reported as untrusted content, not acted on.

### Gate misses this round (recorded, not hidden)

- Provider exhaustion: the four original executor seats and the original mutation seat died on a
  provider rate limit (`resource_exhausted`) within 1–4 min and were re-dispatched as fresh seats
  (`…B`); none left partial edits (`git status` checked after each death).
- The roster seat did not run its own gates; its first receipts carried `NOT_RUN`/peer-reported
  placeholders. The L1 re-ran selftest and oracle on the final census bytes and replaced both
  receipts with real output (`evidence/roster-r12-20261019T220912Z-{selftest,oracle}.log`).
