# Mo87Si01Simplify — round 87 w1: dead weight in the two frozen counters and the six new arms

seat: `Mo87Si01Simplify` (leaf, no dispatch) · lane: mori · round 87 · attempt 1 · wave w1
date: 2026-11-04 · axis reported on: operability
scope: read-only. No counter was edited; no lane commit, no git/jj mutation in the lane repo.
Entering `6fc09d69edbb11e5070ff33258de49f062c0fb9b`; freeze `142542e0d853b4e8ec1aa1adb86708dc5786d9c0`;
C1 target `03b66a437e68d493ce0aacd1d80c321cc2e6bf7c`; C2 target `98f48dba3267a73714b862d0fd4fc8c0e82a1d04`.

## Files read, and the bytes I actually read

| path | sha256 | note |
|---|---|---|
| `.ufo/waves/round-87/contract.md` | `afa154ff5db5058e5dbd5bbbf4c80f73ecf0222f0419daaa2f7a802ff822e11a` | worktree; includes A1 and the post-data erratum E1 |
| `.ufo/waves/round-87/count-c1.py` | `e2ff968721678cc61d6a1674def8da3e27a43f3fed8daab79d53c657ae2c266e` | worktree; `git diff HEAD` empty; frozen at `142542e0` |
| `.ufo/waves/round-87/count-c2.py` | `264a43f04af1f9f939da7b3890f608a669a0c7fc2922656ee83f35adb236b14d` | worktree = `142542e0` + A1 (`b9e6f68d`, 9 lines) |
| `.ufo/waves/round-86/count-c1.py` @`03b66a43` | `bcd66561093aa3046739f2be57a5f418e1ce87dd2da451beaece1e6ecffd5e7a` | `git diff 03b66a43 -- .ufo/waves/round-86/` empty |
| `.ufo/waves/round-86/count-c2.py` @`03b66a43` | `28d667338674402fa6e72aa9c567f3f18c2387e4f8c1f0f5e4c63a894e02c584` | same |
| `.ufo/waves/round-86/count-c3.py` @`03b66a43` | `2e618dce42b38418e85868e48f4da2c895c39dcb634fd5626c5761818927a760` | same |
| `.ufo/waves/round-87/evidence/controls-r87.txt`, `probe-r87.txt` | read | frozen receipts, not re-measured |

## 0. What I measured (so the report rests on runs, not reading)

All runs used a private scratch base (`/fast/scratch/hyaku/mori-r87/Mo87Si01Simplify/tmp`) via `--scratch`; `python3 -I` throughout.

- `count-c1.py 03b66a437e68d493ce0aacd1d80c321cc2e6bf7c` → six `MUTANT … killed rc=1` lines then
  `C1=met mutants=6 killed=6 survivors=0 total=6 arms=54 rev=03b66a437e68`, rc 0.
