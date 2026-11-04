# Round 84 — mori (L1 MoriR84), attempt 1, wave w1

round: 84
date: 2026-11-04
entering: 5adf4337b6510dd246b247092c11cbaa97c930d3
freeze: daa77bd5684c8db75eec1e80c87ee4fa5c3a6bb4 (contract + three counters + entering controls)

Axes: operability 7, calibration 5 (tied lowest), depth 5 (tied lowest) — the three the contract
freezes. No scalar score change is asserted. Detection and report only; neither a source nor a
receipt authorizes remediation.

Frozen authority: `.ufo/waves/round-84/contract.md` (P-C1, P-C2, P-C3), the three counters in the
same directory, and the do-nothing controls `evidence/controls-r84.txt` (`C1=unmet harness=absent`,
`C2=unmet arm=absent`, `C3=unmet delta=absent`, each rc 1 at `5adf4337`). This lesson does not
amend that authority.

| Claim | Keeper (run from the lane root) | Target, exit 0 |
|---|---|---|
| C1 — operability (7): the r83 counter family's four extra mutants (M24a–M24d) get the failing arm each needs, with M24c/M24d adjudicated equivalent behind byte coupling proofs | `python3 -I .ufo/waves/round-84/count-c1.py <rev>` | `C1=met mutants=4 killed=2 equivalent=2 survivors=0 total=4 pristine=green detector=green` |
| C2 — calibration (5, tied lowest): the record sweep's revision arm grades every row the anchor selects on both sides, with two defeated ambiguous fixtures | `python3 -I .ufo/waves/round-84/count-c2.py <rev>` | `C2=met arm=all-rows defeated=2 fixtures=3/3 bindings=3 revisions=0 arms=44` |
| C3 — depth (5, tied lowest): the r83 drift counter's live reading becomes a per-token delta classification (absent-live / added-live / class-changed / agreed) | `python3 -I .ufo/waves/round-84/count-c3.py <rev>` | `C3=met delta=classified tokens=64 classified=union residual=0 live=derived` |

