# Mo59Connector56 — connector pattern scan (round 59, read-only)

Scope: compare how kama, kotoba and chousa structure depth-entry claim grammar and frozen counters; report patterns mori should or should not adopt; report overlap and refusal boundaries. No edits, no commits, no VCS mutation, no fleet or sibling writes. Frozen bytes read as given: contract.md, count-c1.py, count-c2.py (freeze 60b3a76a; entering 2b9f0397).

Commands run were read-only (`grep`, `ls`, `git log`/`git show`/`git cat-file`, and in-memory Python regex checks on literal strings). No counter was executed and no fixture was created. My scratch dir `$HYAKU_SCRATCH/mori-r59/Mo59Connector56` was created empty and removed before yield.

## 1. Frozen claim grammar: what peers do

Measured with `grep -l` over `corpus/knowledge/*.md` in each lane (entry counts = knowledge files):

| lane | entries | `coverage-map:` | `Quote: \`` claim lines | `pin <sha64>` | `recheck:` | `verified-at:` | Limits / "does not establish" heading |
|---|---|---|---|---|---|---|---|
| mori | 71 | 19 | 1 (driver-events-r58.md) | 0 | 62 | 64 | 18 |
| kama | 38 | 1 | 0 | 0 | 38 | 38 | 8 |
| kotoba | 64 | 0 | 0 | 0 | 31 | 31 | 25 |
| chousa | 82 | 0 | 0 | 0 | 78 | 81 | 18 |

Findings:

- **The quote-claim grammar is mori-only.** No kama, kotoba or chousa knowledge entry uses `Quote: \`` or a `pin` binding. Mori's only prior instance is `driver-events-r58.md` K1–K11 (`- **K1** — … Quote: \`(…)\` (tools/mori-driver-liveness.py:55).`). That form has no pin. I checked it against the frozen CLAIM regex in count-c2.py:78-80 (in-memory string): `False`. The new grammar therefore forks mori's own last depth entry. This is by design, but any lesson must say so, and r58 cannot be re-verified by the round-59 counter. Do not retrofit r58.
- **kama** (`battery-execution-evidence.md`) uses prose plus an opening frontmatter line `source: S517 — <title>, <URL> (anchor …); code <path> @ <rev>` and a `## What it establishes / does not establish / Reuse boundary` shape. No claim IDs and no quote grammar. Its `recheck:` is a command (`python3 tools/round58-c1-counter.py …`).
- **kotoba** (`sibling-overlap-census-round74.md`) carries its claims in tables. Its checker reads a `path:line` plus quote, not a pinned digest; `verifiers/check_sibling_reread.py --rev <rev>` re-pins at a commit rather than at a copy sha. Its `## Limits` section says the counter "measures pins, cells, quotes, deltas and evidence lines; it does not measure judgement."
- **chousa** (`normative-reference-chain-china-r57.md`) uses one `source:` line per S-id (five lines, lines 3-7), then `verified-at`, `recheck: 180d` (time-based), `ground`, `adopted`, and `## Observation / Inference / Unknown / Limits` sections.

## 2. Frozen-counter structure: what peers do

- **kotoba** `verifiers/check_sibling_census.py` is a persistent verifier reused across rounds (r49 and r74 both point at it). Its docstring states the R2 lesson: a counter must FAIL on empty or false content, because "an empty table, a quote never in the file it is attributed to, a commit that does not hold the bytes" otherwise pass vacuously. Mori's C2 meets this with `claims_min`, `span:`, `pin:` and the 12 hostile trees.
- **kama** round counters are round-local under `.ufo/waves/round-N/c1|c2/` and `frozen/`. `c2/survivors.py` (docstring lines 1-25) classifies mutants as `site_missing`, `site_ambiguous`, or `stillborn` and counts each as NOT killed, "never skipped." Kama's ConnectKake advice (`.ufo/waves/round-17/build/advice/ConnectKake.md:112-113`) cites the convention "name the mutant/control population and the 0/1/2 exit map (kama QUALITY.md:10, :18; kama SKILL.md:303-306)."
- **mori** (round-59 frozen): output is a single `C1=…`/`C2=…` line with `key=value` tokens, exit 0 met / 1 unmet / 2 setup, `--scratch` and `TMPDIR` honored, `git show` / `ls-tree` only. This matches kama's 0/1/2 map. Mori's counters are the most hermetic of the four (sha pin on the tool, committed hostile trees, `git show` only). Kotoba's `git`-recompute is weaker on hermeticity but cheaper to maintain across rounds.

## 3. Mechanical checks on the frozen grammar (in-memory, literal strings only)

