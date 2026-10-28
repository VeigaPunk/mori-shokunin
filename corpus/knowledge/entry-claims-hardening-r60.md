source: S561 — committed attack report `.ufo/waves/round-59/w1/Mo59Critic22.md` (D1–D5: claim text unchecked, spans not distinct, grammar orphaned, row↔artifact binding absent)
source: S562 — committed sentinel report `.ufo/waves/round-59/w1/Mo59Sentinel57.md` (F1–F4: unpinned tool bytes executed, symlink materialization escape demonstrated)
source: S563 — committed critic report `.ufo/waves/round-59/w1/Mo59Critic25.md` (drift arm accepts any nonzero exit; mutants on the wrong axis pass)
verified-at: 2026-10-28 — round-60 amended freeze `ac496c7cde8cad965079858accae3bedfe4a73f2`; counters `C2=met` / `C3=met` at that revision (`.ufo/waves/round-60/evidence/c2-at-freeze.txt`, `c3-at-freeze.txt`)
recheck: `python3 .ufo/waves/round-60/count-c2.py R` and `python3 .ufo/waves/round-60/count-c3.py R` at any named revision (both exit 0 with the frozen tokens)
coverage-map: Core — the lane's own claim-verification instruments for wave-settlement evidence (deepens the r59 entry-class instrument; no frontier row advanced, no sibling surface claimed)

# Hardened entry-claims verification and counter execution boundary (round 60)

The round-59 verifier spot-check decertified the r59 C2 instrument with four
verified met-flip classes and routed two HIGH execution-boundary findings.
The r60 hardening closes each class on the SAME real entry with no false
negative (13 claims, 13 distinct byte spans, minimum span 12 bytes at the
freeze revision).

## Entry-class predicates (`tools/mori-entry-claims-check.py`, H1–H5)

| id | predicate | closes |
|---|---|---|
| H1 | any claim-shaped line failing the frozen grammar emits `grammar:` AND blocks the verdict (r59: `grammar:` reached no arm in `measure()`; a met entry could carry unlimited malformed lines) | Mo59Reviewer08 F1; Mo59Critic22 D3 |
| H2 | every claim resolves to a distinct byte span — `line:` and `offset:` collapse to one span so aliasing is a `distinct:dup_span` duplicate; whitespace-only quotes are `span:blank`; each span carries ≥8 bytes (`span:short`) | Mo59Critic22 D2; Mo59Critic23 F1–F3 |
| H3 | claim texts are pairwise distinct and ≥10 chars (`text:short`, `text:dup`) | Mo59Critic22 D1 |
| H4 | every cited copy binds to a registry row that is mined, used-by exactly the entry, and whose source cell names the copy's `.ufo` artifact (`rows:binding`) — one fabricated row can no longer cover every copy | Mo59Critic22 D4 |
| H5 | the drift arm is reason-attributed: the pinned scan must FAIL the r53 file with a `:extra_keys=` member key-set reason AND scan OK over r54 bytes renamed to an r53-named scratch path (kills the filename-heuristic mutant M1; the reason-attribute requirement kills M2-class mutants) | Mo59Critic25 |

Limits (declared, not defects): H3/H4 check form and binding, not truth — a
false-but-well-formed sentence still needs judge scrutiny; H4's binder match
is a substring over the source cell, so a source cell naming two artifacts
binds both (over-binding is accepted, never under-binding); the drift control
uses one renamed file, so a mutant keying on bytes other than the r53
member-key set is caught only if it also flips one of the five real scans.

## Counter execution boundary (round-60 counters, G1–G3)

| id | gate | closes |
|---|---|---|
| G1 | a counter materializes and executes repo-supplied tool bytes ONLY when their sha256 equals the frozen pin; a mismatch is reason `tool_sha` with zero execution — demonstrated by the EXEC-MARKER PoC blob (never runs under the r60 counter; the revision-pinned r59 counter still reproduces the marker as the committed control) | Mo59Sentinel57 F1; Mo59Sentinel58 F1 (S562; S564 rejected as duplicate scope) |
| G2 | `materialize()` asserts containment before every write: `..` walks and symlink parents are refused (`containment:`), one honest inside-root write is accepted, nothing lands outside the scratch root | Mo59Sentinel57 F1 step 4–5 (plain `root / rel` join + symlink follow) |
| G3 | hostile-tree expect prefixes live in the counter's frozen table; a committed `expect.txt` that disagrees is `expect_tamper:<tree>` — the scored repo can no longer grade itself | Mo59Sentinel58 F2 (attacker-controlled expect.txt) |

count-c1 executes no repo-supplied tool blob at all — its re-runs are
revision-pinned (`git show <rev>:…`), which is the stronger pin; G1 is
therefore structural there.
