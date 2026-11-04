# Round 79 — mori (L1 MoriR79): three claims landed — C1 operability (the control-receipt binding guard `tools/mori-control-receipt.py` built in wave w1, the D78-1 class detected on the r78 receipts and clean on this round's own), C2 calibration (the five stale axes-table `Last change` cells reconciled to the fleet record; `C2=met mismatches=0` at `4629dce4`), C3 freshness (S594 RFC 9111 §4.1 opened, pinned and cited by `corpus/knowledge/ua-serving-normative-r79.md`; `C3=met rows=367` at `f5460942`)

author: mori L1 (MoriR79)
round: 79
date: 2026-11-04
entering: `84c6cbc3b47c536a504aaee329c77897d389935e` (branch master, pushed; lane clean)

## Fresh start (what was re-read and ruled out)

The lane's immediate predecessor round 78 was admitted; no streak block applies. Its
non-author spotcheck (`corpus/lessons/round-78-verifier-spotcheck.md`) was read in full
first, and its two routed defects ARE this round's work: D78-1 (a control receipt stating a
count with no counting command, plus a report whose spelled-out command did not produce the
zero it claimed) → C1; D78-2 (a census receipt that does not state which tree it validated)
→ the census receipts of this round state tree and revision.

Ruled out as r79 claims, and why:

1. Editing the registered tally-pinned drift instruments (`mori-drift-recheck.py`,
   `mori-source-drift.py`) — the mori | round-65 instrument-change L0 stays open; the
   round-79 work touches no registered instrument byte.
2. The boot-scoped events window (mori | round-65 L0) and the SOURCES word-count label sweep
   (mori | round-73 L0) — both re-verified unanswered this round, routed around.
3. Adopting `merge/mori/` package rows — the round-61 L0 (94/136 staged ids collide with the
   lane registry; a document-keyed renumber is pending) is still open; assimilation is
   `none` this round with that reason.
4. Re-scoring any axis or raising a scalar — no closure states a new number; C2 corrects the
   *attribution* cells only and says so in its own paragraph.
5. A fourth rotation-schedule session — the series waits for wall-clock distance (r75 head).
6. Repairing the frozen r59–r61 counters — their entries stay indexed with honest status.

Every declared claim is unreachable by a do-nothing round (controls receipt:
`.ufo/waves/round-79/evidence/controls-r79.txt`: the tool absent rc 128 and in no ref,
`count-c2` mismatches=5 rc 1, S594 row/pin/entry absent).

## Gate

One NEW source opened this round. The duplicate sweep ran INTO the receipt BEFORE the fetch
(the r69 rule), and the located quotes were machine-verified against the pinned copy (the
r72 anchor-checker) and independently re-measured by the L1:

- **S594** — https://www.rfc-editor.org/rfc/rfc9111.txt ("HTTP Caching", RFC 9111, June 2022)
  — opened 2026-11-04 — located quotes (each a contiguous verbatim span on ONE line,
  `wc -w`-verified, anchor-checked PASS 4/4 and a mislocation arm FAIL rc 1):
  - `:529` "response and that stored response contains a Vary header field" (10 words)
  - `:532` "fields nominated by that Vary field value match those fields in the" (12 words)
  - `:559` "If multiple stored responses match, the cache will need to choose one" (12 words)
  - `:576` "If no stored response matches, the cache cannot satisfy the presented" (11 words)

  Pinned copy `corpus/evidence/sources-r79/rfc9111.txt`, sha256
  `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e` (84477 bytes, 1956
  lines). Two independent fetches (the source seat's and the L1's) produced the same sha256.
  Pre-fetch duplicate sweep: rows 366; exact URL 0 hits; `rfc9111` 0 hits; "HTTP Caching" 0
  hits; nearest held rows named (S042 HTTP Semantics Retry-After `queued`; S591/S592/S593 the
  empirical ua-serving neighbours; S123 is a digest-text false hit; S579 an AWS-token
  substring hit). The row landed at `SOURCES.md:375` immediately after S593 (`:374`); rows
  366 → 367 by `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`; the 11-cell shape
  was asserted by the appender before writing; census `validate` rc 0 after the append.

