author: hyaku closure (non-author integrator, @m_opus)

# mori round 29 — verifier spot-check (non-author closure)

Round: mori 29, L1 `MoriR29`, attempt 1. Base `7118f320a5ef18d20c1e361eff77db0e1a97b2d6` → landed tip
`b581173afd85d82283291492de12666d505eb58b` (lane `master`; content parent `67779aa8`, the tip adds only receipts).
Report: fleet `.ufo/reports/round-29/mori.md` (fleet commit `9a133307d4d382f35cf17b429d5d41aef84764e6`). Driver
digest (`.ufo/watchdog.log`, copied):
`2026-10-22T16:46:17-03:00 launch mori round=29 pgid=619064 driver=hyaku-inline attempt=1`;
`2026-10-22T17:53:20-03:00 complete mori round=29; hyaku-inline attempt=1`.

Read-only seats (non-author, dispatched by this closure): C2EvidenceCheck, HarmRuling, GateSpotcheck,
RetentionAndAxes, PromptConformance. No lane gate, selftest or counter was executed by this closure.

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an %ae %H' -- .ufo/reports/round-29/mori.md` | `mori-shokunin mori@shokunin.local 9a133307d4d382f35cf17b429d5d41aef84764e6` | ok |
| `SHONEN` heading, one line per box | report `## SHONEN` vs `git show b581173a:SHONEN.md` | 4 lines for 4 boxes: `[~]` tables, `[~]` end-to-end, `[~]` executable, `[ ]` no bleed | ok |
| Cited lane commits exist and are ancestors of `master` | `git cat-file -e <h>^{commit} && git merge-base --is-ancestor <h> master` | all 15 cited (`8a45cefe` `3a147138` `66125164` `69349c2a` `c3216969` `e1c6bbe7` `420d05ad` `221cbd8f` `d6d5cb0a` `255b7051` `8809a3fe` `cdfcf66d` `07b9a4b9` `67779aa8` `b581173a`) plus base `7118f320`: ok | ok |
| Pushed | `scripts/hyaku/jj-lane.sh state …/mori-shokunin` | `branch=master local=b581173a… remote=b581173a… ahead=0 behind=0 head=detached tracked=0 untracked=1` | ok |
| Remote ref | `git ls-remote origin refs/heads/master` | `b581173afd85d82283291492de12666d505eb58b` | ok |
| Leftovers | `git status --porcelain` | `?? .scratch/` only | not round work (below) |
| Prompt carries template contract | template `{{…}}` substitution diff vs `.ufo/prompts/mori-round-29.md` | 2 hunks, both placeholder resolutions; §§1–5 byte-identical; §6 hyaku addendum present; embed-clause round-level items and five child-lane items all present | ok |
| Report contract minimum | read report | work + evidence, landed-changes table tied to LOG entries (13 rows), sources/cross-domain (systemd, earlyoom; kake stray attributed), SHONEN | ok |

**Uncommitted path `.scratch/`:** `find .scratch -newermt '2026-10-22 16:00'` prints nothing; newest mtime
`2026-10-21 17:05` (directory), contents from round 22 (`.scratch/round22/measure3/…`). It predates the round-29
launch (16:46 -03:00) and was ruled pre-round at r24; the report names it as left untouched. **Not round work.** The
six inherited round-28 paths the r28 closure flagged are resolved (untracked 6 → 1).

## 2. Claims

### C1 — calibration: six `## Axes` rows agree with the admitted closure record — **verified (re-measured)**

Plain re-measure (no lane counter run):

```
git show 63729047:MANIFEST.json | jq -c '[.rounds|to_entries[]|select(.value.lane=="mori" and .value.type=="closure"
  and .value.admitted==true)|{i:.key,lr:.value.lane_round,v:.value.verdicts}]|.[-8:][]'
→ latest admitted closure grading each axis improved: coverage lr26 (rounds[462]), operability lr28 ([476]),
  freshness lr28 ([476]), calibration lr25 ([455]), adjacency lr19 ([398]); depth: only lr12 ([313]) admitted
  (lr27 [468] improved but rejected-honest-stop)
git show <rev>:SCORECARD.md | sed -n '10,15p' | awk -F'|' '{print $2,$3,$5}'
  7118f320: coverage round 12 · operability round 14 · depth round 12 · freshness round 1 · calibration round 1 · adjacency round 1
  b581173a: coverage round 26 · operability round 28 · depth round 12 · freshness round 28 · calibration round 25 · adjacency round 19
```

