# Round 26 — wave 1 — WriteOomKillersCases (C2 frozen cases)

Seat: `MoriR26.WriteOomKillersCases` (executor). Lane: `mori-shokunin`. Sandbox clone:
`/fast/scratch/hyaku/mori-r26/wt-cases`, branch `r26-wt-cases`, base `28b0494004fe1f064544224eca56dd42605db384`.

## 1. Files changed

One file, written in the seat's sandbox clone only. No lane file other than this report was touched.

| Path | Action | Commit |
|---|---|---|
| `tools/fixtures/mori-oom-killers/cases.json` | added (new file), then amended twice (772 lines) | `eaa13ef98d83a1323dbb29e3bf2a418f18828cdd` (initial freeze), `4447597ffeb0c0d20c7872e0d8cdf6aa6e33e109` (amendment 1) and `da9af118799683a7a3df19d6e5a84586ff825d6e` (amendment 2; **the freeze tip**) |

- sha256 of the file bytes at the freeze tip: `277684eb8f622c2c3eeaf118f65c28d02c0196dd459052aa387989b4fb11269d`
  (earlier commits hold earlier sha256 values: `84d2343f…` at `eaa13ef`, `f6fbe301…` at `4447597`; land the tip)
- git blob id at the freeze tip: `d7c9040bb0c385d8251098c6cd0e69b70d3056b0`
- case count: **32** (contract.md:111-113 asks for the case file; the wave item asks for 24–32)
- the case ids are stable but not contiguous: `c19`, `c24` and `c28` were withdrawn and `c33`, `c34` and
  `c35` were added by amendment 1, at the request of the wave-2 mutation battery. Amendment 2 changed one
  case only: the journal of `c21` grew by the five real v1.9.0 lines that are outside the contract grammar
  (kill.c:272, 282, 329, 338, 609), with every expectation left untouched. No tool existed when either
  amendment was made, so the cases are still frozen before the tool's first commit (contract.md:57-59).
- schema: `mori-oom-killers-cases-v1`; every case has exactly `id`, `why`, `inputs`, `expect`
  (`verdict`, `exit`, `fields`); every `inputs` has exactly `earlyoom_show`, `oomd_show`,
  `earlyoom_journal`, `oomd_notices`.
- No tool was written and no tool exists in the tree (`tools/mori-oom-killers.py` is absent here), so the
  cases land strictly before the tool's first commit (contract.md:57-59).

## 2. Validation actually run

Only the checks the wave item allows (JSON parses, required keys present). No tool, no selftest.

```
$ python3 -c "<parse cases.json, assert schema, 24<=len<=32, unique ids, per-case key sets,
   verdict in {KILLER_ACTED,KILLERS_UNKNOWN,KILLERS_QUIET}, exit in {0,1,2}, fields is dict,
   inputs key set)>"
OK cases= 32
$ git show HEAD:tools/fixtures/mori-oom-killers/cases.json | sha256sum
277684eb8f622c2c3eeaf118f65c28d02c0196dd459052aa387989b4fb11269d  -
```

Verdict spread over the 32 cases: `KILLERS_QUIET` 12, `KILLER_ACTED` 11, `KILLERS_UNKNOWN` 9;
exit spread: 0 / 1 / 2 = 12 / 11 / 9. The two byte-array `MESSAGE`s were decoded once with
`bytes(...).decode('utf-8','replace')` and read back as `sending SIGTERM to process 4242 "imaginary-keeper"`
and `sending SIGTERM to process 4242 "imaginary-<?>keeper"` (one U+FFFD), i.e. the bytes are the intended ones.

## 3. Sources used for every MESSAGE string

Fetched 2026-10-22 with `curl` from the public raw URLs (no browser, no bot challenge):

