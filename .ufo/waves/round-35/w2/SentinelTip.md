measured 2026-10-23T09:14:58Z

# Scope and result
Scanned additions in `git diff dd76eb79 cedb0ec4f3a4f672804deac388b7191258f01fcd` and the committed `c0/` and `w1/` reports at the target revision. The diff reports 73 files changed, 11,934 insertions, and 2 deletions (`git diff --stat dd76eb79 cedb0ec4f3a4f672804deac388b7191258f01fcd`). The read-only scan covered 11,934 added lines and found five email-shaped candidates, listed below; it found no candidates for UID, PID/process-group ID, session ID, numeric per-user slice, OMP setting value, credential token, private URL, or journal MESSAGE content.

# Email-shaped candidates
- `.ufo/waves/round-35/c0/CtlShotgun-register.md:19` — A generic address-shaped token is carried in negative evidence-path fixture material, not in a contact or identity field. This is duplicated in the next record.
VERDICT: no defect found

- `.ufo/waves/round-35/c0/CtlShotgun-register.md:20` — Same generic fixture token in a second register record.
VERDICT: no defect found

- `.ufo/waves/round-35/c0/CtlShotgun.md:244` — The checker report identifies the address-shaped token as part of a malformed-path test input; the surrounding record is a negative test result.
VERDICT: no defect found

- `.ufo/waves/round-35/c0/CtlShotgun.md:245` — Duplicate malformed-path test result for the same fixture input.
VERDICT: no defect found

- `corpus/evidence/sources-r35/S204.src:3847` — An author contact appears in an upstream source attribution macro. This is source attribution, not host or user data.
VERDICT: no defect found

Severity: none found. Exploit path: none evidenced. Smallest remediation: none for these candidates; retain the generic negative-test fixture and upstream attribution.