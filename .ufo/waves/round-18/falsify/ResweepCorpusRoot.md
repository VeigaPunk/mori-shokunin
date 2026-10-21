# Round-18 corpus-root privacy re-sweep

## Scope and method

Scanned the requested tracked paths at `e2bfbd6f8dccc51fc06455efc41f720301112dd4`: `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`, `LOG.md`, `README.md`, `AGENTS.md`, `MINT.md`, `corpus/**`, and `tools/**`. Used read-only `git -C /home/vgpnk/Projects/shokunin/mori-shokunin grep` against that revision, suppressing matched text to path:line during scans, then read only candidate line ranges for classification. Also read the round-18 contract, L1 draft/triage, and frozen C1/C2/C3 inputs as directed. No source edits, VCS mutations, tests, builds, network access, or tool installations.

Per-file SHA-256 values below are over the complete tracked blob at the scanned revision, not line digests. They are provenance fingerprints, not redactions.

## Confirmed private-context findings

### P-OMP: routing/model assignments and configuration fingerprint

The generic `@m_` alias scan found 12 lines. In context, these are operator OMP routing/model assignment values, not synthetic fixture identities:

- `LOG.md:126-127,129-130` — observed role/model assignment and fallback details; `LOG.md:128` also retains a global configuration fingerprint. These lines are private configuration data even though C1-R8 (which searches known table-key names) has no hit.
- `SCORECARD.md:79-81` — duplicated role bindings and model assignments.
- `corpus/lessons/round-13-verifier-spotcheck.md:3`
- `corpus/lessons/round-14-verifier-spotcheck.md:3`
- `corpus/lessons/round-15-verifier-spotcheck.md:1`
- `corpus/lessons/round-16-verifier-spotcheck.md:1`
- `corpus/lessons/round-17-verifier-spotcheck.md:1`

The latter five are model-alias attribution tags in non-author verifier headers. Their classification as private configuration aliases is supported by the alias use in `LOG.md`/`SCORECARD.md`; the source values are not repeated here.

### P-IDENTITY: personal-name references

Four remaining identity-bearing lines were found:

- `corpus/knowledge/lane-silence-r2.md:100` — personal name in a historical author/committer example.
- `corpus/knowledge/silence-grading-r2.md:146,153` — a first-name fragment remains at `:146` despite the withheld-identity placeholder; `:153` retains the full personal name.
- `corpus/lessons/round-16-verifier-spotcheck.md:47` — the same personal name in an author attribution.

This falsifies the redaction decision recorded at `.ufo/waves/round-18/out-of-metric-triage.md:29` for `silence-grading-r2.md:146`: a placeholder is present, but a personal-name fragment remains, and the full name remains at `:153`. The duplicate name references also occur outside that triage row. No personal name is quoted here.

### P-IDENTITY? identity-bearing public account link (inference)

- `README.md:4,8` and `LOG.md:718` contain a public wiki/account handle that appears identity-linked to the personal-name references above. This may be an intentionally public organization handle rather than private context, so it is **[INFERENCE]**, medium confidence, and is not counted as a confirmed private-name disclosure. The URL and handle are withheld.

### P-HOME? absolute home-path identifier (inference)

- `tools/mori-round17-context-check.py:565` embeds an absolute operator-home path to an agent rules file. No rules-file contents or configuration values are present in that line. Treating the path itself as sensitive is **[INFERENCE]**, low-to-medium confidence; it is a path-only candidate, not a configuration-value finding.

## Synthetic and non-finding classifications

- The email-shaped scan returned 97 matching lines. Review classified them as lane/test identities, or `@`-bearing systemd unit/service identifiers—not operator email disclosures. The 11 occurrences using the explicitly synthetic `.invalid` fixture domain are at `tools/mori-census.sh:4090-4091,4270`; `tools/mori-dispatch-ledger.py:390,437,439`; `tools/mori-freeze-order.py:325,327`; and `tools/mori-retention-gate.py:411,482-484`. Tool context confirms these are selftest/fixture values. Other fixture identities include `tools/mori-round17-jj-regressions.py:135` and `tools/mori-misroot-sweep.py:514-515`. Fleet-lane identity patterns in census/silence test helpers are synthetic lane identities, not personal identities. No operator email was observed.
- The exact frozen C1 scans had these results: R1, R2, R3, R4, R5, R7, and R8 each returned no match (raw `git grep` exit 1). R6 returned 3 name-only mentions at `corpus/lessons/round-17-verifier-spotcheck.md:315,341` and `corpus/lessons/round-17.md:241` (exit 0); they mention the privileged surface without retaining its setting/value. R9 returned one field-name-only mention at `corpus/lessons/round-17-verifier-spotcheck.md:312` (exit 0); no session-record field value is present there.
- The personal-name token scan also found the synthetic test author rows at `tools/mori-census.sh:4090-4091,4270`; their invalid-domain fixture context distinguishes them from the personal-name occurrences above.
- The explicit home-path scan found only the path-only candidate at `tools/mori-round17-context-check.py:565`; no `/home/.../Documents/` or shell-history path was found.

