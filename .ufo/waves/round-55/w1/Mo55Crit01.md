# Mo55Crit01 — C1 extractor and scope: independent completeness audit

Seat: Mo55Crit01 (critic, leaf). Lane: mori-shokunin, round 55, wave w1.
Scope of this review: the frozen C1 extractor in `.ufo/waves/round-55/count-c1.py`
(`scope()` + `TOKEN`/`HEADER_LINES` regexes), tested against the cited line-pointer
forms in the three contributing entries at the entering tip
`ca52426ea496bc6592e3e867cc9d28843e45f196`; comparison of `--scope` output against
the frozen evidence and the landed ledger; duplicate/miss analysis. No frozen files
edited. This seat emits no C1/C2 vote lines.

## Method (all commands run, evidence in scratch, scratch removed after)

1. `python3 .ufo/waves/round-55/count-c1.py --scope` (exit 0) → 78 pointers,
   byte-identical to frozen receipt `evidence/c1-scope.txt` (`diff` clean).
2. Independent audit script (`audit.py`, own candidate regexes deliberately broader
   than the frozen `TOKEN`/`HEADER_LINES`): every `path:spec`, backtick-continuation
   and `header line(s)` candidate in the four entries resolved against the v7.2-pinned
   `corpus/SOURCES.md` rows each entry cites (same basename→path rule as the frozen
   extractor), then compared normalized keys to the frozen scope set.
3. Regex-level reproduction of the frozen `TOKEN` behaviour on the failing strings.
4. `python3 .ufo/waves/round-55/count-c1.py b8b7064c2b54c8b6b22c288232a96c43fae1af47`
   (exit 1) at the measured data revision.
5. Ledger hash-set/order comparison against `--scope`; raw-bytes check of the one
   row whose disposition cell looked blank in a truncated display.
6. Basename-ambiguity scan across every S-id each entry cites.
7. v7.2 committed-copy line checks for the dropped pointer pieces.

## Counter state at data revision (reproduces the data read)

Command: `python3 .ufo/waves/round-55/count-c1.py b8b7064c2b54c8b6b22c288232a96c43fae1af47`
Output: `C1=unmet scope=78 rows=78 matched=78 status_ok=78 line_ok=78 source_rows=ok
pins=ok provenance=ok same=69 moved=7 changed=2 broken=0 holds=78 stale=0 voted=0
dissent=0 rev=b8b7064c2b54c8b6b22c288232a96c43fae1af47 failed=votes` — exit 1.
The 78/69/7/2 numbers match the frozen contract exactly; the only open arm is votes,
which the wave supplies. Ledger `corpus/knowledge/kernel-v7.3-recheck-r55.md`: 78 rows,
hash set identical to `--scope`, identical order, zero duplicate hashes, every
disposition cell populated (row `7b2d297eec60` ends `| holds |`; an earlier
120-char display truncation made it look blank — raw bytes confirm `holds`).

## Findings

### F1 — MEDIUM — header-line group truncated by a hard line wrap (miss)
`corpus/knowledge/oom-tracepoints-r47.md:17-18` cites one token:
`(S475, header lines 12, 34,` / `76, 118, 134, 150, 166, 183).` — the eight
TRACE_EVENT declaration lines of `include/trace/events/oom.h`. The frozen
`HEADER_LINES` regex runs per physical line, so it captures only `12, 34`;
the continuation `76, 118, …` on the next line has no `header line(s)` prefix
and is never seen. Frozen scope row `7b2d297eec60` therefore names
`include/trace/events/oom.h:12,34` where the entry cites
`12,34,76,118,134,150,166,183`. The committed v7.2 copy
(`corpus/evidence/sources-r47/include_trace_events_oom.h`) confirms TRACE_EVENT
starts at exactly lines 12, 34, 76, 118, 134, 150, 166, 183 — six cited v7.2
header lines silently escape the v7.3 recheck. Intended hash for the full token
`1947db66de87` is absent from scope and ledger.

### F2 — MEDIUM — comma-group spec truncated by a hard line wrap (miss)
`corpus/knowledge/oom-victim-selection-r27.md:89-90` cites
`(S148 `fs/proc/base.c:1131-1133,` / `1156-1157`)`. `TOKEN`'s `SPEC` stops at the
end of line 89 after `1131-1133` (trailing comma swallowed); line 90's leading
`1156-1157` is bare — not a backticked `:` continuation — so it is lost. Frozen
row `3b61086e4467` names `fs/proc/base.c:1131-1133` where the entry cites
`1131-1133,1156-1157`. v7.2 copy lines 1156-1157 (the
`CAP_SYS_RESOURCE`/`oom_score_adj_min` write) are real and cited but never
rechecked. Intended hash `0f9d85c18d0c` absent from scope and ledger.

