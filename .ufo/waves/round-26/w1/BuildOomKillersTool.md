# BuildOomKillersTool — round 26, wave 1, claim C2

Seat: `MoriR26.BuildOomKillersTool` (executor, leaf). Lane repo:
`/home/vgpnk/Projects/shokunin/mori-shokunin`. Sandbox clone:
`/fast/scratch/hyaku/mori-r26/wt-tool` (branch `r26-wt-tool`, base `28b0494`).
Contract: `.ufo/waves/round-26/contract.md`, section C2 (lines 48-118).

## 1. What was built

One new file, written in the sandbox clone and committed there only:

| Item | Value |
|---|---|
| Path | `tools/mori-oom-killers.py` (734 lines) |
| sha256 | `7dfc65af1a6a71a1834bf0f045ed63cca384113a06f5ac242105f23bd3c2bd19` |
| Clone commit | `74df6f5` on `r26-wt-tool` (parent `28b0494`) |
| Python | 3.14.8 on this host, standard library only (`argparse`, `json`, `re`, `subprocess`, `sys`, `pathlib`) |
| Runs under | `python3 -I -B tools/mori-oom-killers.py` |

The tool is not in the lane repo and no lane commit was made. The L1 owns the
integration commit; the contract requires the frozen cases file to be committed
**before** the tool's first commit (contract.md:52-53), so the merge order is
`tools/fixtures/mori-oom-killers/cases.json` first, then this tool.

## 2. Interface as implemented

* `--inputs FILE` — reads one JSON inputs object, runs the pure reader, prints
  one JSON result object, exits with the verdict code (0 quiet, 1 acted, 2
  unknown). Contract lines 60-61.
* `--selftest [--cases FILE]` — runs every case through the same pure function
  `read_inputs()`. The default path is resolved from the script location:
  `<script dir>/fixtures/mori-oom-killers/cases.json`. A missing or empty
  cases file is a setup error: exit 2 with `verdict: KILLERS_UNKNOWN` and an
  `error` field, never a silent fall-back. Contract lines 61-63.
* no arguments — collects the inputs live, then runs the same pure function.
* `--dump-inputs` — prints the live inputs object with every `MESSAGE`
  redacted (section 6).

Result object, schema `mori-oom-killers-v1` (contract.md:90-95):

```json
{"schema": "mori-oom-killers-v1",
 "earlyoom": {"state": "active|inactive|absent|unavailable", "version": null,
              "grammar": "verified-1.9.0|unverified",
              "thresholds": {"term_mem_pct": 0.0, "term_swap_pct": 0.0, "kill_mem_pct": 0.0, "kill_swap_pct": 0.0},
              "scope_complete": false,
              "actions": {"sigterm": 0, "sigkill": 0, "escalations": 0, "kill_failed": 0, "low_memory_warnings": 0},
              "dryrun": false},
 "oomd": {"state": "active|inactive|absent|unavailable", "notices_this_boot": 0},
 "verdict": "KILLER_ACTED|KILLERS_UNKNOWN|KILLERS_QUIET"}
```

`thresholds` and `actions` are `null` when the data is unavailable; they are
never zero-filled for a killer that cannot report. An error result is
`{"schema", "earlyoom": null, "oomd": null, "verdict": "KILLERS_UNKNOWN",
"error": "<text>"}`. An uncaught exception is caught and reported as an error
result with exit 2, never exit 1 (contract.md:104-106).

Read-only: the only subprocesses are `systemctl show` and `journalctl` reads;
the only writes are stdout and stderr; no network, no unit or journal change.

## 3. Contract readings that the case seat must match

These are the places where the contract text admits more than one reading. The
tool implements the first column; if the frozen cases disagree, this is the
list of places to look.

