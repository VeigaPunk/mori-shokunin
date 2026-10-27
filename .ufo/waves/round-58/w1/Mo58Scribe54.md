# Mo58Scribe54 — cross-claim no-harm review (round 58, w1)

Seat: scribe, leaf (no dispatch). Scope: frozen contract, frozen counters, round-56/57
records — falsifier arms, axis overlap, frozen-rule drift, detection/report boundary bleed.
Read-only in the lane: no corpus, registry, SCORECARD, LOG or VCS mutation. Every fixture was
an isolated throwaway repo under `$HYAKU_SCRATCH/mori-r58/Mo58Scribe54/` driven with
`git -C <fixture>`; scratch removed before yield.

Revisions observed: freeze `fe8801120a67c1a6b8899d7d0423839caa09e7d0`, entering
`b783d0b892637ce8d20f188cad20e4d8913ca635`, lane HEAD at review `4272736c` (freeze + dispatch
payload). Disk guard at start: `/fast/scratch/hyaku` 32% used, 553.3G free (green).

## 1. Frozen-state receipts (first-hand)

| Check | Command | Observed |
|---|---|---|
| Counter bytes unchanged post-freeze | `sha256sum` freeze blob vs worktree, per file | c1 `6ecdb627…`, c2 `aab888ad…`, contract `3aeff1d1…` — identical, all three |
| Freeze diff | `git diff --name-only fe880112 HEAD` | only `build-w1-spec.py`, `w1-dispatch.json`, `w1-spec.json`, `w1/swarm-registry.json` |
| C1 at freeze | `python3 .ufo/waves/round-58/count-c1.py fe880112…` | `C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=fe880112…`, rc 0 |
| C2 at freeze | `python3 .ufo/waves/round-58/count-c2.py fe880112…` | `C2=unmet entry=absent failed=entry`, rc 1 |
| Selftests (my run, `TMPDIR` = my scratch) | both `--selftest` | `C1_SELFTEST pass=4 fail=0`, `C2_SELFTEST pass=6 fail=0`, rc 0 each |
| SCORECARD blob entering vs freeze | `git rev-parse <rev>:SCORECARD.md` | both `fded56fc5a4961fef3de550174e56aaf7f01ae42` |
| Row pointers at freeze | `git cat-file -e fe880112:<path>` | `tools/mori-vote-bind.py`, `tools/mori-driver-liveness.py`, `…round-56/evidence/c{1,2}-at-landed.txt` all exist; `corpus/evidence/sources-r58/…`, `corpus/knowledge/driver-events-r58.md` absent |
| Fleet MANIFEST binding | `json.load` `rounds[832]` | `admitted: true`, `capabilities_added` = [vote binding, driver-liveness probe] — both counter hints present; index→content match holds |

So the kill-rule byte condition holds and C1's two live rows genuinely resolve at R. C1 has **no
round-58 register delta**: its measured output at entering `b783d0b8` and at freeze is identical
(`C1=met … failed=none`), so the only live C1 delta is the counter file itself (corroborates
Mo58Connector60).

## 2. Frozen-rule drift: C1 target string is unreachable from its own counter

- `contract.md` C1 target: `C1=met rows=2 pointers=ok manifest=ok binding=ok selftest=ok rev=R`.
- `count-c1.py:124-126` prints `C1={state} rows=… pointers=… manifest=… binding=… failed=… rev=…`;
  the only selftest token is `C1_SELFTEST pass=N fail=0` (`:229`), a separate invocation. `selftest=ok`
  is emitted nowhere (grep `selftest=` → no hit in either round-58 counter).
- Precedent for the target shape: round-56's counter did print it inline —
  `.ufo/waves/round-56/evidence/c1-at-landed.txt`: `C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=…`.
  The round-58 target looks copied from that convention while the counter moved selftest out of line.
