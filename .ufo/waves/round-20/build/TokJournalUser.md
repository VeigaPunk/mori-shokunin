# TokJournalUser: C1 classification of two journal finding tokens

Seat: MoriR20.TokJournalUser (leaf). Lane root: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Entering tip `2061780`; census `tools/mori-census.sh` sha256 `87b8d680…ab28` (matches the receipt).
Receipt: `.ufo/waves/round-20/evidence/c1-drift-entering.json` (rc 1, 50 tokens, 8 unclassified).

## Verdict

- `+FINDING:COREDUMP_NOTICE_JOURNAL_USER`: **census-schema-change**.
- `+FINDING:SEGFAULT_SIGNAL11_JOURNAL_USER`: **census-schema-change**.
- No census-regression found for either token. Neither blocks the re-pin on its own.
- Both ids are count-gated. They appear only while the current boot holds positive records, so
  their presence will flip with host state (see Notes). The class answers why the baseline lacks
  the id. Host state only decides whether the line appears.
- Round-13 register: agrees for SEGFAULT (paired predecessor entry). No direct entry for COREDUMP,
  because its capture had zero such records.

## JSON-ready table

```
token|class|reason|evidence
+FINDING:COREDUMP_NOTICE_JOURNAL_USER|census-schema-change|Id first exists at 18d7d55 (documented r13 finding id); the r10 census-r5 pin has no such id; present now only because 36 user-scope systemd-coredump notices exist in the current boot (count-gated, count masked); emission path unchanged since 18d7d55|git log -S COREDUMP_NOTICE_JOURNAL_USER -> 18d7d55 only; tools/mori-census.sh:1076,1325,1433,1457-1459,1468; census 5be8943 has 0 occurrences; corpus/evidence/baseline-r10-20261015T2231Z.json has no COREDUMP line; .ufo/waves/round-13/build/CensusFix.md:94-95; LOG.md:725; SCORECARD.md:678; corpus/knowledge/structured-journal-scopes-r13.md:44; .ufo/waves/round-20/evidence/c1-drift-entering.json:13
+FINDING:SEGFAULT_SIGNAL11_JOURNAL_USER|census-schema-change|Documented r13 replacement of the r10 text-derived SEGFAULT_JOURNAL (its paired -FINDING token); anchored on MESSAGE_ID=fc2e22bc AND COREDUMP_SIGNAL=11; count=1 now (count masked); emission path unchanged since 18d7d55|git log -S SEGFAULT_SIGNAL11_JOURNAL_USER -> 18d7d55 only (same commit removes emit_finding SEGFAULT_JOURNAL, census 5be8943:778); tools/mori-census.sh:1327,1405-1406,1457-1459,1461-1462,1468; corpus/evidence/baseline-r10-20261015T2231Z.json:38; .ufo/waves/round-13/build/CensusFix.md:109; LOG.md:38-44,67-71; corpus/knowledge/structured-journal-scopes-r13.md:45; .ufo/waves/round-13/evidence/drift-classification.json:36; .ufo/waves/round-20/evidence/c1-drift-entering.json:16,47
```

Register-ready JSON (same content, `schema: mori-drift-classification-v1` entries):

```json
{
  "+FINDING:COREDUMP_NOTICE_JOURNAL_USER": {
    "class": "census-schema-change",
    "reason": "Id first exists at 18d7d55 (documented r13 finding id); r10 census-r5 pin has none; present now only because 36 user-scope systemd-coredump notices exist in the current boot (count-gated, count masked); emission path unchanged since 18d7d55.",
    "evidence": "git log -S COREDUMP_NOTICE_JOURNAL_USER -> 18d7d55; tools/mori-census.sh:1076,1325,1433,1457-1459,1468; corpus/evidence/baseline-r10-20261015T2231Z.json (no COREDUMP line; census 5be8943 has 0 occurrences); .ufo/waves/round-13/build/CensusFix.md:94-95; LOG.md:725; SCORECARD.md:678; corpus/knowledge/structured-journal-scopes-r13.md:44; .ufo/waves/round-20/evidence/c1-drift-entering.json:13"
  },
  "+FINDING:SEGFAULT_SIGNAL11_JOURNAL_USER": {
    "class": "census-schema-change",
    "reason": "Documented r13 replacement of the r10 text-derived SEGFAULT_JOURNAL (paired -FINDING token); anchored on MESSAGE_ID=fc2e22bc AND COREDUMP_SIGNAL=11; count=1 now (count masked); emission path unchanged since 18d7d55.",
    "evidence": "git log -S SEGFAULT_SIGNAL11_JOURNAL_USER -> 18d7d55 (same commit removes emit_finding SEGFAULT_JOURNAL, census 5be8943:778); tools/mori-census.sh:1327,1405-1406,1457-1459,1461-1462,1468; corpus/evidence/baseline-r10-20261015T2231Z.json:38; .ufo/waves/round-13/build/CensusFix.md:109; LOG.md:38-44,67-71; corpus/knowledge/structured-journal-scopes-r13.md:45; .ufo/waves/round-13/evidence/drift-classification.json:36; .ufo/waves/round-20/evidence/c1-drift-entering.json:16,47"
  }
}
```