| # | Contract wording | Tool implements | Why |
|---|---|---|---|
| R1 | "a needed read is `null`" (contract.md:99) | `earlyoom_show` and `oomd_show` are always needed. `earlyoom_journal` is needed only while earlyoom is `active`. `oomd_notices` is needed unless oomd is `absent` (an absent unit cannot have emitted notices). | The qualifier "needed" is doing work; an inactive killer needs no journal, and an absent oomd unit needs no notice count. |
| R2 | "An inactive or absent killer reports `actions: null`" (contract.md:101-104) | For a non-active earlyoom the journal is not consulted at all: `version` null, `grammar` `unverified`, `thresholds` null, `scope_complete` false, `actions` null, `dryrun` false, and no line counts as "in scope". | The scope is defined for "the current earlyoom invocation" (contract.md:78-79); a killer that is not active has none. Contract rules 2 and 3 are also conditioned on "earlyoom active". |
| R3 | thresholds type (contract.md:91-92) | JSON numbers (`10.0`, `5.0`), not the strings `"10.00"`. The contract says the output holds "states, numbers, the version string and counts" (contract.md:107-108). | The selftest comparison also accepts the numeric string spelling, so either spelling in the frozen file passes. |
| R4 | `grammar` (contract.md:91) | `verified-1.9.0` only when the in-scope version line reads exactly `1.9.0`; otherwise `unverified`. A missing version line gives `version: null` and `unverified`. | The grammar was verified against tag `v1.9.0` only. |
| R5 | `scope_complete` (contract.md:92-93) | True only when a version line is inside the scope. A journal entry without a parsable `__MONOTONIC_TIMESTAMP` is kept in scope (evidence is never dropped). | The scope is a lower bound filter on the timestamp. |
| R6 | `earlyoom.state` mapping | `LoadState=not-found` → `absent`; else `ActiveState=active` → `active`; else `ActiveState` present → `inactive`; else → `unavailable`. `unavailable` also covers a failed read. | contract.md:90-91 lists the four states; the "show text that lacks `ActiveState`" rule (contract.md:100) maps to `unavailable`. |
| R7 | thresholds all-or-nothing | `thresholds` is `null` unless both the SIGTERM and the SIGKILL threshold lines are in scope. | The contract gives the thresholds as one object of four fields (contract.md:91-93). |
| R8 | low memory warnings | Both `low memory! at or below SIGTERM limits` and `... SIGKILL limits` count into `low_memory_warnings`. | contract.md:87-88. |

Exit codes follow the contract exactly: quiet 0, acted 1, unknown 2, setup or
internal error 2.

## 4. Message grammar, checked against upstream `v1.9.0`

Fetched by this seat on 2026-10-22 with `curl` from the public raw URLs, into
`/fast/scratch/hyaku/mori-r26/BuildOomKillersTool/src/`:

| File | sha256 of fetched bytes |
|---|---|
| `main.c` | `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4` |
| `kill.c` | `b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3` |
| `msg.h` | `e36604984a916fb00a624c27c73034bcd87d7d6facff9b290a6a561ee58de56c` |

URLs: `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c`,
`.../kill.c`, `.../msg.h`. Quotes are verbatim, at most 25 words each, with the
line number in the fetched file. The contract's line numbers (main.c:161, 295,
414, 416, 519-523; kill.c:318, 627, 654) all match this fetch, so the tag is
the one the contract was written against.

* `main.c:161` — `fprintf(stderr, "earlyoom " VERSION "\n");`
* `main.c:295` — `warn("dryrun mode enabled, will not kill anything\n");`
* `main.c:414` — `fprintf(stderr, "sending SIGTERM when mem avail <= " PRIPCT " and swap free <= " PRIPCT ",\n",`
* `main.c:416` — `fprintf(stderr, "        SIGKILL when mem avail <= " PRIPCT " and swap free <= " PRIPCT "\n",`
* `main.c:519` — `warn("low memory! at or below SIGKILL limits: mem " PRIPCT ", swap " PRIPCT "\n",`
* `main.c:523` — `warn("low memory! at or below SIGTERM limits: mem " PRIPCT ", swap " PRIPCT "\n",`
* `kill.c:318` — `warn("escalating to SIGKILL after %.3f seconds\n", secs);`
* `kill.c:627` — `warn("sending %s to process %d uid %d \"%s\": oom_score %d, oom_score_adj %d, VmRSS %lld MiB, cmdline \"%s\"\n",`
* `kill.c:654` — `warn("kill failed: %s\n", strerror(saved_errno));`
* `msg.h:10` — `#define PRIPCT "%5.2lf%%"`

Two upstream details the tool handles and the contract does not spell out. The
L1 confirmed both on 2026-10-22 (PRIPCT padding accepted after `<=`;
`kill failed` and low-memory warnings counted but never positive evidence).

* `PRIPCT` is `%5.2lf%%`, so the percentage is padded to five columns: the live
  host line is `SIGKILL when mem avail <=  5.00% and swap free <=  5.00%` with
  two spaces before `5.00`. The threshold patterns accept that padding.
* `main.c:416` prints eight leading spaces before `SIGKILL`. The contract
  matches after stripping leading whitespace, so the tool strips first.
* Dry-run still prints the action literal: `kill.c:627` logs
  `sending %s to process ...` before `kill_wait()` runs at `kill.c:640`, and
  `kill_wait()` returns early in dry-run mode at `kill.c:271-274`. The tool
  follows contract rule 1 literally (an in-scope action line is positive
  evidence, with no dry-run exemption) and exposes `dryrun: true` so the
  consumer can reconcile it. Verified: a dry-run journal with one action line
  gives `KILLER_ACTED`, exit 1, `dryrun: true`.

The threshold patterns accept the trailing comma of the SIGTERM line as
optional; the upstream line carries it (`main.c:414`), and a threshold line
without it still parses.

## 5. My own tests

