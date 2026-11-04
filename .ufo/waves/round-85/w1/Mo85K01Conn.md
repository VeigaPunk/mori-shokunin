# Mo85K01Conn — sibling-overlap scan and contract clause sweep (round 85, w1, attempt 1)

Seat: Mo85K01Conn (connector, leaf — no subagent dispatch). Date: 2026-11-04.
Scope: read-only on the mori lane and on sibling lanes except this report. No lane file, sibling
repo, fleet-root file, `.ufo/state/`, watchdog log or orchestration state was written; no git/jj
mutation was run; no tool was installed or upgraded (no pacman transaction).

Revisions: entering `2cc4b1ae35a83e4fd3fc48bae842bdf38df2e80e`; freeze/HEAD
`ab2608655ea52ba6d151b3a31d69a3b18cd2b41e`. The three round-85 counters in the worktree are
byte-identical to HEAD (`git diff HEAD` empty; sha256 prefixes `da5fb27b9cd9b9cf` / `b7a4e691738f8161`
/ `c035e32f465eb545`), so every run below used the frozen bytes. Scratch
`/fast/scratch/hyaku/mori-r85/Mo85K01Conn/` was deleted before this seat yielded.

Paths: mori paths are relative to `/home/vgpnk/Projects/shokunin/mori-shokunin`; sibling paths are
relative to `/home/vgpnk/Projects/shokunin`.

## 0. Verdict

