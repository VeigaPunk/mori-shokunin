# ScoutQualityBar — QUALITY criteria governing round-40 claims + receipt rev-naming audit

Scope: `corpus/QUALITY.md` (926 lines, read in full at HEAD `ede486b7`), every file
under `.ufo/waves/round-40/evidence/`, `contract.md`, `w1-spec.json`,
`fixtures/run-c11-dags.py`, `corpus/lessons/round-40.md`, `corpus/lessons/round-39{,-verifier-spotcheck}.md`,
`corpus/evidence/sources-r40/S229.src`, `corpus/SOURCES.md` S229 row.
All file observations are of working-tree bytes at HEAD `ede486b7a09afbacfb380d5871c46a8051a6dc2e`
(scored tip `265a955cc67be4eae97d2dc5a9338a25f31eb29b`; entering tip
`bb1f2457bb8d3e8d5dfe98488b91e8c02e378ca3`).

## 1. The criteria that govern the round-40 claims

QUALITY.md holds the claim-admission bar; its last entries are 112–113 under the
round-38 heading — no criteria were added in rounds 39–40, so nothing new binds
this round beyond the standing text. Grouped by the three themes the item named:

### a) Measurement discipline — "a verdict names the revision" and friends

- **#1–#5 (admission bar):** falsifiable; measured anchor (path:line, command,
  evidence id); observation/inference/unknown kept separate; errata append-only;
  rejections kept.
- **#9:** every path/line/commit pointer resolves at the carrying commit; a report
  names the commit that carries its work; replacements sweep every mention.
- **#12:** no cumulative counter read without its baseline/window anchor.
- **#20:** a tally cites the counted universe recomputed from delivered artifacts.
- **#22:** an evidence timestamp is no later than the commit that carries it.
- **#23:** a /tmp path is never evidence; commit the fixture generator and a digest
  (the r40 freeze pins the *builders* — `make-survivor-fixtures.py`,
  `run-c11-dags.py` — plus instrument bytes; generated-fixture digests are not
  pinned, but the bytes are committed under `fixtures/generated/`).
- **#25:** a claim is admitted at the scope it was measured.
- **#31:** a verdict-producing gate needs its registry row; a self-test tally names
  the revision and is measured on delivered bytes.
- **#33:** a receipt's provenance is the identity+content of every verdict-driving
  input, hashed at load and end.
- **#52:** a `pre-build` freeze label is a verdict of the freeze-order check, not
  prose (freeze-r40.txt is `sha256`-pinned, `pinned: 2026-10-24T05:46:06Z`).
- **#55:** frozen rule beats contradictory example; executor reports the conflict.
- **#58:** a freeze-order receipt carries measured full commit, input digests,
  script digest, resolved bases/tips, overrides, argv.
- **#68:** a bound artifact is re-run from its original revision, never a sanitized
  copy — the `fixtures/extracted/*-bb1f2457.py` bytes run via `git show
  bb1f2457:<path>` satisfy this.
- **#70:** every reconciled count names its exact population, measured commit and
  policy-excluded identities.
- **#76:** a self-test evidence file names the **full 40-hex** measured commit, the
  command, the tool blob, fixture tree and exit code, and carries the full stdout
  (born from r24 D1, which is `c11-after-selftest.txt`'s exact shape — see §3).
- **#78:** a counting command reads every input from committed bytes at a named
  revision; refuses bad revisions, missing files, short input lists (exit 2).
- **#84/#87/#88:** tip receipts name the full 40-hex first parent, the tip batch
  adds only receipt files, receipts cited in LOG.md/lesson.
- **#95:** a judge receipt names the sha256 of judged bytes, not only a revision.
- **#109 (as corrected by #111):** a drawn-arm measurement is replayable only with
  the tip it drew from; runnable form is `conform.py <rev> --selftest --counter …`.
  (Plus note: the recorded pin is HEAD, not the drawn rev.)
- **#113:** registry quote corrections ride a superseding row, never an in-place
  edit — S229 is an append-only row (QUALITY 81/102 also bind it).

### b) Fix shown able to fail — controls, mutants, kill rules

- **#13:** pre-registered expected gradient (exact tally + PASS set against frozen
  gate SHA) — the contract's kill rules and named expected FAIL per survivor.
- **#26:** a census verdict is exactly one complete verdict record agreeing with
  its exit code.
- **#32:** a mutation witness states the exact code delta it installs and the
  causal scope it does not establish (`conform-*-conjunct-gutted.py` witnesses
  name the gutted mutation-table entry).
- **#91:** a gate enters a counted condition only with a committed selftest that
  shows it discriminates (clean input → 0; every planted class → a violation) —
  `CONFORM_SELFTEST pass=11` and `MORI_SOURCES_APPENDONLY_SELFTEST pass=15` are
  the r40 arms.
- **#98/#99/#101:** pre-data leg-rejection-shape controls; shortcut controls
  (label-keyed, harness-keyed); a met control's fields must be full/non-denying —
  the r40 survivor fixtures + multicounter + gutted-conjunct controls play this
  role (do-nothing control = r39 bytes on r40 fixtures, per contract §hygiene).
