# mori round 28 — claim contract (attempt 1, L1 MoriR28)

Entering tip `6ebd518f` (round-27 verifier spot-check; round 27 closed `rejected-honest-stop`, C1 depth verified,
C2 withdrawn and therefore not verified). Written before any round-28 implementation. Targets, not results. Both
claims are repairs routed by `corpus/lessons/round-27-verifier-spotcheck.md` (routed defects 3, 4 and 5). Nothing
declared here will be withdrawn: a declared claim that misses is reported as a miss.

## Why these two claims

- Lowest-scoring active axes are depth, freshness and calibration (5 each, `SCORECARD.md:12-14`). C1 works
  freshness ("skill claims re-verified against live surfaces; stale items flagged or fixed", AXES.md).
- C2 is the case freeze withdrawn in round 27 (r26 D7). Its case writers are blind seats on a working route.
- The two are causally separable: C1 touches `corpus/SOURCES.md` only; C2 touches the oom-killers fixtures, the
  round-28 C2 counter and, only if a frozen case shows a tool defect, `tools/mori-oom-killers.py`.

## C1 — freshness (score 5, tied lowest): eight carried row defects superseded, first-published cells restored

Statement: at the landed tip the round-27 QUALITY 81 check (`.ufo/waves/round-27/check-row-identity.py`, blob taken
from `df886be1`) prints `changed=0 removed=0 bad=0` (S096, S097, S101 restored byte-equal to their first-published
cells), and `corpus/SOURCES.md` holds, for each of S096, S097, S101, S127, S128, S129, S131 and S140, a new row (id
above S144) with status `mined` whose `teaches` opens `supersedes S0NN — `, re-opened against the upstream bytes in
round 28 and recorded in the lesson `## Gate` with URL, access time and a located quote of at most 25 words.

Counting command (committed bytes only; exit 0 met, 1 unmet, 2 bad revision or missing input):

```sh
bash /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-28/count-c1.sh <rev>
```

Before (at `6ebd518f`): `row_identity=rows=144 changed=3 removed=0 bad=0`, `superseding=0/8 ids=none`, `C1=unmet`,
exit 1 (`evidence/c1-before.txt`). Declared after (at the landed tip): `C1=met`, exit 0.

## C2 — operability (score 7): pin the ten round-26 amendment-A2 rules with frozen blind cases (r26 D7)

Rule list: identical to `.ufo/waves/round-27/contract.md` lines 49-58 (A2-01 … A2-10).

Statement: `tools/fixtures/mori-oom-killers/cases-a2.json` is assembled from cases written by ten seats that do not
read `tools/mori-oom-killers.py` (one seat per rule; they read only the rule text, the round-26 contract and the
round-26 frozen case file for its schema), committed before the L1 runs the tool on it (the freeze hash is written
to `LOG.md` in the freeze commit's own batch and the first tool run is later), unchanged after that commit, and at
the landed tip the round-28 counter prints `C2=met`.

Counting command:

```sh
bash /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-28/count-c2.sh <rev>
```

The round-28 counter is the round-27 counter hardened against `.ufo/waves/round-27/w1/CriticC2Counter.md`
F1–F8 and F11: ≥20 cases; every case printable unique `id` and exactly one listed `rule`; every rule ≥2 cases
with distinct `inputs` and ≥1 case whose `expect.fields` pins the field the rule names; the round-26 `cases.json`
blob equal to its `fc09f96c` blob; tool exit 0 and exactly one `MORI_OOM_KILLERS_SELFTEST:` line per file; the
freeze commit found with full history and rename following. It is committed before the case file.

Before (at `6ebd518f`): `a2_cases=0`, `C2=unmet`, exit 1 (`evidence/c2-before.txt`). Declared after (at the landed
tip): `C2=met`, exit 0. If the tool fails a frozen case, the L1 may change the tool (never the case file); a case
the tool cannot meet without breaking a round-26 frozen case is a miss, reported as one.

## Held, not claimed

Depth 5, calibration 5, coverage 6, adjacency 6 observed. No retirement, waiver, exploratory claim or promotion.
No-harm check: lane retention scan unallowlisted metric at the landed tip must not exceed its value at `6ebd518f`
(`python3 -I -B tools/mori-retention-gate.py scan --repo <lane> --rev <rev> --policy
.ufo/waves/round-18/frozen/c1-policy.json --allowlist corpus/evidence/retention-allowlist.json`); the five
round-26 selftests keep their tallies.

## Routed hygiene (never a counted claim)

Round-27 routed defects 1 (W1 future-dated: dated correction appended below), 2 (tip receipts: committed for
`df886be1` and, as the last lane batch, for the round-28 tip), r25 R1 and R5 (sandboxed fixes, landed only when a
non-author check passes; otherwise carried with the reason).

## Correction to round-27 amendment W1 (appended 2026-10-22, round 28; W1 itself is not rewritten)

See `.ufo/waves/round-27/contract.md` "Correction to amendment W1 (round 28)".

## Amendment A1 (round 28, before any superseding row or case exists; times are read from git at commit)

Raised by wave-1 critics CriticC1Design (findings 1-3), CriticRoutingCoverage (gaps 1-3, 5) and CriticC2Design (F1).
Every change below makes a claim harder to meet or corrects a status rule CORPUS.md already sets; none narrows a
target, and no data existed when it was written.

- **C1 scope.** "C1 touches `corpus/SOURCES.md` only" is replaced by: C1 touches `corpus/SOURCES.md`, the round-28
  lesson `## Gate`, and the live readers (`SKILL.md`, `PROVINCE.md`, `corpus/README.md`, `corpus/knowledge/`) that
  cite a superseded id; history files (LOG, SCORECARD, lessons, `.ufo/`) are untouched.
- **C1 counter** (`count-c1.sh`, rewritten in this commit). A superseding row counts only when: its `teaches` after the
  prefix differs from the superseded row's; its status is `mined` with a non-empty `used-by`, or `rejected` when the
  row it supersedes is `rejected` (S097 is a 404 page; CORPUS keeps rejections as rows; `verified` is no CORPUS status
  and is no longer accepted); every `used-by` path cites the new id as a word at `<rev>`; and the round-28 lesson
  `## Gate` holds a line for the new id with an https URL, a 64-hex sha256 and a quoted span. New: `readers_left` (live
  reader lines citing any of the eight superseded ids as a word, lines naming tsukuroi's own ids excluded) must be 0.
  Before with the amended counter at `6ebd518f`: `superseding=0/8`, `readers_left=27`, `C1=unmet`, exit 1
  (`evidence/c1-before-a1.txt`).
- **C2 field map.** A2-07's required pinned field is `earlyoom.earlier_invocation_send_lines` with an integer value
  above 0 (CriticC2Design F1: `actions.sigterm` does not decide A2-07); an `exit` pin must be an integer, not a bool.
  The C2 before-value is re-run with the round-28 counter when it lands.
- **Tip receipts.** "Receipts for the round-28 tip" means: the last lane batch adds only receipt files, measured at
  that batch's parent; the report cites both hashes (a commit cannot hold a receipt of itself).
- **W1 bound.** The round-27 W1 correction's author-time bound is replaced by the committer-time bound (jj author time
  is when the change was opened); see `.ufo/waves/round-27/contract.md`.
