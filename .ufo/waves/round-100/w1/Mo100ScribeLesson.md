# Mo100ScribeLesson — lesson material draft for `corpus/lessons/round-100.md`

Role: scribe (lesson material). Lane: mori. Round 100, wave w1, attempt 1.
Entering `d1bd1b339b894de0249b0f60702dff9962da88d9` · freeze `9579cff6cfab2f06b1918e54aec4a5553b705a9c` ·
landing `5e2bcf2c487e377b51287c587144bdde5b233f8f`.
Contract read first, not edited: `.ufo/waves/round-100/contract.md`.

**Scope note.** This seat writes only this file and its scratch. The draft below is *draft material for the
integrator*; it is not landed into `corpus/lessons/round-100.md` by me. A round-100 lesson draft already exists
in the lane working tree as an **untracked** file (`corpus/lessons/round-100.md`, `git status` → `?? corpus/lessons/round-100.md`,
not written by this seat, not edited by it) and `corpus/QUALITY.md` carries an **uncommitted** modification
adding rows 213–214 (`git status` → `M corpus/QUALITY.md`; `git show 5e2bcf2c:corpus/QUALITY.md | grep -c '^21[34]\.'` → `0`).
Both are reported as observed, not touched.

---

## 1. Draft material — `## Mistakes` rows (CORPUS: class · evidence · captured-by · fix)

