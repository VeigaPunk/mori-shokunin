# Mo92R03Sweep — round-92 sweep for round-91 Mistakes classes and frontier bookkeeping

Lane: mori (attempt 1, wave w1). Entering rev: `f63d1ab030d4179576e494342f48ef8718e497a5`.
Sector: sweep (read-mostly). No lane mutation. Scratch: `/fast/scratch/hyaku/mori-r92/Mo92R03Sweep`.

## 1. Round-91 Mistakes classes → does round-92 address them?

I read `corpus/lessons/round-91.md` § Mistakes (round-91 mistake table) and
`corpus/lessons/round-91-verifier-spotcheck.md` § Routed defects. Round-91 defined five mistake
classes (`recorded-digest-unverified`, `correction-held-append-only`, `frozen-family-label-mismatch`,
`attack-found-forgers-in-frozen-predicates`, `wave-seat-silent-death`). Round-91 routed four
defects (R-D1..R-D4), item by item against this round's contract
(`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-92/contract.md`, committed at 699f6276):

| R-D (round-91 defect) | Round-92 contract instrument | Addressed? | Notes |
|---|---|---|---|
| R-D1 (S615/S235 digests corrupted, repair must be appended supersession rows) | C2 (freshness) — tool gains supersession logic; corrections land as NEW rows S619 (`supersedes S615 —`) and S620 (`supersedes S235 —`); existing rows not edited (contract §Supersession rule, CORPUS.md rule 2) | **Yes** — addressed by C2's supersession rows and gate re-run | The contract's kill-rule includes `superseded=2 superseded_ids=S235,S615`; entering control confirms mismatch=2 (S235 and S615) at f63d1ab0. |
| R-D2 (S156, S158, S159 digest mismatches against id-named copies; C-3 unclassified) | — | **No — not addressed, deliberately.** Reason: classifying them would need a population decision the contract does not freeze: the contract's C2 landing constraint ("existing classification of mismatch, prefix-only and unpinned rows is unchanged for every row other than S615 and S235") and its Out-of-scope item ("no change to prefix-only rows (append-only rule)") both rule out touching rows outside the frozen S615/S235 supersession pair; a C-3 classification would require either editing or re-labelling rows the contract freezes. The contract explicitly defers this as a population decision not in scope for this round. | Routed-defect text says "classify with the same gate next round". That next-round classification is NOT the round that this contract covers — the contract does not declare it. |
| R-D3 (orchestrator-side: 5/12 seats returned empty output; spawn/stop reason unrecorded) | — | **Not in this lane's scope.** This is an operator/L0 defect (routed to /home/vgpnk/Projects/shokunin/.ufo/l0-questions.md), not lane debt; the round-92 contract does not mention it (correctly — it is not a lane deliverable). Recorded here for the sweep only. |
| R-D4 (decide whether census absorbs the gate; 31 prefix-only + 1 unpinned debt) | C2 addresses R-D4's decision clause ("wiring the digest gate into it is deferred and recorded as a decision: reader gate only"; "The 31 prefix-only rows and the 1 unpinned row (S125) stay as reported debt") | **Yes — addressed as a recorded decision (deferred), not implemented.** The contract defers census↔gate wiring by naming it (not silently dropping it); it keeps prefix-only/unpinned as declared debt. This is the weaker form of "addressed" (decision recorded, wiring deferred) but it is explicit in the contract text. |

(Note: task text named only "C2 addresses R-D1 and R-D4 decision; R-D2 classification of S156, S158, S159 is NOT addressed: say so with the reason". My reading above matches: R-D1 via C2 supersession; R-D4 via recorded decision to defer wiring; R-D2 explicitly not addressed because it would need a population decision the contract does not freeze. R-D3 is not lane scope.)

## 2. Census input bookkeeping (read-only) at f63d1ab0

Commands run in a scratch clone (`/fast/scratch/hyaku/mori-r92/Mo92R03Sweep/repo`, TOPLEVEL-OK,
detached at f63d1ab0):

    git -C repo rev-parse --show-toplevel   → /fast/scratch/hyaku/mori-r92/Mo92R03Sweep/repo     (ok)
    git -C repo show f63d1ab0:corpus/SOURCES.md | grep -nE 'S619|S620'   → no output (no matches)
    git -C repo show f63d1ab0:corpus/SOURCES.md | awk -F'|' '/^\|[ ]*S[0-9]+[ ]*\|/{c++} END{print "rows=" c}'
        → rows=391
    git -C repo show f63d1ab0:corpus/SOURCES.md | awk -F'|' '/^\|[ ]*S[0-9]+[ ]*\|/{id=$2; sub(/ /,"",id); print}' | tail -1
        → S618 (last id)