- **Multi-ID `source:` lines are invisible to the rows arm.** `SID = re.compile(r"source:\s*(S\d+)")` (count-c2.py:82) with `findall` on `source: S022 (https://x), S023 (https://y), S018 (https://z)` returns `['S022']`. `S023` and `S018` are never checked against the registry. Kotoba's census line 1 has exactly this shape. Chousa's one-`source:`-per-ID form is the one the frozen counter sees in full. Recommendation for the depth entry: one `source:` line per S-id (chousa form). This is prose guidance only; the frozen SID regex cannot change.
- **Predicate scope.** The rows arm checks only S-ids on `source:` lines (count-c2.py:161-190). An S-id cited in claim body text (for example `(S127, S131)` in chousa's body) is unchecked. Mori's entry should keep every cited S-id on a `source:` line, or accept that the body citation is outside the counter.
- **Quote floor.** The frozen floor is `len(q.encode()) < 3` (count-c2.py:151). Kotoba's base sourced-quote rule requires six or more words within two lines of `path:line` (census Limits, "Quote shape"). A three-byte quote passes mori's counter but says little. Recommendation (prose, not counted): quote at least six words per claim, following kotoba.
- **Claim lines must be single-line.** The CLAIM regex is anchored `^…\s*$` (count-c2.py:78-80). A wrapped K-line fails and is reported as `grammar:` (count-c2.py:121). Keep each claim on one line.
- **Frontmatter window is the first ten lines** (count-c2.py:112). Five source lines plus `verified-at`, `recheck` and `coverage-map` fit (8 lines). Adding a title block above frontmatter can push the keys out of the window.

## 4. Patterns: adopt / do not adopt

Adopt (prose-level, not counted by the frozen counter):

1. One `source:` line per S-id (chousa; see §3).
2. A `## Limits` or `## What it does not establish` section. Present in 25/64 kotoba, 18/82 chousa, 18/71 mori, 8/38 kama entries. For the depth entry, state what a byte-exact pin proves (the quoted bytes exist in that copy at that line or offset) and what it does not (that the schema verdict is semantically right, or that any wave settled).
3. Kotoba's disclosure that a counter "does not measure judgement," written into the entry's limits.
4. Kotoba's six-word quote floor (§3), applied voluntarily.

Do not adopt:

1. Kotoba's commit-cell git recompute as the primary binding. Mori's copy-sha pin is more hermetic and is already frozen.
2. Chousa's time-based `recheck: 180d`. Mori's `recheck:` should stay a command pointing at the frozen counter (`python3 .ufo/waves/round-59/count-c2.py R`).
3. Kotoba's cross-round persistent verifier for claim-bound counters. Frozen per-round counters are the contract's immutability rule.
4. `coverage-map:` as a cross-lane convention. It is mori-only (19/71 mori, 1/38 kama, 0 kotoba, 0 chousa). Frozen C2 requires it, so it stays for mori readers; peers will not recognise it.

## 5. Overlap and refusal boundaries

- **Settlement vocabulary collision (highest-risk boundary).** `tools/mori-wave-settlement.py` (round 20) already reports `settled`/`partial`/`unsettled`/`no-spawn` over `.ufo/waves/*` dispatch and report presence. `PROVINCE.md:145-154` says its `settled` is "report-file settlement only, not kumitate's lifecycle settlement or result acceptance." `PROVINCE.md:162-181` (Round21 correction) says "retained loss is not lifecycle settlement." C2 adds `tools/mori-settlement-scan.py` with verdict `SETTLEMENT_SCAN_OK`/`FAIL`. The name and verdict both reuse the word "settlement." The depth entry must restate the PROVINCE:150/153/178-181 refusal and must not describe the C2 verdict as settlement, acceptance, or completion.
- **Results-artifact ownership (kumitate).** `kumitate-shokunin/scripts/inline-dispatch-evidence.mjs:261` reads `${wave}-results.json` as kumitate's gate. `PROVINCE.md:65` (mori's Adjacent row for kumitate) says kumitate owns "wave plan/run/record/collect semantics; mori passively grades `.ufo/waves/*` filesystem settlement state. No conflicting settlement contract was found." C2's scanner is a second reader of the same artifact family, with its own schema copy: `ROLES` (`tools/mori-settlement-scan.py:39-40`) and `MEMBER_KEYS` (`:41`). Refusal: mori reports schema drift (the r53 FAIL) to kumitate and does not change the results schema. The entry should cite kumitate's gate as the owner of acceptance.
- **Role enum agrees with this wave.** The round-59 spec (`.ufo/waves/round-59/w1-spec.json`, 64 items, key `role`) has roles reviewer 20, critic 10, mutation-tester 8, executor 8, scribe 4, scout 4, revenger 4, connector 2, sentinel 2, simplifier 2. Every role is in the scanner's `ROLES`. Attack share is reviewer+critic+mutation-tester+sentinel = 40/64, as the contract states. The scanner's selftest (`:181`) uses `agent="planner"` as a negative case, which matches "planner is not a validator role."
- **Sourcing discipline (chousa, kotoba).** Chousa owns research method and citation discipline; kotoba owns skill craft and rejects sibling-scope overlap. The depth entry cites only mori's own S-rows and does not restate those methods. No overlap beyond citation style.
- **Kama, tsukuroi, kagi.** No C2 or C1 claim touches endpoint health, host OS, or secrets. No overlap found.

## 6. Repo state observed

- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse --show-toplevel` → the lane path. Lane HEAD `8ff344ff` (2026-10-28 02:50:48), branch `master`.
- Entering `2b9f0397` is an ancestor of HEAD. `git log --oneline 2b9f0397..HEAD` shows three commits: `8ff344ff` (validated w1 dispatch payload, 64 seats, v2), `60b3a76a` (freeze amendment), and `ccfd554e` (freeze contract, C1/C2 counters, tools, fixtures). The two tools are absent at `2b9f0397` and present at `60b3a76a`, consistent with the contract's "before" control.
- `tools/mori-settlement-scan.py` working-tree SHA-256 = `4c04bf2170b0484192dd157ee04851e8243e030c54046c5e8806d46eea5ac9a9`, equal to the frozen PIN. Tracked; no status change.
- Untracked under round-59: `.ufo/waves/round-59/assimilation/`, `.ufo/waves/round-59/w1/`, `.ufo/waves/round-59/w1-dispatch.stderr`, `.ufo/waves/round-59/w1.ready.dispatched`.

## 7. Verification

Not run by this seat. The main agent should run `count-c1.py` and `count-c2.py` after landing, with explicit `--scratch`. The rows-arm gap in §3 should appear in the round lesson as a known limit.

## 8. Tool installs

None.