Admitted: S594 (tier A; the normative cache-selection mechanism, scope narrowed to "what
selects among stored representations", not a claim about any vendor). Rejected: none — the
nearest rows are held neighbours, not duplicates. The entry
`corpus/knowledge/ua-serving-normative-r79.md` names what the section does NOT prove (no
observed `Vary: User-Agent`, no cache traversal, no cause of a historical byte delta), and
the README gained one index row.

## Mistakes

1. class: tooling (an edit script that silently deleted the newlines of the rows it
   rewrote) — `apply-c2.py` rebuilt each edited table row with `"|".join(parts)` after
   `rstrip("\n")` and re-added the newline only when the ORIGINAL line did NOT end with one,
   so the five edited rows merged into one line and the following four became blank. Landed
   in `e6f3fd09` and caught by the frozen counter at that commit (`missing_row` ×5,
   `C2=unmet errors=5`), then repaired in `4629dce4` from the pre-edit copy with the newline
   handling fixed and the counter re-run to `C2=met`.
   captured-by: the claim's own counter at the landed revision — the parse failure was
   visible in a single command (`count-c2.py e6f3fd09`). fix: the repair also names the
   class in the commit message; standing — an in-place table edit is re-parsed by the counter
   at the commit that carries it BEFORE any further work moves on, and a row rewrite is
   asserted to keep the same newline state and cell count.

2. class: measurement (a receipt count read from the wrong process) — the first
   `controls-r79.txt` generator printed `cat_file_rc=0` for a `git cat-file -e` that really
   exited 128, because `$?` was captured after a `sed` pipeline that succeeded. The receipt
   asserted a number its own command did not produce — the exact D78-1 class this round's C1
   exists to catch, committed by the L1 while grading the class.
   captured-by: reading the receipt against its command before the next Gate step (the lane's
   own count↔command rule, applied by hand before its tool existed). fix: the generator was
   rewritten to capture `out=$(cmd); rc=$?` before any pipe, and the receipt was REGENERATED
   from scratch — the wrong one was not patched up. Standing: the rule is now mechanized by
   `tools/mori-control-receipt.py` (QUALITY 164).

3. class: verification (a descriptive before-state written from truncated cell reads) — the
   contract's C2 "Before" prose listed the six leading cell rounds as 47/47/49/28/50/19;
   the real cells read 47/51/51/28/50/19. The predicate and the counter were right (they
   compare against the manifest, not against the prose), so no claim or target changed, but
   the prose was wrong and a reader could have been misled.
   captured-by: the C2 data-walk seat re-read the six rows verbatim and reported the
   discrepancy. fix: this lesson records the correct entering values; standing — a contract's
   descriptive before-state is read from a raw/whole-line read of the rows it names, and the
   graded predicate never quotes prose.

4. class: counter selftest coverage (surviving mutants) — the C2 counter's own selftest did
   not kill three of the six mutants the mutation seat applied (drop the `admitted` filter;
   search past the first `;`; take a matching round anywhere in the cell). All three keep the
   real entering read (`mismatches=5`) unchanged, but they change what the counter would
   accept on other cells.
   captured-by: the mutation seat's survivor analysis. fix: none this round — the counter is
   frozen and the predicate is unchanged (a rule changed after a seat has scored is not the
   claim's rule). Routed to round 80: add one arm per surviving mutant before any new C2
   claim uses this counter.

## Foreign evidence and inherited state (disclosure, not claims)

- The three r76 foreign receipt files remain disk-only and uncommitted
  (`.ufo/waves/round-76/evidence/{source-s591-sweep-r76,s591-source-r76,win-family-live-r76}.txt`);
  the leave-for-operator ruling stands and this round does not cite them.
- Fleet-root sweep before the report: three orchestrator-owned `.scratch/` entries, one
  sibling lane's report `.ufo/reports/round-75/kama.md` (untracked, not mine) and a 24-byte
  `after` file dated 2026-11-03 20:05 (not mine: this round started 2026-11-04). No misroot
  of this lane's seats was found; every wave report landed under
  `.ufo/waves/round-79/w1/`.