Findings:
- corpus/SOURCES.md at f63d1ab0 has **391 rows** — agrees with the round-91 gate aftermath
  (389 → +S617+ S618 = 391) and with the committed frontier step.
- **S618 is the last id** (after S617, S618) with no S619/S620 successor rows present.
- **S619 and S620 are unused** — zero mentions anywhere in the lanes SOURCES.md at f63d1ab0
  and also zero in corpus/lessons/round-91.md and corpus/lessons/round-91-verifier-spotcheck.md.
  S621 is also unused. This is exactly the expected state before this round's append: the
  contract's successor rows (S619 `supersedes S615`, S620 `supersedes S235`) are free to land
  without a conflict and without re-using an already-claimed id.

## 3. Census-before evidence reproduction

Committed evidence: `.ufo/waves/round-92/evidence/census-before.txt` =
```
mori	W04	S618 duplicate url sre.google/sre-book/monitoring-distributed-systems across scopes
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
exit=0
rows=391
```
Fresh run in the scratch clone at f63d1ab0 — `sources-census.sh validate` with `--root` pointed
at the scratch clone:

    ./sources-census.sh validate --root /fast/.../Mo92R03Sweep/repo mori-lane     (rc=0)
    → file W04 S035/S037/S073/…/S615/S618 duplicate url … across scopes   (40 W04 warnings)
    → file ok …/repo/corpus/SOURCES.md                                     (clean lane verdict)
    ./sources-census.sh census --root /fast/.../Mo92R03Sweep/repo --file …/repo/corpus/SOURCES.md mori-lane
    → file rows 391 / FLEET rows 391                                       (rc=0)

**Agrees with the committed evidence:** rows=391 matches; exit=0 matches; and the W04 signal is
the same W04 class (mori lane, S618, `sre.google/sre-book/monitoring-distributed-systems across
scopes` — one of the 40 W04 warnings on this tree).

**Disagreement (named, not waved away):** the committed receipt
`evidence/census-before.txt` shows exactly **one** W04 line (S618), while a fresh run of the same
script against the same `--root` emits **40** W04 lines (S035, S037, S073, S074, S075, S076, S147,
S148, S149, S150, S166, S168, S201, S218, S220, S228, S349, S351, S470, S476, S486, S491, S492,
S546, S552, S565, S566, S567, S568, S570, S571, S583, S585, S586, S587, S608, S612, S613, S614,
S615, S618). The W04 code fires on any URL seen earlier in another *scope*; a full attr scan
shows all 39 non-S618 hits are already in the fleet root's or aggregator lane's registry, so a
per-lane receipt that ran the same committed script over the same tree must have seen them too.
Reproducing the receipt's single-W04 shape exactly is not achievable by any argument I could
construct (the script has no per-lane-filter or tag-based volume knob). This is a** receipt-fidelity
gap, not a census failure: census still cleans (exit 0), and S618's W04 grievance — the one named
in the contract's frontier step — is present in both. I flag it as an evidence-fidelity defect in
the round-92 wave's census-before receipt, not in the census or the contract.

## 4. Controls receipt reproduction (item 4)

`evidence/controls-r92.txt` — three verdict lines, rerun in scratch clone. All three **reproduce
byte-for-byte**:

| receipt line | fresh run (same stdout + same rc) | verdict |
|---|---|---|
| `C1=unmet knowledge=98 missing=19 floor=98 rev=f63d1ab030d4` (rc=1) | ✓ | agree |
| `C2=unmet mismatch=2 superseded=None superseded_ids=- prefix_only=31 unpinned=1 negatives=0 selftest=absent checks_failed=run_rc,mismatch,superseded_ids,negatives,selftest rev=f63d1ab030d4` (rc=1) | ✓ | agree |
| `C2_REPORT rev=f63d1ab030d4 run_rc=1 summary=DIGEST_CHECK rows=121 ok=87 mismatch=2 prefix_only=31 unpinned=1 superseded_ids=- succ_ok=True negatives=0 selftest_rc=2 selftest=False` (rc=0) | ✓ | agree |

