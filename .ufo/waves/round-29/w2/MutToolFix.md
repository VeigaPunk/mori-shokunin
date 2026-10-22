# L1 tool-fix.py mutation probe

## Scope and detector

I cloned the lane into `/fast/scratch/hyaku/mori-r29/w2/MutToolFix/repo`, checked out detached `8809a3fe1eaa87a0afa177a15263d174378e7462`, and copied `/fast/scratch/hyaku/mori-r29/L1/judge/tool-fix.py` to the clone as `tools/mori-oom-killers.py`. The clone command reported `HEAD is now at 8809a3f ...`; the initial copy hash was `2609103210967b04cb7fab6e67886291a4ae8b336df64ec8823c01732b84e187` (`sha256sum`). Mutations target the changed logic in `fix.diff:3-96`.

For every state, the detector was `python3 tools/mori-oom-killers.py --selftest --cases tools/fixtures/mori-oom-killers/<file>`, in order: `cases-a2-r29.json` (r29), `cases-a2.json` (a2), `cases.json` (core), `cases-supplementary.json` (supp). Every mutant was one source-point change; all four cases files were run before restoring the pristine bytes.

No tools were installed or updated; the mutation probe used the available Python 3 runtime.

## Pristine and restored output

Pristine output: r29 `FAIL 18/24`, a2 `PASS 30/30`, core `PASS 32/32`, supp `PASS 32/32`. The six pre-existing r29 failures were `r29-a2-07-dryrun-then-real-missing-enter`, `r29-a2-07-real-then-dryrun-zero-enter`, `r29-a2-07-real-dryrun-real-missing-enter`, `r29-a2-10-inactive-lone-missing-stamp`, `r29-a2-10-failed-stamped-positive`, and `r29-a2-10-not-found-earlier-stamped-positive` (selftest output). A mutant failing only one of those is **inconclusive**, not killed. Restored output was identical: r29 `FAIL 18/24`; the other three `PASS 30/30`, `PASS 32/32`, `PASS 32/32` respectively.

| Mutant | Single-point defect | Selftest output (r29 / a2 / core / supp) | Killed by (new failing case IDs; baseline failures excluded) | Survived? |
|---|---|---|---|---|
| M01 | Drop `close_segment()` at a version boundary. | F17/24; P30/30; P32/32; P32/32 | r29: `r29-a2-07-dryrun-inside-scope` | No |
| M02 | Drop the final `close_segment()`. | F6/24; F20/30; F26/32; F26/32 | r29: `r29-a2-07-dryrun-before-boundary`, `r29-a2-07-two-prior-invocations`, `r29-a2-07-dryrun-inside-scope`, `r29-a2-07-real-before-scope-current-dryrun`, `r29-a2-07-real-escalation-before-boundary-current-dryrun`, `r29-a2-07-earlier-real-dryrun-then-current-real`, `r29-a2-07-dryrun-before-real-signals`, `r29-a2-07-real-before-dryrun-signals`, `r29-a2-07-all-dryrun-multiple-sends`, `r29-a2-10-zero-unbounded-mixed-sigterm`, `r29-a2-10-zero-unbounded-mixed-sigkill`, `r29-a2-10-stamped-send-survives`; a2: `a2-01-suppressed-in-scope-with-action`, `a2-03-group-kill-one-with-sigterm-action`, `a2-03-group-kill-three-after-earlier-invocation`, `a2-04-dryrun-sigterm-send-not-positive`, `a2-04-dryrun-two-sigterm-sends-counted`, `a2-04-dryrun-send-with-oomd-notices`, `a2-06-active-earlier-and-current-send-acted`, `a2-07-earlier-real-then-current-dryrun`, `a2-07-earlier-dryrun-then-current-real`, `a2-07-three-invocations-dryrun-in-the-middle`; core and supp: `c03-scope-boundary-exactly-at`, `c04-incomplete-scope-with-action`, `c11-byte-array-message-action`, `c12-byte-array-invalid-utf8`, `c13-sigterm-action`, `c14-sigkill-action` | No |
| M03 | Admit stamp-less records into the unbounded active-unit scope. | F15/24; P30/30; P32/32; P32/32 | r29: `r29-a2-10-unbounded-missing-stamp-alone`, `r29-a2-10-zero-unbounded-mixed-sigterm`, `r29-a2-10-zero-unbounded-mixed-sigkill` | No |
| M04 | Keep stamp-less records in `earlier` instead of excluding them. | F6/24; F22/30; P32/32; P32/32 | r29: `r29-a2-07-two-prior-invocations`, `r29-a2-07-dryrun-inside-scope`, `r29-a2-07-real-before-scope-current-dryrun`, `r29-a2-07-real-escalation-before-boundary-current-dryrun`, `r29-a2-07-earlier-real-dryrun-then-current-real`, `r29-a2-07-real-before-dryrun-signals`, `r29-a2-10-unbounded-missing-stamp-alone`, `r29-a2-10-zero-unbounded-mixed-sigterm`, `r29-a2-10-zero-unbounded-mixed-sigkill`, `r29-a2-10-unclocked-send-alone`, `r29-a2-10-stamped-send-survives`, `r29-a2-10-oomd-evidence-survives`; a2: `a2-06-active-earlier-invocation-sends-quiet`, `a2-06-inactive-earlier-invocation-sends-acted`, `a2-06-active-earlier-and-current-send-acted`, `a2-07-earlier-real-then-current-dryrun`, `a2-07-three-invocations-dryrun-in-the-middle`, `a2-09-removed-unit-single-sigterm-send`, `a2-09-removed-unit-two-invocations-mixed-sends`, `a2-09-removed-unit-three-sends-oomd-active` | No |
| M05 | Reset the segment's `dryrun` flag to `True`. | F10/24; F24/30; F27/32; F27/32 | r29: `r29-a2-07-dryrun-before-boundary`, `r29-a2-07-two-prior-invocations`, `r29-a2-07-dryrun-inside-scope`, `r29-a2-07-earlier-real-dryrun-then-current-real`, `r29-a2-07-dryrun-before-real-signals`, `r29-a2-10-zero-unbounded-mixed-sigterm`, `r29-a2-10-zero-unbounded-mixed-sigkill`, `r29-a2-10-stamped-send-survives`; a2: `a2-01-suppressed-in-scope-with-action`, `a2-03-group-kill-one-with-sigterm-action`, `a2-03-group-kill-three-after-earlier-invocation`, `a2-06-active-earlier-and-current-send-acted`, `a2-07-earlier-dryrun-then-current-real`, `a2-07-three-invocations-dryrun-in-the-middle`; core and supp: `c03-scope-boundary-exactly-at`, `c11-byte-array-message-action`, `c12-byte-array-invalid-utf8`, `c13-sigterm-action`, `c14-sigkill-action` | No |
| M06 | Delete the segment reset of signal counts and dryrun state. | F17/24; P30/30; P32/32; P32/32 | r29: `r29-a2-07-dryrun-inside-scope` | No |
| M07 | Count SIGTERM directly in global counts rather than the segment. | F14/24; F27/30; P32/32; P32/32 | r29: `r29-a2-07-real-before-scope-current-dryrun`, `r29-a2-07-real-escalation-before-boundary-current-dryrun`, `r29-a2-07-real-before-dryrun-signals`, `r29-a2-07-all-dryrun-multiple-sends`; a2: `a2-04-dryrun-sigterm-send-not-positive`, `a2-04-dryrun-two-sigterm-sends-counted`, `a2-07-earlier-real-then-current-dryrun` | No |
| M08 | Count SIGKILL directly in global counts rather than the segment. | F15/24; F29/30; P32/32; P32/32 | r29: `r29-a2-07-real-escalation-before-boundary-current-dryrun`, `r29-a2-07-real-before-dryrun-signals`, `r29-a2-07-all-dryrun-multiple-sends`; a2: `a2-04-dryrun-send-with-oomd-notices` | No |
| M09 | Omit the per-segment `dryrun=True` mark while retaining the global marker. | F14/24; F26/30; P32/32; P32/32 | r29: `r29-a2-07-real-before-scope-current-dryrun`, `r29-a2-07-real-escalation-before-boundary-current-dryrun`, `r29-a2-07-real-before-dryrun-signals`, `r29-a2-07-all-dryrun-multiple-sends`; a2: `a2-04-dryrun-sigterm-send-not-positive`, `a2-04-dryrun-two-sigterm-sends-counted`, `a2-04-dryrun-send-with-oomd-notices`, `a2-07-earlier-real-then-current-dryrun` | No |
| M10 | Omit SIGKILL from `dryrun_send_lines` aggregation. | F15/24; F29/30; P32/32; P32/32 | r29: `r29-a2-07-real-escalation-before-boundary-current-dryrun`, `r29-a2-07-real-before-dryrun-signals`, `r29-a2-07-all-dryrun-multiple-sends`; a2: `a2-04-dryrun-send-with-oomd-notices` | No |

