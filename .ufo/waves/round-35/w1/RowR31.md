measured 2026-10-23T08:52:19Z

# Round 31 capabilities-register findings

Axes checked: execution evidence and strong-path eligibility.

## Rows

ROW: | rounds[495].capabilities_added[0] | Blind-writer gate | Provides a blind-writer gate with a passing --selftest; its round-30 run reports three missing-list hits and no longer flags CaseR30a.md:105. | `tools/mori-blind-check.sh` | 31 |
The selected path is the gate itself; the closure report names it as the landed C2 tool and records the self-test and regression results (`.ufo/reports/round-31/mori.md:28-30`, fleet commit `37b51a243302e8009c7067431e8a47f9a722fd14`). The committed receipt gives `PASS`, exit 0, and the round-30 run's three hits and exit 1 (`.ufo/waves/round-31/evidence/c2-tool-selftest-and-r30.txt:1-11` at lane commit `52435f2f425c2b4a5e7ba63d7abc1292b8736367`).
VERDICT: supported — execution is evidenced by those committed receipts. The verifier says its closure did not run the gate; it marks C2 evidence-verified and distinguishes corroborating sandbox counter runs (`corpus/lessons/round-31-verifier-spotcheck.md:9-11,109-132` at `641a6e86ecc60634d215c0a47ab86c47661abf86`).

ROW: | rounds[495].capabilities_added[1] | Watchdog identity decision table | Provides a sourced FR5 table explaining what pid probes can and cannot establish about watchdog liveness; measurements used throwaway processes and did not change the census probe. | `corpus/knowledge/watchdog-identity-r31.md` | 31 |
The selected path is the C1 decision table itself; the closure report names it, describes its FR5 scope, and records live probes on throwaway processes (`.ufo/reports/round-31/mori.md:9-11,18-20`, fleet commit `37b51a243302e8009c7067431e8a47f9a722fd14`). The report says the census probe stayed unchanged (`.ufo/reports/round-31/mori.md:87`).
VERDICT: supported — the closure records live pid-probe measurements and landed C1 table; the verifier re-measured the committed entry and reports 13 supported rows, with row 9 unsupported (`.ufo/reports/round-31/mori.md:18-20,25-27,105-107`; `corpus/lessons/round-31-verifier-spotcheck.md:81-107` at `641a6e86ecc60634d215c0a47ab86c47661abf86`). This is a documented detection/report capability, not a claim that the table is an executable tool.

## Gates and provenance

- `MANIFEST.json` at fleet commit `37b51a243302e8009c7067431e8a47f9a722fd14`, `rounds[495]`, records round 31, admitted closure, both capability strings, report path `.ufo/reports/round-31/mori.md`, and verifier spot-check `mori-shokunin/corpus/lessons/round-31-verifier-spotcheck.md@641a6e86ecc60634d215c0a47ab86c47661abf86` (read with `git show ...:MANIFEST.json | jq -c '.rounds[495]'`).
- Strong-path checks: read-only `git diff --name-status 5c99f2d4213b41966d670d10006a2ff5135273e4 52435f2f425c2b4a5e7ba63d7abc1292b8736367 -- tools/mori-blind-check.sh corpus/knowledge/watchdog-identity-r31.md` returned `A` for both paths. `git ls-tree --name-only` for the closure and lane `HEAD` (`913d22e29f131ef9cb5de9dcb7e3e272256c5f0`) listed both paths in each tree. Both paths match the capability strings and the allowed roots; the report and verifier spot-check name each whole path (`mori.md:10-11,28-30`; spot-check `:85-86,113-116`).
- The specific script and decision-table artifacts were read at lane closure `52435f2f425c2b4a5e7ba63d7abc1292b8736367`; the spot-check was read at its manifest-named revision. This checks the nominated paths, not every counter condition or claim in the round.

## Surfaces, limits, and findings

- Only this scoped report was written. No product code, judge, manifest, other report, or source artifact was edited.
- No counter or runtime check was executed by this scribe. Execution claims above rely on the closure report, committed receipt, and non-author verifier record; the verifier explicitly says it did not itself run the blind-check gate.
- No tool was installed or updated. No scratch file or background process was created. No git or jj write command was run.