Rows disagreeing with the closure record on "Last change": **5/6 before → 0/6 after**; scores unchanged
(6, 7, 5, 5, 5, 6). Cited closure lines read at tip and they say what the rows claim
(`round-26-verifier-spotcheck.md:133` coverage improved; `round-28…:92` freshness improved; `round-28…:93`
operability improved; `round-25…:124` calibration improved; `round-12…:17` depth 4→5). Pin `63729047` is an
ancestor of fleet HEAD. Evidence-verified: `evidence/c1-before.txt` (`7118f320`, `mismatches=11`, `C1=unmet`, exit 1)
and `evidence/tip-c1.txt` (`67779aa8`, `mismatches=0`, `C1=met`, exit 0). The author's finer counter (11 mismatch
kinds) and my row-level count agree in direction and endpoint (0).

### C2 — operability: A2-07/A2-10 shapes pinned by frozen blind cases — **miss (evidence-verified; agrees with the report)**

```
git show {d6d5cb0a,b581173a}:tools/fixtures/mori-oom-killers/cases-a2-r29.json | sha256sum
→ 1c76ea1f10e08acedb82c001a875ea84a9f552acf931ca2837645d482bb9d252 (both); same hash in LOG.md by 255b7051
jq '.cases|length' → 24 ; jq -c .sources → ["S153","S154","S155"] (rows at corpus/SOURCES.md:159-161)
git merge-base --is-ancestor d6d5cb0a 8809a3fe → yes ; git diff --quiet 7118f320 8809a3fe -- tools/mori-oom-killers.py → unchanged
git log --format=%h 7118f320..b581173a -- tools/mori-oom-killers.py → cdfcf66 (only)
```

Committed evidence: `c2-freeze-selftest.txt` FAIL 11/24 (tool unchanged) → `c2-fix-selftest.txt` FAIL 21/24, older
files PASS 32/32, 32/32, 30/30; `tip-c2.txt` (`67779aa8`, case blob `cc309d8e` = tip blob): `provenance=24/24
unselected=0`, `shape_a207=3/2`, `shape_a210=6/2`, `blind_violations=20`, `a2_r29_selftest=FAIL(exit=1)`,
`C2=unmet`, exit 1. Seat C2EvidenceCheck re-derived provenance (24/24 authors ∈ CaseA207a–d/CaseA210a–d, all eight
writer reports in `w1/`) and shape counts (3/2, 6/2) statically from the committed JSON — identical. Contract A4 R3:
a nonzero blind count "is a miss, reported as one"; the counter's own `valid` conjunction also fails on the selftest.
The three residual FAILs are A2-10 non-active cases (`inactive-lone-missing-stamp`, `failed-stamped-positive`,
`not-found-earlier-stamped-positive`) failing on fields only.

### Disputed harm ruling (operability) — **not harmed**

Shape: active earlyoom, `ActiveEnterTimestampMonotonic` missing or 0, a real send, then a plain restart: before
`cdfcf66d` → `KILLER_ACTED`; after → `KILLERS_UNKNOWN` (send in `earlier_invocation_send_lines`).

- Code read (seat HarmRuling, `git show 7118f320:` vs `b581173a:tools/mori-oom-killers.py`): base `:280-287` scoped the
  whole journal when the start stamp was absent, so a send before the restart's version line counted as current
  `sigterm`; landed `:297-302` scopes from the last version line, `:465-469` counts earlier sends toward `acted` only
  for a non-active unit, `scope_known` stays false → `KILLERS_UNKNOWN`.
