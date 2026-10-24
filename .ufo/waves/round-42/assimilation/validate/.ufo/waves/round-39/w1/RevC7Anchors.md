# RevC7Anchors — independent `anchors_v2` resolution at 13bfba23 (mori r39)

Verdict: **PASS on `anchors_v2`** (detection only; no FAIL). All three `anchor:` lines of
`corpus/knowledge/source-drift-content-anchor-r38.md` resolve independently, byte-exactly, at a
non-comment code position in `tools/mori-source-drift.py` at
`13bfba23b7ca063c76d3504a2ff6eb7b6a294932`; the counter detail in
`.ufo/waves/round-39/evidence/c7-after.txt` agrees exactly and hides nothing. Two low-severity
provenance/discriminator residuals are disclosed below; neither changes the verdict on the frozen
predicate.

Write scope: this report only. Scratch verifier and outputs:
`.ufo/waves/round-39/scratch/RevC7Anchors/{verify_anchors.py,docstring_probe.py,after-13bfba23.txt}`.
No lane file mutated, no vetoed path touched, no tool installed.

## Inputs (revision-pinned, byte-verified)

| input at 13bfba23 | sha256 | bytes |
|---|---|---|
| `corpus/knowledge/source-drift-content-anchor-r38.md` | `0fd361d4d0c0d1b70f07b03661b22fb9af0c2b3c3a0fc24f2700f68506736005` | — |
| `tools/mori-source-drift.py` | `453c5d8e260301df7a99daf62b4c16ea08e4a0b4f9e4f53821cdbce447011552` | 19624 |
| `.ufo/waves/round-39/count-c7.py` | `b92c65f224a6268a901aa6bc5ad66b499048eaca82b493356eb8e1f324ef0520` | — |
| `.ufo/waves/round-39/evidence/c7-after.txt` | `d4fa1b8c44897e84ec244a2536ca8f33b0a8db2d` (git blob) | — |

Worktree bytes (HEAD `ebc61f47`, which has 13bfba23 as ancestor) are identical to the 13bfba23
blobs for all five files checked — `count-c7.py`, `c7-after.txt`, `contract.md`, the tool and the
entry (`sha256sum` vs `git show 13bfba23:<p> | sha256sum` → `SAME` each). The counter reads blobs
with `git show` (`count-c7.py:192-207`), so the worktree advance by later wave-report commits does
not move the measured bytes. Both input files contain 0 CR bytes, so the counter's text-mode read
does not perturb the "byte-exactly" claim.

## Rule applied independently (not via the counter)

For each line whose **stripped** form starts with `anchor:`, the anchor is the remainder stripped;
require length ≥ 8, byte-exact occurrence in the tool blob, at least one occurrence starting at a
position that is **not inside a comment**, and no duplicate anchors. Comment classification was done
two ways: Python `tokenize` COMMENT token spans (lexical truth) and the counter's stated rule
(strip-startswith-`#` lines never count; otherwise the occurrence must start before the first `#` on
its line). Occurrences were also checked against STRING tokens and `ast` docstring spans so a
string-parked occurrence could not be silently counted as code.

## Per-anchor resolution (entry lines 26–28; each line is indented 3 spaces as markdown list continuation)

| # | anchor (after strip) | len | ≥8 | tool occurrence(s) at 13bfba23 | classification | counter rule |
|---|---|---|---|---|---|---|
| 1 | `FETCH_MAX_BYTES = 4 * 1024 * 1024` | 33 | yes | **line 54, col 0**, offset 1930 — exactly one | code (COMMENT=false, STRING=false, docstring=false); `#` begins later in the line | counts |
| 2 | `if not _public_redirect_target(final):` | 38 | yes | **line 158, col 20**, offset 5882 — exactly one | code (not in COMMENT/STRING/docstring) | counts |
| 3 | `return "drifted"` | 16 | yes | **line 208, col 4**, offset 7939 — exactly one | code (not in COMMENT/STRING/docstring) | counts |

