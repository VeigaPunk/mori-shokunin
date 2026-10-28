# Mo59Reviewer01 — C1 fixture battery re-verification (round 59, w1)

**Scope.** Materialize each of the 13 committed `.ufo/waves/round-59/fixtures-c1/`
trees at freeze revision `60b3a76ad0524c8978cc51922940be1c8c388915`, run the
pinned `tools/mori-register-check.py` over each, confirm the observed reason
prefixes cover `expect.txt`, and report any fixture that scores met or fails
for a different reason. Read-only on lane and fleet; all writes under
`/fast/scratch/hyaku/mori-r59/Mo59Reviewer01/` (deleted after this report).

**Verdict.** No counterexample to the frozen predicate: 13/13 fixtures exit 1
with `verdict=REGISTER_UNMET`, valid JSON, empty stderr, and every
`expect.txt` token prefix-covered by observed reasons; the designed hostile
reason token is present in all 13. One MEDIUM harness defect (nested
materialization dilutes the pointer-class fixtures) plus three low/info items.

## Method (bounded)

- Tool blob at freeze: `git show 60b3a76a:tools/mori-register-check.py` →
  sha256 `38b733d896f880f5b7ecb464848b80798810ab052fcf0a8afb320918151472b8` ==
  counter `PIN` (count-c1.py:40). `git cat-file -e
  2b9f0397…:tools/mori-register-check.py` → 128 (absent at entering, as claimed).
- Enumeration identical to counter: `git ls-tree --name-only
  60b3a76a:.ufo/waves/round-59/fixtures-c1` → exactly the 13 dirs f01–f13
  (all `tree` type; no `.py` blobs).
- Faithful harness replication of `measure()`'s fixture arm
  (count-c1.py:130–161): same `ls-tree -r` per fixture, same skip set
  (`scorecard.md|manifest.json|expect.txt`), same `materialize(repo,rev,[f],
  fdir/"_files")` **with the full repo-relative path `f`** (line 151 — see F1),
  same argv (`--scorecard … --manifest … --root <fdir>/_files --require
  rounds[832].capabilities_added[0] --require
  rounds[832].capabilities_added[1]`), `cwd=<scratch>/cwd`, same coverage
  predicate `all(any(r.startswith(e) for r in reasons) for e in
  expect.split(","))` (line 158) and `verdict_unmet` (lines 159–160).
- Positive control: flat-root run with clean scorecard+manifest payloads
  → `REGISTER_MET`, `reasons:[]`, exit 0 (proves met is reachable and the
  missing-pointer reasons below are layout-induced, not tool bugs).
- End-to-end: `python3 .ufo/waves/round-59/count-c1.py 60b3a76a…
  --scratch <seat>` → `C1=met selftest=ok fixtures=ok real=ok pointers=ok
  rev=60b3a76a…` exit 0 (target line verbatim). At entering `2b9f0397…`:
  `C1=unmet … failed=tool_absent,selftest,fixtures_absent,real,pointers`
  exit 1 (before-arm consistent; `fixtures_absent` because fixtures were
  committed at freeze).
- Tool selftest: `REGCHECK_SELFTEST pass=12 fail=0` exit 0 (== EXPECT_SELFTEST).
- Byte identity: worktree `count-c1.py`, `count-c2.py`, `contract.md` sha256 ==
  freeze blobs (no post-freeze drift observed at HEAD `8ff344ff`).

## Per-fixture results (freeze rev; designed token = the hostile edit's reason)

