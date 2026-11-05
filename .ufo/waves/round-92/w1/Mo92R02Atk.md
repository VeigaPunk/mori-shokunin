# Mo92R02Atk — attack on the frozen C2 predicate and black-box counter (round 92, w1)

Seat: Mo92R02Atk (reviewer, attack). Lane read-only; all work in scratch
`/fast/scratch/hyaku/mori-r92/Mo92R02Atk` (deleted before yield). Clone:
`git clone --shared -q /home/vgpnk/Projects/shokunin/mori-shokunin $S/repo` →
`git checkout -q --detach f63d1ab030d4179576e494342f48ef8718e497a5` →
`git rev-parse --show-toplevel` = `$S/repo` (TOPLEVEL_OK). No commits, no jj, no lane writes.
No tools installed (python3 3.14 + git only); TMPDIR=$S for every run; nothing over 50 MB in /tmp.

## 1. What the counter trusts (exact surface, from the frozen count-c2.py at 699f6276)

The counter performs **no digest judgment of its own**; it trusts five observations of the tool
it extracts from R via `git archive` (full tree):

1. **Main run**: `python3 -I <tree>/tools/mori-source-digest.py <tree>/corpus/SOURCES.md
   <tree>/.ufo/waves/round-90/w1/Mo90S01Sources/sources` (cwd=<tree>). Trusts `returncode == 0`.
2. **Summary line**: the **last** stdout line matching `DIGEST_CHECK\b.*` (last-match-wins; a
   tool that prints a failing summary and then a passing one is trusted on the passing one).
   Fields read by name from that one line: `mismatch=0`, `superseded=2`, `prefix_only=31`,
   `unpinned=1` (a missing field → None → clause fail; extra text ignored).
3. **Superseded-by pairs**: every stdout line matching `^DIGEST (S\d+) superseded-by (S\d+)\s*$`
   (multiline, exact shape). The id set must equal exactly {S235,S615} (any extra id fails) and
   each pair must map S615→S619, S235→S620.
4. **Mismatch ban**: ANY stdout line matching `^DIGEST (S\d+) mismatch\b` fails `mismatch` even
   if the summary line says `mismatch=0`.
5. **Negative fixtures** (built from `git show R:corpus/SOURCES.md`): negA = the first line
   starting with the literal prefix `"| S619 "` with the last hex char of its **first** 64-hex
   token flipped; the tool must exit 1 and print `^DIGEST S615 mismatch\b` on it. negB = that
   line list minus the first `"| S620 "` line; must exit 1 and print `^DIGEST S235 mismatch\b`.
   **The fixture line-finder requires the padded spelling `| S619 ` / `| S620 `.** If either
   prefix is not found, both fixtures are silently skipped and `negatives` stays 0.
6. **Selftest**: `python3 -I <tree>/tools/mori-source-digest.py --selftest` (cwd=<tree>);
   requires rc 0 and `DIGEST_SELFTEST pass=(\d+) fail=(\d+)` with fail=0, pass>=8 (stdout+stderr).

Not inspected anywhere: `rows=`, `ok=`, the actual digest values, pinned files, stderr, file
bytes. **A tool that exits 0 and prints the required lines CAN make the counter print met
without performing any check** — demonstrated in §3 (keyed forgery, rc=0, `C2=met`).

## 2. Baseline (entering revision, real counter, real tool)

