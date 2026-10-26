# mori round 51 — frozen contract (L1 MoriR51, attempt 1)

Entering lane tip: `aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd` (round 50 closure,
`corpus/lessons/round-50-verifier-spotcheck.md`). This file, both counters, `controls/` (builder and witness
bytes), the control receipts under `evidence/`, the census-start receipt, the sweep and the five source copies
under `corpus/evidence/sources-r51/` land in one freeze commit before any wave seat runs. A predicate, counter,
floor or kill rule changed after any seat has scored is not the claim's rule. Frozen bytes are listed with
sha256 in `evidence/freeze-sha256.txt`; if working-tree bytes ever differ, the claim is measured with
`git show <freeze>:<path>`.

Scores entering (SCORECARD.md `## Axes`): coverage 6, operability 7, depth 5, freshness 5, calibration 5,
adjacency 6. Lowest non-retired axes: depth, freshness, calibration (tied at 5). C2 works a lowest axis (depth);
C1 works operability. No stagnation waiver; no exploratory claim. Two claims (the prompt prefers two).

## C1 — operability: pin re-execution is hermetic and says why a pin failed

Surface: `tools/mori-pin-check.py` (the registry pin reconciler; its `--rev` mode is how closures and the lane
re-execute every SKILL.md self-test pin) and `.ufo/waves/round-40/conform.py` (a pinned gate). Routed by
`corpus/lessons/round-50-verifier-spotcheck.md` §5 item 1 (`tools/mori-pin-check.py:884-887` exports a full
tree under `<repo>/.scratch`; `conform.py:69` hardcodes the lane path; re-executions are not hermetic, D-d) and
`considerthese/2026-10-26.md` suggestion 1 (split "can't run here" from "stale"). Pre-data probes at the entering
tip (`evidence/control-c1-do-nothing.txt`): a SIGKILLed `--rev` run leaves 12547 untracked/ignored paths in the
repo it reads; with the lane path hidden, one pin fails (`conform.py`, setup error); mismatch lines carry no class.
A witness probe also showed why the export sat inside the repo: two pinned instruments
(`.ufo/waves/round-49/count-c1.py`, which also reads the `master` branch, and `tools/mori-round19-regressions.py`)
and `conform.py` read git objects from the tree they run in, which a `git archive` export outside the repo does not
have (`evidence/control-c1-scratch-only.txt`: 3 relocated mismatches). The witness therefore measures a
`git clone --shared` checked out at R in scratch instead of an archive.