| URL | sha256 of bytes | lines |
|---|---|---|
| `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c` | `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4` | 552 |
| `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c` | `b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3` | 666 |
| `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.h` | `e36604984a916fb00a624c27c73034bcd87d7d6facff9b290a6a561ee58de56c` | 24 |
| `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/meminfo.c` | `526e512c89c58cb0b1db2ae98ea62d287cdc1516846be80c9173bdc4bf0edfeb` | 286 |
| `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/globals.h` | `8cc122f9006bbad159082b0532299f4e2caee25dd556db28d4149642559c8668` | 63 |

Local copies: `/fast/scratch/hyaku/mori-r26/src-fetch/` (mine) and `/fast/scratch/hyaku/mori-r26/` (L1's, read only). Verbatim quotes used to build the fixture strings, one per grammar line:

- `main.c:161` — `fprintf(stderr, "earlyoom " VERSION "\n");`
- `main.c:414` — `fprintf(stderr, "sending SIGTERM when mem avail <= " PRIPCT " and swap free <= " PRIPCT ",\n",`
- `main.c:416` — `fprintf(stderr, "        SIGKILL when mem avail <= " PRIPCT " and swap free <= " PRIPCT "\n",`
- `main.c:295` — `warn("dryrun mode enabled, will not kill anything\n");`
- `main.c:519` — `warn("low memory! at or below SIGKILL limits: mem " PRIPCT ", swap " PRIPCT "\n",`
- `main.c:523` — `warn("low memory! at or below SIGTERM limits: mem " PRIPCT ", swap " PRIPCT "\n",`
- `kill.c:318` — `warn("escalating to SIGKILL after %.3f seconds\n", secs);`
- `kill.c:627` — `warn("sending %s to process %d uid %d \"%s\": oom_score %d, oom_score_adj %d, VmRSS %lld MiB, cmdline \"%s\"\n",`
- `kill.c:654` — `warn("kill failed: %s\n", strerror(saved_errno));`
- `msg.h:10` — `#define PRIPCT "%5.2lf%%"`

The v1.9.0 lines that exist but are **not** in the contract grammar (contract.md:80-88), pinned as negatives in
the journal of `c21`, so a reader that matches loosely cannot pass:

- `kill.c:272` — `warn("dryrun, not actually sending any signal\n");`
- `kill.c:282` — `warn("killing whole process group %d (-g flag is active)\n", res);`
- `kill.c:329` — `warn("process %d exited after %.3f seconds\n", pid, secs);`
- `kill.c:338` — `warn("process %d did not exit\n", pid);`
- `kill.c:609` — `warn("Could not find a process to kill. Sleeping 1 second.\n");`

**Why `c21` pins no dry-run flag** (checked independently against my own fetch of the v1.9.0 sources,
`kill.h` sha256 `abf8577b434096e1eb980bacc24508e8421af9edbefb0d78cf5b8b5f28160bfb`): `args.dryrun` is
assigned in exactly one place, `main.c:296` `args.dryrun = 1;`, immediately after the
`warn("dryrun mode enabled, will not kill anything\n")` at main.c:295; every other occurrence is a read
(`kill.c:197`, `kill.c:271`) or the declaration (`kill.h:37`). The `kill.c:272` line fires only from inside
that branch, and the startup print order in `main()` is banner (main.c:161), option parsing with the dry-run
warn (main.c:295), totals and thresholds (main.c:412-417), poll loop (main.c:431). So on a real host a
journal that holds a `kill.c:272` line also holds the `main.c:295` line earlier in the same invocation, both
inside the scope window. The combination in `c21` (a `kill.c:272` line with no `main.c:295` line) is
therefore a synthetic state, and the dry-run flag stays unpinned there; `c18` pins it true from main.c:295
and `c23` pins it false. The contract's grammar list stays complete for the capability it claims, so no
contract amendment is needed on this point.

**Reachability of the two non-action shapes, checked against my own fetch of the v1.9.0 sources.** The
low-memory warning of main.c:519 and main.c:523 is printed in `poll_loop()` before a victim is chosen
(main.c:526-527 `find_largest_process`), and the re-check at main.c:535-537 can print "memory situation has
recovered while selecting victim" and skip `kill_process()` (main.c:539) entirely, so a low-memory warning with
no action line is a physically reachable host state, which is the shape `c17` pins. The failed-kill line of
kill.c:654 differs: it lives in the failure branch of `kill_process()` (kill.c:653-654) and follows
`kill_wait()` at kill.c:640, always preceded by the action line printed at kill.c:627, so "kill failed: "
without an action line is a synthetic shape, like the dry-run combination in `c21`. Both `c16` and `c17` are
rule pins rather than host shapes: the L1 ratified on 2026-10-22 that neither line is positive evidence
(contract.md:97 enumerates only an in-scope `sending SIG…to process` line, an escalation line, or
`oomd_notices > 0`); nothing in the file changes because of this note.

`kill.c:627` renders `sending SIGTERM to process <pid> uid <uid> "<name>": ...`. The fixture keeps only
the invented process name after the pid (no uid, no cmdline), because the lane bound forbids carrying uid
or command line values into anything I write. The grammar is prefix anchored (contract.md:80), so the
shortened tail does not change which lines count.

`PRIPCT` is `"%5.2lf%%"`, so a one digit percent renders with a pad space (` 5.00%`) and a two digit
percent renders without one (`10.00%`). The fixture therefore carries the real byte shapes, and the
threshold expectations are numbers `10.0`/`5.0`, not strings.

Show texts use real `systemctl show` property syntax, read on this host on 2026-10-22 (read only):

- `systemctl show earlyoom.service -p LoadState,ActiveState,UnitFileState,ActiveEnterTimestampMonotonic`
  → `LoadState=loaded`, `ActiveState=active`, `UnitFileState=enabled`, `ActiveEnterTimestampMonotonic=19964362`.
- `systemctl show systemd-oomd.service -p ...` → `LoadState=loaded`, `ActiveState=inactive`,
  `UnitFileState=disabled`, `ActiveEnterTimestampMonotonic=0`.
- `systemctl show nonexistent-unit-xyz.service -p ...` → `LoadState=not-found`, `ActiveState=inactive`,
  `UnitFileState=` (empty), `ActiveEnterTimestampMonotonic=0`; this is the absent shape used in c07.

Host journal was consulted for shape only (`journalctl -q -b -u earlyoom.service -o json
--output-fields=MESSAGE`): it confirms the version line, the two threshold lines, the `mem total:` and
`mem avail:` report lines and the systemd `Started Early OOM Daemon.` line. Nothing that names a process,
a command line or a uid was copied; the host's `--prefer`/`--avoid` regex lines and any uid were not copied.
The `mem total:` / `mem avail:` figures in the fixture are invented (main.c:412, meminfo.c:279 formats);
the thresholds 10.00/10.00/5.00/5.00 are the host configuration the contract asks for.

## 4. Case table — id → rule covered

`contract.md` line numbers refer to `.ufo/waves/round-26/contract.md`.

| id | rule covered | expect |
|---|---|---|
| c01 | host shaped quiet case; grammar lines `main.c:161`, `main.c:414`, `main.c:416`; scope complete; verdict 3 (contract.md:102-104) | QUIET / 0 |
| c02 | scope boundary, one microsecond **before** `ActiveEnterTimestampMonotonic` (contract.md:78) | QUIET / 0 |
| c03 | scope boundary, **exactly at** `ActiveEnterTimestampMonotonic` (contract.md:78) | ACTED / 1 |
| c04 | incomplete scope **with** action: positive evidence stands (contract.md:97, `scope_complete` false at contract.md:90) | ACTED / 1 |
| c05 | incomplete scope **without** action (contract.md:99) | UNKNOWN / 2 |
| c06 | inactive earlyoom; `actions: null`, never zero counts (contract.md:102) | QUIET / 0 |
| c07 | absent earlyoom (`LoadState=not-found`); `actions: null` (contract.md:90, 102) | QUIET / 0 |
| c08 | **null journal** (read failed) (contract.md:66, 99) | UNKNOWN / 2 |
| c09 | **unverified version** (`earlyoom 1.4.2`) → grammar `unverified` (contract.md:90, 99) | UNKNOWN / 2 |
| c10 | **oomd notices** > 0 are positive evidence (contract.md:97) | ACTED / 1 |
| c11 | **byte-array MESSAGE** decoded as UTF-8 (contract.md:66) | ACTED / 1 |
| c12 | byte-array MESSAGE with an invalid UTF-8 byte (replacement) (contract.md:66) | ACTED / 1 |
| c13 | grammar line `sending SIGTERM to process ` (kill.c:627) | ACTED / 1 |
| c14 | grammar line `sending SIGKILL to process ` (kill.c:621, 627) | ACTED / 1 |
| c15 | grammar line `escalating to SIGKILL after ` (kill.c:318) | ACTED / 1 |
| c16 | grammar line `kill failed: ` (kill.c:654); not positive evidence per contract.md:97 | QUIET / 0 |
| c17 | grammar lines `low memory! at or below SIGTERM limits` / `... SIGKILL limits` (main.c:519, 523) | QUIET / 0 |
| c18 | grammar line `dryrun mode enabled` (main.c:295) | QUIET / 0 |
| c19 | *withdrawn* (version line only, `thresholds: null`) — replaced by c33 | — |
| c20 | near miss 1: `sending SIGTERM when` (main.c:414) is **not** an action (kill.c:627) | QUIET / 0 |
| c21 | near miss 2: mid-line `sending SIGKILL to process` is not prefix anchored (contract.md:80); plus the five real v1.9.0 lines outside the grammar (kill.c:272, 282, 329, 338, 609) must not count | QUIET / 0 |
| c22 | near miss 3: `low memory! at or below SIGTERM limit` (singular) does not match main.c:523 | QUIET / 0 |
| c23 | near miss 4: `dryrun modes enabled` does not match main.c:295 | QUIET / 0 |
| c24 | *withdrawn* (near miss 5: `kill failed` without the colon) — the near-miss count stays at 4 | — |
| c25 | null `earlyoom_show` read (contract.md:66, 99) | UNKNOWN / 2 |
| c26 | null `oomd_show` and null `oomd_notices` (contract.md:66, 99) | UNKNOWN / 2 |
| c27 | show text **lacking ActiveState** (contract.md:99) | UNKNOWN / 2 |
| c28 | *withdrawn* (oomd active and quiet) — the oomd active state is still pinned by c10 | — |
| c29 | oomd notices > 0 while earlyoom is inactive (contract.md:97 vs 102) | ACTED / 1 |
| c30 | null journal but oomd notices > 0: positive evidence stands (contract.md:97) | ACTED / 1 |
| c31 | setup error: `earlyoom_journal` is not a list (contract.md:105) | UNKNOWN / 2 |
| c32 | setup error: `earlyoom_show` is not a string or null (contract.md:105) | UNKNOWN / 2 |
| c33 | threshold lines whose mem and swap percentages differ, all four fields pinned (catches a swapped mem/swap parser) | QUIET / 0 |
| c34 | journal holding **only** an escalation line, no version line in scope → incomplete scope but positive evidence (contract.md:97) | ACTED / 1 |
| c35 | malformed `__MONOTONIC_TIMESTAMP` in a journal record → setup error, exit 2 with an error field (contract.md:105) | UNKNOWN / 2 |

Verdict rules: 1 (c03, c04, c10, c11, c12, c13, c14, c15, c29, c30, c34), 2 (c05, c08, c09, c25, c26, c27,
c31, c32, c35), 3 (c01, c02, c06, c07, c16, c17, c18, c20, c21, c22, c23, c33), 4 (c31, c32, c35).
Every grammar line of contract.md:80-88 is exercised: version (c01, c09), term thresholds (c01, c20, c33),
kill thresholds (c01, c20, c33), SIGTERM action (c03, c13, c35), SIGKILL action (c14), escalation (c15, c34),
kill failed (c16), low-memory warnings (c17, c22), dryrun (c18, c23). Near-miss cases: 4 (c20, c21, c22,
c23), which is the minimum the wave item asks for.
Cases that pin counters or thresholds and not only the verdict: c01, c03, c04, c10, c11, c12, c13, c14,
c15, c16, c17, c18, c20, c21, c22, c23, c29, c30, c33, c34 (19 of 32).

## 5. Privacy and hygiene of the fixture

- Process names are invented (`imaginary-keeper`, `imaginary-indexer`); pids are invented (4242, 5150).
- No uid, no command line, no `--prefer`/`--avoid` expression, no `/etc/default/earlyoom` value.
- The version string `1.9.0` and the thresholds `10.00/10.00/5.00/5.00` are the values contract.md:91
  allows in the output.
- `kill failed: Operation not permitted` is the `strerror` text for EPERM (kill.c:654); it names nothing.

## 6. Risks, decisions the L1 must ratify, blockers

1. **Contract-literal pins on non-action evidence.** c16 (`kill failed:` alone) and c17 (low memory warning
   alone) expect `KILLERS_QUIET`, because contract.md:97 enumerates the positive evidence as an in-scope
   `sending SIG…to process` line, an escalation line, or `oomd_notices > 0` — a failed kill and a low memory
   warning are not in that list. If the L1 wants either to be positive evidence, the contract has to be
   amended **before** the tool is written; the cases are frozen.
2. **Leading whitespace is not treated as a near miss.** contract.md:80 says the grammar is matched "after
   stripping leading whitespace", so an indented action line does count. The wave item listed "leading
   whitespace" among near-miss examples; I did not freeze a case asserting the opposite, because that would
   contradict contract.md:80. The stripping rule is exercised the other way round by the eight-space
   indented real SIGKILL threshold line (main.c:416) in c01, c20 and c33, which must still be recognised as
   a threshold line.
3. **PRIPCT padding.** The tool must accept the pad space before a one digit percent (` 5.00%`), otherwise
   c01, c20 and c33 fail on the kill thresholds. This is the one place where the contract's grammar sketch
   (`<c>%`) is looser than the real bytes.
4. **`actions: null` for a null journal (c08)** is my reading of contract.md:102 ("unavailable", "never zero
   counts") applied to a failed journal read, not an explicit contract sentence. [INFERENCE]
5. **A malformed `__MONOTONIC_TIMESTAMP` is a setup error (c35), not a record to skip.** The scope of
   contract.md:78 is defined by the numeric timestamp of every record, so a record whose timestamp is not a
   number cannot be placed in the scope. contract.md:105 gives exit 2 with `verdict: KILLERS_UNKNOWN` and an
   `error` field for setup errors; dropping the record silently would understate the action counts, which is
   what contract.md:102 forbids for unavailable data. [INFERENCE] — if the L1 wants a malformed record to be
   skipped instead, c35 has to change before the tool is written.
6. **The `error` field is not pinned.** contract.md:105 requires an `error` field on a setup error, but its
   text is implementation defined, so c31, c32 and c35 assert only `verdict` and `exit` (their `fields` is
   `{}`). The file's top level `note` says so explicitly for the tool seat.
7. **Empty `fields` for the error cases** relies on the round-25 fixture convention already in the repo
   (`tools/fixtures/mori-job-runway/cases.json`, top level `note`: "compare only the keys present in expect").
   The tool seat should compare only the dotted paths present in `expect.fields`.
8. **Version `1.4.2` in c09** is invented, used only to make the grammar unverified; the tool must report it
   verbatim as `earlyoom.version`.
9. **Threshold values are pinned as numbers** (`10.0`, `5.0`, `20.0`, `15.0`, `8.0`), because PRIPCT renders
   two decimals with a pad space and the contract names the fields as percentages (contract.md:91). A reader
   that returns the rendered strings instead of numbers fails c01, c20 and c33.
10. **Amendment history.** c19 (version line only, `thresholds: null`), c24 (fifth near miss) and c28 (oomd
   active and quiet) were withdrawn to stay inside the 24-32 band while adding c33, c34 and c35 at the wave-2
   mutation battery's request. Nothing that the wave item lists as required was dropped: the near-miss count
   is still 4, the oomd `active` state is still pinned by c10, and the version, grammar and `scope_complete`
   values are still pinned by c01 and c09. The `thresholds: null` inference of the withdrawn c19 is no longer
   pinned anywhere.
11. **The error path adds a key, so a strict key-set check must exempt it.** contract.md:105 requires the
   result of a setup or internal error to carry an `error` field next to `verdict`. The output key set of
   contract.md:90 therefore has one legitimate extra key on that path only. Any detector that asks for "the
   result carries exactly the contract's key set, no extra key anywhere" must exempt `error` on the error
   path, otherwise a tool that obeys contract.md:105 is reported as carrying an extra key. The error cases
   c31, c32 and c35 are the ones that exercise that path.

## 7. Tooling

No install, upgrade or downgrade was performed in this wave; nothing was needed beyond the pre-installed
`curl`, `python3` and `git`. No pacman transaction was run (host wide pacman pause honoured). No unit was
started, stopped, enabled or restarted; every host read was read-only (`systemctl show`, `journalctl` read).
Nothing was written outside the sandbox clone and this report.

## 8. Handoff

- Land the sandbox branch `r26-wt-cases` at its **tip** `da9af118799683a7a3df19d6e5a84586ff825d6e`
  (amendment 2 on top of `4447597ffeb0c0d20c7872e0d8cdf6aa6e33e109` and
  `eaa13ef98d83a1323dbb29e3bf2a418f18828cdd`) **before** the tool's first commit, so the cases are frozen
  first (contract.md:57-59). sha256 of the frozen file at the tip:
  `277684eb8f622c2c3eeaf118f65c28d02c0196dd459052aa387989b4fb11269d`.
- The tool seat must implement `--selftest` over these 32 cases and print `MORI_OOM_KILLERS_SELFTEST: PASS 32/32`.
- The three decisions in section 6 (items 1, 2 and 5) are the only points where the file pins a reading the
  contract does not spell out; each is ratified by the L1 on 2026-10-22.
- Wave 2 reads two artifacts, the counted file (the one the contract names) and the uncounted supplementary;
  they are not nested, so every mutant runs against both, reported separately, counted file primary. There the
  two non-action shapes are distinguished on purpose: c17's low-memory shape is physically reachable on a real
  host, c16's failed-kill shape is synthetic and a rule pin, so a survival of M10 is a coverage gap on a
  reachable state and a survival of M09 is a rule-reading question judged against contract.md:97 as ratified.
- No blocker: the case file is written, validated and frozen.
## 9. Appendix — pinned field paths per case (wave-2 detector aid)

`verdict/exit` is the pair every case pins; the column lists the dotted paths pinned in `expect.fields`.
`earlyoom.actions: null` pins the whole block as null, so the tool must compare the block, not descend into it.

| id | verdict/exit | pinned field paths |
|---|---|---|
| c01-host-quiet-thresholds | KILLERS_QUIET/0 | `earlyoom.actions.escalations`, `earlyoom.actions.kill_failed`, `earlyoom.actions.low_memory_warnings`, `earlyoom.actions.sigkill`, `earlyoom.actions.sigterm`, `earlyoom.dryrun`, `earlyoom.grammar`, `earlyoom.scope_complete`, `earlyoom.state`, `earlyoom.thresholds.kill_mem_pct`, `earlyoom.thresholds.kill_swap_pct`, `earlyoom.thresholds.term_mem_pct`, `earlyoom.thresholds.term_swap_pct`, `earlyoom.version`, `oomd.notices_this_boot`, `oomd.state` |
| c02-scope-boundary-one-microsecond-before | KILLERS_QUIET/0 | `earlyoom.actions.escalations`, `earlyoom.actions.sigkill`, `earlyoom.actions.sigterm`, `earlyoom.scope_complete`, `earlyoom.state`, `oomd.notices_this_boot`, `oomd.state` |
| c03-scope-boundary-exactly-at | KILLER_ACTED/1 | `earlyoom.actions.escalations`, `earlyoom.actions.kill_failed`, `earlyoom.actions.low_memory_warnings`, `earlyoom.actions.sigkill`, `earlyoom.actions.sigterm`, `earlyoom.scope_complete`, `earlyoom.state`, `oomd.notices_this_boot` |
| c04-incomplete-scope-with-action | KILLER_ACTED/1 | `earlyoom.actions.sigkill`, `earlyoom.actions.sigterm`, `earlyoom.grammar`, `earlyoom.scope_complete`, `earlyoom.state` |
| c05-incomplete-scope-without-action | KILLERS_UNKNOWN/2 | `earlyoom.grammar`, `earlyoom.scope_complete`, `earlyoom.state` |
| c06-earlyoom-inactive | KILLERS_QUIET/0 | `earlyoom.actions`, `earlyoom.state`, `oomd.notices_this_boot`, `oomd.state` |
| c07-earlyoom-absent | KILLERS_QUIET/0 | `earlyoom.actions`, `earlyoom.state`, `oomd.notices_this_boot`, `oomd.state` |
| c08-null-journal | KILLERS_UNKNOWN/2 | `earlyoom.actions`, `earlyoom.state`, `oomd.notices_this_boot`, `oomd.state` |
| c09-unverified-version | KILLERS_UNKNOWN/2 | `earlyoom.grammar`, `earlyoom.scope_complete`, `earlyoom.state`, `earlyoom.version`, `oomd.notices_this_boot`, `oomd.state` |
| c10-oomd-notices-positive | KILLER_ACTED/1 | `earlyoom.actions.sigkill`, `earlyoom.actions.sigterm`, `earlyoom.scope_complete`, `earlyoom.state`, `oomd.notices_this_boot`, `oomd.state` |
| c11-byte-array-message-action | KILLER_ACTED/1 | `earlyoom.actions.sigkill`, `earlyoom.actions.sigterm`, `earlyoom.scope_complete`, `earlyoom.state` |
| c12-byte-array-invalid-utf8 | KILLER_ACTED/1 | `earlyoom.actions.sigkill`, `earlyoom.actions.sigterm`, `earlyoom.scope_complete`, `earlyoom.state` |
| c13-sigterm-action | KILLER_ACTED/1 | `earlyoom.actions.escalations`, `earlyoom.actions.kill_failed`, `earlyoom.actions.low_memory_warnings`, `earlyoom.actions.sigkill`, `earlyoom.actions.sigterm`, `earlyoom.grammar`, `earlyoom.scope_complete`, `earlyoom.state` |
| c14-sigkill-action | KILLER_ACTED/1 | `earlyoom.actions.escalations`, `earlyoom.actions.sigkill`, `earlyoom.actions.sigterm`, `earlyoom.scope_complete`, `earlyoom.state` |
| c15-escalation | KILLER_ACTED/1 | `earlyoom.actions.escalations`, `earlyoom.actions.kill_failed`, `earlyoom.actions.sigkill`, `earlyoom.actions.sigterm`, `earlyoom.scope_complete`, `earlyoom.state` |
| c16-kill-failed-only | KILLERS_QUIET/0 | `earlyoom.actions.escalations`, `earlyoom.actions.kill_failed`, `earlyoom.actions.low_memory_warnings`, `earlyoom.actions.sigkill`, `earlyoom.actions.sigterm`, `earlyoom.scope_complete`, `earlyoom.state` |
| c17-low-memory-warnings | KILLERS_QUIET/0 | `earlyoom.actions.escalations`, `earlyoom.actions.kill_failed`, `earlyoom.actions.low_memory_warnings`, `earlyoom.actions.sigkill`, `earlyoom.actions.sigterm`, `earlyoom.scope_complete`, `earlyoom.state` |
| c18-dryrun-flag | KILLERS_QUIET/0 | `earlyoom.actions.sigkill`, `earlyoom.actions.sigterm`, `earlyoom.dryrun`, `earlyoom.scope_complete`, `earlyoom.state` |
| c20-nearmiss-threshold-line-is-not-an-action | KILLERS_QUIET/0 | `earlyoom.actions.escalations`, `earlyoom.actions.sigkill`, `earlyoom.actions.sigterm`, `earlyoom.state`, `earlyoom.thresholds.kill_mem_pct`, `earlyoom.thresholds.kill_swap_pct`, `earlyoom.thresholds.term_mem_pct`, `earlyoom.thresholds.term_swap_pct` |
| c21-nearmiss-midline-sigkill | KILLERS_QUIET/0 | `earlyoom.actions.escalations`, `earlyoom.actions.kill_failed`, `earlyoom.actions.sigkill`, `earlyoom.actions.sigterm`, `earlyoom.scope_complete`, `earlyoom.state` |
| c22-nearmiss-low-memory-singular-limit | KILLERS_QUIET/0 | `earlyoom.actions.low_memory_warnings`, `earlyoom.actions.sigterm`, `earlyoom.scope_complete`, `earlyoom.state` |
| c23-nearmiss-dryrun-plural | KILLERS_QUIET/0 | `earlyoom.actions.sigkill`, `earlyoom.actions.sigterm`, `earlyoom.dryrun`, `earlyoom.state` |
| c25-null-earlyoom-show | KILLERS_UNKNOWN/2 | `earlyoom.state`, `oomd.notices_this_boot`, `oomd.state` |
| c26-null-oomd-show-and-notices | KILLERS_UNKNOWN/2 | `earlyoom.scope_complete`, `earlyoom.state`, `oomd.notices_this_boot`, `oomd.state` |
| c27-show-without-activestate | KILLERS_UNKNOWN/2 | `oomd.notices_this_boot`, `oomd.state` |
| c29-oomd-notices-with-inactive-earlyoom | KILLER_ACTED/1 | `earlyoom.actions`, `earlyoom.state`, `oomd.notices_this_boot`, `oomd.state` |
| c30-null-journal-with-oomd-notices | KILLER_ACTED/1 | `earlyoom.state`, `oomd.notices_this_boot`, `oomd.state` |
| c31-error-journal-not-a-list | KILLERS_UNKNOWN/2 | (none) |
| c32-error-show-not-a-string | KILLERS_UNKNOWN/2 | (none) |
| c33-differing-thresholds-mem-and-swap | KILLERS_QUIET/0 | `earlyoom.actions.escalations`, `earlyoom.actions.kill_failed`, `earlyoom.actions.low_memory_warnings`, `earlyoom.actions.sigkill`, `earlyoom.actions.sigterm`, `earlyoom.grammar`, `earlyoom.scope_complete`, `earlyoom.state`, `earlyoom.thresholds.kill_mem_pct`, `earlyoom.thresholds.kill_swap_pct`, `earlyoom.thresholds.term_mem_pct`, `earlyoom.thresholds.term_swap_pct`, `earlyoom.version`, `oomd.notices_this_boot`, `oomd.state` |
| c34-escalation-only-incomplete-scope | KILLER_ACTED/1 | `earlyoom.actions.escalations`, `earlyoom.actions.kill_failed`, `earlyoom.actions.low_memory_warnings`, `earlyoom.actions.sigkill`, `earlyoom.actions.sigterm`, `earlyoom.grammar`, `earlyoom.scope_complete`, `earlyoom.state` |
| c35-malformed-monotonic-timestamp | KILLERS_UNKNOWN/2 | (none) |
