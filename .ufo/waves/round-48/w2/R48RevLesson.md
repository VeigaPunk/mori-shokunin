# R48RevLesson — lesson-file falsification (round 48, wave 2)

**Attacked:** `corpus/lessons/round-48.md` — every pointer (path, line, commit, section),
every number (251 registry ids, 136 staged, 8 collisions, 39/49 seats, 13/395 portability,
12-vs-11 cells, offsets, page/line counts), and every Mistakes row's captured-by plus each
"shown able to fail" command/arm, all re-derived at tip `e4dfff32d4f97c7ef250e9a7538fa75d4f284492`.

**Verdict: BREAKS** — two claims do not reproduce (one wrong-cause mechanism claim, one
number-drift claim); every pointer, hash, count and fail-arm named in the lesson otherwise
reproduces. Both counters met at the tip as claimed.

## Findings (by severity)

### F1 — wrong cause stated for a negative-claim failure (M7, class: fabricated mechanism)

`corpus/lessons/round-48.md` M7 evidence: *"`w1/ScribeEntryA.md` stated that `Disk quota
exceeded` is absent from the Aliyun copy; it searched the raw HTML, where the words are
split by tags; the normalised copy holds it (offset 5042)."*

- `w1/ScribeEntryA.md:99-103` did claim the string absent (verified).
- The normalised copy holds it — my re-derivation with `count-c2.py`'s exact `normalise`
  gives offset **5042** for `Disk quota exceeded` and 5002 for the full dd phrase. That part
  reproduces.
- **The mechanism does not.** The committed copy's *raw bytes* contain the contiguous
  English string **twice**: raw offsets 26626 (inside the JSON-escaped markup) and 81461
  (rendered HTML body), both as
  `<code>dd: closing output file '/data/1G.txt': Disk quota exceeded</code>` — no tag splits
  the words; even the full 12-word quote is a contiguous raw substring (raw idx 26586).
  Command: `python3 -c "raw=open('corpus/evidence/sources-r48/aliyun-nas-quota.html','rb').read().decode('utf-8','replace'); print([i for i in range(len(raw)) if raw.startswith('Disk quota exceeded',i)])"` → `[26626, 81461]`; `raw.find("dd: closing output file '/data/1G.txt': Disk quota exceeded")` → `26586`. So "searched the raw HTML, where the words are split by tags" is not what ScribeEntryA did or could have observed: the literal string is present in raw HTML too. The lesson's correction *content* (the claim holds; ScribeEntryB located it) is right; the stated *mechanism* of the mistake is wrong — ScribeEntryA's own scratch (`analyse_sources.py`, `pins_candidates.py`, `check_entry.py`) only ever searched `normalise()`d copies, which already contain the string, making its "absent" assertion inexplicable by any documented search at all.

### F2 — "four legitimate mutant-command rows" does not reproduce (M3 not-closed note, class: number-drift)

`corpus/lessons/round-48.md` M3 fix tail: *"Not closed: D7 … — a rule turns four legitimate
mutant-command rows red."* (Same figure embedded at `SKILL.md:962`.)

Header-aware parse of the registry at `e4dfff32` (self-test column taken from each table's
own header): exactly **three** rows carry a bindable mutant-command path in their self-test
cell — SKILL.md:190 (`round-45/count-c1.py` → `fixtures/mutants/count-c1.py`), :191 (count-c2),
:192 (count-c3). Rows 183 and 186 name `.ufo/waves/round-44/fixtures/mutants/*.py` only in the
pinned-values cell, where no command binds. Five backticked mutant-path spans exist repo-wide,
six rows mention them anywhere, three rows actually bind a mutant argv. No reading of the
registry yields four. The "not closed" disposition itself is right (D7 survives; a
bind-argv-to-entry rule would redden the three r45 mutant rows), but the stated count is off
by one — and it is now frozen into SKILL.md:962 as well.

### F3 — minor: `evidence/after-c1-at-e4dfff32.txt` is a 0-byte receipt (observation, not a lesson defect)

`ls -la` → `after-c1-at-e4dfff32.txt` = 0 B (mtime 19:37), while `after-c2-at-e4dfff32.txt`
(152 B) holds the C2 receipt. The lesson does not cite these files; my own run below supplies
the C1 receipt. Recorded because a wave-2 reader may mistake the empty file for evidence.

## Verified claims (each re-derived, command + output)

Both claims:

- `python3 .ufo/waves/round-48/count-c1.py --tool tools/mori-pin-check.py --rev e4dfff32…` →
  `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12 rev=e4dfff32…`, exit 0
  (wall 935 s; all J1–J8 unmet rc=1, H1–H4+real met rc=0). **C1 holds.**
- `python3 .ufo/waves/round-48/count-c2.py e4dfff32…` →
  `C2=met claims=15 located=15 quote_missing=0 bad_rows=0 sources=4 source_rows=ok pins=ok provenance=ok`, exit 0. **C2 holds.** Entry has exactly 15 claim rows over sources S479–S482; S483/S484 are source-line boundaries only, matching `sources=4`.

Gate / SOURCES rows:

- Rows S479–S484 exist (`SOURCES.md:258-263`), all `mined`, all `opened 2026-10-25`,
  `used-by` = `corpus/knowledge/quota-observability-r48.md`; S483/S484 recheck `on-release`,
  rest `180d`. Tip diff on SOURCES.md: **6 `+` rows, 0 `-`** → "changed in place: none" holds.
- All six copy sha256 prefixes match the lesson table (`6375e40e…`, `0d4ab273…`, `66a5ad60…`,
  `747fef1b…`, `006286df…`, `530c3cc2…`).
- Live re-fetch with a browser UA (2026-10-25): `xfs_quota.8.html`, `quotactl.2.html`,
  `errno.h` each **byte-identical** to the committed copy (`cmp`); the Aliyun page **differs**
  in bytes (fresh sha `5d0cf6ed…`) while all three cited strings locate in its normalised
  text — exactly the lesson's claim.
- `errno.h:107` = `#define EDQUOT 122 /* Quota exceeded */`; `arch-mips-errno.h:131` =
  `EDQUOT 1133`; `arch-sparc-errno.h:43` = `EDQUOT 69` — all at the stated line numbers.
  The lesson's `for a in mips sparc alpha parisc` curl → `1133, 69, 69, 69` verbatim.
- `assimilation/{reg-ids,staged-ids,collisions}` = **251 / 136 / 8**; collisions file lists
  `S471 S472 S473 S474 S475 S476 S477 S478`. Renumber mapping (staged S477→S479, S478→S480,
  S482→S481, S479→S482) matches the landed rows' URLs.
- `grep -cE '^ {0,3}\| *S26[01] *\|' corpus/SOURCES.md` → **0** (S260/S261 absent, as the
  reject says); `S233` = gihyo cgroup v2 article (line 239). Staged `SOURCES.append.md` S502
  row splits to **12 cells** on the unescaped `|` inside the recheck command (`pdftotext … - \
  | grep -c`) — "12 cells, not 11; used-by displaced" reproduces.
- S478 recheck cell = `180d`; awk sweep of every registry row's recheck column → **zero**
  ISO-date cells (ExecS478Recheck's cadence tally consistent). `w1/ExecS478Recheck.md` §1–3:
  plain curl 418, browser-UA 200, sha256 `1603404dd25b3a0dff93f2dcb23c75b671d4e2d78da3cce8f461e87ebde6add2`, 14 pages — all verbatim.
- `evidence/sweep-quota-rows.txt` → `grep -cE 'xfs_quota|quotactl|EDQUOT|repquota'` at
  `e5dbac05` = **0**; re-derived: `git show e5dbac05:corpus/SOURCES.md | grep -cE …` → 0.
- Portability counts re-run at both `e5dbac05` and `2d85e33d`: tools/ `.py|.sh` containing
  `/home/vgpnk` → **3** both; top-level `round-4[0-3]` instruments → **10** both; all
  `tools/` + `.ufo/waves/round-*/` `.py|.sh` containing it → **395** both (885/883 in-scope
  files). `count-c1.py`, `count-c2.py`, `mori-pin-check.py`, `mori-unlanded-check.py` hold 0;
  `build-w1-spec.py` holds 12 → "a wave builder" caveat holds.
- Quarantine slice: file lists S244/S262/S268 with the stated class; lane registry has no
  S244 or S268 row (S262 exists as the ROMA abstract record — consistent with the lesson's
  "same document as lane S262/S478"); no admitted row cites them. Scout reports verified:
  S244 DOI/arXiv quote, S262 IEEE 202/0+418 + sha256 `1603404d…`, S268 PDF quote lines 139–141.
- `considerthese/2026-10-25.md` suggestion 2 = the portability count (lands as QUALITY 127 —
  row text matches the counting commands); `w1/ScoutConsiderthese.md` marks 2026-10-25 #3
  (critic flags fixed-vs-unfixed) **Unimplemented** → "next unimplemented" holds.
- `seat-terminal-status-r17.md:20` maps `dead_quota` to a Z.AI provider quota token; the
  staged entry `quota-observability-r38.md:63-66` does link `Disk quota exceeded` to
  `dead_quota` — the refused-link claim reproduces.
- `w1/ExecCensusGuard.md` documents the 0–3-space fixture re-proof (its example ids differ
  from the lesson's `  | S002 |` illustration, semantics identical — indented ≤3-space rows
  are counted and can collide).
- `w1/ScribeLessonGate.md` draft offered admit S479–S482 + reject the 12-cell mapping-files
  entry — the "sample offered" claim reproduces.

Mistakes table (each row):

- **M1:** `tools/mori-unlanded-check.py --selftest` → `UNLANDED_SELFTEST pass=13 fail=0`,
  arm `untracked_late_result_exit1_names_it` PASS (`rc=1`, names `w2/Late.md`; clean run
  `UNLANDED=clean` rc 0). Live run `--repo <lane> --round 48` → `UNLANDED=dirty round=48
  paths=16` **exit 1**, listing the uncommitted w2 artifacts. Round-47 routed defect 1's
  files (`w2/CritV2Junk.md`, `MutV2Rebound.md`, `ScoutMisroot.md`, `w2-results.json`) all
  committed in `356fb94a` (verified `git show --stat`); LOG erratum exists at LOG.md ~line
  2689. captured-by "none" accurate.
- **M2:** `evidence/control-c1-tool-v2-entering.txt` → `junk_met=8` / `C1=unmet`;
  `control-c1-stub-always-met.txt` → `junk_met=8` unmet; `control-c1-stub-always-unmet.txt`
  → `honest_unmet=4 real=unmet`; controls are byte-identical to `git show e5dbac05` bytes
  (v2 sha `9832e38c…`). Landed v3 scored met by my run above. QUALITY 123 = "re-runs from
  committed bytes" — characterization "checked values, not visibility" consistent.
- **M3:** all five named selftest arms exist in `tools/mori-pin-check.py` and PASS under
  `--selftest` (`PIN_CHECK_SELFTEST pass=60 fail=0`): `r10_digest_decoy_file_in_other_cell`
  and `r10_trunc_digest_decoy_file_in_other_cell` → unmet/mismatch; `r9a_…`/`r9b_…` →
  unmet/hidden; `r9c_…` → unmet/unparsed. D1/D2/D5/D18 confirmed `met` under v2 and
  survivors under R1–R8 in `w1/CritJunkClasses.md`; D7 survivor confirmed → see F2 for the
  only defect (the "four" count).
- **M4:** `w1/ExecRealRegistryAudit.md` documents `pin line=168 kind=digest state=mismatch`,
  whole-tree scan 12,111 files, no `c39e5a73` carrier; current SKILL.md:168 names the
  historical blob and pins `533218a566030fda…`; `sha256sum tools/mori-round14-regressions.py`
  → `533218a566030fda…` — the repaired pin matches the file.
- **M5:** `w1-results.json` ExecV3ImplA output = self-reported abort after editing and
  restoring `tools/mori-pin-check.py` (sha `9832e38c…` restored — verified matches
  `controls/tool-v2-entering.py` and `git show e5dbac05:` bytes); `w1/CritC1Counter.md`
  records the dirty observation ~18:35 (`9832e38c…` → `17cc5ba1…`, ` M`); `ExecV3Residuals.md`
  records the sibling edit in flight. The unlanded tool lists a modified `tools/` file
  (scope includes `tools/`, verified in its selftest arms).
- **M6:** `w1-results.json` `seats=49`, results list 49; eight named seats' outputs carry
  reports at `.ufo/waves/round-45/`, `round-47/`, `round-49/`, `round-40/`, `round-55/` (each
  output quoted verbatim — e.g. MutC2Counter targets `round-55/c55_quote_truth.py`);
  `w1/` holds **39** `.md` reports + `swarm-registry.json`; the ten no-report seats are
  exactly the eight of M6 plus `ExecV3ImplA` and `ExecUnlandedCheck` (name-set diff, no
  extras). 49/39/10 all reproduce.
- **M7:** claim substance verified; mechanism wrong — see F1.

Wave-1 findings section:

- `w1/CritC1Counter.md` F1 reproduces as described (variant `J*/H*` basename + per-variant
  `c1-J1-…` TMPDIR both leak the label; a file-name-keyed tool prints `C1=met`).
  `w1/CritC2Counter.md`: eight 8–10-word `<script>`/JSON fragments score `C2=met` — matches
  the report's counterexample verbatim.
- `w1/CritContractFreeze.md` "no freeze defects, four precision observations (O1–O4)" ✓;
  `w1/ExecC1Replay.md` J/H labels ✓; `w1/SentCopies.md` credential scan ✓;
  `w1/SimpCounters.md` identity `text.replace("(743 lines)", "(743 lines)")` in the C1
  selftest confirmed at `count-c1.py` (line present); `w1/RevAssimPlan.md` F1/F2/F3 including
  `SOURCES-PROPOSED.md` absent from the package, bulk-append-136 conflict, 80 entries — all
  confirmed in `MERGE-REPORT.md` and the append file.
- `w1/CritV3Spec.md` R4-keys-on-(row name, prefix) and R5/R6-path-disagreement notes read as
  the lesson paraphrases; `w1/CritEntryRisk.md` six rejected claim/quote pairs (overclaim,
  negation, example scope, other filesystem, vendor-as-Linux, number-from-example) ✓.

Routed-defect dispositions (spot-check section): routed items 1–5 of
`corpus/lessons/round-47-verifier-spotcheck.md` each map as the lesson says — defect 4 is
the "lesson cites the closure file" item (cited, done); defect 5's S478 browser-UA note is
in the Gate section. Frozen files `count-c1.py`, `count-c2.py`, `contract.md`, `v3-spec.md`
byte-identical between freeze `4387cf94` and tip `e4dfff32` (git diff empty). The four
frozen copies were in the freeze tree; `arch-mips/sparc-errno.h` were added at the tip —
"S483/S484 added after the counter froze" confirmed.

## UNVERIFIED / not reproducible by construction

- "opened by me … on 2026-10-25" and "no campaign tool run; nothing written" in the merge
  package — authorship/non-events, not checkable; consistent with all opened cells.
- The freeze-time HTTP 403 for the RHEL 9 PDF (contract states plain+browser UA; scouts got
  HTTP 200 later, `1,555,738 B`) — historical network state, not re-derivable; the contract
  text itself reproduces the claim verbatim.
- Solaris `errno=49` document and the staged `+`/`grace` claims' origin page — not fetched;
  stays rejected either way.
- "a rule turns four legitimate mutant-command rows red" — the *count* is wrong (F2); the
  *direction* (such a rule reddens the three r45 mutant rows) holds.

## Constraints honored

Report only at `.ufo/waves/round-48/w2/R48RevLesson.md`; scratch under
`.scratch/r48w2-R48RevLesson/` (live-fetch downloads only). Lane tools run with
`TMPDIR=.scratch/r48w2-R48RevLesson`; git used read-only (`show`/`ls-tree`/`diff`/`log`/`status`);
no tracked file, tool, corpus file, or frozen artifact modified; no installs (host curl,
python3, sha256sum sufficed). Leaf seat — no subagents. Live re-fetches were read-only GETs.
