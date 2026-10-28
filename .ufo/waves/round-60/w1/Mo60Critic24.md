# Mo60Critic24 — drift-arm mutant wave (r60 C2 H5)

Seat: critic, leaf. Read-only on the lane; all writes under
`/fast/scratch/hyaku/mori-r60/Mo60Critic24/` (removed after the receipts below
were copied). No lane VCS mutation, no commits, no fleet/sibling writes.
Frozen contract read first: `.ufo/waves/round-60/contract.md` (freeze
`ac496c7cde8cad965079858accae3bedfe4a73f2`, entering
`ddfb12fb0838b4307c445194a844f0c4b1950195`). Disk guard green before work:
`/fast/scratch/hyaku` 26% used, 601G free. No tools installed.

## Verdict

`C2=met` reproduces at both the freeze revision and the lane tip
(`b3c25613…`), and the frozen pin (G1) refuses every one of the eleven mutant
scanners with **zero execution**. Bypassing G2-in-isolation (pin set to the
mutant's own sha, sandbox copy differing only in the `PIN_SCAN` literal), the
drift predicates kill **nine of eleven** mutants — including all three assigned
classes in their natural form. **Two strongest forms survive the drift
predicate pair and reach `C2=met`:**

1. **M1c** — filename heuristic keyed on the *exact parent directory name*
   (`round-53`), reasons forged to the true `:extra_keys=report_file` text.
2. **M2c** — note-nullability mutant (rejects non-null `note`) that labels its
   failure `:extra_keys=note`.

Neither is a natural bug; both are reason-string forgeries that the frozen
attribution rule (`any(DRIFT_REASON in r for r in reasons)`, `count-c2.py:249-252`)
cannot distinguish. This does **not** flip the scored claim (the executed tool
is byte-pinned, so a mutant can never be the executed tool), but the contract's
parenthetical justification for H5 — *"the filename-heuristic mutant dies"* —
is true only for the natural class, and the knowledge entry's declared limit
(`entry-claims-hardening-r60.md:29-31`) does not describe reason forgery at all.

## Evidence

### 1. Baseline (lane, read-only)

```
$ cd mori-shokunin && python3 .ufo/waves/round-60/count-c2.py ac496c7cde8cad965079858accae3bedfe4a73f2 --scratch …/c2-freeze
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 spans=13 rev=ac496c7cde8cad965079858accae3bedfe4a73f2   (exit 0)
$ python3 .ufo/waves/round-60/count-c2.py b3c256138f00c704d5aa56eb0332d74506502ef2 --scratch …/c2-head
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 spans=13 rev=b3c256138f00c704d5aa56eb0332d74506502ef2   (exit 0)
```

Pinned tool bytes at both revs: `tools/mori-settlement-scan.py`
`4c04bf21…ac9a9`, `tools/mori-entry-claims-check.py` `cffe9f33…e6e69` — both
equal their `PIN_SCAN`/`PIN_EC`. Drift file truth: every r53 member (67) carries
exactly `{agent,name,note,output,report_file}`; every r54 member (74) carries
`{agent,name,note,output}`. r53 `note` is non-null on 67/67 members; r54 `note`
is null on 74/74 — the drift pair differs on **two** columns at once.

Pinned scan on the drift probe:
`exit=1 verdict=SETTLEMENT_SCAN_FAIL` with 67 reasons, all
`member[i]:extra_keys=report_file`. On r54 bytes at an r53-named path:
`exit=0 verdict=SETTLEMENT_SCAN_OK`, `members==seats`.

### 2. Fixture (throwaway repo, explicit scratch path)

`D=$(mktemp -d -p /fast/scratch/hyaku/mori-r60/Mo60Critic24 poc-XXXXXX)`,
`git -C "$D" init -q`, every path `count-c2.py` reads extracted with
`git show b3c25613:<path>` (no lane clone, no worktree, no `.git` touch).
`git -C "$D" rev-parse --show-toplevel` → `/fast/scratch/hyaku/mori-r60/Mo60Critic24/poc-C23ChA`.
Base commit `e69fed4a`; pristine base scores
`C2=met … drift=ok … rev=e69fed4a` — fixture fidelity confirmed before mutation.

Eleven mutants, each committed at `tools/mori-settlement-scan.py` on its own rev:

| mutant | defect | drift probe | control probe | full counter (real pin) | sandbox (pin := mutant) |
|---|---|---|---|---|---|
| m0_always_pass | accepts everything | OK (no failure) | OK | `unmet … scan_tool_sha`, ran=**false** | `failed=drift` (attribution) |
| m1a_filename_substring_generic | `"round-53" in path`, generic reason | FAIL | FAIL (alias contains substring) | `unmet … scan_tool_sha` | `failed=drift` (attribution **and** ctrl) |
| m1b_filename_substring_forged | same heuristic, reason `member[0]:extra_keys=report_file` | FAIL | FAIL (alias contains substring) | `unmet … scan_tool_sha` | `failed=drift` (**ctrl only**) |
| **m1c_filename_parent_exact_forged** | `Path(p).parent.name == "round-53"`, per-member forged reason | FAIL | **OK** (parent `round-53-alias`) | `unmet … scan_tool_sha` | **`C2=met`** |
| m1d_filename_parent_exact_generic | same heuristic, honest reason `path:round-53` | FAIL | OK | `unmet … scan_tool_sha` | `failed=drift` (**attribution**) |
| m1f_filename_basename_exact_forged | basename `w1-results.json`, forged reason | FAIL | OK | `unmet … scan_tool_sha` | `failed=scan` (**scan arm**: five real files share the basename) |
| m2a_note_required | requires `note` non-null | OK (no failure) | FAIL | `unmet … scan_tool_sha` | `failed=drift,scan` |
| m2b_note_forbidden | rejects non-null `note`, honest reason | FAIL, reasons `note_nonnull` | OK | `unmet … scan_tool_sha` | `failed=drift` (**attribution**) |
| **m2c_note_forbidden_as_extrakeys** | rejects non-null `note`, labels it `member[i]:extra_keys=note` | FAIL, key-set `note` | **OK** | `unmet … scan_tool_sha` | **`C2=met`** |
| m3a_unconditional_fail | always exit 1, `always_fail` | FAIL, no extra_keys | FAIL | `unmet … scan_tool_sha` | `failed=drift,scan` |
| m3b_unconditional_fail_forged | always exit 1, forged `extra_keys` reason | FAIL | FAIL | `unmet … scan_tool_sha` | `failed=drift,scan` (**ctrl + scan**) |

Raw sandbox lines for the two survivors (evidence, `--repo $D`):

```
m1c  C2=met   selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 spans=13 rev=cc84eb2cc132109dd5114d5858b60bbaf0d21fad
m2c  C2=met   selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 spans=13 rev=99f0495d21f534b59c540d455bef3076a5d98751
```

Real-counter lines for the same revs (frozen pin untouched):

```
m1c  C2=unmet selftest=ok scan=bad drift=bad … failed=drift,scan,scan_tool_sha   ran=false
m2c  C2=unmet selftest=ok scan=bad drift=bad … failed=drift,scan,scan_tool_sha   ran=false
```

Non-execution proof: each mutant appends its tag plus argv to `$MUTANT_TRACE`
on entry; `count-c2.py` passes `env={**os.environ, TMPDIR:…}` into the tool
(`count-c2.py:144-158`), so the trace file is the execution record. After each
real-pin run the tag of that mutant was absent; the tag appeared only in the
sandbox run. Sandbox fidelity: `diff -u` of the lane counter against the
sandbox copy shows exactly one hunk, the `PIN_SCAN` literal (`count-c2.py:49-50`).

### 3. Why m1c and m2c survive

- **m1c.** The drift probe is materialized at
  `<scratch>/drift/round-53/w1-results.json`; the control at
  `<scratch>/alias/round-53-alias/w1.json` (`count-c2.py:234, 257`). The two
  paths differ in three components (grandparent, parent, filename), so a
  heuristic keyed on the parent directory name fires on the drift probe only and
  the control passes. The forged reason text is then indistinguishable from the
  correct one: on the drift probe m1c emits exactly the 67 reasons the pinned
  tool emits (`member[i]:extra_keys=report_file`, all `member[`-prefixed), and
  `attributed` inspects only `any(":extra_keys=" in r)`.
- **m2c.** r53 and r54 differ on `note` nullability as well as on the extra key.
  A scanner that rejects non-null `note` therefore fails exactly the drift file
  and passes the control, the five real scans (all null notes) and all thirteen
  trees. Naming that failure `:extra_keys=note` satisfies the substring rule
  while naming a key that is a member key, not an extra key.

Neither survivor needs a path heuristic plus forgery to be *killed in practice*:
G1 (byte pin) is the operative barrier, and it held for all eleven mutants.

### 4. Corrections, measured against the same eleven mutants

`probe/` materialized four inputs: drift (=r53 bytes), control_current
(=r54 at `round-53-alias/w1.json`), control_fixed (=r54 at
`round-53/w1-results.json` — identical parent dir and filename, different
grandparent), drift_renamed (=r53 bytes with `"report_file"` → `"extra_note"`,
67 occurrences, JSON-valid, key-set `extra_note`).

| predicate variant | kills m1c | kills m2c | pinned tool | survivors |
|---|---|---|---|---|
| current (any `:extra_keys=` substring, alias path) | no | no | pass | m1c, m2c (+m1f via drift arm only, caught by scan arm) |
| A: path-identical control `…/round-53/w1-results.json` | **yes** (ctrl FAIL) | no | pass | m2c |
| B: exact reason class (`member[i]:extra_keys=report_file`, all reasons, count == members) | no | **yes** (key-set `note`) | pass | m1c |
| **C: third content-varied probe** — renamed key at the drift path, require the reason key-set to equal the *renamed* key | **yes** (names `report_file`) | **yes** (names `note`) | pass (names `extra_note`, 67/67) | none |

Exact evidence for C:

```
pinned  drift_renamed: FAIL SETTLEMENT_SCAN_FAIL  key-set=extra_note  67/67 member-prefixed
m1c     drift_renamed: FAIL SETTLEMENT_SCAN_FAIL  key-set=report_file 67/67   ← constant, not derived
m2c     drift_renamed: FAIL SETTLEMENT_SCAN_FAIL  key-set=note        67/67
m3b     drift_renamed: FAIL SETTLEMENT_SCAN_FAIL  key-set=report_file 1/1
```

### 5. Secondary observations (no behavior change shown)

- `count-c2.py:209` reads `if not (ec_ok is not None and scan_ok_sha) or not rfiles:`
  — `ec_ok is not None` is a tautology (a bool is never `None`), so the scan arm
  is gated on `scan_ok_sha` alone. Observable in the committed control at the
  entering revision: `control-c2-do-nothing.txt` has `tool_absent` **and**
  `scan=ok drift=ok`, i.e. the scan and drift arms ran with the entry-claims
  tool absent. Harmless (independent tools, G1 still gates execution) but the
  condition is dead weight.
- `C2_SELFTEST pass=8` (`count-c2.py:424-455`) covers four constants and four
  G2 containment checks; it has **zero** assertions over the drift arm
  (`count-c2.py:229-273`), the scan arm's `members==seats` assertion, or the G3
  `expect_tamper` branch. The `expect_tamper` branch is exercised cross-counter
  by count-c3's expectgate; the drift arm is exercised only by the real run.
- Ignored `materialize()` return at `count-c2.py:234` and `:257` is fail-closed:
  a refused/absent drift file scans as `unreadable` → `FAIL` → `attributed`
  false; a refused control → `ctrl` false. Verified directly (missing-path probe:
  `exit=1 SETTLEMENT_SCAN_FAIL reasons=["unreadable"]`). No containment hole here.

## Impacted axes

- **C2 depth (score 5) — verdict unchanged, `C2=met` at freeze and tip.** The
  scored predicate is the two-probe pair plus the reason substring; both hold,
  the tool is byte-pinned, and `--selftest` prints the frozen summary. Nothing
  in this report flips it.
- **H5 justification text — over-strong.** "the filename-heuristic mutant dies"
  holds for heuristics keyed on a path substring or on the basename (the latter
  additionally by the scan arm), not for one keyed on the exact parent
  directory, and not for reason forgery. Impact: the r61 hardening route, not
  this round's score.
- **Declared limit in `corpus/knowledge/entry-claims-hardening-r60.md:29-31`** —
  describes byte-keying only; reason-string forgery (`:extra_keys=`-shaped text
  attached to an unrelated failure class) is uncovered by any arm and should be
  the recorded limit.
- **Not impacted: C1, C3.** No C1 artifact was touched; the C3 toolgate claim is
  the mechanism that made all eleven mutants inert (independent confirmation).

## Smallest safe correction (r61, not r60)

Post-freeze edits to `count-c2.py` invalidate the frozen claim, so this is a
route, not an edit: **add one content-varied probe to the drift arm** — write
`git show <R>:<DRIFT_SCAN>` with the single extra key token renamed
(`"report_file"` → `"extra_note"`, 67 occurrences, JSON-valid) at the *same*
drift path, run the pinned scan, and require every reason to be
`member[i]:extra_keys=extra_note` (all reasons member-prefixed, count == the
file's member count). One `materialize` + one `run_pinned`, no new committed
fixture, no change to the existing two probes. Measured: it kills m1c, m2c, m3b
and leaves the pinned tool green (§4 row C). If a no-new-run edit is preferred,
A **and** B together also kill both survivors, but neither alone does.

## Reproduction

```
S=/fast/scratch/hyaku/mori-r60/Mo60Critic24            # recreated by the steps below
cd /home/vgpnk/Projects/shokunin/mori-shokunin
python3 .ufo/waves/round-60/count-c2.py ac496c7cde8cad965079858accae3bedfe4a73f2 --scratch $S/c2-freeze
python3 .ufo/waves/round-60/count-c2.py b3c256138f00c704d5aa56eb0332d74506502ef2 --scratch $S/c2-head
# fixture
D=$(mktemp -d -p $S poc-XXXXXX) && git -C "$D" init -q
# for each path p in: tools/mori-settlement-scan.py, tools/mori-entry-claims-check.py,
#   corpus/knowledge/wave-settlement-artifacts-r59.md, corpus/SOURCES.md,
#   corpus/evidence/sources-r59/* , .ufo/waves/round-53|54|55|56|57|58/w1-results.json,
#   .ufo/waves/round-58/evidence/w1-settlement.json, .ufo/waves/round-60/count-c2.py,
#   .ufo/waves/round-60/trees-c2h/** :
#     mkdir -p "$D/$(dirname $p)"; git show b3c25613:$p > "$D/$p"
git -C "$D" add -A && git -C "$D" commit -q -m base
# mutate: copy a mutant over tools/mori-settlement-scan.py, commit, then
#   real pin : python3 .ufo/waves/round-60/count-c2.py <rev> --repo "$D" --scratch …
#   sandbox  : sed the PIN_SCAN literal in a *scratch copy* of count-c2.py to the
#              mutant sha, then python3 <copy> <rev> --repo "$D" --scratch …
```
Mutant sources: `m0_always_pass`, `m1a_filename_substring_generic`,
`m1b_filename_substring_forged`, `m1c_filename_parent_exact_forged`,
`m1d_filename_parent_exact_generic`, `m1f_filename_basename_exact_forged`,
`m2a_note_required`, `m2b_note_forbidden`, `m2c_note_forbidden_as_extrakeys`,
`m3a_unconditional_fail`, `m3b_unconditional_fail_forged` — each a structural
clone of the pinned scanner (same CLI, same schema) with one defect in the
verdict predicate and a `$MUTANT_TRACE` execution record. Scratch root removed
after these receipts were copied; nothing was written outside it.
