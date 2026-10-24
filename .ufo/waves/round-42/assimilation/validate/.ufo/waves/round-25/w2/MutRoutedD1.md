# MutRoutedD1 — mutation test of the D1 predicate in `tools/mori-routed-r24.py` (C1)

**Verdict: HELD, with two coverage findings (no contract change proposed).**

19 mutants of the D1 predicate were built and applied one at a time to the tool in a private
clone. 18 of 19 were killed by a 24-entry sandbox corpus of red and green commits. **One
mutant survived** (M15), and it survives for a structural reason that is worth knowing but
changes no contract: the `revision` hex-format clause is verdict-redundant with the
commit-resolution clause that follows it.

One **real coverage gap** was found that is not a mutant but a property of the tool: D1
compares the recorded evidence body against a hardcoded constant, not against the output that
revision R's tool actually produces. Details in Finding 2.

No lane file was modified. The lane checkout is byte-identical to its pre-run state
(`git status --porcelain` shows only the pre-existing untracked `.scratch/`).

---

## 1. What was attacked

`tools/mori-routed-r24.py` at lane tip `07a31ae8e22514bbc603afa13f2de7c8b2424cca`.
Tool sha256 `cf5ef5815f1118ae3595171edde7f527176fde03480665eb6bbb46921c2969ef`
(identical in the lane and in the private clone).

The D1 predicate lives in `_check_d1()` (`tools/mori-routed-r24.py:436-520`). The clauses
attacked were exactly those named in the assignment plus the adjacent ones that share the
same function:

| clause | source line | mutant |
|---|---|---|
| ancestor check | `tools/mori-routed-r24.py:462-463` | M1 |
| `tool_blob` equality at R | `tools/mori-routed-r24.py:480-481` | M2 |
| `tool_blob` equality at REV | `tools/mori-routed-r24.py:482-483` | M3 |
| `fixtures_tree` equality at R | `tools/mori-routed-r24.py:495-496` | M4 |
| `fixtures_tree` equality at REV | `tools/mori-routed-r24.py:497-498` | M5 |
| `exit: 0` check | `tools/mori-routed-r24.py:503-504` | M6 |
| exact-body comparison | `tools/mori-routed-r24.py:508-509` | M7, M8 |
| `revision` is a commit | `tools/mori-routed-r24.py:459-461` | M9 |
| `command` line equality | `tools/mori-routed-r24.py:466-467` | M10 |
| pressure tool present | `tools/mori-routed-r24.py:478-479` | M11 |
| fixtures present | `tools/mori-routed-r24.py:493-494` | M12 |
| ancestor argument order | `tools/mori-routed-r24.py:462` | M13 |
| header key order | `tools/mori-routed-r24.py:315-337` (`_split_header`) | M14 |
| `revision` 40-hex format | `tools/mori-routed-r24.py:453-454` | M15, M15b, M15c |
| `tool_blob` 40-hex format | `tools/mori-routed-r24.py:471-472` | M16 |
| `exit` numeric format | `tools/mori-routed-r24.py:501` | M17 |
| whole D1 check bypassed | `tools/mori-routed-r24.py:436-438` | M18 |
| D1 removed from the counted rows | `tools/mori-routed-r24.py:927` | M19 |
| process exit forced to 0 | `tools/mori-routed-r24.py:946` | M20 |

## 2. Method

**Private clone.** `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin
/fast/scratch/hyaku/mori-r25/w2-MutRoutedD1`. All commits and all mutations happened there.
The lane checkout was never written to; no `jj` command was run; no lane `git add/commit/
checkout/reset` was run.

**Detector.** The bounded behavioural detector is the tool's own verdict on a corpus of
sandbox commits: `python3 -I -B <tool> --repo <clone> --rev <sandbox-commit>`, reading the
D1 row (`held`, `reasons`) and the process exit code. A mutant is **killed** when the tool's
verdict changes on some corpus entry — specifically a *false hold* (a red entry flips to
`D1 held=true`, or D1 disappears from the report), a *false alarm* (a green entry flips to
`held=false`), or a *verdict change* (exit code or `mismatches` moves). A mutant whose change
is confined to the `reasons[]` text is **reason-only**, which is weaker than a kill.

**Baseline first.** The pristine tool was run over the whole corpus before any mutation. Every
green entry holds (`exit 0`) and every red entry is red (`exit 1`) with the expected reason.
A baseline failure would have made the run inconclusive; there was none.