These observations are out-of-metric reading-sweep findings, consistent with the frozen policy's stated recall limitation (`.ufo/waves/round-18/frozen/c1-policy.json:29`). They do not change the C1 frozen-class count.

## Blob SHA-256 provenance

| Lane-relative blob | Affected lines / class | SHA-256 |
|---|---|---|
| `LOG.md` | P-OMP `126-130`; P-IDENTITY? `718` | `c46d3162c53a42559c6df5cdfd11123c859cd15494d3c2d952ca4dcf6514c891` |
| `SCORECARD.md` | P-OMP `79-81` | `3fddc6bf249c1d14d550eaa601178e60a2e33ab017926e5b2885809f5c7099b1` |
| `corpus/lessons/round-13-verifier-spotcheck.md` | P-OMP `3` | `e8b64126dafe00faf162218e540acdcab0f42deb14650c96a8f805e5947f8b16` |
| `corpus/lessons/round-14-verifier-spotcheck.md` | P-OMP `3` | `4f7015a9c7eb311aaac38ba3403fde5767fe58994f69c681dca18283cfbd428d` |
| `corpus/lessons/round-15-verifier-spotcheck.md` | P-OMP `1` | `b65a36e1e0ae1a3010f15df206ef8ec78bd7e6aa8fa0271ff679e5fd6494083d` |
| `corpus/lessons/round-16-verifier-spotcheck.md` | P-OMP `1`; P-IDENTITY `47` | `6a8e706e992e86d857df1f4726c6aaa6e57e8595b0ee4fb4dd80d164ed3305be` |
| `corpus/lessons/round-17-verifier-spotcheck.md` | P-OMP `1` | `98f8f1c631fcb565af69d884330177ebe01bfb31f21218028157d2acc40698dd` |
| `corpus/knowledge/lane-silence-r2.md` | P-IDENTITY `100` | `4a92969c358017b6674b90ca5e9262e4b23b1093ee225e8460b50e3a9c0f2b8d` |
| `corpus/knowledge/silence-grading-r2.md` | P-IDENTITY `146,153` | `35cdc293671ce2e5768bf43d3027fae9f8cee23f7a92183c449b1226e44937fd` |
| `README.md` | P-IDENTITY? `4,8` | `56d9f3f085f70b7ff3fd0dc83c55b72ec77eb9160bec10a2536fac1df2c2a69f` |
| `tools/mori-round17-context-check.py` | P-HOME? `565` | `ffdcd1154f5bc0d5af45cea6f14a4c125852f1f667ca0990350872261213681c` |

## Append-only correction proposal for `LOG.md`

Do not rewrite existing log history. Append a correction that identifies `LOG.md:126-130` as retaining operator OMP routing/model-assignment material and a configuration fingerprint, and `LOG.md:718` as an identity-bearing link candidate. State that values are withheld and that future summaries must use role-neutral descriptions; do not repeat any alias, fingerprint, name, or URL. Separately redact the non-append-only `SCORECARD.md`, README candidate, and corpus identity/model-attribution references, while preserving provenance with whole-blob hashes. This report proposes the correction only; it does not edit `LOG.md` or any scanned source.

## Commands and observed statuses

All grep scans used the fixed revision and target pathspecs above; output was restricted to path:line or counts. Raw `git grep` status (the adjacent `cut`/`wc` filter returned 0):

- Frozen classes R1–R5: each 1 (no matches); R6: 0 (3 matches); R7–R8: each 1 (no matches); R9: 0 (1 match).
- `@m_` alias scan: 0 (12 lines). Email-shaped scan: 0 (97 lines). `.invalid` fixture scan: 0 (11 lines). Absolute-home-path scan: 0 (1 line). Personal-name token scan: 0 (10 path:line references, including the synthetic fixture rows). Generic authored-name candidate scan: 0 (4 candidates, one non-name false positive reviewed).
- For each affected blob above, `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show e2bfbd6:<path> | sha256sum` completed with `show_rc=0`, `sha256sum_rc=0` and emitted the listed digest.
- No URLs were fetched. No tools were installed or updated.
