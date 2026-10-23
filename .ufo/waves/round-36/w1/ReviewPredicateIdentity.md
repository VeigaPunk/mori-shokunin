measured 2026-10-23T12:04:45Z

# ReviewPredicateIdentity — mori round 36 wave 1 (QUALITY 97/§9 predicate identity)

Scope: P-C1 / P-C2 byte identity across contract, counter first line, c0 receipts; clause → enforcing-line map; weaker-enforcement check. No code in the lane was edited.

## Findings

None. No defect found. All checks below passed; every clause of P-C1 and P-C2 has an enforcing line of at least the stated strength.

VERDICT: no defect found

## 1. Byte identity

Canonical sentences: contract.md:21 (P-C1), contract.md:23 (P-C2).

- count-c1.py PREDICATE (lines 50-56) == contract P-C1: exact True, whitespace-collapsed True (script b968e2d1…, see §5).
- count-c2.py PREDICATE (lines 32-38) == contract P-C2: exact True, collapsed True.
- Both counters print the predicate as their first stdout line: count-c1.py:669 `print(PREDICATE)` precedes all other output; count-c2.py:656 same. Empirically confirmed by smoke runs (failing tool, seed 1):
  - `count-c1.py 6bd57097 --tool /bin/false --seed 1` first line = P-C1 sentence verbatim (exit 1, C1=unmet).
  - `count-c2.py 6bd57097 --tool /bin/false --seed 1` first line = P-C2 sentence verbatim.
- c0 receipts: 56 predicate lines scanned (P-C1=17 in CtlK*.md, P-C2=39 in CtlJ*.md, 25 files) — all byte-identical to the contract sentence including the v1-met controls CtlK13.md:34 and CtlJ11.md:30/47/77.
- Frozen bytes pinned: sha256sum matches evidence/freeze-v2.txt (contract.md dbd3f6d7…, count-c1.py 86dd3b7a…, count-c2.py c7edaacf…; lines 2-4).

Note: `echo` `head` on the C2 smoke run produced a Broken-pipe exit-2 (stream closed by the pipe) — a harness artifact, not a counter path; full-capture runs are unaffected.

## 2. P-C1 clause map (contract.md:21)

| Clause | Enforcing line(s) in count-c1.py |
|---|---|
| at revision R | rev arg + `rev-parse --verify` 649-677; tool from `git show <rev>:tools/mori-source-drift.py` 679-689; worktree corpus must equal R (git diff --quiet rev -- corpus; no untracked under corpus/) 574-580 |
| 40-row blind fixture drawn at run time | N_ROWS=40 (71), PER_STATE=8 (72), build_fixture 378-526; seed from os.urandom 699-701 |
| classifies every row exactly as the counter's hidden truth | blind_arm: per-row compare 298-312 flags missing/dup/extra rows; passed = not mismatches and rc in (0,1) 555 |
| agrees with independent live oracle on every row the oracle classified | real_arm 567-640; oracle_classify 235-268; only oracle-unfetchable rows excluded (excluded list), matching contract.md:53-57; unavailable-on-fetched re-probe 609-619 matches contract.md:55-57 |
| at least 10 oracle-fetched rows | `fetched >= 10` in passed (630), shortfall detail 632-633 |
| at least one oracle-fresh and one oracle-drifted | `fresh >= 1 and drifted >= 1` (630), detail 634-637 |

## 3. P-C2 clause map (contract.md:23)

| Clause | Enforcing line(s) in count-c2.py |
|---|---|
| at revision R | rev resolution 648-668; tool from `git show <rev>:tools/mori-sources-appendonly.py` 678-686; real arm rev 6bd57097 (44, 629) |
| 24 sandbox histories drawn at run time | N_SANDBOX=24 (46), blind_arm loop 593-621; seed 657-658 |
| prints exactly hidden truth for ids, deleted, superseded, round_changed on each history | truth_from_states 166-225 mirrors contract definitions (endpoint ids 197-198, deleted 199, superseded 200-201, round_changed 202-204, changed-back 205-217); same_lists 517-522 compares all four lists + violations; expected exit 603; met only when 24/24 722 |
| lane's own history (rev 6bd57097, base f10a320d) prints exactly the independent oracle | real_arm 624-643; oracle() independent git walk 527-585; same_lists 632 |
| which lists at least one id | `bool(expected["ids"])` 632 |

Draw guarantees backing the sentence's coverage: ≥12 deletions and ≥12 changed-back histories and ≥1 supersede enforced at 703-706 (exit 2 if below minimum); deletion/changed-back assigned by index parity 386-387.

## 4. Weaker-enforcement review (none found)

- C1: the real arm requires `fetched >= 10`, `fresh >= 1`, `drifted >= 1` conjunctively with zero mismatches (630); coverage minima cannot be satisfied by excluded rows because excluded rows are never counted as fetched. Blind arm cannot pass with any row missing/duplicated (298-312).
- C2: `same_lists` compares violations + all four id lists exactly (517-522); summary regex requires all five fields, exactly one summary line (53-55, 498-514); a history passes only with both correct lists and expected exit (603-615).
- Nothing weaker than the sentence is tested: the only relaxations (C1 oracle-excluded rows; C1 unavailable re-probe) are exactly the contract's own exclusions (contract.md:53-57). Neither counter checks output beyond the sentence's object (C1 per-row states; C2 summary lists), and exit-code strictness is equal to or stronger than the interface (contract.md:46-47, 76-77).
- No clause lacks an enforcing line.

## 5. Verification gaps / residual risk

- Not run: full scored counter runs against the live tool (tools not yet landed at the reviewed tip; real arm would touch network hosts). The predicate-identity object of this review does not depend on scoring.
- C2 real-arm exit code is not checked (632-643 compares content only); exit semantics are outside the frozen sentence, so this is not a clause gap.
- Receipts scanned are the c0 files present at review time; any receipt generated later inherits the same counter path.

Scratch code: /fast/scratch/hyaku/mori-r36/ReviewPredicateIdentity/check_identity.py, sha256 b968e2d12028289d29d94fa5aff216c2981f8a602429ff7e5c11bef90aaf2c60. No tools installed (none needed).