**P-C1.** At revision R, `python3 .ufo/waves/round-51/count-c1.py R` prints `C1=met …` and exits 0, i.e. all four
arms hold (the counter's docstring is the operational text):
(A) kill_residue — in a fresh `--no-local` clone C0 at R, `tools/mori-pin-check.py --rev R --repo C0` with
TMPDIR in scratch, SIGKILLed (process group) 3 s after it starts writing, leaves 0 lines in
`git -C C0 status --porcelain --ignored --untracked-files=all`;
(B) relocated — in a second fresh clone C1 at R, run under bubblewrap with the lane working-tree path hidden
(`--tmpfs`), `tools/mori-pin-check.py --rev R --repo C1` exits 0 with a last line `PIN_CHECK=met`;
(C) classified — over the counter's frozen five-row fixture registry, R's pin-check tags the two no-tally pins
`class=env`, the different-tally pin and the rc-contradicting pin `class=stale`, the matching pin carries no class,
and the summary ends ` env=2 stale=2`;
(D) selftest — R's `tools/mori-pin-check.py --selftest` exits 0 with `PIN_CHECK_SELFTEST pass=N fail=0`, N >= 114.

Counting command: `python3 .ufo/waves/round-51/count-c1.py R [--scratch DIR]` (scratch must lie outside the lane).

- Before (entering `aa3af1ec`): `C1=unmet kill_residue=12547 relocated=unmet reloc_mismatch=1 classified=bad
  selftest=pass=114,fail=0 … failed=kill_residue,relocated,classified` (`evidence/control-c1-do-nothing.txt`).
- Target after: `C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok selftest=pass=N,fail=0` at the
  landed tip.
- Controls (commits in a throwaway `--no-local` clone built by `controls/c1-controls.py`, scored by this counter
  before data; receipts `evidence/control-c1-<name>.txt`): do-nothing; scratch-only (entering pin-check with the
  export moved to TMPDIR); conform-only (conform.py path fix alone); class-only (classes without the scratch move);
  always-env (every tally mismatch tagged env); witness (feasibility only, built by the L1 — disclosed, not the
  claim's landing). Readings are in the table at the end of this file, filled from the receipts before data.
- Kill rule: `C1=unmet` (or exit 2) at the landed tip → C1 not verified; no re-scoring under a changed counter.
- Named limits (before data): arm A kills at one moment (3 s after the first write) and proves nothing about a kill
  at another moment; arm B hides one path (the lane) and does not prove portability to another host, user or
  kernel; arm C's fixture is five rows and the env/stale rule is "no tally line ⇒ env" — a tool that prints a
  tally and then fails for an environmental reason is classed stale; the counter trusts bubblewrap's mount
  namespace and checks only that `<lane>/SKILL.md` is invisible inside it; `--root` mode still writes temp dirs
  under `<root>/.scratch` (unchanged; not claimed).

## C2 — depth: what MemAvailable is — the kernel's estimate, its formula, and what it leaves out

Surface: `corpus/knowledge/` — resource runway. The fleet dispatcher gates seat spawns on `MemAvailable`
(`.scratch/goal-20261026-hyaku-run9.md` host limits: `MEM_MIN_GB`), and the lane's census and pressure probes read
`MemAvailable/MemTotal` (`corpus/knowledge/surfaces-r7.md:83`, `observability-surfaces-r2.md:234`), but the lane
holds no source on what the number is. Sweep before data (`evidence/sweep-memavailable.txt`, at `aa3af1ec` over
`corpus/SOURCES.md corpus/knowledge SKILL.md`): `si_mem_available`, `totalreserve`, `wmark_low`,
`folio_is_file_lru`, `34e431b0`, `show_mem.c` occur 0 times; `MemAvailable` occurs only as a read value (7 files),
never defined. New entry `corpus/knowledge/memavailable-estimate-r51.md`; new rows (ids continue the registry):
`Documentation/filesystems/proc.rst` at v7.2 (same URL and bytes as S082, other scope — a W04 warning),
`mm/show_mem.c`, `fs/proc/meminfo.c`, `include/linux/mm_inline.h` at v7.2, and commit `34e431b0ae39` (the patch
that introduced MemAvailable).

**P-C2.** The predicate is the docstring of `count-c2.py` verbatim (same sentence): at R the entry opens with
source:, verified-at:, recheck:; a claim/source/quote table of >= 12 rows; claim cells >= 6 words, unique, >= 3
words of 3+ letters absent from the quote; source cell one S-id naming a SOURCES row at R that is mined, opened
2026-10-26, names its URL among the five frozen sources and lists the entry in used-by; quote one backticked span
of 6–25 words, unique, located (whitespace collapsed) in the committed copy; all 5 sources drawn on; copies match
their frozen sha256; and the **entailment arm** (routed defect 4 of the round-50 spot-check): for every row, the
wave report files at R under `.ufo/waves/round-51/w1/` (names not starting `MoriR51`) carry >= 1
`ENTAIL <h> entailed` line and no `ENTAIL <h> overclaim` line, `<h>` = first 12 hex of sha256 of the row's claim
cell, whitespace collapsed. `count-c2.py --hashes R` prints each row's `<h>`.

Counting command: `python3 .ufo/waves/round-51/count-c2.py R`.

- Before (entering `aa3af1ec`): `C2=unmet claims=0 … pins=bad … failed=entry_absent,pins`
  (`evidence/control-c2-do-nothing.txt`).
- Target after: `C2=met claims=N located=N quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok
  provenance=ok entailed=N dissent=0`, N >= 12, at the landed tip.
- Controls: do-nothing (above); the data commit itself before any seat has reviewed it must read
  `failed=entailment` (receipt `evidence/c2-at-data.txt`) — located quotes without a recorded entailment judgment do
  not meet P-C2. Selftest `C2_SELFTEST pass=34 fail=0` (`evidence/selftest-c2.txt`) carries the entry-level
  controls (altered quote, wrong copy, breadcrumb claims, echo claims, unreviewed row, dissent, L1-authored vote,
  vote in another dir, vote on other text).
- Kill rule: `C2=unmet` at the landed tip → C2 not verified. An `overclaim` vote is resolved only by replacing the
  claim text with text a non-L1 seat voted `entailed` (new hash); the dissent on the old text then no longer
  matches a row. Votes are never deleted from a report.
- Named limits: a located quote proves the words occur; an `entailed` vote proves a non-L1 wave seat recorded that
  judgment for that exact text — seats are the lane (LEARNING.md), so this is a committed reviewer step, not
  outside verification; v7.2 code says nothing about other kernels; no host meminfo value is claimed as typical.

## Separability

C1 touches `tools/mori-pin-check.py`, `.ufo/waves/round-40/conform.py`, and the pin cells that name their tallies
(SKILL.md registry row, SHONEN.md, receipts). C2 touches the entry, its SOURCES rows, `corpus/evidence/sources-r51/`
and the wave's `ENTAIL` lines. `count-c1.py` reads no corpus entry; `count-c2.py` reads no tool. Either counter can
be run with the other claim's changes reverted.

## Frontier step, assimilation, mistake, considerthese (not claims)

- Census at round start: `evidence/census-start.txt` (rc 0; 22 W04 + `ok`). Round end: same command.
- Sourced claim: C2 rests on the five rows opened 2026-10-26.
- Assimilation: none — `merge/mori/` holds no staged entry or row on MemAvailable (`evidence/sweep-memavailable.txt`
  tail); the round's frontier ground is chosen on the lowest axis.
- considerthese: `considerthese/2026-10-26.md` suggestion 1 (env versus stale) is implemented inside C1 (arm C).
- Mistake to mine: the round-49/50 instruments that silently depended on the export sitting inside the lane
  repo (the git-object reach found by the relocation witness).

## Round-50 closure routed defects (§5) — carriers

1 `.scratch` producers → C1; 2 round shape → this contract fixes one v2 wave `w1` (64–100 seats) after data lands,
total <= 128 including any residual call, and no other wave; 3 successor calibration counter and K4 beyond SHONEN →
not claimed this round (stays routed to round 52, named in LOG.md); 4 C2 entailment → the entailment arm of P-C2;
5 contract deviations → any deviation from this file is named in LOG.md and the lesson; 6 fleet-owned author date →
operator's (report notes it).

## Round shape

One v2 wave `w1` (policy `scripts/hyaku/ufo-wave-policy-v2.json`, band 64–128), dispatched after the data commit:
build items (frontier lesson drafts, QUALITY/README drafts, relocation sweep of the other host-path instruments)
and attack items (entailment votes on every C2 row by at least two seats of different roles, re-opening each
source, re-running both counters and the controls, mutation of pin-check v5, sentinel review of the bwrap arm).
Attack share >= 25 %. The L1 holds the planner seat.

## C1 control readings (filled from the receipts before data)

| control | counter line (rev elided) | reading |
|---|---|---|
| do-nothing | `C1=unmet kill_residue=12547 relocated=unmet reloc_mismatch=1 classified=bad selftest=pass=114,fail=0 failed=kill_residue,relocated,classified` exit=1 | the target is not reachable without work |
| scratch-only | `C1=unmet kill_residue=0 relocated=unmet reloc_mismatch=3 classified=bad selftest=pass=114,fail=0 failed=relocated,classified` exit=1 | moving the export alone breaks three git-reading pins outside the repo |
| conform-only | `C1=unmet kill_residue=12478 relocated=met reloc_mismatch=0 classified=bad selftest=pass=114,fail=0 failed=kill_residue,classified` exit=1 | the path fix alone makes the relocated run green but leaves the residue and the classes |
| class-only | `C1=unmet kill_residue=1 relocated=unmet reloc_mismatch=2 classified=ok selftest=pass=118,fail=1 failed=kill_residue,relocated,selftest` exit=1 | classes without the scratch move leave the export in the repo |
| always-env | `C1=unmet kill_residue=0 relocated=unmet reloc_mismatch=1 classified=bad selftest=pass=118,fail=1 failed=relocated,classified,selftest` exit=1 | a classifier that says env for everything fails the stale fixtures |
| witness | `C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok selftest=pass=119,fail=0 failed=-` exit=0 | feasibility only; built by the L1 (`controls/witness/`), disclosed |

The kill_residue count of the do-nothing control varies between runs (12475–12547 observed): it counts the paths the
export had written when the kill landed. Any nonzero value is unmet.
