# mori round 26 — claim contract (attempt 1, L1 MoriR26)

Entering tip `248408f5b6610a85bcbdebe7ac0b4fa7ed51422a` (round 25 admitted, `MANIFEST.json` rounds[455]).
Written before any round-26 implementation. Targets, not results.

## Frontier area and why

Rounds 23–25 each counted a routed repair on calibration (the drift sentinel in the round-25
spot-check). This round works a different frontier area: **FR10, userspace OOM killers**
(`PROVINCE.md:53`). The admitted entry `corpus/knowledge/userspace-oom-killers-r12.md` says, in the
present tense, that both userspace killers are inactive on this host. On 2026-10-22 a read-only
check shows `earlyoom.service` active and enabled (earlyoom 1.9.0, Arch package `earlyoom 1.9.0-1`)
and `systemd-oomd.service` inactive and disabled (systemd 262). The admitted knowledge is stale, and
mori has no tool that reads what earlyoom is set to do or whether it has acted.

Routed round-25 defects R1–R8 (`corpus/lessons/round-25-verifier-spotcheck.md:172-202`) are hygiene
or named debt this round, never a counted claim.

## C1 — freshness (score 5, tied lowest active axis): supersede the stale FR10 host-state entry

Statement: four enumerated present-tense statements that this host's userspace killers are inactive
(list below) contradict the committed round-26 capture; at the landed tip none of the four phrases
remains, and a superseding entry `corpus/knowledge/userspace-oom-killers-r26.md` exists whose
`source:` line cites at least one `corpus/SOURCES.md` row opened in round 26.

Frozen list (file → exact phrase, fixed-string match):

| Id | File | Phrase |
|---|---|---|
| F1 | `corpus/knowledge/userspace-oom-killers-r12.md` | `On this host both services are inactive` |
| F2 | `corpus/knowledge/userspace-oom-killers-r12.md` | `` `systemctl is-active earlyoom.service` → `inactive` `` |
| F3 | `corpus/knowledge/userspace-oom-killers-r12.md` | `Both service units are inactive` |
| F4 | `corpus/README.md` | `inactive on this host` |

Counting command (one command over committed bytes; `R` is a revision):

```sh
R=<rev>; n=0; while IFS='|' read -r f p; do git -C /home/vgpnk/Projects/shokunin/mori-shokunin grep -q -F "$p" "$R" -- "$f" && n=$((n+1)); done < .ufo/waves/round-26/c1-phrases.txt; echo "stale_present=$n"; git -C /home/vgpnk/Projects/shokunin/mori-shokunin cat-file -e "$R:corpus/knowledge/userspace-oom-killers-r26.md" && echo r26_entry=present || echo r26_entry=absent
```

`c1-phrases.txt` holds the four `file|phrase` lines above and is frozen with this contract.
Before (at `248408f5`): `stale_present=4`, `r26_entry=absent`. Declared after (at the landed tip):
`stale_present=0`, `r26_entry=present`. The stale lines are rewritten as dated past-tense records that
name the superseding entry; they are not shadowed by a banner (QUALITY 77).

Not claimed by C1: any statement about other entries, any host-wide unit census, any kill history.

## C2 — coverage (score 6): userspace OOM killer read capability (FR10 → Core, bounded)

New read-only tool `tools/mori-oom-killers.py`, Python 3 standard library only, runs under
`python3 -I -B`. Statement: the tool passes N/N frozen cases, where the cases file
`tools/fixtures/mori-oom-killers/cases.json` is written by a seat other than the tool seat and is
committed before the tool's first commit, and N = `jq '.cases|length'` of that file at its freeze
commit (N ≥ 20). Before: `git cat-file -e 248408f5:tools/mori-oom-killers.py` exits 128. Declared
after: `python3 -I -B tools/mori-oom-killers.py --selftest` prints
`MORI_OOM_KILLERS_SELFTEST: PASS N/N` and exits 0 at the landed tip.

### Interface (binding on the tool seat and the case seat)

- `--inputs FILE`: run the pure reader on one JSON inputs object (shape below), print one JSON result
  object, exit with the verdict code. `--selftest [--cases FILE]`: run every case through the same pure
  function; default cases path resolved from the script location; an empty or missing cases file is a
  setup error (exit 2), never a silent fall-back. No arguments: collect the inputs object live
  (commands below), then run the same pure function. `--dump-inputs`: print the live inputs object
  (for receipts) without the reader.
