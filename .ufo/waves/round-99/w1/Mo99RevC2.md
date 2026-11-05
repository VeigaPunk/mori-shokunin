# Mo99RevC2 — C2 review (mori round 99, wave w1)

Reviewer seat. Scope: `git diff 73308ff6 5013f0be -- SCORECARD.md`, frozen counter
`.ufo/waves/round-99/count-c2.py`, transform `.ufo/waves/round-99/candidate/apply-c2.py`.
Lane untouched (read-only git only); mutations ran in scratch clones
(`/fast/scratch/hyaku/mori-r99/Mo99RevC2/fixture{,2}`, toplevel asserted before every commit).

## 1. Counter before/after (claim reproduction) — PASS

```
python3 .ufo/waves/round-99/count-c2.py 73308ff6…  →  axis coverage expect=round_98 pointer=missing
… (operability, depth, freshness, calibration all missing; adjacency ok)
C2=unmet mismatches=5 cells_unchanged=yes gate=rc1 mismatched_axes=coverage,operability,depth,freshness,calibration rev=73308ff6e5c9  (rc=1)
python3 .ufo/waves/round-99/count-c2.py 5013f0be…  →  all six pointer=ok
C2=met mismatches=0 cells_unchanged=yes gate=ok mismatched_axes=- rev=5013f0be8ac9  (rc=0)
```
Byte-identical to `evidence/before-c2.txt` (in landing commit, blob 4f754b4410f9 at both freeze
462cef1 and landing) and `evidence/landing-c2.txt` (on disk; untracked `??` — it cites the rev it
measures, so it cannot be inside that commit). Controls receipt `evidence/controls-r99.txt`
(in landing): K0c/K1c/K2c/K3c/K4c unmet AS_EXPECTED, P1c met AS_EXPECTED, `CONTROLS_DONE unexpected=0`.
Frozen-file binding: count-c2.py / contract.md / apply-c2.py / before-c2.txt git-blob-identical at
freeze and landing; controls header digest `count-c2.py=b9b58acae05f0d88` = sha256-16 of the bytes I ran.

## 2. Transform equivalence — PASS

`python3 candidate/apply-c2.py <copy of entering SCORECARD>` then `diff` vs landing SCORECARD:
empty → **apply-c2(entering) == landing byte-for-byte**. The whole SCORECARD delta is exactly the
six `## Axes` Evidence cells (five moved) plus the two Last-change prepends; Score cells and the
other four Last-change cells byte-equal entering (verified cell-by-cell). `score held` is factual:
gate at entering reports `columns_unchanged=yes`, i.e. Score+Evidence bytes still equal the r95-era
base after r98, so r98 moved no score.

## 3. Pointers open to the right grading line — PASS (all six)

| axis | pointer | cited line at landing | verdict |
|---|---|---|---|
| coverage | `round-98-verifier-spotcheck.md:89` | `\| coverage \| improved \| C1 above \|` | r98's own verdict-table row for coverage |
| calibration | `round-98-verifier-spotcheck.md:90` | `\| calibration \| improved \| C2 above \|` | r98's verdict row for calibration |
| operability | `round-97-verifier-spotcheck.md:78` | `\| operability \| improved \| C1 above \|` | r97's verdict row for operability |
| freshness | `round-97-verifier-spotcheck.md:79` | `\| freshness \| improved \| C2 above \|` | r97's verdict row for freshness |
| depth | `round-86-verifier-spotcheck.md:145` | `\| depth \| **improved** \| 64-row classification … \|` | r86's verdict row for depth |
| adjacency | `rounds[398]` (no r19 spot-check file: `cat-file -e` → does not exist at landing) | — | token present in cell |