- **#106/#107:** discrimination checked against an arm-detector, not a constant;
  per-id lines checked, not only summaries — the C2 fixture DAGs (dag-n/p/r) are
  exactly these arms.
- **#94 (supersedes #93):** a gate carries a counted condition only with a
  pre-freeze, fully-adjudicated receipt of the frozen gate blob on the round's own
  inputs — the c10-red/c11-red series is the before side of this.
- **#110/#112:** supersede timing is ancestry-based; P-C11 extends the eligible
  set — the criterion whose check the v3 gate now implements.

### c) Quote word counts and Gate hygiene (frontier/lesson leg)

- **#60:** rejected source rows need a located quote ≤25 words or an explicit
  unavailable limitation (round-40 Gate: "Rejected: none new" — declaration form).
- **#86:** the Gate records every reject decision; none met → `reject sample:
  none met` declaration. Round-40 uses the equivalent "Rejected: none new" prose;
  whether that satisfies #86's exact-token requirement is a reviewer question
  (the check greps for the literal `reject sample: none met`).
- **#89:** absence-asserting reject reasons carry the exact `grep` invocation and
  output — n/a, no absence rejects this round.
- **#90:** every `(N words)` label equals `wc -w` of the quoted text; off-by-one is
  a defect, not rounding. **Fired in round 40 — see finding F1.**
- **#105 (SOURCES freshness witness):** compare source full-document sha256
  against the open-time copy — S229 copy is `corpus/evidence/sources-r40/S229.src`.

Also in force but not triggered: #37 (dispatch carries restrictions — the wave
context does carry the full VCS/tooling bounds), #38/#39 (seat write bounds;
selftest-writer≠selftest-runner), #54/#64/#66 (settlement scan, stub≠report),
#44/#53/#56 (context/dispatch binding), #83 (dated headings read from clock/git).

## 2. Receipt rev-naming audit (r39 finding-9 discipline)

r39 finding 9 (`round-39.md:72-75`): `c7-after.txt` recorded the command rev
`f920eaf7` (a data commit) rather than the scored tip `13bfba23` — measurement
stood, receipt naming was wrong. Round-40's contract adopts "receipts name the
measured revision." Observed, per file:

### Names the measured rev — PASS

| receipt | how named |
|---|---|
| `c10-after*.txt` (13 files) | `command:` line carries full 40-hex `265a955cc…` **and** `check head_pin` echoes `pin=265a955cc… tip=265a955cc…` |
| `c10-red-*.txt` (9 survivor + multicounter) | `command:` carries `bb1f2457` (prefix, resolves to the entering tip — verified `git rev-parse bb1f2457` = full hash) and `head_pin` echoes the full hash |
| `c10-parity.txt` | header names `bb1f2457` (prefix) + sha256 of both counter blobs |
| `c11-before-lane.txt` | `command:` names `bb1f2457` + instrument path `gate-v2-bb1f2457.py` |
| `c11-after-lane.txt` | `command:` names full 40-hex `265a955cc…` |
| `c11-after-e37dcc6.txt` | `command:` names `e37dcc6` (prefix; resolves to `e37dcc6dffde…`) |
| `freeze-r40.txt` | names `bb1f2457` (prefix) + sha256 pins for every frozen path |

### Rev-naming gaps — findings

- **F2 — `c11-after-selftest.txt` (3 lines) names no revision at all.** The file is
  `command: python3 tools/mori-sources-appendonly.py --selftest` /
  `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0` / `EXIT=0`. No rev, no tool-blob
  digest, no fixture tree. This is the exact shape QUALITY **#76** was written
  against (r24 D1: a selftest file naming no revision is stale-adjacent evidence).
  Qualification [INFERENCE]: the tool is a *tracked* path; the freeze pin
  `bde5a9a3…` binds its bytes, so the omission is recoverable from
  `freeze-r40.txt` — the defect is naming, not binding.
- **F3 — `c10-red-conjunct.txt` and `c10-after-conjunct.txt` are selftest receipts;
  #76's full-40-hex bar applies.** Red side names only `bb1f2457` (prefix) in the
  command; the after side names the full hash — asymmetric. The mutated checker
  (`fixtures/generated/conform-r39-conjunct-gutted.py`,
  `conform-v3-conjunct-gutted.py`) is not pinned in `freeze-r40.txt` by sha256; the
  generated bytes are committed, so identity is recoverable but not receipt-bound.
- **F4 — the six DAG receipts (`c11-red-*.txt`, `c11-after-fixture-*.txt`) name no
  lane revision and no fixture-tip hash.** `run-c11-dags.py:51-54` runs
  `<gate> HEAD --repo <tmp dag>` inside a mkdtemp under `.scratch`; the receipt
  records only `command:` (script path + lane path + out path + kind) and the
  section header `(dag-*, --round-base b0=07be6c7f1765)` — a **truncated** base sha
  of an ephemeral repo whose tip SHA is never printed. For the *after* receipts the
  gate path is `tools/mori-sources-appendonly.py` (working tree): the receipt does
  not record which lane rev the tree matched; only the freeze pin closes that.
- **F5 — `census-start.txt` / `census-end.txt` carry no `command:`, no revision, no
  timestamp, and no recorded exit code.** Both files are byte-identical
  (`cmp -s` → identical): 16 `W04` duplicate-url rows + `mori ok` row. The contract
  claims "census exit 0" twice; neither receipt can show its own exit — a
  finding-9/QUALITY-33 class gap. The identity of start and end is consistent with
  [INFERENCE] no SOURCES change between the two runs other than S229's landing
  (which adds no new warning class), matching `round-40.md`'s claim.
- **F6 — `evidence/.parity-c7.txt` / `.parity-c8.txt` carry no command or revision
  line at all** (line 1 is the P-C7 predicate). Dotfiles — likely internal parity
  captures, not cited receipts; flagged for completeness, low severity.

## 3. Findings

- **F1 — word-count label defect (QUALITY #90; repeats routed defect 4's class).**
  `corpus/lessons/round-40.md:7` S229 Gate row labels its quote **"(15 words)"**;
  the quote `"When a name is used in a code block, it is resolved using the
  nearest enclosing scope."` measures `wc -w` = **17**. Verified against the
  committed source copy `corpus/evidence/sources-r40/S229.src:294-295` ("When a
  name is used in a code block, it is resolved using the nearest enclosing scope."
  — byte-faithful quote; off by 2, not 1). The `corpus/SOURCES.md:235` S229 row
  carries the same quote **without** a label, so only the lesson cell fails #90.
  This is the third instance of the one/two-off quote-label defect class
  (r29: five labels; r39 routed defect 4: S227 18-vs-17).
