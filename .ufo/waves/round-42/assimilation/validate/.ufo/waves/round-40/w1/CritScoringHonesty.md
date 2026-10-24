# CritScoringHonesty — round-40 SCORECARD-number calibration attack

Seat: critic. Scope: every number in the drafted `SCORECARD.md` round-40 section
(`SCORECARD.md:2216-2260` at HEAD `ede486b`), re-derived from committed receipts
with one command each. Evidence dir: `.ufo/waves/round-40/evidence/` (41 files,
all `git ls-files`-tracked; three c10 receipts carry peer wall-time/command
annotations in the worktree — verified their result lines are byte-identical to
the committed blobs via `git show HEAD:<path> | sha256sum`).

## Re-derivation table (committed receipt → drafted number)

| Drafted number | One command | Receipt output | Verdict |
|---|---|---|---|
| `pass=11` selftest | `grep -c '^PASS ' evidence/c10-after-selftest.txt` + `grep -oE 'pass=[0-9]+ fail=[0-9]+'` | 11 PASS lines; `CONFORM_SELFTEST pass=11 fail=0` | SUPPORTED |
| `pass=15` selftest | `grep -oE 'pass=[0-9]+ fail=[0-9]+' evidence/c11-after-selftest.txt` | `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0` | SUPPORTED |
| `pass=8` (r39 gutted) | `grep -oE 'pass=[0-9]+ fail=[0-9]+' evidence/c10-red-conjunct.txt` | `CONFORM_SELFTEST pass=8 fail=0` | SUPPORTED |
| `pass=0 fail=10` (v3 gutted) | `grep -oE 'pass=[0-9]+ fail=[0-9]+' evidence/c10-after-conjunct.txt` | `CONFORM_SELFTEST pass=0 fail=0`? NO — prints `pass=0 fail=10`, `selftest_conjunct` in every `failing=` list | SUPPORTED |
| **34** as-of ids | `grep -oE 'superseded_as_of=\[[^]]*\]' evidence/c11-after-lane.txt \| tr ',' '\n' \| wc -l` minus the predicate-echo literal `superseded_as_of=[...]` | **35 ids** (list ends `…,S193,S226]`; `superseded=[...]` also 35) | **UNSUPPORTED — measured value is 35** |
| 18 v2 as-of ids | same command on `evidence/c11-before-lane.txt` | 18 ids, S226 absent | SUPPORTED |
| `pass=0 fail=10` (v3 gutted) | `grep -oE 'pass=[0-9]+ fail=[0-9]+' evidence/c10-after-conjunct.txt` | `CONFORM_SELFTEST pass=0 fail=10`, `selftest_conjunct` in every `failing=` list | SUPPORTED |
| nine survivor fixtures | `grep -l 'CONFORM=met' evidence/c10-red-*.txt` | only **8 of 9** survivor fixtures printed `CONFORM=met exit 0`; `c10-red-divzero.txt` prints `conformance setup error: division by zero`, `EXIT=2`, no CONFORM line | **WORDING UNSUPPORTED — "eight survivor fixtures + a two-counter audit"; divzero is a separate exit-2 class (contract line 82 already says so)** |
| two-counter audit | `grep -E 'CONFORM=|EXIT' evidence/c10-red-multicounter.txt` | `CONFORM=met` / `EXIT=0` (v2); after: `CONFORM=unmet` per-counter violations | SUPPORTED |
| 228→229 census | `git show bb1f2457:corpus/SOURCES.md \| grep -cE '^\| S[0-9]+'` and same at `HEAD` | **228** and **229**; `S229` row at HEAD:235 directly after S228:234 | SUPPORTED |
| census exit 0 both ends | `cd /home/vgpnk/Projects/shokunin && bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` | `CENSUS_EXIT=0`, output **byte-identical** to committed `census-end.txt` (16 W04 rows + `mori ok`) | SUPPORTED (live re-run) |
| `stale_supersede=[S069]` | `grep -oE 'stale_supersede=\[[^]]*\]' evidence/c11-after-e37dcc6.txt` | `[S069]`; as_of 33 there (34 eligible − S069) | SUPPORTED |
| conjunct-gutted signature | receipts `c10-red/after-conjunct.txt` | r39 `pass=8 fail=0` vs v3 `pass=0 fail=10` | SUPPORTED |
| `stale=[S008]` kill-rule signature | `grep stale evidence/c11-red-readd.txt` | v2 dag-r prints `stale_supersede=[]` — signature **absent from committed receipts**; it comes only from the uncommitted scratch mutant (`w1/MutGateReadd.md` selftest `stale=[S008]`) | **MISATTRIBUTED** (rule is real; the committed-fixture discriminator is `superseded=[]/as_of=[]` → `[S008]`, not `stale`) |
| dag-p "fabricated changed line" | compare `c11-red-firstparent.txt` vs `c11-after-fixture-p.txt` | **both** print `changed S001 superseded_by=S002`; v3 flips only `as_of=[]→[S001]` and `stale=[S001]→[]` | **WORDING UNSUPPORTED** — the `changed` line is the tip-vs-first-sighting drift channel (gate docstring :241-247); v2's fabrication was the **stale verdict**, not the changed line |
| 66 seats | `python3 -c "len(items)"` over `w1-spec.json` | 66 items | SUPPORTED (but the frozen contract prose still says "64 seats" — same stale arithmetic the draft corrects) |
| 32 attack = 48.5% | role Counter over spec | critic 9 + reviewer 16 + mutation-tester 4 + sentinel 2 = **31**; reaches 32 only if `revenger` (1 seat) counts as attack | TAXONOMY-AMBIGUOUS — cite the role list or drop to 31/47.0% |
| held scores 6/7/5/5/5/6 | Axes table SCORECARD.md:10-15 | coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6 | SUPPORTED — but "calibration 5 and depth 5 (tied)" **omits freshness 5** from the lowest-tie set (rounds 21-24 precedent names all three); selection still valid since depth ∈ lowest |
| instrument shas | `sha256sum conform.py count-c8.py tools/mori-sources-appendonly.py fixtures/extracted/*.py` | all six match `freeze-r40.txt` pins (incl. `fe0be179…` r39 checker, `62cd4132…` v2 gate quoted in the draft) | SUPPORTED |

