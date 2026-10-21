# Review: evidence-minimization note at `e2bfbd6`

**Verdict:** actionable defects remain. The note is an added file at the attacked tip (`git diff-tree` reports `A` versus `d005cdd`), so there is no prior note body to compare; this is a review of the added claims and command, not a code-behavior change.

## Findings, by severity

### HIGH — line 43 recommends content digests more broadly than the privacy evidence supports

`corpus/knowledge/evidence-minimization-r18.md:41-43` correctly warns that a short, guessable private line's unsalted SHA-256 can be confirmed by guessing, then recommends committing whole-file or “long line” digests. The committed `SentinelPrivacyDesign` receipt instead recommends removing per-line content digests and using structural hit identities (`path`, `line`, `class`) or aggregate counts; it explicitly rejects a public salt as a remedy (`.ufo/waves/round-18/build/SentinelPrivacyDesign.md:32-38`). A long line can still contain predictable content, and the note supplies no entropy test or other basis for treating whole-file/long-line hashes as safe. S052 also warns that hashes of small/predictable identifiers may be reversible in practice (`corpus/SOURCES.md:58`).

**Fix:** remove the blanket “Commit digests of whole files or long lines” recommendation. Prefer structural metadata or aggregate counts; if any content digest is retained, state the narrow justification and residual guessability risk, and do not describe it as redaction or a general safe substitute.

### HIGH — lines 37-40 make the local “privacy finding” rule too narrow and too absolute

The note says only items in its `Never commit` column are privacy findings. The L1 triage definition also lists personal identities/emails and host home-config paths with values (`.ufo/waves/round-18/out-of-metric-triage.md:8-17`), but the decision table at `corpus/knowledge/evidence-minimization-r18.md:22-33` has no explicit general row for personal identities/emails; the host-log row only covers adjacent private context. That leaves known sweep categories without a clear table treatment while line 37 purports to make the table exhaustive. This is also a local C1 adjudication, not a general definition of privacy: the frozen policy itself says its classes are a recall floor (`.ufo/waves/round-18/frozen/c1-policy.json:27-29`).

**Fix:** add explicit `Never commit` coverage for the triage categories (including personal identities/emails) or name them as residuals, and scope the sentence to “the round-18 C1 triage classification” rather than all privacy findings. Cite the triage and frozen policy at the point of use.

### MEDIUM — line 2 claims a measured gate run without a resolving committed result

The pointer “see SCORECARD round 18” does not resolve at `e2bfbd6`: a revision-pinned search of `SCORECARD.md` for round 18 / the retention gate / C1 retention returned no matches (exit 1). The committed gate receipt records scans at `d005cdd` and `29b0dc7`, not the claimed final measured revision; the latter is explicitly non-clean (metric 120, population mismatch, four new rows) (`.ufo/waves/round-18/build/RetentionGate.md:14-24`). The round-18 evidence tree contains only `c1-before-d005cdd.json`, not a final C1 scan receipt. Thus “gate run by the L1 at the round-18 measured commit” is unsupported at the carrying commit.

**Fix:** cite a committed receipt that names the exact measured revision and its command/result, or mark the final run as unverified and remove the claim until that receipt exists. Do not use the draft verdict as the measurement receipt.

### MEDIUM — line 3 recheck is not runnable as written

`TMPDIR=<empty dir>` and `--rev <rev>` are placeholders, not usable values (the angle brackets are also shell redirection syntax). In addition, `corpus/evidence/retention-allowlist.json` is absent from the committed `e2bfbd6` tree. When `--allowlist` is supplied, the gate attempts to read that file (`tools/mori-retention-gate.py:314-320`); `read_json` converts a missing/unreadable file to setup failure (`:49-55`). The scan needs to run from the repository root for `--repo .` and the relative tool/policy paths to resolve.

**Fix:** provide an actual existing `TMPDIR`, the full revision to scan, and a repository-root working-directory instruction. Omit the optional `--allowlist` flag until a tracked allowlist exists, or point to a committed file. The interface supports the command shape (`tools/mori-retention-gate.py:673-685`), but this particular invocation does not.

### MEDIUM — line 18 overstates the OpenTelemetry recommendation

S052 supports collecting only data needed for an observability purpose, and gives separate examples of deleting an attribute, hashing a selected attribute, truncating/coarsening data, and deleting attributes outside a redaction processor's allowed list. It does not say to “hash or truncate the rest” as a general residual treatment. The source scribe records these as distinct examples and limits the source to OpenTelemetry guidance, not legal compliance (`.ufo/waves/round-18/build/SrcOtelSensitiveData.md:21-31`).

**Fix:** describe the source's distinct examples without “the rest”; make clear that the examples are selective controls, not a blanket rule for all remaining telemetry. If relying on the Collector allow-list semantics, cite that specific section/source separately.

