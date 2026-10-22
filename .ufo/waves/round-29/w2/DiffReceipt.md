# Round 29 wave 2 — full-output differential receipt

Measured sandbox: lane commit `8809a3fe1eaa87a0afa177a15263d174378e7462` (`git checkout --detach` reported `HEAD is now at 8809a3f`). The runner used the four requested case files and all 16 JSON files under round-26 `a2-detectors`: 32 + 32 + 30 + 24 + 16 = 134 inputs. Each fixture case's `.inputs` object and each standalone input were copied into the assigned scratch sandbox, then each tool was invoked with `--inputs` for every input; no live mode was used.

Runner: `/fast/scratch/hyaku/mori-r29/w2/DiffReceipt/differential-receipt.py` (included in scratch). Invocation: `python3 /fast/scratch/hyaku/mori-r29/w2/DiffReceipt/differential-receipt.py`. It recursively compared the complete JSON values and compared return codes; complete stdout and stderr are retained at `/fast/scratch/hyaku/mori-r29/w2/DiffReceipt/run/outputs/{base,fix}/`, and the emitted receipt at `/fast/scratch/hyaku/mori-r29/w2/DiffReceipt/run/receipt.txt`. Tool SHA-256: base `343acaf4b94a1d18f2133b7967ef4078f0605de111a22e803ae36ace77f73d3b`; fix `2609103210967b04cb7fab6e67886291a4ae8b336df64ec8823c01732b84e187`.

Receipt: changed-paths are full JSON paths; `exit-code` marks a return-code delta. `same —` means both complete JSON output and return code matched.

