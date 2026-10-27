# Mo58Connector59 — C1 MANIFEST binding attack + connector sibling-overlap (round 58)

Freeze revision: `fe8801120a67c1a6b8899d7d0423839caa09e7d0`. Entering: `b783d0b892637ce8d20f188cad20e4d8913ca635`.
Frozen counter: `.ufo/waves/round-58/count-c1.py` (read only; not modified; sha256 not re-derived).
Receipt: `.ufo/waves/round-58/w1/Mo58Connector59.receipt.txt`; fixture driver: `.ufo/waves/round-58/w1/Mo58Connector59.attack.py`.

## Verdict

The frozen C1 counter is **bypassable on the MANIFEST binding arm**. Renaming or re-keying the two round-56 rows, and
spoofing the MANIFEST hint text, all still score `C1=met`. The counter binds the register only by the presence of key
strings and substrings, never by content-to-key identity. Its MANIFEST arm also reads the **live fleet working-tree file**,
not the measured revision, so the verdict at a fixed `R` changes when a sibling lane commits to `MANIFEST.json`.
Nothing here changes the frozen target output on the real register at `fe8801…`; the real register is met and correct.
These are counter false-greens under adversarial edits, reported as detection only.

## Evidence: real register at freeze (no edit)

- `python3 .ufo/waves/round-58/count-c1.py fe8801120a67c1a6b8899d7d0423839caa09e7d0` → `C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none`, rc 0.
- `python3 .ufo/waves/round-58/count-c1.py b783d0b892637ce8d20f188cad20e4d8913ca635` → also `C1=met … rev=b783d0b8…`, rc 0. The SCORECARD register is identical at both (blob `fded56fc…`), so the counter's "met" at entering does not discriminate round-58 work on the register; the only before/after delta is the counter file's existence.
- Selftest: `C1_SELFTEST pass=4 fail=0`, rc 0.
- Active register `## Capabilities` at SCORECARD.md:1951 (preamble line 1953 holds the bind sentence). Stub at :596. Rows at :1989 (`[0]`, vote binding, pointers `tools/mori-vote-bind.py` and `.ufo/waves/round-56/evidence/c2-at-landed.txt`) and :1990 (`[1]`, driver-liveness, pointers `tools/mori-driver-liveness.py` and `.ufo/waves/round-56/evidence/c1-at-landed.txt`). All four pointers exist at freeze (`git cat-file -e`).
- MANIFEST `rounds[832]` (fleet root, index 832, `round` field 56, the only `lane=="mori"` round 56 entry) has `capabilities_added[0]` = `dual-shape seat-output vote binding (…)` and `[1]` = `strict per-event driver-liveness probe over .ufo/watchdog.log (…)`.

## Fixture arms (scratch only; each fixture = own throwaway git repo under `$TMPDIR/<arm>/lane`, sibling `MANIFEST.json` at `$TMPDIR/<arm>/`; `git -C` throughout; real repo not touched)

| arm | edit to the freeze SCORECARD / MANIFEST | frozen counter verdict | reading |
|---|---|---|---|
| m0 | none (control; evidence tree copied in) | `C1=met` rc 0 | fixture faithful |
| m1 | swap the **capability text and evidence** between keys `[0]` and `[1]` (key cells stay in place) | `C1=met rows=2 pointers=ok manifest=ok binding=ok` rc 0 | **false green**: key `[0]` now describes the driver probe and cites only `tools/mori-driver-liveness.py`, yet passes against MANIFEST `[0]`=vote binding |
| m2 | swap the **key cells** (text stays under the other key) | `C1=met` rc 0 | **false green**: key-to-content mismatch not detected |
| m3 | MANIFEST `capabilities_added` = `["RETRACTED: not a vote binding", "RETRACTED: not the driver-liveness probe"]` | `C1=met` rc 0 | **false green**: `manifest` arm is `hint in caps[j]` substring (`MANIFEST_HINTS` = "vote binding", "driver-liveness"); negated text passes |
| m4 | MANIFEST `capabilities_added` order swapped | `C1=unmet … failed=manifest,manifest` rc 1 | control: positional order is enforced |
| m5 | junk row `rounds[999].capabilities_added[0]` whose **evidence cell** contains `` `rounds[832].capabilities_added[0]` `` (real `[0]` row removed) | `C1=met rows=2` rc 0 | **false green**: row selection is substring match over whole line (`any(k in ln for k in R56_KEYS)`), not key-column match |
| m6a | `[0]` evidence `` `scripts/no-such-tool.sh` ``, `[1]` evidence `` `./tools/no-such-tool.py` `` (both nonexistent) | `C1=met pointers=ok` rc 0 | **false green**: pointer check only applies to paths starting `.ufo/`, `tools/`, `corpus/`; any other form (`scripts/`, `./`, absolute, `../`, slash-less) is skipped |
| m6b | `[1]` evidence `` `tools/no-such-tool.py` `` | `C1=unmet pointers=bad` rc 1 | control: in-prefix missing path caught |
| m7 | copy of the whole active section inserted **before** the stub at :596 (first `## Capabilities` whose first 12 body lines hold the sentence); real `[0]`/`[1]` rows deleted from the real active section | `C1=met` rc 0 | **false green**: binding is "first heading with the sentence", not table identity; the copy and the real section are indistinguishable to the counter |
| m8 | identical SCORECARD at freeze; only the fleet `MANIFEST.json` changed (`caps[0]`="retracted") | `C1=unmet manifest=bad` rc 1 | **non-revision-bound**: MANIFEST is read from `FLEET/MANIFEST.json` working tree (`FLEET = dirname(LANE)`), never `git show R:…`; same rev, different verdict |
| m9 | `[0]` evidence `` `tools/fixtures` `` (existing directory) | `C1=met pointers=ok` rc 0 | directory accepted as evidence (`cat-file -e` passes for trees) |
| m10 | no MANIFEST file | `C1=unmet manifest=bad` rc 1 | control: missing fleet file caught |