### F3 — MEDIUM — dir-prefixed extensionless basename cannot match (miss ×2)
`corpus/knowledge/system-pressure-r24.md:70` `` `init/Kconfig:730-731` `` and
`:127` `` `init/Kconfig:743-760` `` (both S093, which is v7.2-pinned at
`init/Kconfig` and cited by the entry). Frozen `TOKEN` requires a dotted basename,
and the bare-`Kconfig` alternative fails the `(?<![A-Za-z0-9_./-])` lookbehind
because `Kconfig` is preceded by `/`. Proven by direct regex reproduction: both
strings produce no match. Basename `Kconfig` resolves uniquely in the entry's
basename map, so both pointers are silently dropped. Intended hashes `5ff00a82fbd5`,
`a578fc15f99e` absent. Note: `COPIES` carries no `init/Kconfig` pair either, so
the counter could not derive a status for them today — but the extractor defect is
independent of that, and the contract's own scope description says such a token
should count.

### F4 — LOW / informational — continuation with a non-token antecedent is skipped
`corpus/knowledge/oom-victim-selection-r27.md:66` backtick continuations
`` `:86-88` `` and `` `:102-103` `` have no `file:lines` token earlier on their
physical line (antecedent is the words "S149 adj page"); the frozen extractor's
per-line `last` is `None`, so they are skipped. This is per-spec behaviour — and
moot, because S149 is a man7.org page, not a v7.2-pinned source, so these lines
are outside the frozen scope definition anyway. Reported only to complete the
continuation-arm test. No scoped pointer is affected.

### F5 — OK — the arms that work (control side of the test)
Same-line backtick continuations resolve correctly, incl. comma groups:
`system-pressure-r24.md:143,242` (`cgroup-v2.rst:1066-1081` + `:1083-1087` +
`:1215-1221` + `:1911-1915` + `:2171-2175` → rows `68afd0d6fa2f`, `1490a683aca7`,
`edd8b8c361b4`, `02b8d2d11094`, `77bd396cffd3`); single-line `header line 105`
→ row `c9f1c6e1a950`; single-line comma groups and en-dash ranges normalize
(`1540,1545,1550`, `998-1006,1040-1053`, `–`→`-`). Repeat textual citations of
the same pointer dedupe by `(entry, path, norm-spec)`: 87 candidate occurrences
→ 78 keys, no duplicates. No cited basename is ambiguous across v7.2 paths in any
entry (the `len(paths)!=1` skip never fires). `watchdog-identity-r31.md` carries
no pointer token against its resolvable basenames (grep clean), matching the
contract's "contributes no pointer" claim.

## Impact on the C1 verdict

The frozen predicate defines SCOPE extractor-referentially ("every pointer the
frozen extractor finds"), so F1-F3 do NOT trip the frozen kill rules: counter,
ledger and contract stay internally consistent at 78 rows, and the data read's
only failure is the not-yet-voted arm. The defects are coverage gaps against the
contract's stated purpose ("release recheck of out-of-ledger v7.2 Linux pointers
… including comma-line groups"): four cited pointer forms are dropped or
under-specified, so the lines in F1/F2 plus the two Kconfig ranges in F3 would go
unre-checked at v7.3 with no row to flag a move or change. This is a fixable
extractor defect (cross-line continuation; dir-prefixed extensionless basenames),
not a tradeoff — but frozen edits are out of bounds this round, and adding the
missed pointers now would break `rows == len(scope)`. Route to the L1/planner for
a future freeze; score C1 on the frozen extractor as it stands.

## Findings

- MEDIUM — F1 header-line group truncated by line wrap: entry line 17-18; frozen row
  `7b2d297eec60` under-specs `include/trace/events/oom.h`; v7.2 copy lines verified.
  Evidence: scratch audit output + this report §F1.
- MEDIUM — F2 comma-group truncated by line wrap: entry line 89-90; frozen row
  `3b61086e4467` under-specs `fs/proc/base.c`. Evidence: §F2.
- MEDIUM — F3 `init/Kconfig:N` tokens unmatched (×2): system-pressure-r24.md:70,127;
  regex reproduction attached in §F3. Evidence: §F3.
- LOW — F4 non-token continuation antecedent skipped: entry line 66; per-spec, no
  scoped pointer affected. Evidence: §F4.
- OK — F5/F6/F7/F8: duplicates none; `--scope` == evidence == ledger (set+order);
  counter at data revision reproduces frozen 78/69/7/2; watchdog contributes none.
  Evidence: §"Counter state", §F5.
