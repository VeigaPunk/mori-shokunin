# Round 100 — verifier spot-check (mori)

author: hyaku closure (non-author integrator, @m_zfl)

Closure of lane-round mori r100. Report `.ufo/reports/round-100/mori.md` (fleet repo); prompt
`.ufo/prompts/mori-round-100.md`; entering `d1bd1b339b894de0249b0f60702dff9962da88d9`, tip
`79c673bfc794c86a4c0b3da81c82f9e904d8413f`. Driver digest (copied from `.ufo/watchdog.log`):
`2026-11-05T19:46:04-03:00 launch mori round=100 pgid=2032920 driver=hyaku-inline attempt=1`;
`2026-11-05T21:01:21-03:00 complete mori round=100; hyaku-inline attempt=1`.
This closure took its measurements on 2026-11-06 UTC over `git archive` trees of `d1bd1b33` (before), `5e2bcf2c`
(landing) and `79c673bf` (tip) under `/tmp/mori100close.wtqZ/`. That directory is scratch: the commands are the
evidence, not the directory. I re-ran the frozen claim counters `count-c1.py` and `count-c2.py` from the tip tree.
They are claim instruments, not registered gates; `count-c1.py` invokes the tool's `--selftest` and the r17 fixture
gate as conjuncts. I executed no other lane gate. I verified the append-only gate from its committed receipt only.