Throwaway cases live outside the lane and outside the clone, at
`/fast/scratch/hyaku/mori-r26/BuildOomKillersTool/my-cases.json` (20 cases).
They are not the frozen file and are not committed anywhere.

```sh
cd /fast/scratch/hyaku/mori-r26/wt-tool
python3 -I -B tools/mori-oom-killers.py --selftest \
  --cases /fast/scratch/hyaku/mori-r26/BuildOomKillersTool/my-cases.json
# MORI_OOM_KILLERS_SELFTEST: PASS 20/20   (exit 0)
```

The 20 cases, with the rule each one pins down:

1. `host-quiet` — active earlyoom 1.9.0, thresholds 10/10/5/5, oomd inactive, zero notices → quiet 0, grammar `verified-1.9.0`, `scope_complete` true, all action counts 0.
2. `inactive-earlyoom` — `actions: null` (not zero counts), version null, thresholds null → quiet 0.
3. `absent-earlyoom` — `LoadState=not-found` → state `absent`, `actions: null`.
4. `null-journal-active` — journal null while active → `KILLERS_UNKNOWN` 2.
5. `acted-sigterm` — one in-scope `sending SIGTERM to process ` line → acted 1, `sigterm` 1.
6. `acted-sigkill-and-escalation` — SIGKILL action plus escalation → acted 1, `sigkill` 1, `escalations` 1.
7. `acted-oomd-notices` — `oomd_notices` 3 with an inactive oomd → acted 1.
8. `scope-boundary-before` — a line one microsecond before `ActiveEnterTimestampMonotonic` is out of scope → not counted, scope incomplete → unknown 2.
9. `scope-boundary-at` — a line exactly at `ActiveEnterTimestampMonotonic` is in scope → acted 1.
10. `incomplete-scope-with-actions` — version line out of scope, action line in scope → acted 1, `scope_complete` false (positive evidence stands).
11. `incomplete-scope-without-actions` — version line out of scope, threshold lines in scope → unknown 2, `scope_complete` false.
12. `unverified-version` — `earlyoom 1.8.0` → `grammar: unverified` → unknown 2.
13. `byte-array-message` — `MESSAGE` as a byte array, decoded as UTF-8 with replacement; the version line arrives as bytes and still parses.
14. `dryrun-and-warnings` — dry-run flag, two low-memory warnings, one failed kill → counts only, `dryrun` true, no message text in the result.
15. `show-lacks-activestate` — show text without `ActiveState` → state `unavailable`, unknown 2.
16. `null-earlyoom-show` — failed show read → state `unavailable`, unknown 2.
17. `null-oomd-notices` — null notice count for a readable oomd unit → unknown 2.
18. `inactive-earlyoom-null-journal` — reading R1: an inactive killer needs no journal → quiet 0.
19. `absent-oomd-null-notices` — reading R1: an absent oomd unit cannot have emitted notices → quiet 0.
20. `thresholds-with-width-padding` — the `%5.2lf` padding parses → 5.0/10.0/2.5/5.0.

Command-line behaviour, each run and observed:

| Command | Result |
|---|---|
| `--selftest --cases <my file>` | `MORI_OOM_KILLERS_SELFTEST: PASS 20/20`, exit 0 |
| `--selftest` (default path, cases file not written yet) | error result, `verdict: KILLERS_UNKNOWN`, `error: cannot read cases file ...`, exit 2 |
| `--selftest --cases <empty file>` | error result, `error: cases file ... is empty`, exit 2 |
| `--selftest --cases <invalid JSON>` | error result, `error: ... is not valid JSON`, exit 2 |
| `--inputs <missing file>` | error result, `error: cannot read inputs file ...`, exit 2 |
| `--inputs <invalid JSON>` | error result, `error: ... is not valid JSON`, exit 2 |
| `--inputs <case with one action line>` | result with `sigterm: 1`, `KILLER_ACTED`, exit 1 |
| `--inputs <dry-run journal with one action line>` | `sigterm: 1`, `dryrun: true`, `KILLER_ACTED`, exit 1 (rule 1 has no dry-run exemption) |
| `--inputs <quiet case>` | `KILLERS_QUIET`, exit 0 |
| `--help` | usage, exit 0 |
| no arguments (live) | section 7, exit 0 |

Every setup and internal error prints the JSON error result on stdout and one
line on stderr, and exits 2. No path exits 1 except a verdict of
`KILLER_ACTED`.

## 6. Privacy

* The result object never carries `MESSAGE` text. Swept mechanically on the
  live inputs: every journal message was searched for in the printed result
  JSON; zero hits (`leaked classes: []`).
* `--dump-inputs` replaces every `MESSAGE` that is not a version line or a
  threshold line with its grammar class name. Class names are
  `version`, `term_thresholds`, `kill_thresholds`, `sigterm_action`,
  `sigkill_action`, `escalation`, `kill_failed`, `low_memory_term`,
  `low_memory_kill`, `dryrun`, `unclassified`. A grep of the live dump for
  `uid`, `oom_score`, `MiB` and `cmdline` returns 0 hits.
