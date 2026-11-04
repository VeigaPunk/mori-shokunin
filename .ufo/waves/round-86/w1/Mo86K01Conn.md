# Mo86K01Conn — sibling-lane overlap scan (round 86, w1)

Seat: connector (leaf, read-only). Milestone: round 86 w1: sibling-lane overlap scan.
Deliverable: this report only. **No file outside it was written; no scratch dir was created** (every
command below is a read-only `grep`/`sed`/`sha256sum`/`git rev-parse`; no fixture, clone or run was
needed, so there is nothing to clean up and `/tmp` was never used). No tool was installed or upgraded.

Snapshot honesty: siblings land work while seats run. `mori-shokunin` was at
`4eab48c0f721e5917f7611d51561894873a21ea4` when I read it (the round's entering revision is
`fec2b328…`; the r85 counters and the three r86 counters exist on disk at `4eab48c0`). Sibling lanes
read at: kama `2880af05`, chousa `8a28732b`, kengaku `614f0055`, mado `c702094a`, kotodama
`1b0f3767`, kumitate `eca7debd`, tsukuroi `06f1bbbb`. Every verdict below is against **those** bytes,
hashed in §7.

## 0 — The three rules this round lands (as I read them, not as I endorse them)

| id | rule mori lands this round | anchor |
|---|---|---|
| **R1** | A counter's `--selftest` is mutation-adequate: pristine green first, `old` anchor occurs **exactly once**, an unanchored anchor is never counted killed, kill rule reads both channels (non-zero exit **or** `fail=n>0`), the counter's own detector selfcheck is bound into its verdict; six named source mutants must each be killed by a named arm (selftest 20 → 26). | `contract.md` P-C1; `corpus/knowledge/counter-mutation-adequacy-r83.md` K2 |
| **R2** | A receipt's **body is bound to its command**: header `# cmd:`, `# rev: <40-hex>`, `# limits:`, `# counter-sha256:`, `# replay: required\|none`; body split at `# ---`; a `required` receipt's body must equal the stdout of its `# cmd:` executed in a scratch export of its `# rev:` (`GIT_CONFIG_GLOBAL=/dev/null`). | `contract.md` P-C2; `count-c2.py:46-52,62-73` |
| **R3** | A stated classification is reconciled with a **value-level** observation: the r82 name-rule derivation must agree for all 64 rows, and a stated `value-changed` row whose baseline value **equals** its live value is `contradicting` (the label the value channel does not support); observed twice per surface in separate scratch trees. | `contract.md` P-C3; `count-c3.py volatile_fields()/atom_map()/reconcile()` |

**Prior self-statement (load-bearing for R1).** mori already froze R1's four requirements in
`corpus/knowledge/counter-mutation-adequacy-r83.md` K2 (2026-11-04, sha256 `5745a200…`). Round 86 C1
is therefore the *application* of an existing lane rule to six named r85 survivors; the claim is
"the arms were landed and killed 6/6", **not** "a new rule". Any entry this round writes should cite
K2 and say so.

## 0b — The fleet already froze this seat's rule (tsukuroi r27 C2) — `duplicate` for the seat, and a vocabulary mori should adopt

`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-adjacency-overlap.py` (sha256 `a10dd8db…`)
is a frozen counter whose predicate is *this seat's rule, in another lane, keyed to mori*:

> "C2 adjacency overlap register with mori's admitted entry `userspace-oom-killers-r26.md` at mori
> commit `ef9dbee136d6ed2ef98687f5cb0c0a16506a5155` (inbound pointers into this lane replayed,
> overlaps classified with an owner, **reported not absorbed**)" — `tsukuroi-shokunin/SCORECARD.md:998`