None cites a different claim's line. r98's closure prose confirms the table ("Verdict: **coverage
improved** … capability `user-namespace runway and sysctl-write scan` enters", "Verdict:
**calibration improved**").

## 4. rounds[] indices in pinned MANIFEST (4ad377ea) — PASS

Re-derived expectations from all 60 admitted mori closures in `git show 4ad377ea…:MANIFEST.json`
(1390 rounds):
`coverage (98, 1389, improved)`, `operability (97, 1384, improved)`, `depth (86, 1205, improved)`,
`freshness (97, 1384, improved)`, `calibration (98, 1389, improved)`, `adjacency (19, 398, improved)`.
Row dumps confirm: rounds[1389]=mori r98 closure admitted {coverage improved, calibration improved,
others unchanged}; rounds[1384]=r97 {operability, freshness improved}; rounds[1205]=r86 {depth
improved (also operability+calibration — superseded by 97/98)}; rounds[398]=r19 {adjacency improved}.
No higher admitted closure grades any axis, so the five pointers really are "latest admitted".

## 5. Last-change prefix convention vs r50/r79 — PASS

SCORECARD.md:21–27 (Round-50 correction): "Each cell now leads with the latest round and keeps the
older history after a `;`". :31–40 (Round-79 correction): "Each cell now leads with its latest
admitted round and verdict word and keeps its older history after the first `;`". r98's own landed
precedent (r98 lesson line 74): new cell = `round 97 (improved, score held); ` + old cell. The two
landing cells are exactly `round 98 (improved, score held); ` + entering bytes — same convention.

## 6. Passing-mention resistance — counter is evadable in theory; landing unaffected

Fixture experiments on a landing clone:
- **mutA** — coverage pointer → `round-98-verifier-spotcheck.md:91` (`| operability | unchanged | …
  the new tool is counted under coverage |`; names coverage, no verdict word):
  `axis coverage expect=round_98 pointer=bad-line`, `C2=unmet mismatches=1` → **rejected**.
- **mutB** — same line edited to `…counted under coverage (improved elsewhere) |` (passing mention
  co-locating axis + verdict word): `axis coverage … pointer=ok`, `C2=met mismatches=0` → **accepted**.

So the pointer check is purely textual: [axis word ∧ verdict word] on the cited line. It cannot
distinguish "grades the axis" from "names the axis in passing next to a verdict word". This is a
residual weakness of the frozen counter, **not exercised by the landing**: all five cited lines are
the closures' own verdict-table rows for the graded axis (§3). A future counter could require the
axis in the first table-cell position of the cited line.

## 7. Lead-round binding — gate load-bearing and sufficient

`last_ok` in count-c2.py accepts ANY `round N (improved|harmed, score held); ` prefix; the embedded
gate run (`--base rev`, expectation from the pinned MANIFEST) is what binds N:
- **mutD** — single prepend `round 97 (improved, score held); ` on coverage (expect 98):
  `pointer=ok, cells_unchanged=yes`, `gate=rc1` → `C2=unmet mismatches=0` → **caught by gate only**.
- Gate `--selftest`: `CALIB_SELFTEST pass=11 fail=0` (rc 0); sha256 at landing == entering ==
  GATE_SHA `662fafde…`.

## 8. Gate with DEFAULT --base (66c5518e) at landing — columns_unchanged=no is expected, no axis harmed

```
python3 tools/mori-scorecard-calibration.py 5013f0be…   (all defaults)
→ six lines state=ok, C1=unmet axes=6 mismatches=0 columns_unchanged=no rows=6 rev=5013f0be8ac9 (rc=1)
python3 tools/mori-scorecard-calibration.py 73308ff6…   (entering)
→ C1=unmet axes=6 mismatches=2 columns_unchanged=yes (coverage round_80≠98, calibration round_93≠98)
python3 tools/mori-scorecard-calibration.py 5013f0be… --manifest <pinned> --base 5013f0be…
→ C1=met axes=6 mismatches=0 columns_unchanged=yes (what the counter runs; gate=ok)
```
The r96 predicate pins Score+Evidence bytes to base 66c5518e (r95-era); the Evidence-cell move is
exactly what this wave's frozen contract C2 sanctions (executing the r98 D3 finding "five cells cite
closures that later admitted closures supersede"). So `columns_unchanged=no` is the designed
detection firing on a sanctioned change — **expected consequence, not a harm**: no score moved, all
six leads are now correct (mismatches 2→0 under the default base), and the counter's gate invocation
(`--base rev`) is C1=met. The SKILL.md registry row (line 1447) already discloses the base pin
("Score and Evidence cells pinned to base 66c5518e…"). Residual: the bare documented command
`python3 tools/mori-scorecard-calibration.py <rev>` now exits 1 at landing (it already did at
entering, via mismatches=2); a future round must re-freeze the gate's base — outside this wave.

## 9. Regression sweep

`.ufo/waves/round-79/count-c2.py` prints `C2=unmet axes=6 mismatches=5 errors=0 rows=46 through=78`
identically at entering and landing — pre-existing stale round bound (runs "through 78"), unchanged
by this landing; not a regression. Its exit code was not captured (pipe); the identical stdout at
both revs is the evidence used.

## Unrun checks

- The `MANIFEST.json@63729047` blob reference inside the (unchanged) adjacency cell was not
  re-resolved; P2 keys on `rounds[398]` in the pinned manifest, which was verified.
- `controls-r99.py` was not re-executed; its frozen receipt (`unexpected=0`) is cited as-is.
- r50/r79 counters' exit codes not captured (output text used).

## VERDICT

VERDICT C2 holds: counter unmet(5)/met(0) at entering/landing exactly as claimed and as frozen in the
receipts; apply-c2 reproduces the landing byte-for-byte; every pointer opens to that closure's own
verdict row for that axis; rounds[1389]/[1384]/[1205]/[398] correct in the pinned MANIFEST;
Last-change prepends match the r50/r79 convention; gate with default base reporting
columns_unchanged=no at landing is the expected consequence of the contract-sanctioned Evidence move
(r98 D3), harming no axis. Residual (counter, not landing): passing-mention co-location of axis+verdict
words on one line can satisfy the pointer check (mutB), and only the embedded gate binds the lead round.
