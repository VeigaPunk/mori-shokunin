# Final R17 falsification

## Result

**Axes:** malformed-input behavior; oracle branch attribution; retained-red accounting. Static review only—no commands, fixtures, or tests were executed. **R17 holds for the delivered fixture and source path examined; no current-source counterexample found.** The frozen oracle does not, however, isolate the malformed-JSON branch: it lacks a same-command valid-red control.

## Branch trace

- The effective requirement is `R17 malformed JSON returns2` (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-22/contract.md:19`). The v2 requirements file enumerates R17 but does not carry separate per-ID prose (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-22/frozen/requirements-v2.json:3-34`). The denominator correction does not change this malformed-input requirement.
- `make(..., variant='malformed')` builds the measured tree, policy, allowlist, and wrapper, replaces the receipt blob with malformed JSON, then commits the final fixture tree (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-22/frozen/fixture-builder-v2.py:35-43,63-64,76-99`). Other builder variants establish the normal retained-red receipt shape; R17 itself does not invoke a paired valid receipt from this same final revision.
- In the shipped checker, `check()` resolves the input revision and retrieves the committed receipt/policy/allowlist before parsing the wrapper (`/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-retention-reconcile.py:154-159`; committed-blob checks at `:81-86`). `parse()` maps JSON decoding errors to `Invalid` (`:43-47`); `main()` catches `Invalid`, emits the setup finding, and returns exit 2 (`:263-276`). Thus the builder's malformed receipt reaches the intended parse-failure path, whose result matches R17.
- The oracle maps R17 to `malformed` with expected exit 2 and setup finding (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-22/oracle-reconcile-v2.py:54`). `record()` checks exit, JSON-object output, finding, and empty stderr (`:40-46`). This is a useful assertion of the expected external result, but not of which checker branch produced it.

## Smallest counterexample to R17 isolation

A one-field fixture defect suffices: for the `malformed` variant only, point the policy input at a missing committed path. `committed()` then raises a setup error before `check()` reaches `parse(raw['receipt'])`; the existing R17 assertion still accepts exit 2 and the setup finding. This is a counterexample to **branch attribution**, not an observed defect in the delivered builder: its current malformed fixture supplies the policy and allowlist.

R01 is not the missing control: it invokes a separate `valid` fixture, hence a different repository/revision and command inputs. Add a valid, internally consistent retained-red receipt blob to the malformed fixture's final commit and run the same checker command against that same repo/revision/policy/allowlist, changing only the receipt path. Require exit 0, `RETENTION_RECONCILED`, `receipt_match=true`, red retention state, and `privacy_clearance=false`. That paired control would show that R17's setup result is attributable to the malformed receipt rather than another setup failure. The current R17 arm also covers only its one malformed byte sequence, not arbitrary malformed JSON encodings.

## Limits and confidence

No LSP device was mounted (`xd://lsp` returned unavailable), so I used literal source search and targeted reads; these are not LSP semantic results. Confidence is high for the static branch trace and the stated oracle gap; runtime behavior remains unverified by design.