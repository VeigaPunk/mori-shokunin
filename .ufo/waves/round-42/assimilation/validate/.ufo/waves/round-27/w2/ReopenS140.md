# ReopenS140 — re-open of SOURCES row S140 (with S141) at tip `5f00fd0`

Seat: MoriR27.ReopenS140 (wave-2 falsify, leaf). Date: 2026-10-22. Tip attacked: `5f00fd045c137b7e3835506d69946cfd9d010eb5`
(branch master). Lane HEAD during the work: `47f6543a4840840acede397064c3ab481b7f9659` (`git rev-parse`);
`5f00fd0` is its ancestor (`merge-base --is-ancestor` → yes).

Assignment: re-open SOURCES row S140 (oh-my-pi commits `6962d5cd` = S140 and `c4a2441d` = S141): row
`corpus/SOURCES.md:146-147`, Gate entry `corpus/lessons/round-27.md:81`, every URL, hash comparison, every anchor
and quote, `teaches` vs bytes, scope width, duplication, and every lane statement citing S140.

Method: every URL fetched by plain `curl` to `/fast/scratch/hyaku/mori-r27/ReopenS140/`; every line pin from
`grep -n`/`sed -n` on the downloaded bytes (no read-tool URL windows — see the drift incident in
`.ufo/waves/round-27/w1/ReviewR7Knowledge.md` §6); lane text pinned by `git grep -n 'S140' 5f00fd0…` at the rev.
Access window: fetched 2026-10-22, last byte before 2026-10-22T17:19:58Z (`date -u`).

Tooling record (operator directive): no installs or upgrades were needed — curl, jq, sha256sum, coreutils, and
read-only git only. pacman untouched (transactions paused host-wide).

## 1. Fetch and hash ledger (all HTTP 200 via `curl -f`; sha256 of the bytes as fetched)

| Artifact | URL | sha256 (full) | Size |
|---|---|---|---|
| S140 commit patch | https://github.com/can1357/oh-my-pi/commit/6962d5cd2ef157ebf9f415acd58b8744f66400d8.patch | `0c8fa1ee3d1a241b6eb740eb117e56dcfd7ca7fa5e4dcd947fd1eb98a5a8d2e7` | 2,740,033 B |
| S141 commit patch | https://github.com/can1357/oh-my-pi/commit/c4a2441d8f9195de810b3492be5bf5673cecf9c9.patch | `a4e2e4db4c03937ca94ac7d477fe9c4bcd3f74cf8829c9502ebdcde1b6ac5c29` | 468,933 B |
| S140 commit API JSON | https://api.github.com/repos/can1357/oh-my-pi/commits/6962d5cd2ef157ebf9f415acd58b8744f66400d8 | `ff56022fce1f209b25030b9292649185cdaf890fc863a91d2437dd176067c03f` | 1,161,775 B |
| S141 commit API JSON | https://api.github.com/repos/can1357/oh-my-pi/commits/c4a2441d8f9195de810b3492be5bf5673cecf9c9 | `f61b7b3f9771381e0dcebaba174a2f1bd25b39453475e269af4ff40ae1ce60b3` | 562,098 B |
| sdk.ts @ 6962d5cd | https://raw.githubusercontent.com/can1357/oh-my-pi/6962d5cd2ef157ebf9f415acd58b8744f66400d8/packages/coding-agent/src/sdk.ts | `84f3a112a670f36de9c030756f4babc0ad83e37efeca99154ea4d4263423e633` | 5,029 lines |
| sdk.ts @ parent d9bc4fbd | …/d9bc4fbdc06a967c5cb1f41a53d67a4dda8dfd1f/packages/coding-agent/src/sdk.ts | `fde5a959e3a310be1d9fd291163dd817d2328d2b5a2012697b75b3205d592104` | 4,586 lines |
| sdk.ts @ c4a2441d | …/c4a2441d8f9195de810b3492be5bf5673cecf9c9/packages/coding-agent/src/sdk.ts | `4f4897502a75b0b4e0dc5cfa633559e610410a84cb719745fe7d057906029186` | 5,054 lines |
| sdk.ts @ v18.12.6 = 45c35e40 | …/45c35e40c46166dc726ccc52f5d27f40f2449f99/packages/coding-agent/src/sdk.ts | `c0228addd4cfe93cfd370c7248e9db29743f0fa802aea0e1d1adf4994dbe6957` | — |
| job-manager.ts @ 45c35e40 | …/45c35e40…/packages/coding-agent/src/async/job-manager.ts | `0f37afaaa822ef1de845b8eb21473a70210176ff61e2dcff5925f85ec0e544e7` | 1,331 lines |
| tools/settings.ts @ 45c35e40 | …/45c35e40…/packages/coding-agent/src/tools/settings.ts | `514974143d47db0c9765bc47e86dcb9a38bd6bc23113a4ffe557bff0d8e30507` | — |
| S140 commit HTML page | https://github.com/can1357/oh-my-pi/commit/6962d5cd2ef157ebf9f415acd58b8744f66400d8 | `a7650cc3bed0cab5482209e41ee2f79d4777ffd65cc151e9f83c36c43fa1da9e` | page digest |
| S141 commit HTML page | https://github.com/can1357/oh-my-pi/commit/c4a2441d8f9195de810b3492be5bf5673cecf9c9 | `8d67f92bb2282e783718ebc74be725949c63c8693482b8c8f19e428f4ad19ca5` | page digest |