### MEDIUM — line 32 names an unverified “SOURCES gate”

The “Checked by” cell says “SOURCES gate,” but the exact-string search at `e2bfbd6` finds only this occurrence in the note; no gate or committed check receipt is identified. The source registry itself records sources and anchors, but the note provides no evidence that an automated or defined manual gate enforces the ≤25-word, URL, and access-date conditions.

**Fix:** name the actual review/check procedure and cite its committed receipt, or call this a local manual rule and identify the required `SOURCES.md` fields. Do not imply enforcement by an unnamed gate.

### LOW — line 24 overstates what the retention gate summary reproduces

The gate's `_population_summary` emits only total hits, non-author hits, must-redact hits, file count, and `metric_before` (`tools/mori-retention-gate.py:125-133`); it does not emit per-class tallies. The scan includes individual hit records, from which a separate aggregation could be calculated, but “gate summary reproduces” does not identify that calculation or a receipt.

**Fix:** restrict the cell to the actual summary fields, or name and cite a deterministic per-class/per-file aggregation command and receipt.

### LOW — lines 37-46 have incomplete or non-resolving internal anchors

The line-37-to-40 triage decisions and same-round exception are stated without pointing to their committed L1 disposition (`.ufo/waves/round-18/out-of-metric-triage.md:8-17`). Line 42 cites “round-18 SentinelPrivacyDesign” without a path or line; line 45 uses `build/ConnectKagiExposure.md`, which is not a lane-root path and has no line; line 46 gives no source for the runtime-prevention limitation. These are resolvable receipts, but the note's citations do not meet `QUALITY.md:3-5`'s measured-anchor rule.

**Fix:** use exact lane-relative anchors, e.g. `.ufo/waves/round-18/build/SentinelPrivacyDesign.md:32-38`, `.ufo/waves/round-18/build/ConnectKagiExposure.md:18-20,32-34`, `.ufo/waves/round-18/contract.md:16-17`, and the triage lines above.

## Source coverage and overreach check

The four external IDs in the note resolve in `corpus/SOURCES.md:55-58` and have committed opening receipts: S049 and S050 in `.ufo/waves/round-18/build/SrcOwaspLogging.md:7-13,31-35`, S051 in `SrcNist800122.md:8-27`, and S052 in `SrcOtelSensitiveData.md:9-27`. S050 is covered by the OWASP Logging receipt's alternative-source section; it is not a missing scribe. I also opened the cited source URLs on 2026-10-21:

- S049: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
- S050: https://raw.githubusercontent.com/OWASP/ASVS/v5.0.0/5.0/en/0x25-V16-Security-Logging-and-Error-Handling.md
- S051: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-122.pdf
- S052: https://opentelemetry.io/docs/security/handling-sensitive-data/

The note does **not** claim that C1 is a privacy proof; it explicitly says the classes are a recall floor and that instruction text is not runtime prevention (`:37-46`), consistent with the frozen policy's known limit. S051's PII/federal-agency scope and voluntary non-federal use are recorded in `SOURCES.md:57`; the note's “by analogy” wording avoids asserting direct legal applicability. I found no independence or canonical-JSON claim in this note. The overreach is the line-43 digest recommendation, line-37 classification scope, and line-18 OTel paraphrase above.

## Verification performed and gaps

- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff-tree --no-commit-id --name-status -r d005cdd e2bfbd6f8dccc51fc06455efc41f720301112dd4 -- corpus/knowledge/evidence-minimization-r18.md` — exit 0; `A`.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin grep -n -i -E 'round.?18|round-18|mori-retention-gate|c1 retention' e2bfbd6f8dccc51fc06455efc41f720301112dd4 -- SCORECARD.md` — exit 1; no matching round-18 retention anchor.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin grep -n -F 'SOURCES gate' e2bfbd6f8dccc51fc06455efc41f720301112dd4` — exit 0; only the note's line 32.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-tree e2bfbd6f8dccc51fc06455efc41f720301112dd4 corpus/evidence/retention-allowlist.json` — exit 0; no tree entry.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-tree -r --name-only e2bfbd6f8dccc51fc06455efc41f720301112dd4 -- .ufo/waves/round-18/evidence .ufo/waves/round-18/build` — exit 0; the listed round-18 evidence includes the before receipt but no final C1 scan.
- I also ran `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show e2bfbd6f8dccc51fc06455efc41f720301112dd4:SCORECARD.md | nl -ba | head -n 60` — exit 0, read-only. This used shell `head` rather than the prescribed file-read route; no repository mutation occurred.
- LSP was unavailable in the exposed routes: `read xd://lsp` returned “No such tool.” Therefore no LSP status/references/definition/diagnostics were possible; Git search was used only for literal presence/absence, not semantic proof.
- No build, tests, selftest, or retention scan were run. No tool was installed or updated.
