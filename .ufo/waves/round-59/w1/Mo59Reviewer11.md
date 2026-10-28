# Mo59Reviewer11 — C2 real-scan replay

Seat: re-run the pinned `tools/mori-settlement-scan.py` over the five committed
r54–r58 `.ufo` results files (expect OK/exit 0) and the r53 drift file (expect
FAIL/exit 1) with exact output. Result: **no counterexample** — replay
confirms the frozen scan/drift arms; one non-exploitable counter-arm weakness
noted (I1).

## Method (bounded)

- Lane `/home/vgpnk/Projects/shokunin/mori-shokunin`, HEAD `8ff344ff18924c1ea63d46c3b3969f9fea05bc51`
  (entering `2b9f0397` is its grandparent; freeze `60b3a76a` between). Working
  tree: 4 untracked wave entries (`.ufo/waves/round-59/w1/`,
  `corpus/evidence/sources-r59/`, dispatch receipts) — data not yet committed.
- Tool materialized via `git -C <lane> show HEAD:tools/mori-settlement-scan.py`
  into seat scratch `/fast/scratch/hyaku/mori-r59/Mo59Reviewer11/`; sha256
  `4c04bf2170b0484192dd157ee04851e8243e030c54046c5e8806d46eea5ac9a9` = PIN in
  `count-c2.py:53`. Tool absent at entering rev (`cat-file` → fatal).
- The six `.ufo` files materialized via `git show HEAD:…` (all committed at
  HEAD; `ls-tree HEAD` lists all six paths). File shas:
  r53 `0d644e0f…584260`, r54 `ea48a0cc…59335f`, r55 `2e5b0a0f…d9763b`,
  r56 `19536201…d761`, r57 `29e7a35d…79eb1`, r58 `a57b660d…61fc`.
- Ran the materialized pinned bytes directly (not the counter's harness) on
  read-only inputs; mutations written only under scratch. All `python3` runs
  on the pinned bytes, CPython on this host.

## Replay results — contract-expected

| arm | command | exit | verdict/output |
|---|---|---|---|
| selftest | `tool.py --selftest --scratch <S>` | 0 | `SETSCAN_SELFTEST pass=10 fail=0` (exact, sole stdout line) |
| real scan | `tool.py real/w1-results-r{54,55,56,57,58}.json` | **0** | `SETTLEMENT_SCAN_OK`; `files` = 5 entries, `failures` = [] |
| drift | `tool.py real/w1-results-r53.json` | **1** | `SETTLEMENT_SCAN_FAIL`; `files` = 1 summary, `failures` = 1 entry |

Per-file scan summaries (all `members == seats`, `duplicates=[]`,
`empty_output=0`, `notes_nonnull=0`):

- r54: seats=74 members=74; roles: connector 2, critic 18, executor 15,
  mutation-tester 2, revenger 1, reviewer 19, scout 4, scribe 9, sentinel 3,
  simplifier 1
- r55: seats=64 members=64; roles: connector 2, critic 26, executor 4,
  mutation-tester 6, revenger 2, reviewer 14, scout 2, scribe 4, sentinel 2,
  simplifier 2
- r56: seats=64 members=64; roles: connector 2, critic 10, executor 20,
  mutation-tester 6, revenger 1, reviewer 9, scout 4, scribe 7, sentinel 4,
  simplifier 1
- r57: seats=64 members=64; roles: connector 2, critic 10, executor 6,
  mutation-tester 8, revenger 1, reviewer 22, scout 4, scribe 8, sentinel 2,
  simplifier 1
- r58: seats=64 members=64; roles: connector 2, critic 10, executor 8,
  mutation-tester 8, revenger 1, reviewer 22, scout 4, scribe 6, sentinel 2,
  simplifier 1

r53 failure detail: `reasons` = **67 entries, all
`member[i]:extra_keys=report_file`** (i = 0..66, one per member; file has
seats=67, members=67) — exactly the "report_file extra keys — schema drift"
the contract names, and no other reason kind.

Output is one `mori-settlement-scan-v1` JSON line (`sort_keys=True`), stable.

## Discrimination probes (adversarial, mutated copies under scratch)

- r53 with `report_file` deleted from all 67 members → `SETTLEMENT_SCAN_OK`,
  exit 0, zero failures ⇒ the r53 FAIL is caused solely by the extra key.
- r54 + `report_file` on member[0] → exit 1, FAIL,
  `member[0]:extra_keys=report_file` only.
- r54 with `seats` +1 → exit 1, FAIL, `seats_mismatch`.
- zero files → exit 1, `{"verdict": "SETTLEMENT_SCAN_FAIL", files:[], failures:[]}`.
- nonexistent path → exit 1, FAIL `unreadable`.

Exit codes observed: 0 iff every input file validates with zero failures;
1 otherwise (including zero-arg and unreadable). No path emits exit 2 (the
docstring's "usage/setup exit 2" is unreachable — `main` filters `--*` args
and `scan()` never returns 2); cosmetic only, no predicate depends on it.

## Counter cross-check

`count-c2.py HEAD --scratch <S>` → exit 1,
`C2=unmet selftest=ok scan=ok drift=ok trees=ok entry=bad rows=bad pins=bad
tree=bad claims=0 files=0 rev=HEAD failed=copy_absent:…,entry_absent,tree` —
selftest/scan/drift/trees arms green mid-wave; `copy_absent`/`entry_absent`
consistent with `corpus/evidence/sources-r59/` still untracked.
`count-c2.py 2b9f0397` → exit 1, `C2=unmet … failed=…,tool_absent,…` — the
before-arm met-proof holds (tool absent at entering rev).

## Findings

**No counterexample.** The pinned tool reproduces the frozen scan/drift arms
on the committed artifacts: 5×OK/exit 0 with members==seats everywhere, r53
FAIL/exit 1 with a single failure kind (`extra_keys=report_file` ×67).

- **I1 (informational, non-blocking):** `count-c2.py:258-260` accepts any
  nonzero exit for the drift arm — a crash (e.g. unhandled exception, rc 1 via
  `sys.exit` of a traceback) would satisfy `drift=ok` without a FAIL verdict.
  Cannot be exploited through the committed r53 file under the pinned tool
  (verified: real run yields verdict `SETTLEMENT_SCAN_FAIL`, exit 1, for the
  stated reason); tightening to require `verdict==SETTLEMENT_SCAN_FAIL` would
  close it, but bytes are frozen this round.

## Notes

- Tool read-only on inputs: all writes confined to `--scratch`; verified by
  source (only `selftest`/`write()` touches disk) and by scratch-only diffs.
- Scratch `/fast/scratch/hyaku/mori-r59/Mo59Reviewer11/` cleaned after receipt
  (this report carries all evidence).