- **F7 — second number-drift: the committed lane receipt lists 35 as-of ids, not
  34.** `c11-after-lane.txt:22` `superseded_as_of=` contains exactly 35 ids
  (18 original + 16 never-edited + S226 = 35; enumerated below). Both the wave
  context ("34 as-of ids") and `round-40.md` M24 ("lists **34** as-of ids", "16
  rows: S226 plus 15 earlier") state 34 — which is itself arithmetically wrong:
  18 + 16 = 34 only if the "16 rows" **includes** S226 (18+16=34), but 18+15+S226
  = 34 also parses; the counted receipt says **35**, i.e. 18 unchanged + 17 newly
  eligible (S226 + 16 earlier). Either the receipt regenerated after M24 was
  written, or M24 counted wrong. Both claims cite the same tip `265a955cc`;
  reviewers should diff the lesson's 34/16 against `c11-after-lane.txt`'s 35/17.
  [INFERENCE] The "16 rows" phrasing suggests the lesson counted the extension
  set as 16 where the receipt admits 17. Exact 35 ids: S041,S044,S051,S062,S064,
  S067,S069,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,
  S131,S140,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193,S226.
- **F8 — `run-c11-dags.py` truncates the fixture base hash** (`shas[base_name][:12]`)
  and never records the fixture tip SHA; combined with F4 the DAG receipts are
  the least-bound receipt set in the round (deterministic builders presumably
  reproduce them, but the receipt itself is not self-identifying).

## 4. Commands run (verbatim)

- `read` ranges over `corpus/QUALITY.md` (1-300, 301-600, 604-926) — full file.
- `grep -nE 'rev|revision|commit|bb1f2457|265a955|HEAD|sha' evidence/` — every
  receipt; output cited above.
- `git -C <lane> rev-parse e37dcc6 bb1f2457 265a955cc` →
  `e37dcc6dffde8e74d5f0b89b002586390c65e6fa`, `bb1f2457bb8d3e8d5dfe98488b91e8c02e378ca3`,
  `265a955cc67be4eae97d2dc5a9338a25f31eb29b`; `HEAD` = `ede486b7a09afbacfb380d5871c46a8051a6dc2e`.
- `printf '%s' '<quote>' | wc -w` → **17** (lesson label says 15).
- `python3` count of `superseded_as_of=[...]` on `c11-after-lane.txt:22` → **35**
  ids; `stale_supersede=[]`.
- `cmp -s census-start.txt census-end.txt` → byte-identical;
  `grep -c EXIT` → 0 in both.
- `grep -nE '\([0-9]+ words?\)' corpus/lessons/round-40.md corpus/SOURCES.md` →
  exactly one label, the S229 row's (15 words).

## Residuals / unknowns

- Whether "Rejected: none new" satisfies QUALITY #86's literal `reject sample:
  none met` check — [INFERENCE] the r40 check would need to accept this phrasing;
  not adjudicated here.
- Whether F7's 34-vs-35 reflects an older T1 receipt superseded by the committed
  one — needs the receipt's commit ancestry, outside this seat's read scope.
- Fixture determinism of `run-c11-dags.py` (timestamps env-frozen via
  `gate._selftest_env()`) assumed, not re-run — re-running is an executor seat's job.