| # | class | evidence | captured-by | fix |
|---|---|---|---|---|
| 1 | number-drift | Rows **S581** (stated 10, quote has 9; stated 15, quote has 14), **S582** (14→13), **S583** (14→13), **S584** (17→15; **22→26 — the failed-call sentence is 26 words, over the 25-word cap**) and **S634** (17→18) state a word count their own quote does not have. Evidence pointer: `.ufo/waves/round-100/evidence/before-c2.txt` (`uncorrected S581 10->9,15->14` / `S582 14->13` / `S583 14->13` / `S584 17->15,22->26` / `S634 17->18`, `uncorrected=7`); quotes and labels read from `corpus/SOURCES.md` rows S581–S584, S634 at `d1bd1b33`. S581/S582 landed at r70 (`de431a74`, 2026-11-01), S583/S584 at r71 (`3627fac0`, 2026-11-01); the r72 round (`d2f55d8c`) wrote the *corrected* values into **new supersedes rows S585/S586/S587** (`corpus/lessons/round-72.md` §"S585 … corrects the two misstated counts 22→26 and 17→15"; "S586 corrects two S581 word-count labels 10→9 and 15→14"; "S587 corrects the S582/S583 `:829` definition label 14→13") — CORPUS rule 2 (fleet `CORPUS.md` §Rules, item 2) allows exactly that and forbids editing the stating row, so **the rows that state the counts kept the wrong labels** until the r100 landing. I re-derived the labels and the whitespace counts of all eight mismatched quotes from the entering tree independently of the frozen counter: S585/S586/S587 now carry matching counts, S581–S584/S634 do not. | **none, for 30 rounds, in the stating rows.** The r99 closure found **one** instance by hand — S634 17 vs 18 — (`corpus/lessons/round-99-verifier-spotcheck.md` §3 "it has **18** words (`wc -w`)"; routed as D1). The standing label check **QUALITY 90** (`corpus/QUALITY.md:526`) is a manual command not wired to any round's counted run; run by me on the entering tree it prints `word_labels=22 mismatched=4` exit 1 — it catches S581's `:70-71` 15, S584's 17 and 22, S634's 17, and **misses S581's 10, S582's 14 and S583's 14**, because its regex (`Q + r"\s*\((\d+) words?\)"` / `r"\((\d+) words?\)\s*:\s*Q"`) requires the count adjacent to the quote while those three labels are written `"quote" (`locator`, N words)` — the locator breaks the adjacency. | QUALITY 213 (working tree, uncommitted): a number a row states about its own quote is computed by a command when the row is written and the command is named; a wrong count is answered by an appended, named correction in the same row, never by rewriting the stated text. Landing shape (verified in `corpus/SOURCES.md` at `5e2bcf2c`): four appended blocks, `[r100 word-count correction: 10→9, 15→14; counted by whitespace]`, `[r100 word-count correction: 14→13; counted by whitespace]` ×2, `[r100 word-count correction: 17→15, 22→26 (over the 25-word cap); counted by whitespace]`, `[r100 word-count correction: 17→18; counted by whitespace]`. **Shown able to fail:** the frozen counter on the entering tree → `C2=unmet stated=58 mismatches=7 uncorrected=7 spurious=0 altered=0 census=ok checks_failed=mismatch`, exit **1** (I re-ran it, rc=1). |
| 2 | breaking-class-set | The round-17 fixture gate grades the tool's `totals` by **exact key-set equality**: `tools/mori-round17-seat-regressions.py` `validate_totals()` → `if set(value) != CLASS_SET: return None, "totals_keys"`, with `CLASSES` (lines ~194–204) and `CLASS_SET = frozenset(CLASSES)`. The entering gate carries **eight** classes; the landed tool carries **nine** (`dead_auth` added at `tools/mori-seat-terminal.py` `CLASSES`). So adding a class to the tool turns a registered gate red until the gate's class set is updated in the same commit — the gate is a *breaking-change detector*, not a classifier test. Evidence pointer: control **K7** in `.ufo/waves/round-100/evidence/controls-r100.txt` (`r17gate=rc1 … checks_failed=r17gate`); `SKILL.md:173` r17 registry row now states "the class set carries `dead_auth` since round 100, so the gate refuses a tool without it (`totals_keys`)". | the pre-freeze control set (K7: entering gate on the landed tool → `r17gate=rc1`); QUALITY 214 (working tree, uncommitted) | the class lands together with every in-lane consumer of the exact class/key set (QUALITY 214); the landing updates the gate's `CLASSES` in the same commit and re-runs the 66 fixture cases. **Shown able to fail:** (a) control K7; (b) my own independent run — entering gate + landed tool → `GATE mismatch: 5/66 cases matched`, rc **1**, with `totals_keys` in 181 case reasons of `run-manifest.json`; (c) landed gate + landed tool → `GATE ok: 66/66`, rc **0**. |
| 3 | misfiled-death-cause | On the two days before the round the census filed **190** seats as `dead_error_other`, of which **187 carry auth evidence** — 149 with `status=401`, 32 with no status but an auth spelling, 6 with `status=403` — and **3 with neither** (the real unknowns) were filed in the same bucket next to them. Evidence pointer: `.ufo/waves/round-100/evidence/live-errors-prefreeze.txt` (`files_read 4812 window_days 2.0`; `r99_dead_error_other 190 of_which_auth_evidence 187`; the per-status lines `149 status=401 … auth-evidence`, `32 status=None … auth-evidence`, `6 status=403 … auth-evidence`, `3 status=None … -`), counts only, no transcript text. | **none** — the class set had no auth bucket; the operator diagnosed the provider outage by hand from transcripts (contract §C1, "the orchestrator diagnosed the provider outage by hand"). | C1's `dead_auth` class, read **after** Z.AI codes, quota evidence and rate evidence (so it only reclaims seats the r99 rules called `dead_error_other`): HTTP 401/403 or one of `permission_denied`, `PERMISSION_DENIED`, `unauthenticated`, `UNAUTHENTICATED`, `authentication_error`, `permission_error`; grounded in S637, S638 and the re-opened S221 (`corpus/knowledge/seat-auth-deaths-r100.md` §"Rule (as landed)" 1–5). QUALITY 214. **Shown able to fail:** `.ufo/waves/round-100/evidence/before-c1.txt` → `C1=unmet cases_ok=23/50 families_failed=A1-auth-status,A2-auth-spelling,A3-auth-escaped,A4-auth-status-composed,A5-auth-spelling-composed,Z1-zai-unmapped-auth … checks_failed=battery,registry,sourced`, exit 1 (I re-ran the frozen counter on the entering tree with seed 100 and got the same line, rc 1); controls K1–K5 keep the precedence honest (`K4 … families_failed=N1-quota-wins,N2-rate-wins`). |

### Additional row I can trace (not required by the seat brief, offered for the integrator)

| # | class | evidence | captured-by | fix |
|---|---|---|---|---|
| 4 | number-drift (own draft) | The round-100 draft rows for S637/S638 were first typed as "11 words" for two 12-word quotes and corrected **before** the freeze; the frozen candidate already carries 12 (`git show 9579cff6:.ufo/waves/round-100/candidate/apply-c1.py` → `(12 words, raw lines 646-647)`, `(12 words, raw line 88)`), and I count both quotes at 12 by whitespace. Evidence pointer: `corpus/QUALITY.md` (working tree) row 213. | the L1 counting the drafts before freezing | QUALITY 213's "computed by a command when the row is written, and the command is named"; the C2 counter reads new rows too (`stated=60` at landing vs `stated=58` entering). **Shown able to fail:** an 11 in either row makes `count-c2.py` print `uncorrected=1` (the counter's own mismatch rule; not re-run here — see §5 unrun list). |