Attack-share cross-check (no duplication of effort): Mo58Critic30 and Mo58Reviewer02 independently found the prefix-skip and
absolute/wrong-tree pointer gaps (m6a); those are consistent with this receipt. The row-key swap (m1/m2), hint spoof (m3),
substring row selection (m5) and first-heading duplicate (m7) are new to this seat's arm.

## Sibling-surface overlap and refusal boundaries (connector duty)

1. **Shared MANIFEST is a live cross-lane write surface.** `git -C /home/vgpnk/Projects/shokunin log -- MANIFEST.json` shows
   consecutive fleet ledger commits from other closures: `d8ec11dc` (14:29:52, revenger r71), `80cff289` (13:43:36, mado r53),
   `217c119a` (13:43:30, mori r57), `342dfc74` (13:31:06, kotoba r75). The C1 manifest arm reads that file directly, so a sibling
   closure can flip `manifest=` at a fixed `R` (m8 demonstrates the mechanism). Boundary: the C1 claim is not reproducible from
   the lane repo alone; it depends on fleet HEAD state. Not remediated here (detection only).
2. **Two frozen counters in this lane disagree on the same register at F.** `.ufo/waves/round-35/count-c1.py fe8801…` prints
   `C1=unmet rows=20 matched=18 extra=2 mismatches=2` (oracle `manifest_rev=37b51a243302`, register `'## Capabilities'`), because
   its oracle predates the round-56 closure; the round-58 counter prints `met`. Both are "frozen". Neither is wrong on its own
   predicate, but the lane has no single authority for the register. Report only; not reconciled.
3. **Round-57 counter** (`.ufo/waves/round-57/count-c1.py fe8801…`) prints `C1=unmet rows=0 evidence=bad` — the known wrong-table
   false negative (first `## Capabilities`). Consistent with the contract's routed defect 1. (Its rc was not captured cleanly in
   this run; the pipeline masked it. Do not cite rc from this seat.)
4. **Parallel round-58 sibling lanes** (`chousa`, `kake`, `kotoba`, `kotodama`, `kumitate` each carry `.ufo/waves/round-58/`) have
   their own wave/build surfaces; none references `rounds[832]`, `count-c1.py` or the mori register. No overlap with the C1 arm found
   by a targeted search of their round-58 trees. Their `w1-spec`/`build-spec` files are not to be read as mori evidence.
5. **C2 driver-event overlap (out of this seat's arm, noted for boundary only):** `tools/mori-driver-liveness.py` event classes are
   parser-observed syntax; kumitate owns lifecycle/dispatch interpretation (`kumitate-shokunin/PROVINCE.md`), tsukuroi owns the
   driver/firmware plane. Mo58Reviewer13 and Mo58Scout55 record the same boundary; no mori-owned claim should use "driver" as a lane
   health or dispatch outcome. Refusal boundary: this report makes no health, settlement or provider-death inference.

## Assumptions and limits

- Attack fixtures used copies of the committed evidence tree at `fe8801…` (`git archive`) and a rewritten SCORECARD; they do not
  exercise live fleet MANIFEST beyond m8's documented mechanism.
- Revision hashes in the receipt differ between runs (fixture commit timestamps). Verdict lines are the evidence, not the hashes.
- The rc of the round-57 check above was masked by a pipeline; treat as unobserved.
- `[INFERENCE]`: the m5/m7 constructions are plausible only for an author who writes SCORECARD; the frozen counter is not
  designed to resist a hostile lane author (the contract's stated residual). They are reported as counter predicate gaps, not as
  evidence that round-58 work is fraudulent.

## Suggested counter-side changes (drafts only; frozen counter NOT edited — kill rule applies)

- Bind row content to key: require `[0]` row's capability cell to contain the MANIFEST `[0]` text's distinctive token and the
  `[1]` row the `[1]` token; compare key cell by exact match, not substring anywhere on the line.
- Read MANIFEST at revision: `git -C <fleet> show <fleet-rev>:MANIFEST.json` with a recorded fleet commit, or pin a copy
  under `corpus/evidence/` with sha256 at freeze.
- Pointer check: apply `git cat-file -e R:<path>` to every backticked token containing `/` or a known extension, not only the three prefixes; reject `./`, absolute, and `..`.
- Require a blob (`cat-file -t` = blob) for evidence pointers, not a tree.
- Bind the table identity to a stable anchor (heading occurrence count == 1 for the active sentence), or fail on duplicates.

These are proposals for a successor counter under a new freeze; they are not applied.

## Restoration

No production, corpus, SCORECARD, LOG or lane-VCS files changed. No commits. No fleet or sibling writes. Scratch fixtures were
created under `/fast/scratch/hyaku/mori-r58/Mo58Connector59/` and removed before yield.
