# Mo51CritContractFreeze — attack on the round-51 contract vs counters/controls/evidence

Seat: Mo51CritContractFreeze (critic). Scope: contract.md P-C1/P-C2 sentences = counters'
code and receipt labels; before-values equal receipts; controls really skip the claimed work;
freeze manifest; frozen bytes unchanged between freeze commit `4677910e` and data commit
`87e0c374`. Machine: MACHINE_ID (container, same host as the lane). Scratch:
`/fast/scratch/hyaku/mori-r51/Mo51CritContractFreeze/` (created, used, removed on exit).
No tool installs (none needed).

## 1. Freeze manifest and frozen bytes

Command: `cd /home/vgpnk/Projects/shokunin/mori-shokunin && sha256sum -c .ufo/waves/round-51/evidence/freeze-sha256.txt`
Result: all 21 entries OK, rc=0.

Frozen bytes unchanged freeze->data: for every one of the 21 manifest paths,
`git show 4677910e:<path> | sha256sum` == `git show 87e0c374:<path> | sha256sum`
== manifest digest; the comparison script printed no CHANGED line.

Commit topology (read-only `git log`): line is `aa3af1ec` (entering tip, parent)
→ `4677910e` (freeze, "freeze — contract, C1/C2 counters, controls and receipts, five
source copies (before any seat)") → `87e0c374` (data). `git diff --name-status
4677910e 87e0c374` shows exactly the claimed landing set: M `.ufo/waves/round-40/conform.py`,
M `SHONEN.md`, M `SKILL.md`, M `corpus/SOURCES.md`, A
`corpus/knowledge/memavailable-estimate-r51.md`, M `tools/mori-pin-check.py`, A
`.ufo/waves/round-51/evidence/selftests/mori-pin-check.txt`, A
`.ufo/waves/round-51/evidence/selftests/mori-unlanded-check.txt`. None of the 21 frozen
paths is touched by the data commit. `git diff --name-status aa3af1ec 4677910e` shows 22
additions, no modifications (freeze adds only round-51 files).

## 2. P-C1 vs count-c1.py

`count-c1.py` docstring (lines 4-27) is the operational text; contract P-C1 (lines 30-43)
restates it. Each clause maps to code and receipts:

- Arm A (kill_residue): `arm_kill` — fresh `git clone --no-local --no-checkout` then
  `git checkout -q -B master R` (fresh_clone, lines 73-81); run
  `python3 <c0>/tools/mori-pin-check.py --rev R --repo C0` with `TMPDIR=<scratch>/tmpA`
  (line 105-108); start-write detection = first nonempty `git -C C0 status --porcelain
  --ignored --untracked-files=all` line OR `tmpA` >= 100 entries in `count_entries`
  (lines 114-117), then `time.sleep(3)`, `os.killpg(..., SIGKILL)` (lines 118-123);
  kill = `len(status_lines(C0))` (line 127). Identical to contract sentence.
- Arm B (relocated): `arm_relocated` — second fresh clone C1; bwrap `--bind / / --dev
  /dev --proc /proc --tmpfs <lane> --setenv TMPDIR <scratch>/tmpB`; probe asserts
  `<lane>/SKILL.md` absent (`C1_RELOC_SETUP` guard, lines 136-147); success =
  returncode 0 and last line startswith `PIN_CHECK=met` (line 150). The `--hide`
  default is the lane (line 215), i.e. "the lane working-tree path hidden".
- Arm C (classified): `arm_classified` uses the frozen five-row `FIXTURES` registry
  (lines 44-66): enva (no tally, rc 2 setup error), envb (no tally, rc 1 traceback),
  stla (different tally), stlb (pinned tally but rc 1), okay (match). WANT map (line 66)
  = env/env/stale/stale; checks one `state=mismatch` line ending `class=env`/`class=stale`
  per pinned prefix, one `state=match` line without class, summary last line startswith
  `PIN_CHECK=unmet` and endswith ` env=2 stale=2` (lines 176-183).
- Arm D (selftest): `arm_selftest` runs `git archive R` (line 190), `--selftest` with
  `TMPDIR=<scratch>/tmpD`, last `PIN_CHECK_SELFTEST` line, rc 0, fail=0, pass >= 114
  (ENTERING_SELFTEST, line 40, 208).
- Exit codes: 0 met / 1 unmet / 2 setup (lines 254-257); scratches refused inside the
  source repo (lines 226-229).

Receipt labels: counter output format line 250-253 matches contract "Output" line and
the C1 control table (`reloc_mismatch`, `classified=ok|bad`, `selftest=pass=N,fail=N`,
`failed=<arms>`). No mismatch found.

## 3. P-C2 vs count-c2.py

`count-c2.py` docstring (lines 5-18) is verbatim the P-C2 sentence (contract lines 74-82).
Code matches each clause:

- opens with `source:`/`verified-at:`/`recheck:`: `has()` over first 14 nonblank lines
  (lines 164-165); entry lines 3-9 satisfy it.
- table `claim|source|quote` >= 12 rows: `parse_claims` header match (lines 103-106),
  `MIN_CLAIMS=12` (lines 172-173); actual 21 rows.
- claim cell >= 6 words, unique (case/whitespace folded), >= 3 words of 3+ letters absent
  from quote: lines 180-196 with `words_beyond` (lines 75-77).
- source cell: one `S<3+ digits>` id; SOURCES row at R mined, opened 2026-10-26, URL
  among the five frozen copies, entry in used-by: lines 186-212. Verified against real
  SOURCES.md header (11 cells) and rows S492-S496 at the data commit: cell 7 `status`=
  `mined`, cell 8 `opened`=`2026-10-26`, cell 10 `used-by` contains the entry, cell 1
  contains the URL. Rows S493-S496 read clean; S492 same shape.
- quote: exactly one backticked span, 6-25 words, unique, located whitespace-collapsed in
  the committed copy: lines 185-195, 213-217 (`normalise_text`). Located=21/21 at data.
- all 5 sources drawn on: line 229-230 (`sources=5`).
- copies match frozen sha256: `COPIES` digests equal freeze manifest digests (5/5),
  checked via `pins=ok` and independently by sha256sum of the five committed copies.
- entailment arm: `entail_votes` reads `git ls-tree --name-only R .ufo/waves/round-51/w1/`
  files ending `.md` not starting `MoriR51`; per claim hash (first 12 hex of sha256 of
  the collapsed claim cell) counts `entailed`/`overclaim`; dissent if any overclaim,
  entailed++ otherwise; fails if `dissent or entailed != claims` (lines 218-226). The
  `ENTAIL_RE` (line 117) accepts `^\s*ENTAIL\s+<12 hex>\s+(entailed|overclaim)\b` —
  exactly the contract's line shape.

`--hashes` path prints `<h>` per row; re-run at the data rev reproduces
`evidence/c2-hashes-at-data.txt` row-for-row (21 rows, same hashes).

## 4. Before-values equal receipts

- C1 before (contract lines 44-45) = `evidence/control-c1-do-nothing.txt` line 9 exactly:
  `C1=unmet kill_residue=12547 relocated=unmet reloc_mismatch=1 classified=bad
  selftest=pass=114,fail=0 ... failed=kill_residue,relocated,classified`, exit=1.
- C2 before (contract lines 86-87) = `evidence/control-c2-do-nothing.txt` line 2 exactly:
  `C2=unmet claims=0 ... pins=bad ... failed=entry_absent,pins`, exit=1.
- Census (contract line 111): `evidence/census-start.txt` rc=0, 22 W04 lines + `ok`.
- Sweep (contract lines 66-68): `evidence/sweep-memavailable.txt` shows MemAvailable in 7
  files and zero hits for `si_mem_available`, `totalreserve`, `wmark_low`,
  `folio_is_file_lru`, `34e431b0`, `show_mem.c` (empty sections).

## 5. Controls really skip the claimed work

`controls/c1-controls.py` builds one commit per control on the entering tip in a
throwaway `--no-local` clone K; every variant maps to exactly the factor it claims:

- do-nothing: base itself (revs["do-nothing"] = (LANE, base)); receipt command uses
  `--repo /home/vgpnk/Projects/shokunin/mori-shokunin` at `aa3af1ec` — no commit.
- scratch-only: `sub(ent_pc, SCR_OLD, SCR_NEW_ENTERING)` — only the export parent line
  (`scratch_parent = tempfile.gettempdir()`), entering pin-check unchanged.
- conform-only: `{CF: wit_cf}` — only conform.py replaced by witness conform.py; pin-check,
  SKILL.md unchanged (receipt selftest=pass=114,fail=0 confirms).
- class-only: `{PC: sub(wit_pc, SCR_NEW_WIT, SCR_OLD), SK: wit_sk}` — witness pin-check
  with the export parent reverted to `<repo>/.scratch`, SKILL.md pin 114->119. Receipt
  shows class=env/stale lines but kill_residue=1 and relocated=unmet (export still inside
  repo) and selftest=pass=118,fail=1 (one witness self-arm depends on the scratch move).
- always-env: `{PC: sub(wit_pc, CLS_OLD, 'kind = "env"'), CF: wit_cf, SK: wit_sk}` —
  witness pin-check with every tally-mismatch tagged env; receipt shows env=4 stale=0 and
  classified=bad (stale fixtures fail), exactly as the table reads.
- witness: `{PC: wit_pc, CF: wit_cf, SK: wit_sk}` — both witness files + pin 119; receipt
  `C1=met ...` exit=0 (feasibility).

All six C1 control readings in the contract table (lines 137-144) match their receipts
byte-for-byte (rev elided), including exit codes. The receipts are committed in the freeze
commit (manifest entries) and were scored with the frozen counter before data (receipt
command lines invoke `count-c1.py` with `--repo K --scratch s-<name>`).

## 6. Target-after receipts are reproducible

Re-ran the frozen counters at the data rev (read-only `git show`/`git ls-tree`; scratch
under `/fast/scratch/hyaku/mori-r51/Mo51CritContractFreeze/`, removed afterwards):

- `python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-51/count-c2.py
  87e0c374...` -> `C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=5
  source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=87e0c374... failed=entailment`,
  exit=1 — identical to `evidence/c2-at-data.txt`.
- `count-c2.py --selftest` -> `C2_SELFTEST pass=34 fail=0`, exit=0 — matches
  `evidence/selftest-c2.txt` (34 PASS lines; the named entry-level controls altered quote,
  wrong copy, breadcrumb, echo, unreviewed row, dissent, L1-authored vote, vote in another
  dir, vote on other text are all present as checks).
- `count-c1.py 87e0c374... --scratch <seat-scratch>` -> `C1=met kill_residue=0 relocated=met
  reloc_mismatch=0 classified=ok selftest=pass=119,fail=0 rev=87e0c374... failed=-`, exit=0
  — identical to `evidence/c1-at-data.txt`.

## Findings

- LOW — `evidence/c1-at-data.txt`, `evidence/c2-at-data.txt` and `evidence/c2-hashes-at-data.txt`
  exist only as untracked working-tree files: `git cat-file -e 87e0c374:<path>` fails for all
  three (`git ls-tree` at the data commit does not list them). The freeze manifest is only for
  pre-data receipts, so this is not a freeze violation, but the target-after receipts are not
  recoverable from the data commit alone. File: `.ufo/waves/round-51/evidence/{c1-at-data,
  c2-at-data,c2-hashes-at-data}.txt`.
- LOW — the landed `tools/mori-pin-check.py` (sha256 `35c69d91...`) and
  `.ufo/waves/round-40/conform.py` (sha256 `7f5174d5...`) at `87e0c374` are byte-identical to
  the disclosed witness bytes under `controls/witness/`. Contract line 51-52 calls the witness
  "not the claim's landing"; the landing is in fact exactly the witness bytes (it is disclosed,
  so no P sentence is violated, and the witness control then double-tests the shipped code
  rather than a separate prototype). File: `controls/witness/{mori-pin-check.py,conform.py}`
  vs `tools/mori-pin-check.py`, `.ufo/waves/round-40/conform.py`.
- LOW/INFO — the control receipts reference ephemeral revs (`cb0a8c52`, `d57cd56e`,
  `a7223fe2`, `8ee22bde`, `42719d0f`) in the throwaway clone K (`/fast/scratch/hyaku/mori-r51/
  L1/ctl/K`), which is not part of the lane, so the control commits cannot be re-verified from
  the repository alone; the builder (`controls/c1-controls.py`) and the receipts are mutually
  consistent (Section 5). Expected by design; named for completeness.

No HIGH/MED contradiction found: every P-C1 and P-C2 sentence matches the counters' code and
receipt labels; before-values equal receipts; controls skip exactly the claimed work; the
freeze manifest verifies (rc=0); frozen bytes are unchanged between `4677910e` and
`87e0c374`; and the target-after receipt lines reproduce on re-run.
