# W2 RevC4Anchors — independent re-derivation of P-C4's `anchors` check at f725f307

Seat: wave-2 falsification, anchor check. Everything below was re-run by this seat; nothing is
taken from wave-1 reports. Lane repo untouched; scratch at
`.ufo/waves/round-38/scratch/RevC4Anchors/` (tool bytes extracted there). No tools installed
(git/python3/grep already present).

## Verdict: PASS — no defect found

Every `anchor:` line in `corpus/knowledge/source-drift-content-anchor-r38.md` resolves byte-exactly
in `tools/mori-source-drift.py` at `f725f3076972e6e70595b5ac8279be524a111ff8`, in executable code,
each at exactly one site. The counter's `check anchors PASS (anchors=3 missing=[])` matches my
independent resolution, and its extraction rule neither hides nor invents an anchor. The token
witness is rejected by the anchors arm itself (0 anchor lines), proven by direct projection.

## 1. Anchor enumeration (my own)

`grep 'anchor:' corpus/knowledge/source-drift-content-anchor-r38.md` → lines starting `anchor:`
are exactly three, entry lines 26–28:

| # | entry line | anchor string |
|---|---|---|
| 1 | 26 | `FETCH_MAX_BYTES = 4 * 1024 * 1024` |
| 2 | 27 | `if not _public_redirect_target(final):` |
| 3 | 28 | `return "drifted"` |

Line 22 of the entry contains `` `anchor:` `` mid-sentence ("Every line … beginning `anchor:` …")
but does not start with it; it is prose, not a fourth anchor. Counter extraction (below) agrees.

## 2. Byte-exact resolution at the pinned rev (my own `grep -F`)

`git show f725f307…:tools/mori-source-drift.py` (466 lines) saved to scratch; fixed-string search:

| # | anchor | tool line | hits | line content |
|---|---|---|---|---|
| 1 | `FETCH_MAX_BYTES = 4 * 1024 * 1024` | 54 | 1 | `FETCH_MAX_BYTES = 4 * 1024 * 1024  # bodies larger than this cannot be classified; read is capped at +1` |
| 2 | `if not _public_redirect_target(final):` | 158 | 1 | `                    if not _public_redirect_target(final):` |
| 3 | `return "drifted"` | 208 | 1 | `    return "drifted"` |

3/3 resolve. Re-derived independently in Python against the counter's own `show()`:
anchor→lines `54`, `158`, `208`; occurrence counts `1/1/1`.

## 3. Executable vs comment-only (per anchor)

1. **Line 54 — executable.** Module-level constant in the constants block (after
   `FETCH_TIMEOUT_S`/`FETCH_TRIES`, tool lines 51–53). Used at lines 163–164
   (`resp.read(FETCH_MAX_BYTES + 1)` and the over-cap `unavailable` branch). Load-bearing, not
   decorative.
2. **Line 158 — executable.** Live conditional inside `fetch()`'s redirect branch
   (`if final != url:` → line 158 refuses non-public redirect targets). Callee
   `_public_redirect_target` is defined at line 113 — not a dangling reference, not dead code.
3. **Line 208 — executable.** Sole drift branch of `classify()` (lines 202–208): fresh → excerpt →
   drifted. Exactly one occurrence in the file, so no comment/dead duplicate exists. Independent
   liveness proof: the counter's `drift_kill` arm replaces this exact string with
   `return "excerpt"` and the selftest then FAILs naming S103
   (`want=[('S103', 'drifted')]` vs `got=[('S103', 'excerpt')]` in the counter output below) —
   the anchor string is the code doing the work.

No anchor is comment-only or dead-code-only.

## 4. Counter's `check anchors` detail vs my resolution

Run: `python3 .ufo/waves/round-38/count-c4.py f725f3076972e6e70595b5ac8279be524a111ff8` → exit 0,
`C4=met`. Relevant output (verbatim):

```
negative witness-token-entry        rejected
negative witness-dangling-row       rejected
negative witness-summary-only-live  rejected
check anchors          PASS (anchors=3 missing=[])
check capability       PASS (paths=[…] missing=[])
check live_rows        PASS (named=10 summary_drifted=10 unknown=[])
check named_row_drift  PASS (exit=0 row_states=('PASS', ''))
check drift_kill       PASS (exit=1 row_states=('FAIL', "got=[…('S103', 'excerpt')…] want=[…('S103', 'drifted')…]"))
```

- `anchors=3` matches my enumeration of exactly 3 `anchor:` lines; `missing=[]` matches my
  3/3 byte-exact resolution. No hiding: the extraction rule (count-c4.py:137–143) takes every line
  whose stripped form starts with `anchor:` — it cannot skip one, and over-extraction would have
  printed 4. `check_anchors` (count-c4.py:169–173) requires `len(anchors) >= 3` AND empty missing,
  and its detail prints the full count and missing list — nothing excluded silently.
- Matching is substring (`a not in tool_text`, count-c4.py:171), so a comment-embedded match would
  in principle pass — but §2/§3 close that for this rev: each anchor has exactly one occurrence and
  I read its context. (Residual, disclosed by the entry's own "Limits" section.)

## 5. Witness rejection is due to the anchors arm (direct projection)

`fixtures/witness-token-entry.md` carries the r37 tokens (`huge_cap`, `redirect_private_refused`,
`1caa242`) and zero `anchor:` lines. Projected onto the real bytes at the pinned rev via the
counter's own functions:

```
real entry anchors:    ['FETCH_MAX_BYTES = 4 * 1024 * 1024',
                        'if not _public_redirect_target(final):', 'return "drifted"']
real check_anchors:    (True, 'anchors=3 missing=[]')
witness anchors:       []
witness check_anchors: (False, 'anchors=0 missing=[]')
```

So the token entry fails the anchors check itself (0 < 3), not incidentally via another check —
this is the content-vs-token discrimination C1 claims.

## Findings by severity

- CRITICAL: none.
- HIGH: none.
- MEDIUM: none.
- LOW: none.
- Note (not a defect): the anchors check is substring-based and cannot by itself distinguish
  executable from comment-only occurrences; closed for this rev by manual context reads and
  single-occurrence counts (§3), and the `drift_kill` arm independently proves anchor 3 is live.

## Residual risk / verification gaps

- Verified at the single pinned rev only; a future tool edit can stale an anchor by design (the
  entry's `recheck:` line covers that cadence).
- capability/live_rows/named_row_drift internals were not re-audited (other seats' scope); the
  counter's printed details for them were recorded, not re-derived, except the drift_kill S103
  detail used as anchor-3 liveness evidence.