---

## 2. Draft material — `## Gate` table skeleton (S637, S638, S221 re-open, old→new used-by)

Rows written this round per CORPUS rule 1 (fleet `CORPUS.md` §Rules item 1): URL, access date, a ≤25-word located
quote with its location grounding `teaches`. Every byte below was re-read from the pinned copies in
`corpus/evidence/sources-r100/`.

| row | URL | access (UTC) | located quote (≤25 words) | decision |
|---|---|---|---|---|
| S637 | https://connectrpc.com/docs/protocol/ — pinned `corpus/evidence/sources-r100/S637-connect-protocol.html` | 2026-11-05T23:00:13Z, HTTP 200, 148033 B, sha256 `55d644c62a7d094ec836dbc4f9fbcb1f5b0cca27b675ba68902568fef9ca2578` | "use unauthenticated if the user can’t be identified or presents invalid credentials." (12 words, raw lines 646-647, tags stripped) | admit, mined, tier A |
| S638 | https://grpc.github.io/grpc/core/md_doc_statuscodes.html — pinned `corpus/evidence/sources-r100/S638-grpc-statuscodes.html` | 2026-11-05T23:00:13Z, HTTP 200, 18133 B, sha256 `95459b760813d4cde87ad3c449753ff55bbd138cdf6c5bfdfacf6566b763e3c4` | "PERMISSION_DENIED must not be used for rejections caused by exhausting some resource" (12 words, raw line 88) | admit, mined, tier A |

Grounding I re-located in the pinned copies myself (tags stripped):

| row | raw line | text |
|---|---|---|
| S637 | 646 | "…use unauthenticated if the user can’t be identified or presents invalid credentials." (the code-choice paragraph, lines 645-650) |
| S637 | 711 | HTTP→code table: "401 Unauthorized unauthenticated 403 Forbidden permission_denied" (also 429→unavailable) |
| S638 | 88 | "PERMISSION_DENIED must not be used for rejections caused by exhausting some resource" |
| S638 | 90 | "RESOURCE_EXHAUSTED … Some resource has been exhausted, perhaps a per-user quota…" |
| S638 | 106 | "UNAUTHENTICATED … The request does not have valid authentication credentials for the operation." |

Row changes logged old→new (CORPUS rule 2: only `status`, `recheck`, `used-by` change in place):

| row | field | old (at `d1bd1b33`) | new (at `5e2bcf2c`) | evidence |
|---|---|---|---|---|
| S221 | `used-by` | `corpus/knowledge/source-drift-hardening-r37.md` | `corpus/knowledge/source-drift-hardening-r37.md, corpus/knowledge/seat-auth-deaths-r100.md` | `git show d1bd1b33:corpus/SOURCES.md` vs `git show 5e2bcf2c:corpus/SOURCES.md`, row S221 (diff touches only this cell) |
| S221 | `status` | mined | mined (unchanged) | same diff |
| S221 | `recheck` | 180d | 180d (unchanged) | same diff |
| S221 | `opened` | 2026-10-23 | 2026-10-23 (unchanged) | same diff |
| S637 | `used-by` | — (new row) | `corpus/knowledge/seat-auth-deaths-r100.md` | row S637 at `5e2bcf2c` |
| S638 | `used-by` | — (new row) | `corpus/knowledge/seat-auth-deaths-r100.md` | row S638 at `5e2bcf2c` |
| S581, S582, S583, S584, S634 | anchor cell | stated count without correction | stated count **plus** the appended `[r100 word-count correction: …]` text | `git diff d1bd1b33 5e2bcf2c -- corpus/SOURCES.md` |

S221 re-open grounding (pinned copy `corpus/evidence/sources-r100/S221-rfc9110-r100.txt`, sha256
`21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a`, 502941 B; §15.5.2 heading at raw line 7548,
§15.5.4 at 7569):

| raw line | text | section |
|---|---|---|
| 7551 | "been applied because it lacks valid authentication credentials for" | §15.5.2 401 Unauthorized |
| 7572 | "the request but refuses to fulfill it." | §15.5.4 403 Forbidden |

Rejections worth carrying into the Gate section (from the contract and the landed rows):
a second RFC 9110 row for §15.5 (the URL is already S221 — a within-scope duplicate URL, census W04), and
Connect's HTTP→code table as the rule for 429 (it maps 429 to `unavailable`; the lane keeps 429 as rate evidence).