| fixture | expect | exit | verdict | covered | designed token fired | reasons (full set) |
|---|---|---|---|---|---|---|
| f01-stub-only | `binding` | 1 | UNMET | yes | `binding:declared_register=0(capabilities_sections=1)` | + `keys:missing` ×2 (rows never parsed: n_decl≠1 short-circuits row collection) |
| f02-two-declared | `binding` | 1 | UNMET | yes | `binding:declared_register=2(capabilities_sections=3)` | + `keys:missing` ×2 (same short-circuit) |
| f03-dup-key | `keys` | 1 | UNMET | yes | `keys:duplicate=rounds[832].capabilities_added[0]` | + `manifest:name=…[0]` (dup row's "dup name"), `pointers:missing` ×4 |
| f04-missing-key | `keys` | 1 | UNMET | yes | `keys:missing=rounds[832].capabilities_added[1]` | + `pointers:missing` ×2 (row 0) |
| f05-pointer-missing | `pointers` | 1 | UNMET | yes* | `pointers:missing=.ufo/waves/round-56/evidence/c2-at-landed.txt` (the one file absent from f05's tree) | + `pointers:missing` ×3 more |
| f06-pointer-absolute | `pointers` | 1 | UNMET | yes | `pointers:bad=/etc/passwd` | + `pointers:missing` ×3 |
| f07-pointer-relative-parent | `pointers` | 1 | UNMET | yes | `pointers:bad=../../etc/passwd` | + `pointers:missing` ×3 |
| f08-manifest-name-altered | `manifest:name` | 1 | UNMET | yes | `manifest:name=rounds[832].capabilities_added[0]` (manifest `renamed capability (x)`) | + `pointers:missing` ×4 |
| f09-manifest-substring-only | `manifest:name` | 1 | UNMET | yes | `manifest:name=rounds[832].capabilities_added[0]` (manifest `zzdual-shape…more`: neither equal nor name-prefix) | + `pointers:missing` ×4 |
| f10-manifest-foreign-lane | `manifest:lane` | 1 | UNMET | yes | `manifest:lane='kotoba'` ×2 (once per required key) | + `pointers:missing` ×4 |
| f11-manifest-wrong-index | `manifest` | 1 | UNMET | yes* | `manifest:entry_missing` ×2 (caps live at `rounds[700]`; `rounds[832]={}` in a 900-entry list) | + `manifest:lane=None` ×2, `manifest:lane_round` ×2, `pointers:missing` ×4 |
| f12-lane-round-mismatch | `manifest:lane_round` | 1 | UNMET | yes | `manifest:lane_round` ×2 (`lane_round:55` vs cell `56`) | + `pointers:missing` ×4 |
| f13-empty-pointer | `pointers` | 1 | UNMET | yes* | `pointers:none=rounds[832].capabilities_added[1]` (literal `none` cell, no backticks) | + `pointers:missing` ×2 (row 0) |

`*` = covered, but coverage does not depend on the designed token — see F1.
Manifest blobs: f01–f07 + f13 share the canonical manifest
(`29d520da…`); f08–f12 each carry a distinct mutated manifest.

## Findings (by severity)

### F1 — MEDIUM: fixture-arm materialize nests files → every committed payload unresolvable → pointer-class fixtures' expect coverage is vacuous

`count-c1.py:151` calls `materialize(repo, rev, [f], fdir / "_files")` where
`f` is the **repo-relative** path
(`.ufo/waves/round-59/fixtures-c1/<name>/tools/mori-vote-bind.py`), while the
tool resolves scorecard pointers as `<root>/<pointer>` with root =
`fdir/_files` (count-c1.py:153). Observed on disk:

```
harness/fx/f05-pointer-missing/_files/
  .ufo/waves/round-59/fixtures-c1/f05-pointer-missing/tools/mori-vote-bind.py   ← nested
  # tool wants _files/tools/mori-vote-bind.py                                 ← absent
```

Consequence: every `tools/mori-*.py` and `.ufo/…/at-landed.txt` pointer in every
fixture reports `pointers:missing` (the ×2–×4 noise in the table). All file
payloads the fixtures commit are dead weight — a fixture consisting of only
`scorecard.md`+`manifest.json`+`expect.txt` scores identically. Positive
control with a flat root using the *same* payloads emits `REGISTER_MET`,
confirming the layout (not the tool) produces the noise.

Impact on the battery: for f05 (`pointers`), f07 (`pointers`), f13
(`pointers`) the `expect` token is satisfied by incidental
`pointers:missing` even if the designed reason never fires — regressions in
missing-pointer detection, `..` rejection, and empty-cell detection are
uncatchable at coverage level (only total removal of all pointer reasons,
which would flip verdict to MET, is caught). f06 is unaffected
(`pointers:bad=/etc/passwd` is unique in the battery). The frozen predicate
itself still holds — every fixture is genuinely UNMET and its designed token
is present — so this does not invalidate today's counter, but the hostile
battery is materially weaker than "each MUST score UNMET covering its frozen
expect prefix" implies. Fix direction (not applied): `materialize(repo, rev,
[rel], fdir/"_files")` at line 151 — i.e., strip the `base + "/"` prefix, as
the counter already computes `rel` at line 148 for the skip check.

### F2 — LOW: f11's expect token `manifest` is namespace-wide

Any `manifest:*` reason satisfies it. If `entry_missing` detection regressed,
the incidental `manifest:lane=None`/`manifest:lane_round` (both fire because
`rounds[832]={}`) would still cover `manifest`. The designed defect
(caps at `rounds[700]`, not 832) is detected today, but the token cannot
attribute failure to it. A sharper token (`manifest:entry_missing`) would bind
the fixture to its named hostility.

### F3 — LOW (latent): `manifest:lane` prefix-collides with `manifest:lane_round`

`'manifest:lane_round=x'.startswith('manifest:lane')` → True. f10's expect
token could be satisfied by a lane_round reason if lane-checking regressed.
Today f10 emits the correct `manifest:lane='kotoba'` and no `lane_round`
(value matches), so latent only. Tokens are not prefix-disjoint by
construction.

### F4 — INFO: cosmetic reason-set noise

`manifest:lane`/`entry_missing`/`lane_round` emit once per required key (f10,
f11 emit duplicates); `manifest:lane=None` renders Python `None` for the
missing `lane` field. Harmless; noted for report-readers diffing reason sets.

## Honest-statement check

- "13 committed trees": confirmed — 13 `tree` entries, each with
  `scorecard.md`+`manifest.json`+`expect.txt` present at freeze.
- "each MUST score UNMET covering its frozen expect prefix": observed true
  (table above); no fixture scored met, none failed for a different reason
  (designed token present in all 13).
- "Any scoring met invalidates the counter": none scored met.
- Counter end-to-end at freeze reproduces the frozen target output exactly;
  at entering it reports `tool_absent` first as the contract's before-arm
  claims.

## Residual risk / verification gaps

- Re-verification replicates the counter's own harness by construction; an
  independent *flat-layout* run of the 13 fixtures was used only for the
  positive control. Under flat layout f05's designed miss would still fire
  (its tree genuinely lacks `c2-at-landed.txt`); f06/f07/f13 unchanged.
- Single environment (host python3); no fuzzing beyond committed trees;
  no mutation testing of the tool (mutation-tester lane owns that).
- `expect.txt` tokens parsed with counter semantics (no empty-token
  filtering); all files are single-token with no trailing commas — no
  ambiguity exercised.
- The nested-materialize defect is reported, not fixed (detection/report
  only; seat charter).

## Housekeeping

- No production/corpus/SCORECARD/VCS writes; lane repo read-only throughout.
- Scratch `/fast/scratch/hyaku/mori-r59/Mo59Reviewer01/` deleted after this
  report; the receipt above is self-contained.
- Tool installs/updates: none (all work used system `python3`+`git`; no
  package channels touched).