Hash comparison: the row (`SOURCES.md:146`) and the Gate entry (`round-27.md:81`) record **no sha256** for these
commits. The recorded hashes live in the w1 report the Gate names (`.ufo/waves/round-27/w1/ReviewR7Knowledge.md`
§7) and in the entry's `verified-at` line (`harness-job-capacity-r25.md:2`). All five comparable digests match:
sdk.ts @ 6962d5cd `84f3a112…e633` ✓, @ parent `fde5a959…2104` ✓, @ c4a2441d `4f489750…9186` ✓ (R7 §7);
sdk.ts @ 45c35e40 `c0228add…` ✓ and tools/settings.ts `51497414…` ✓ (entry `verified-at`, S099/S100 rows).
My `.patch`/API-JSON/HTML digests have no prior record; R7 §7's `0f061b53…8366` is a different artifact (API
patch dump), not comparable — no mismatch claimed. The HTML pages are JS-rendered (`grep -c maxRunningJobs`
→ 0 hits in both); the commit bytes above are the evidence.

## 2. Row S140 (`corpus/SOURCES.md:146`) — verdicts per cell

- **URL**: names the commit page; fetched (HTML 200) and its canonical bytes via `.patch` + API. ✓
- **Kind code, tier A, status mined, opened 2026-10-22, recheck on-release, used-by
  `corpus/knowledge/harness-job-capacity-r25.md`** ✓ (the entry cites S140 at `:277`, `:330`, `:1`, `:3`).