`P`/`F` above abbreviate the actual selftest `PASS n/n` / `FAIL n/n` first line; the listed IDs are those with additional failure output beyond the pristine baseline. Both core and supplementary runs failed the same six IDs when killed by M02 or M05; both passed for the other mutants.

## Hashes and verdict

Pristine draft SHA-256 (direct `sha256sum` before probes): `2609103210967b04cb7fab6e67886291a4ae8b336df64ec8823c01732b84e187`. The following are SHA-256 hashes of each one-point variant formed from those pristine bytes using the table's exact replacement; M10's hash was also directly observed on the applied file before restore (`e8783c4ada445d739f66b50f565791b4855eec5a84297147af2397897e00724a`).

- M01 `9dd4d9327cb5096e83bbf96ad092b65554f239ebfa907957b0b981829408f2f3`
- M02 `6a71fb40bb51f10afd8d80a616797626e925a7b9c193813571661717cdefea71`
- M03 `b5ae95cfcabcfcb5bd30a2244416c69a646f87b85bd92ce4b2e6343b2dff3e71`
- M04 `a999e00ae004cf920f249f2f5a6d39e3f1b4feade7631a1f80f867bc44f5968f`
- M05 `a29dd3e965bed2b3b440a3c60082a168857f408cc71a991bd398fbbec668711f`
- M06 `3e3b9648d951ba42691da5bf890a5657dbbb458565695d8d28e561a466d021ab`
- M07 `232febb6ae05f1bf3b7bc2082246f6763486d2667efeb195e73743f29346531e`
- M08 `6565220f11b27ce96f4f34a7d1c85e6023914a1a19823261ec5d2302bc1e3442`
- M09 `52312e8066ca9c22fb5161a057d065887c657aeae0c1492dd9ecff44ad462d8a`
- M10 `e8783c4ada445d739f66b50f565791b4855eec5a84297147af2397897e00724a`

After restoring the saved original, direct `sha256sum` of `tools/mori-oom-killers.py` and the pristine backup both returned `2609103210967b04cb7fab6e67886291a4ae8b336df64ec8823c01732b84e187`; the restored four-file run reproduced the pristine outputs above. Verdict: 10/10 mutants killed by a previously passing detector case; no survivors / coverage gaps identified by this probe. The six baseline failures remain inconclusive findings, not mutant kills.