* The five v1.9.0 literals that exist outside the contract grammar (kill.c:272, :282, :329, :338, :609) classify as `unclassified` and are redacted like any other
  non-version, non-threshold message.
* No `--avoid` or `--prefer` expression and no `/etc/default/earlyoom` value
  is read, printed or quoted anywhere. No process name, command line or uid
  from this host's journal appears in this report or in the tool output; the
  only journal-derived values reproduced here are counts, states, thresholds,
  the version string and the monotonic timestamps.
* Invented process names (`widgetd`, `gadgetd`) appear only in my throwaway
  fixture file outside the repo.

## 7. Live run on this host (2026-10-22)

```sh
cd /fast/scratch/hyaku/mori-r26/wt-tool
python3 -I -B tools/mori-oom-killers.py
```

Output (exit code 0):

```json
{
  "earlyoom": {
    "actions": {
      "escalations": 0,
      "kill_failed": 0,
      "low_memory_warnings": 0,
      "sigkill": 0,
      "sigterm": 0
    },
    "dryrun": false,
    "grammar": "verified-1.9.0",
    "scope_complete": true,
    "state": "active",
    "thresholds": {
      "kill_mem_pct": 5.0,
      "kill_swap_pct": 5.0,
      "term_mem_pct": 10.0,
      "term_swap_pct": 10.0
    },
    "version": "1.9.0"
  },
  "oomd": {
    "notices_this_boot": 0,
    "state": "inactive"
  },
  "schema": "mori-oom-killers-v1",
  "verdict": "KILLERS_QUIET"
}
```

The underlying reads on this host, for the receipt:

* `systemctl show earlyoom.service -p LoadState,ActiveState,UnitFileState,ActiveEnterTimestampMonotonic`
  → `LoadState=loaded`, `ActiveState=active`, `UnitFileState=enabled`,
  `ActiveEnterTimestampMonotonic=19964362`.
* `systemctl show systemd-oomd.service -p ...` → `LoadState=loaded`,
  `ActiveState=inactive`, `UnitFileState=disabled`,
  `ActiveEnterTimestampMonotonic=0`.
* `journalctl -q -b -u earlyoom.service -o json --output-fields=MESSAGE` → 13
  JSON lines; the JSON carries `__MONOTONIC_TIMESTAMP` alongside `MESSAGE`. The
  in-scope classes are one version line, one SIGTERM threshold line and one
  SIGKILL threshold line; the rest are `unclassified` and are redacted in
  `--dump-inputs`. The oomd notice read
  (`journalctl -q -b MESSAGE_ID=d989611b15e44c9dbf31e3c81256e4ed -o json
  --output-fields=MESSAGE_ID`) returned 0 lines, so `oomd_notices` is 0.

The live JSON holds no private text by design: it carries states, counts, the
thresholds and the version string only.

## 8. Tooling

No tool was installed or upgraded by this seat: the work needed only the system `python3` (3.14.8) and `curl`, both already present. No pacman transaction was run.

## 9. Risks and what the L1 must do

* **Merge order.** The contract requires the cases file to be committed before
  the tool's first commit (contract.md:52-53). The L1 must land
  `tools/fixtures/mori-oom-killers/cases.json` first, then this file.
* **Reading R2 is the one real fork.** If the frozen cases expect a kill to
  count for an inactive earlyoom (journal consulted even when the unit is not
  active), the tool answers quiet instead. The change is local: compute the
  scope from `ActiveEnterTimestampMonotonic` regardless of state, and let the
  in-scope action and escalation lines trigger `KILLER_ACTED` while the
  reported `actions` stays `null` for a non-active killer. The L1 should say
  which reading the frozen file encodes.
* **Reading R1** decides whether a null journal with an inactive earlyoom, or a
  null notice count with an absent oomd unit, is quiet or unknown. The tool
  answers quiet; a stricter reading answers unknown. Also local to
  `read_inputs()`.
* **Thresholds type.** The tool prints numbers. The selftest comparison
  accepts a numeric string as well, so a frozen case that spells `10.00` as a
  string still passes, but a case that expects the string and reads the live
  output as text would see `10.0`.
* **`LOG.md`.** The clone carries no `LOG.md` entry: the lane bounds restrict
  this seat to its report file, and the integrating seat should add the entry
  at integration with the evidence above.
* **Not verified here.** The selftest was run against my own 20-case file, not
  against the frozen file, which does not exist yet. The frozen-file run is
  the L1's to run after the merge; the tool prints
  `MORI_OOM_KILLERS_SELFTEST: PASS n/N` and exits 0 only when `n == N > 0`,
  and prints the failing case ids otherwise.