1. **No sibling lane owns any of mori's three surfaces.** Every match is an adjacent doctrine,
   primitive or instrument applied to a different lane's artifact; none is a contested duplicate
   (no sibling claims mori's counters, receipts or census). Verdict for all matches: **report**
   (cite as prior art in the round lesson), not absorb (the predicates are frozen this round) and
   not hand off (no sibling owns the artifacts).
2. **The sweep found 13 divergences** between the frozen prose and the frozen code: 7
   graded-defects, 3 target/control mismatches, 3 harmless-wording rows. The largest are C1's
   unenforced arm-label clause (the function that would enforce it is dead code), C2's revision
   binding being verified against R rather than the receipt's `# rev:`, and C3's entering control
   naming a token the counter never prints.
3. **Three frozen strings cannot be matched literally by the frozen counters**: C2's defeat control
   `C2=unmet headers=<receipt>`, C3's entering control `C3=unmet observed=absent harness=absent`,
   and C3's target omits the `subject_deltas=` field the counter prints between `subject_tokens=`
   and `unmatched=`. These are the rows to resolve before an after receipt is compared literally.
4. Nothing was edited and no check was run against the after state (it does not exist yet).

## 1. Sibling-overlap scan

Read-only search of sibling `corpus/` (`knowledge/`, `lessons/`, `QUALITY.md`, `README.md`) and
sibling `.ufo/waves/round-8*/` for `mutant`, `equivalent mutant`, `receipt`, `sha256`+`rev`,
`reconcile`, `census`, `hash-bound`. The scan is bounded: it covers the lanes and directories named
below and is not proof of absence in every sibling file or in history.

| # | Concept | Match (path:line) | One-line scope | Relation | Verdict |
|---|---|---|---|---|---|
| 1 | (a) mutation-arm adjudication | `chousa-shokunin/corpus/QUALITY.md:195-198` (rule 28) | "A surviving mutant becomes a fixture class before data" — a survivor of a landed tool is a coverage gap, closed by the class that breaks it before data runs. | Adjacent: the same doctrine mori's C1 applies, owned by chousa for chousa's counters. | report |
| 2 | (a) equivalent-mutant rule | `chousa-shokunin/corpus/QUALITY.md:958` (rule 107) | "A frozen mutant set holds no equivalent mutant; a survivor is classified before the target is fixed" — adjudicate equivalence before fixing the target. | Adjacent: doctrine is fleet-wide; the mutant set is chousa's. | report |
| 3 | (a) survivor isolation | `kake-shokunin/.ufo/waves/round-80/l1/quality-criterion.md:10-19` | A survivor is closed only by a fixture that isolates its own conjunct; `killed == 3` only when each fixture is red through its own mechanism. | Adjacent: same adjudication primitive, kake's counter/population. | report |
| 4 | (a) CAUGHT/SURVIVED protocol | `kama-shokunin/.ufo/waves/round-80/w1/MT01Mutation.md:56-83` | `CAUGHT` = the mutant's `--selftest` failed or a detector differed; 11/11 caught; restored copies must equal pristine. | Adjacent: operational protocol, kama's modules. | report |
| 5 | (a) battery kill tallies | `kengaku-shokunin/.ufo/waves/round-80/w1/C1BatteriesR80.md:41-54` | Committed vs fresh mutant tallies (6/6 and 4/4 killed), with divergent diagnostic codes called out. | Adjacent: reproducibility of kill tallies, kengaku's batteries. | report |
| 6 | (a) equivalent mutant example | `audio-shokunin/corpus/live/r94-simplifier/r94s_evidence_arm_entailment.txt:26-29` | A dropped arm entailed by the kept arm is "an equivalent mutant" by a mutation tester's score. | Adjacent: a single classification instance, audio fixture. | report |
| 7 | (a) equivalence classification | `kotoba-shokunin/corpus/knowledge/corpus-integrity-round11.md:196-210` | Four equivalent mutants with named reasons ("each has a named reason, not a tolerance"). | Adjacent: kotoba's checker population. | report |
| 8 | (b) hash-bound receipt grammar | `tameshi-shokunin/tools/receipt-bytes-bind.py:1-63` and `tameshi-shokunin/.ufo/waves/round-80/w1/T80W1CN1.md:15-18` | A receipt header (`# measured_rev:`, `# tool:`, `# tool_sha256:`, optional `# measured_bytes_rev:`) binds a recorded tool sha to the committed bytes of the revision the receipt names; states `bound`/`corrected`/`design`/`unbound`. The connector table calls chousa/audio "adjacent receipt mechanisms, not the design class". | **Adjacent, closest**: same text-header + sha256 primitive as mori C2, different population and predicate; no contested claim. | report |
| 9 | (b) receipt provenance | `chousa-shokunin/corpus/knowledge/receipt-binding-r38.md:20-38`, `chousa-shokunin/corpus/knowledge/receipt-verifier-subject-r39.md:37-41`, `chousa-shokunin/corpus/knowledge/receipt-expectation-digests-r40.md:12-15` | JSON receipts bind `counter_sha256`, `expect_sha256`, `verifier_sha256` and `subject_counter_sha256`; a verifier re-derives them and refuses by name. | Adjacent: different grammar (JSON + verifier), different subjects. | report |
| 10 | (b) receipt re-derivation | `kake-shokunin/.ufo/waves/round-80/l1/quality-criterion.md:17-22` and `kake-shokunin/.ufo/waves/round-80/contract.md:35` (R79-3) | "A gate's receipt is re-derived, never trusted": the counter re-runs the producing command at the measured revision and compares the line. | Adjacent: receipt-vs-re-run discipline, kake's gate. | report |
| 11 | (c) live-vs-declared reconcile | `kama-shokunin/tools/round78-live-reconcile.py:19-43` and `kama-shokunin/corpus/knowledge/live-reconcile-trial.md:1-20` | Runs its own live probe and reconciles the served model against the registry (`MODEL_OK`/`MODEL_MISMATCH`/`DEAD`), requiring runtime evidence. | Adjacent: same own-observation-vs-declared shape as mori C3, subject is a model server, not the fleet census. | report |
| 12 | (c) receipts-vs-runs census | `audio-shokunin/corpus/live/r89-reverify/runs/census-summary.py:1-13` and `audio-shokunin/corpus/live/r89-reverify/runs/census-summary.txt` | "committed-bytes receipts vs the mutant runs, law-class census, and custody checks" — a census over committed receipt bytes and run outputs. | Adjacent: re-run census against receipts, audio cells. | report |
| 13 | (c) record/artifact reconcile | `tameshi-shokunin/tools/wave-reconcile.py:1-40` | Round record claims (seats, seat reports, roles, attack share) re-derived from committed wave artifacts. | Adjacent by the word "reconcile" only: object is wave records, not a live survey. | report |

Also noted but not a match: `revenger-shokunin/.ufo/waves/round-85/census-*.log` runs the fleet
`sources-census.sh` over the lane registry — a registry census, not a re-run reconciliation of a
subject's live reading (adjacent to C3's word, not its surface).

