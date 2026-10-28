# Mo59Reviewer03 — C1 pointer attack (backticked evidence tokens)

Scope: adversarial probe of the pointer arm of frozen counter
`.ufo/waves/round-59/count-c1.py` (freeze `60b3a76a`; worktree bytes verified
identical to freeze, sha256 match) against syntactically-valid / semantically-wrong
backticked evidence tokens in the active `## Capabilities` register rows
(`SCORECARD.md:1989-1990`, cells `` `…`; `…` `` separated by `;`).

Method (bounded): `--shared` clone of the lane into scratch (object store untouched,
18 throwaway commits, `git rev-parse --show-toplevel` asserted = scratch clone).
Each variant mutates exactly one pointer cell of row `rounds[832].capabilities_added[0]`,
commits, and runs the real frozen counter:
`python3 .ufo/waves/round-59/count-c1.py <rev> --repo <clone> --fleet <fleet> --scratch <seat-dir>`.
The tool itself is exercised identically to the counter's real arm
(pass 1 learns `pointers`, counter runs `git cat-file -e R:ptr` then `materialize`,
pass 2 re-judges). Baseline on the real lane HEAD `8ff344ff`:
`C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=HEAD`, rc 0.

## Findings (by severity)

### F1 — Hostile pointer tokens crash the counter instead of scoring UNMET (medium)

The tool emits **raw** backticked tokens in `out["pointers"]`
(`tools/mori-register-check.py:176-177` — `all_ptrs.extend(ptrs)` before the
`pointer_ok` filter), and the counter loops `git cat-file -e` + `materialize`
over all of them (`count-c1.py:186-193`). Two crash shapes, both rc=1 with an
uncaught `IsADirectoryError`/`FileExistsError` traceback and **no `C1=` line on
stdout** (frozen output contract unmet — a verdict parser sees silence, not a grade):

| variant cell (row [0]) | counter result |
|---|---|
| `` `tools/mori-vote-bind.py`; `` `` (empty token) | crash: `IsADirectoryError: …/_root` — `cat-file -e "R:"` resolves the **root tree** (rc 0), `materialize` writes the root listing onto `_root/` itself (`write_bytes` at `count-c1.py:87`) |
| `` `./`; `…` `` | same crash — `./` strips to `""`, root tree again |
| `` `tools/`; `.ufo/waves/round-56/evidence/c2-at-landed.txt` `` | crash: `FileExistsError: …/_root/tools` — dir materialized as a **file** containing `tree <rev>:tools`, then the next pointer needs `_root/tools/` as a directory |
| `` `.ufo`; `.ufo/waves/…` `` | crash: `NotADirectoryError: …/_root/.ufo/waves/…` — same ancestor-collision |

Tool pass-1 correctly emits `pointers:bad=`/`pointers:missing=…` reasons for these
tokens, but the counter crashes in its own materialize pass before pass 2.

### F2 — Directory pointers are accepted as evidence (low; spec-shaped gap)

The frozen predicate requires only that each reported path "resolves under R via
`git cat-file -e R:path`" — which succeeds on **tree** objects. A register row
whose evidence pointer is a directory still earns `C1=met … pointers=ok`:

| variant cell | counter result |
|---|---|
| `` `…`; `corpus` `` (extra pointer) | `C1=met … pointers=ok`, rc 0 (`rev=b6c3bb1d`) — `_root/corpus` materialized as a **file** containing `tree b6c3bb1d…:corpus` listing bytes |
| `` `…`; `.ufo/waves/round-59` `` | `C1=met … pointers=ok`, rc 0 |
| `` `…`; `tools/fixtures` `` | `C1=met … pointers=ok`, rc 0 — `_root/tools/fixtures` = tree-listing file |

Semantic cost: a row "bound" to an evidence directory carries no artifact
binding at all (every directory trivially resolves); the tool's `is_file()`
check at `tools/mori-register-check.py:185` is bypassed because materialize
turns the tree listing into a regular file before pass 2.

### F3 — Duplicate pointer accepted (informational)

`` `tools/mori-vote-bind.py`; `tools/mori-vote-bind.py` `` → `C1=met … pointers=ok`,
rc 0 (`rev=57809f85`). No distinctness check exists in tool or counter.
Consistent with the frozen predicate (resolution-only), flagged because the
fixture suite does exercise duplicate *keys* but no pointer-shape arm covers it.

### F4 — Reachability-only: unrelated file accepted (informational)

`` `.gitignore`; `.ufo/waves/round-56/evidence/c2-at-landed.txt` `` → `C1=met`,
rc 0 (`rev=5cafbf4e`). Any existing in-tree file satisfies the arm; nothing binds
the pointer to the capability's round or evidence dirs. Per frozen predicate this
is conformant — noted so the claim isn't oversold as "evidence validated".

## Rejected cleanly (no counterexample)

| variant | counter result |
|---|---|
| `` `…` `` (bare U+2026) | `C1=unmet … failed=pointer:…,real,pointers`, rc 1 |
| `` `tools/mori-…-bind.py` `` | `C1=unmet … failed=pointer:tools/mori-…-bind.py,…` |
| `` `tools/mori-vote-bind.py ` `` (trailing ws in backticks) | `C1=unmet … failed=pointer:tools/mori-vote-bind.py ,…` — `pointer_ok` strips for the form check but the raw token feeds `is_file()`/`cat-file`, no bypass |
| `` ` tools/mori-vote-bind.py` `` (leading ws) | `C1=unmet … failed=pointer: tools/…` |
| `` `.` `` | `C1=unmet … failed=pointer:.,…` (`cat-file -e R:.` = 128) |
| `` `tools/./mori-vote-bind.py` `` | `C1=unmet` (git refuses `.` segments) |
| `` `~/etc/passwd` `` | `C1=unmet` (tilde rejected by `pointer_ok`) |
| `` `tools/a; b` `` (one token with `;`) | `C1=unmet` (raw token unresolved) |
| trailing ws **outside** backticks in the cell | `C1=met` (cell strip — conformant) |

## Residual risk / verification gaps

- Symlink-pointer and gitlink-pointer shapes untested (lane carries no gitlinks
  at HEAD: `git ls-tree -r HEAD` shows no `160000` entries); a symlink pointer
  would materialize as its target-text file — same accept shape as F2.
- F1's crash occurs only on the *real arm* path; the 13 hostile fixtures run a
  single `run_tool` pass against pre-materialized `_files`, so fixture coverage
  cannot exhibit it — the crash is reachable only through register rows at R.
- Pointer content is never pinned (no sha check of the resolved file); not
  claimed by the predicate, so out of scope as a defect.
- Bounded: 18 mutated-cell variants + git object probes; manifest arm,
  name-binding arm and expect-prefix matching not exercised (other seats' scope).

Receipts: variant revs inline above; scratch `/fast/scratch/hyaku/mori-r59/Mo59Reviewer03/`
(clone + run dirs) removed after this report.