- Consequence under the kill rule (contract: "any post-freeze change to … the target output
  invalidates the claim"): the token mismatch is freeze-internal and unfixable in-wave; C1 cannot
  score green on a literal target comparison. The lane already records C1 as unverified
  (`corpus/lessons/round-58.md`, Mistakes row 3). My measurement confirms the mechanism; the
  lesson is accurate.
- C2 target is a token subset of real output (`failed=none` is extra but appended after; all
  target tokens appear in order), so C2's target is literally satisfiable — only C1's is not.
- `tree=ok` is not an independent arm: `count-c2.py:69-74` sets `copy_arm = tree_arm` in every
  branch, so `tree=ok` repeats `copy=ok` (corroborates Mo58Critic26 item 3).

## 3. C1 falsifier arms (new constructions; frozen bytes imported, not edited)

Frozen `count-c1.py` module imported, `LANE`/`FLEET` pointed at scratch fixture + fixture
MANIFEST, `measure(rev)` called directly. Fixture toplevel asserted before every git call.

| Arm | Construction | Observed | Reading |
|---|---|---|---|
| A1 | two register rows; row[0] evidence `` `tools/mori-vote-bind.py`; tools/no-such-tool.py `` (nonexistent path **not backticked**) | `C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none`, rc 0 | pointer parse is markup-driven, not column-driven: an unbackticked evidence path is never `cat-file -e`'d |
| A2 | row[0] evidence `no-such-tool.py` (extension-only, no `/`) | `C1=met … pointers=ok`, rc 0 | second escape from the same predicate |
| A3 | legitimate active register with **exactly** the two keyed rows (no padding) | `C1=unmet rows=2 pointers=ok manifest=bad binding=bad failed=binding`, rc 1 | `count-c1.py:88-90` requires ≥10 keyed rows; `manifest` is then skipped and forced `bad`, i.e. `manifest=ok` is not an independent arm once `binding` fails |
| A4 (control) | row[0] evidence `` `tools/no-such-tool.py` `` (backticked, allowlisted prefix) | `C1=unmet rows=2 pointers=bad manifest=ok binding=ok failed=pointers`, rc 1 | the intended negative control does fail |

Prior coverage (do not double-count): Mo58Critic30 already reported the prefix-allowlist escape
(`scripts/…`, root, `./`, absolute, empty evidence cell) and Mo58Reviewer12 the
"identity at R, not against the freeze target" issue; Mo58Connector59/60 the unpinned fleet
`MANIFEST.json` read. A1/A2 add the unbackticked case, A3 the false-*negative* + manifest cascade.

## 4. C2 falsifier arms (new constructions)

Same import technique for frozen `count-c2.py`; fixture carries tool, pinned copy, entry, S550 row.

| Arm | Construction | Observed | Reading |
|---|---|---|---|
| B1 | 8 claim lines whose quotes are genuine substrings of cited lines 10–17, and **no mention of launch / complete / lane-dead-no-report / launch-fail / wrap anywhere** | `C2=met claims=8 located=8 copy=ok tree=ok rows=ok sources=ok failed=none`, rc 0 | the counter never tests the claim *subject*; the contract's "≥8 located claims on the event-class semantics (five classes)" is under-enforced |
| B2 | `source: S550`, `verified-at: 2026-10-27`, `recheck:`, `coverage-map:` present only in the **body**, frontmatter absent | `C2=met … sources=ok`, rc 0 | `count-c2.py:61` substring-tests the whole entry, so contract §9(c) ("frontmatter missing … → `sources=bad`") is not enforced positionally |
| B3 | live draft entry, `- **K1 — …**` shape vs frozen `KLINE` (`:37`, requires `**K<n>**` closed immediately) | `KLINE` matches **0 of 8** lines | independently reproduces Mo58Scribe49 F1: if the draft lands unchanged, `C2=unmet claims=0` |
| B4 (control) | conformant entry | `C2=met`, rc 0; junk quotes → `failed=quotes` | intended controls behave |

Prior coverage: Mo58MutationTester33 (short substring, duplicate K numbers), Mo58Scribe50 F2
(identifier-only span), Mo58Reviewer06/20 (extra pipe cell), Mo58Reviewer08 (claim prose not
entailed). B1/B2 are the subject and frontmatter-position gaps.

## 5. Cross-claim / axis no-harm verdict

- **Artifact disjointness.** C1 reads only `SCORECARD.md` (+ fleet `MANIFEST.json`); C2 reads
  `corpus/knowledge/driver-events-r58.md`, `corpus/evidence/sources-r58/…`, `corpus/SOURCES.md`,
  `tools/mori-driver-liveness.py`. No shared measured file, no counter reads the other's artifact.
  SCORECARD is unchanged entering→freeze→HEAD, so C2 cannot move C1 and C1 adds no register edit
  that C2 could ride.
- **Registry/adjacency overlap (quantified).** S548 (r57) anchor `parse_log` 122–174; S550 (r58)
  anchor 95–163 → anchor intersection **122–163 = 42 lines**. Quote-line intersection is **∅**
  (r57 cites 118,133,143,150,157,162,172,173; r58 cites 96,101,103,123,135,145,152,159), but
  **6 of 8** r57 quote lines sit inside S550's declared anchor and **5 of 8** r58 quote lines sit
  inside S548's. Both rows pin the same sha256 `6b3dba74…` and S548's `teaches` cell already reads
  "Grounds the exact launch, completion, wrap, dead, launch-fail, in_flight and unclosed parser
  transitions". Verdict: no identical bytes are double-counted, but the depth increment re-grounds
  the same five branches S548 already declares; the judge should read C2's scope as a deepening,
  exactly as the entry's `coverage-map:` states. (Extends Mo58Scribe49 F2/F4 and
  Mo58MutationTester35 with the arithmetic.)
- **Freshness nuance.** `corpus/evidence/sources-r58/mori-driver-liveness.py`,
  `…/sources-r57/…` and `tools/mori-driver-liveness.py` are all `6b3dba74…` (18,347 bytes class).
  `copy=ok` therefore shows identity-at-R, not a fresh capture; do not read C2 as freshness evidence.
