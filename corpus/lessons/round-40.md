# Round 40 — 2026-10-24 (L1 mori-r40, attempt 1 resumed)

## Gate

| source | decision | located quote |
|---|---|---|
| S229 — Python execution model, Naming and binding `https://docs.python.org/3/reference/executionmodel.html#naming-and-binding`, opened 2026-10-24 (copy `corpus/evidence/sources-r40/S229.src`) | **admitted** (mined) | `S229.src` §4.2.2 Resolution of names: "When a name is used in a code block, it is resolved using the nearest enclosing scope." (15 words) |

Rejected: none new. Search log: bounded search for the name-binding rule grounding
the scope-aware timeout fold — identified 1 (Python execution model §4.2), opened 1,
included 1 as S229, excluded 0; stop rationale: Python's own reference documentation
is the primary source for Python scoping semantics (tier A for this scope).
Registry rows before → after: 228 → 229 (+S229); no existing row's
`status`/`recheck`/`used-by` changed in place. Census: start exit 0
(`evidence/census-start.txt`), end exit 0 (`evidence/census-end.txt`); S229
introduces no new warning class (the standing 16 W04 duplicate-URL rows are
pre-existing fleet debt, routed by the r39 closure to the owning lane).

## Mistakes

| # | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M23 | inherited-unverified-freeze (a prior launch froze instruments in prose but died before persisting the freeze receipt or any receipt) | the inherited working tree held `contract.md` claiming pins in `evidence/freeze-r40.txt`, but that file did not exist; no before/after receipt existed either — only `census-start.txt` | none — no criterion required a freeze receipt to be verified present before integration; the r39 finding-9 discipline (receipts name the measured rev) extends to freeze receipts now | the resuming L1 re-verified every inherited instrument byte-by-byte (gate v3 diff audit, conform v3 selftest, parity, survivor regeneration), completed the unfinished work (gate selftest arms 12→15; dag-r redesign), and persisted `evidence/freeze-r40.txt` with sha256 pins plus an honest note that it was written at integration; before-controls all run bytes extracted via `git show bb1f2457:<path>`, so entering-state measurement is uncontaminated. Shown able to fail: any post-freeze instrument edit would mismatch the pinned sha256 set |
| M24 | number-drift (a parenthetical arithmetic inside the frozen predicate mis-predicted the measured value) | the contract and the P-C11 sentence's parenthetical say "S226 joins superseded_as_of (19 ids) at the landed tip"; the measured lane line at T1 lists **34** as-of ids — the eligible-set extension admits every never-edited superseded row present at R (16 rows: S226 plus 15 earlier), which the parenthetical arithmetic did not count | claim-sizing lesson (brief §9: declare after-states as one command over committed bytes; never freeze a counted prediction that the counter does not enumerate) — applied one round late | the SCORECARD after-cell and this lesson record the measured 34 and name the 16 never-edited ids as a class; the predicate's semantic sentence (the real counter) is unchanged and verified; the parenthetical is marked corrected-by-measurement |

Also recorded (honest-stop class, not a mistake): the v2 red for the re-add
*changed event itself* is invisible at the frozen bytes — on the first dag-r design
(delete+re-add of an un-superseded row) v2's extra changed event altered no printed
list, because `round_changed` is a set and the deletion already contributed the id.
The fixture was redesigned so the re-added row is superseded: v2's edit-bounded
eligible set then visibly omits it (`evidence/c11-red-readd.txt` prints an empty
timing line where v3 prints `as_of=[S008]`), and the gate selftest's hand-written
dag-r expectation pins the no-changed-event semantics able-to-fail.

## Round shape and debts

Routed items discharged: closure routed defects 1 (drain-shape re-claim via the
decoy-communicate control + r39-erratum wording correction), 2 (name-not-value
survivors + decoy drain + per-counter comm_violations + own-table conjunct), 3
(P-C11 predicate/code single source; the "first parent's state" words are now what
the gate computes; the unreachable "18 ids + S226" prose is corrected by M24), 4
(S227 17-word label corrected in `corpus/lessons/round-39-erratum.md`). Finding 1
(P-C7 prose) narrowed reading recorded in the same erratum. Debt (f)
(SIGTERM/grace tradeoff) stays OPEN/operator-owned — not worked this round.
Standing W04 duplicate-URL census debt (16 rows) remains fleet-owned per the r39
closure's routing.

Inherited state: the 01:32 launch's uncommitted outputs (contract, conform v3 draft
with two failing selftest arms, gate v3 partial — merge fall-through fixed but
re-add branch and selftest arms missing, fixtures, scratch drafts) were re-verified
and completed; the three root strays (`bypass-none.py`, `bypass-wait.py`,
`count-c1-r38.py`, mtime 01:27) were deleted after inspection: `count-c1-r38.py`
was a byte-size-exact extract of the committed `.ufo/waves/round-38/count-c1.py`
(48,680 bytes, recoverable), but the two bypass files existed in **no commit** —
their exact bytes are unrecoverable; only their class recipes remain committed
(`.ufo/waves/round-39/fixtures/make-m19-bypass.py` + the committed r38 counter
bytes). This round neither needed nor regenerated them (C1's controls use the
round-39 checker bytes and the new survivor set); the loss is recorded here as the
honest disposition.
