# Mo59Executor42 — trees-c2 enumeration / eval_entry per-tree verdicts

Seat: `Mo59Executor42` (executor). Round 59, wave `w1`.
Scope: enumerate `.ufo/waves/round-59/trees-c2/`, extract each tree at the
freeze revision into scratch, run the frozen counter's **internal**
`eval_entry()` (imported from the frozen `count-c2.py`), print verdict +
reasons per tree.

Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`
Freeze rev: `60b3a76ad0524c8978cc51922940be1c8c388915`
Entering rev: `2b9f03975bfb6e508f35074ac8181ec8bf54e805`
Scratch: `/fast/scratch/hyaku/mori-r59/Mo59Executor42/` (created; TMPDIR set
there; cleaned before yield).
No commits, no lane VCS mutation, no production/corpus/SCORECARD/LOG edits.
Only file written outside scratch: this report.

---

## 1. Frozen counter identity (pre-flight)

```
$ git show 60b3a76:.ufo/waves/round-59/count-c2.py | sha256sum
2df3ae84f6d66f9ee46cd46cf2cb199ca85e7400301c5a0e9dd94b7b375877be  -
$ sha256sum .ufo/waves/round-59/count-c2.py
2df3ae84f6d66f9ee46cd46cf2cb199ca85e7400301c5a0e9dd94b7b375877be  .ufo/waves/round-59/count-c2.py
$ git diff --stat 60b3a76 HEAD -- .ufo/waves/round-59/count-c2.py
(empty — counter bytes unchanged freeze→HEAD)
$ git diff --stat 60b3a76 HEAD -- .ufo/waves/round-59/trees-c2/
(empty — all 12 trees byte-identical freeze→HEAD)
```

The counter used for every evaluation below is the **frozen** copy
(`sha256 2df3ae84…`), materialized from `60b3a76` into scratch and loaded
via `importlib.util.spec_from_file_location` — not the worktree file, so
the run cannot drift with post-freeze edits.

Tool pin verified independently:
```
$ git show 60b3a76:tools/mori-settlement-scan.py | sha256sum
4c04bf2170b0484192dd157ee04851e8243e030c54046c5e8806d46eea5ac9a9  -
```
matches the frozen `PIN` constant in `count-c2.py` (line 56).

---

## 2. Method

Per tree:

1. `git ls-tree --name-only 60b3a76:.ufo/waves/round-59/trees-c2/` → 12 names.
2. `git ls-tree -r --name-only 60b3a76 <base>/` → file list; each file
   extracted with `git show 60b3a76:<path>` into
   `$SCRATCH/trees/<name>/` (expect.txt excluded from the evaluated root,
   matching the counter's own tree-arm extraction at count-c2.py:333-343).
3. `eval_entry(tree_root)` called directly from the frozen module.
4. Acceptance replicated **exactly** from the counter's tree arm
   (count-c2.py:344-357):
   `want_ok = not expect`; `ok != want_ok` → `tree:<name>:verdict`;
   every expect prefix must be matched by some reason prefix
   (`any(r.startswith(e) for r in reasons)`) → else `tree:<name>:reasons`.

Driver script (scratch only, removed at cleanup):
`/fast/scratch/hyaku/mori-r59/Mo59Executor42/enum_trees.py`.

---

## 3. Per-tree verdicts (verbatim from the run)

Listing rc=0, count=12. **All 12 trees: `eval_entry` → ok=False (UNMET),
verdict matches expectation, expect prefix covered → tree arm PASS for
every tree.**

| tree | expect | eval_entry | reasons (verbatim) | claims/files | expect covered | tree arm |
|---|---|---|---|---|---|---|
| t01-no-frontmatter | `frontmatter` | UNMET | `frontmatter:source, frontmatter:verified-at, frontmatter:recheck, frontmatter:coverage-map, rows:no_source_ids` | 10/3 | yes | PASS |
| t02-dup-k | `distinct` | UNMET | `distinct:dup=K1` | 10/3 | yes | PASS |
| t03-quote-wrong-line | `span` | UNMET | `span:1` | 10/3 | yes | PASS |
| t04-stale-pin | `pin` | UNMET | `pin:1` | 10/3 | yes | PASS |
| t05-few-claims | `claims_min` | UNMET | `claims_min:7` | 7/3 | yes | PASS |
| t06-outside-file | `files` | UNMET | `files:outside=tools/mori-settlement-scan.py` | 10/4 | yes | PASS |
| t07-no-row | `rows:missing` | UNMET | `rows:missing=S901` | 10/3 | yes | PASS |
| t08-extra-cell-row | `rows:bad_row` | UNMET | `rows:bad_row=S901` | 10/3 | yes | PASS |
| t09-usedby-other | `rows:usedby` | UNMET | `rows:usedby=S901` | 10/3 | yes | PASS |
| t10-queued-status | `rows:status` | UNMET | `rows:status=S901` | 10/3 | yes | PASS |
| t11-quote-short | `span` | UNMET | `span:short=1` | 10/3 | yes | PASS |
| t12-malformed-claim | `grammar` | UNMET | `grammar:- **K5** — claim 5. Quote: ` "seats": 3,, claims_min:9` | 9/3 | yes | PASS |

