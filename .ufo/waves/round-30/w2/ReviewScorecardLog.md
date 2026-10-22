# ReviewScorecardLog — calibration attack on the round-30 SCORECARD and LOG sections

**Verdict: agree.** Every statement in the round-30 SCORECARD declaration (`SCORECARD.md:1802-1814`), the round-30
measured outcome (`SCORECARD.md:1816-1825`), and the LOG round-30 entries (`LOG.md:1952-1988`) that names a hash,
number, verdict, or file name checks out against committed bytes; both counters were re-run from their commit blobs
and reproduce the receipts byte-for-byte. Findings below are verification gaps and one trivial timestamp drift, not
contradictions. Lane moved during review: `ad0f047` (the measured-outcome commit) → `713be29` → `95cd794`; the new
commits do not touch SCORECARD.md or LOG.md (`git show --name-only 95cd794 | grep -E 'SCORECARD|LOG'` → neither).

## Method

- All `git` in the lane was read-only (`rev-parse`, `cat-file`, `show`, `log`, `ls-files`, `ls-tree`, `status`, `diff`).
- Counters re-run from commit blobs per the wave context recipe:
  `bash <(git show 6c47dd03:.ufo/waves/round-30/count-c1.sh) 58b61681` → `rows=0 … C1=unmet` (matches
  `evidence/c1-before.txt` exactly); same blob at `ee61010dec12…` → `rows=13 rows_ok=13 new_ids=5 new_id_rows=13
  excerpts_ok=5/5 skill_rows=4 C1=met` (matches `c1-after.txt`).
  `bash <(git show 8ac9535e:.ufo/waves/round-30/count-c2.sh) 58b61681…` → `r29_selftest=FAIL 21/24 … C2=unmet`;
  same blob at `2ec25cc1…` → `… blind_violations=1 C2=unmet` (matches `c2-before.txt` / `c2-after.txt`; my
  `tail -22` clipped the first two `writer_absent` lines, the receipts show all four CaseR30a–d).
- No tools installed; none needed.

## Findings

### Medium — metric/census values asserted with no committed receipt (unverifiable, not falsified)

1. `LOG.md:1987` "Retention metric 4 at the C1 draft (sandbox commit of the same bytes), base 4" and
   `SCORECARD.md:1824` "Retention metric 4 at the C1 batch (base 4)". The base-side value is receipted
   (`.ufo/waves/round-30/w1/RetentionBase.md:19` prints `"commit":"58b61681…","metric":4`, and :57 shows the
   synthetic-probe clone also at 4). But no committed file under `.ufo/waves/round-30/` contains a scan at the C1
   draft/batch (`grep -rln 'metric":4'` over `.ufo/waves/round-30/` → only `RetentionBase.md`, which scans
   `58b61681` and its sandbox clone, not `ee61010d`/`ad0f047`-era bytes). The lane's own convention is "one committed
   command over committed bytes"; this number has neither. [Gap, not contradiction: the value is plausible — base 4,
   C1 batch added only sourced rows and excerpts.]
2. `LOG.md:1987` "Census at the C1 batch: `mori ok`, exit 0." No committed receipt; the only census receipts are
   `evidence/census-start.txt` (at `58b61681`, 21:06:17Z) and an **untracked** `evidence/census-end.txt` in the
   working tree (run at `95cd794`, `mori ok`, exit 0 — ten W04 then ok, same shape as census-start). The claimed
   C1-batch census is neither file.

### Low — named tip receipts still absent (forward reference, pending)

3. `SCORECARD.md:1824-1825` and `LOG.md:1988` name `tip-c1.txt`, `tip-c2.txt`, `tip-retention.txt` as the
   receipts-only last batch. At HEAD `95cd794` none exist (`git ls-files` and `ls` over
   `.ufo/waves/round-30/evidence/` — 13 files, none `tip-*`). The text itself labels them a future batch, so this is
   pending rather than false; closure should verify the batch lands with exactly these names at a commit whose
   counter outputs match (routed R1, per `w1/TipReceiptsR1.md`).

### Trivial — timestamp drift

4. `LOG.md:1961` "Round-start census 21:05Z" vs `evidence/census-start.txt:1` header `2026-10-22T21:06:17Z` (and
   contract commit `a66751b` committer `21:08:28Z`). The printed receipt is the ground truth: off by ~1 minute.

### Observation — no defect, flag for closure write-up

5. Differential numbers live at two scopes: `c2-differential.txt` prints `inputs=126 changed=5 older_changed=2`
   (LOG.md:1981-82 quotes it faithfully), while the counter's own differential cell in `c2-after.txt` prints
   `differential=94/94 changed=2`. Both receipts are committed; nothing in SCORECARD/LOG reconciles 94-vs-126 or
   2-vs-5, so a closure reader sees two unexplained `changed` figures. LOG's claim matches the receipt it cites;
   recommend the closure note the counter's narrower input set. [INFERENCE on the cause of the narrower scope.]

## Verified-true sample (every claim class exercised)

- Entering tip `58b61681a0e3f3b821a17d38a4e713ccd9921615` = commit `58b6168`, subject "round-29 verifier spot-check";
  MANIFEST `rounds[483]` = mori r29, `"verdict":"rejected-honest-stop"`, `verdicts.calibration="improved"`,
  `operability="unchanged"` (consistent with "C1 met, C2 miss" in `LOG.md:1955`). Fleet `MANIFEST.json` len 487.