### 1.1 Adjacency verdict

None of the three concepts is unowned, but none is owned on mori's surface: the sibling occurrences
are doctrine (chousa QUALITY 28/107; kake's survivor-isolation criterion), protocol (kama MT01;
kengaku batteries), or instruments over different populations (tameshi `receipt-bytes-bind.py` over
`.ufo/evidence` receipts; chousa's JSON receipt verifier; kama's live model reconcile; audio's
receipt/run census; tameshi's wave-record reconcile). The closest single match is tameshi C3's
`receipt-bytes-bind.py`, which shares mori C2's primitive — a text receipt header naming a revision
and a sha256 — and already names the exact distinction mori C2's prose leaves ambiguous (`# rev:`
vs the revision that actually carries the bytes, via `# measured_bytes_rev:`); mori should cite it
in the round lesson as prior art, but should not absorb its grammar mid-round because the round-85
predicate is frozen. Mori's verdict is therefore **report** for every row: no absorb (no predicate
change this round), no handoff (no sibling owns mori's counters, receipts or census; the claims are
mori-local capability/operability rows), and no contested duplicate (no sibling claims the same
artifact + predicate).

## 2. Contract clause sweep

Method: read `.ufo/waves/round-85/contract.md` against `count-c1.py`, `count-c2.py`, `count-c3.py`
line by line at HEAD; executed each counter's `--selftest` and the entering-revision invocation;
exercised the pure parser/classifier functions on synthetic inputs (pure functions, no lane writes).
Quotes are exact substrings; line numbers are those of the frozen files.

### 2.1 C1 — the five conjuncts and the `arms` / `r84` requirements

The predicate sentence (`contract.md:21-26`) has five conjuncts: (1) the exact target line and
rc 0; (2) both `old` anchors exactly once in the r84 counter at R; (3) the pristine copy's own
`--selftest` green, exactly 17 arms, both new arm labels; (4) each mutated copy's own `--selftest`
reads killed; (5) the r84 counter at R still prints its frozen 4-mutant line, rc 0.

| ID | Contract quote (line) | Code quote (line) | Class | How established |
|---|---|---|---|---|
| C1-D1 | "the pristine copy's own `--selftest` is green with exactly 17 arms and **carries both new arm labels**" (`contract.md:23-24`; also `:32` "a missing arm label keeps the claim unmet") | `arms_ok()` is the only function that tests the labels as selftest output: `return (green(rc, out) and failed == 0 and passed == TARGET_ARMS and all(("PASS " + marker) in out for marker in SUBJECT_MARKERS[:2]))` (`count-c1.py:109-114`). It is called only at `:237`, `:240`, `:242`, all inside `selfcheck()`. The met path uses `arms = arms_of(out)[0]` (`:138`), `green(rc, out)` (`:139`), `subject_ok(loader(SUBJECT))` (`:354`) where `subject_ok` is only `all(marker in text ...)` (`:105-106`), and `int(tail_arms.group(1)) != TARGET_ARMS` (`:359`). | **graded-defect** (false-pass exposure) | Full-file grep of `arms_ok(`: one definition + three selfcheck calls; no call from `grade()`/`main()`. A counter carrying the two labels in a comment/docstring and 17 unrelated arms satisfies `subject_ok` + `arms=17` while the labels are not live arms. |

