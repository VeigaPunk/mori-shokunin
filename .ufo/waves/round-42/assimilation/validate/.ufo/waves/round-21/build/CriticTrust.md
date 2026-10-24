# CriticTrust — round 21

## Acceptance blocker: `independent:true` is not proof of independence

**Answer: yes.** The proposed audit permits `state: disposed` when a referenced evidence copy has valid path/revision/hash provenance, `independent: true`, an actor distinct from cleanup, and a wave-specific disposition (`.ufo/waves/round-21/contract.md:14`). Those checks bind and validate the submitted bytes and fields; the contract does not specify an authenticated source for the actor identity or an independent review that vouches for the disposition. A cleanup author can submit a self-authored record asserting `independent: true` and a different actor, hash and commit that record, and satisfy the stated data checks without any independent disposition. **[INFERENCE]** From the contract, such a claim could then set `disposed` and permit the pin.

### Evidence

- Round 20's register records that the per-path Souji cleanup receipts were committed by the same Souji identity as the deletion, two minutes later (`.ufo/waves/round-20/build-register.py:53`). This accounts for cleanup, not independent settlement.
- The prior critic records that the non-author r12 receipt explicitly says missing registry/dispatch/run markers do **not** prove settlement, and recommends an independent explicit closeout/settlement record; unexplained disappearance remains a blocker (`.ufo/waves/round-20/build/C1Critic.md:11,22`).
- Git author metadata is not a sufficient independence check: the r20 audit notes that the harness and tool were first committed together under the same author name, so separate authorship could not be shown from Git (`.ufo/waves/round-20/falsify/CountC2.md:71`).

### Impacted axes

- **C1 freshness:** a cleanup-author assertion could convert the two unresolved historical observations into disposed rows and allow baseline acceptance while independent disposition is still unknown.
- **C2 calibration:** the evidence-loss-first rule can classify lost required evidence as safe using an unverified `independent_disposition` claim, recreating the cause-only false permission it is meant to supersede.

### Smallest safe correction

Treat `independent:true` and the distinct-actor value as claims, not permission. Require a separate, per-wave non-author review record bound to the exact disposition evidence hash/revision; it must explicitly accept `settlement` or `cleanup-accounted` and identify the reviewer. The CLI may validate paths, hashes, structure, and binding, but MUST NOT claim to authenticate authorship or independence. A human acceptance step must establish that the reviewer is not the cleanup author; until that review is present and accepted, keep the row unresolved and `pin_allowed: false`. If the external identity/review condition cannot be established, fail closed and leave the pin blocked.