- **Anchor** — holds, every pin on sha-verified bytes:
  - `sdk.ts:1949` = `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings) ?? 100),` — exact at
    `sdk_6962.ts:1949` (`grep -n maxRunningJobs` → sole hit; leading indent is 5 tabs, `cat -A`).
  - parent `d9bc4fbd` — API: 6962d5cd's sole parent is `d9bc4fbdc06a967c5cb1f41a53d67a4dda8dfd1f` ✓.
  - parent "still static (`:1797`, `:1811`)" — `sdk_parent.ts:1797`
    `const asyncMaxJobs = Math.min(100, Math.max(1, settings.get("async.maxJobs") ?? 100));` and `:1811`
    `? new AsyncJobManager({ maxRunningJobs: asyncMaxJobs })` — both static, computed once. ✓ (R7 §7's
    "(static, `:1797`)" was the incomplete citation; the row's two-line anchor is the correct one.)
  - "authored 2026-09-24T18:04:41Z" — API `commit.author.date` exact ✓ (author can1357).
- **Scope** "the 2026-09-24 rewrite of the clamp from a static value to a per-check function; that rewrite only" —
  holds as a row-coverage limiter. The rewrite is real and in this commit: `s140.patch:28271` removes
  `const asyncMaxJobs = Math.min(100, Math.max(1, settings.get("async.maxJobs") ?? 100));`, `:28279` removes the
  static construction, `:28282` adds the function form; the job-manager option type widens to
  `number | (() => number)` (section header `s140.patch:3727`, lines `:3735-3737`). Context: the commit is a large
  settings-registry refactor (300 files, +21217/−15807, subject "feat: implemented centralized settings registry
  and internal URL routing"; the sdk.ts section alone has 93 hunks) — the anchor makes no commit-size claim, so
  the limiter reading is the only one available and it is accurate.
- **Teaches** "The clamp site is not immutable: the same ceiling can be re-expressed as a per-check function, and
  the explicit floor can vanish in the rewrite." — holds: ceiling 100 present in both forms; per-check function at
  `:1949`; the explicit `Math.max(1, …)` floor present at parent `:1797` is absent from `:1949` and is removed by
  this commit (`s140.patch:28271`). Scoped to the clamp site, which is what the bytes show.
- **Not a duplicate**: `grep -n '6962d5cd|c4a2441d|sdk\.ts'` over `SOURCES.md` at the tip shows only S140/S141
  name these commits; older rows touching sdk.ts bytes are S099 (`:105`, file at 45c35e40, digest `c0228add…` —
  different bytes) and S104 (`:110`, commit `476b858b` — different artifact). No older row holds this row's file. ✓

## 3. Row S141 (`corpus/SOURCES.md:147`, named by the assignment) — verdicts per cell

- **Anchor** — holds: `sdk.ts:1964` = `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings)),`
  exact at `sdk_c4a2.ts:1964` (sole `maxRunningJobs` hit in that file); "diff removes `?? 100`" exact at
  `s141.patch:5354-5355` (`-… ?? 100),` → `+… (settings)),`); "authored 2026-09-24T23:02:43Z" exact per API ✓.
- **Scope** "the 2026-09-24 removal of the `?? 100` fallback; that change only" — holds as a limiter, same
  convention as S139/S140. Context: c4a2441d touches 151 files (+3265/−1412) and its sdk.ts section alone has 67
  changed lines, so the cell must be read as row-coverage, not commit-size — which is how the sibling rows use it.
- **Teaches** "The fallback inside the clamp can disappear without the ceiling changing." — holds: `?? 100` gone,
  `Math.min(100, …)` kept (`sdk_c4a2.ts:1964`).
- **Not a duplicate** ✓ (same check as §2).
- **New fact, no defect**: c4a2441d's parent is `4a7b586821a4df0afcea657717247f6ec9db8f88`, **not** 6962d5cd — an
  intermediate commit exists between S140 and S141 (which is why the line moved 1949 → 1964: sdk.ts grew from
  5,029 to 5,054 lines across that gap plus this commit). No landed statement claims direct succession; U1's
  "dropped the same day" claims only the same UTC calendar day, which both author dates satisfy.

## 4. Lane statements citing S140 (`git -C <lane> grep -n 'S140' 5f00fd0…`, 6 hits) — verdict per statement

Working-tree note: `harness-job-capacity-r25.md` is byte-identical between `5f00fd0` and HEAD
(`git diff --stat 5f00fd0 HEAD -- <three files>` lists only SOURCES.md +1 new S142 row and round-27.md's S142 Gate
row plus an unrelated learned-bullet rewording; the S140/S141 rows and the S138–S141 Gate line are untouched).
Line numbers below are the rev-pinned ones.

1. `corpus/SOURCES.md:146` — the row; verified in §2. **Holds.**
2. `corpus/SOURCES.md:147` — S141; verified in §3. **Holds.**
3. `corpus/knowledge/harness-job-capacity-r25.md:277-284` (U1; cites S140, S141 at `:277`) — each sub-claim:
   - "the clamp itself was rewritten on 2026-09-24 (S140, S141)" — holds (§2 dates + diff).
   - "from the static `Math.min(100, Math.max(1, …))` computed once at session construction" — holds
     (`sdk_parent.ts:1797` is a session-construction `const`).
   - "to the function `() => Math.min(100, cfgAsyncMaxJobs.get(settings) ?? 100)`" — holds (`sdk_6962.ts:1949`).
   - "whose `?? 100` fallback was dropped the same day" — holds (c4a2441d authored 2026-09-24T23:02:43Z;
     `sdk_c4a2.ts:1964`).
   - "The ceiling of 100 held to v18.12.6, where the clamp reads … (`sdk.ts:2284`, F2)" — holds
     (`sdk_45c3.ts:2284` = `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings)),`, sha matches the
     entry's `verified-at` line).
   - "the explicit floor `Math.max(1, …)` did not survive that rewrite — neither the clamp expression nor the
     accessor (`tools/settings.ts:941-946`) carries a floor at v18.12.6" — holds as scoped: the clamp expression
     at `:2284` has no `Math.max`; the accessor at `settings_45c3.ts:941-946` is a plain `register({ … default:
     100 })` and the file has no `Math.min`/`Math.max` at all (`grep -n 'Math\.(max|min)'` → 0 hits), sha
     `51497414…` matching S100 and `verified-at`. Entry-internal consistency holds: F3 (`:69-78`) documents the
     manager getter's own floor `Math.max(1, Math.floor(value ?? DEFAULT_MAX_RUNNING_JOBS))`
     (`job-manager.ts:330-335`; verified `jm_45c3.ts:334`) and composes `effective = max(1, floor(min(100, base)))`,
     so the entry never claims the cap is unfloored. Notably that getter floor was **added by this same commit**
     (`s140.patch:3767`, job-manager.ts section from `:3727`) — the floor left the sdk clamp site and reappeared
     in the manager. **Holds** (wording note → Low-1).
4. `corpus/knowledge/harness-job-capacity-r25.md:330` (correction log) — "the clamp rewritten on 2026-09-24,
   S140, S141 … and the explicit floor of 1 did not survive the rewrite" — holds as a summary; it drops U1's
   dash-clause scoping (see Low-1). **Holds** with the Low-1 note.
5. `corpus/lessons/round-27.md:81` (Gate row) — quote `sdk.ts:1949 "maxRunningJobs: () => Math.min(100,
   cfgAsyncMaxJobs.get(settings) ?? 100),"` matches `sdk_6962.ts:1949` word-for-word (indent tabs rendered as
   spaces — Low-2); "re-opened and re-verified by ReviewR7Knowledge, routed R7" is accurate — all five digest
   comparisons against that report's §7 match (§1). **Holds.**
6. `corpus/knowledge/harness-job-capacity-r25.md:1` (source line) — lists "S138, S139, S140, S141 (oh-my-pi
   commits 944d7f8d, e398f831, 6962d5cd, c4a2441d — the clamp history after the feature commit; added round 27,
   routed R7" — ids, shas, and description all accurate; the `recheck:` line (`:3`) "re-open S098–S103, S112–S113
   and S138–S141" is consistent. **Holds.**

## 5. Findings by severity

- **High**: none. Every anchor line number, every quote, both author dates, both parent statements, and all five
  recorded digests check out against the fetched bytes.
- **Medium**: none.
- **Low-1 (wording)** — `corpus/knowledge/harness-job-capacity-r25.md:330` (and the unqualified head clause of
  U1 at `:282`) can be read as "the v18.12.6 cap has no floor": in fact the floor left the sdk clamp site while
  the same S140 commit added an explicit `Math.max(1, …)` floor to the job-manager getter (`s140.patch:3767`;
  v18.12.6 `jm_45c3.ts:334`), which F3 (`:69-78`) documents. Exact old → new text (recommendation only; I do not
  edit the lane):
  - old: `the ceiling of 100 held to v18.12.6, and the explicit floor of 1 did not survive the rewrite.`
  - new: `the ceiling of 100 held to v18.12.6, and the clamp site's explicit floor of 1 did not survive the rewrite (the manager getter's own floor stayed; F3).`
- **Low-2 (cosmetic)** — the S140 anchor and the Gate quote render the 5-tab indent of `sdk.ts:1949` as spaces;
  the words are verbatim, whitespace is not. No change required; flagging for the quote convention only.

## 6. Residual risk and verification gaps

- Commit-page HTML digests are session-specific (embedded relative timestamps, JS rendering); the stable commit
  bytes used here are the `.patch`, raw-file, and API endpoints. The HTML pages were fetched only to satisfy
  "fetch every URL the row names" and add nothing the patch lacks.
- The intermediate commit `4a7b5868` between S140 and S141 was not opened; no landed statement depends on it.
- S138/S139 (including S138's "touches only CHANGELOG, settings-schema.ts, sdk.ts" commit-size claim) belong to
  sibling seats and were not attacked here, beyond the duplication check.
- R7 §8's own caveats stand unchanged (getter not executed at runtime; no omp run; single-version reading).
- No statement in this report is [INFERENCE]; every pin cites a command and its output on the bytes listed in §1.
- Privacy: this report contains only commit ids, URLs, digests, line numbers, upstream code quotes, and counts —
  no operator settings values, session data, uid/pid digits, journal text, or earlyoom flag values.

Scratch (retained): `/fast/scratch/hyaku/mori-r27/ReopenS140/` — the twelve fetched artifacts of §1.
