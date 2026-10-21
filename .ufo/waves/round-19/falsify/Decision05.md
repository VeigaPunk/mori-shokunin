# Decision05

Verdict: **keep** the `unresolved` decision.

- `.ufo/waves/round-18/falsify/AuditMisrootsScratch.md:7,20,23` — `host-account-path`; `.ufo/waves/round-18/falsify/AuditMisrootsScratch.md:7-25` — `repository-path/count/status-metadata`, no configuration-content class observed. The stated reason is supported at content level.
- `.ufo/waves/round-19/build/Content03.md:43-51` and `.ufo/waves/round-19/content-reviews-before.json:147-151` — `blob-binding/matched`; recorded full-blob digest matches the retained bytes and frozen-commit blob.
- `.ufo/waves/round-18/falsify/AuditMisrootsScratch.md:7,20,23` — `minimization/not-performed`; the host-account paths remain in the retained content. The source row records `unresolved`, not a completed minimization.
- `.ufo/waves/round-18/falsify/AuditMisrootsScratch.md:7,20,23`; `.ufo/waves/round-19/build/Content03.md:47-51` — `ownership/origin-not-explicit`; the artifact presents these as command paths, while the review classifies them as host-account paths but does not explicitly distinguish public-instruction ownership from private observed-value ownership. This gap does not justify clearing the conservative unresolved decision.

No checks or tests run.