---

## 3. Measurements behind the verdicts (frozen instruments, replayed by me)

Frozen instruments unchanged between freeze and landing —
`git diff --stat 9579cff6 5e2bcf2c -- .ufo/waves/round-100/count-c1.py .ufo/waves/round-100/count-c2.py .ufo/waves/round-100/controls-r100.py .ufo/waves/round-100/contract.md .ufo/waves/round-100/candidate/` → **empty**.

| check | command | output | rc |
|---|---|---|---|
| C1 entering | `git archive d1bd1b33 \| tar -x -C $S/before`; `python3 .ufo/waves/round-100/count-c1.py --root $S/before --work $S/w-before --seed 100` | `C1=unmet cases_ok=23/50 families_failed=A1-auth-status,A2-auth-spelling,A3-auth-escaped,A4-auth-status-composed,A5-auth-spelling-composed,Z1-zai-unmapped-auth selftest=ok r17gate=ok registry=unmet sourced=unmet checks_failed=battery,registry,sourced seed=100 tool_rc=1` | 1 |
| C1 landing (fresh seed 7) | `python3 .ufo/waves/round-100/count-c1.py --root $S/landing --work $S/w-landing --seed 7` | `C1=met cases_ok=50/50 families_failed=- selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=- seed=7 tool_rc=1` | 0 |
| C2 entering | `python3 .ufo/waves/round-100/count-c2.py --root $S/before --repo …/mori-shokunin --list` | `C2=unmet stated=58 mismatches=7 uncorrected=7 spurious=0 altered=0 census=ok checks_failed=mismatch base=d1bd1b33` | 1 |
| C2 landing | `python3 .ufo/waves/round-100/count-c2.py --root $S/landing --repo …/mori-shokunin --list` | `C2=met stated=60 mismatches=7 uncorrected=0 spurious=0 altered=0 census=ok checks_failed=- base=d1bd1b33` | 0 |
| r17 gate, landing gate + landing tool | `python3 tools/mori-round17-seat-regressions.py --tool tools/mori-seat-terminal.py --fixtures .ufo/waves/round-17/fixtures/seat --output $S/gate-out` | `GATE ok: 66/66 cases matched` | 0 |
| r17 gate, **entering** gate + landing tool | same, with `$S/before/tools/mori-round17-seat-regressions.py` | `GATE mismatch: 5/66 cases matched`; `totals_keys` in 181 case reasons | 1 |
| tool selftest, landing | `python3 tools/mori-seat-terminal.py --selftest` | `{"arms":53,"passed":53,"finding_id":"SELFTEST_OK","schema":"mori-seat-terminal-selftest-v1"}` | 0 |
| row counts | `git show <rev>:corpus/SOURCES.md \| grep -cE '^ {0,3}\| *S[0-9]{3,}'` | `d1bd1b33` → 408 · `5e2bcf2c` → 410 | — |
| census before | `.ufo/waves/round-100/evidence/census-before.txt` | `mori ok …/corpus/SOURCES.md`, `exit=0`, 44 `W04` | 0 |

---

## 4. Findings the integrator should route (detection and report only; I changed nothing)

**F1 — the r17 fixture gate cannot see the new class's behaviour.** `.ufo/waves/round-17/fixtures/seat/expected.json`
has 66 cases and **zero** mention `dead_auth` (`grep -c dead_auth` → `0`). I patched a scratch copy of the landed
tool to empty `AUTH_STATUSES` and `AUTH_TOKENS` (the whole auth rule) and ran the landed gate against it:
`GATE ok: 66/66 cases matched`, rc **0** — while the same mutant's own `--selftest` failed
(`arms 53 passed 51`, failures `auth-401-status` and `auth-connect-permission-denied-no-status`, rc **1**).
So the gate checks that the key set is exactly right, not that the new class classifies anything; the
classification is carried by the tool's selftest and the C1 battery, not by the fixture gate. Route: a fixture
case (or an explicit note) so the registered gate is not mistaken for coverage of `dead_auth`.

