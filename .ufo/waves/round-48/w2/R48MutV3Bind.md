# R48MutV3Bind — mutation test of the landed v3 pin reconciler (R4/R5/R6/R10 arms)

**Attacked:** the claim that the landed v3 tool `tools/mori-pin-check.py` (tip `e4dfff32`,
sha256 `85a89a3b6ba4eb5ed0b3f784763cfe78652e6493b055b3dcf8924feaffff82e1`) has `--selftest`
arms that kill single-point removals/weakenings of R4 (rebound by prefix), R5 (line-count
pins), R6 (truncated-digest pin) and R10 (full digest binds to the nearest *preceding*
in-tree path of its own cell). 8 single-point mutants, all in a scratch copy under
`.scratch/r48w2-R48MutV3Bind/`; the tracked file was never opened by an edit tool.

**Verdict: BREAKS (coverage class, 2 of 8 mutants survive).**
R4 (both mutants), R5 binding, R6 (both) and R10 row-wide-resurrection are killed by
existing arms. But the suite cannot distinguish (a) an R5 comparison flipped from
`!=` to `>` — a line-count pin claiming *more* lines than the file has is accepted — nor
(b) an R10 binding flipped from nearest-*preceding* to nearest-*following* path. Both
survivors score `PIN_CHECK=met` (exit 0) on a registry the real tool scores `unmet`
(exit 1). This is a selftest-coverage finding about the mutant-kill arms, not a defect
observed in the landed tool: on both reproducers the real tool itself answers `unmet`
correctly. Per contract, reported as a limit; no tool or contract change made.

## Method

- Pristine copy: `cp tools/mori-pin-check.py .scratch/r48w2-R48MutV3Bind/pristine.py`,
  sha256 `85a89a3b…` — byte-identical to the tracked file (verified before and after).
- Baseline detector: `TMPDIR=<scratch> python3 pristine.py --selftest` → rc 0,
  `PIN_CHECK_SELFTEST pass=60 fail=0`. Detector valid; every verdict below is a
  baseline-passing comparison.
- Detector per mutant: `TMPDIR=<scratch> python3 <mutant>.py --selftest`; **killed iff
  non-zero exit**; the killing arm is the `FAIL` case the run prints.
- Reproducers: fixture trees under the scratch dir, measured via
  `python3 <tool> --root <fixture> --repo <scratch>` (read-only over the fixture; tool
  scratch dirs land inside the seat scratch).

## Result table

| # | rule | mutation (single point) | verdict | killing arm (observed FAIL) |
|---|---|---|---|---|
| m_r4a | R4 | `check()`: `rebound = True  # existing row changed its bound argv` → `rebound = False` (existing-row argv change never flagged) | **killed** (rc 1, `pass=58 fail=2`) | `v2_rebound_to_other_tool`; also `v2_entry_rebound` — both print `PIN_CHECK=met … rebound=0` where `rebound` was required |
| m_r4b | R4 | `check()`: `len(base_bind_prefix[prefix]) == 1` → `== 0` (new-row rebind of a single-instrument prefix never flagged) | **killed** (rc 1, `pass=59 fail=1`) | `r4_rebound_new_row_same_prefix` — `PIN_CHECK=met tally_pins=2 … rebound=0` |
| m_r5a | R5 | `check()` line-count branch: `if nl != num:` → `if nl > num:` (a pin claiming **more** lines than the file has is accepted) | **SURVIVED** (rc 0, `pass=60 fail=0`) | none existing — reproducer + proposed arm below |
| m_r5b | R5 | `line_count_pins()`: binding `_nearest_in_tree_path(st[:m.start()], root)` → `None` (pins never bind → always `unparsed`) | **killed** (rc 1, `pass=58 fail=2`) | `r5_line_count_match` (honest registry goes `unmet unparsed=1`); also `r5_line_count_mismatch` |
| m_r6a | R6 | `trunc_digest_pins()`: `.startswith(pfx)` → `.startswith(pfx[:4])` (only 4 hex chars must match) | **killed** (rc 1, `pass=59 fail=1`) | `r6_trunc_digest_mismatch` — `PIN_CHECK=met digest_pins=1 mismatches=0` |
| m_r6b | R6 | `trunc_digest_pins()`: `hit = p if …startswith(pfx)… else None` → `hit = p` (any in-tree path satisfies the truncated digest) | **killed** (rc 1, `pass=58 fail=2`) | `r6_trunc_digest_mismatch`; also `r10_trunc_digest_decoy_file_in_other_cell` |
| m_r10a | R10 | `check()` full-digest loop: `_nearest_in_tree_path(st[:dm.start()], root)` → `_nearest_in_tree_path(" ".join(cells), root)` (row-wide binding, the pre-R10 behaviour) | **killed** (rc 1, `pass=59 fail=1`) | `r10_digest_decoy_file_in_other_cell` — decoy path in another cell satisfies the digest |
| m_r10b | R10 | same site: `st[:dm.start()]` → `st[dm.end():]` (digest binds to the nearest **following** path) | **SURVIVED** (rc 0, `pass=60 fail=0`) | none existing — reproducer + proposed arm below |

