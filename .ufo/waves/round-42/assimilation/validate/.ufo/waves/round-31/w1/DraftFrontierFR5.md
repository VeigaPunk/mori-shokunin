# Round-31 FR5 draft report — DraftFrontierFR5

## Behavior

Prepared paste-ready text for the two Round-31 C1 FR5 additions and the D5 coverage-map row. This is a draft for the L1 integration owner; it does not claim that C1 or D5 has landed. The requested watchdog entry was absent when read (`corpus/knowledge/watchdog-identity-r31.md` → not found), so the C1 summary follows the frozen contract's subject and source scope (`.ufo/waves/round-31/contract.md:12-16,28-37`), not an inspection of a completed entry.

## Ready-to-paste drafts

### C1 — appended FR5 coverage addition and frontier note

Target: `corpus/README.md`; append after the current end, line 524. Format follows the existing coverage-additions example at `corpus/README.md:447-451`.

```md
## Round-31 coverage additions

| Ground | Entry | Bounded advance |
|---|---|---|
| Watchdog daemon identity and degraded-`pgrep` visibility (FR5 partial advance) | `knowledge/watchdog-identity-r31.md` | A sourced decision table distinguishes a `pgrep` candidate from evidence of the fleet watchdog's identity and explains the limits of process-name, command-line, and start-time observations. It clarifies what a PID probe can and cannot support; it does not claim host liveness. |

## Round-31 Frontier note — FR5 narrowed, not closed

The entry narrows FR5 by explaining how PID and `/proc` observations support, and limit, watchdog-identity inference; the census probe itself is unchanged (`tools/mori-census.sh:705-720`; the C1 surface is knowledge-only under `.ufo/waves/round-31/contract.md:22-24`). [INFERENCE] No pid file exists to anchor a candidate PID: the fleet watchdog script has no PID-file references (a read-only search for `pidfile|pid_file|pid-file|\.pid|PIDFILE` returned no matches). D06 remains frontier shared with kumitate: authoritative daemon identity still needs positive real-process and negative argv-mention fixtures, since `pgrep -af` plus substring filtering can count an editor or command merely mentioning the name (`corpus/knowledge/audit-r11.md:201`; `tools/mori-census.sh:711-713`).
```

### D5 — missing coverage-map row

Target: `corpus/README.md`; append to the coverage-map table after line 43 and before its blank line 44. The map's columns are `Note | Holds | Sources` (`corpus/README.md:5-8`).

```md
| `knowledge/earlyoom-invocation-scope-r30.md` | Which current-boot earlyoom invocation a send line belongs to: version-line segmentation, systemd active-enter bounds, earlier-invocation and dry-run separation, and incomplete-scope limits. No host read or restart claim. | S118–S120, S122, S154–S160; `.ufo/waves/round-30/rule-text.md`; `tools/fixtures/mori-oom-killers/cases-a2-r30.json` |
```

## Evidence and provenance

- Coverage-map headers and existing rows: `corpus/README.md:3-8,31-43`; FR5's current boundary is `corpus/README.md:338`. The end of the current README is line 524. The Round-24 addition is the requested three-column style example (`corpus/README.md:447-451`).
- The C1 contract limits its changes to the entry, Round31 skill lines, S161+ source rows and Gate/copy artifacts; C2 is a separate new lane tool (`.ufo/waves/round-31/contract.md:22-24`). The C1 predicate requires a decision table on the named entry (`:28-37`).
- The census's watchdog probe invokes `pgrep -af shokunin-watchdog`, filters the returned text, and reports unavailable when pgrep is missing (`tools/mori-census.sh:703-720`); the current filter is at `:711-713`. The read-only search of `/home/vgpnk/Projects/shokunin/scripts/shokunin-watchdog.sh` for `pidfile|pid_file|pid-file|\.pid|PIDFILE|pgrep|daemon` returned `No matches found`. The claim that no PID file exists is therefore marked `[INFERENCE]`, not upgraded to a direct observation.
- D06 is explicitly an open argv-substring false-positive class shared with kumitate, with positive real-process and negative argv-mention fixtures required (`corpus/knowledge/audit-r11.md:201`).
- The D5 defect is verbatim in the round-30 spot-check: the entry had no map row, so the expansion could not be `improved` (`corpus/lessons/round-30-verifier-spotcheck.md:144-150,187`). The existing entry supports the proposed map summary: version-line invocation segmentation/current-boot scope (`corpus/knowledge/earlyoom-invocation-scope-r30.md:21-29`), earlier/dry-run and incomplete-scope behavior (`:46-90`), and no host read or restart claim (`:127-130`). Its older source set is stated at `:1`; S156–S160 are the new Round-30 sources recorded at `corpus/lessons/round-30.md:114-140`.

## Gates and verification

No gate, counter, test, build, or runtime probe was run. C1 acceptance remains unverified; the C1 entry did not exist at read time. D5 is a draft row only. No source files were fetched and no tools were installed.

## Touched surfaces and out of scope

Only this report file was written. `corpus/README.md`, the watchdog entry, `tools/mori-census.sh`, the fleet watchdog script, `SKILL.md`, SOURCES, lesson/Gate files, and the D5 entry were not edited. No git or jj commands, host/service changes, or live watchdog checks were performed.

Report: .ufo/waves/round-31/w1/DraftFrontierFR5.md