**One mutant at a time, exact restore.** For each mutant: the tool file in the clone was
overwritten with the mutated bytes, `py_compile` was checked, the whole corpus was run, then
the original bytes were written back and the sha256 re-verified. **All 19 mutants restored to
`cf5ef5815f1118ae3595171edde7f527176fde03480665eb6bbb46921c2969ef`; the assertion
`restored_exactly == true` held for every mutant.** The lane and clone tool files are
byte-identical to each other and to the pre-run state.

## 3. Corpus (24 sandbox commits, branch `sandbox` in the clone)

Green — D1 must hold:
- `G0-green-pristine` — the landed tip unchanged.
- `G1-green-unrelated-commit` — an unrelated file added on top.

Red — each breaks exactly one D1 clause:
- `R1-revision-not-ancestor` — the `revision` header names a commit on a side branch that is
  not an ancestor of REV.
- `R2-tool-blob-wrong-value` — recorded `tool_blob` matches no blob.
- `R3-tool-changed-after-evidence` — `tools/mori-pressure.py` edited at REV only.
- `R4-fixtures-tree-wrong-value` — recorded `fixtures_tree` matches no tree.
- `R5-fixtures-changed-after-evidence` — `tools/fixtures/mori-pressure/` edited at REV only.
- `R6-exit-not-zero` — header says `exit: 1`.
- `R7-body-extra-line` — the two expected lines plus one extra trailing line.
- `R8-body-expected-line-absent` — `MATCHER` line present, `PASS 12/12` line absent.
- `R9-evidence-file-missing` — the evidence file deleted at REV.
- `R10-tool-differed-at-named-revision` — R is an ancestor where the tool differs; the
  recorded `tool_blob` equals the blob at REV, so only the at-R comparison fires.
- `R11-fixtures-differed-at-named-revision` — the same shape for the fixtures tree.
- `R12-round24-evidence-restored` — **the round-25 fix reverted**: the round-25 evidence file
  replaced by the round-24 file `.ufo/waves/round-24/evidence/c2-selftest-after.txt`
  (no revision header, one line of body).
- `R13-revision-not-a-commit` — the `revision` header names the pressure tool's blob.
- `R14-command-line-wrong` — header names a different command line.
- `R15-pressure-tool-missing-at-rev` / `R16-pressure-fixtures-missing-at-rev` — the tool or
  the fixtures tree deleted at REV, still present at the named revision.
- `R17-revision-names-an-annotated-tag` — the `revision` header names an annotated **tag
  object** that peels to a commit but is not itself a commit.
- `R18-forged-body-vs-real-tool-output` — R's tool prints `MATCHER: rejected 0/0` while the
  evidence body claims `rejected 48/48` (see Finding 2).
- `R19-header-out-of-order` — the five header lines present but reordered.
- `R20-revision-not-40-hex` / `R21-tool-blob-not-40-hex` / `R22-exit-not-numeric` — format
  violations of the three header values.

The pristine baseline over this corpus (all 24 entries behaved as intended) is in
`mutant-report.json` under `baseline`, reproduced here:

```
G0-green-pristine                             exit 0   []
G1-green-unrelated-commit                     exit 0   []
R1-revision-not-ancestor                      exit 1   ['revision_not_rev_or_ancestor']
R2-tool-blob-wrong-value                      exit 1   ['tool_blob_mismatch_at_revision']
R3-tool-changed-after-evidence                exit 1   ['tool_blob_mismatch_at_rev']
R4-fixtures-tree-wrong-value                  exit 1   ['fixtures_tree_mismatch_at_revision']
R5-fixtures-changed-after-evidence            exit 1   ['fixtures_tree_mismatch_at_rev']
R6-exit-not-zero                              exit 1   ['exit_line_not_zero']
R7-body-extra-line                            exit 1   ['body_not_byte_equal']
R8-body-expected-line-absent                  exit 1   ['body_not_byte_equal']
R9-evidence-file-missing                      exit 1   ['evidence_file_missing']
R10-tool-differed-at-named-revision           exit 1   ['tool_blob_mismatch_at_revision']
R11-fixtures-differed-at-named-revision       exit 1   ['fixtures_tree_mismatch_at_revision']
R12-round24-evidence-restored                 exit 1   ['header_missing: revision', 'revision_line_malformed', ...]
R13-revision-not-a-commit                     exit 1   ['revision_not_a_commit', 'pressure_tool_missing', 'pressure_fixtures_missing']
R14-command-line-wrong                        exit 1   ['command_line_malformed']
R15-pressure-tool-missing-at-rev              exit 1   ['pressure_tool_missing']
R16-pressure-fixtures-missing-at-rev          exit 1   ['pressure_fixtures_missing']
R17-revision-names-an-annotated-tag            exit 1   ['revision_not_a_commit', 'pressure_tool_missing', 'pressure_fixtures_missing']
R18-forged-body-vs-real-tool-output           exit 0   []          <-- see Finding 2
R19-header-out-of-order                       exit 1   ['header_missing: revision', ...]
R20-revision-not-40-hex                       exit 1   ['revision_line_malformed', 'pressure_tool_missing', 'pressure_fixtures_missing']
R21-tool-blob-not-40-hex                      exit 1   ['tool_blob_line_malformed']
R22-exit-not-numeric                          exit 1   ['exit_line_malformed']
```