- **No axis harmed.** Census append-only: `git diff corpus/SOURCES.md` adds S550 + one round-58
  search-log line, no prior cell changed; rows 322→323; `scripts/sources-census.sh validate --root
  /home/vgpnk/Projects/shokunin mori` → `mori ok`, rc 0, same W04 set. README adds a round-58
  Core-deepening row that explicitly claims no Frontier advance. Contract claims no scalar change
  on either axis; nothing I observed contradicts that.

## 6. §9 do-nothing control status, read literally

- C1: "a fixture register whose two rows name a nonexistent evidence path MUST score
  `C1=unmet … failed=pointers`" — **violated** by A1/A2 (met, rc 0) and by Mo58Critic30's forms.
  Under the contract's own words ("If either scores met, the counter is broken and no data is
  collected") this needs an explicit control-scope ruling (backticked allowlisted paths only), not
  a counter edit. The live rows are unaffected (A4 and the freeze measure both resolve).
- C2: (a) junk quotes → `failed=quotes` holds (selftest + my arm); (b) sha mismatch → `copy=bad`
  holds; (c) frontmatter missing → **`sources=ok`** when the four tokens exist in the body, so the
  control holds only under a positional reading of "frontmatter".
- No control arm produced a green where green was unintended on live data; all findings above are
  fixture-only.

## 7. Detection / report boundary bleed scan

- 41 `w1/*.md` reports scanned (grep for remediation, provider-death, `C2=met`, fleet writes; 8 read
  in full: Connector60, Critic26/Critic30, MutationTester33/35/38, Reviewer12, Scout57,
  Scribe49/Scribe50). Every `C2=met` occurrence is fixture-framed; Mo58Scribe49 explicitly declines a
  lane measurement because the entry is untracked. No report claims remediation, a commit, a fleet
  write, or provider death; the detection-only boundary is respected.
- Contract/entry limit language is present and accurate: entry lines 8 and 19 disclaim provider
  death / health verdict / authoritative settlement; S550's stop rationale says "no lane-health or
  authoritative settlement claim".
- Documentation precision nit (detection only): `corpus/lessons/round-58.md` Mistakes row 1 says C1
  "resolves row paths with `git cat-file -e`" and its selftest "includes … nonexistent-pointer
  refusals" — true only for backticked allowlisted paths (A1/A2, Critic30). Not a data defect.
- Formatting nit: the new round-58 search-log line in `corpus/SOURCES.md` is appended with no blank
  separator before/after, unlike every prior entry (visible in `git diff corpus/SOURCES.md`).

## 8. Live-artifact snapshot (time-bounded; seats were still running)

- `corpus/knowledge/driver-events-r58.md` sha256 `e7fc469cf4ffd86a6ba14e8b6e2f66ec6366e46f853b0733553ee414c81a9e55`,
  19 lines, 8 claim lines (entry:10–17). I re-located all 8 quotes against the tool: 8/8 are
  substrings of the cited lines (96,101,103,123,135,145,152,159). Five class tokens each appear
  once (launch 3×, complete/wrap/lane-dead-no-report/launch-fail 1× each).
- Strict-wording risk for the judge: only K3–K7 (5 claims) are directly per-event-class claims;
  K1 (`other_lines`), K2 (field split) and K8 (malformed timestamp) are classification/grammar
  claims. The contract asks for "≥8 located claims on the event-class semantics"; the counter's 8
  and the contract's 8 are the same 8 rows, but a strict topical reading yields 5–6. Not a defect —
  an interpretation the judge should fix before scoring.
- S550 row (worktree line 330): tier A, `mined`, used-by names the entry, anchor 95–163, sha
  `6b3dba74…`; anchor/search-log/gate quote for the row (`other_lines += 1  # ts-first driver prose
  (steer, watchdog tick, ...)`, line 101) is byte-faithful in `corpus/lessons/round-58.md`.
- If landed unchanged, C2 prints `C2=unmet claims=0` because of B3; blocker already routed by
  Mo58Scribe49 F1.

## 9. Out of scope / limits

- No post-landing revision exists (entry is untracked), so no end-of-wave counter run; C2's landed
  value is a forward-looking statement, not an observation.
- I did not score axes, did not re-judge claims, did not edit or propose edits to counter bytes.
- Not inspected in full: the other 33 `w1` reports (grep-screened only); round-55 and earlier
  contracts; fleet `LOG.md`/SCORECARD history beyond the register/stub ranges and MANIFEST[832].
- Peer receipts are labeled as such above; everything in §1, §3, §4, §5 (census), §8 is first-hand.

## 10. Commands (exact, read-only unless stated)

```
git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --oneline -8
git show fe880112:SCORECARD.md | sha256sum           # vs b783d0b8 blob
git cat-file -e fe880112:<path>                      # 4 row pointers + 2 absent artifacts
TMPDIR=<scratch> python3 .ufo/waves/round-58/count-c1.py {fe880112,HEAD}; --selftest
TMPDIR=<scratch> python3 .ufo/waves/round-58/count-c2.py {fe880112,HEAD}; --selftest
scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori    # rc 0, mori ok
python3 <scratch>/falsify.py, falsify2.py, minreg.py      # frozen-counter imports over scratch fixtures
git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff corpus/SOURCES.md corpus/README.md
```
