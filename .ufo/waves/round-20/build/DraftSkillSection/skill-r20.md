## Wave settlement scan and drift re-pin (r20)

Detection only. The settlement scan is read-only; the re-pin is an L1 ritual. Neither starts, steers, retries or settles a seat.

| Intent | Correct surface | Never | Expected output |
|---|---|---|---|
| When to run the settlement scan | `python3 tools/mori-wave-settlement.py scan --lane-root <lane> [--fleet-root <fleet>] [--out FILE]`, after the census `SURFACE waves` age shows no recent writes, and before any closure note that says a wave settled | running during active writes (premature settlement); copying or moving reports to flip a member to `present` | per-wave `state`, per-member counts, sorted `missing` names; `mori-wave-settlement-v1` JSON, byte-identical on re-run |
| `settled` | every member `present` (regular, non-symlink, size > 0); exit 0 | reading it as "the work is correct" (it counts non-empty files only) | `missing=0` |
| `no-spawn` | dispatch with `taskCall: null`; exit 0 | treating it as an unsettled wave | `members=0` |
| `partial` | at least one `present`, at least one not; exit 1 | calling the missing seats dead, failed or killed; auto-re-dispatching | list `missing`; any re-dispatch decision belongs to kumitate |
| `unsettled` | zero `present`, at least one member; exit 1 | inferring a crash from zero reports at dispatch time | re-scan after the stall threshold |
| `unavailable` | no member had a parseable, safe report path; exit 1 | reading an unsafe path, following a symlink, or reporting zero | `unsafe` / `unparsed` counts |
| `empty` / `misrooted` | `empty` = size 0; `misrooted` = report exists only under `--fleet-root` at the same relative path | counting either as `present` | both count as not present; fix routing, not counts |
| `unsafe` / `unparsed` | `unsafe` = absolute, `..`, or escapes the lane root; `unparsed` = no trailer line | reading an `unsafe` target | counts only |

Exit map: 0 all discovered waves `settled` or `no-spawn`; 1 any other state; 2 usage error or unreadable lane root. Exit 1 means *not settled*, never *failed*.

**Never conclude dead, failed or killed.** The output must not contain those words (oracle `no_vocab`). A missing report only means no non-empty file sat at the trailer path at scan time. Closure evidence is the watchdog `complete`/`wrap` line or a committed report (silence grading, r2); this probe is neither.

**Drift re-pin ritual (r20 C1; L1 only).** `corpus/evidence/baseline-r10-20261015T2231Z.json` stays byte-unchanged.

1. Measure once at the measured commit: `bash tools/mori-census.sh --drift corpus/evidence/baseline-r10-20261015T2231Z.json > DRIFT` (census SHA must be `87b8d680…ab28`; about 2 min, heavy CPU).
2. Count unclassified tokens with the `comm` recipe in the r20 contract against `corpus/evidence/drift-classification-r20.json`; it must be `0` before any pin.
3. Classify every token as exactly one of `census-schema-change | roster-change | live-state | census-regression`, each with an evidence pointer (commit, path:line or receipt) and a one-line reason.
4. Any `census-regression` token: stop, report it verbatim, do not pin.
5. Otherwise `bash tools/mori-census.sh --pin corpus/evidence/baseline-r20-<UTC>.json`, recording the reason.
6. Re-run `--drift` against the new baseline; record rc and tokens whatever they are. A non-`none` result is the measured stability window: report it, never suppress it.

Never edit `tools/mori-census.sh`. `--pin` writes only its path; `--drift` writes nothing.