## Survivors — reproducers (mutant `met`/exit 0, real tool `unmet`/exit 1) and killing arms

### m_r5a (R5 comparison flipped to `>`)

Fixture `.scratch/r48w2-R48MutV3Bind/fix-r5a/`: `tools/lc.py` has exactly **42** newlines and
prints `LC_SELFTEST pass=1 fail=0`; `SKILL.md` row (8-cell v3 header):

```
| foo | gate | `python3 tools/lc.py` | 0 ok | `python3 tools/lc.py --selftest` → `LC_SELFTEST pass=1 fail=0` (99 lines) | none | none | mori |
```

Observed (`--root fix-r5a --repo <scratch>`, both tools on identical bytes):

- REAL `pristine.py`: rc **1**, `PIN_CHECK=unmet … mismatches=1 …`, pin line
  `pin line=3 kind=lines state=mismatch pinned='99 lines' file=tools/lc.py observed=42`
- MUTANT `m_r5a.py`: rc **0**, `PIN_CHECK=met … mismatches=0` (it still *prints*
  `state=mismatch` on the pin line but no longer counts it — 42 > 99 is false).

**Proposed killing arm** (verified: under this row the mutant's `check()` returns
`met=True` so the case `(…, 1, False, "mismatch")` fails and `--selftest` exits non-zero;
pristine returns `met=False` with a `state=mismatch` line, so the arm passes on the real tool):

```python
("r5_line_count_overpin_mismatch", HDR + row("`python3 tools/lc.py --selftest` → `LC_SELFTEST pass=1 fail=0` (43 lines)",
                                             entry="`python3 tools/lc.py`"), 1, False, "mismatch"),
```

### m_r10b (R10 preceding→following binding flip)

Fixture `.scratch/r48w2-R48MutV3Bind/fix-r10b/`: `tools/foo.py` prints
`FOO_SELFTEST pass=3 fail=0`; `tools/slow.py` sha256 `641f3f27d494…`; the row places the
digest **before** its file path:

```
| foo | gate | `python3 tools/foo.py` | 0 ok | `python3 tools/foo.py --selftest` → `FOO_SELFTEST pass=3 fail=0`; sha256 `641f3f27d494…64 hex…` of `tools/slow.py` | none | none | mori |
```

Observed (same command shape):

- REAL `pristine.py`: rc **1**, `PIN_CHECK=unmet … mismatches=1`, pin line
  `pin line=3 kind=digest state=mismatch digest=641f3f27d494 file=tools/foo.py`
  (nearest *preceding* in-tree path is `tools/foo.py`, whose sha differs).
- MUTANT `m_r10b.py`: rc **0**, `PIN_CHECK=met … mismatches=0`, pin line
  `pin line=3 kind=digest state=match digest=641f3f27d494 file=tools/slow.py`
  (it happily binds to the path *after* the digest).

**Proposed killing arm** (verified the same way — mutant `met=True` → case fails; pristine
`met=False` with `state=mismatch`):

```python
("r10_digest_binds_to_nearest_preceding_path_not_following", HDR + row(
    "`python3 tools/foo.py --selftest` → `FOO_SELFTEST pass=3 fail=0`; sha256 `%s` of `tools/slow.py`" % slow_digest,
    entry="`python3 tools/foo.py`"), 1, False, "mismatch"),
```

Both proposed arms reuse only fixtures the selftest already builds (`tools/lc.py`,
`tools/slow.py`, `tools/foo.py`); no new fixture class is needed to close the gaps.

## Restoration / integrity evidence

- Pristine scratch copy sha256 **before** any mutation:
  `85a89a3b6ba4eb5ed0b3f784763cfe78652e6493b055b3dcf8924feaffff82e1`;
  **after** all runs (unchanged — mutants live in separate `m_*.py` files):
  `85a89a3b6ba4eb5ed0b3f784763cfe78652e6493b055b3dcf8924feaffff82e1`.
- Tracked `tools/mori-pin-check.py` after all runs:
  `85a89a3b6ba4eb5ed0b3f784763cfe78652e6493b055b3dcf8924feaffff82e1`;
  `git status --porcelain -- tools/` empty; HEAD `e4dfff32d4f97c7ef250e9a7538fa75d4f284492`.
- Mutant hashes (for the record): m_r4a `c8727bfb…`, m_r4b `51691d17…`, m_r5a `7676ca9e…`,
  m_r5b `fb7b4ec6…`, m_r6a `43796288…`, m_r6b `c91803f9…`, m_r10a `c5950354…`,
  m_r10b `05946274…`.
- No tracked path was passed to an edit tool; no git/jj mutating command run; every lane-tool
  run used `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48MutV3Bind`.

## Limits

- Single-point mutations only, one per listed defect class; a compound or differently-shaped
  weakening of R4/R5/R6/R10 may behave differently.
- The detector is the tool's own `--selftest` (per seat tasking); `count-c1.py`'s 12 variants
  were not run against the mutants, so a survivor's impact on the frozen C1 predicate is
  UNVERIFIED here.
- The survivors show the selftest would accept two *weakened tools*; they do not show the
  landed tool mis-scoring any registry — on both reproducers the real tool answers `unmet`.