- `count-c2.py 98f48dba3267a73714b862d0fd4fc8c0e82a1d04` → `C2=met receipts=7 absent=0 bindings=9
  bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1
  unexpected=0 rev=98f48dba3267`, rc 0. This is the **canonical form per erratum E1**: counter bytes
  at `b9e6f68d` (the worktree counter is byte-identical to it) over subject `98f48dba`.
  I also measured the **pre-A1** frozen counter (`142542e0` bytes, scratch sha256 `e1dfd45a…`) over
  `98f48dba`: it prints the whole target tail `receipts=7 … unexpected=0`, then
  `subject=selftest arms=(13, 0) labels=True`, rc 1 — the sub-gate is the sole difference between a
  receipt-perfect tail and `C2=met` (E1's F1, re-measured by me).
- `--selftest`: `count-c1.py` 18/0, `count-c2.py` 17/0; r86 copies at `03b66a43`: 18/0, 13/0, 23/0.
- Six-mutant matrix **at `03b66a43`** (each r86 copy mutated with the frozen `old`→`new`, own
  `--selftest` re-run): each mutant fails **exactly one** arm, and it is the arm added for it —
  `M1`→`unanchored_plus_killed_unmet`, `M2`→`zero_mutants_unmet`, `M3`→`arms_tally_from_subject`,
  `M4`→`summary_required`, `M5`→`binding_required`, `M6`→`derive_keyshape`. No pre-existing arm
  fails under any of the six (consistent with `probe-r87.txt`'s "survived" at `6fc09d69`).
- Not re-measured by me: the entering/label-only/header-only controls at `6fc09d69` and
  `bc108f00`/`bc319680`; I read them in `controls-r87.txt` and do not restate them as my own.

## 1. Item 1 — dead weight in the two new counters

### 1.1 `count-c1.py` re-carries the M1 clause it grades in the r86 counter, with no arm that can see it (highest-value finding)

The counter's own `unanchored_plus_killed_unmet` arm (`.ufo/waves/round-87/count-c1.py:240-245`) does
not contain an unanchored mutant and does not contain a killed mutant:

- fixture `zero.py` = `print('FAKE pass=1 fail=0')\nGUARD = 1\n` (`:240`); `GUARD` is never read, so
  the mutation `GUARD = 1 → GUARD = 0` leaves a green, surviving copy;
- `GUARD = 1` occurs once, so the mutant is anchored, not unanchored;
- `zero.py` prints no `COUNTER_SELFTEST`, so `arms_of(out) = (-1,-1)` and the `want_arms=1` floor
  (`{"zero.py": 1}`, `:243`) marks the pristine red too.

Measured pristine print: `PASS unanchored_plus_killed_unmet mutants=1 killed=0 survivors=1 total=1 arms=0`.
The arm passes only because the string `unanchored` occurs in the extra line
`survivor tools/zero.py M1-unanchored-conjunct` — i.e. in the mutant **label**, not in a detected
unanchored occurrence. So the assertion `"unanchored" in " ".join(extras)` is satisfied by the label.

Proof by mutation (measured): replacing the counter's own
`met = (pristine_ok and total > 0 and survivors == 0 and not any(e.startswith(("empty-mutation", "unanchored")) for e in extras))`
with `… and True` leaves `C1_COUNTER_SELFTEST pass=18 fail=0`, rc 0. The same clause is armed in
two of the three clauses it shares: `total > 0 → >= 0` is killed by `zero_mutants_unmet` (rc 1),
and `arms_total += max(passed, 0) → TARGET_ARMS` is killed by `arms_tally_read` (rc 1). So the file
is 2/3 armed on its own clauses; the unanchored conjunct is the gap.

The r86 original (`@03b66a43`, `.ufo/waves/round-86/count-c1.py:246-251`) uses `dup.py`
(two occurrences → genuinely unanchored) **plus** `sensitive2.py`, a copy of the GUARD-sensitive
program, so its fixture has both properties the name claims. The r87 port kept the name and the
assertion but dropped both halves of the fixture. `unanchored_excluded` (`:234-239`) and
`empty_mutation_unmet` (`:248-253`) are likewise satisfied by `total == 0` (the total floor), not by
the unanchored/empty conjunct; they were already that way in r86. Net: three arms in the new counter
have titles about the unanchored/empty clauses, none of them kills M1.

### 1.2 `count-c1.py` — the tallies are three fields over two independent quantities (frozen; do not delete)

`:181` prints `mutants=%d killed=%d survivors=%d total=%d arms=%d` from
`% (total, killed_n, survivors, total, arms_total)` with `killed_n = total - survivors` (`:178`).
So `mutants ≡ total` and `killed ≡ total − survivors` by construction. `COUNT` (`:75`) parses
`mutants`, but `target_split` (`:118-120`) reads only `killed`, `survivors`, `total`, `arms` — no
assertion ever reads `mutants`. The value is a write-only duplicate. **Cannot be deleted**: the
frozen target string `C1=met mutants=6 killed=6 survivors=0 total=6 arms=54` and the contract sentence
require the exact bytes. Reader cost of keeping: three numbers look like three independent checks;
only `total` and `survivors` (and `arms`) are. Worth one line of comment, not a deletion.

### 1.3 `count-c1.py` — small dead weight

| path:line | dead weight | evidence |
|---|---|---|
| `count-c1.py:194` | `return path` in nested `write()` — every call site ignores the return | read; `write(d, …)` used 6×, never bound |
| `count-c1.py:81` | `run(…, timeout=300)` — `timeout` is never passed by any caller | grep: five `run(` call sites (`:92,295,297,304,307`), none with `timeout` |
| `count-c1.py:269-270` | `marker_literal` arm asserts `"M1-unanchored-conjunct" in open(__file__).read()`; the literal is in `MUTANTS` at `:59`, so the arm is a source self-reference, not a detection | read; mutation-free by construction |
| `count-c1.py:152` | `want_arms is not None` — never false: `ARMS_BY_FILE` keys every subject (`:48-52`) and every fixture passes a keyed dict | coverage: branch not taken; read |
| `count-c1.py:292-325` | `main`'s rev path (expected: selftest path only) | coverage report: 79% stmt, missing `93-94,137-138,140,292-325` |
| `count-c1.py:28` | docstring "files only under `--scratch`" is false in the canonical invocation: `base` falls back to `tempfile.gettempdir()` (`:286`) when neither `--scratch` nor `HYAKU_SCRATCH` is set, and the contract's P-C1 command passes no `--scratch` | read of `main` |

`per_file_arms_frozen` (`:265-267`) is **not** redundant: the dict equality pins 18/13/23 and the
`sum(...) == TARGET_ARMS` conjunct pins `TARGET_ARMS == 54`; each can fail alone.

### 1.4 `count-c2.py` — the grading core is unreachable from `--selftest`

Coverage of `count-c2.py` under `--selftest`: **38% stmt, 126 branches, 182 missed**. Unreached
entirely: `export_rev` (`:150-172`), `replay_body` (`:170-200`), `sha256_at` (`:203-208`),
`ancestor` (`:211-214`), `grade_population` (`:217-303`). The 17 arms cover `header_and_body` and the
supersede helpers only. Consequence, measured: the same two mutants C1 added arms for in the r86 copy
**survive** here —

- `:250 if token in body:` → `if True:` → rc 0, `C2_COUNTER_SELFTEST pass=17 fail=0`;
- `:262 if measured == sha:` → `if True:` → rc 0, `pass=17 fail=0`.

So the new C2 counter re-carries the M4/M5 clauses without any arm over them. By contrast the new
supersede rule itself is armed (`supersede_verdict` `name in clean_names` tampered → rc 1, `FAIL
supersede_absent_target`, `FAIL supersede_requires_clean`). Two copies of one rule now exist
(r86 `count-c2.py:250/262` armed; r87 `count-c2.py:250/262` unarmed), and the unarmed copy is the one
the C2 claim runs. This is a test gap, not deletable code: the `else` branches (`:252-253`, `:264-265`)
are also unreached at the graded revision (`summary=7` of 7 receipts, `bound=9` of 9 bindings), so
they are neither tested nor exercised at `98f48dba`.

### 1.5 `count-c2.py` — docstring sentences contradicted by the code

- `:16` `` `# replay: legacy` receipts are header-bound only … `` — the parser has **no `legacy`
  value**: `REPLAY = r"^#\s*replay:\s*(required|none|clone)\s*$"` (`:53`). `legacy` is a POPULATION
  column (`:39-47`), not a header value; a literal `# replay: legacy` line would be ignored and add no
  problem. The sentence invents a header value.
- `:20` `Read-only: `git show`, `git clone --shared`; files only under --scratch` — contradicted twice:
  (a) `replay_body` executes the receipt's command with `bash -c cmd` (`:195`), so the counter is only
  read-only if the receipts' commands are; (b) the same `tempfile.gettempdir()` fallback as 1.3 puts
  the scratch under `/tmp` when `--scratch`/`HYAKU_SCRATCH` are unset.
- `:70` `header_and_body` says the body "keeps no trailing newline"; code `.rstrip("\n")` also strips
  a body that legitimately ends in newlines — intended (the replay compare does `out.rstrip("\n")`),
  but the sentence overstates: it strips all trailing newlines, not one.

### 1.6 `count-c2.py` — parameters never passed, dead initializers, redundant guards

| path:line | dead weight | evidence |
|---|---|---|
| `count-c2.py:220-222` | `counts` initializers `"legacy": 0, "superseded": 0` | both assigned unconditionally at `:295`; never incremented in the loop (`grep` shows no `counts["legacy"] +=`) |
| `count-c2.py:217` | `population=POPULATION` parameter | the only call is `:435` with 4 args; nothing in this file passes `population=` (the r86 copy uses it at `:296-303`) |
| `count-c2.py:170` | `mode="required"` default | only call `:270` passes `mode` |
| `count-c2.py:65` | `run(…, timeout=900)` | `timeout` never passed |
| `count-c2.py:155` | `not token` and `token.startswith("-")` | both subsumed by `PATHISH.match` (`:62`) — empty and a leading `-` cannot match; deleting both is behavior-identical |
| `count-c2.py:212-213` | `if rev == tip: return True` | same answer as `merge-base --is-ancestor` for equal commits; keep (saves a subprocess), not dead weight |
| `count-c2.py:419-422` | `missing` precheck | duplicates `labels_ok` (`:432`); distinct message only |
| `count-c2.py:267-268` | legacy→required promotion | unreached at `98f48dba` (no legacy POPULATION row carries `# replay:`); untested. Keep: it is the r86 inheritance rule |
| `count-c2.py:298-302` | superseder naming an absent target | unreached at `98f48dba` and untested; keep (guards a malformed successor) |
| `count-c2.py:369-370` | `subject_arms` arm | see §3 |
| `count-c2.py:371-372` | `marker_literal` (`"supersede_verdict"` in own source) | same self-reference shape as 1.3 |
| `count-c2.py:394-457` | `main`'s non-selftest path | expected |

## 2. Item 2 — do any of the six new arms duplicate an existing arm?

**Measured answer: no duplicate kill.** Each of the six mutants fails exactly one arm at `03b66a43`,
and that arm is the new one added for it (§0). No pre-existing arm fails under any of the six; the
entering probe confirms they were green at `6fc09d69`. So none of the six is a duplicate kill.

One **assertion-level** pair does exist, and it is the only one:

- new `unanchored_plus_killed_unmet` — `.ufo/waves/round-86/count-c1.py:250-251`
- existing `unanchored_excluded` — `.ufo/waves/round-86/count-c1.py:229-230`

Both assert the **same expression verbatim**:
`(not met) and "unanchored" in " ".join(extras)`. The fixtures differ (one unanchored mutant only vs
one unanchored + one anchored-killed). The overlap is not a duplicate kill: `unanchored_excluded` is
green under M1 because the fixture's `total == 0` already forces `met` false, so it cannot see the
`met` conjunct; the new arm's fixture forces `total == 1, survivors == 0`, which is what makes
`not met` discriminate. Measured: M1 → only `unanchored_plus_killed_unmet` fails.

Two consequences for the simplification ledger:

1. The shared second conjunct is **not discriminating in either direction**: the unanchored extra is
   emitted in every state of both fixtures, so `"unanchored" in extras` is always true and the kill
   comes from `not met`. The substring is also unsafe in this file because the mutant labels
   (`M1-unanchored-conjunct[ -old]`) contain it — §1.1 shows the r87 port passing for that reason.
2. The r86 pair makes the old arm the redundant one (the new fixture is a strict superset of the old
   one's assertions); deleting `unanchored_excluded` would be the honest simplification, but it is
   blocked by the frozen 18-arm count (see §4).

The other five new arms have no pair at all: `zero_mutants_unmet`'s `"total=0" in tail` is not
asserted elsewhere; `arms_tally_from_subject` is the first arm on `grade()`'s tail (`arms_parse`
tests `arms_of` directly); `summary_required`/`binding_required` are the first arms to call
`grade_population` on a fixture in that file; `derive_keyshape` is the first arm on `derive()`'s
non-keyshape branch (`derive_key_unknown`, `count-c3.py:216-217`, exercises the keyshape branch).

**Naming defect in `derive_keyshape`** (`.ufo/waves/round-86/count-c3.py:262-263`): `KEYSHAPE =
r"^[A-Za-z0-9_]+$"` (`:39`); `foo*bar` does **not** match it, so the arm exercises
`if not KEYSHAPE.match(body): return "value-changed"` — the *non*-keyshape branch, exactly the clause
M6 mutates (the contract calls M6 "the non-keyshape branch of `derive()`"). The arm is correct and
load-bearing; its label names the opposite branch. A reader looking for keyshape coverage will believe
it exists here when it is `derive_key_unknown`.

## 3. Item 3 — does `SUBJECT`/`SUBJECT_LABELS` still earn its place after A1?

Measured reading of the code path:

- `SUBJECT`, `SUBJECT_ARMS`, `SUBJECT_LABELS` (`.ufo/waves/round-87/count-c2.py:32-36`) are used in
  exactly two places: the gate in `main` (`:415-433`) and the `subject_arms` constant arm (`:369-370`).
- `grade_population` never reads `SUBJECT`; it reads receipts and git only (`:217-303`). So the
  sub-gate cannot change the receipt verdict in either direction — it can only turn a would-be
  `C2=met` into `C2=unmet subject=…`.
- **Measured** (my run, §0): the pre-A1 frozen counter over `98f48dba` shows exactly that — the full
  tail is the target tail and the run still exits 1 on `subject=selftest arms=(13, 0) labels=True`.
  It is a false unmet at the claim's own revision, produced only because another file gained two
  arms. Nothing the gate reads is an input to the receipt measurement, so it cannot produce the
  opposite error (a false met); its only possible correction is downward.
- The arm-count half is an exact duplicate of C1's authority: `ARMS_BY_FILE["count-c2.py"] = 13`
  (`count-c1.py:48-52`) already requires that same file's pristine selftest to be green with 13 arms,
  and C1 additionally grades M4/M5 in it. The marginal information is the **label names**.
- One of the 13 labels it certifies is a tautology: `export_lists_token`
  (`.ufo/waves/round-86/count-c2.py:265`) is `cases.append(("export_lists_token", True, …))` — a
  literal `True` — and its computation `listed = export_rev(...)` (`:264`) is an unused local
  (pyflakes `F841`). `labels_ok` is therefore partly a check that a cannot-fail arm still prints.
- A1 is the bill: moving 11→13 and appending two labels (`b9e6f68d`) was required to keep
  `C2=met` byte-identical after an unrelated file's arms changed. The frozen predicate P-C2 in the
  contract names **no** subject gate; the counter is stricter than its own claim, and the strictness
  is what A1 had to chase.

**Verdict: it does not earn its place as a second arm-count authority.** It adds label-name pinning
(the weakest half, with one tautological label) at the cost of a second frozen number over another
file's internals, plus a disclosed amendment whenever that file's arms move. C1 already tripwires the
same file harder (13 arms + two killed mutants). Retire the sub-gate as a unit in the next round
(exact ranges in §4); it cannot be retired now — the counter is frozen, A1 is pre-data, and both
controls already read the gated counter.

## 4. Item 4 — exact deletions proposed (none applied)

Rule used: delete only what cannot change a frozen target, a frozen arm count, or a claim's verdict.
"Cost to reader" is what the reader loses, not what the code loses.

### Safe now (no frozen dependency)

| path:line | deletion | effect | cost to reader |
|---|---|---|---|
| `.ufo/waves/round-87/count-c1.py:194` | `return path` in `write()` | none (return never bound) | none |
| `.ufo/waves/round-87/count-c1.py:81` | `timeout=300` parameter of `run()` (hardcode at the `subprocess.run` call) | none | a knob nobody turns; reader no longer has to check callers |
| `.ufo/waves/round-87/count-c1.py:269-270` | `marker_literal` arm | selftest 18→17; P-C1 does not name this file's own arm count | loses a check that cannot fail; reader trusts the remaining 17 more |
| `.ufo/waves/round-87/count-c2.py:222` | `"legacy": 0, "superseded": 0` initializers | none (assigned at `:295`) | the dict no longer lists two keys that are overwritten; both still appear at `:295` and `:443` |
| `.ufo/waves/round-87/count-c2.py:155` | `not token or token.startswith("-")` | none (`PATHISH` already rejects empty and leading `-`) | none; one guard remains instead of three |
| `.ufo/waves/round-87/count-c2.py:170` | `mode="required"` default | none (only call passes `mode`) | none; a default that was never taken suggests an API that does not exist |
| `.ufo/waves/round-87/count-c2.py:65` | `timeout=900` parameter | none | as above |
| `.ufo/waves/round-87/count-c2.py:371-372` | `marker_literal` arm | selftest 17→16 | as above |

### Docstring corrections (delete the false sentence, keep the code)

| path:line | correction |
|---|---|
| `count-c1.py:28` | "files only under `--scratch`" → "under `--scratch`/`HYAKU_SCRATCH`, else `$TMPDIR`" (`:286` is the fallback) |
| `count-c2.py:16` | delete `` `# replay: legacy` ``; write "a receipt with no `# replay:` line is legacy" (`REPLAY` has no `legacy` value) |
| `count-c2.py:20` | "Read-only: git show, git clone --shared" → add that `replay_body` executes the receipt's `cmd` via `bash -c` (`:195`), so read-onlyness holds only for read-only commands |
| `count-c2.py:70` | "keeps no trailing newline" → "all trailing newlines are stripped" (`.rstrip("\n")`) |

### Blocked by the freeze (propose to the next round, do not delete now)

| path:line | candidate | why blocked |
|---|---|---|
| `.ufo/waves/round-87/count-c1.py:75,118,181` | drop `mutants=` (≡ `total`) and the derived `killed=` | P-C1's target string is byte-frozen (`mutants=6 killed=6 survivors=0 total=6 arms=54`); the contract repeats it |
| `.ufo/waves/round-86/count-c1.py:229-230` | `unanchored_excluded` is subsumed by `unanchored_plus_killed_unmet` | the r86 counter's 18 arms are frozen by P-C1; deleting one makes the pristine arm count 17 and the claim unmet |
| `.ufo/waves/round-86/count-c1.py:250-251` | tighten to `not met` only, or `e.startswith("unanchored")` | same frozen 18; the shared substring is not discriminating either way |
| `.ufo/waves/round-87/count-c2.py:32-36,369-370,415-433` | retire the `SUBJECT` sub-gate as a unit | frozen counter + A1; see §3. Retiring takes the selftest 17→16 and removes the `subject=absent|stub|selftest` paths; P-C2 unaffected |
| `.ufo/waves/round-87/count-c2.py:217` | `population=` parameter (never passed here) | either delete it or — better — port the r86 fixture arms that use it |

### Do not delete (they are the rule, not the weight)

`count-c2.py:250-253` and `:262-265` (`summary`/`binding` clauses), `:267-268` (legacy promotion), `:298-302`
(absent supersede target) are the code that can report unmet. They are unarmed, not dead. The fix is
an addition (port `summary_required`/`binding_required` from `.ufo/waves/round-86/count-c2.py:296-306`
into the r87 file, using the existing `population=` seam), which would also make the parameter earn
its keep. Likewise `count-c1.py:240-245`: keep the arm, restore the r86 fixture
(`dup.py` + a GUARD-sensitive copy) and assert on `not met` (or on an extra that starts with
`unanchored`), so the name becomes true again.

## 5. Preserved contract and stop point

- Both frozen target lines reproduce byte-identically at their claimed revisions (rc 0): `C1=met … arms=54`,
  `C2=met … superseded=2 legacy=1 unexpected=0` (§0).
- The six new arms are each singly load-bearing at `03b66a43`; the supersede rule is armed; the two
  GIT fixtures the new arms build do not touch the lane (they `git init` under scratch only).
- Nothing above proposes a change to either claim, the population, the kill rule, or the targets.
- I stopped where the next deletion would rewrite a frozen predicate: `mutants=`/`killed=` and the r87
  `SUBJECT` gate are the only remaining duplicates I found, and both are priced by the freeze. The
  largest remaining weight is not deletable at all — the unarmed grading core of `count-c2.py` — and
  its fix is an addition, which is a different round's claim.

## 6. Honesty, non-goals, and scratch

- I did not edit `.ufo/waves/round-87/count-c1.py` or `count-c2.py`; the only lane path I wrote is
  this report.
- The lane worktree was already dirty on entry (`corpus/SOURCES.md` modified; `after-r87.txt`,
  `w1/`, `w1-validator.err`, `w1.ready.dispatched` untracked) — not mine, left untouched. Siblings
  advanced HEAD while I ran (to `22fa2919`, including contract erratum E1); I re-read the amended
  contract and re-hashed the two counters at the end — both are byte-identical to the bytes cited
  above (`e2ff…`, `264a…`), so this report describes the bytes it names, not a moving tree.
- Tools used, none installed or upgraded: `python3 3.14.8`, `ruff 0.17.2`, `pyflakes 4.0.3`,
  `coverage 7.17.0` (all pre-existing on PATH; no pacman transaction).
- All mutant copies, the three r86 subjects, coverage data and the `/tmp`-avoiding scratch lived under
  `/fast/scratch/hyaku/mori-r87/Mo87Si01Simplify/` and that tree is deleted before yield.
- Fixture-repo rule observed: the r86 `count-c2.py` selftest's fixture repo was created by the frozen
  counter itself under my scratch; I ran no git mutation in the lane.