- Inputs object:
  ```json
  {"earlyoom_show": "<text of systemctl show earlyoom.service -p LoadState,ActiveState,UnitFileState,ActiveEnterTimestampMonotonic>" | null,
   "oomd_show": "<same four properties for systemd-oomd.service>" | null,
   "earlyoom_journal": [{"MESSAGE": "...", "__MONOTONIC_TIMESTAMP": "<usec>"}] | null,
   "oomd_notices": <int> | null}
  ```
  `null` means the read failed. Live collection: `systemctl show <unit> -p ...`;
  `journalctl -q -b -u earlyoom.service -o json --output-fields=MESSAGE` (keep `MESSAGE` and
  `__MONOTONIC_TIMESTAMP` only, in memory); `journalctl -q -b MESSAGE_ID=d989611b15e44c9dbf31e3c81256e4ed -o json --output-fields=MESSAGE_ID`
  line count for `oomd_notices`. A `MESSAGE` that is a byte array in journal JSON is decoded as UTF-8
  with replacement.
- Scope: earlyoom lines whose `__MONOTONIC_TIMESTAMP` ≥ `ActiveEnterTimestampMonotonic` of the
  current earlyoom invocation, in the current boot.
- Message grammar (earlyoom 1.9.0, `main.c`/`kill.c` at tag `v1.9.0`), matched after stripping
  leading whitespace, prefix-anchored:
  - `earlyoom <version>` → version (the first line of an invocation; `main.c:161`)
  - `sending SIGTERM when mem avail <= <a>% and swap free <= <b>%,` → term thresholds (`main.c:414`)
  - `SIGKILL when mem avail <= <c>% and swap free <= <d>%` → kill thresholds (`main.c:416`)
  - `sending SIGTERM to process ` / `sending SIGKILL to process ` → one action each (`kill.c:627`)
  - `escalating to SIGKILL after ` → escalation (`kill.c:318`)
  - `kill failed: ` → failed kill (`kill.c:654`)
  - `low memory! at or below SIGTERM limits` / `... SIGKILL limits` → low-memory warning (`main.c:519-523`)
  - `dryrun mode enabled` → dry-run flag (`main.c:295`)
- Output (`schema: mori-oom-killers-v1`): `earlyoom` {`state` (`active`, `inactive`, `absent`,
  `unavailable`), `version`, `grammar` (`verified-1.9.0` or `unverified`), `thresholds`
  {`term_mem_pct`, `term_swap_pct`, `kill_mem_pct`, `kill_swap_pct`} or null, `scope_complete` (true
  only when the version line of the current invocation is inside the scope), `actions`
  {`sigterm`, `sigkill`, `escalations`, `kill_failed`, `low_memory_warnings`} or null, `dryrun`},
  `oomd` {`state`, `notices_this_boot` or null}, `verdict`.
- Verdicts and exits:
  1. `KILLER_ACTED`, exit 1: any earlyoom `sending SIG…to process` or escalation line in scope, or
     `oomd_notices` > 0. Positive evidence stands even when the scope is incomplete.
  2. `KILLERS_UNKNOWN`, exit 2: no positive evidence, and any of: a needed read is `null`; earlyoom
     active but `scope_complete` false; earlyoom active and `grammar` `unverified`; a show text that
     lacks `ActiveState`.
  3. `KILLERS_QUIET`, exit 0: otherwise. An inactive or absent killer reports `actions: null`
     (unavailable), never zero counts; quiet then means "no positive evidence from the killers that are
     readable", and the output names which killers were unavailable.
  4. Setup or internal error: exit 2 with `verdict: KILLERS_UNKNOWN` and an `error` field; an
     uncaught exception never exits 1.
- Privacy: the tool never prints `MESSAGE` text, process names, command lines, uids or the
  `--avoid`/`--prefer` expressions; output holds states, numbers, the version string and counts.
- Read-only: no writes outside stdout/stderr, no unit or journal changes, no network.

### Case file (written by the case seat, frozen before the tool)

`tools/fixtures/mori-oom-killers/cases.json`: `{"schema": "mori-oom-killers-cases-v1", "cases":
[{"id", "why", "inputs", "expect": {"verdict", "exit", "fields": {<dotted path>: <value>}}}]}`.
The cases cover each verdict rule, each grammar line, the scope boundary (a line one microsecond
before and at `ActiveEnterTimestampMonotonic`), an incomplete scope with and without actions, an
inactive and an absent earlyoom, a `null` journal, an unverified version, oomd notices, a byte-array
`MESSAGE`, and the host-shaped quiet case (thresholds 10.00/10.00/5.00/5.00). Case `MESSAGE` text uses
invented process names only.

## Held, not claimed

operability 7, depth 5, calibration 5, adjacency 6. No retirement, waiver, exploratory claim or
promotion. No-harm check: the lane retention scan (R8) is run at the entering tip and at every
candidate tip; its value at the landed tip must not exceed the entering value.
