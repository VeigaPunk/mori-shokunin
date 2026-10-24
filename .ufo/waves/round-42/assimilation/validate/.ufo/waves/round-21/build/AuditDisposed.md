# AuditDisposed — independent-disposition trust boundary
Axes: **C1 pin safety** (a false disposition must not unblock the baseline) and **evidence trust/binding** (wave, actor, disposition, and digest must describe the same authenticated evidence bytes).


## Finding — High (specification blocker)

**The contract allows a self-asserted disposition to clear the pin gate; it does not require the actor or disposition bytes to be independently authenticated or bound to the row being disposed.**

Evidence:
- `.ufo/waves/round-21/contract.md:14` requires a `path/revision/sha256`, `independent:true`, a distinct actor, and an explicit wave id/disposition. It does not define a disposition-record schema, require `wave_id == observation.id`, say that actor/wave/disposition must be parsed from those exact hash-verified committed bytes, or authenticate the actor. `independent:true` and a different actor string are caller-provided assertions under the written interface.
- `corpus/evidence/loss-accounting-r21.json:17-23,38-44` currently has the cleanup actor in the accounting object and null dispositions for both required waves. `.ufo/waves/round-21/evidence/historical-provenance.json:38-40` explicitly says independent disposition is null and settlement is unknown; same-identity cleanup proves cleanup, not settlement.

**Concrete counterexample (specification-level, not an observed tool run):** a lane author changes `aggregator-r10-resume` to `state: "disposed"`, writes a committed own-lane disposition file claiming `wave_id: "aggregator-r10-resume"`, `actor: "reviewer@example"`, `disposition: "settlement"`, and calculates its exact SHA-256. The author sets `independent:true` and points the row at that file/revision/hash. The actor differs from the current cleanup actor (`souji-shokunin <souji@shokunin.local>`), the wave id is explicit, the disposition is an allowed value, and the bytes/hash agree—but the lane author can make the entire claim without any independent reviewer having acted. A conforming implementation of the listed checks can therefore count it disposed and set `pin_allowed=true`. A second binding gap is that “explicit wave id” does not say it must equal the current observation id, permitting a hash-valid disposition for `aggregator-r10` to be attached to `aggregator-r10-resume` if the implementation only checks that a wave id is present.

**Smallest safe contract change:** define one mandatory, hash-pinned disposition-record schema containing `wave_id`, `actor`, and the exact enum `disposition`; require `wave_id` to equal the accounting row's `id`; read and hash the bytes at the specified committed `revision:path`, then parse and compare those same bytes (not parallel accounting fields). Resolve the cleanup actor from its hash-bound evidence as well. Require the disposition actor to be authenticated against an independent trust source (for example, a signed reviewer attestation verified with a pre-established trusted key); a boolean, a distinct name/email string, or unsigned Git author metadata is not authentication. If the trust check cannot be performed, preserve `unresolved` and `pin_allowed=false`.

## Residual risk and verification gaps

- The existing accounting correctly remains unresolved; this review does not claim a current false settlement or pin acceptance.
- The specified new implementation was not present at either checked path: `tools/mori-evidence-loss.py` and `.scratch/round21/ImplLoss/tools/mori-evidence-loss.py`. Thus this is a contract gap, not a demonstrated implementation defect; no audit invocation or tests were run, as assigned.
- No `lsp` device/server was mounted (the `xd://lsp` lookup returned the mounted-device inventory without `lsp`), so semantic LSP checks were unavailable. No grep result is used as semantic proof. No production files were changed and no tools were installed.