## 4. Results — 18 of 19 mutants killed

| mutant | killed | killing input (verdict change) |
|---|---|---|
| M1 drop ancestor check | **yes** | `R1`: pristine `held=false ['revision_not_rev_or_ancestor']` → mutant `held=true`, exit 1→0 |
| M2 drop `tool_blob` equality at R | **yes** | `R10`: pristine `held=false ['tool_blob_mismatch_at_revision']` → mutant `held=true`, exit 1→0 |
| M3 drop `tool_blob` equality at REV | **yes** | `R3`: pristine `held=false ['tool_blob_mismatch_at_rev']` → mutant `held=true`, exit 1→0 |
| M4 drop `fixtures_tree` equality at R | **yes** | `R11`: pristine `held=false ['fixtures_tree_mismatch_at_revision']` → mutant `held=true`, exit 1→0 |
| M5 drop `fixtures_tree` equality at REV | **yes** | `R5`: pristine `held=false ['fixtures_tree_mismatch_at_rev']` → mutant `held=true`, exit 1→0 |
| M6 drop `exit: 0` check | **yes** | `R6`: pristine `held=false ['exit_line_not_zero']` → mutant `held=true`, exit 1→0 |
| M7 drop exact-body comparison | **yes** | `R7`: pristine `held=false ['body_not_byte_equal']` → mutant `held=true`, exit 1→0 (also `R8`) |
| M8 weaken exact-body to containment | **yes** | `R7`: pristine `held=false` → mutant `held=true`, exit 1→0 |
| M9 drop `revision is a commit` check | **yes** | `R17`: pristine `held=false` → mutant `held=true`, exit 1→0 |
| M10 drop `command` line check | **yes** | `R14`: pristine `held=false ['command_line_malformed']` → mutant `held=true`, exit 1→0 |
| M11 drop pressure-tool-present check | **yes** | `R15`: pristine `held=false ['pressure_tool_missing']` → mutant `held=true`, exit 1→0 |
| M12 drop fixtures-present check | **yes** | `R16`: pristine `held=false ['pressure_fixtures_missing']` → mutant `held=true`, exit 1→0 |
| M13 swap ancestor arguments | **yes** | `G0`: pristine `held=true` exit 0 → mutant `held=false`, exit 0→1 (false alarm) |
| M14 drop header key-order requirement | **yes** | `R19`: pristine `held=false` → mutant `held=true`, exit 1→0 |
| **M15 drop `revision` 40-hex format check** | **NO — survived** | see Finding 1 |
| M15b same clause, control flow flipped | yes | `G0`: false alarm (the mutant rejects every well-formed revision) |
| M15c same clause removed entirely | **NO — survived** | same as M15 |
| M16 drop `tool_blob` 40-hex format check | **yes** | `R21`: pristine `held=false ['tool_blob_line_malformed']` → mutant `held=true`, exit 1→0 |
| M17 drop `exit` numeric format check | **yes** | `R22`: pristine `held=false ['exit_line_malformed']` → mutant `held=true`, exit 1→0 |
| M18 bypass the whole D1 check | **yes** | every red entry: pristine `held=false` → mutant `held=true` |
| M19 drop D1 from the counted rows | **yes** | `R1`: pristine exit 1 → mutant exit 0 (D1 gone, `mismatches` 1→0) |
| M20 force the process exit to 0 | **yes** | `R1`: pristine exit 1 → mutant exit 0 |