The other four conjuncts are enforced: (1) main's `met` + `target_split` + `arms==17` + `r84=met`
(`:357-371`), target-split `(2,0,2)` at `:54`, `TARGET_ARMS = 17` at `:55`; (2) `base.count(old) != 1`
→ `unanchored` and excluded from `total` in `grade()`; (4) `killed()` applied to every mutated copy;
(5) `R84` regex (`:58`) over the r84 counter's output plus rc 0 in `r84_at_rev()`.

No divergence was found in the anchors or counts: at `2cc4b1ae` the X1 anchor
`if not k and coupling is not None:` occurs exactly once at r84 `count-c1.py:150`, the X2 anchor
`coupled = all(base.count(marker) == 1 for marker in coupling)` exactly once at `:151`, the r84
counter's own entry control prints `arms=15` (case count 15), and the r84 counter at `2cc4b1ae`
prints its frozen line rc 0 (measured below). The `rev=` suffix the counter appends
(`count-c1.py:371`) is a prefix-compatible extension of the target, the same convention the r84
record accepted.

### 2.2 C2 — command, revision and bytes

| ID | Contract quote (line) | Code quote (line) | Class | How established |
|---|---|---|---|---|
| C2-D1 | "each ... carries exactly one `# cmd:`, one `# rev:` (40-hex), one `# limits:` line" (`:63-64`); "a duplicate cmd/rev/limits line ... is a mismatch" (`:79`) | Duplicates are counted only when the line matches the strict regexes: `REV = ^#\s*rev:\s*([0-9a-f]{40})\s*$` (`:42`), `CMD`/`LIMITS` require `\S` (`:41`, `:43`); `seen["rev"] += 1` only inside the match (`:72-77`); `elif seen[name] > 1: duplicate-...` (`:94-98`). A second `# rev: zz` is invisible: fields keep the valid rev and `duplicate-rev`/`bad-rev` are both absent. | **graded-defect** (detector gap) | Pure `parse_receipt` probe: valid rev + `# rev: zz` → `problems == []`; two valid revs → `['duplicate-rev']`. Same for a second empty `# cmd:`/`# limits:` (regex requires `\S`). |
| C2-D2 | "`bindings` counts `# counter-sha256:` lines; `bound` counts the ones whose hash verifies" (`:80-81`) | `bindings` is appended only when `SHA` matches (`:44`, `:86-88`); `total_bindings += len(fields["bindings"])` (`:181`). A line beginning `# counter-sha256:` with a 63-hex digest is not counted and raises no problem. | **graded-defect** (count semantics; a malformed binding line is silently dropped) | Probe: two literal `# counter-sha256:` lines, one 63-hex → `len(bindings) == 1`, `problems == []`. |
| C2-D3 | "a header line is `# cmd: ...`" (`:78`); "the receipt body (after the single `# ---` line)" (`:66`) | `parse_receipt` scans every line of the file for header shapes before computing the body (`:66-90`), then splits the body after the first separator (`:91-93`). A `# cmd:` appearing after `# ---` increments `seen["cmd"]` and yields `duplicate-cmd`. | **graded-defect** (over-enforcement; body text can break a receipt) | Probe: appending `# cmd: quoted in body` after the separator → `problems == ['duplicate-cmd']`; the body is not exempt. |
| C2-D4 | "`# limits: <text containing the word "limit">`" (`:64`) | `if fields["limits"] is not None and ("limit" not in limits or len(limits.split()) < 3): problems.append("weak-limits")` (`:108-109`). The `>= 3`-word conjunct is not in the contract's rule list (`:78-81`). | **graded-defect** (code stricter: a prose-compliant line is rejected) | Probe: `# limits: limit` → `['weak-limits']`; `# limits: the limit holds` (3 words) → clean. |
| C2-D5 | "the `# rev:` resolves to a commit that is R or an ancestor of R; every bound path's bytes at **that revision** hash to the stated sha256" (`:65-66`) | `loader(path)` is bound to R: `q = run(["git", "-C", repo, "show", "%s:%s" % (rev, path)])` (`:278-280`, `rev` = resolved R). The receipt's `rev` is used only for `rev_ok`/ancestry (`:170-173`); `verify_bindings(fields["bindings"], loader)` (`:179`) hashes R's bytes. | **graded-defect** (ambiguous antecedent; ancestor receipts can false-pass if "that revision" means the named commit, and false-fail if it means R and the receipt names an ancestor) | Code reading; no after receipt exists. The goal sentence ("the sha256 of the subject bytes at that revision", where "that revision" is the graded revision) supports the R reading; the clause's antecedent supports the named-commit reading. tameshi's `receipt-bytes-bind.py` already resolves this distinction explicitly (`measured_rev` vs `measured_bytes_rev`). |
| C2-D6 | "a receipt without headers reads `C2=unmet headers=<receipt>` rc 1" (`:86-87`); the other defeat control "reads `C2=unmet bound=4 mismatch=1`" (`:85-86`) | No code path prints `headers=<receipt>`; the only `headers=` is the integer in `RECEIPT %s headers=%d rev=%d limits=%d bindings=%d bound=%d summary=%d` (`:192-196`), and header failures print `PROBLEM <name> missing-cmd` etc. (`:168`, `:179`, `:189`, `:194`). The tail is `C2=unmet receipts=3 bindings=... bound=4 ... mismatch=1` (`:199-201`), so the first control's two fields exist but are non-contiguous. | **target mismatch** (the second defeat control is not reproducible by the counter as written; the first is a shorthand, not a literal line) | Code reading of all print sites in `count-c2.py`. The controls file does not contain either defeat line (`evidence/controls-r85.txt` has only the entering control for C2, line 14). |