`OVERALL trees arm (all 12): PASS` — exit 0.

Observations per tree (why each is UNMET, in the counter's own words):
- t01: entry body present but the four frontmatter keys (`source:`,
  `verified-at:`, `recheck:`, `coverage-map:`) are absent from the first
  ten lines → `frontmatter:*` ×4; consequently no `source: S###` id is
  harvested from the head → `rows:no_source_ids` (a second, benign
  consequence — the expect prefix `frontmatter` is still covered).
- t02: two claims share `K1` → `distinct:dup=K1`.
- t03: quote bytes do not equal the copy's line *n* → `span:1`.
- t04: claim pin ≠ sha256 of the cited copy → `pin:1`.
- t05: only 7 claim lines → `claims_min:7`.
- t06: one claim cites `tools/mori-settlement-scan.py`, which is not in
  the frozen `ARTIFACTS` map → `files:outside=…`.
- t07: head cites `S901`, registry has no `S901` row → `rows:missing=S901`.
- t08: the `S901` row carries 12 cells, the predicate requires 11 →
  `rows:bad_row=S901`.
- t09: the `S901` row's `used-by` cell is `corpus/knowledge/other.md`,
  not the entry → `rows:usedby=S901`.
- t10: the `S901` row status cell is `queued`, not `mined` →
  `rows:status=S901`.
- t11: quote shorter than 3 bytes → `span:short=1`.
- t12: one claim line is malformed (double comma) → `grammar:…`, and the
  malformed line is not counted, dropping the claim count to 9 →
  `claims_min:9`.

Every tree carries exactly 5 evaluated files (SOURCES.md, 3 artifact
copies, entry) plus expect.txt, which is excluded from the evaluated root.

### expect.txt sha256 at freeze (integrity receipt)

```
a39cb081a3221638d717036562e943cb6440ba5c272ec642998427d23cbbc3b3  t01-no-frontmatter
972979ebb0d1ca111c18859c38d8683b4fed52f3333c8c333da0f13ed718de78  t02-dup-k
cf7a7c2076a9899dd1a7329504f73c6dc6bbbafea762e76b4e016f9c0273ecd5  t03-quote-wrong-line
96ca82a29877656739be7136cce284c3b892881d1c506a1bf641aca692ed9cfa  t04-stale-pin
26fcb735e82ad1b376b292c1bd44fc36030feaa62d88bd30554223a4d828579d  t05-few-claims
43807f5b6bd11fa19ebb9234650fa77106a86dac8ad70406d50b7b3d865f9a9a  t06-outside-file
ceb3851aead57cf46ead24f2bbda4f5e1f044e6c458e020f06f2749758c74816  t07-no-row
998a002adf161289151fe9e2d09e337c3a62410f1b72e019d10c9ca8a4cdb643  t08-extra-cell-row
37f233b87a749321dc8feecea03c235caeb9d12b4bbd07c17499b27581d5e443  t09-usedby-other
c8c5059b7415c4d35524931645af1391daf31e0fc9b8f22691fb2dc47ad3060f  t10-queued-status
cf7a7c2076a9899dd1a7329504f73c6dc6bbbafea762e76b4e016f9c0273ecd5  t11-quote-short
2be265b0eee38add45e54d3fdbf23363e427d735843e94552852f219e415ff26  t12-malformed-claim
```
(t03 and t11 share a sha because both expect files are the single token
`span` — distinct trees, identical expected reason prefix.)

No tree entry cites an absolute or parent-relative path
(grep for `(/` or `(` + `../` → no hits), so no tree escapes its root.

---

## 4. Non-vacuity controls (the arm actually discriminates)

A tree arm that fails everything for one constant reason would be
vacuous. Two probes, both run against the frozen module:

**Positive probe** — a synthetic well-formed tree (10 distinct claims over
3 copies, all pins/spans correct, frontmatter present, one 11-cell
`mined` row with the correct `used-by`):
```
PROBE good-tree: ok=True reasons=[] stats={'claims': 10, 'files': 3}
```
`eval_entry` can return MET, so the 12 UNMET verdicts are discriminative.

**Negative probe** — t01 with the four frontmatter keys prepended (i.e.
"repairing" the defect the tree is supposed to exhibit):
```
NEG t01-repaired: ok=True reasons=[] want_ok=False verdict_matches=False covered={'frontmatter': False}
NEG -> counter tree-arm outcome: tree:t01:verdict FAIL (arm fires, non-vacuous)
```
A repaired tree flips the arm to `tree:t01:verdict`, so the arm detects
over-fixing as well as under-fixing.

**Tamper probe** — one byte changed in a copy of an otherwise-good tree:
```
PROBE tampered-copy: ok=False reasons=['pin:1','span:1','pin:4','span:4','pin:7','span:7','pin:10','span:10']
```
Pin and span checks are coupled to the actual copy bytes, not to a
recorded digest.

---

## 5. End-to-end counter corroboration

```
$ python3 .ufo/waves/round-59/count-c2.py --selftest
C2_SELFTEST pass=9 fail=0          # exit 0  (matches contract.md:84 "pass=9 fail=0")
```
Note: the counter's own print label is `C2_SELFTEST`; the frozen
`EXPECT_SELFTEST` constant inside it is the *tool's* label
`SETSCAN_SELFTEST pass=10 fail=0` (count-c2.py:55), which the tool
satisfies:
```
$ python3 <tool from 60b3a76> --selftest --scratch $SCRATCH/st2
SETSCAN_SELFTEST pass=10 fail=0     # exit 0
```

Frozen counter at the **freeze revision**:
```
$ python3 .ufo/waves/round-59/count-c2.py 60b3a76... --scratch $SCRATCH/c2freeze
C2=unmet selftest=ok scan=ok drift=ok trees=ok entry=bad rows=bad pins=bad tree=bad claims=0 files=0 rev=60b3a76... failed=copy_absent:corpus/evidence/sources-r59/w1-results-r54.json,...,entry_absent,tree
EXIT=1
```
At the **entering revision** (do-nothing control):
```
$ python3 .ufo/waves/round-59/count-c2.py 2b9f0397... --scratch $SCRATCH/c2enter
C2=unmet selftest=bad scan=bad drift=bad trees=bad entry=bad rows=bad pins=bad tree=bad claims=0 files=0 rev=2b9f0397... failed=copy_absent:...,drift,entry_absent,scan,selftest,tool_absent,tree,trees,trees_absent
EXIT=1
```
`git cat-file -t 2b9f0397:tools/mori-settlement-scan.py` → absent at the
entering revision, present at freeze → `tool_absent` in the do-nothing
arm is honest, and `trees_absent` there is because the trees themselves
did not exist yet.

**Trees arm at both revisions: `trees=ok`.** That is the arm this seat
owns, and it holds at freeze and at HEAD.

---

## 6. Findings

**F1 — the trees arm is complete, discriminating and correctly frozen.**
All 12 committed trees under `.ufo/waves/round-59/trees-c2/` evaluate
UNMET under the frozen `eval_entry`, each with its frozen expect prefix
covered, each failing for the reason it was frozen to fail (and no other
tree sharing the same reason class by accident — t03/t11 share the prefix
`span` but fail via distinct sub-codes `span:1` vs `span:short=1`).
Non-vacuity is demonstrated in both directions (§4). No tree escapes its
root. Expect files and all tree bytes are identical freeze→HEAD.

**F2 — C2 as a whole is not yet met at the freeze revision or at HEAD.**
The counter reports `C2=unmet` at both `60b3a76` and `HEAD` (8ff344ff)
because the entry `corpus/knowledge/wave-settlement-artifacts-r59.md` and
the six artifact copies under `corpus/evidence/sources-r59/` do not exist
in either tree (`entry_absent`, `copy_absent:…` ×6), while the tool,
selftest, scan, drift and trees arms are already green. The contract's
frozen target `C2=met … claims=N files=F` therefore still depends on the
entry + copies + registry rows being landed by the round's build lane.
This is expected for a pre-build freeze revision; flagged so the L1 does
not read `trees=ok` as `C2=met`.

**F3 — the trees arm does not by itself constrain the entry's content.**
The tree arm exercises `eval_entry` only over synthetic tree roots. The
entry that ships in `corpus/knowledge/` is validated by the same
`eval_entry` in the entry arm (`entry`/`rows`/`pins`/`tree`), which is
currently `bad` only because the entry file is absent — not because any
predicate mis-fires. Any entry landed later must satisfy the *identical*
grammar (frozen `CLAIM` regex, count-c2.py:74-76) that the 12 trees
already exercise in 12 distinct failure modes.

**F4 — no post-freeze drift in the artefacts this seat audits.**
`git diff 60b3a76 HEAD` over `trees-c2/` and `count-c2.py` is empty; the
tool's sha256 at freeze equals the frozen `PIN`. Kill rule (contract.md
§C2, "frozen bytes/predicate/target") is currently satisfied for every
byte this seat evaluated.

