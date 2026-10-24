measured 2026-10-23T08:56:16Z
# Round 35 W1 — privacy scan

Scope: the 18 admitted capability strings in frozen fleet MANIFEST `37b51a243302e8009c7067431e8a47f9a722fd14`, plus the closure text sources the counter assembles: each `verification` object, its referenced spot-check files, and each `report` file (`.ufo/waves/round-35/count-c1.py:103-125`). Capability strings are at `MANIFEST.json:6211,7494,7744,8084,9473-9475,10144,12007,12910-12911,13431-13432,13722,14312-14313,15102-15103`; there are 18 (`git show 37b51a243302e8009c7067431e8a47f9a722fd14:MANIFEST.json | jq …` → `18`).

## Findings

VERDICT: defect — severity Low; closure spot-checks expose historical process-group identifiers.

Location: `corpus/lessons/round-14-verifier-spotcheck.md:24`; `round-15-verifier-spotcheck.md:66`; `round-16-verifier-spotcheck.md:71`; `round-24-verifier-spotcheck.md:33,35`; `round-25-verifier-spotcheck.md:25`; `round-26-verifier-spotcheck.md:25`; `round-28-verifier-spotcheck.md:8`; `round-31-verifier-spotcheck.md:14`.

Safe paraphrase: driver launch records contain concrete PGID values; no values are reproduced here. These are process-group identifiers, not fields labelled PID.

Exploit path: if the register copies closure text as assigned, it propagates these runtime identifiers from the referenced records into the longer-lived SCORECARD. Impact: unnecessary host/runtime correlation data becomes easier to discover; the records are historical, so no live-process access is asserted. Smallest remediation: omit or redact PGID values in copied closure text.

VERDICT: defect — severity Medium; closure spot-checks expose committer email addresses.

Location: `corpus/lessons/round-15-verifier-spotcheck.md:46`; `round-16-verifier-spotcheck.md:38`; `round-18-verifier-spotcheck.md:21`; `round-28-verifier-spotcheck.md:34`; `round-31-verifier-spotcheck.md:21`.

Safe paraphrase: these lines include a commit author's mailbox alongside authorship evidence; no address is reproduced here.

Exploit path: copying the closure text into SCORECARD makes the mailbox more prominent and readily harvestable. Impact: personal contact information exposure and possible targeted contact. Smallest remediation: replace mailbox text with a generic author-identity note in copied closure text.

VERDICT: defect — severity Low; reviewer metadata contains a route-like alias.

Location: `MANIFEST.json:7498,7748,8088,9479,12915,13436,13726,14317,15107` (`verification.reviewer`); the referenced spot-check author metadata repeats it at `round-14-verifier-spotcheck.md:3`, `round-15-verifier-spotcheck.md:1`, `round-16-verifier-spotcheck.md:1`, `round-18-verifier-spotcheck.md:1`, `round-24-verifier-spotcheck.md:3`, `round-25-verifier-spotcheck.md:3`, `round-26-verifier-spotcheck.md:3`, `round-28-verifier-spotcheck.md:1`, and `round-31-verifier-spotcheck.md:1`.

Safe paraphrase: reviewer/author metadata contains a short `@m_…` identity label; its classification as a model-route alias is [INFERENCE], because the record does not define the label. The alias is not reproduced here.

Exploit path: copying the closure text exposes the reviewer-routing label in SCORECARD. Impact: discloses internal reviewer identity/routing metadata. Smallest remediation: redact the alias while retaining a generic reviewer attribution.

## No other listed hazards found

VERDICT: no defect found — the 18 capability strings themselves contain no UID values, per-user slice identifiers, session IDs, concrete OMP setting values, credential/token values, email addresses, private/local URLs, journal MESSAGE payloads, or route aliases (locations listed above). The closure reports named at `MANIFEST.json:6213,7496,7746,8086,9477,10146,12009,12913,13434,13724,14315,15105` and the referenced spot-check sources were also scanned. The `MESSAGE` occurrence at `round-15-verifier-spotcheck.md:192` is a control-description label, not journal payload.
