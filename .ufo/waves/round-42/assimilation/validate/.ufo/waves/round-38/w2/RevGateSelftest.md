# RevGateSelftest — wave-2 review of `tools/mori-sources-appendonly.py --selftest`

Lane HEAD at review time: `f725f3076972e6e70595b5ac8279be524a111ff8` (scored tip, jj-colocated).
Review method: every claim below is backed by a command I ran this session; nothing is cited
from a prior report. LSP is not applicable — the artifact under review is a standalone Python
script verified by direct execution.

## Verdict: PASS (no findings)

## Tally

| Run | Command | Output | Exit |
|---|---|---|---|
| current | `python3 tools/mori-sources-appendonly.py --selftest` | `MORI_SOURCES_APPENDONLY_SELFTEST pass=9 fail=0` | 0 |
| e37dcc6 baseline | `git show e37dcc6:tools/mori-sources-appendonly.py > scratch/tool-before.py && python3 scratch/tool-before.py --selftest` | `MORI_SOURCES_APPENDONLY_SELFTEST pass=8 fail=0` | 0 |

Tally improved 8 → 9; no regression. The stored evidence agrees:
`.ufo/waves/round-38/evidence/gate-selftest-before.txt` shows `pass=8`,
`gate-selftest-after.txt` shows `pass=9`.

## Case-inventory delta (e37dcc6 → f725f30)

`grep -n '^        ("'` on both versions shows one new named case: `"supersede before edit"`
(`tools/mori-sources-appendonly.py:441-444`). The `"superseding row"` case
(`:437-440`) predates round 38 but was materially strengthened: at e37dcc6 its expectation was
only `{ids, deleted, superseded, round_changed, superseded_by}` — the old tool contains **zero**
occurrences of `supersede_timing` / `stale_supersede` / `superseded_as_of`, so all timing
assertions are new this round. The "two new cases" framing in the claim holds in substance:
one new fixture + one existing fixture extended with the two timing keys.

## Both timing cases — source, fixture bytes, observed output

### Case "superseding row" (supersede lands AFTER the edit) — source `tools/mori-sources-appendonly.py:437-440`

Snapshots: `base` (S001, anchor "anchor a") → `edited` (S001 anchor → "anchor a v2") →
`superseding` (S002 lands with `teaches=supersedes S001 — replacement`).
Hand-written expectation: `ids=[S001]`, `superseded=[S001]`, `round_changed=[S001]`,
`superseded_by={S001:S002}`, `superseded_as_of=[S001]`, **`stale_supersede=[]`**, exit 1.

Fixture bytes (rebuilt via the tool's own `_row`/`_render`, byte counts verified):

- `after_c2_superseding.md` (454 bytes):
  ```
  # SOURCES — selftest registry

  ## Registry

  | id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
  |---|---|---|---|---|---|---|---|---|---|---|
  | S001 | https://example.invalid/a | docs | A | scope a | anchor a v2 | teaches a | mined | 2026-01-01 | on-release | n/a |
  | S002 | https://example.invalid/b | docs | A | scope a | anchor b | supersedes S001 — replacement | mined | 2026-01-01 | on-release | n/a |
  ```

Observed output (real sandbox repo, same `HEAD --repo <sandbox> --round-base <sha>` call shape
as `selftest()`, exit=1):
```
changed S001 superseded_by=S002
appendonly_violations=1 ids=[S001] deleted=[] superseded=[S001] round_changed=[S001]
supersede_timing superseded_as_of=[S001] stale_supersede=[]
```
→ prints `stale_supersede=[]` (the `sto=[]` acceptance). **Requirement met.**

### Case "supersede before edit" — source `tools/mori-sources-appendonly.py:441-444`

Snapshots: `with_old_superseder` (S001 original + S002 already carrying
`supersedes S001` in commit c0) → `old_superseder_then_edit` (S001 anchor → "anchor a v3"
in commit c1, superseder unchanged). Hand-written expectation: `ids=[S001]`,
`superseded=[S001]`, `round_changed=[S001]`, `superseded_by={S001:S002}`,
`superseded_as_of=[]`, **`stale_supersede=[S001]`**, exit 1.

Fixture bytes:

- `before_c0_with_old_superseder.md` (451 bytes):
  ```
  # SOURCES — selftest registry

  ## Registry

  | id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
  |---|---|---|---|---|---|---|---|---|---|---|
  | S001 | https://example.invalid/a | docs | A | scope a | anchor a | teaches a | mined | 2026-01-01 | on-release | n/a |
  | S002 | https://example.invalid/b | docs | A | scope a | anchor b | supersedes S001 — replacement | mined | 2026-01-01 | on-release | n/a |
  ```
- `before_c1_old_superseder_then_edit.md` (454 bytes): identical except S001's anchor cell is
  `anchor a v3`.

Observed output (real sandbox repo, exit=1):
```
changed S001 superseded_by=S002
appendonly_violations=1 ids=[S001] deleted=[] superseded=[S001] round_changed=[S001]
supersede_timing superseded_as_of=[] stale_supersede=[S001]
```
→ the before-edit fixture **does list its id in `stale_supersede`**. Requirement met.

## Logic cross-check (`analyze`, lines 282–289)

`superseded_as_of` requires `landing > last_edit[cid]` — strict commit-index ordering — and
`stale_supersede` takes everything else, including `landing == last_edit` (same-commit
supersede counts as stale; consistent with the docstring "landed at or before the edit",
line 33). For the before-edit fixture: superseder landing index 0, last edit index 1 →
`0 > 1` false → `stale_supersede=[S001]`; S001 still correctly appears in `ids` and
`round_changed` because the edit itself is a real in-round immutable change. The harness
enforces exactly one `supersede_timing` line per run (lines 506–509) and compares all six
expected keys including both timing lists (516–520) plus `superseded_by` per-id lines
(523–529), so the expectations are genuinely load-bearing, not decorative.

## Residual risk / gaps

- Timing verdict is commit-index ordering along `git log --reverse` of the file's history,
  not DAG ancestry; on a linear fixture this is equivalent, and the docstring honestly
  describes index semantics. A merge/branchy sandbox would exercise it differently — no
  selftest case covers that. Not a defect of the claimed behavior; noted as untested surface.
- No case covers `landing == last_edit` (supersede row and the edit landing in the same
  commit). The code treats it as stale, which is the conservative direction.
- No tools installed; none needed.

## Fail checks (from acceptance)

- before-edit case lists id in `stale_supersede` → **yes** (`stale_supersede=[S001]`, observed).
- tally regression → **none** (8→9 at the scored tip; both runs reproduced live).
