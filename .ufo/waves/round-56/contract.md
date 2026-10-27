# mori round 56 — frozen contract (L1 MoriR56, attempt 1)

Entering lane tip: `5b295eeebd87ebd610d8d39bfe2035742f740cfa` (round-55 closure
`corpus/lessons/round-55-verifier-spotcheck.md`, rejected-honest-stop; both
claims unmet on recorded causes). Scores entering: coverage 6, operability 7,
depth 5, freshness 5, calibration 5, adjacency 6. Two non-exploratory claims,
distinct owned axes (coverage is the lowest owned axis), no scalar score
change claimed; closure sets axis verdicts. The planner seat is held by the L1
(the validator does not permit a planner role).

Freeze includes this contract, both counters, the controls module, the pinned
tool sha256 values, the evidence copies and their pins. The contract and
counters are immutable after any seat scores; the counters carry `PIN = None`
in the working tree and receive their frozen pins in the freeze commit (the
pin value is the sha256 of the tool file at the data commit).

## C1 — coverage: FR5 bounded advance, the driver-liveness probe

Predicate P-C1 is the exact counter docstring in `count-c1.py`. Surface: the
hyaku driver's `.ufo/watchdog.log` launch/complete/dead/wrap/fail lines as a
second fleet-liveness source (FR5's round-33 named open ground), reported as
per-lane log-shape facts only. Data: `tools/mori-driver-liveness.py` (probe +
13-case selftest + frozen fixtures under `.ufo/waves/round-56/fixtures/driver/`),
`corpus/knowledge/driver-liveness-r56.md`, source row S544 (own-work, the two
writer scripts; extract `corpus/evidence/sources-r56/watchdog-log-grammar.txt`).

Target at landed revision: tool sha pinned, selftest `pass=13 fail=0 skipped=0`,
every frozen fixture parses with its frozen malformed count, the entry names
S544 and the tool, the S544 registry row is mined with used-by naming the
entry, and the tool text carries no health-verdict string. Command:
`python3 .ufo/waves/round-56/count-c1.py R`. Before: tool absent at entering
tip → `C1=unmet … failed=tool_absent`, exit 1 (control receipt). Kill: any
pin/selftest/fixture/entry/row failure or a health-verdict string => unmet.
C1 is separable from C2 (no shared file except the registry append).

## C2 — operability (capability): the dual-shape seat-output vote binder

Predicate P-C2 is the exact counter docstring in `count-c2.py`. Surface:
seat-output vote binding that accepts BOTH plain-text vote lines and
JSON-wrapped string-scalar votes (the run-10 binding note; the round-55 vote
arm failure cause (1)), plus the re-bound round-55 RECHECK tally over committed
bytes. Data: `tools/mori-vote-bind.py` (extract + tally + 16-case selftest),
`corpus/knowledge/vote-binding-r56.md`, source row S545 (RFC 8259; copy
`corpus/evidence/sources-r56/rfc8259.txt`).

Target at landed revision: tool sha pinned, selftest `pass=16 fail=0`, the
tally over the committed round-55 ledger + results prints exactly
`TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16
bound_voters=15`, a junk-output do-nothing control tallies `zero=78`, the
frozen round-55 C1 counter at R still prints `voted=0` (contrast), the entry
names S545 and the tool, and the S545 row is mined with used-by naming the
entry. Command: `python3 .ufo/waves/round-56/count-c2.py R`. Before: tool
absent at entering tip → `C2=unmet … failed=tool_absent`, exit 1 (control
receipt). Kill: pin/selftest/tally/control/contrast/entry/row failure =>
unmet. C2 is separable from C1.

## Frontier and routed defects

Round-55 routed defects carried here: (1) census before→after must be captured
bytes or the counting command (QUALITY 152 — applied to this round's census
receipts); (2) a before→after row cites the receipt's stamped revision
(receipts here stamp the measured revision themselves). Carried planned item:
the voter final-output format rule is implemented as the dual-shape binder
(C2), not as a seat-format rule; the dispatch-coverage validator (≥2 voters
per scoped row) stays planned — the binder now surfaces single-voted rows
honestly instead of zeroing the arm.

Mistake mined for the frontier step: the round-55 census row-count
misstatement (routed defect 1) — class and fix in the round lesson. Start
census receipt: `evidence/census-start.txt` (exit 0, 316 rows, 23 W04). End
census must exit 0. Assimilation: none unless package material is located and
opened this round; quarantine slice re-derived. considerthese proposals
checked. One v2 wave `w1` (64 seats) carries build and falsification; attack
seats ≥ 16 (25%). Residual work only if it is fewer than 32 concrete attack
items, with an explicit residual call.