Distinct anchors: yes. Each anchor occurs **exactly once** in the tool blob, so even a stricter
"unique occurrence" reading would pass; `unique=True` in the counter detail is not masking a
duplicate occurrence.

Raw evidence (`python3 .ufo/waves/round-39/scratch/RevC7Anchors/verify_anchors.py`), abridged:

```
{"entry_line": 26, "anchor": "FETCH_MAX_BYTES = 4 * 1024 * 1024", "len": 33, ... "occurrences": [{"offset": 1930, "line": 54, "col": 0, "comment_token": false, "string_token": false, "docstring": false, "counter_rule_noncomment": true}]}
{"entry_line": 27, "anchor": "if not _public_redirect_target(final):", "len": 38, ... "occurrences": [{"offset": 5882, "line": 158, "col": 20, ... "counter_rule_noncomment": true}]}
{"entry_line": 28, "anchor": "return \"drifted\"", "len": 16, ... "occurrences": [{"offset": 7939, "line": 208, "col": 4, ... "counter_rule_noncomment": true}]}
distinct anchors: True
counter code_occurrences per anchor: [('FETCH_MAX_BYTES = 4 * 1024 * 1024', [1930]), ('if not _public_redirect_target(final):', [5882]), ('return "drifted"', [7939])]
counter check_anchors_v2: (True, 'anchors=3 short=[] not_in_code=[] unique=True')
```

