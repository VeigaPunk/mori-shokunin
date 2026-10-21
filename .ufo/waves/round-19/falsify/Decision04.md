# Decision04 — SrcSlsaProvenance content-review falsification

**Disposition: reject.**

- **Hash binding:** The current retained file's SHA-256 matches the review record.
- **Reason truth:** Not true as stated. Public specification material is present, but the artifact also contains project-specific implementation observations; describing the analysis as generic and asserting that no private source values remain omits those observations.
- **Minimization:** No performed minimization is evidenced. The artifact retains the implementation-specific details; its listed recheck steps are proposed source checks, not redaction or minimization.
- **Ownership:** Public specification excerpts are attributed separately from the C3-specific observations; one implementation detail is explicitly identified as project-private. The ownership distinction is present, but does not support the retain rationale.

Findings (path:line/class):
- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-18/build/SrcSlsaProvenance.md:38-43/project-private-implementation-observations
- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-18/build/SrcSlsaProvenance.md:42/private-observed-serialization-detail
- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-18/build/SrcSlsaProvenance.md:62-66/proposed-source-checks-not-minimization
- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-19/content-reviews-before.json:112-116/retain-review-record
- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-19/build/Content03.md:35-40/duplicate-retain-rationale
