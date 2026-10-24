# AttackTokSeatNaming — falsification of the L1's round-18 token redactions (wave 2)

Seat: `MoriR18Recovery.AttackTokSeatNaming-2`. Leaf; no subagent dispatch. Advice to L1
MoriR18Recovery only; not a verdict.

Scope: the round-18 token-redaction change to `.ufo/waves/round-17/build/SeatNaming.md`,
attacked at tip `e2bfbd6` against entering tip `d005cdd`. Readings: `.ufo/waves/round-18/contract.md`,
`draft-verdicts.md`, `out-of-metric-triage.md`, `frozen/c1-policy.json`, `frozen/c1-population.json`,
`corpus/knowledge/evidence-minimization-r18.md`. No private text is quoted below; retained line
identity is given as path:line + SHA-256 per lane convention.

## Method (all read-only, all rc=0 unless noted)

- `git diff d005cdd e2bfbd6 -- <path>`: 1 file, 2 changed lines (2 ins / 2 del), commit `b8f5c6c`
  (the only commit touching the file in the range; `git log d005cdd..e2bfbd6 -- <path>`).
- Independent re-scan of both blobs against all nine frozen classes R1–R9, regexes copied
  verbatim from `frozen/c1-policy.json`: d005cdd = 3 hits, e2bfbd6 = 0 hits.
- Full-tree residue probes at `e2bfbd6` for the redacted token fragments: 0 tracked files each.
- Digit-run sweep of the tip blob: every 4–6-digit run is a census aggregate or the snapshot
  year; no stray process id remains.
- Old-line/new-line delta check on hunk 2: shared tail identical from the fixed anchor clause;
  exactly one token changed.
- Not run: the gate tool itself (correctness is MutRetentionGate/ReviewC1Schema scope). No tool
  installs were needed or made.

## Per-line judgment

**Hunk 1 — old line 15 (`Target (S)` line; population rows: line 15 R1 + line 15 R2, shared
`line_sha256` `8cd3f37b…`).**

1. Every private token removed: the line carried both a frozen R1 session-identity token
   (timestamp+UUID-prefix shape) and an R2 session-store path; the replacement withholds the
   whole value as a placeholder. Post-edit scan: 0 hits on the line. Tree-wide: the UUID
   fragment appears in 0 tracked files at tip.
2. No residual on the same or neighbouring lines: line 16 is a lane contract reference, line 17
   carries permitted field NAMES plus an aggregate count, line 18 carries the scan wall-clock
   instants and file-count drift — not R1-shaped, not session-record values (R9 scan 0 file-wide),
   no routing values (R8 scan 0), no retry values. PASS.
3. Meaning preserved: every downstream use references the symbol `S` (`os.walk(S, …)`,
   `find "$S"`, §9), never the literal value; the placeholder keeps `S` defined. PASS.

**Hunk 2 — old line 33 (`Log grammar` line; population row: line 33 R3, `line_sha256`
`bde28b9d…`).**

1. Every private token removed: the line's only private token was the pid-bearing tool-log name
   (R3); replaced with a generic placeholder. Tree-wide: the pid log name appears in 0 tracked
   files at tip.
2. No residual: remaining values on the line are aggregate counts (7488; tool histogram
   5454/1079/727/225/3) and tool names — inside the decision table's "counts, totals, class
   tallies" commit-as column. The single-token delta check confirms nothing else on the line
   changed. PASS.
3. No technical break: the grammar statement (`<pid>.<tool>.log`) and §1 headline stay exact.
   Cosmetic nit only: the redacted example placeholder now reads `<n>` while the same sentence's
   grammar says `<pid>` — two names for the same component; harmless, meaning intact. PASS.

JSON validity: N/A — the file is Markdown and both changed lines are prose/list items; no JSON
block exists to validate.

## Finding F-1 (low→medium): a concrete session-store file name survives the redaction

- `.ufo/waves/round-17/build/SeatNaming.md:50` (`line_sha256` `9f4f8288…`) and `:243`
  (`line_sha256` `5aea3bfa…`) each cite one concrete store cache file as
  `S/url-search/<opaque 12-char alphanumeric stem>.md` (same stem in both lines; it occurs in
  exactly 1 tracked file at tip, both lines).
- Kind: session-store artifact file name + path below the store root. `corpus/knowledge/
  evidence-minimization-r18.md`, decision table row "Session store": never commit "session
  directory/file names, paths below its root". The frozen classes do not cover it (R2 needs the
  literal `.omp/agent/sessions/` prefix) — exactly the `known_limit` recall floor the reading
  sweep exists to cover.
- Why the triage missed it: `out-of-metric-triage.md` rejects the SeatNaming family wholesale
  ("filename census counts, record-type names, key names … identity tokens in them were already
  redacted"). That rationale does not reach this token: an opaque store-minted cache stem is
  neither a count, nor a record-type/key name, nor a roster-published lane seat name. It is the
  same exposure class as the R3 pid that WAS redacted — a store-artifact identifier with low
  standalone identifying power, redacted there for consistency's sake.
- Severity: low as exposure (cache of public-source web searches; stem maps to nothing without
  store access), medium as precedent: it shows the file-wide reject outran its own rationale.
- Action: generalize the stem in both lines (e.g. `S/url-search/<stem>.md`) — zero loss of
  meaning (the lines' claims are about counts and subtree shape). No allowlist row needed.
  Single-file occurrence; no routing to other seats' files required.

## Judgment: L1's decision to keep name-only mentions as allowlistable

Defensible, with one boundary that must be stated rather than assumed:

- What is safe and consistent with the frozen policy's `adjudication_rule` (a)/(b): the retained
  mentions in this file are roster-published lane identifiers (110 prefix names, seat ids also
  used by the round-17 contract interface and accepted in `seat-live-final.json`), public-doc
  field names (`type`, `message.role`, `message.stopReason`), and record-type tokens
  (`assistant`/`toolUse`/`toolResult`). None is a value copied from a private source; none
  matches R9.
- Where the criterion breaks: "name-only" is safe only while the name exists independently of the
  observed store (lane roster, contract, public docs). Store-minted opaque tokens — timestamped
  UUID session dirs (R1), pid log names (R3), the url-search cache stem (F-1) — are VALUES that
  merely look like filenames; the fact that R1 and R3 are frozen classes while the cache stem is
  not is an accident of regex drafting, not a principled line. Recommendation: state the rule as
  "a name is allowlistable only if it is published or contractual outside the store; anything
  minted inside the store is a value" — then F-1 becomes a mechanical application, not a
  judgment call.

## Context notes (for the C1 seats, not findings)

- `corpus/evidence/retention-allowlist.json` (the path in the knowledge note's recheck command)
  does not exist at tip — consistent with draft-verdicts' "pending allowlist rows". SeatNaming
  needs no row either way: 0 frozen-class hits at tip, confirmed independently.
- `daceeec` sits after `b8f5c6c` in the range, so the "55 remaining hits at daceeec, all
  name-only" population excludes this file (0 hits) — no contradiction with the token-redaction
  claim for SeatNaming.
- Residual risk accepted, within rule: line 18's scan wall-clock instants pin the observation
  window to the minute; they are not session identities and reconstruct nothing redacted (the
  removed session id's embedded instant is not derivable from them). Noted, no action.

## Verification gaps

- I did not execute `tools/mori-retention-gate.py`; my 9-class scan reproduces the frozen
  population's 3 rows for this file exactly (lines 15 R1+R2, 33 R3), which cross-checks the
  population for this file only, not the tool.
- Exposure assessment of pushed history (pre-redaction blobs remain reachable) is
  operator/kagi-owned per the knowledge note; out of scope here.