Its register `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/adjacency-mori-oom-r27.json`
(sha256 `b094b889…`) holds six rows OV1–OV6 with a **closed class vocabulary**
`INBOUND-RESOLVES | INBOUND-DRIFTED | AGREES | CONFLICTS | LANE-GAP`, an **owner**
`mori | tsukuroi | contested`, an action, and a report surface (`PROVINCE.md` §"Adjacent — mori
userspace OOM killers (round 27)"), graded by anchored rows with pinned snapshot digests. Its
`--selftest` fixtures include a `province_row(..., owner='mori')` arm.

Consequences for mori:

* **My seat's verdict vocabulary is not new.** `conflict` → `CONFLICTS`, `complement` → topical
  overlap under `AGREES`/`INBOUND-DRIFTED`, `duplicate` → `INBOUND-RESOLVES` (pointer replay). A
  round-86 overlap record should either use tsukuroi's five classes or state that it supersedes them;
  inventing a parallel three-word set adds a dialect the fleet has to reconcile later.
* **The instrument's named limit is the mirror of my seat's:** "It does not check that a class or
  owner is the right judgement" (`SCORECARD.md:1018`). That is why my report gives evidence per row
  instead of a class alone.
* **`mutants-adjacency-overlap.py` (sha256 `b85a8b1b…`) applies R1's mechanism to an overlap
  counter** — one more precedent that mori's C1 (arm every survivor) is standard practice in this
  fleet, not a novel construction.
* **tsukuroi's census emits handoff lines addressed to mori** —
  `HANDOFF ADJ-04 mori class=kill-events value=<n> kind=dated-event state=prepared window=… source=journal-window`
  and `class=coredumps …` (`tsukuroi-shokunin/tools/tsukuroi-census.sh:4763-4769`, sha256
  `89026b9a…`). It does **not** read mori's repo or counters; the header states "`value=` is the
  census's OWN count, never one of mori's". It is a producer-side contract whose *subject matter*
  (MESSAGE_ID-per-scope kill events, coredumps) is mori's counting rule — so a change to mori's
  kill-event accounting changes what those handed-off classes mean.



### R1 — source-mutant → arm kill. Four lanes already hold it. Verdict: `complement` (cite, do not re-claim novelty)

| absolute path | the rule it implements | verdict |
|---|---|---|
| `/home/vgpnk/Projects/shokunin/kama-shokunin/tools/round75-survivor-probe.py` (sha256 `25551516…`) | `SURVIVORS2 mutants=5 killed=5 escaped=0`: applies five named source mutations to a copy of a committed tool, requires **the pristine module's selftest green and every mutated copy's selftest red**, and **names for each mutant the selftest arm that fails** (`EXPECTED_ARMS`); "the selftest rejects a count-only cheat whose mutation catalogue is empty" | **complement.** Mechanism identical; distinct axis: kama certifies the arms of a module *built in the same round*; mori arms a *pre-existing legacy counter* (`round-85/count-c3.py`, 20 arms) and grows it, with an exactly-once anchor population gate and `unanchored`/`empty-mutation` classes mori adds. mori's `mutants=6 killed=6 … arms=26` is a strict superset in shape of kama's line. |
| `/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/QUALITY.md:726-727, 994` (sha256 `c7140540…`) | battery receipts carry `MUTANT <id> <class> killed by=<fixture> attributed=<line>` — one fixture per survivor, the killing fixture named | **complement.** Same attribution shape; kengaku's is fixture-keyed, mori's arm-keyed. |
| `/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-37.md:41,43` (sha256 `d92cbf2e…`) | the **vacuous-battery control** (`MUTANTS total=55 killed=5 survived=50` — 5 of 55 advertised classes demonstrated) **and the derived-count hazard** (a `grep 'killed by='` counted 51 ids at 01:44 and 55 at 01:46 while receipts landed) | **complement, and a warning mori's C1 inherits.** mori's frozen target is a *self-reported tally* (`mutants=6 killed=6 survivors=0 total=6`); kengaku's r37 lesson is precisely that such a tally is re-derivable from different populations in the same wave. mori's counter avoids this only because the population is frozen in code (`POPULATION`/mutant table), not grepped — worth stating in the C1 record. |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-counter-discrimination.py` (sha256 `e396b95e…`) | 3 accept + 22 reject **control inputs**, each differing from an accept control in one committed input; a crashing instrument is `ERROR`, never `ok` | **complement.** Grades an instrument against *input* mutants, not source mutants. No overlap with the arm-kill rule. |
| `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/mutants-adjacency-overlap.py` (sha256 `b85a8b1b…`) | the mutation probe of tsukuroi's own `check-adjacency-overlap.py` counter (see §0b) — R1's mechanism applied to an *overlap register* rather than a census | **complement.** Fourth independent instance of "mutate the instrument, require the arm to kill". Reinforces §5 item 2: the mechanism is fleet practice. |

No lane holds mori's exact clause set (exactly-once anchor + unanchored-never-killed + 20→26 arm
growth on a legacy subject) as a *frozen predicate*; kama's r75 is the nearest and should be cited.

### R2 — receipt body bound to its command by replay. **No sibling replays a recorded command string — and one sibling holds the same structure with the opposite decision. Verdict: `complement` against chousa's digest notes; `conflict` against kotodama.**

| absolute path | the rule it implements | verdict |
|---|---|---|
| `/home/vgpnk/Projects/shokunin/kotodama-shokunin/tools/replay-frozen.py` (sha256 `a2fb5c98…`, 677 lines, `--selftest` at `:494`), manifest `kotodama-shokunin/tools/gates/frozen/round-3/MANIFEST.tsv` (sha256 `d5337590…`), caller `kotodama-shokunin/reports/round-8/run-validation.py:1205-1248` (sha256 `7eaa3678…`) | The manifest's columns are `gate gate_sha256 input input_sha256 exit_code finding_count output output_sha256 input_snapshot command`. For every row the tool **verifies the three digests before any gate runs**, copies the pinned snapshot into an isolated mirror, runs `[python3, <pinned gate>, <input>]` there, and compares observed exit code, `^FINDING ` count and **output bytes** with the record — "Replay a frozen gate manifest **without ever executing its recorded commands** … so no string from the `command` column is ever parsed or executed"; the result row even carries `"recorded_command_ignored": row["command"]`. Three-valued exit: 0 reproduced, 1 mismatch, 2 could-not-evaluate, and **2 outranks 1** | **`conflict` — the two rules disagree on the same input.** Nearest structural prior in the fleet to mori R2 (recorded command column + recorded output + isolated replay + byte comparison). Named input: a row whose `command` string carries arguments beyond `<gate> <input>` (for example `python3 gate.py --strict foo.txt`). kotodama replays the **typed columns** and deliberately ignores the command text; mori executes the **recorded string** verbatim in a `bash -c` and compares the body. kotodama reproduces the row from `gate`+`input`; mori reproduces it only from `cmd`. Neither can be derived from the other, and on that input the two verdicts diverge. Secondary divergence: kotodama replays at a **pinned input snapshot** (no revision export, no `# rev:`), mori at a **scratch export of `# rev:`**. Shared and consistent: the three-valued exit contract and fail-closed digest verification *before* any run. |
| `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/receipt-binding-r38.md` (sha256 `c9fe9b2a…`) | digest/identity binding, re-derived by `verify-receipts.py`: `gate_sha256_pre/post`, `counter_sha256`, `expect_sha256`, `receipt_sha256`, later `verifier_sha256`/`subject_counter_sha256`. "Certifies integrity and self-consistency against committed bytes — NOT authorship. **A fabricator holding the public hashes who reproduces honest observations can write a receipt indistinguishable from an executed one.**" | **complement.** That named limit *is* mori's C2 defect class (the stale/fabricated body with correct headers). mori's replay rule is the missing witness; it is not the same rule as chousa's digest binding and neither subsumes the other. |
| `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/receipt-digest-provenance-r67.md` §Limits | "Re-derivability is provenance, not truth: a digest that re-derives proves the bytes are committed, **not which command produced them, that the recorded run happened**" | **complement, citation-grade.** This is chousa stating R2's motivating gap a round after r38. mori's C2 record should cite r67 §Limits, not invent the observation. |
| `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/lessons/round-57.md:36,72,98` (sha256 `b3f677b1…`) | a measured forge class in chousa's own C3: "a fabricated `refetch.tsv` success row plus byte-replayed captures under a forged (id,url) — both a same-id/new-URL replay and a fresh-id replay reach `C3=PASS`"; the record leg "checks the record only for self-consistency, and nothing ties `.txt` to `.raw`" | **complement.** chousa recorded the exact failure shape mori's C2 defends against (self-consistent provenance record + unrelated body). mori's rule ties body to command; chousa's named "smallest safe correction" was left for a future re-freeze, so mori is not duplicating a live rule. |
| `/home/vgpnk/Projects/shokunin/kama-shokunin/tools/round72-receipt-tip-binding.py` (sha256 `a9a4e8d3…`), predicate at `kama-shokunin/SKILL.md:313` | a receipt path cited by the round self-record must exist at rev, carry `# tip=<40-hex>` or `# rev=<40-hex>`, name an **ancestor** of the tip, and every commit in `rev..tip` must touch only declared record paths → `RECEIPT_TIP_BINDING cited/bound/unbound/shifted/stale` | **complement.** Binds the receipt *path* to revision ancestry; never reads or reproduces the body. Verified that neither r72 nor `round74-receipt-claim-binding.py` executes a receipt's command (their only `subprocess` calls are `git` and `sys.executable`). |
| `/home/vgpnk/Projects/shokunin/audio-shokunin/corpus/live/r89-critic/replay.py`, `corpus/live/r89-reverify/runs/replay-global.py` | "replay" here = slicing committed verdict blocks out of a commit and re-`exec`ing them against recorded receipt fields, or re-running a verdict function over recorded windows | **no overlap.** Replays a *verdict function* over recorded data; never re-executes a recorded command. |

**Live conflict candidate (grammar reuse, not a live mis-grade).** Twelve lanes write `# cmd:` (or
`# command:`) header lines whose body is an unfenced transcript and which carry **no `# ---`
separator and no `# replay:` line**: kama 120 files, mado 73, kengaku 55, souji 27, tsukuroi 26,
tameshi 21, chousa 19, kotoba 9, tabi 6, kasegi 3, kaidoku 2, kake 1 (counts = files matching
`^# cmd:` anywhere in that lane's checkout, wave scratch included).

Named input: `/home/vgpnk/Projects/shokunin/kama-shokunin/.ufo/waves/round-79/measured/after/c1-green.out`
— `# rev: 5ac1a8d…` (matches mori's `REV`), `# command: …` (does not match mori's `CMD`), no
`# ---`, no `# replay:`. Kama's verifier cites it as "Evidence-verified"; fed to
`mori/.ufo/waves/round-86/count-c2.py` it would parse as `body=""`, `cmd=None`, and report
`missing-replay,summary` → `failed`. Under mori's `grade_population()` the only waiver for a legacy
receipt is `missing-replay` (`count-c2.py:208-209`); the `# ---` split
(`header_and_body()`, `SEP` at `:52`) is required for **every** receipt, legacy included.

So: **no disagreement today** — mori's population is frozen to five mori receipts, and no sibling
tool reads mori's counter. The disagreement is latent in the token `# cmd:`: if either lane adopts
the other's counter, kama/mado/kengaku transcripts read `defeated` under mori's rule while their own
gates read them valid. The distinguishing facts to record are (a) mori requires `# ---` and a
`# replay:` line, (b) kama writes `# command:`/bare `cmd:` and never `# cmd:`, (c) `# rev:` **is**
shared verbatim (`# rev: <40-hex>`) between mori and kama, so a naive `# rev:` grep will find both.

### R3 — value-level reconciliation of a stated classification. Verdict: `complement`; one false friend

| absolute path | the rule it implements | verdict |
|---|---|---|
| `/home/vgpnk/Projects/shokunin/kama-shokunin/tools/round73-province-host-drift.py` (sha256 `ec7bfd3f…`), r74 successor alongside | grades the **last** `Round-<N> host-identity block` in `PROVINCE.md` (append-only: a host move is answered by appending, never editing) against the live `uname -s`, `uname -m` and `/etc/os-release` `ID`; `PROVINCE_HOST_DRIFT blocks= recorded= live= stale=<n>`; an unparseable block is a `stale-host` finding naming its line, **never a skip** | **complement.** Nearest prior instrument in the fleet: recorded value vs live value, one observation, one surface, three fixed fields. mori grades something different — *whether a stated class label is supported by the value channel* (`value-changed` whose baseline value equals its live value), 14 rows, two surfaces × two runs, with atom-multiset stability. Neither is a special case of the other. |
| `/home/vgpnk/Projects/shokunin/tabi-shokunin/.ufo/waves/round-58/counters/R58Counter.md:40` | `swallow-value-changed`: `backspaceSwallow.valueAfter` / `digitSwallow.valueAfter` must EQUAL the pre-step value (a keystroke-swallow receipt check id) | **false friend — name it.** Same token `value-changed`, unrelated meaning (a DOM input value after a keypress). A `value-changed` grep across lanes will surface tabi; it is not a duplicate and does not conflict. |
| `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh:4041-4058, 4355-4365, 6006-6010` (sha256 `d5d48128…`) | chousa's gate **adapts mori r10's pin/drift**: lineage named to `tools/mori-census.sh --pin/--drift`, `corpus/knowledge/drift-pin-r10.md` and the `d7710981…` refinement; declares `GATE_DRIFT_VOLATILE_FIELDS='ts gate_sha256'`; "The declared contract is compared too: a baseline pinned under a DIFFERENT volatile list is drifting … (the recorded list is the contract — mori r10's `d7710981` refinement)"; three-valued exit so "cannot-compare" never reads clean (cites mori r10's lesson) | **duplicate of mori's own r10 rule, already attributed to mori by chousa.** Not a conflict. **But an asymmetry the L1 should hold:** chousa compares the baseline's declared volatile list against the current one and refuses on mismatch; mori's r86 `count-c3.py` takes the baseline's `# volatile_fields=` only as a drop-mask (`volatile_fields()` → `atom_map(drop=vol)`) and performs no such comparison. Same contract, stricter sibling. If a later round claims "the volatile-field contract is enforced in the value channel", chousa's gate is the bar to meet. |

No lane holds mori's `contradicting=<n>` idea (label-vs-value support) or its two-surface/two-run
atom-multiset stability rule.

## 2 — Who reads mori's artifacts (the L1's notify list)

* **`corpus/evidence/drift-classification-r82.txt`: no lane reads it.** Only
  `/home/vgpnk/Projects/shokunin/.ufo/reports/round-82/mori.md`, `round-83/mori.md` (fleet
  coordinator records) reference it.
* **`.ufo/waves/round-85/count-c{1,2,3}.py`: no lane reads them.** Only
  `/home/vgpnk/Projects/shokunin/.ufo/reports/round-85/mori.md` and `MANIFEST.json` (registry
  notes at lines 2303/2350/2362-2369).
* **`chousa-shokunin` is the one lane whose production tool carries mori lineage**: its
  `tools/research-gate.sh` implements an adaptation of mori r10 `tools/mori-census.sh` pin/drift,
  `corpus/knowledge/drift-pin-r10.md` and the `d7710981` volatile-list refinement. It reads **no**
  mori file at run time (the gate is self-contained), but it is the lane to notify if mori's r10
  contract, volatile-field semantics or drift exit code changes — otherwise the two definitions can
  drift apart while both cite the same origin.
* **`tsukuroi-shokunin` is the one lane whose tool reads a mori blob at a pinned commit.**
  `tools/check-adjacency-overlap.py` resolves `git cat-file -p ef9dbee136d6:corpus/knowledge/userspace-oom-killers-r26.md`
  in `mori-shokunin` when present, and grades its own committed snapshot
  `.ufo/waves/round-27/siblings/mori/corpus/…` against the pinned sha256 (see §0b). Exposure is
  **frozen to the round-27 path set** — no register row names `drift-classification-r82.txt`, the
  r10 baseline or any r85/r86 counter, so nothing mori lands this round moves tsukuroi's count.
  Notify tsukuroi if a mori knowledge entry pinned by that register is ever amended, or if mori's
  kill-event/MESSAGE_ID accounting rule changes (the ADJ-04 handoff classes).
* **Corrected count:** `grep -rn 'mori' *-shokunin --include=*.py --include=*.sh --include=*.mjs |
  grep -v mori-shokunin/ | grep -v '/.ufo/waves/' | grep -v node_modules` returns **185 lines**, of
  which 8 are chousa's `research-gate.sh`. The `\bmori\b` residue is **83 lines across 14 files**:
  tsukuroi 5 files (70 lines — `check-adjacency-overlap.py` 32, `mutants-adjacency-overlap.py` 17,
  `tsukuroi-census.sh` 12, `score-census-handoff-r32.py` 8, `check-adjacency-table-r51.py` 1), souji
  7 files (11), tameshi 1, kengaku 1. The tsukuroi set is the substantive one and is analysed in
  §0b. An earlier sentence in this report said "9 hits, all in the chousa gate"; that was read off a
  `head -20` truncation and is wrong.

## 3 — Assignment-specific checks

**kumitate-shokunin (orchestration) — no receipt gate with R2's claim.** `ufo-task-receipt-v1`
receipts are gated for **existence/parse** plus `priorReceiptSha256` chaining and
`receipt_snapshot_binding_accepted/retracted` pairs (`kumitate-shokunin/SKILL.md:94-95,121,126-127`).
`^# cmd:` → 0 files, `^# rev:` → 0 files in the whole lane. Receipt *identity and chaining*, no body,
no command, no revision. `complement`, no conflict.

**kotodama-shokunin — it does hold the structure, with the opposite decision (see §1 R2).** My first
pass returned "no receipt gate" because kotodama has zero `^# cmd:`/`^# rev:` files; that reading was
**wrong** and is corrected here. kotodama's D2 gate manifest records a **`command` column** per row
plus `output`/`output_sha256`, and `tools/replay-frozen.py` replays it in an isolated mirror with
byte comparison — while explicitly refusing to execute the command text (`recorded_command_ignored`).
That is the same shape as mori R2 and the opposite rule; it is filed as a `conflict`, not an absence.
kotodama's round-79 `freeze-matrix.py` (s01 green, `s02_do_nothing` refused, s03 lands==base,
s04 off-first-parent, s05 not-ancestor, s06 claims amended) is a separate, unrelated freeze-ancestry
matrix whose `s02_do_nothing` is only the same *shape* of control as mori's do-nothing arms.

**Counters that grade a subject's bytes at a revision (mori's C1 pattern) — the pattern is
fleet-standard, the rule is not.** Holders: `kama-shokunin/.ufo/waves/round-{25..32}/count-c*.py`,
`mado-shokunin/quality/counters/c1-r65-register.py` (sha256 `2ccedc68…`: "The counter reads git
objects at `--rev` only; it never reads the worktree"), `chousa` archive-extraction counters
(`.ufo/waves/round-46/gen-w1-spec.py`), `kaidoku` round-22/23/24 `count-c*.py`. mori's C1 should
cite mado's docstring as the cleanest statement of the read-at-rev discipline rather than present it
as new.

**Searched and absent from every sibling lane** (each grep run fleet-wide, `.git` excluded, and the
`*-shokunin/` glob includes mori, so the non-mori residue was checked by path):
`^# counter-sha256:` → 7 files, **all under `mori-shokunin/`** (chousa's `counter-sha256` is the
*label* inside `VERIFY-FAIL:` lines, not a header); `^# limits:` → 7 files, **all under
`mori-shokunin/`** (chousa's `## limits:` is a markdown heading in `gate-baseline-r12.md`); the
strings `GIT_CONFIG_GLOBAL`, `drift-classification-r82`, `DRIFT_CLASS`, `added-since-r10` → no
sibling *tool*; a sibling file that parses a recorded command **and executes it** → none.

**`^# replay:` — three non-mori hits exist and none is a receipt header; the earlier "0" is
corrected.** (a) `kasegi-shokunin/.ufo/waves/round-42/wave1/ExecJ1Evidence.sh:376` — a section
comment (`# replay: this family's committed defeat and the fresh mutants`); (b)
`mado-shokunin/.ufo/waves/round-48/w2/MutC2OneByte/receipts/mutant-matrix.tsv:3` — a TSV header
comment naming the replay *basis*; (c)
`kotodama-shokunin/reports/round-10/fix-02.md:59` — a report line quoting a replay summary
(`# replay: {"rows": 5, "reproduced": 5, "mismatch": 0, ...}`). Under mori's `REPLAY` regex
(`^#\s*replay:\s*(required|none)\s*$`) all three are unparseable, and none of them is a receipt body
header in its own lane's grammar either. `^# no-replay:` → 0 hits anywhere outside mori.

## 4 — Exact greps run (reproducible inventory)

```
# header grammars, per lane, strict anchors (whole checkout, .git excluded)
for d in *-shokunin; do grep -rl -E '^# cmd:' "$d" | wc -l; done        # kama 120 mado 73 kengaku 55 souji 27 tsukuroi 26 tameshi 21 chousa 19 kotoba 9 tabi 6 kasegi 3 kaidoku 2 kake 1
for d in *-shokunin; do grep -rl -E '^# rev:' "$d" | wc -l; done        # kama 39 kaidoku 2 mado 1 kotoba 1
for d in *-shokunin; do grep -rl -E '^# (cmd|rev|limits|counter-sha256|replay|no-replay):' "$d" | wc -l; done
# concepts
grep -rn --exclude-dir=.git 'drift-classification-r82' .
grep -rn --exclude-dir=.git -E 'mori-shokunin/\.ufo/waves/round-85/count-c[123]\.py|round-85/count-c[123]\.py' .
grep -rln --exclude-dir=.git -E 'counter-sha256|body[- ]versus[- ]command|replay.*receipt|receipt.*replay' .
grep -rn --include='*.md' -F 'counter-sha256' *-shokunin/
grep -rn --include='*.md' -F '# limits:' *-shokunin/
grep -rn --exclude-dir=.git -l -E 'value-changed|added-since-r10|DRIFT_CLASS' .
grep -rn --include='*.py' -E '(body|recorded|expected)[a-z_]*\s*(==|!=)\s*(out|stdout|live|actual)|(out|stdout|live|actual)[a-z_]*\s*(==|!=)\s*(body|recorded)' *-shokunin/
grep -rn --include='*.py' -E '^def [a-z_]*(replay|bind|receipt)[a-z_]*\(' *-shokunin/
grep -rn --include='*.py' --include='*.sh' --include='*.mjs' 'mori' *-shokunin/ | grep -v mori-shokunin/ | grep -v '/.ufo/waves/' | grep -v node_modules
grep -rn 'mori' tools/ scripts/                                    # fleet root
grep -rn --exclude-dir=.git -E '^#( |)(replay|no-replay):' *-shokunin/            # found the 3 non-mori hits in §3
grep -rn --exclude-dir=.git -E '\bcommand\b' --include='MANIFEST.tsv' *-shokunin/ | head   # found kotodama's command column
grep -rn --include='*.py' -E 'without ever executing|recorded_command_ignored|replay_isolated|replay-frozen' *-shokunin/
grep -rn --include='*.py' --include='*.sh' --include='*.mjs' '\bmori\b' *-shokunin/ | grep -v mori-shokunin/ | grep -v '/.ufo/waves/' | grep -v node_modules   # 83 lines / 14 files; tsukuroi 70 — THIS is what found tsukuroi's r27 register (32 hits in check-adjacency-overlap.py)
sha256sum <the files cited in §7>; git -C <lane> rev-parse --short HEAD
```
(`-F 'GIT_CONFIG_GLOBAL'` was also run fleet-wide; its hits are git-isolation boilerplate in
kake/kama probes — no receipt replay.)
False positives rejected while scanning: `tameshi` "DryBinder"/"binder.py" = cold-read ledger
binding (report → section → credit), unrelated to receipts; `audio` "replay" = verdict-function
replay over recorded fields; `tabi` `value-changed` = keystroke swallow; `kengaku` "memory" hits =
`memorized answer` in shortcut-readers, not mori.

## 5 — Contradictions, stated plainly (not smoothed into a score)

1. **This seat's rule already exists as a frozen counter in tsukuroi (r27 C2), with a closed class
   vocabulary** (`INBOUND-RESOLVES | INBOUND-DRIFTED | AGREES | CONFLICTS | LANE-GAP`, owners
   `mori | tsukuroi | contested`). My three words are a dialect of it. If mori writes an overlap
   record this round, it should reuse tsukuroi's classes or say it supersedes them — two vocabularies
   for the same act is exactly the drift these registers exist to catch.
2. **Duplicated mechanism, not a duplicated claim.** R1's mechanism exists four times in the fleet
   (kama r75, kengaku batteries, mado discrimination, tsukuroi `mutants-adjacency-overlap.py`).
   mori's C1 is still a distinct *movement* (arming a legacy counter's survivors), but a future
   contract should read "applies the r83 K2 rule, cf. kama r75" rather than "introduces mutation
   adequacy".
3. **The stronger statement on the shared r10 contract currently sits in another lane.** chousa's
   gate compares the baseline's declared volatile list and refuses on mismatch; mori's r86 C3 uses
   that list as a mask only. mori is not wrong (it grades a classification, not a baseline), but a
   claim of enforcement cannot be made without matching chousa.
4. **`# rev:` is two different bindings under one token.** kama: receipt path must exist at rev and
   its header rev must be an ancestor of the tip. mori: the rev's blobs are exported and the
   receipt's command re-run there. A shared receipt corpus would satisfy one and not the other.
5. **The one true `conflict` in this scan is kotodama on R2's decision, not its structure.** Given a
   recorded row whose `command`/`# cmd:` carries more than `<tool> <input>`, kotodama's
   `tools/replay-frozen.py` reproduces from the typed columns and never parses the command string
   (`recorded_command_ignored`), while mori's `count-c2.py` executes that string in `bash -c` and
   compares the body. Both are consistent internally; they cannot both be applied to the same
   receipt row. mori's design carries the injection surface kotodama's design removes, mitigated
   only by the scratch tree, `TMPDIR`, `GIT_CONFIG_GLOBAL=/dev/null` and a timeout — that mitigation
   is a risk note for the L1, not a defect in the C2 claim, but it should be stated in the C2 record
   rather than left implicit.
6. **R2 has no sibling holder that replays a recorded command string** — that reading is a *negative*
   result of the searches in §4 and is bounded by the bytes in §7 (I read every sibling checkout
   available: 20 sibling lanes of the 21 in the fleet). It is not a claim about lanes I could not see.

## 6 — Limits of this scan

* Read-only; nothing was executed from any sibling lane except `git rev-parse`/`git show`-class reads
  and `sha256sum`. No sibling counter or gate was run, so no verdict here rests on a sibling's
  *behaviour* — only on its committed bytes (docstrings, predicates, regexes, manifest columns).
* **Corrected in-flight:** my first pass filed kotodama as "no receipt gate" from the absence of
  `^# cmd:`/`^# rev:`. The `^# replay:`/`command` sweep found `tools/replay-frozen.py` and the D2
  manifest, and the verdict became `conflict`. The lesson to carry: absence of *mori's header
  tokens* is not absence of the *rule*; the manifest's `command` column is the same artefact under a
  different grammar. Any future overlap scan of this lane must grep for `command` columns and
  "replay" verbs, not only for `# cmd:`.
* The `^# cmd:` file counts are checkout-wide (wave scratch included) and therefore upper bounds on
  "lane conventions"; only the files quoted in §1 were read in full.
* Lane revisions move. A hit found here can be superseded by a sibling's later commit; the hashes in
  §7 are the bytes I judged.
* No claim is made about `.ufo/reports/*` prose beyond "it references mori's artifacts"; those are
  coordinator records, not tools.

## 7 — Bytes read (hashes of the files I actually judged)

```
mori-shokunin/.ufo/waves/round-86/count-c2.py                          fcc1d805b877f6dabc99ba7082fb414fd0e3b4c900822a1fd9ef5285675f8b97
mori-shokunin/.ufo/waves/round-86/count-c3.py                          6b7fc2ddb560f58cb155605510fbf4e3f3801d1766050219abdec2ca5c5668c9
mori-shokunin/corpus/knowledge/counter-mutation-adequacy-r83.md        5745a20020579afb881803cde6ba3fe647f6459b3e47a8d67a27fee7334bcf2a
mori-shokunin/corpus/knowledge/drift-pin-r10.md                        60ae38b54a8bbf5b8c989ac024151a47759bd6a3bb836860d38fa9b8b22791f7
kama-shokunin/tools/round75-survivor-probe.py                          255515165653d90cd30be6274b7baeb4c027e90f4ca9cad15b838ea2d625e989
kama-shokunin/tools/round72-receipt-tip-binding.py                     a9a4e8d30546a11e6d5165b566e856e4eb8cccb11d48c5526587fd3d859b2bbd
kama-shokunin/tools/round73-province-host-drift.py                     ec7bfd3fdf26be7338975c07443cdd15945f378d6f01774a70ef8e71934cd919
kotodama-shokunin/tools/replay-frozen.py                               a2fb5c98260a07f0801f4bf21f349283638da6796645780393262e4368c79464
kotodama-shokunin/tools/gates/frozen/round-3/MANIFEST.tsv              d5337590b343c65b42fd6e55457862fa325c138ad652e59c81b887daf9971399
kotodama-shokunin/reports/round-8/run-validation.py                    7eaa36789b4d71ce94ffadc93d2f5e10d6e0ca353df1c233d0ba94f29bff8369
tsukuroi-shokunin/tools/check-adjacency-overlap.py                     a10dd8dba25df34b52754f99e58e7a0831d4ea5f223044866bc1bf66907edd6b
tsukuroi-shokunin/corpus/knowledge/adjacency-mori-oom-r27.json         b094b889d7e13fe9aea750f2f63a2f43215b3a497c4d89ea3bdc3adb424acaa7
tsukuroi-shokunin/tools/mutants-adjacency-overlap.py                   b85a8b1bcade49418565bfa9ed1f95bef26c17a72a332f3004d524b41f1718fd
tsukuroi-shokunin/tools/tsukuroi-census.sh                             89026b9a8012a3da20501a5b0eaee3b6dec8b335ab72278214f325685399b1d6
chousa-shokunin/tools/research-gate.sh                                 d5d48128509f77edf161e4d8b10b833e6e00f822906460fa049f27d1244d41e2
chousa-shokunin/corpus/knowledge/receipt-binding-r38.md                c9fe9b2a0a6ba87fc453945eb737160b9f8658471a801ba2505ac27c14047331
chousa-shokunin/corpus/lessons/round-57.md                             b3f677b1c21e3147d9eb77b470309e17bd607ac74f1df713734a94f27d1b1c0c
kengaku-shokunin/corpus/QUALITY.md                                     c71405405f1e0f0f1b37b8517d44bda4c6faa81a5f2c204e07e7ad3ddfb3fef7
kengaku-shokunin/corpus/lessons/round-37.md                            d92cbf2e04a16179b9dc636562f972cc976f0d72927c552ac99821e0621bf0ca
mado-shokunin/quality/check-counter-discrimination.py                  e396b95eff5b1f6a4212866a134f690eeef8bb59878c3b97dde4bd48ea5ddb86
mado-shokunin/quality/counters/c1-r65-register.py                      2ccedc6852a35a8cfbaaf8a92b1ad473c1464499cc892fa8753dc199eaaa1871
```
Unhashed but quoted (read-only, one section each): `chousa-shokunin/corpus/knowledge/receipt-digest-provenance-r67.md`,
`chousa-shokunin/corpus/evidence/round39/verify-receipts.py`,
`kumitate-shokunin/SKILL.md:94-127`, `kotodama-shokunin/.ufo/waves/round-79/w1/stage/RevFreeze/freeze-matrix.py`,
`tabi-shokunin/.ufo/waves/round-58/counters/R58Counter.md:37-46`,
`audio-shokunin/corpus/live/r89-critic/replay.py`,
`kama-shokunin/.ufo/waves/round-79/measured/after/c1-green.out`,
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-85/mori.md:149-151,205`.
