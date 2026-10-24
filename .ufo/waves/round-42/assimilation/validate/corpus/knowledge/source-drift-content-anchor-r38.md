# the content half of a corpus binding: anchors that must resolve

source: S205 — the corpus contract (a row is a claim; append-only cells); S221–S225 — the round-37
redirect and fetch semantics the probe's policies rest on; S226 — canonical-path resolution.
verified-at: 2026-10-23 — `python3 .ufo/waves/round-38/count-c4.py <rev>` over the committed bytes
of the round-38 tip; the three fabricated witnesses under `.ufo/waves/round-38/fixtures/`.
recheck: on the next change to `tools/mori-source-drift.py`'s classify path or to the live receipt
format, and with the S221–S225 cadence.

## Why a token check is not a content check

The round-37 counter asked whether the knowledge entry *contained* the strings `huge_cap`,
`redirect_private_refused` and `1caa242`, whether the capability row contained the tool path, and
whether the live receipt contained the summary sentence. A critic built three witnesses that satisfy
every one of those tokens and point at nothing: an entry with the tokens and no located code, a
capability row citing a receipt that does not exist, and a live receipt with only the summary
sentence. Combined with the real tool they printed `C2=met` (r37 lesson M9). The tokens were real;
the content was imitation.

## The four content checks (counter P-C4)

1. **Anchors.** Every line of this lane's round-38 knowledge entry beginning `anchor:` names a code
   string that must occur byte-exactly in `tools/mori-source-drift.py` at the measured revision.
   Three anchors are of record:

   anchor: FETCH_MAX_BYTES = 4 * 1024 * 1024
   anchor: if not _public_redirect_target(final):
   anchor: return "drifted"

   The first two are the round-37 hardening policies; the third is the classifier's drift branch.
   A quoted code string that no longer resolves in the bytes is a stale entry, and the check fails
   rather than trusting the quote.
2. **Capability paths.** Every path the SCORECARD capability row cites must resolve at the measured
   revision **from the repository root**. The round-37 row mixed bases (`evidence/drift-live-r37.txt`
   resolved only from the wave directory), which an outside seat found by resolving each cited path;
   the round-38 correction makes every path repo-relative and the check enforces it.
3. **Named live rows.** The live receipt must carry one `<S###> drifted` line per drifted row its
   summary counts, and each id must be a registry row. The summary alone is a claim about a set the
   reader cannot enumerate.
4. **Named-row arm and its kill.** The probe's selftest asserts a named row (`S103`) grades
   `drifted` (`selftest row_states PASS`); a copy with the classifier's `return "drifted"` replaced
   by `return "excerpt"` must fail that arm and name `S103` in the failure detail. This is the
   content anchor for the *tool's own* claim: the arm is load-bearing, not decorative.

The counter also rejects the three witnesses above. `evidence/c4-before.txt` is the measured
before-state (the round-38 tip before these artifacts: `anchors=0`, capability `missing=[...]`,
`C4=unmet`); `evidence/c4-after.txt` is the after-state (`C4=met`); `evidence/v3-token-control.txt`
is the round-37 counter scoring the fabricated binding `C2=met`.

## Limits

- An anchor is a substring, not a semantics proof; the mutation arm is what makes "the code does
  the work" a separate, checkable statement.
- The live receipt is the round-37 sweep: the check proves the receipt is enumerable and matches
  the registry, not that the live bodies were reachable this round (a re-fetch is a separate run).
- The capability-path check reads the **last** row containing the capability name; an older row's
  dangling path would not be seen. The round-37 row is the last one and is the one corrected.