## Decision rule (applies to the other 48 tokens too)

- **census-schema-change**: the id, or the id it replaces, is absent from the baseline census
  schema, or was renamed or retired by a documented round. A count-gated id that is new to the
  schema is schema-change even though its presence depends on host state.
- **live-state**: the id is present in both the baseline schema and the current schema, and only
  its presence differs through host counts or activity.
- **census-regression**: same id, same input class, different behavior, with no documented intent.
- **roster-change**: the lane or roster set differs.

## Token 1: `+FINDING:COREDUMP_NOTICE_JOURNAL_USER`

Emitted now (`tools/mori-census.sh`):
- `:1076` `JOURNAL_ID_COREDUMP=fc2e22bc6ee647b6b90729ab34a250b1`.
- `:1325` `user:coredump_notice)` maps to `COREDUMP_NOTICE_JOURNAL_USER` (function `journal_finding_id`, `:1321`).
- `:1433` default query branch, `MESSAGE_ID=$JOURNAL_ID_COREDUMP` through `JOURNAL_JQ_MSGID`. The
  aggregate must be `ok`: one boot, every record in the current boot.
- `:1457-1459` gate: `[ "${js[$key]}" = ok ] || continue`; `n=${jn[$key]}`; `[ "$n" -gt 0 ] || continue`.
- `:1466` subject line; `:1468` `emit_finding ... info`.
- Drift masks the count: `:2745` lists `count` in `DRIFT_COUNTER_KEYS`; `:2791` rewrites
  `\b(count|...)=[0-9]+` to `=<V>`. Only presence is compared.

Baseline (r10 pin, census `5be8943`, sha `d7710981…`, `VERSION=census-r5`):
- Zero occurrences of `COREDUMP_NOTICE_JOURNAL`, `coredump_notice` or `fc2e22bc` in `5be8943` (counted).
- `corpus/evidence/baseline-r10-20261015T2231Z.json` has no COREDUMP line. Its journal lines are
  `:10` (`SURFACE journal:`, text-derived), `:37` (`KILL_SIGNAL_JOURNAL`) and `:38` (`SEGFAULT_JOURNAL`).

Introducing commit:
- `git log -SCOREDUMP_NOTICE_JOURNAL_USER --oneline -- tools/mori-census.sh` gives only
  `18d7d55 round-13: structured journal scopes and verdict-contract repair` (2026-10-20 01:27:11 -0300).

Live state (read-only; field names and aggregates only, no MESSAGE text):
- Current boot `3e7084f470464957a8a2c00542a3b469`, up since 2026-10-20 09:57:08 local.
- `journalctl --user -b ... MESSAGE_ID=fc2e22bc…`: **36 records**, 1 boot, 36 unique `__CURSOR`,
  `_UID=1000` (36/36), `_COMM=systemd-coredum` (36/36; the 15-character `_COMM` truncation of
  systemd-coredump, a trusted field set by journald).
- Crashed `COREDUMP_COMM`: chromium 27, chrome_crashpad 3, git 3, ZCode 1, python3 1, waybar 1.
  `COREDUMP_SIGNAL_NAME`: SIGABRT 30, SIGBUS 3, SIGQUIT 1, SIGSEGV 1, SIGTRAP 1.
  First record 2026-10-20T12:57:17Z, last 2026-10-21T08:04:49Z.
- `journalctl --system -b` with the same id: 0. The system scope is readable (rc 0, records returned,
  no stderr seen), so the zero is real.
