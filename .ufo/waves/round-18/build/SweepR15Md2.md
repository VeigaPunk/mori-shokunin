# Earlier-round finding: round-15 Markdown privacy sweep

## Scope and method

- Scanned the 32 tracked `.md` files in `git ls-files` order from `.ufo/waves/round-15/build/PackSignalUser.md` through `.ufo/waves/round-15/build/SkillInterface.md`, inclusive, at the frozen round-18 base `d005cdde0e009dea6c0cc29b37163de536528658`.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-files '.ufo/waves/round-15/*.md'` returned exit 0. For each source file listed below, `set -o pipefail; git -C /home/vgpnk/Projects/shokunin/mori-shokunin show d005cdde0e009dea6c0cc29b37163de536528658:<path> | sha256sum` returned a digest with exit 0; digests are committed-blob SHA-256s.
- Searched the frozen C1 R1–R9 expressions (policy `.ufo/waves/round-18/frozen/c1-policy.json:6-15`) plus the requested extra tokens and round-15 lane/seat identifiers. The frozen expressions were checked case-insensitively, a superset of their exact case-sensitive spellings. Every match was read with surrounding context. The REA `grep` device does not expose shell exit codes; its returned results are summarized below.
- No LSP device was available in the seat tool inventory, so this is a literal search/context review, not semantic proof. No tools were installed or updated.

## Findings

### Extra lane/seat identity hits

A case-sensitive scan for the round-15 lane/seat identifier form found **35 matching lines across 22 files**. These are lane/agent identifiers, not the timestamped OMP session-directory identities covered by frozen class R1. Some hits identify the report author; others identify peer seats or coordination targets. Redact concrete identifiers and use role-level labels or anonymous references. The table gives every matching path/line and the committed source-blob SHA-256; no identifier text is reproduced.

| Lane-relative path:line(s) | Class / matching lines | Blob SHA-256 |
|---|---:|---|
| `.ufo/waves/round-15/build/PackSignalUser.md:3,42` | `X-LANE-ID` / 2 | `a845f66146c362d2ff42b291b7e64292d9f3f3c179cfe09eaafc25e5ec1b2123` |
| `.ufo/waves/round-15/build/PackSubjectUnknown.md:3` | `X-LANE-ID` / 1 | `8886bf3b77e3cb7c71c964a5e3a94dc3b4e49b8f1f70dbd8403bcaee068ed49d` |
| `.ufo/waves/round-15/build/PackUnitSystem.md:4,7` | `X-LANE-ID` / 2 | `212b8b95a3a63277c8275ffdc19c4e66d28a4be398b61c0f7060ac8a916c1ba7` |
| `.ufo/waves/round-15/build/PackUnitUser.md:54` | `X-LANE-ID` / 1 | `25596e2fb35a0fd468e4e7bf0ff0cd9e63536e0fdc1eaef3aa093824ad80f51d` |
| `.ufo/waves/round-15/build/ProvenanceCapture.md:3` | `X-LANE-ID` / 1 | `f1d74649b3218cab734699f12beaa47aeb97d45b5f5b99e584fe791900455ee7` |
| `.ufo/waves/round-15/build/QualityDebt.md:3,9` | `X-LANE-ID` / 1; `X-AUTH-PATH` / 1 | `6095f0c3cb865a2e65e0e626787f734259c7a5d0e0f2289f5dd589ff5f88d9be` |
| `.ufo/waves/round-15/build/ReconBootScope.md:3,20` | `X-LANE-ID` / 2 | `bdaba8e33258b4687facdc0cec756d3bcadf3c983bddbcfed7c678f9ae195d57` |
| `.ufo/waves/round-15/build/ReconDirtyRevision.md:3,123` | `X-LANE-ID` / 2 | `e05cdb96b70d60c7f1c4983379f904246c4d36a53245c892bd2626f2d16e27fc` |
| `.ufo/waves/round-15/build/ReconFieldTypes.md:3` | `X-LANE-ID` / 1 | `df3fa59668c39cff525d4758f8c3a15a28f4df76d9920f00e6d09b6d99e21284` |
| `.ufo/waves/round-15/build/ReconLegacySignal.md:3` | `X-LANE-ID` / 1 | `45ad9952759914223c766af40a35a89a0bd1a717f953bc07ee87e757486abd37` |
| `.ufo/waves/round-15/build/ReconProtectedTeaching.md:3,30` | `X-LANE-ID` / 2 | `4c78588bbadb696fd2ec7c1af64818087e00d09e95e93a2bb92032b6e4ac780d` |
| `.ufo/waves/round-15/build/ReconQueryBounds.md:4,172` | `X-LANE-ID` / 2 | `b7279ca5ce63a0fc78c8df6b1137add484462fef9a3168ff732776b6ee98581a` |
| `.ufo/waves/round-15/build/ReconResultEmitter.md:3` | `X-LANE-ID` / 1 | `be170d5aa5ae189bdb99725f33ccea72f3db79208c346773de4d11dc3951a4ef` |
| `.ufo/waves/round-15/build/RegistryFrontier.md:3,44,141` | `X-LANE-ID` / 3 | `5a05cca9e89c333375a7da708f085b2b65cfd250dfb558297c7db3fbb3f3359d` |
| `.ufo/waves/round-15/build/ReviewHarnessPacks.md:3` | `X-LANE-ID` / 1 | `53ae2f89d5d910b287df776a0a5935a1b944f4ec35b372e442e9a313e9a157f6` |
| `.ufo/waves/round-15/build/ReviewRouting.md:3` | `X-LANE-ID` / 1 | `2437506252b5f25b53bad97c644351ca2dca4ee9fd9aba3f26fccece0757143b` |
| `.ufo/waves/round-15/build/ScribeGateDecisions.md:26` | `X-LANE-ID` / 1 | `fb1788d4ffc9bb3ef5408c49e72212a6f776ccafdb8c1281fc11c9825c9b4216` |
| `.ufo/waves/round-15/build/ScribeReportContract.md:44-45` | `X-LANE-ID` / 2 | `2dec695747b41381472763805cdd4f5f9d456a7dfcb5ece20b18ca261ebd60a9` |
| `.ufo/waves/round-15/build/ScribeRoutedDebt.md:3` | `X-LANE-ID` / 1 | `70b038453e114b1bd831bf91a87d7838b14f879fd7f5deafefc5794936617948` |
| `.ufo/waves/round-15/build/ScribeSourceCensus.md:55,60` | `X-LANE-ID` / 2 | `1731f2299c90e34528aa2b3054ab4cedd8c9aabfe6f1b4a1a1befd97d2a8d602` |
| `.ufo/waves/round-15/build/SecurityTrust.md:3` | `X-LANE-ID` / 1 | `9e827faa6327a8c9a178c5621d654fcdb241fcbf9b5569f24419b1aac596254c` |
| `.ufo/waves/round-15/build/SkillInterface.md:3,98,126,132` | `X-LANE-ID` / 4 | `6562cb4396e80f596ca731735ae08b8ecb68644a58f5347b8d92dda1b15b7e00` |

### Contextual private material

- **Peer roster and tool-output excerpt — `ScribeGateDecisions.md:17-27`** (`X-PEER-ROSTER`, one disclosure block; blob hash above). This span enumerates named seats by role, gives a seat-to-agent identity form, and summarizes a task-tool response. Minimal redaction: remove the named roster, identity mapping, and response excerpt; retain only an anonymous role-level summary if needed.
- **Peer message summaries — `RegistryFrontier.md:44-47,141-143`; `SkillInterface.md:98-100,126-138`** (`X-PEER-OUTPUT`, two reports; hashes above). These attribute detailed confirmation/implementation facts to peer messages and carry peer identifiers or peer-delivered artifact details. Minimal redaction: remove peer identities and copied message-derived details; retain independently verifiable lane-owned artifact citations instead.
- **Working-tree command output — `ScribeReportContract.md:37`** (`X-TOOL-OUTPUT`, one line; hash above). This line retains a literal status-command result and path-state from the earlier report. Minimal redaction: replace the raw output with a generic statement that the wave directory was untracked at that observation, or omit it.
- **Host state and privileged-access detail — `ReconBootScope.md:20-23`; `ReconProtectedTeaching.md:30-31`** (`X-HOST-PRIV`, two repeated disclosures; hashes above). The context preserves a peer/parent-sourced package-database state and a specific privileged-access availability fact. Minimal redaction: remove the host state and access-availability detail; retain only a generic note that the applicable safety policy was followed and no package action occurred.
- **Sensitive-store pathname mention — `QualityDebt.md:9`** (`X-AUTH-PATH`, one line; hash above). It states that no credential/auth store was accessed, but names the protected store surface. No credential value was present in this context. Minimal redaction: remove the concrete store pathname, keeping the no-access assertion only if necessary.
- **Registry identity snapshot — `ScribeSourceCensus.md:55,60`; mapping note `ScribeReportContract.md:45`** (`X-REGISTRY-META`, three lines across two reports; hashes above). These preserve a timestamped registry state, the identity scheme, and a statement about the set of members. Minimal redaction: remove the timestamp, identity scheme, and member-set detail; retain a generic statement that the registry was reviewed.
- **Possible sibling-report filename in a synthetic example — `ReconDirtyRevision.md:225-229`** (`X-REPORT-ID`, one illustrative block; hash above). The surrounding text frames this as a hypothetical scenario, not observed tool output, so it is not classified as a transcript/log leak. Minimal redaction: replace the specific sibling report filename with “an untracked Markdown report” if file-identity minimization is intended.

### Search disposition

- **Frozen C1 classes:** R1–R9 each returned 0 matching lines across the requested 32-file scope. The one file omitted from the initial R9 path list was separately scanned with the same expression and also returned no matches. Thus no matching timestamped session identity, session-store path, numbered tool-output artifact, personal-document path, shell-history path, `sudoers` reference, operator config reference, routing-table key, or listed session-record field was found.
- **Extra tokens:** `bash.log` 0; `Documents` 1 (`ReconProtectedTeaching.md:183`, ordinary prose, not a personal-document path); `history` 2 (`ScribeReportContract.md:18,39`, ordinary prior-review/commit history, not shell history); `config.yml` 0; `fallback` 6 (`PackSubjectUnknown.md:149,190`; `ReconBootScope.md:129`; `ReconDirtyRevision.md:223`; `ReviewHarnessGate.md:239`; `ReviewUnitPredicate.md:26`, all technical fallback behavior rather than operator routing); `sudo` 1 (`ReconProtectedTeaching.md:31`, included above).
- No credential/auth values appeared in the searched or read match contexts. This was a scoped pattern-and-context review, not a general secret scan. Frozen policy `.ufo/waves/round-18/frozen/c1-policy.json:29` also states that its regex classes are a recall floor; this earlier-round finding is separate from the frozen C1 metric.