- The written rules decide the new answer (`git show b581173a:.ufo/waves/round-27/contract.md`, read by me):
  A2-05 (`:53`) "missing or `0` leaves the invocation unbounded: `scope_complete` false"; A2-06 (`:54`) earlier-invocation
  sends are "positive evidence (`KILLER_ACTED`) for an earlyoom that is not active, reported without a verdict change
  for an active one"; A2-07 (`:55`) "split at each version line". Round-26 `contract.md:99-101`: no positive evidence +
  "earlyoom active but `scope_complete` false" → `KILLERS_UNKNOWN`, exit 2; `:178-179` discloses the limit (A2a).
- A writer-blind frozen case pins the same split: `r29-a2-07-real-dryrun-real-missing-enter` (CaseA207c) expects
  `earlyoom.actions.sigterm: 0`, `earlier_invocation_send_lines: 1` (its `KILLER_ACTED` comes from a current-invocation
  SIGKILL, not the earlier send). Judge03 ruled a draft that moved the earlier send into `sigterm` wrong under A2-06.
- No older frozen case pins `KILLER_ACTED` for this shape (seat parse of `cases.json`, `cases-supplementary.json`,
  `cases-a2.json` at `7118f320`: the only two active-unbounded cases carry no send line), and all 94 older pins hold.
- CriticC2Verdict F4 rests on round-29 `contract.md:139-140`, which defines the counter's `shape_a207` case class, not
  the tool's scope rule. The old `KILLER_ACTED` was wrong under A2-06; the change loses no correct behavior and
  drops no evidence (the send is still reported). Ruling: **not harmed**; the lost confidence is the disclosed A2a limit.

## 3. Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| calibration | improved | C1 re-measured 5/6 → 0/6 rows (author counter 11 → 0), scores held |
| operability | unchanged | C2 miss (FAIL 21/24, `blind_violations=20`); tool change not harmed (ruling above); score 7 held |
| coverage | unchanged | no surface change; SKILL.md, PROVINCE.md, `corpus/knowledge/*` untouched |
| depth | unchanged | no knowledge entry change; +3 SOURCES rows feed C2 only |
| freshness | unchanged | no re-pin or recheck change; no older SOURCES row changed |
| adjacency | unchanged | PROVINCE untouched; no sibling file touched (kake stray left untouched) |

No-harm audit: `git diff 7118f320 b581173a -- SCORECARD.md` removes only the six Axes rows, replaced with identical
scores; everything else appended. `LOG.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, `corpus/lessons/round-28.md`:
`git diff … | grep '^-[^-]'` → no removed lines (append-only held). Retention metric 4 at base (`w1/RetentionBase.md`)
= 4 at `67779aa8` (`evidence/tip-retention.txt`). Tool diff: all hunks inside `read_inputs`; no CLI, field or verdict
vocabulary change.

## 4. Discernment spot-check (`corpus/lessons/round-29.md` `## Gate`)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S155 earlyoom `ca2251fc` dry-run | admit | `curl -sSL https://github.com/rfjakob/earlyoom/commit/ca2251fcd222af8c857aec4a26e182cf5f9c596e.patch \| grep -n 'args.dryrun && sig != 0'` | agree | `35:+    if (args.dryrun && sig != 0) {` (re-run by me); seat: HTTP 200, sha `893e238e…` matches, `:21-22`, `:71`, `:79-82` as rowed |
| S154 entry-object monotonic stamp (five systemd v262 files) | admit | `curl -sSIL` + `sha256sum` each raw v262 URL | agree | all HTTP 200, shas match the row; `journal-def.h:120 le64_t monotonic;`, `sd-journal.c:2839-2841` `VALID_MONOTONIC` guard, `journald-socket.c:153` `__MONOTONIC_TIMESTAMP=` |
| S153 `sd_journal_get_realtime_usec.xml` | admit | raw v262 URL | agree | HTTP 200, sha `dd224fc9…` matches; quote at `:61-63` verbatim |
| S154 `src/libsystemd/sd-journal/journal-export.c` | reject (404) | `curl -sS -o /dev/null -w '%{http_code}' https://raw.githubusercontent.com/systemd/systemd/v262/src/libsystemd/sd-journal/journal-export.c` | agree | `404` (re-run by me) |
| S153 `man/sd_journal_get_monotonic_usec.xml` | reject (404) | raw v262 URL | agree | HTTP 404, body `404: Not Found` |
| S155 `testsuite_cli_test.go` ; `kill.h` | reject (does not carry the fact) | raw URLs + `grep -in -e dryrun -e version` | agree (decision); wording defect | test file: no match; `kill.h:36-37` does match `dryrun` (`/* Flag --dryrun was passed */ bool dryrun;`) — a flag declaration, not the behavior fact, so the reject stands, but the row's "returned no line in either file" is false (R2) |