- At the round-13 capture (`live-measurement.json:6`, captured 2026-10-20T04:33:14Z, boot
  `430d3038…`), `coredump_notice=0` in both scopes (`live-measurement.json:230`).
  `drift-retained-baseline.json` contains 0 occurrences of either token.

Why schema-change and not live-state:
- Live-state needs the id in both schemas. This id is absent from the r10 schema (`5be8943`).
- The `+` means the line exists now and not in the baseline. The census-logic difference is the
  documented r13 change.

Why not census-regression: see "Regression check" below. The coredump gate, severity and subject
are unchanged from `18d7d55` to the tip.

Intent statements:
- `LOG.md:725`: declared claim, "structured journal notice counts in separately labeled user/system scopes".
- `SCORECARD.md:660-661` and `:678`: C1 "dual-scope structured journal records" row.
- `.ufo/waves/round-13/build/CensusFix.md:94-95`: finding ids incl. `COREDUMP_NOTICE_JOURNAL_{USER,SYSTEM}`, INFO.
- `corpus/knowledge/structured-journal-scopes-r13.md:44`: "coredump notice, not an OOM kill".
- `LOG.md:766-769` (round 14): "retaining all six independently scoped counts".
- `corpus/knowledge/journal-alarm-routing-r14.md:178-180`: coredump and segfault coverage stays in the existing classes.

## Token 2: `+FINDING:SEGFAULT_SIGNAL11_JOURNAL_USER`

Emitted now (`tools/mori-census.sh`):
- `:1327` `user:segfault_signal11)` maps to `SEGFAULT_SIGNAL11_JOURNAL_USER`.
- `:1405-1406` query `MESSAGE_ID=$JOURNAL_ID_COREDUMP COREDUMP_SIGNAL=11` through `JOURNAL_JQ_SIGSEGV`.
- `:1457-1459` gate (same as above); `:1461-1462` subject `class=segfault_signal11 unit=record source_field=COREDUMP_SIGNAL value=11`; `:1468` info.

Baseline:
- `5be8943:759`: unanchored `journalctl --user -b -o json COREDUMP_SIGNAL=11` count.
- `5be8943:778`: `emit_finding SEGFAULT_JOURNAL info "class=segfault count=$c_seg boot=current scope=user"`.
- Baseline file `:38`: `FINDING SEGFAULT_JOURNAL severity=info obs=class=segfault count=<V> boot=current scope=user`.

Introducing commit:
- `git log -SSEGFAULT_SIGNAL11_JOURNAL_USER` gives only `18d7d55`. That commit also removes the
  `emit_finding SEGFAULT_JOURNAL` line.

Live state: one user record (`MESSAGE_ID=fc2e22bc` AND `COREDUMP_SIGNAL=11`): `COREDUMP_COMM=waybar`,
`COREDUMP_USER_UNIT=app-Hyprland-waybar-55f739b8.scope`, `_UID=1000`. System scope 0.

Why schema-change: `.ufo/waves/round-13/build/CensusFix.md:109` records the replacement:
`segfault=N (text grep + unfiltered JSON COREDUMP_SIGNAL=11)` replaced by `segfault_signal11`,
field-validated, "coredump notices are NOT relabelled segfaults". The receipt pair
`-FINDING:SEGFAULT_JOURNAL` (`c1-drift-entering.json:47`) and `+FINDING:SEGFAULT_SIGNAL11_JOURNAL_USER`
(`:16`) is one schema change. The drop from a text-derived count (hundreds in r10 windows) to a
structured count of 1 is the intended narrowing. The pre-r13 intent that the segfault count be
structured and signal-specific is at `LOG.md:38-44` and `:67-71` (round-1 corrections 4 and 7) and
`corpus/knowledge/structured-journal-scopes-r13.md:45`.

## Regression check (both tokens)

- Exact anchor comparison of non-comment production lines, `18d7d55` against the tip. Identical:
  the coredump and segfault mappings, the `JOURNAL_ID_COREDUMP` constant, the segfault query, the
  default coredump query, the `[ "${js[$key]}" = ok ] || continue` and `[ "$n" -gt 0 ] || continue`
  gate, both subject strings. The only difference on these classes is severity: `18d7d55` sets
  `sev=info` (warn only for the user unit-SIGKILL record), the tip emits literal `info`. Same result.
- `JOURNAL_JQ_TAIL` (`:1081`), `JOURNAL_JQ_MSGID` (`:1082`) and `JOURNAL_JQ_SIGSEGV` (`:1084`) were
  rewritten from `type == "object" and ...` to `if type == "object" then ... else false end`. For
  object records the two forms are equivalent. Coredump and segfault records are objects.
