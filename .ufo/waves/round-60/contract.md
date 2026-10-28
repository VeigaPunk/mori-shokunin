# mori round 60 — frozen contract (claims, predicates, kill rules, controls)

Frozen by L1 MoriR60 before any seat scores. Entering branch revision:
`ddfb12fb0838b4307c445194a844f0c4b1950195` (lane `master` tip;
`jj-lane.sh state` local=remote, tree clean). All counting commands run
read-only from the lane repo root (`--repo` defaults to `.`; no r60
instrument carries an absolute host path).

Fresh-start duty (run-11): the last three rejected closures were read first
(`corpus/lessons/round-57-verifier-spotcheck.md`,
`corpus/lessons/round-58-verifier-spotcheck.md`,
`corpus/lessons/round-59-verifier-spotcheck.md`; fleet MANIFEST rounds for
mori 57–59). Every claim below names a surface a do-nothing control cannot
reach; the §9 control receipts were scored at the entering revision and are
committed under `.ufo/waves/round-60/evidence/control-c{1,2,3}-do-nothing.txt`
before this wave dispatches.

Round-59 verifier spot-check routed defects this round must fix:
1. dead evidence pointers in report+SCORECARD (C1);
2. uncommitted round work at tip (resolved before this round by lane commits
   `f091bd77` + `a86e5f83`; C1's absent-set arm reconciles the record);
3. report↔lesson absent-at-filing inconsistency (C1);
4. missing committed receipts for `C1=met`/`C2=met` at data rev `7b86704d`
   (C1);
5. instrument-robustness items — gate execution on `tool_ok`, containment
   asserts, attacker-controlled expect.txt, selftest blind spots,
   `grammar:` orphaning, distinct-span minimum, per-copy row binding,
   drift-arm attribution (C2 and C3).

Instrument-claim axis ruling (round-60 planned item): instrument claims stay
capability-only this round — no scalar axis score moves unless a closure
states one; the SCORECARD rows carry the verified outputs.

## C1 — calibration (score 5, tied lowest non-retired)

Claim: the lane's round-59 self-record is pointer-honest, receipt-complete,
and reconciled with the tree. After-state, all at revision R over committed
bytes:

- DEAD-NAME ARM: `SCORECARD.md` contains no occurrence of
  `c1-entering.txt` or `c2-entering.txt` outside lines carrying the literal
  marker `r60-correction:`; every corrected line names the real committed
  pointer it supersedes the dead name with, and
  `.ufo/waves/round-59/evidence/control-c1-do-nothing.txt` and
  `control-c2-do-nothing.txt` exist at R.
- RECEIPTS ARM: `.ufo/waves/round-60/evidence/r59-c1-met.txt` and
  `r59-c2-met.txt` exist at R and each byte-equals a fresh re-run, at the
  frozen r59 data revision `7b86704d7c0754a09958d131b64dbfa2a6d3eaed`, of
  the corresponding committed r59 counter (exit 0 required).
- ABSENT-SET ARM: `.ufo/waves/round-60/evidence/r59-absent-set.md` exists at
  R with one 5-cell row per frozen name
  {Mo59Executor40, Mo59MutationTester31, Mo59MutationTester32, Mo59Critic29,
  Mo59Reviewer16}; its at-data-rev and at-R cells agree with
  `git cat-file -e` truth at `7b86704d…` and R; disposition is
  `late-committed` exactly when the file was absent at `7b86704d…`, else
  `wrong-superseded`; and `corpus/lessons/round-60.md` exists at R naming
  every wrong-superseded name with `supersedes`, every late-committed name
  with landing pointer `f091bd77`, and the string `supersedes round-59`.

- Counting command: `python3 .ufo/waves/round-60/count-c1.py R [--scratch DIR]`
- Frozen target output (after): `C1=met dead-uncorrected=0 receipts=2/2
  absent-set=5/5 lesson=ok rev=R`, exit 0.
- Do-nothing control (§9): at entering `ddfb12fb…` → `C1=unmet
  dead-uncorrected=2 receipts=0/2 absent-set=0/5 lesson=absent`, exit 1 —
  `evidence/control-c1-do-nothing.txt`.
- Selftest: `count-c1.py --selftest` → `C1_SELFTEST pass=6 fail=0`, exit 0.
- Kill rule: any post-freeze change to counter bytes, contract bytes, the
  predicate sentence or the target output invalidates the claim.

## C2 — depth (score 5, tied lowest non-retired)

Claim: the hardened entry-claims verifier
`tools/mori-entry-claims-check.py` (frozen sha
`cffe9f3359097277a7ea39729309efdc5831a1738994ceb30ee023ac0eae6e69`) closes
the routed r59 entry-class defects on the SAME real entry, with no false
negative: H1 `grammar:` reasons block the verdict; H2 claims resolve to
distinct byte spans (line/offset aliasing collapses; whitespace-only quotes
rejected; ≥8 distinct bytes per span); H3 claim texts pairwise distinct and
≥10 chars; H4 every cited copy binds to a mined used-by-exact registry row
whose source cell names the copy's `.ufo` artifact; H5 the drift arm is
reason-attributed (pinned `tools/mori-settlement-scan.py` sha
`4c04bf21…ac9a9` must FAIL the r53 file with a `:extra_keys=` member
key-set reason while r54 bytes at an r53-named scratch path scan OK — the
filename-heuristic mutant dies). Thirteen committed hostile trees
(`trees-c2h/`, builder `build-fixtures-r60.py`) each evaluate with the
verdict their counter-frozen expect table demands; a committed expect.txt
that disagrees with the frozen table is `expect_tamper` (G3).

- Counting command: `python3 .ufo/waves/round-60/count-c2.py R [--scratch DIR]`
- Frozen target output (after): `C2=met selftest=ok scan=ok drift=ok
  trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 spans=13
  rev=R`, exit 0.
- Do-nothing control (§9): at entering `ddfb12fb…` → `C2=unmet …
  failed=…,tool_absent,selftest,trees,trees_set`, exit 1 —
  `evidence/control-c2-do-nothing.txt`.
- Selftest: `count-c2.py --selftest` → `C2_SELFTEST pass=8 fail=0`;
  `mori-entry-claims-check.py --selftest` → `ENTRYCLAIMS_SELFTEST pass=13
  fail=0`.
- Kill rule: same as C1.

## C3 — operability (score 7, owned axis)

Claim: the Sentinel57/58 execution boundary is closed in the round-60
counters and the closure is demonstrated by replaying the routed PoC
constructions: G1 toolgate — an unpinned tool blob that writes an
EXEC-MARKER is never executed by the pinned round-60 count-c2 (reason
`tool_sha`, no marker anywhere under its scratch) while the revision-pinned
r59 counter against the same PoC DOES write the marker (the hole, reproduced
as control); G2 containment — the counters' materialize() refuses `..`
walks and symlink-parent escapes with nothing written outside the scratch
root; G3 expectgate — a PoC repo committing an expect.txt that disagrees
with the frozen table yields `expect_tamper:h02-malformed-claim`.

- Counting command: `python3 .ufo/waves/round-60/count-c3.py R [--scratch DIR]`
- Frozen target output (after): `C3=met toolgate=ok containment=ok
  expectgate=ok cases=6 rev=R`, exit 0.
- Do-nothing control (§9): at entering `ddfb12fb…` → `C3=unmet …
  failed=count_c1_absent,count_c2_absent,g1_new_skipped,g2_skipped,g3_skipped`
  with the old-counter arm reproducing the marker hole, exit 1 —
  `evidence/control-c3-do-nothing.txt`.
- Selftest: `count-c3.py --selftest` → `C3_SELFTEST pass=3 fail=0`.
- Kill rule: same as C1. count-c3 pins count-c1 (sha `795c1f31…ddbae`) and
  count-c2 (sha `8c4814f5…df976`); count-c1 executes no repo-supplied tool
  blob (its re-runs are revision-pinned), so G1 is structural there.

## Sourced-claim rule (§2b)

C2 and C3 rest on registry rows opened this round (own-work tier A/B:
the committed r59 attack reports Mo59Critic22, Mo59Sentinel57, Mo59Critic25;
Mo59Sentinel58 opened and rejected as a duplicate-scope row) recorded in
`corpus/SOURCES.md` with Gate quotes in `corpus/lessons/round-60.md`. The
hardened-grammar knowledge entry `corpus/knowledge/entry-claims-hardening-r60.md`
cites those rows.

## Round shape

One v2 wave `w1`, 64 seats, policy v2 (band 64–128). Attack share ≥ 25%
(reviewer+critic+mutation-tester+sentinel). §3 planner seat held by the L1;
bounded planning data-walks ride connector/scout items. Assimilation:
none (no merge/mori theme fits the instrument-hardening claims; recorded in
the report). considerthese: the 2026-10-26 reflection's absolute-host-path
item is honored by construction (no r60 instrument carries an absolute host
path) and recorded as a lesson line, not a claim.

## Census

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin mori` at round start (before: exit 0, 333
rows, standing W04 set) and round end (exit 0 required; new S rows raise
the count).

## Amendment clause

Amendments are allowed only before any seat scores; every amendment is
recorded here with its reason.

- Amendment 1 (pre-dispatch, no seat scored): the rewritten tool selftest
  was missing its summary print (the counter's `selftest=ok` token checks
  the printed line) and the fixture builder wrote empty expect.txt files
  because it never passed the frozen expects into `write_tree`. Fixed both;
  tool sha is now `cffe9f33…e6e69` (PIN_EC), count-c2 `8c4814f5…df976`,
  count-c3 re-pinned. Trees regenerated with byte-exact expect.txt files.
  No predicate, target or kill rule changed.