- Pinned digests recomputed from the lane at f63d1ab0: ast html `7891c5…a42f5` ✓, S235.pdf
  `9855a4…ad8020` ✓ (both match the contract's stated values; rc 0).
- Entering tool direct run (rc 1): `DIGEST_CHECK rows=121 ok=87 mismatch=2 prefix_only=31
  unpinned=1` — reproduces the round-91 receipt. Corrupt recorded values confirmed in-tree:
  S615 `…ac94b8f1a60ad1a6f0` (true `…ac94b0f83b9a8a42f5`), S235 `…a30cda99359e…` (true
  `…a30dca99359e…`). Entering tool contains zero `selftest`/`supersed` markers (grep count 0).
- Real counter on the scratch clone (rc 1):
  `C2=unmet mismatch=2 superseded=None superseded_ids=- prefix_only=31 unpinned=1 negatives=0
  selftest=absent checks_failed=run_rc,mismatch,superseded_ids,negatives,selftest
  rev=f63d1ab030d4` — byte-identical to the committed do-nothing control in
  `evidence/controls-r92.txt`. ✓
- Harness fidelity: my harness (frozen counter code, only `extract`→variant-tree copy and
  `git show R:SOURCES.md`→variant bytes overridden, both documented) on the unmodified base
  tree prints the exact same control line (HARNESS_FIDELITY_MATCH=True).

## 3. Attacks — command, exit code, verdict, clause

All variant runs execute the frozen counter's own code (harness above) against scratch trees =
`git archive f63d1ab0` + the described SOURCES.md edit (+/or tool replacement). Per-attack
results (every run's stdout verdict line and rc recorded here; full lines in §3 table):

| # | Attack (fixture) | Tool-level result | Counter verdict (rc) | Verdict | Deciding clause |
|---|------------------|-------------------|----------------------|---------|-----------------|
| a | S619 row `supersedes S615` but recorded digest = **S235's pinned-copy digest** `9855a4…ad8020` (padded rows) | `DIGEST S619 mismatch recorded=9855… actual=7891…`; tool rc 1 | `C2=unmet mismatch=3 … superseded_ids=- … negatives=2 selftest=absent checks_failed=run_rc,mismatch,superseded_ids,selftest` (1) | **REJECTED** | digest pairing: a successor is paired with its OWN named pinned copy; the `supersedes` marker (in cell 8, which the entering tool never reads) cannot launder a wrong digest. Also contract: successor counts only if itself classified ok |
| b | `supersedes S615 —` + full digests placed in **non-table prose lines** | prose invisible: `ROW_RE ^\|\s*(S\d+)\s*\|` never matches; run = entering state, rc 1 | `C2=unmet mismatch=2 … superseded_ids=- … negatives=0 … checks_failed=run_rc,mismatch,superseded_ids,negatives,selftest` (1) | **REJECTED** | tool parses table rows only; counter's SUPER_RE needs tool-emitted `DIGEST <id> superseded-by <id>` lines — none exist; fixtures also skipped (no `\| S619 ` lines) |
| c | S619 in table, true digest, but teaches cell reads `note: supersedes S615 — ` and cell 8 carries no supersedes phrase | S619 classifies ok; no supersession anywhere (no code path emits `superseded-by`); rc 1 | `C2=unmet mismatch=2 … superseded_ids=- … negatives=2 selftest=absent checks_failed=run_rc,mismatch,superseded_ids,selftest` (1) | **REJECTED** (must-not-supersede holds) | no supersession logic exists at entering; phrase position is unread (cells 5/8 not parsed). Falsifier F3 carries to the landed tool |
| d1 | **Edit-in-place**: S615's recorded digest replaced by the true copy digest, successor rows still present | S615 classifies **ok** (as predicted); S235 still mismatch; rc 1 | `C2=unmet mismatch=1 … negatives=1 … checks_failed=run_rc,mismatch,superseded_ids,negatives,selftest` (1) | **REJECTED by counter** | negA: with S619 corrupted the counter demands `DIGEST S615 mismatch` — impossible once S615 was fixed in place → neg=1 → `negatives` clause. The tool itself accepted the forgery; the counter did not |
| d2 | Edit-in-place of **both** S615+S235 to true digests, no successor rows | tool's own summary clean: `mismatch=0 ok=89 prefix_only=31 unpinned=1`; tool rc **1** (not 0 — see §5) | `C2=unmet mismatch=0 superseded=None superseded_ids=- … negatives=0 selftest=absent checks_failed=run_rc,superseded_ids,negatives,selftest` (1) | **REJECTED** | `superseded_ids` (no pairs) + `negatives` (fixtures skipped, neg=0) + `run_rc` + `selftest`. Digest-edit shortcut is caught without any digest judgment by the counter |
| succ-padded | plain successor rows, corpus spelling `\| S619 \|` (control for the neg fixtures) | S619/S620 both ok; S615/S235 still mismatch; rc 1 | `C2=unmet mismatch=2 … negatives=2 selftest=absent checks_failed=run_rc,mismatch,superseded_ids,selftest` (1) | REJECTED (expected) | negA/negB pass **vacuously** (S615/S235 mismatch on their own) — the fixtures alone do not test supersession at the entering tool |
| succ-unpadded | successor rows in the task's verbatim spelling `\|S619\|…` | tool classification identical to padded (ROW_RE is whitespace-tolerant) | `C2=unmet … negatives=0 …` (1) | **LANDING TRAP — false unmet** | counter's fixture finder needs literal `\| S619 `/`\| S620 ` prefixes; unpadded rows → fixtures silently skipped → `negatives` fails a perfect landing. See §6 |
| f-naive | forged tool: prints required lines + selftest line, exits 0, **no** content/argv distinction | zero checks performed | `C2=unmet mismatch=0 superseded=2 superseded_ids=S235,S615 prefix_only=31 unpinned=1 negatives=0 selftest=pass checks_failed=negatives` (1) | **REJECTED** | negatives: negA/negB get rc 0 and no mismatch lines → neg=0 |
| f-keyed | forged tool keyed on the harness's own filenames: `--selftest` → selftest line; basename `negA.md`/`negB.md` → one mismatch line + rc 1; else success block + rc 0. **Zero digest computation** | prints exactly what each counter call wants to see | **`C2=met mismatch=0 superseded=2 superseded_ids=S235,S615 prefix_only=31 unpinned=1 negatives=2 selftest=pass rev=f63d1ab030d4` (rc 0)**; C2_REPORT: run_rc=0 succ_ok=True negatives=2 selftest_rc=0 | **ACCEPTED — forger wins** | none fails: every clause is output-shaped and the tool distinguishes harness invocations by the counter's chosen fixture names |

**Accepted limit (to report, not fix):** the counter's entire trust surface is the tool's
stdout lines + exit codes, and the negative fixtures hand the subject enumerable inputs
(`<tmpdir>/negA.md`, `<tmpdir>/negB.md`, `--selftest`) distinguishable from the main run's
`corpus/SOURCES.md`. Any tool that keys its output on those names defeats negA, negB and the
selftest simultaneously while computing nothing. The counter cannot be fixed from inside its
frozen predicate; mitigation lives outside it: tool identity/review at landing, the
mutation-tester's mutants (Mo92M01Mut), and the L1's own reading of the landed tool diff
(this attack's forged tools are 16 lines; a reviewer diffing the landed tool against the
entering one will see there is no hashing code left).

## 4. Additional counter-trust defects found (all frozen; no fixes proposed)

- **Last-line-wins**: only the LAST `DIGEST_CHECK` line is parsed — a tool may print a failing
  summary then a passing one.
- **negA flips the first 64-hex token of the S619 line**: if the landed S619 row carries any
  other 64-hex token before its digest (e.g. a script/blob sha in the source cell), the flip
  corrupts the wrong token and negA may pass or fail for the wrong reason.
- **negB drops every line string-equal to the first S620 line**, not just the first occurrence.
- **Fixtures are skipped, not failed**, when the `| S619 ` / `| S620 ` prefixes are absent —
  the deadliest property (§6).

## 5. Required-by-contract semantic change the L1 must know about

The entering tool's documented exit rule is "0 only when mismatch=0 **and prefix_only=0 and
unpinned=0**" (tool docstring, verified: attack d2 with mismatch=0/prefix_only=31/unpinned=1
still exits 1). The frozen predicate demands the landed tool **exit 0 while
prefix_only=31 unpinned=1**. The landing constraint freezes row *classification*, not the exit
rule — so the executor's landed tool MUST change its exit rule (e.g. `exit 0 iff mismatch==0
and superseded rows classified ok`), otherwise `run_rc` fails an otherwise perfect landing.
Flagging so it is done deliberately and recorded, not discovered as a failed counter.

## 6. Landing-shape requirement (the one thing the landing must not get wrong)

The counter's negative fixtures find rows only by the literal prefixes `| S619 ` / `| S620 `.
The successor rows in the wave spec are written unpadded (`|S619|…`). If the scribe lands the
verbatim unpadded spelling, negA/negB never run, `negatives=0`, and the claim prints
`checks_failed=…negatives…` even with a fully correct landed tool (measured: v_succ row).
The padded corpus spelling `| S619 | …` makes the fixtures run (measured: v_succP).
**The landed SOURCES.md rows must use the padded spelling.**

## 7. Falsifiers the tool's own selftest must reject (for the L1 to run after integration)

The `--selftest` (pass>=8, fail=0) must include, and fail on, at least these inputs:

- F1 (attack a): a successor whose recorded digest equals a *different* pinned copy's digest
  classifies `mismatch` and is NOT eligible to supersede (contract: successor counts only if
  itself ok).
- F2 (attack b): a `supersedes <id>` phrase on a non-table line produces no `superseded-by`
  output and no verdict change for the predecessor.
- F3 (attack c): `note: supersedes S615 — ` in the teaches cell does NOT supersede S615
  (phrase must be recognized only in its declared cell/shape).
- F4 (negA shape): flipping the last hex char of the successor's recorded digest flips the
  predecessor's verdict to `mismatch` and exits 1 — including when the predecessor row was
  otherwise correct (this is the only thing that catches edit-in-place, measured in d1).
- F5 (negB shape): deleting the successor row restores the predecessor's `mismatch`, exit 1.
- F6: a successor that is itself `mismatch`/`prefix-only`/`unpinned` must not mark its
  predecessor `superseded` (no `superseded-by` line for it).
- F7: emitting any extra `DIGEST <id> superseded-by <id>` pair (e.g. S619 superseding S235)
  must be impossible; the pair set is exactly {S235→S620, S615→S619}.
- F8: classification no-harm: after supersession, the remaining row classes still sum to
  `prefix_only=31 unpinned=1` and no row other than S615/S235 changed class.
- F9: exactly ONE `DIGEST_CHECK` line is ever printed (counter trusts the last one), and no
  `DIGEST <id> mismatch` line is printed for a superseded pair on a clean run (counter bans
  any mismatch line regardless of the summary).
- F10: `--selftest` itself cannot be satisfied by a constant string — it must derive pass/fail
  from the fixtures above (otherwise a keyed forgery prints `pass=8 fail=0` unconditionally,
  as mine did).

## 8. Verdict

ATTACK C2 forger-accepted=1 rejected=6 (a, b, c, d1, d2, f-naive; the keyed forgery was
accepted with rc 0). Accepted-limit named, not fixed. Two landing hazards named for the L1:
row spelling must be padded (§6) and the tool's exit rule must change to allow
prefix_only=31/unpinned=1 at rc 0 (§5).

### Commands and exit codes (all in scratch; lane untouched)

1. `git clone --shared -q <lane> $S/repo` → 0
2. `git -C $S/repo checkout -q --detach f63d1ab030d4179576e494342f48ef8718e497a5` → 0
3. `git -C $S/repo rev-parse --show-toplevel` = `$S/repo` → TOPLEVEL_OK (0)
4. `git -C <lane> show f63d1ab0:…python-ast-3.15.2.html \| sha256sum` → 0 (7891c5…a42f5, matches contract)
5. `git -C <lane> show f63d1ab0:…S235.pdf \| sha256sum` → 0 (9855a4…ad8020, matches contract)
6. entering tool on entering SOURCES.md → rc 1, `DIGEST_CHECK rows=121 ok=87 mismatch=2 prefix_only=31 unpinned=1` (round-91 receipt reproduced)
7. `python3 -I .ufo/waves/round-92/count-c2.py f63d1ab0… --repo $S/repo` (real counter, scratch clone) → rc 1, control line byte-identical to `evidence/controls-r92.txt`
8. harness-on-base fidelity run → rc 1, HARNESS_FIDELITY_MATCH=True
9. v_succ (unpadded rows) → rc 1 (negatives=0 — landing trap)
10. v_succP (padded rows) → rc 1 (negatives=2, vacuous pass)
11. v_aP → rc 1 (mismatch=3)
12. v_cP → rc 1 (no supersession)
13. v_d1P → rc 1 (negatives=1 — negA catches edit-in-place)
14. v_d2 → rc 1 (mismatch=0 but run_rc/superseded_ids/negatives/selftest fail)
15. v_b → rc 1 (negatives=0)
16. v_fnaive → rc 1 (checks_failed=negatives)
17. v_fkeyed+report → rc 0 (C2_REPORT run_rc=0 succ_ok=True negatives=2 selftest_rc=0)
18. v_fkeyed → **rc 0, `C2=met … rev=f63d1ab030d4`** (forgery accepted)

Dead ends: none. One harness correction (copytree `symlinks=True` for the tree's round-17
dangling-symlink fixtures, matching `tarfile.extractall` semantics) — not an attack result.

Scratch directory `/fast/scratch/hyaku/mori-r92/Mo92R02Atk` deleted before yield. No patches
produced (attack seat: report only). No tools installed.
