# Mo60Scout83 — assimilation / considerthese

**Line:** `Assimilation: none`

No staged `merge/mori` theme matches round-60 instrument-hardening (C2 H1–H5, C3 G1–G3). The 2026-10-26 absolute-host-path item is a lesson line, not an assimilation theme and not a claim. It holds for the frozen instruments and does not hold for the post-freeze spec builder.

Pins: freeze `ac496c7cde8cad965079858accae3bedfe4a73f2`; entering `ddfb12fb0838b4307c445194a844f0c4b1950195` (round-60 tree absent); lane HEAD when read `b3c256138f00c704d5aa56eb0332d74506502ef2`. Disk-guard `check` rc 0 (`/tmp` 14%, `/var/tmp` 38%, `/fast/scratch/hyaku` 26%, soft 70%). Read-only. No LSP: the question is theme identity, not a symbol contract.

## Assimilation

Package (`/home/vgpnk/Projects/shokuknow/merge/mori/MERGE-REPORT.md:3-9`): nothing written into the lane; 136 rows accepted, 0 refused, 80 knowledge entries. `find` of that tree: 83 files (80 entries + `MERGE-REPORT.md`, `MERGE-REPORT.json`, `SOURCES.append.md`).

Every entry has a `coverage-map:` line (80/80). Counts, read from those lines:

| n | coverage-map as written | subject (from a ground line actually read, or the title) |
|---|---|---|
| 47 | FR1 | kernel OOM event-time attribution and fleet correlation |
| 8 | FR12, FR1 | PSI / census level-pairing, plus FR1 |
| 5 | FR5, FR1 | watchdog identity; census selection |
| 5 | FR2 | quota: `df` cannot see exhaustion (`quota-observability-r38.md:13-14`) |
| 4 | FR12, FR5 | census selftest level pins; standing sampler |
| 2 | FR4 | a recorded verdict is a declared policy |
| 2 | FR5 | absent-vs-dead probe; unit identity lifetime |
| 1 | FR13, FR1 | OOM victim selection has no container context |
| 1 | FR3, FR4 | wave-settlement amendment: vendor workflow status (`wave-settlement-r20.md:11-12`, sources S475/S476) |
| 1 | FR1, FR12 | agent memory peak |
| 1 | FR8 | alarm threshold is not an instant |
| 1 | FR13 | three named OOM tracepoints |
| 1 | FR2, FR8 | quota counter is lagged |
| 1 | journal-store runway (not an FR id) | `--list-boots` vs what the boot produced |

Round-60 instrument-hardening, from the frozen contract (`contract.md:25-28`, `:72-87`, `:103-112`), is: H1 `grammar:` blocks, H2 distinct spans ≥8, H3 non-degenerate texts, H4 per-copy row binding, H5 attributed drift on `tools/mori-settlement-scan.py`, G1 pin-gated execution, G2 containment, G3 expect-table tamper. None of the maps above is that subject.

Lexicon control over the whole package (bodies included) for `entry-claims|tool_sha|tool_ok|expect_tamper|mori-pin-check|mori-entry-claims|containment|grammar:|distinct byte|absolute host path|QUALITY 127|instrument-hardening|pin-gated`: no matches. Same for `entry-claims-check|mori-pin-check|expect_tamper|tool_sha|QUALITY 127|absolute host` in `SOURCES.append.md`.

Near misses, rejected:

- `census-field-enforcement-r48.md:2,7-8`, `selftest-cannot-tell-levels-r49.md:2,7-8`, `census-level-pins-change-r49.md:2,9-10` — `tools/mori-census.sh` selftest pins (`MORI_CGROUP_*` all pointing at one fixture). FR5/FR12. Not H1–H5 or G1 sha pins.
- `negative-result-patterns-r42.md:2,7-12` — a cgroup `memory.events` sweep whose shell pattern matched nothing (FR1). Calibration-adjacent method, not a verifier.
- `wave-settlement-r20.md` — name collides with the H5 settlement-scan arm; the staged text is Aliyun/Alibaba workflow status (FR3/FR4), not `extra_keys` attribution.
- The word "instrument" inside the package means the runner's pre-kill watch or `memory.stat`, not a lane counter.

## considerthese absolute-host-path item

`considerthese/2026-10-26.md:16-26` (lesson 1) and `:57-59` (suggestion 4 restating 2026-10-25 suggestion 2): `conform.py:69` hardcodes `LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"`; QUALITY 127 exists; the stated scope was still 13 files; r48/r49 spec builders repeat the path. This is lane self-reflection, not a merge theme. Contract `:139-143` already classifies it as a lesson line, not a claim. That classification is right.

Frozen instruments, both revisions (blobs identical freeze to HEAD):

```
git grep -c -F '/home/vgpnk' ac496c7c -- \
  .ufo/waves/round-60/count-c1.py count-c2.py count-c3.py \
  build-fixtures-r60.py tools/mori-entry-claims-check.py
# rc 1, no hits
git grep -E '/home/|/fast/scratch' ac496c7c -- <same five>
# rc 1, no hits
```

Same five blobs at `b3c25613`. Entering `ddfb12fb`: `git grep` of `.ufo/waves/round-60` rc 1 (tree not present).

Not instruments, but they do contain the path at the freeze: `contract.md:147-148` (census command) and `evidence/census-start.txt:26` (the path the census printed).

Not honored, and this is the class the reflection named. `build-w1-spec.py` is absent at `ac496c7c` (`cat-file -e` says the path exists on disk but not in that commit) and tracked at `b3c25613` with 7 `/home/vgpnk` hits, including:

- `build-w1-spec.py:9` `LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"`
- `build-w1-spec.py:10` `FLEET = "/home/vgpnk/Projects/shokunin"`

Generated `w1-spec.json` and `w1-dispatch.json` at the same HEAD: 50 hits each. Path-limited `git log ac496c7c..b3c25613 -- .ufo/waves/round-60` is only `76904b21` (dispatch payload) and `398d3225` (C1 data). So "no r60 instrument carries an absolute host path" (`contract.md:6-7,141-142`) is true for the counters, the fixture builder, and `tools/mori-entry-claims-check.py`, and false for the spec builder. The lesson line should say that split. It still does not make the item a claim, and it still does not assimilate anything.

## Unknowns

Bodies of the other 76 entries were not re-read line by line. The coverage-map tally plus the lexicon grep is the evidence they do not discuss entry-claims hardening under another header. QUALITY 127's current check-clause scope was not re-derived this seat; the reflection's own statement of that scope is what is cited.