```text
cases.json:c01-host-quiet-thresholds same —
cases.json:c02-scope-boundary-one-microsecond-before same —
cases.json:c03-scope-boundary-exactly-at same —
cases.json:c04-incomplete-scope-with-action same —
cases.json:c05-incomplete-scope-without-action same —
cases.json:c06-earlyoom-inactive same —
cases.json:c07-earlyoom-absent same —
cases.json:c08-null-journal same —
cases.json:c09-unverified-version same —
cases.json:c10-oomd-notices-positive same —
cases.json:c11-byte-array-message-action same —
cases.json:c12-byte-array-invalid-utf8 same —
cases.json:c13-sigterm-action same —
cases.json:c14-sigkill-action same —
cases.json:c15-escalation same —
cases.json:c16-kill-failed-only same —
cases.json:c17-low-memory-warnings same —
cases.json:c18-dryrun-flag same —
cases.json:c19-version-line-only same —
cases.json:c20-nearmiss-threshold-line-is-not-an-action same —
cases.json:c21-nearmiss-midline-sigkill same —
cases.json:c22-nearmiss-low-memory-singular-limit same —
cases.json:c23-nearmiss-dryrun-plural same —
cases.json:c24-nearmiss-kill-failed-without-colon same —
cases.json:c25-null-earlyoom-show same —
cases.json:c26-null-oomd-show-and-notices same —
cases.json:c27-show-without-activestate same —
cases.json:c28-oomd-active-quiet same —
cases.json:c29-oomd-notices-with-inactive-earlyoom same —
cases.json:c30-null-journal-with-oomd-notices same —
cases.json:c31-error-journal-not-a-list same —
cases.json:c32-error-show-not-a-string same —
cases-supplementary.json:c01-host-quiet-thresholds same —
cases-supplementary.json:c02-scope-boundary-one-microsecond-before same —
cases-supplementary.json:c03-scope-boundary-exactly-at same —
cases-supplementary.json:c04-incomplete-scope-with-action same —
cases-supplementary.json:c05-incomplete-scope-without-action same —
cases-supplementary.json:c06-earlyoom-inactive same —
cases-supplementary.json:c07-earlyoom-absent same —
cases-supplementary.json:c08-null-journal same —
cases-supplementary.json:c09-unverified-version same —
cases-supplementary.json:c10-oomd-notices-positive same —
cases-supplementary.json:c11-byte-array-message-action same —
cases-supplementary.json:c12-byte-array-invalid-utf8 same —
cases-supplementary.json:c13-sigterm-action same —
cases-supplementary.json:c14-sigkill-action same —
cases-supplementary.json:c15-escalation same —
cases-supplementary.json:c16-kill-failed-only same —
cases-supplementary.json:c17-low-memory-warnings same —
cases-supplementary.json:c18-dryrun-flag same —
cases-supplementary.json:c20-nearmiss-threshold-line-is-not-an-action same —
cases-supplementary.json:c21-nearmiss-midline-sigkill same —
cases-supplementary.json:c22-nearmiss-low-memory-singular-limit same —
cases-supplementary.json:c23-nearmiss-dryrun-plural same —
cases-supplementary.json:c25-null-earlyoom-show same —
cases-supplementary.json:c26-null-oomd-show-and-notices same —
cases-supplementary.json:c27-show-without-activestate same —
cases-supplementary.json:c29-oomd-notices-with-inactive-earlyoom same —
cases-supplementary.json:c30-null-journal-with-oomd-notices same —
cases-supplementary.json:c31-error-journal-not-a-list same —
cases-supplementary.json:c32-error-show-not-a-string same —
cases-supplementary.json:c33-differing-thresholds-mem-and-swap same —
cases-supplementary.json:c34-escalation-only-incomplete-scope same —
cases-supplementary.json:c35-malformed-monotonic-timestamp changed $.earlyoom.earlier_invocation_send_lines
cases-a2.json:a2-01-suppressed-in-scope-active-quiet same —
cases-a2.json:a2-01-suppressed-before-scope-start same —
cases-a2.json:a2-01-suppressed-in-scope-with-action same —
cases-a2.json:a2-02-earlyoom-activestate-failed same —
cases-a2.json:a2-02-earlyoom-activestate-deactivating same —
cases-a2.json:a2-02-earlyoom-activestate-activating-empty-journal same —
cases-a2.json:a2-03-group-kill-one-with-sigterm-action same —
cases-a2.json:a2-03-group-kill-two-no-action-oomd-notices same —
cases-a2.json:a2-03-group-kill-three-after-earlier-invocation same —
cases-a2.json:a2-04-dryrun-sigterm-send-not-positive same —
cases-a2.json:a2-04-dryrun-two-sigterm-sends-counted same —
cases-a2.json:a2-04-dryrun-send-with-oomd-notices same —
cases-a2.json:a2-05-monotonic-zero-active-quiet same —
cases-a2.json:a2-05-monotonic-missing-active-oomd-notices same —
cases-a2.json:a2-05-monotonic-zero-inactive-quiet same —
cases-a2.json:a2-06-active-earlier-invocation-sends-quiet same —
cases-a2.json:a2-06-inactive-earlier-invocation-sends-acted same —
cases-a2.json:a2-06-active-earlier-and-current-send-acted same —
cases-a2.json:a2-07-earlier-real-then-current-dryrun same —
cases-a2.json:a2-07-earlier-dryrun-then-current-real same —
cases-a2.json:a2-07-three-invocations-dryrun-in-the-middle same —
cases-a2.json:a2-08-null-journal-inactive-earlyoom same —
cases-a2.json:a2-08-null-journal-absent-earlyoom same —
cases-a2.json:a2-08-null-journal-active-earlyoom-readable-oomd same —
cases-a2.json:a2-09-removed-unit-single-sigterm-send same —
cases-a2.json:a2-09-removed-unit-two-invocations-mixed-sends same —
cases-a2.json:a2-09-removed-unit-three-sends-oomd-active same —
cases-a2.json:a2-10-malformed-action-line-uncounted changed $.earlyoom.earlier_invocation_send_lines
cases-a2.json:a2-10-positive-evidence-elsewhere-stands changed $.earlyoom.earlier_invocation_send_lines
cases-a2.json:a2-10-oomd-notices-positive-malformed-records changed $.earlyoom.earlier_invocation_send_lines
cases-a2-r29.json:r29-a2-07-dryrun-before-boundary same —
cases-a2-r29.json:r29-a2-07-two-prior-invocations same —
cases-a2-r29.json:r29-a2-07-dryrun-inside-scope changed $.earlyoom.actions.sigkill,$.earlyoom.dryrun_send_lines,$.verdict,exit-code
cases-a2-r29.json:r29-a2-07-real-before-scope-current-dryrun same —
cases-a2-r29.json:r29-a2-07-real-escalation-before-boundary-current-dryrun same —
cases-a2-r29.json:r29-a2-07-earlier-real-dryrun-then-current-real same —
cases-a2-r29.json:r29-a2-07-dryrun-then-real-missing-enter changed $.earlyoom.actions.sigterm,$.earlyoom.dryrun_send_lines,$.verdict,exit-code
cases-a2-r29.json:r29-a2-07-real-then-dryrun-zero-enter changed $.earlyoom.actions.sigterm,$.earlyoom.dryrun_send_lines,$.verdict,exit-code
cases-a2-r29.json:r29-a2-07-real-dryrun-real-missing-enter changed $.earlyoom.actions.sigkill,$.earlyoom.actions.sigterm,$.earlyoom.dryrun_send_lines,$.verdict,exit-code
cases-a2-r29.json:r29-a2-07-dryrun-before-real-signals same —
cases-a2-r29.json:r29-a2-07-real-before-dryrun-signals same —
cases-a2-r29.json:r29-a2-07-all-dryrun-multiple-sends same —
cases-a2-r29.json:r29-a2-10-unbounded-missing-stamp-alone changed $.earlyoom.actions.sigterm,$.verdict,exit-code
cases-a2-r29.json:r29-a2-10-zero-unbounded-mixed-sigterm changed $.earlyoom.actions.sigkill
cases-a2-r29.json:r29-a2-10-zero-unbounded-mixed-sigkill changed $.earlyoom.actions.sigterm
cases-a2-r29.json:r29-a2-10-unclocked-send-alone changed $.earlyoom.earlier_invocation_send_lines
cases-a2-r29.json:r29-a2-10-stamped-send-survives changed $.earlyoom.earlier_invocation_send_lines
cases-a2-r29.json:r29-a2-10-oomd-evidence-survives changed $.earlyoom.earlier_invocation_send_lines
cases-a2-r29.json:r29-a2-10-inactive-lone-missing-stamp changed $.earlyoom.earlier_invocation_send_lines,$.verdict,exit-code
cases-a2-r29.json:r29-a2-10-failed-stamped-positive changed $.earlyoom.earlier_invocation_send_lines
cases-a2-r29.json:r29-a2-10-not-found-earlier-stamped-positive changed $.earlyoom.earlier_invocation_send_lines
cases-a2-r29.json:r29-a2-10-empty-and-letters same —
cases-a2-r29.json:r29-a2-10-negative-and-decimal same —
cases-a2-r29.json:r29-a2-10-whitespace-and-missing same —
.ufo/waves/round-26/evidence/a2-detectors/in-Y1-stopped-real-then-dryrun.json:in-Y1-stopped-real-then-dryrun same —
.ufo/waves/round-26/evidence/a2-detectors/in-Y2-active-earlier-real-and-dryrun.json:in-Y2-active-earlier-real-and-dryrun same —
.ufo/waves/round-26/evidence/a2-detectors/in-Y3-stopped-null-journal.json:in-Y3-stopped-null-journal same —
.ufo/waves/round-26/evidence/a2-detectors/in-Y4-stopped-suppressed.json:in-Y4-stopped-suppressed same —
.ufo/waves/round-26/evidence/a2-detectors/in-Y5-active-dryrun-group.json:in-Y5-active-dryrun-group same —
.ufo/waves/round-26/evidence/a2-detectors/in-Y6-never-started.json:in-Y6-never-started same —
.ufo/waves/round-26/evidence/a2-detectors/in-Y7-stopped-unverified-version-send.json:in-Y7-stopped-unverified-version-send same —
.ufo/waves/round-26/evidence/a2-detectors/in-Y8-absent-with-sends.json:in-Y8-absent-with-sends same —
.ufo/waves/round-26/evidence/a2-detectors/in-Y9-active-earlier-real.json:in-Y9-active-earlier-real same —
.ufo/waves/round-26/evidence/a2-detectors/m1-suppressed.json:m1-suppressed same —
.ufo/waves/round-26/evidence/a2-detectors/m2-nonsteady.json:m2-nonsteady same —
.ufo/waves/round-26/evidence/a2-detectors/m3-dryrun-send.json:m3-dryrun-send same —
.ufo/waves/round-26/evidence/a2-detectors/m4-process-group.json:m4-process-group same —
.ufo/waves/round-26/evidence/a2-detectors/m5-earlier-invocation.json:m5-earlier-invocation same —
.ufo/waves/round-26/evidence/a2-detectors/m6-malformed-timestamp.json:m6-malformed-timestamp changed $.earlyoom.earlier_invocation_send_lines
.ufo/waves/round-26/evidence/a2-detectors/m7-aetm-zero.json:m7-aetm-zero same —
totals: inputs=134 same=116 changed=18
```

**Changes outside `cases-a2-r29.json`:** five inputs changed, and every changed output path is `$.earlyoom.earlier_invocation_send_lines`: supplementary `c35-malformed-monotonic-timestamp` 1→0; A2 `a2-10-malformed-action-line-uncounted` 1→0, `a2-10-positive-evidence-elsewhere-stands` 1→0, and `a2-10-oomd-notices-positive-malformed-records` 2→0; round-26 `m6-malformed-timestamp` 1→0. No outside-case verdict or exit-code path changed. This follows the draft diff: unclocked records are excluded from the `earlier` candidates at `fix.diff:27-33`, and missing/zero-boundary scope similarly skips unplaceable records at `fix.diff:11-19`. These are non-R29 behavior changes to historical reported counts, retained here as a risk for L1 judgment.

Tool installs/updates: none. Blockers: none.