Note on M2/M4: both also change the reason text on `R2`/`R4` (the at-REV clause catches the
value instead), but the verdict-level kills are `R10` and `R11`, which are the entries that
isolate the at-R comparison.

### Confirmed contract values (unmutated tool, lane checkout)

```
python3 -I -B tools/mori-routed-r24.py --repo . --rev HEAD
  items 4  held 4  mismatches 0  status held   hygiene held True   exit 0
  D1 True []   D2 True []   D3 True []   D5 True []

python3 -I -B tools/mori-routed-r24.py --repo . --rev 28b79d3d1b76824f0c825aabe6cb6c5dc49961bf
  items 4  held 0  mismatches 4  status failed  hygiene held False  exit 1
  D1 False ['evidence_file_missing']
  D2 False ['phrase_present_outside_corrections: refreshed on (each|every) read', ...]
  D3 False ['no_line_with_correction_s07_and_pass_marker']
  D5 False ['axis_score_mismatch: coverage 5!=6', 'axis_score_mismatch: operability 6!=7',
            'axis_score_mismatch: depth 4!=5']
```

Both reproduce the declared before/after values (`mismatches 4` at `28b79d3d`, `mismatches 0`
and exit 0 at the tip).

---

## 5. Findings

### Finding 1 — `revision` hex-format clause is verdict-redundant (M15 survived). Severity: informational.

**What survived.** M15 removes the `REVISION_LINE_RE` check at
`tools/mori-routed-r24.py:453-454` (`if not REVISION_LINE_RE.match(revision_value): reasons.append("revision_line_malformed")`),
keeping the else-branch that resolves the revision. M15c removes the whole `if/else` block,
so a malformed revision flows straight into the resolution check. Both survive: **no corpus
entry flips the D1 verdict**; only the `reasons[]` text changes (`revision_line_malformed`
disappears, replaced by `revision_not_a_commit`).

**Why it survives.** The check is redundant with the clause immediately after it. The tool
resolves the revision with `cat-file --batch-check` on `<rev>^{commit}`
(`tools/mori-routed-r24.py:225-249`) and rejects when `resolved != revision`
(`tools/mori-routed-r24.py:459-461`). For any revision string, the resolution check rejects
at least everything the format check rejects, because git resolves abbreviations and refs to
the full 40-hex id while the tool compares that resolved id against the *raw* string.

**Proof.** `probe_m15.py` enumerated 23 candidate revision values (full id, uppercase id,
7/8/12/39-char abbreviations, 41-char id, all-zeros, all-ones, `HEAD`, `master`, `sandbox`,
`@`, `-`, `..`, empty, whitespace, non-hex 40-char, the annotated tag object, the pressure
blob) and compared the two rejection decisions directly:

```
candidates probed : 23
format-only rejects (would survive dropping the format check): 0
```

Every value the format check rejects is also rejected by the resolution check. There is no
input that distinguishes the two clauses on the D1 verdict.

**Smallest fix.** None is required — the clause is a harmless, cheap early-out that produces a
better reason string. If the reason text is worth keeping, it is. **No contract change is
proposed**; per the wave rules a surviving mutant is a coverage finding, not permission to
change the contract.

**Input that would kill it, if one were wanted.** To make the format clause load-bearing, the
resolution check would have to *accept* a value the format check rejects — i.e. compare
`resolved` to the resolved form of the raw value rather than to the raw value. No current
corpus entry can distinguish them, and no repository state can either, because git's
resolution is total over these inputs. The clause is dead weight for the verdict, not a
missing check.

### Finding 2 — the D1 body clause is a constant comparison, not a check of R's real output. Severity: medium (coverage).

**What was observed.** `R18-forged-body-vs-real-tool-output` is a sandbox commit in which the
pressure tool at revision R has been altered to print `MATCHER: rejected 0/0 corrupted
expectations`, while the committed evidence body still claims
`MATCHER: rejected 48/48 corrupted expectations`. The pristine tool reports:

```
D1 held: True   reasons: []
```

D1 holds even though the recorded body is not what R's tool prints. The reason is structural:
the body clause compares the recorded bytes to a hardcoded constant
(`tools/mori-routed-r24.py:98-101`, `EXPECTED_BODY`), not to the output R's tool produces.
The constant currently equals the real output —