---

## 7. Risks / blockers

- None blocking for this seat's item. F2 is a *status* observation, not a
  defect: the entry/copies/rows are the build lane's deliverable.
- Residual risk: `eval_entry` reads `root/<file>` for cited copies, so a
  landed entry that cites a copy path outside the frozen `ARTIFACTS` map
  is rejected (`files:outside=…`, as t06 demonstrates) — the build lane
  must cite exactly the six frozen copy paths.
- `ROW` matching in the counter accepts an optional leading indent
  (`^\s{0,3}\|\s*(S\d{3,})\s*\|`), so the registry row shape must keep
  `S###` inside the first three cells; t08's 12-cell row is what the
  `len(cells) != 11` check rejects.

## 8. Tooling

No package installed or updated this wave; no pacman transaction
(`pacman` is paused host-wide and was not invoked). Disk guard checked
before heavy work — green (`/fast/scratch/hyaku` 592.6G free, 27% use);
no ENOSPC.

## 9. Cleanup

`/fast/scratch/hyaku/mori-r59/Mo59Executor42/` (enum_trees.py, extracted
trees, materialized counter copy, tool copy, counter scratch dirs) was
removed after the receipt above was captured. Lane tree left clean apart
from this report and the pre-existing untracked round-59 dispatch
artifacts (`w1/`, `w1.ready.dispatched`, `w1-dispatch.stderr`,
`assimilation/`) that I did not create and did not touch.