- Contract landed `a66751b1` before any data: committer `21:08:28Z` vs first data commit `b039dd4f` `21:15:51Z`;
  `git show --stat a66751b1` adds `contract.md`, `rule-text.md`, `evidence/census-start.txt` (LOG.md:1955-56).
- Wave 1: `LOG.md:1963` "35 seats (11 executor, 12 scribe, 4 scout, 4 critic, 3 reviewer, 1 connector)" — registry
  roles count exactly `{executor:11, scribe:12, scout:4, critic:4, reviewer:3, connector:1}` = 35 members;
  `wave1-run.json` counts `{spawn:35,total:35}`; 35 `w1/*.md` reports on disk ("0 dead" consistent).
- Amendment order claims (`LOG.md:1971-74`): A1 `05db57ed` 21:19:42Z → A2 `3767108e` 21:22:16Z → gate `32e287ff`
  21:32:49Z → A3 `55f9a694` 21:33:54Z; `gate-a2-prefreeze.txt` (A2 blob `893e69d1…`, confirmed by
  `git rev-parse 32e287ff:check-blind-wave.sh`) run 21:33:43Z shows `blind_violations=4`, one per writer — all
  godspeed `SKILL.md` lines confirmed at `CaseR30a.md:96`, `b:116`, `c:79`, `d:110`. A3 gate blob `dbcbe50e…`
  (at `55f9a694`, `db1ec469`, tip) adds the two-file allowlist (contract `Amendment A3`, contract.md:207-221,
  disclosed as after-data — matches LOG).
- Freeze claims (`LOG.md:1977-79`): `db1ec469` = `db1ec4694242a9c1acef03fef2852c7e943b1ed7`; file sha256
  `b68843e7…3735` reproduced; JSON holds `cases`=8 with authors {CaseR30a:2, CaseR30b:2, MoriR30.CaseR30c:2,
  CaseR30d:2} = "4 writers × 2"; `c2-freeze-selftest-base.txt` ran 21:48:29Z on the `58b61681` tool blob,
  `PASS 8/8` — after the freeze committer `21:48:21Z`, consistent with "no tool run before this commit".
- Tool fix (`LOG.md:1980-82`): `7aa77484` full hash verified; `evidence/fix-tool.diff` = the commit's tool diff
  (28 added lines, set-identical to `git diff 7aa77484^ 7aa77484`, sandbox `---/+++` headers only). Differential
  receipt: `inputs=126 changed=5`, the 2 "older" changed rows are `a2-02` (deactivating) and `a2-06` (inactive) —
  "both non-active" accurate.
- C2 miss (`SCORECARD.md:1821`, `LOG.md:1983-84`): counter re-run at `2ec25cc1` prints `blind_violations=1 C2=unmet`
  exit 1; flagged line `CaseR30a.md:105` reads `The scratch JSON passed python3 json.load; …` — the closing sentence
  with the dotted token `json.load;`, matching the receipt explanation. Diagnostic gate prints 0/exit 0
  (`gate-a4-diagnostic.txt`), explicitly uncounted — matches LOG wording.
- C1 met (`SCORECARD.md:1820`, `LOG.md:1985-86`): counter blob identical at `6c47dd03`, `ee61010d`, `ad0f047`
  (`325168f6…`); S156–S160 present at `SOURCES.md:162-166`; `new_ids=5` = five new ids. Note: `6c47dd03` is a
  **commit** (`git cat-file -t` → commit), called "blob" in SCORECARD — the project's own idiom is "commit blob"
  (`c1-after.txt:1` says "counter from its commit blob 6c47dd03"), so the SCORECARD parenthetical is loose wording,
  not an error; same for "C2 counter `8ac9535e`" (commit).
- Held-axes claims: r30 held list (freshness 5, calibration 5, coverage 6, adjacency 6; operability 7, depth 5 in
  outcome) matches r29 measured outcome (`SCORECARD.md:1799-1800`) and depth 5 "tied lowest" is true (freshness 5,
  calibration 5 equal).
- Receipt/commit timing is honest once author-vs-committer dates are separated: every receipt's embedded run time
  falls inside its containing commit's author→committer window (author dates pinned to batch start, e.g. `a66751b`
  author = `58b6168`'s author date). No receipt timestamp postdates its own commit's committer date.
- Untracked inheritance (`LOG.md:1962`): `.scratch/` is untracked and pre-round; at HEAD the only other untracked
  path is the in-progress `evidence/census-end.txt` — wave-2 work, outside the declaration's claim scope.

## Residual risk

- The two unreceipted numbers (finding 1-2) are the only "miss" class available to this item: honest-but-unverifiable.
  If the receipts-only batch lands `tip-retention.txt` showing 4 and a census receipt at `mori ok`, both gaps close.
- Counter blob `8ac9535e` before-receipt used the pre-commit working file (`c2-before.txt:1-2` header admits this);
  my blob re-run reproduces identical output, so no drift, but the receipt's own provenance wording is imprecise
  ("one command over committed bytes" holds only for the committed-blob re-run).

Seat: MoriR30.ReviewScorecardLog. No installs. All lane git read-only; only this report file written.