Targets are the frozen strings, not observed values: a `C1=unmet`/`C2=unmet`/`C3=unmet` reading at
the integration revision is an honest stop for that claim and no target is narrowed after data.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix delivered this round and what makes it able to fail |
|---|---|---|---|
| A round's instruments were never mutation-probed: the round-83 report read its counters met while its own mutation-probe seat died without a tally, so a survivor inside the counters that graded the round stayed invisible | `.ufo/waves/round-83/w1/` holds no `Mo83M01Mut.md`; `corpus/lessons/round-83.md` §"Wave and seat record" names six dead seats; the round-84 C1 population exists only because the **C1 reviewer** ran its own 24th-mutant sweep (`.ufo/waves/round-83/w1/Mo83R01C1.md` §6, M24a–M24d) | `none` — no QUALITY criterion required a counter's own mutation tally before a round reports met | The r84 C1 counter grades the four mutants against the r83 counters at the graded revision, one arm per non-equivalent survivor: `M24a` (tally) and `M24b` (green token) land as the `blind_case_tally` and `green_requires_fail_zero` arms in the r83 `count-c1.py` `selfcheck()` (6 → 8 arms; that file's own six-arm selftest reads `C1_COUNTER_SELFTEST pass=6 fail=0` at `daa77bd5`, and `M24a` survives it), and `M24c`/`M24d` count `equivalent` only while their coupling markers occur exactly once. The frozen population control is `C1=unmet mutants=4 killed=0 equivalent=2 survivors=2` rc 1 at the freeze commit, `survivors=0` after the arms. **That control is not reproduced by the freeze bytes** — see below. |

**Measured conflict (this seat, read-only, at `daa77bd5`).** The same keeper command prints:

```text
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && python3 -I .ufo/waves/round-84/count-c1.py daa77bd5684c8db75eec1e80c87ee4fa5c3a6bb4
MUTANT count-c1.py M24a_killed_tally survived rc=0
EXTRA unanchored .ufo/waves/round-83/count-c1.py M24b_green_fail_token occurrences=2
EXTRA unanchored .ufo/waves/round-83/count-c2.py M24c_met_unclassified occurrences=0
EXTRA unanchored .ufo/waves/round-83/count-c2.py M24d_met_residual occurrences=0
C1=unmet mutants=1 killed=0 equivalent=0 survivors=1 total=1 pristine=green detector=green rev=daa77bd5684c
rc=1
```

`M24b`'s `old` string occurs twice in the graded file — the r83 counter's own `MUTANTS` row for the
r82 `count-c1.py` `green()` (`count-c1.py:33`) and the real `green()` body (`:129`) — and the
`M24c`/`M24d` `old` occurs zero times because the r83 `count-c2.py` `met` expression is split across
`:241-242` (`... and not unclassified` / `and residual == 0 ...`). The same two counts measure at
`c4845c83`, the revision the population was measured on. Under the frozen rule that an anchor not
occurring exactly once is `unanchored` and never counted killed, `mutants=4` cannot be printed on
these bytes: the C1 target is unreachable until the L1 re-pins the two anchors (a pre-data
amendment) or records an honest stop. Reported, not resolved here; this seat changed no counter and
no contract byte.

## Census

Run by this seat now, verbatim, from `/home/vgpnk/Projects/shokunin` (35 tolerated W04 duplicate-URL
warnings; the validator prints no row count):

```text
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
mori	W04	S035 duplicate url raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in across scopes
mori	W04	S037 duplicate url www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html across scopes
mori	W04	S073 duplicate url docs.python.org/3/library/pathlib.html across scopes
mori	W04	S074 duplicate url kubernetes.io/docs/concepts/architecture/controller across scopes
mori	W04	S075 duplicate url ftp.gnu.org/gnu/bash/bash-5.3.tar.gz across scopes
mori	W04	S076 duplicate url michaelfeathers.silvrback.com/characterization-testing across scopes
mori	W04	S147 duplicate url raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/docs/settings.md across scopes
mori	W04	S148 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c across scopes
mori	W04	S149 duplicate url man7.org/linux/man-pages/man5/proc_pid_oom_score_adj.5.html across scopes
mori	W04	S150 duplicate url raw.githubusercontent.com/systemd/systemd/v262/man/systemd.exec.xml across scopes
mori	W04	S166 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c across scopes
mori	W04	S168 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst across scopes
mori	W04	S201 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c across scopes
mori	W04	S218 duplicate url github.com/torvalds/linux/commit/b6866318657717c8914673a6394894d12bc9ff5e.patch across scopes
mori	W04	S220 duplicate url raw.githubusercontent.com/sysstat/sysstat/v12.8.0/iostat.c across scopes
mori	W04	S228 duplicate url docs.python.org/3/library/os.path.html across scopes
mori	W04	S349 duplicate url www.openeuler.org/whitepaper/openEuler%2024.03%20LTS%20%E6%8A%80%E6%9C%AF%E7%99%BD%E7%9A%AE%E4%B9%A6.pdf across scopes
mori	W04	S351 duplicate url www.freedesktop.org/software/systemd/man/latest/journalctl.html across scopes
mori	W04	S470 duplicate url www.freedesktop.org/software/systemd/man/latest/journalctl.html across scopes
mori	W04	S476 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c across scopes
mori	W04	S486 duplicate url www.freedesktop.org/software/systemd/man/latest/journalctl.html across scopes
mori	W04	S491 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c across scopes
mori	W04	S492 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst across scopes
mori	W04	S546 duplicate url www.rfc-editor.org/rfc/rfc8259.txt across scopes
mori	W04	S552 duplicate url doi.org/10.1109/TSC.2026.3698682 across scopes
mori	W04	S565 duplicate url git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/accounting/psi.rst?h=v7.3 across scopes
mori	W04	S566 duplicate url git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/kernel/sched/psi.c?h=v7.3 across scopes
mori	W04	S567 duplicate url git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/linux/psi_types.h?h=v7.3 across scopes
mori	W04	S568 duplicate url git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/admin-guide/cgroup-v2.rst?h=v7.3 across scopes
mori	W04	S570 duplicate url git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/admin-guide/kernel-parameters.txt?h=v7.3 across scopes
mori	W04	S571 duplicate url git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/kernel/sched/psi.c?h=v7.3 across scopes
mori	W04	S583 duplicate url learn.microsoft.com/en-us/windows/win32/api/sysinfoapi/nf-sysinfoapi-gettickcount64 across scopes
mori	W04	S585 duplicate url learn.microsoft.com/en-us/windows/win32/api/realtimeapiset/nf-realtimeapiset-queryunbiasedinterrupttime across scopes
mori	W04	S586 duplicate url docs.aws.amazon.com/waf/latest/developerguide/waf-tokens-immunity-times.html across scopes
mori	W04	S587 duplicate url learn.microsoft.com/en-us/windows/win32/api/sysinfoapi/nf-sysinfoapi-gettickcount64 across scopes
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
rc=0
```

**371** source rows by the separate grammar count
`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`, not a number the
validator prints.

AFTER (L1, integration, 2026-11-04 after the S599 append): the same command reads
`mori ok` for `corpus/SOURCES.md`, exit **0**, with the same **35** tolerated W04 duplicate-URL
warnings; **372** source rows by the separate grammar count
`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` (371 → 372 with
S599), malformed 0 (the row is 11 columns). Full output retained in
`.ufo/waves/round-84/evidence/after-r84.txt`? No — the census receipt is the command above; its
last line is `mori ok /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md`.

## Record slots owned by the L1

Not written by this seat: the `## Gate` block (admission and reject-class decisions), the measured
after-block at the integration revision (keeper runs pasted into
`.ufo/waves/round-84/evidence/after-r84.txt`), the wave and seat settlement, the SCORECARD and LOG
records, and every commit.

## Gate

**One admit, one reject-class decision, one no-change note.** L1 decision on the scout's material
(`.ufo/waves/round-84/w1/Mo84Sc01Source.md`), which independently fetched and pinned every
candidate; the L1's own fetch of the admitted URL is byte-identical (sha256 `68822410…`).

| Candidate | Decision | Evidence / flip condition |
|---|---|---|
| S599 — arXiv:2408.01760v1, "Large Language Models for Equivalent Mutant Detection: How Far Are We?" (Tian et al., ISSTA'24; preprint v1 opened) — pinned at `corpus/evidence/sources-r84/arXiv-2408.01760-abs.html`, sha256 `688224106999973f3b5c318af871b77923df2c36d0e3e2d799424e2c697cff49`, 42566 bytes, 597 newlines | **ADMIT** (tier A, paper) | Access 2026-11-04T09:39:47–09:40:11Z, HTTP 200, no redirect; three fetches (`cmp` byte-identical), `last-modified: Mon, 24 Aug 2026 20:41:50 GMT`, no ETag, an `If-Modified-Since` revalidation returns 304. Located quote at pinned body line 121 (24 words): "However, the presence of equivalent mutants is known to introduce redundant cost and bias issues, hindering the effectiveness of mutation testing in practical use." The same sentence is copied in page metadata at lines 28, 32 and 39; the anchor is the abstract body. Scope: the abstract's cost-and-bias claim only. |
| `https://arxiv.org/abs/2404.09241` — "An Empirical Evaluation of Manually Created Equivalent Mutants" (Straubinger, Degenhart, Fraser) | **REJECT** (no row) | Fetched 2026-11-04, HTTP 200, no redirect, 40386 bytes, sha256 `4bcb20b2…`, screening copy not pinned. It defines equivalence and reports a weaker "hamper this process" cost over *manually created* mutants in a game study; it states no bias half, has a different population, and gives no adjudication procedure. It would ground a definition this lane does not need (its coupling-marker rule is analytic) — flip only if a revision states the cost-and-bias half for a gate's tally or an adjudication procedure, as a freshly pinned and quoted row, never a back-fill. |
| S595 (arXiv:2102.11378v2 abstract, already in the registry) | **not re-admitted** | Different document on the same concept; S595's own limit line says it does not discuss equivalent mutants. No row change. |

The admitted row grounds only the premise that equivalent mutants are a known cost and bias. It
says nothing about a kill tally, an exemption, a coupling marker, an exit status or this lane;
those are the lane's own decisions, and `corpus/knowledge/equivalent-mutant-adjudication-r84.md`
keeps them separate (K2–K3). The page never defines equivalence (`differ only in syntax` → 0 hits),
never says "survivor" (0 hits) and never mentions counters or selftests (0 hits each) — measured
sweeps in the scout's report §5.

### Routed observation — the r83 reviewer's anchor uniqueness claim

`.ufo/waves/round-83/w1/Mo83R01C1.md` §6 said its four anchors were "verified unique". Measured
2026-11-04 against the graded bytes, three were not: `M24b`'s flat string occurs twice in
`.ufo/waves/round-83/count-c1.py` (the r83 counter's own MUTANTS literal at line 33 and `green()`'s
body at line 129), and `M24c`/`M24d`'s flat `and not unclassified and residual == 0` occurs zero
times because `met` wraps at lines 241-242. The r83 report and lesson are filed records and are not
rewritten; this paragraph is the correction of record, and amendment A2 re-pins the anchors. It is
the second observation of this round, not the mined mistake (that remains the missing
counter-mutation tally above).

### Pre-data amendment A2 (resolution of the conflict recorded above)

The `## Mistakes` paragraph "Measured conflict" is superseded on its conclusion by amendment A2
(commit `39190f8a8b32af30e6a180f91d77aa92542735d9`): the anchors were re-pinned to byte-exact
strings (M24b four-space-indented; M24c `and not unclassified` → deleted; M24d `and residual == 0`
→ deleted), each measured exactly once at the freeze and at the entering revision. No predicate,
kill rule, equivalence map, coupling marker, target or control changed. The corrected population
control reads `C1=unmet mutants=4 killed=0 equivalent=2 survivors=2 total=4 pristine=green
detector=green` rc 1 at `daa77bd5`. Three independent seats (S01, S02, K01) found the same defect
before any after-value existed; A2 is the fix, and their findings are the reason it was found
before data. At the amended bytes the two equivalences are *graded*, not presumed: the mutated
`count-c2.py` copies ran their own selftest green (rc 0) before reading `equivalent`, whereas at
`c4845c83` the flat anchor never matched and no mutation could be applied at all.


## Measured after-block (L1)

At `da7631f4a44aaa6d7c1c822308df4d265fb8d7da` (receipt
`.ufo/waves/round-84/evidence/after-r84.txt`; counters are the worktree bytes at that revision):

```text
$ python3 -I .ufo/waves/round-84/count-c1.py da7631f4
MUTANT count-c1.py M24a_killed_tally killed rc=1
MUTANT count-c1.py M24b_green_fail_token killed rc=1
MUTANT count-c2.py M24c_met_unclassified equivalent rc=0
MUTANT count-c2.py M24d_met_residual equivalent rc=0
C1=met mutants=4 killed=2 equivalent=2 survivors=0 total=4 pristine=green detector=green rev=da7631f4a44a
rc=0
$ python3 -I .ufo/waves/round-84/count-c2.py da7631f4
C2=met arm=all-rows defeated=2 fixtures=3/3 bindings=3 revisions=0 arms=44 rev=da7631f4a44a
rc=0
$ python3 -I .ufo/waves/round-84/count-c3.py da7631f4
C3=met delta=classified tokens=64 classified=64 union=64 residual=0 live=derived live_tokens=64 live_agree=64 deltas=0 arms=16 classifier=5/5 rev=da7631f4a44a
rc=0
```

The C3 live run at `da7631f4` read 64 tokens, every one agreeing with the snapshot, so no
`LIVE_DELTA` line printed — the classification is exercised by the five imported classifier cases
(`classifier=5/5`) and the real run is the observation. A scratch clone reads a different fleet
root (the counter resolves `dirname(repo)`), which is why the seat's probe saw `deltas=26` there
and the lane checkout reads `deltas=0`; neither is a class change.

## Wave and seat record

ONE v1 wave, 14 seats under `ufo-wave-policy.json` (band 8–16): 4 executor, 3 reviewer, 2 scout,
2 scribe, 1 critic, 1 mutation-tester, 1 connector; attack share 5/14 (35.7 %), connectors 1;
residual none; the planner seat is the L1. `w1.ready` was taken at 09:39:36Z
(`w1.ready.dispatched`); seats routed through the host table, no `model` passed.

**Dead seats (never replaced):** `Mo84E02C2Rows` (executor, empty output, no tool edit) and
`Mo84R02C23` (reviewer, empty output). The L1 executed E02's assignment from a scratch prototype
validated against the frozen counter before application — the all-rows rule and its four arms are
in `tools/mori-record-sweep.py` (`RECORD_SWEEP_SELFTEST pass=44 fail=0`, C2 met). R02's C2/C3
attack is covered by the critic (`Mo84C01Crit`), the C1 reviewer, the mutation probe and the
record reviewer; its absence is recorded, not papered over.

**Pre-data amendments (all disclosed in the contract; no predicate, kill rule, target or class
changed after data):**

| amendment | what it fixed | evidence |
|---|---|---|
| A1 | the fixture finding's line number (`rev-ambiguous` reports the carrier row) | contract §A1; L1 prototype |
| A2 | three anchors quoted from r83 prose, not bytes (M24b 2×, M24c/M24d 0×) | contract §A2; S01/S02/K01 found it independently |
| A3 | `tokens=64` is the snapshot count, not a live count | contract §A3; S02 finding 2 |
| A4 | the `blind_case_tally` assertion is `killed=1 survivors=1 total=2` | contract §A4; Sc02 finding D3 |
| A5 | C1 binds the two arm labels and the 2/2/4 split (critic's tripwire control reached the target) | contract §A5; `evidence/controls-r84-defeated.txt` |
| A6 | C3 imports and grades the classifier, recounts the snapshot (critic's null classifier reached the target) | contract §A6; `evidence/controls-r84-defeated.txt` |
| A7 | separability wording (C1 reads the file C3 edits) and C3's import hardening | contract §A7; R03/C01 §2 |
| A8 | supersede pointers and the per-fixture mismatch kind | contract §A8; R03 §1 F1–F5 |
| A9 | P-C3's preservation list superseded by A7 | contract §A9; R01 §3 |

The A2 class is the round's second observation: the r83 reviewer's §6 "anchors verified unique"
was false for three of four rows (prose quoted, not bytes), and three seats found it before data.