**F2 — QUALITY 90 and the r100 correction form disagree on the same bytes.** The QUALITY 90 check
(`corpus/QUALITY.md:526`) reads `(N words)` labels only. Run by me on the **landing** tree it still prints
`word_labels=22 mismatched=4` exit **1** — the same four it prints on the entering tree — because the r100 fix
*appends* `[r100 word-count correction: …]` beside the original label instead of rewriting it (CORPUS rule 2).
`count-c2.py` accepts the appended form (`uncorrected=0` at landing) while QUALITY 90 does not. Route: QUALITY 213
should say which reading binds, or QUALITY 90 should be taught the correction form — otherwise the standing
criterion stays red on an admitted corpus.

**F3 — the S221 re-open's `used-by` grew but the row's own anchor cell did not.** At `5e2bcf2c` the S221 row's
anchor cell still reads "§15.4:7230-7252" and carries only the 3xx quote, while the new consumer
`corpus/knowledge/seat-auth-deaths-r100.md` cites S221 for §15.5.2 (401, raw 7551) and §15.5.4 (403, raw 7572).
Both quotes are present in the pinned copy `corpus/evidence/sources-r100/S221-rfc9110-r100.txt` and the knowledge
entry states them with line numbers, so the grounding exists — but the row that claims to be the source does not
locate the text it is now used for. CORPUS rule 2 forbids editing the anchor cell in place, so the route is a
supersedes row (or a rule decision), not an in-place edit. Route to the L1.

**F4 — the round's own census close is missing.** `.ufo/waves/round-100/evidence/` holds `census-before.txt`
(`mori ok`, 44 `W04`, rows 408) but **no `census-after.txt`**; the working-tree lesson draft's "Frontier step —
census" section correspondingly has only the round-start half. I did not run a census (the census writes to the
lane registry scope and is the L1's step); named here as an unrun artifact, not as a defect of any claim.

**F5 — a stale class-count sentence survives in the gate's own docstring.** `tools/mori-round17-seat-regressions.py:80`
still says "the tool's `totals` must carry exactly the **eight** classes" while `CLASSES` now holds **nine**
(`dead_auth` added at the landing). The prose is not machine-checked, so it did not turn anything red; it is the
same number-drift class the round's C2 claim is about, in the tool rather than the registry. Route to the L1
(correct in place: the gate file is not append-only). I did not edit it — the tool tree is out of this seat's scope.

---

## 5. Unrun / out-of-scope (named, not implied)

- **Not run:** the frozen `controls-r100.py` re-execution (I read the committed receipt
  `.ufo/waves/round-100/evidence/controls-r100.txt`, `CONTROLS_DONE unexpected=0`, 17 rows `AS_EXPECTED`; I did not
  re-run it).
- **Not run:** the round-100 census end-of-round (`census-after.txt` does not exist; see F4).
- **Not run:** any live re-read of `~/.omp/agent/sessions` (the private-transcript rule; I used only the committed
  counts-only receipt `.ufo/waves/round-100/evidence/live-errors-prefreeze.txt`).
- **Not run:** the counter-c2 red case for the "11 words" draft row (Mistake 4's "shown able to fail"); the frozen
  candidate already reads 12 and both quotes count 12.
- **Not run:** mutation/battery testing of the landed `dead_auth` rule beyond the two-arm mutant I built to make
  F1 visible (scratch only, discarded).
- **Not touched:** `corpus/`, `tools/`, `SKILL.md`, `PROVINCE.md`, `LOG.md`, `SCORECARD.md`, the contract, the
  counters, the receipts, `MANIFEST.json`, the fleet root, any sibling lane; no git/jj mutation anywhere; no
  `sudo`; no pacman; no tool install was needed (everything used is already in the lane: `python3`, `git`).
- **Scratch:** `/fast/scratch/hyaku/mori-r100/Mo100ScribeLesson` — removed before finishing; every number in this
  report is reproducible from the committed lane files and the commands quoted above.

---

## 6. Lesson-material summary for the integrator

- The frozen predicates hold as reported: C1 `23/50 → 50/50` (replayed at seed 100 and seed 7) and C2
  `uncorrected=7 → 0` (replayed on the entering and landing trees).
- Three mistakes are ready to carry as `## Mistakes` rows with the evidence pointers, captured-by and
  able-to-fail demonstrations given in §1: the 30-round word-count drift in S581–S584/S634 (with the new finding
  that r72 *had* the right values but CORPUS rule 2 pinned them to new rows, leaving the stating rows wrong, and
  that QUALITY 90's regex misses locator-bearing labels), the r17 gate's exact key-set equality as a
  breaking-change detector, and the 187-of-190 auth deaths the census filed next to 3 real unknowns.
- Five findings (F1–F5) are routed above as observations for the L1; none of them changes a frozen predicate.