The target line (`:83`) is printed as a prefix plus ` detector=green rev=...`
(`count-c2.py:306`), the same extension convention as C1. The `bindings=5` target is internally
consistent with the receipt table (3 + 1 + 1) and with the hard-coded `total_bindings == 5`
(`:197`). The `# ---` split itself is correct: the body is `lines[body_start:]` where `body_start`
is the 1-based separator line (`:88-93`), and `duplicate-separator` is raised for a second one.

### 2.3 C3 — own observation and reconciliation

| ID | Contract quote (line) | Code quote (line) | Class | How established |
|---|---|---|---|---|
| C3-D1 | target `C3=met observed=3 aa=stable own_tokens=N subject_tokens=N unmatched=0 unnamed=0` (`:94`, `:111`) | `tail = ("observed=%d aa=%s own_tokens=%d subject_tokens=%d subject_deltas=%d unmatched=%d unnamed=%d" ...)` (`:359-361`). `subject_deltas` is inserted between `subject_tokens` and `unmatched`; an ordered/prefix match of the frozen target fails. | **target mismatch** | Measured run at `2cc4b1ae` (below) and the freeze control `evidence/controls-r85.txt:23` both print `... subject_tokens=64 subject_deltas=0 unmatched=0 ...`. |
| C3-D2 | entering control "`C3=unmet observed=absent harness=absent`" (`:114`; measured at `evidence/controls-r85.txt:17`) | `count-c3.py` has no `harness=` token at all. Its early unmet lines are `C3=unmet observed=absent census/baseline=absent` (`:320`), `... classification/snapshot=absent` (`:323`), and `C3=unmet observed=3 subject=absent` (`:327`). Running the frozen counter at `2cc4b1ae` prints `C3=met` rc 0, not `harness=absent`. | **target mismatch** (the frozen control line is not producible by the frozen counter; its provenance is a pre-freeze harness/stub, yet the controls header calls its bytes "the round-85 worktree counters") | Full-file grep for `harness` in the three counters: only `count-c1.py` and `count-c2.py` have it. Measured run `python3 -I .ufo/waves/round-85/count-c3.py 2cc4b1ae ...` → `C3=met ... rc=0` (below). |
| C3-D3 | "the subject ... runs and prints a `C2=met` tail" (`:99`) | The tail regex captures the status and discards it: `TAIL = re.compile(r"C2=(met\|unmet)\s+(.*)$")` (`:46`); `fields = dict(FIELD.findall(m.group(2)))` (`:139`); the gate is `if rc != 0 or fields.get("live") != "derived":` (`:337`). | **harmless wording** (r83's own `main` returns 0 iff met — `r83-count-c2.py:496-497` — so rc 0 entails `C2=met` for the fixed subject) | Code reading + the r83 subject's exit lines. Residual: a subject that printed `C2=unmet ... live=derived` and exited 0 would pass; not reachable from the frozen r83 bytes. |
| C3-D4 | the predicate enumerates the met conditions (`:93-102`); classes block (`:105-109`) | `met = (own_ok and stable and own_tokens and subject_tokens == len(own_tokens) and unmatched == 0 and unnamed == 0 and malformed == 0 and duplicates == 0)` (`:352-353`). `own_ok` (the counter's own selftest) and the `malformed == 0 and duplicates == 0` conjuncts are not in the C3 sentence. | **graded-defect (soft)** for `malformed/duplicates` (not stated; inherited from the r83 `met`; the two input files are unchanged between `2cc4b1ae` and the freeze — `git diff --stat` empty — and the measured run is met, which entails both counters are 0 on those bytes); **harmless** for `own_ok` (conservative detector rule) | Code reading; `classifications()` returns the counts at `:117-130`; the two inputs are unchanged from `2cc4b1ae` to the freeze (`git diff --stat` empty), and the measured `2cc4b1ae` run is met, which entails both counters are 0 on those bytes. |
| C3-D5 | "runs `tools/mori-census.sh --drift corpus/evidence/baseline-r10-20261015T2231Z.json` from R's own bytes ... in scratch" (`:95-97`) | `observe()` writes the census and baseline into a scratch work dir and runs `["bash", paths[CENSUS], "--drift", paths[BASELINE]]` with `cwd=work` and `MORI_SHOKUNIN_ROOT=fleet_root` (`:167-179`). The argument is the absolute scratch copy, not the repo-relative path the prose writes. | **harmless wording** (same bytes, same env root; the census's `MORI_DRIFT` line names fields, not paths; the three lines were stable in the measured run) | Code reading; measured `observed=3 aa=stable` at `2cc4b1ae`. |
| C3-D6 | "the snapshot's token line" (`:100-101`); "the subject's `C2=met` tail" (`:99`) | `drift_tokens()` keeps the **last** `MORI_DRIFT:` line (`:107-114`); `subject_signal()` keeps the **last** `C2=` line (`:133-139`). | **harmless wording** (the frozen snapshot carries two `MORI_DRIFT:` lines that are byte-identical per its own line 13; the subject prints one tail) | `git show ab260865:.ufo/waves/round-82/evidence/drift-r82-live.txt` lines 4 and 10; the file's line 13 states the lines are identical. |

The core C3 mechanics do match the prose: `OBSERVATIONS = 3` (`:50`); `observe_three` requires all
three rc 1, all token lines non-empty and identical (`:186-193`); `own_pairs = live_delta(
drift_tokens(snapshot), own_tokens, baseline_names(baseline), stated)` (`:345-346`); `reconcile`
walks every subject pair (unmatched) and every non-agreed own pair (unnamed) (`:133-153`);
`subject_tokens == len(own_tokens)` (`:352`); and the derivation functions (`baseline_names`,
`derive`, `live_delta`, `classifications`) are text-identical to the r83 subject's, so the "r83
rule" is copied, not paraphrased. `derive()` never returns `unexplainable`, which is how "a stated
`unexplainable` class is never equal to a derived class" is enforced.

## 2.4 Claim-provenance note (outside the contract, relevant to it)

`SCORECARD.md:4337-4340` (`## Planned (round 85)` §1) quotes the second survivor as
`coupled = base.count(coupling) == 1`; that string occurs **0×** in the r84 counter at `2cc4b1ae`.
The operative bytes are `coupled = all(base.count(marker) == 1 for marker in coupling)` at
`r84 count-c1.py:151` (1×), which is what the contract table and `count-c1.py:34-41` carry. The
same SCORECARD line cites `Mo84R01C1.md §4`, but the extra-mutant sweep is §5 (the contractual
pointer). This is prose drift of the r84 §6/QUALITY 172 class; no counter reads those strings, and
the contract's table is correct. Recorded so the lesson does not re-mint the wrong anchor.

## 3. Measured checks (commands and outputs)

Scratch `S=/fast/scratch/hyaku/mori-r85/Mo85K01Conn`; every command from the lane root with
absolute paths. `--scratch` is accepted by `count-c1.py` and `count-c3.py`; `count-c2.py` takes no
`--scratch` (passing it is exit 2 usage, not a claim result).

```text
$ python3 -I .ufo/waves/round-85/count-c1.py --selftest --scratch "$S"
... C1_COUNTER_SELFTEST pass=18 fail=0
rc=0

$ python3 -I .ufo/waves/round-85/count-c2.py --selftest
... C2_COUNTER_SELFTEST pass=15 fail=0
rc=0

$ python3 -I .ufo/waves/round-85/count-c3.py --selftest --scratch "$S"
... C3_COUNTER_SELFTEST pass=19 fail=0
rc=0

$ python3 -I .ufo/waves/round-85/count-c1.py 2cc4b1ae --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch "$S"
MUTANT count-c1.py X1_killed_rescued_as_equivalent survived rc=0
MUTANT count-c1.py X2_coupling_duplicate_passes survived rc=0
EXTRA survivor .ufo/waves/round-84/count-c1.py X1_killed_rescued_as_equivalent
EXTRA survivor .ufo/waves/round-84/count-c1.py X2_coupling_duplicate_passes
C1=unmet mutants=2 killed=0 survivors=2 total=2 arms=15 harness=stub missing=killed_mutant_with_coupling_not_equivalent,duplicate_coupling_not_equivalent rev=2cc4b1ae35a8
rc=1

$ python3 -I .ufo/waves/round-85/count-c2.py 2cc4b1ae --repo /home/vgpnk/Projects/shokunin/mori-shokunin
C2=unmet receipts=0 harness=absent rev=2cc4b1ae35a8
rc=1

$ python3 -I .ufo/waves/round-85/count-c3.py 2cc4b1ae --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch "$S"
C3=met observed=3 aa=stable own_tokens=64 subject_tokens=64 subject_deltas=0 unmatched=0 unnamed=0 detector=green rev=2cc4b1ae35a8
rc=0

$ python3 -I "$S/r84-count-c1.py" 2cc4b1ae --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch "$S"
MUTANT count-c1.py M24a_killed_tally killed rc=1
MUTANT count-c1.py M24b_green_fail_token killed rc=1
MUTANT count-c2.py M24c_met_unclassified equivalent rc=0
MUTANT count-c2.py M24d_met_residual equivalent rc=0
C1=met mutants=4 killed=2 equivalent=2 survivors=0 total=4 pristine=green detector=green rev=2cc4b1ae35a8
rc=0
```

Pure-function probes (imported the lane files read-only; no lane write):

```text
count-c2.parse_receipt:
  good headers                                   -> problems []
  valid rev + "# rev: zz"                        -> problems []            (no duplicate-rev, no bad-rev)
  two valid revs                                 -> ['duplicate-rev']
  "# cmd: x" + "# cmd:" (empty)                  -> problems []            (second line invisible)
  "# limits: ..." + "# limits:" (empty)          -> problems []            (second line invisible)
  two "# counter-sha256:" lines, one 63-hex      -> bindings=1, problems [] (literal lines=2)
  "# limits: limit"                              -> ['weak-limits']
  "# limits: the limit holds"                    -> []
  "# cmd: quoted in body" after "# ---"          -> ['duplicate-cmd']
count-c3.reconcile:
  subject [A=absent-live, A=added-live], own A=added-live -> unmatched=1 (duplicate wrong line is caught)
```

## 4. Checked and found matching (no divergence)

- C1: the two anchors and their line numbers at the entering revision (r84 `count-c1.py:150-151`);
  the r84 selftest case count 15 (`grep -c 'cases.append(('` = 15) and `arms=15` in the measured
  entering run; the r84 frozen line regex `R84` (`count-c1.py:58`) matches the r84 line measured at
  `2cc4b1ae`, rc 0. The r85 counter's own selftest is 18 arms (`C1_COUNTER_SELFTEST pass=18`), which
  is not the contract's 17-arm requirement — that requirement is on the r84 subject copy.
- C2: the three receipt paths and summary tokens (`count-c2.py:30-38`) match the contract table;
  the binding count 3 + 1 + 1 = 5 matches `bindings=5`; the target field order is a prefix of the
  printed line; the `# ---` body split is `lines[body_start:]` (correct); `rev_ok` re-resolves the
  candidate and checks `R or ancestor` (`:292-296`, `ancestor()` at `:143-149`).
- C3: `OBSERVATIONS = 3`; the `stable` predicate requires all rc 1, non-empty, identical tokens;
  `own_tokens == subject_tokens` is enforced; both `unmatched` and `unnamed` directions are walked;
  the `derive()`/`baseline_names()`/`live_delta()`/`classifications()` text is identical to the r83
  subject's; the measured retroactive reading is `own_tokens=64 subject_tokens=64`, matching the
  contract's disclosed reading (`:117-119`).
- C1/C2/C3 all append `rev=` (and C2/C3 `detector=...`) after their frozen target fields; this is
  the lane's established suffix convention (r84 record §0) and is prefix-compatible, not a target
  mismatch. The only target-order break is C3's `subject_deltas=` (C3-D1).
- The r84 counter at `2cc4b1ae` still prints its frozen 4-mutant line rc 0 (measured above), so
  C1's fifth conjunct is reachable at the entering revision; the after revision changes only the
  r84 counter's `selfcheck()` (per the contract's seat sentence), not `grade()`.

## 5. Limits and honest stops

- No after state exists at HEAD (the three receipts are not written; the r84 counter arms are not
  landed), so nothing here grades C1/C2/C3 as met/unmet. The findings are contract↔code
  divergences and instrument behaviour on the frozen bytes.
- C2's defeat controls were not built: there are no receipts to mutate, and building them is the
  receipt author's/executor's work, not this seat's. C2-D6 is a code-reading finding (no print site
  produces `headers=<receipt>`).
- C3's fixture defeat control was not re-run (it needs a census-stub fixture repo); its line is
  reachable from `:330-333`, and the *entering* control's line is not reachable from any print
  site — that asymmetry is the finding.
- C3's R-vs-named-revision binding in C2-D5 is a code-reading finding; the after receipts do not
  exist to exercise it. The sibling tameshi instrument is cited as the established distinction, not
  as a measurement of mori's receipts.
- Sibling scan is bounded to the named lanes/directories and the current corpora/wave dirs; it is
  not proof of absence in history or in unsearched files.
- No tools installed or upgraded; no pacman transaction; no mutating git/jj command; no lane or
  sibling write; scratch deleted before yield.
