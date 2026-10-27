# Mo57MutationTester40 — C2 depth probe

## Verdict

**Claim supported, with a precision caveat:** the round-56 report provides the pairing list and explicitly rejects reading `unclosed` as a count of currently running work. Independent round-56 counterexamples in the committed record demonstrate why. No mutation was needed: the assigned behavior claim was directly attacked using the actual paired identities and the contrasting `in_flight` field; introducing a defect would obscure rather than test this interpretation.

## Evidence

- Frozen C2 asks for eight source-grounded interpretation/limits statements and an explicit statement that `unclosed` is a pairing count, not present-running count: `contract.md` (at entering tip) says this at lines 1-3.
- Reopened committed report `.ufo/waves/round-56/w1/Mo56ExecDriverLive.md`: lines 88-96 list all ten mori keys exactly: `[(2,None), (19,2), (20,1), (21,1), (22,1), (37,1), (38,1), (38,3), (40,1), (56,1)]`; it identifies only `(56,1)` as currently-live and the other nine as historic rounds 2–40, then says unclosed is a monotone backlog counter, not “10 things are running now.”
- Its receipt is `.ufo/waves/round-56/evidence/driver-liveness-live.txt`: mori has launches 66, completes 39, deads 17, `in_flight: true`, `unclosed: 10` (lines 195-205). Entry `corpus/knowledge/driver-liveness-r56.md:22-25,62-65` defines `unclosed` as launches with no same-round close, distinguishes it from health verdict, and says it is a pairing fact.
- Counterexample to interpreting counts as active work: the committed semantic review `.ufo/waves/round-56/w1/Mo56CritDriverSemantics.md:149-162` says 9 lanes had `in_flight=false` while `unclosed>0`; its replay classifies at least 123/124 emitted opens as historical ghosts. `:167-172` concludes the number is ~99% historical residue in that real-log replay, while acknowledging the tool's disclaimer.
- Report's own boundary is sound for the observed data, but “currently-live” is an inference from the contemporaneous log/context, not something `unclosed` proves. A live pairing requires external/time-context corroboration; report says so operationally by separating the one current round from the historical pairs.

## Counterexamples / limits

1. Receipt has `in_flight=true, unclosed=10`: one latest launch can coexist with nine unmatched historical pairs, so 10 is not a running-work count.
2. Semantic-review real-log counterexamples have `in_flight=false` with positive unclosed values (9 lanes; e.g. kagi 10, kaidoku 6; `Mo56CritDriverSemantics.md:149-152`). Thus positive unclosed does not even imply a latest launch remains in flight.
3. The entry definition is “no same-round close” (`driver-liveness-r56.md:22-23`), while pairing details elsewhere specify attempt keys; report's explicit list retains `None` for bare attempt and integers for attempts. Interpret identities exactly as report gives them, not as ten distinct active workers.

## Detection / mutation record

- Expected detector for an inverted interpretation: compare the report's “10 currently running” claim against the committed pairing list and semantic-review counterexamples; it should reject that claim. Actual report makes no such claim and explicitly denies it (`Mo56ExecDriverLive.md:90-96`), so this false interpretation is **killed** by the record. No behavior mutation was applied; no probe output was altered.
- Read-only command used to reopen the report at entering revision: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2:.ufo/waves/round-56/w1/Mo56ExecDriverLive.md` (exit 0; repository top-level was `/home/vgpnk/Projects/shokunin/mori-shokunin`).
- Report bytes before/after: unchanged; no scratch mutation was made. Scratch directory created at `/fast/scratch/hyaku/mori-r57/Mo57MutationTester40`; it contains no fixture or changed source.