SOURCES rows re-opened: S153–S155 (`corpus/SOURCES.md:159-161`); every quote ≤25 words by `wc -w` (22, 24, 8, 10, 16,
2, 3 …); S154 and S155 quotes verbatim at the cited location; S153 near-verbatim (`<constant>NULL</constant>`
flattened). Two word-count labels are one high (journal-upload-journal.c labelled 11, `wc` 10; patch guard labelled
17, `wc` 16) (R3). Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → ten W04
(S035, S037, S073–S076, S147–S150; none of S153–S155), `mori ok`, exit 0 — matches `evidence/census-end.txt`.

Spot-check: 6 agree, 0 disagree (decisions); 1 wording defect.

## 5. Trend verdicts

- **expansion: improved** — +3 tier-A rows (152 → 155), each re-opened by this closure with hashes/HTTP status
  reproduced (§4); census ok with no new warnings.
- **quality: improved** — the held self-assessment table now matches the closure record (5/6 → 0/6 rows, re-measured);
  the tool change corrects 10 frozen blind cases (11/24 → 21/24) with all 94 older pins held and, per the ruling, fixes
  a verdict the lane's own A2-06 rule made wrong. The C2 miss stays a miss; this grade rests on C1 and the not-harmed
  tool change, not on C2's after-value.
- **discernment: improved** — 6/6 sampled gate decisions agree on re-open; reject rows now carry ids and reasons;
  pre-data critics overturned both counters (A1–A4) and the L1 reported its own miss rather than withdrawing it.

## 6. Ruling

Status **ok** (real report, all hashes resolve and are ancestors, pushed, prompt conformant). **Not admitted**:
C2 did not verify (declared after-value `C2=met` not reached). No axis harmed → `rejected-honest-stop`.

## 7. Routed defects (lane owes next round)

- R1 `tip_receipts=unmet`: QUALITY 84 check (`.ufo/waves/round-28/check-tip-receipts.sh b581173a 29`) reads LOG.md and
  the lesson, but `tip-c1.txt`/`tip-c2.txt` are cited only in `SCORECARD.md:1796-1797`. Cite receipts where the check
  reads (append before the receipts-only batch) or amend the check pre-data.
- R2 Gate S155 reject reason (`round-29.md` `## Gate`, testsuite_cli_test.go ; kill.h): "no line in either file" is false
  for `kill.h:36-37`; append a correction (decision unaffected).
- R3 SOURCES S154/S155 word-count labels one high (11 vs 10, 17 vs 16); append a correction.
- R4 C2 residual: the three A2-10 non-active cases (Judge11–13 tool errors, declined this round) and Judge02's
  `unclear text` case remain open; carry to a pre-declared claim.
- R5 A4 blindness check prints 20 hits all adjudicated false positives (`w2/AdjudicateBlindHits.md`): the matcher cannot
  separate writer vocabulary from tool leakage; fix and self-test it before the next blind wave.
- R6 The disputed shape (active, start stamp missing/0, real send, plain restart → `KILLERS_UNKNOWN`) has no frozen case
  of its own; pin it and state the A2a limit for it in SKILL/knowledge so the next reader does not re-dispute it.
- R7 Carried: PROVINCE stale in five places (`w1/ScoutShonen.md`); `SKILL.md:661` unqualified citation.

Operator note (promotion is operator-owned): SHONEN box 2 (end-to-end task, `LOG.md:1838-1846`, receipt
`.ufo/waves/round-26/evidence/c2-live-run.txt`) looks fully checkable by a non-author; box 3 carries a non-author run
on record (ScoutShonen `PASS (134 cases)`).