## Live re-run confirmations (independent of receipts)

- `PYTHONDONTWRITEBYTECODE=1 python3 tools/mori-sources-appendonly.py 265a955cc… --repo .` → `superseded_as_of=[35 ids incl. S226] stale_supersede=[]` — confirms **35**, not 34.
- `diff fixtures/extracted/count-c7-r39.py count-c8.py` → 5 lines removed (c7:r39 21.8KB pair), behavior parity per `c10-parity.txt` — SimpCounters "~16 dead lines" is contract prose only; the actual delta is 5 removed lines (1 regex + 4-line dead `table` branch).

## Impacted axes

- **calibration** (primary): the scorecard's folded M24 correction *re-commits the same off-by-one* — contract predicted 19, draft "corrected" to 34, receipts measure **35**; "16 never-edited" is really **17** ("S226 plus 16 earlier"). Three draft sentences carry the wrong arithmetic (correction paragraph ×3, kill rule "18 ids ≠ 34").
- **operability C1 before-cell**: "nine survivor fixtures … CONFORM=met" overclaims vs `c10-red-divzero.txt` (exit 2, no verdict line).
- **depth C2 before-cell/kill-rule**: "fabricates a changed line + stale verdict on dag-p" and "prints stale=[S008] on dag-r" mis-describe committed receipts (see table).

## Smallest safe corrections

1. `34` → `35`; `16` → `17` ("S226 plus **16** earlier"; "omits all **17**"); kill rule `18 ids ≠ 34` → `≠ 35`. P-C11's semantic sentence and the S226 discriminator are untouched; this is pure arithmetic correction, same erratum class as M24 — and M24's lesson text should itself be updated to say the parenthetical arithmetic was wrong **twice**.
2. Before-cell: "print `CONFORM=met` exit 0 on **eight** survivor fixtures + a two-counter audit; the ninth (divzero) exits 2 in setup" — already what the contract says at line 82.
3. dag-p wording: "fabricates a **stale verdict** on dag-p" (the `changed` drift line persists by design — tip vs first sighting).
4. Kill rule 3: cite the mutant selftest (`stale=[S008]`, MutGateReadd) as the signature source, or re-word to the committed-receipt discriminator `superseded=[] → [S008]` / `as_of=[S008]`.
5. Optional nits: name the attack-role taxonomy (or write 31–32), complete the lowest-tie set as "depth/calibration/freshness 5", note the frozen contract's "64 seats" vs spec's 66.

None of these touch the predicates, instruments, or claim structure — the C1/C2 semantic claims survive; only the round's number-quoting is wrong.

## Tooling

No installs needed (python3, git, sha256sum only).
