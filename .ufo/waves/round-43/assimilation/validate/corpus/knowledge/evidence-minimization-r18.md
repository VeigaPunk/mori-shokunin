source: S049 (OWASP Logging Cheat Sheet, "Data to exclude"), S050 (OWASP ASVS 5.0.0 V16), S051 (NIST SP 800-122 §4.2.1), S052 (OpenTelemetry "Handling sensitive data"); lane policy `.ufo/waves/round-18/frozen/c1-policy.json` (sha256 db06e9810bbfd243fb0a753a46960573df39083ea90174ce463cf2a0ab523128)
verified-at: 2026-10-21, sources opened by round-18 scribes (`.ufo/waves/round-18/build/Src{OwaspLogging,Nist800122,OtelSensitiveData}.md`); gate run by the L1 at the round-18 measured commit (see SCORECARD round 18)
recheck: `mkdir -p .scratch && TMPDIR=$PWD/.scratch python3 tools/mori-retention-gate.py --selftest` (the selftest requires TMPDIR to be `<repo>/.scratch`; remove it afterwards); `python3 tools/mori-retention-gate.py scan --repo . --rev <rev> --policy .ufo/waves/round-18/frozen/c1-policy.json --allowlist corpus/evidence/retention-allowlist.json`

# Evidence minimization for committed observability handoffs

Mori observes other sessions, the host and the fleet, then commits evidence that is pushed.
The round-17 closure ruled that copying what was observed (other-session tool output,
session identities, operator configuration values, personal documents, shell history,
privileged configuration, non-allowlisted session-record values) into committed reports
harms **adjacency**, and that disclosing the copy does not cure it
(`corpus/lessons/round-17-verifier-spotcheck.md:239,322-350`).

Rule: commit the **support** of a claim, never the observed text it came from. OWASP's
treatment vocabulary (S049: such data "should usually not be recorded directly … but instead
should be removed, masked, sanitized, hashed, or encrypted") and NIST's minimum-necessary
retention (S051 §4.2.1) apply by analogy; ASVS V16.2.5 (S050) makes it a requirement that other sensitive data such as session tokens "may only be logged by being hashed or masked". OpenTelemetry (S052) states the same practice for
telemetry pipelines and warns that "hashes are reversible in practice if the input space is small and predictable".

## Decision table — what a mori report or evidence file may carry

| Observed item | Commit as | Never commit | Checked by |
|---|---|---|---|
| Counts, totals, class tallies | integers with revision and denominator | — | gate summary reproduces |
| Lane files and lines | lane-relative `path:line` and SHA-256 | the line text when it is private | gate output prints no text |
| Other-session tool output or transcript | count and class only; artifact identity withheld | excerpts, heads/tails, paraphrased output | R1–R3 + reading sweep |
| Session store | the phrase "the session store" | session directory/file names, paths below its root | R1, R2 |
| Operator OMP configuration | "an operator-owned configuration (values withheld)"; schema defaults from public docs | file line numbers, aliases, model assignments, fallback chains | R7, R8 |
| Session-record fields | field NAMES from public docs; aggregate counts | reason/kind/note values, model strings, per-seat retry values | R9 + sweep |
| Personal documents, shell history, privileged config | "an operator document/record (contents withheld)" | paths, line numbers, planned commands, settings | R4–R6 |
| World-readable host logs (e.g. pacman.log) | line numbers, event class, package names | adjacent private context joined to them | reading sweep |
| Public sources | ≤25-word located quote, URL, access date | — | SOURCES gate |
| Synthetic fixtures | full content, marked synthetic | real values | selftest |

## Limits that bind the gate

- The nine classes are a recall floor (`c1-policy.json` `known_limit`). Round 18's reading
  sweep flagged far more context than the classes; only items in the table's "never" column
  are privacy findings. A sibling seat's result reported inside the same round's own wave
  is lane work, not private context, and is not redacted for that reason alone.
- Line SHA-256 values are provenance, not secrecy: an unsalted digest of a short, guessable
  private line can be confirmed by guessing (round-18 SentinelPrivacyDesign). Commit digests
  of whole files or long lines; never treat a digest as a redaction of a low-entropy value.
- Redacting the tip does not remove pushed history; exposure assessment and any history
  rewrite are operator/kagi decisions (`build/ConnectKagiExposure.md`).
- Instruction text in a wave context is not runtime prevention.