```
sha of EXPECTED_BODY constant : d767d1b6fd53e45caaeae8ca430f54f91badc08f89676a4d606bd1e2ac0be16f
sha recorded in the evidence  : d767d1b6fd53e45caaeae8ca430f54f91badc08f89676a4d606bd1e2ac0be16f
sha of the real selftest stdout: d767d1b6fd53e45caaeae8ca430f54f91badc08f89676a4d606bd1e2ac0be16f
byte-equal to constant        : True
```

— but the equality is an accident of the current bytes, not something the gate re-derives.
The `tool_blob` and `fixtures_tree` equality clauses do pin the tool and fixtures bytes at R
and at REV, which is what currently makes the constant safe; the body itself is not checked
against a run.

**The optional `--rerun` flag does catch it**, but only when asked:

```
python3 -I -B tools/mori-routed-r24.py --repo . --rev <R18> --rerun
  held: True  reasons: []
  rerun: {"ran": true, "exit": 0, "body_byte_equal": false,
          "stdout_sha256": "2738d20aee0c7fe409632d6d6150cdcaeb7c7ae27964c4920f74de98e6c7628a"}
```

`body_byte_equal: false` while `held` stays `true`. This matches the contract as written
(A1 says the `--rerun` result "is reported, never needed for `held`"), so this is a coverage
observation about the strength of the D1 gate, not a contract violation.

**Smallest fix, if the round wants one.** Make the body clause derive its expectation rather
than hardcode it: compare the recorded body against the stdout of R's own tool, which the
tool can already produce via `_run_pressure_selftest()` (`tools/mori-routed-r24.py:398-433`),
instead of against `EXPECTED_BODY`. That is a change to the D1 contract and therefore a
decision for the L1 seat, not this one. A cheaper, contract-preserving option is to require
`--rerun` (or its result) in the after-value command so the evidence file's body is
confirmed against a run.

### Finding 3 — the D1 predicate has no committed selftest. Severity: low (coverage).

`tools/mori-routed-r24.py` exposes only `--repo`, `--rev` and `--rerun`; it has no `--selftest`
and no fixture corpus under `tools/fixtures/`. Unlike the C2 runway tool
(`tools/mori-job-runway.py`, which carries a frozen 21-case `cases.json` and a `--selftest`
flag), the D1 predicate is exercised in the repo only by the two one-shot evidence files
`.ufo/waves/round-25/evidence/routed-r24-before-a5.txt` and `routed-r24-after-a5.txt`.

Consequence: the 24-entry sandbox corpus used here — the only thing that killed 18 of the 19
mutants — lives outside the repo and is not reproducible by the next seat from the lane alone.
**Smallest fix:** commit the corpus as a fixture (24 synthetic revisions under
`tools/fixtures/mori-routed-r24/`) plus a `--selftest` flag that runs the tool over them, in
the same shape as the runway tool. This is an addition, not a contract change.

---

## 6. Reproduction

```
# private clone (the lane is never written to)
git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin \
    /fast/scratch/hyaku/mori-r25/w2-MutRoutedD1

cd /fast/scratch/hyaku/mori-r25/mut-harness
python3 build_corpus2.py     # builds the 24 sandbox commits on branch `sandbox`
python3 mutants.py           # 19 mutants, one at a time, exact restore each time
python3 probe_m15.py         # the redundancy proof for Finding 1
```

`mutant-report.json` holds the per-mutant before/after rows and the sha256 of the tool before
mutation, after mutation and after restore.

## 7. Bounds honoured

- The lane checkout was not modified: `git status --porcelain` in
  `/home/vgpnk/Projects/shokunin/mori-shokunin` shows only the pre-existing untracked
  `.scratch/`; `tools/mori-routed-r24.py` there still hashes to
  `cf5ef5815f1118ae3595171edde7f527176fde03480665eb6bbb46921c2969ef`.
- All commits and all mutations are in the private clone
  `/fast/scratch/hyaku/mori-r25/w2-MutRoutedD1`; the harness lives in
  `/fast/scratch/hyaku/mori-r25/mut-harness`.
- No `jj` command was run anywhere; no lane `git add/commit/checkout/reset/stash` was run.
- This report is the only file written to the lane.
- No subagents were dispatched. No tool was installed or upgraded for this task.

## 8. Tooling

No installs, no upgrades. The work used only the preinstalled `python3` (3.13, standard
library) and `git`, both already present.