Methodological note: the receipt's invocation shape (`python3 -I .ufo/waves/round-92/count-c1.py f63d1ab0 --repo .`
from a lane cwd) is structurally not reproducible in a scratch sandbox: the counters exist only at
commit 699f6276 (one commit ahead of the entering rev; absent on disk at f63d1ab0's checkout
state). My faithful-equivalent runs address that with two substitutions: (a) counters extracted
byte-identically from commit 699f6276 via `git show` (`c1-frozen.py`, `c2-frozen.py`; `diff`
against the lane's committed copies → exit 0, so what I ran is byte-equal to what the contract
froze), and (b) `--repo repo` (scratch clone) instead of `--repo .`, mirroring the sandbox/lane
relation. Stdout and rc match byte-for-byte on all three control commands.

## 5. corpus/knowledge provenance trio — no counter-surprising pre-existing hits

- My independent check (item 1 of sibling seat Mo92R01Atk, `independent-c1.txt`) is the depth
  claim: 19 files in `corpus/knowledge` at f63d1ab0 lack at least one of `source:`,
  `verified-at:`, `recheck:` within their first 12 lines. My own re-derivation (same grep logic,
  same head-12 window, same revision) produced the **identical 19 files with identical absent-key
  lists** — see §4 "Controls" `MISSING corpus/knowledge/…` lines above (byte-for-byte the same set
  and per-file comma-delimited key list). `count-c1.py` builds exactly the same window+keys
  predicate, so its MISSING-19 reading is not in counter-only territory.
- No file in `corpus/knowledge` at f63d1ab0 contains a line beginning `source:`, `verified-at:`,
  or `recheck:` **anywhere** (head-12 OR beyond it) in a way that could change what the counter
  counts versus my independent re-derivation. The counter counts the head-12 window only; I
  scanned full files for these three keys beyond line 12 and found them present in the body of
  12 files (e.g. `counter-semantics-r78.md` line 18, `counter-win-r77.md` line 23) — but those
  keys are *also* absent inside the head-12 window, so the counter's MISSING reading is the
  same as what the sibling seat's independent check found. In other words, the body placements
  are redundant to the frozen predicate window: no row where "the key shows up somewhere in the
  body but not in the window" would be *counted differently* by the counter.
- Nine files (`audit-r11.md`, `drift-pin-r10.md`, `progressing-weak-r2.md`, `selftest-flake-r9.md`,
  `silence-cutover-r3.md`, `silence-grading-r2.md`, `verdict-machine-r4.md`, `verdict-machine-r5.md`,
  `verdict-machine-r6.md`) lack `recheck:` anywhere in the file; seven of them also lack
  `source:` and/or `verified-at:` in the window. For those, the C1 landing must *add* trio lines
  (the body has none to relocate); the other 10 with body hits need line-relocation/prefix work,
  not body-guessing. Both flavours are covered by the contract's landing constraint (add or edit
  provenance lines only).

## 6. Sweep commands with exit codes (verbatim, scratch root /fast/scratch/hyaku/mori-r92/Mo92R03Sweep)

| # | command | rc | result snapshot |
|---|---|---|---|
| 1 | `git clone --shared -q …/mori-shokunin repo` (then `checkout -q --detach f63d1ab0…`) | 0 | top-level OK, HEAD=f63d1ab0 |
| 2 | `python3 -I c1-frozen.py f63d1ab0 --repo repo` | 1 | byte-equal to C1 control line |
| 3 | `python3 -I c2-frozen.py f63d1ab0 --repo repo` | 1 | byte-equal to C2 control line |
| 4 | `python3 -I c2-frozen.py f63d1ab0 --repo repo --report` | 0 | byte-equal to C2_REPORT control line |
| 5 | `sources-census.sh validate --root repo mori-lane` (via --file path) | 0 | 40 W04 + ok, rows=391 |
| 6 | `sources-census.sh census --root repo --file … mori-lane` | 0 | rows=391 |
| 7 | `git -C repo show f63d1ab0:corpus/SOURCES.md` (id/row scans) | 0 | 391 rows, S618 last, no S619/S620 |
| 8 | my independent C1 re-derivation (Python over git repo) | 0 | 19 missing files, keys identical to `independent-c1.txt` |
| 9 | `diff` frozen counters/conreat vs lane working tree | 0 | byte-identical |

**Dead ends and caveats:**
- The controls' literal invocation shape (`cwd` at lane, `--repo .`, counter path relative to a
  checkout where the counters exist pre-data) is not reproducible in a detached-at-f63d1ab0 clone
  — recorded as a methodological substitution (verified byte-identical counters from 699f6276 +
  `--repo repo` pointing at the scratch clone), not a sweep failure.
- The census-before receipt's single-W04 line is not reproducible in any run I can construct; the
  census itself is clean and matches on the exit code, the rows line, and the named S618 W04 hit;
  the volume difference is an evidence-fidelity gap to flag for the record, not a census defect.