- The r15 positive fallback (`JOURNAL_Q_POSITIVE_*`) is wired only for kernel OOM (`:1404`), unit
  SIGKILL (`:1408`) and unit failure (`:1415`). Coredump (`:1433`) and segfault (`:1405-1406`) have
  no positive path.
- Census commits after `18d7d55` touching journal code: `8d22d18` (round 14) and `26f6589` (round 15).
  Round-17 commits `273aa74`, `2be8294`, `fe9fa90` do not touch those lines (`git log -G` with the
  id and filter names). `VERSION` stayed `census-r6` (`18d7d55:255`, tip `:281`). The SHA changed.
- Method limit: 34 keyword-filtered hunks were reviewed, and each was printed only to its first 12 lines
  per side. The anchor-line comparison above covers the gating and emission lines that decide these tokens.

## Older register comparison (`.ufo/waves/round-13/evidence/drift-classification.json`)

| token | older entry | verdict | reason |
|---|---|---|---|
| `+FINDING:COREDUMP_NOTICE_JOURNAL_USER` | none (`c1-drift-entering.json:66` lists it unclassified) | agree by family, no direct entry | The round-13 capture (`c13df48`, census `39abda0a` identical to `18d7d55`) had zero coredump records (`live-measurement.json:230`), so the token could not appear. The family reason "intentional journal schema/version/mask change" (`drift-classification.json:38`) covers this class. |
| `+FINDING:SEGFAULT_SIGNAL11_JOURNAL_USER` | none (`c1-drift-entering.json:67`) | agree (paired) | `drift-classification.json:36` classes the retired `-FINDING:SEGFAULT_JOURNAL` as "intentional journal schema/version/mask change". This token is its successor under the same CensusFix.md:109 change. |

Out-of-scope note, not classified here: `drift-classification.json:35` labels `-FINDING:KILL_SIGNAL_JOURNAL`
only "[INFERENCE] current watchdog/wave/lane activity". That id persists in census-r6 (`tools/mori-census.sh:1329`,
user unit-SIGKILL to `KILL_SIGNAL_JOURNAL`), and its absence is count-gated. It is most likely live-state, which is
[INFERENCE] until the L1 classifies it from the closed set.

## Notes for the L1

1. **Stability.** After any re-pin, a boot with zero user coredumps flips
   `-FINDING:COREDUMP_NOTICE_JOURNAL_USER` and/or `-FINDING:SEGFAULT_SIGNAL11_JOURNAL_USER` with no
   census change. Classify those flips as live-state. Magnitude is masked, so it never drifts.
2. **Census identity.** r10 baseline = `5be8943` (`d7710981`). Round-13 = `39abda0a` (`18d7d55`, `c13df48`).
   Entering = `87b8d680`. `VERSION` stayed `census-r6` through rounds 14 to 17, so the SHA is the only identity.
3. **Parser.** `jq` resolves to `~/.local/bin/jq` (jq-1.8.2, user-writable) before `/usr/bin/jq` (jq-1.8.2,
   root-owned). My shell also has a `jq` builtin (jaq 3.1.1). Counts were identical across `/usr/bin/jq`,
   `wc -l` of the journalctl output and the builtin: 36 and 1. The PATH-shadowing concern (JSONAttack D8) remains.
4. **System scope.** Readable by this user (rc 0). The `journal.system` zeros for this boot are real.

## Method and evidence (read-only)

- Commands: `git log -S` / `-G` on the census; `git show` of `18d7d55`, `5be8943`, `2061780`; blob sha256;
  keyword-filtered hunk diff; anchor-line set comparison; `journalctl --user` / `--system` `-b -o json
  --output-fields=…` with `MESSAGE_ID=` filters (fields only); jq aggregation; reads of the receipt,
  both registers, LOG, SCORECARD and knowledge notes.
- Not run: `tools/mori-census.sh` (seat bound), any build or test, any git mutation, any subagent.
- Installs or updates: none.
- [INFERENCE]: the next census run would print `FINDING COREDUMP_NOTICE_JOURNAL_USER ... count=36` and
  `FINDING SEGFAULT_SIGNAL11_JOURNAL_USER ... count=1`. This is inferred from the emission path and the
  replayed journal queries. The census was not executed.