## 1. Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report committed by lane identity | `git log --format='%an <%ae> %H %ci' -- .ufo/reports/round-100/mori.md` (fleet) | `mori-shokunin <mori@shokunin.local> 1a66aacc… 2026-11-05 21:00:33 -0300` (after lane tip commit 20:58:25) | ok |
| `SHONEN` heading, one line per box | read report `## SHONEN` | 4 lines, all `[~]` with pointers | ok |
| cited commits exist, ancestors of `master` | `git cat-file -e <h>^{commit} && git merge-base --is-ancestor <h> refs/heads/master` for d1bd1b33, 9579cff6, 5e2bcf2c, 878708b3, a7951675, 6a1fc283, dc9c9fed, 79c673bf | all 8 `ok`; all 7 round commits authored `mori-shokunin` | ok |
| lane pushed, clean | `scripts/hyaku/jj-lane.sh state …/mori-shokunin`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `local=remote=79c673bf… ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty; remote `79c673bf…` | ok |
| prompt carries template contract | `diff <(head -n 140 prompt) kimi-shokunin/templates/round-prompt.md`, template-side lines without `{{` | 0: placeholder substitutions only; hyaku addendum §6 follows | ok |
| frozen instruments unchanged after freeze | `git diff --stat 9579cff6 79c673bf -- count-c1.py count-c2.py controls-r100.py contract.md candidate/` | empty | ok |
| landed tool == frozen candidate | `diff <(git show 9579cff6:…/candidate/tools/mori-seat-terminal.py) <(git show 5e2bcf2c:tools/mori-seat-terminal.py)` | identical | ok |
| pre-freeze controls | `git show 79c673bf:.ufo/waves/round-100/evidence/controls-r100.txt` | K0–K8 and K0c–K5c `unmet`; P1 and P2 `met`; `CONTROLS_DONE unexpected=0 … seed=100` | ok (single seed: see D1) |

This is a real report, not a marker report. Status `ok`. Step-1 receipt defects (status-neutral) are listed in §5 as D2.

## 2. Claims — re-check

### C1 coverage (6): the seat terminal census names credential and entitlement deaths `dead_auth`

Re-measured with the frozen counter: `python3 79c673bf/.ufo/waves/round-100/count-c1.py --root <tree> --seed S --work W`.

| tree | seed 10 | seed 3 | seed 2611 |
|---|---|---|---|
| `d1bd1b33` | `C1=unmet cases_ok=23/50 … registry=unmet sourced=unmet checks_failed=battery,registry,sourced` rc 1 | same, rc 1 | same, rc 1 |
| `5e2bcf2c` | `C1=unmet cases_ok=49/50 families_failed=A1-auth-status … checks_failed=battery` rc 1 | `C1=met cases_ok=50/50 … sourced=met(S637,S638) checks_failed=-` rc 0 | same as seed 3, rc 0 |
| `79c673bf` | same as landing seed 10, rc 1 | `C1=met 50/50` rc 0 | `C1=met 50/50` rc 0 |

These runs match `evidence/before-c1.txt`, `landing-c1.txt` and `landing-c1-killrule.txt`. The frozen kill rule
(contract line 33, "any family failing on any seed at landing = C1 unmet") fires, so **C1 is unmet as frozen**,
as the lane reports.

The miss case, printed with the counter's own generator
(`count-c1.battery(random.Random(10))`, case C006):
`{"errorStatus": 403, "errorMessage": "403 token expired (request id r-18429)"}`, planted `dead_auth`.
The tool returns `dead_rate_limit` because the request id contains the substring `429`.

The lane calls the label wrong, not the tool. I agree only in part. The counter planted a token it did not label,
but a random request id holding `429` is not rate evidence either. A real 403 with such an id would be misfiled, so
this is also a live precision defect in the round-17 substring rule. The lane routes it to r101 (Planned item 1);
it was not introduced this round.

Evidence-verified, not re-run:
- live trial `w1/Mo100ExecTrial.md:61,69`: `dead_error_other -> dead_auth : 22`, "no other totals key" moved;
- held-out records `w1/Mo100CritC1.md:87`: entering 14/26 (landing 22/26 per the report);
- `selftest=ok` and `r17gate=ok` conjuncts green on every tip run above.

Coverage axis, plain measurement:
- `git grep -c dead_auth <rev> -- corpus/knowledge SKILL.md PROVINCE.md`: no hit at `d1bd1b33`; at `79c673bf`,
  SKILL.md 2 and `corpus/knowledge/seat-auth-deaths-r100.md` 5;
- the class covers 22 real seats that the entering tool filed as unknown.

**Coverage `improved`; claim C1 not verified (unmet).**

### C2 calibration (5): stated quote word counts in SOURCES.md match their quotes

Re-measured with `python3 79c673bf/.ufo/waves/round-100/count-c2.py --root <tree> --repo …/mori-shokunin --list`
(base `d1bd1b33`).

| tree | output | rc |
|---|---|---|
| `d1bd1b33` | `C2=unmet stated=58 mismatches=7 uncorrected=7 spurious=0 altered=0 census=ok checks_failed=mismatch` | 1 |
| `5e2bcf2c` | `C2=met stated=60 mismatches=7 uncorrected=0 spurious=0 altered=0 census=ok checks_failed=-` | 0 |
| `79c673bf` | `C2=unmet stated=66 mismatches=7 uncorrected=7 … checks_failed=mismatch` | 1 |

C2 was met as frozen at landing. The landed form appended corrections inside the anchor cells of S581–S584 and
S634, which breaches CORPUS rule 2 (`CORPUS.md:117-118`: "A correction is a new row whose `teaches` opens
`supersedes S0NN —`"). The repair `878708b3` reverted those edits.
`git diff --stat d1bd1b33 79c673bf -- corpus/SOURCES.md` shows `8 insertions(+)` and no deletions; no S221, S58x or
S634 line changed. The tip therefore reads unmet. The lane withdrew the claim. I agree that a claim met only by a
rule breach cannot be admitted. **C2 not verified.**

Calibration axis, plain measurement independent of the frozen counter: SOURCES rows whose stated word count
mismatches and that have no word-count `supersedes` successor
(`git show <rev>:corpus/SOURCES.md | grep -oE 'supersedes S(58[1-4]|634)…'`).
- At `d1bd1b33`: S581 and S583 are already corrected by S586/S587 (r72). S582 has only a line-pointer successor.
  S634 (17→18) has none.
- At `79c673bf`: every one has a word-count successor (S640–S644). S640 closes r99 D1.

S641 and S643 restate corrections S586/S587 already made, which is redundant: see D3.
**Calibration `improved`** (≥2 → 0 uncorrected stated counts, rule-2 form), with the frozen claim unmet.

### Harm check

- `git diff d1bd1b33 79c673bf -- SCORECARD.md`: additions only (Round 100 verdict and Planned r101). No score
  move is claimed, and no Score or Evidence cell is removed.
- `git diff --numstat`: SKILL.md +2/−2 (registry row edited in place), QUALITY +18, LOG +10, SOURCES +8.
  PROVINCE.md is untouched.
- The disclosed schema change (`totals` gains `dead_auth`) lands together with the r17 gate's class set
  (`r17gate=ok` at tip).
- The append-only gate at the final tree reads `round_changed=[] stale_supersede=[]`, the same as entering
  (committed receipt `evidence/appendonly-final.txt`, not re-run).
- Census `mori ok`, rc 0.

No axis is harmed at the tip. The transient rule-2 breach at `5e2bcf2c` is repaired, not standing harm.

## 3. Discernment spot-check (`corpus/lessons/round-100.md` `## Gate`)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S637 Connect protocol | admit, mined, tier A | `curl https://connectrpc.com/docs/protocol/` → 200, 148033 B, sha256 `55d644c62a7d094e…` (= pinned); quote "use unauthenticated if the user can’t be identified or presents invalid credentials." found after tag strip; 12 words | agree | primary spec text for the code-choice rule; byte-identical to the pin |
| Connect HTTP→code table as the 429 rule | reject | same fetch: the HTTP→code table reads `429 Too Many Requests unavailable`, and the code→HTTP table reads `resource_exhausted 429` | agree | Connect maps 429 to a retry code, not a cause; the census separates deaths by what clears them, so 429 stays rate evidence |
| S221 re-point by `used-by` | reject (reverted) | S221 row at tip: scope "§15.4 Redirection 3xx", `used-by` unchanged vs entering | agree | a row teaches its own scope; §15.5 needs its own row (S639) |
| S644 QueryUnbiasedInterruptTime (new row, SOURCES.md:425) | admit, correction row | `curl` learn.microsoft.com …/nf-realtimeapiset-queryunbiasedinterrupttime → 200, 54774 B; quote "If the function fails because it is called with a null parameter, the return value is zero." found verbatim; `len(q.split())` = 17 ≤ 25 | agree | quote present, count stated correctly, and it replaces S584's 26-word over-cap quote |
| S638 gRPC status codes (new row, SOURCES.md:419) | admit, mined | `curl` grpc.github.io …/md_doc_statuscodes.html → 200, 18133 B; quote "PERMISSION_DENIED must not be used for rejections caused by exhausting some resource" found, 12 words | agree | grounds the quota-over-permission precedence |

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → `mori ok …/corpus/SOURCES.md`,
rc 0, 50 W04 (44 at entering per `evidence/census-before.txt`; the six new W04 are S639–S644). Rows 408 → 416
(`git show <rev>:corpus/SOURCES.md | grep -cE '^ {0,3}\| *S[0-9]{3,}'`), matching the report.

## 4. Trend verdicts

- **expansion: improved** — new knowledge entry `corpus/knowledge/seat-auth-deaths-r100.md`; `dead_auth` had no hit
  in knowledge/SKILL/PROVINCE at entering. It rests on three new tier-A mined spec rows: S637, S638, S639.
- **quality: improved** — the registered seat-terminal probe now names the dominant real death cause:
  - 22 live seats moved `dead_error_other` → `dead_auth` with no other transition (evidence-verified);
  - battery 23/50 → 50/50 on two closure seeds (3, 2611).

  This is tempered by the confirmed substring precision defect (seed 10, C006, D1).
- **discernment: improved** — the lane withdrew a claim that was met as frozen once it saw the CORPUS rule-2 breach.
  It repaired the breach the rule-2 way, published its counter defect as Mistake 7, and every sampled gate decision
  agrees on re-opening. This is tempered by two points:
  - the append-only gate that SKILL.md requires before a SOURCES edit was not run before landing (Mistake 5);
  - S641 and S643 duplicate r72 corrections (D3).

## 5. Routed defects (lane fixes next round)

- **D1 (substring rate/quota evidence; single-seed controls)** — the `429`/`402` substring rule misfiles an
  auth death whose request or trace id holds those digits. This closure reproduced it: seed 10, C006,
  `403 token expired (request id r-18429)` → `dead_rate_limit`. It is a live tool defect, not only a counter-label
  defect. Fix it with digit boundaries (Planned r101 item 1). Run pre-freeze controls on several seeds.
- **D2 (receipt hygiene)** — two receipts do not match what they record:
  - `evidence/final-c1.txt` is headed "final 6a1fc283…" while the report's table labels that column `final (dc9c9fed)`;
  - `evidence/appendonly-final.txt` line 2 interleaves two runs' tokens (`stale_supersede=[...] appendonly_violations=50 … stale_supersede=[...] round_changed=[S581,…]`), which is not cleanly parseable.

  Write one run per labelled line, at the revision named.
- **D3 (redundant correction rows)** — S641 and S643 restate the word-count corrections S586 and S587 made in r72,
  adding census W04 noise. The next stated-count counter must be supersession-aware (QUALITY 213, Planned r101
  item 3) and should count only rows without a successor.
- **D4 (closure-side error, acknowledged)** — the r99 spot-check's D1 told the lane to correct the SOURCES row
  "in place". That contradicts CORPUS rule 2 and led to Mistake 5. The lane was right to override it; this
  closure withdraws that advice.
- **Carried** — r99 D3/D4; battery gaps G1–G5 (`w1/Mo100MutC1.md`); census E11 on intermediate commits
  `878708b3`–`6a1fc283` (disclosed; clean at `dc9c9fed`).

## 6. Closure result

Status `ok`. Neither claim verifies:
- C1 is unmet under the frozen kill rule, reproduced on seed 10;
- C2 was met only through a CORPUS rule-2 breach, was withdrawn, and is unmet at the tip.

No axis is harmed. Axis verdicts:

| axis | verdict |
|---|---|
| coverage | `improved` |
| calibration | `improved` |
| operability | `unchanged` |
| depth | `unchanged` |
| freshness | `unchanged` |
| adjacency | `unchanged` |

Verdict: **rejected-honest-stop** (admitted false). Capabilities added: none admitted (the `dead_auth` class is an
in-place change to a registered probe; its claim did not verify). SHONEN boxes stay `[~]` with resolvable pointers.
Whether they are fully checkable is for the operator (promotion is operator-owned).