My offsets equal the counter's `code_occurrences` results exactly. `git grep -n '^anchor:'` over the
whole corpus at 13bfba23 returns only these three lines for this entry (plus the separate
`corpus/knowledge/gate-ancestry-r39.md:43-45`, out of this check's frozen scope — see INFO-3).

## Agreement with `c7-after.txt`

Evidence line: `check anchors_v2       PASS (anchors=3 short=[] not_in_code=[] unique=True)`
(`.ufo/waves/round-39/evidence/c7-after.txt:7`). Independent re-run:

```
python3 .ufo/waves/round-39/count-c7.py 13bfba23b7ca063c76d3504a2ff6eb7b6a294932 --seed 20261024
→ check anchors_v2       PASS (anchors=3 short=[] not_in_code=[] unique=True)
→ C7=met  EXIT=0
```

The full re-run body is byte-identical to the evidence receipt body
(`diff <(sed -n '2,11p' evidence/c7-after.txt) <(sed -n '1,10p' scratch/.../after-13bfba23.txt)` →
empty; scratch file also captured `C7=met` at its line 11). Exit 0. No counter detail hides a
failing anchor: the detail prints the anchor count, the short list, the whole anchor strings that
fail code resolution, and set-distinctness.

Negative witness attribution (`.ufo/waves/round-39/fixtures/witness-comment-anchors.md`, pin
`fc95dc69…` matches `freeze-r39.txt` and the worktree):

```
counter check_anchors_v2(witness, tool) → (False, "anchors=3 short=[] not_in_code=['bounded read: an untrusted source must not stream past the cap', 'a redirect actually happened: the new authority must be public', 'bodies larger than this cannot be classified; read is capped at'] unique=True")
```

The rejection is attributable to `anchors_v2` itself (the other checks are projected onto real
bytes), and the third witness anchor sits in a **trailing** comment on tool line 54, so the
first-`#` rule is exercised rather than only line-start `#`.

## Findings by severity

**LOW-1 — evidence receipt records the parent revision, not the scored tip.**
`c7-after.txt:1` reads `command: python3 .ufo/waves/round-39/count-c7.py f920eaf7 --seed 20261024`;
`f920eaf7` is the data commit *before* 13bfba23 (`git log --oneline`), not a prefix of the scored
tip. Substantively harmless: `git diff --name-only f920eaf7 13bfba23 -- corpus tools` is empty (0
paths), the entry and tool blobs are identical at both revisions, and my re-run at 13bfba23 emits a
byte-identical check body with `C7=met` exit 0. Impact: the receipt alone does not prove the
scored-tip run without re-execution; the claim's C1 command does hold when executed.

**LOW-2 (residual, frozen-predicate letter met) — docstring/string parking passes the non-comment rule.**
`code_occurrences` classifies positions inside Python STRING tokens as code; only COMMENT tokens and
`#` remainders are excluded (`count-c7.py:245-268`). Probe
`scratch/RevC7Anchors/docstring_probe.py`: a toy entry whose three anchors occur **only** in the
tool's docstrings (tool lines 6, 26, 61; each `docstring=True comment=False string=True`) scores
`check_anchors_v2 → (True, 'anchors=3 short=[] not_in_code=[] unique=True')`. P-C7 as frozen says
"not inside a comment" (contract, P-C7; `count-c7.py` PREDICATE), so the counter conforms to the
letter and the current entry is unaffected — all three real anchors are true code positions. The
residual is that the r38 M18 "documentation, not implementing code" class is only killed for `#`
witnesses, not for string-literal witnesses; a future witness of that shape would pass `anchors_v2`.
Paired with the runtime-drawn `drift_kill_v2` arm (which the full counter still reports PASS), this
is bounded, not a free pass for a fabricated binding.

**INFO-3 — scope of `ENTRY_REL` is the r38 drift entry only.**
`ENTRY_REL = "corpus/knowledge/source-drift-content-anchor-r38.md"` (`count-c7.py:57`). The r39
knowledge entry has its own three `anchor:` lines (`corpus/knowledge/gate-ancestry-r39.md:43-45`)
that this check never reads. That matches P-C7's "committed drift-corpus binding" scope, so it is
not a violation, but "every `anchor:` line in the knowledge entry" should be read as singling out
the r38 entry, not all knowledge entries.

**INFO-4 — indentation is load-bearing for discovery.**
The three anchor lines are indented 3 spaces (entry lines 26–28, verified with `cat -A`), and
`anchors_from` strips before matching (`count-c7.py:236-243`). A column-0-only reading of "beginning
`anchor:`" would find 0 anchors and fail the ≥3 floor; the entry's own prose (entry line 22) uses the
same "beginning `anchor:`" phrasing for these indented lines, and the comment witness uses the same
indentation, so the strip reading is the intended and consistent one. No action implied.

## Residual risk and verification gaps

- One canonical runtime only: `python3` = Python 3.14.8 (the counter runs the tool under
  `sys.executable`). The anchor check itself is text processing over `git show` blobs; no second
  interpreter was exercised.
- `c7-after.txt` is worktree-identical to the 13bfba23 blob; HEAD has advanced to `ebc61f47` with
  later wave-1 report commits, but all five files this review reads are byte-identical between
  worktree and the scored tip.
- `freeze-r39.txt` pins the counter (`b92c65f2…`), contract (`fc36841b…`) and comment witness
  (`fc95dc69…`) — all match the worktree — but does **not** pin the drift tool or the anchor entry.
  Their identity across `f920eaf7 → 13bfba23` was verified directly instead (`diff` of `git show`
  output empty; 0 paths differ under `corpus/` and `tools/`).
- Out of scope and not independently re-derived here: `capability_v2`, `live_rows_v2`,
  `named_row_drift`, `drift_kill_v2` internals. The full counter run printed each `PASS`, and the
  four negative witnesses were rejected, but I did not re-implement those four checks.
- The docstring probe is synthetic (a toy entry over the real tool blob); it demonstrates a
  discriminator limit, not a defect in the committed entry.

CONCLUSION: no anchor fails independent resolution; counter detail matches; `anchors_v2` PASS at
13bfba23 is supported. Residual risk is the docstring-parking discriminator gap (LOW-2) and the
non-tip revision string in the receipt (LOW-1).
