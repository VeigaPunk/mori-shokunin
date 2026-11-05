# mori round 100 — frozen contract (L1 MoriR100, attempt 1)

Entering revision: `d1bd1b339b894de0249b0f60702dff9962da88d9` (r99 admitted; `jj-lane.sh state` local=remote, clean).
Not a fresh-start round (r97, r98, r99 admitted); the r99 spot-check routed defects D1–D4 were read first
(`corpus/lessons/round-99-verifier-spotcheck.md` §5). No earlier attempt (`.ufo/watchdog.log`: only
`launch mori round=100 … attempt=1`).

This file, both counters, the controls runner, the candidate files and their receipts are committed in ONE freeze
commit before any landing. Nothing below changes after the freeze; a miss is reported as a miss.

## C1 — coverage (score 6): the seat terminal census names credential/entitlement deaths

Surface moved: the kill/death-event classification of `tools/mori-seat-terminal.py` gains an edge class,
`dead_auth`, for seats whose last aged record is an HTTP 401/403 or a Connect/gRPC/provider auth refusal, read
after quota and rate evidence; the round-17 fixture gate's class set follows. Motivating evidence:
`evidence/live-errors-prefreeze.txt` — in the fleet's own transcripts of the two days before the round, 187 of 190
terminal errors the round-99 rules call `dead_error_other` carry auth evidence (counts only, no message text).
Sourced: S637 (Connect protocol), S638 (gRPC status codes), opened this round; S221 (RFC 9110) re-opened.

**Predicate P1** (identical in `count-c1.py` docstring and receipt label `C1=met|unmet`):
C1=met iff, for the lane tree, (battery) every case of a battery generated at measurement time from a printed seed
is classified as planted — auth deaths → `dead_auth`; quota/rate evidence beside an auth status or spelling keeps
`dead_quota`/`dead_rate_limit`; Z.AI codes keep their meaning; non-auth errors stay `dead_error_other`;
settled/unsettled/completed/aborted seats keep their class; (selftest) the tool's `--selftest` exits 0 with
`SELFTEST_OK`; (r17gate) the lane's round-17 fixture gate in the tree, on the tree's tool, prints `GATE ok`, exit 0;
(registry) the SKILL.md seat-terminal registry row names `dead_auth`; (sourced) the knowledge entry
`corpus/knowledge/seat-auth-deaths-r100.md` cites S637 and S638 in `source:` lines and both rows are `mined`.

Counting command: `git -C mori-shokunin archive <rev> | tar -x -C DIR` →
`python3 .ufo/waves/round-100/count-c1.py --root DIR [--seed N] --work SCRATCH`.
Before (entering, seed 100): `C1=unmet cases_ok=23/50 … checks_failed=battery,registry,sourced`.
Target: `C1=met cases_ok=50/50 … checks_failed=-` at the landing commit, on the printed seed and on any seed.
Kill rule: any family failing on any seed at landing = C1 unmet; no re-freeze.

Disclosed behaviour change (not a harm claim, read by the closure): the output schema name stays
`mori-seat-terminal-v1`; `totals`, `by_prefix`, `by_provider_model` gain the key `dead_auth`. The round-17 gate at
the entering revision rejects the new tool (`totals_keys`); the landing updates that gate's class set in the same
commit, and its 66 fixture cases are re-run on the candidate (`GATE ok: 66/66`). Seats that were `dead_error_other`
and carry auth evidence move to `dead_auth`; by construction no seat moves between any other classes
(auth is read only where the round-99 rule returned `dead_error_other`).

Counter weakness disclosed before data (QUALITY 212): the battery's fixed templates are readable. Families A4/A5/N5
are composed at measurement time from a word list, so a template lookup fails them (control K5). A forger that
implements the status-and-spelling rule itself is the rule.

## C2 — calibration (score 5, lowest tier): stated quote word counts in SOURCES.md match their quotes

Self-assessment: a registry row states how many words its located quote has (CORPUS rule 1 caps it at 25).
Observed state: the whitespace word count of that quote. Routed by the r99 closure (D1: S634 says 17, the quote
has 18). At entering, 7 stated counts in 5 rows disagree (S581 10→9, 15→14; S582 14→13; S583 14→13; S584 17→15,
22→26 — a quote over the 25-word cap; S634 17→18).

**Predicate P2** (identical in `count-c2.py` docstring and receipt label `C2=met|unmet`):
C2=met iff (mismatch) every stated quote word count in a registry row equals the whitespace word count of its quote
or is answered in the same row by the exact text `[r100 word-count correction: K→W, ...; counted by whitespace]`
(W over 25 written `K→W (over the 25-word cap)`); (spurious) no other `r100 word-count correction` text exists;
(altered) every row that carried a stated count at the entering revision is byte-identical to it once the
correction (and the one space before it) is removed; (census) `sources-census.sh validate --file` exits 0.

Counting command: `python3 .ufo/waves/round-100/count-c2.py --root DIR` (base defaults to the entering revision).
Before: `C2=unmet stated=58 mismatches=7 uncorrected=7 spurious=0 altered=0 census=ok checks_failed=mismatch`.
Target: `C2=met … uncorrected=0 spurious=0 altered=0 census=ok checks_failed=-` at the landing commit.
Causal separability: C1's new rows S637/S638 state counts that match (12/12), so C2 is the same with or without C1
(`apply-c1` alone leaves `uncorrected=7`).

## Controls (executed and committed before the freeze; `evidence/controls-r100.txt`)

`python3 .ufo/waves/round-100/controls-r100.py --rev d1bd1b33… --work SCRATCH` — K0–K8 and K0c–K5c expect `unmet`,
P1 and P2 expect `met`; the receipt must end `CONTROLS_DONE unexpected=0`. Each control id, its construction and
its expected failing conjunct are listed in the runner's docstring.

## Admission reading

Each claim is judged only on its frozen predicate at the landing commit. No score move is claimed for either axis.
At most these two claims; no exploratory claim.
