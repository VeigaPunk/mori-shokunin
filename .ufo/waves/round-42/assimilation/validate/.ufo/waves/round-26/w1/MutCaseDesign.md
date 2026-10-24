# MutCaseDesign — C2 mutation battery design (round 26, wave 1)

Seat: `MoriR26.MutCaseDesign` (leaf). Lane: `mori-shokunin`. Scope: design only.
Artefact: `/fast/scratch/hyaku/mori-r26/MutCaseDesign/mutants.md` — **57 mutants**, each with
(defect, minimal code change, contract rule violated, killing input, expected detector output,
kill route, frozen case id). Detectors **D1–D10**.

## What I did

* Read the claim contract only: `.ufo/waves/round-26/contract.md` (C2 section, interface, message
  grammar, verdicts and exits, case-file format, privacy and read-only clauses), its amendments
  A1–A2, and `PROVINCE.md:53` (FR10). Did **not** read `tools/mori-oom-killers.py`; did not write
  the tool or any case file. The design is blind, as instructed.
* Re-fetched the upstream earlyoom `v1.9.0` files so each mutant has a concrete code change
  (URL, access date 2026-10-22, sha256, ≤ 25-word quotes with line numbers: `mutants.md` §0).
  Later read-only lane checks (`git cat-file`, `git ls-tree`) were limited to digests and to the
  targeted word and pin scans named below; the case map comes from the case seat's written
  description.

## Upstream facts the mutants depend on (fetched 2026-10-22)

| Fact | Where |
|---|---|
| `sending SIGTERM when mem avail <= … and swap free <= …,` | `main.c:414` |
| `        SIGKILL when mem avail <= … and swap free <= …` (leading spaces, no `sending`) | `main.c:416` |
| `#define PRIPCT "%5.2lf%%"` → `10.00` prints `10.00%`, `5.00` prints ` 5.00%` (width 5, extra space) | `msg.h:10` |
| `fprintf(stderr, "earlyoom " VERSION "\n");` | `main.c:161` |
| `dryrun mode enabled, will not kill anything` | `main.c:295` |
| `low memory! at or below SIGKILL limits: …` / `… SIGTERM limits: …` | `main.c:519`, `main.c:523` |
| `sending %s to process %d uid %d "%s": …` (action line) | `kill.c:627` |
| `kill_wait()` call — the action line precedes it | `kill.c:640` |
| `dryrun, not actually sending any signal` (early return in dry-run) | `kill.c:271-273` |
| `killing whole process group %d (-g flag is active)` | `kill.c:281-282` |
| `escalating to SIGKILL after %.3f seconds` | `kill.c:318` |
| `kill failed: %s` (failure branch, after `kill_wait()`) | `kill.c:653-654` |

The `PRIPCT` width is the single most useful fact: the contract's own host-shaped quiet case
(thresholds 10.00/10.00/5.00/5.00) prints the kill pair as ` 5.00%`, so a regex allowing one
space, or an integer-only percentage, silently drops the kill thresholds. M19, M20 and M21 kill
exactly that. `kill.c:640` is the second: the action line is printed **before** `kill_wait()`, so
`kill failed:` always follows an action line, and a dry-run invocation logs `sending SIG… to
process` lines while sending nothing.

## Detector model handed to wave 2

* **D1 (primary, case level)** — `python3 -I -B tools/mori-oom-killers.py --selftest` must print
  exactly `MORI_OOM_KILLERS_SELFTEST: PASS N/N` and exit 0, with
  `N = jq '.cases|length'` of the file handed to `--cases` — **32** at the freeze tip — and the
  comparison set exactly the pinned dotted paths.
* **D2 / D3** — `--selftest --cases <missing>` and `--selftest --cases <empty>` must exit 2 with no
  `PASS` line (setup error, never a silent fall-back).
* **D4** — `--inputs <synthetic file>` must return the pure reader's verdict and exit code. This is
  also the detector for the ad-hoc mutants that no case covers.
* **D5** — privacy scan: stdout and stderr must contain no `MESSAGE` text, process name, uid,
  command line, or `--avoid`/`--prefer` expression.
* **D6** — `--dump-inputs` prints the live inputs object with the four contract keys and does not
  run the reader.
* **D7 (tamper, fields)** — change one pinned `expect.fields` value in a copy of the cases file,
  keep `schema` unchanged; the tool must not print `PASS`. Kills a mutant that ignores
  `expect.fields`.
* **D8 (tamper, count)** — trim one case from a copy; the printed `N` must follow the trimmed
  count. Kills a mutant that hard-codes `N`.
* **D9 (shape)** — on a `--inputs` run that does not take the error path, the result must carry
  exactly the contract's keys: `schema`; `earlyoom` {`state`, `version`, `grammar`, `thresholds`,
  `scope_complete`, `actions`, `dryrun`, `process_group_lines`, `dryrun_send_lines`,
  `earlier_invocation_send_lines`}; `oomd` {`state`, `notices_this_boot`}; `verdict` — no extra key
  anywhere. Carve-outs: `error` is legitimate only on the setup or internal error path
  (`contract.md:105`), so exempt it there or run D9 on every case except `c31`, `c32`, `c35`; and
  `earlyoom.state` must be one of the four enumerated values while `oomd.state` is not enumerated
  by the contract, so check it against the pinned value.
* **D10 (live mode)** — with an unreadable journal, a live-mode run must report
  `earlyoom_journal` as `null` and the verdict as `KILLERS_UNKNOWN` exit 2 (A2 A1c). Read-only: no
  unit is started, stopped or enabled.
* Baseline first: if D1 does not print the contracted line on the unmutated tool, every mutant is
  *inconclusive*, not killed. Restore rule: write back the exact pre-mutation bytes and re-check
  `sha256sum tools/mori-oom-killers.py`; the wave-2 report carries before/after hashes.

## The two case files (relayed by the case seat; digests and targeted scans verified read-only)

| File | Commit | sha256 | Carries the five `kill.c` lines |
|---|---|---|---|
| `tools/fixtures/mori-oom-killers/cases.json` — the **counted** artifact | `5b10649d`, identical at lane tip `21386b9` | `84d2343f1d672a4597a4ec5efe0fd048eb399e8b4f0f5b86cc483ff8f2e547af` | **no** |
| `tools/fixtures/mori-oom-killers/cases-supplementary.json` | `21386b9` | `277684eb8f622c2c3eeaf118f65c28d02c0196dd459052aa387989b4fb11269d` | **yes** |

Both hold 32 cases; the supplementary is byte-identical to sandbox tip `da9af11`. The counted file
was frozen before any tool existed, so the contract's seat-independence and freeze-order rules hold.
**Neither is a superset**: counted-only `c19`, `c24`, `c28`; supplementary-only `c33`, `c34`,
`c35`; 29 ids shared. The five `kill.c` lines added to `c21` are outside the contract grammar
(`kill.c:272`, `:282`, `:329`, `:338`, `:609`); `c21`'s expectations are unchanged in both files and
it pins no `earlyoom.dryrun`.

**Two of my own miscounts, corrected.** M40 (a matcher keyed on the bare word `kill`) does **not**
survive the counted file — it fires in `c16`, `c18`, `c23`, `c24` — and my first hit lists omitted
the byte-array cases. Corrected lists, recomputed read-only with the contract.md:66 decoding
applied (`c11`/`c12` decode to a `sending SIGTERM to process …` line):

* counted — `kill` → `c16`, `c18`, `c23`, `c24`; `sending` → `c01`, `c02`, `c03`, `c04`, `c11`,
  `c12`, `c13`, `c14`, `c20`, `c21`, `c28`; `process` → `c02`, `c03`, `c04`, `c11`, `c12`, `c13`,
  `c14`, `c21`.
* supplementary — `kill` → `c16`, `c18`, `c21`, `c23`; `sending` → the counted list plus `c33`,
  `c35`; `process` → the counted list plus `c35`.

The `kill` lists differ because the counted file carries `c24` and the supplementary carries `c21`
with the real `kill.c` lines. The file holds 4 near-miss cases; leading whitespace is deliberately
not one of them, because `contract.md:80` strips it.

## Amendment A2 (contract.md:152-167) — the headline finding

A2 states: "The frozen cases stay frozen; the L1 changed the tool where a rule does not contradict
a frozen case, and discloses the rest as limits. The counted value stays `PASS 32/32` on the frozen
file." So A2's eight adopted rules have **no case coverage**, with one exception.

| A2 rule | What it requires | Coverage | Mutants |
|---|---|---|---|
| A1b | a `Suppressed N messages from earlyoom.service` line in scope sets `scope_complete` false | none | M46 |
| A1c | live mode only: journal reads count as `null` unless `journalctl -q -b -n 1 _PID=1` returns a record | none, live only | M57 |
| A2b | an `ActiveState` other than `active`/`inactive` maps to `unavailable` and `KILLERS_UNKNOWN` | none | M47 |
| A5 | `killing whole process group ` lines counted in `earlyoom.process_group_lines`; counts are log lines, not processes signalled | supplementary `c21` only (the group line itself) | M48, M49 |
| A6 | under a dry-run invocation, send lines go to `earlyoom.dryrun_send_lines`, `sigterm`/`sigkill` stay 0, never positive evidence | none — no case has a dry-run invocation that also carries a send line | M50, M51, M52, M07 |
| Malformed timestamp | a record without a numeric `__MONOTONIC_TIMESTAMP` is a setup error: `KILLERS_UNKNOWN`, exit 2 | supplementary `c35` only | M24, M53 |
| Unbounded invocation | a missing or `0` anchor leaves the invocation unbounded, so `scope_complete` is false | **reached but not discriminated**: `c06`, `c07`, `c29` carry `AETM=0` in both files, but earlyoom is inactive or absent there and none pins `scope_complete` | M54 |
| Earlier invocations | `earlyoom.earlier_invocation_send_lines` counts send and escalation lines outside the current invocation; for a non-active earlyoom a non-zero count is positive evidence | **negative half only**: `c02` holds a send line at `19964361` against AETM `19964362` and pins the counters at 0; the positive half (an *inactive* earlyoom reading `KILLER_ACTED`) has no case in either file, and no case pins the field at all | M55, M56 |

The statuses above were checked by this seat read-only over both lane blobs with the tool's own
parsing rules (a timestamp is numeric when `int(str(value).strip())` succeeds, so the fixtures'
string timestamps are numeric, not malformed): no case in either file carries a `Suppressed …`
line, an `ActiveState` outside `active`/`inactive`, or a dry-run invocation that also carries a
send line; the group line appears only in the supplementary `c21`, the malformed timestamp only in
the supplementary `c35`.

**Consequence.** The counted after-state `PASS 32/32` exercises none of these rules
discriminatively, so a defect in any of them cannot move the counted value. D1 cannot kill M46,
M47, M50, M51, M54, M55 or M56 — they need ad-hoc inputs (D4); M49, M52 and M56 need the shape
check (D9); M57 needs a live-mode probe (D10). This is a coverage statement about the artifact,
not a defect of the tool, and it is the most consequential fact this battery carries. The two
exceptions where a case reaches the branch without pinning the discriminating field — `c06`/`c07`/
`c29` for the unbounded invocation, `c02` for the negative half of the earlier-invocation rule —
are recorded as *reached but not discriminated*, so the gap is not overstated in either direction.
The dry-run question itself is settled by A6 and is no longer open for anyone.

## Mutant index (57)

* Scope and timestamp: M01 anchor exclusive, M02 no anchor filter, M03 seconds not microseconds.
* Grammar: M04 threshold line counted as an action, M08 dry-run grammar too strict, M09 kill-failure
  line counted as a kill, M10 low-memory warning not counted, M22 match not prefix-anchored, M23
  byte-array `MESSAGE` not decoded, M37 leading whitespace not stripped, M38 grammar matched by
  full-string equality, M39/M40/M41 matchers keyed on the bare words "sending", "kill", "process",
  M43 `kill failed` accepted without the colon, M44 dry-run flag set on the bare word "dryrun".
* Thresholds and scope: M18 mem and swap swapped, M19 parser rejects the width-padded number, M20
  integer-only parser, M21 kill-threshold demands `sending`, M42 thresholds defaulted to a non-null
  object, M45 `scope_complete` derived from the threshold lines.
* Verdicts: M05 oomd notices dropped, M06 escalation not evidence, M07 dry-run treated as evidence,
  M11 null read reported as quiet, M12 show text without `ActiveState` read as inactive, M13
  `scope_complete` from the whole journal, M14 grammar never verified, M15 version token truncated.
* Output shape: M16 inactive killer reports zeros, M17 absent unit reported as inactive, M24
  uncaught exception exits 1, M36 state string with an extra word.
* Selftest, interface, privacy: M25 selftest ignores `expect.fields`, M26 always prints PASS, M27
  missing cases file falls back, M28 hard-coded N, M29 `--inputs` reads live state, M30 message text
  echoed, M32 a null expectation skipped, M34 only the `earlyoom` subtree compared.
* A2-derived: M46 suppressed line ignored, M47 failed unit read as inactive, M48 process-group line
  counted as an action, M49 `process_group_lines` never reported, M50 dry-run send lines counted as
  actions, M51 dry-run send lines are evidence, M52 `dryrun_send_lines` missing, M53 malformed
  timestamp skipped, M54 unbounded invocation still complete, M55 earlier-invocation lines not
  evidence, M56 `earlier_invocation_send_lines` missing, M57 live-mode journal probe skipped.
* Declared expected survivors under D1: M31 (rule 2 loses its `scope_complete` term), M33
  (`expect.exit` not compared), M35 (extra key in the result).

## Coverage, gaps and rules for wave 2

* Every C2 clause a case can discriminate has a mutant; every A2 clause has one too (table above).
* Deliberately not mutated: read-only, no-network, stdlib-only and `python3 -I -B` compliance (not
  observable through the case interface), the exact live collection commands, and the
  case-before-tool commit ordering (a process rule, checked with `git log`).
* **Rule: run every mutant against both files**, report the two runs separately, and keep the
  counted file primary because the contract's declared after-state names it. M42, M43 and M45 are
  killed only by the counted artifact; M48 and M53 only by the supplementary one; M39–M41 by both.
* **Interaction warning.** M32 hides M16 and the `c26` null pin, and M25 hides every
  field-killable mutant (M08, M09, M10, M13, M14, M16, M17, M18, M19, M20, M21). Apply M25 and M32
  last, or on separate copies.
* **How to read a survival of M09 or M10.** They are not equivalent. M10's shape is reachable on a
  live host (the warning at `main.c:519`/`:523` precedes `find_largest_process()` at
  `main.c:526-527`, and the re-check at `main.c:535-537` can print `memory situation has recovered
  while selecting victim` and skip `kill_process()` at `main.c:539`), so a survival is a coverage
  gap on a real state. M09's shape is synthetic — the failure branch at `kill.c:653-654` always
  follows the action line at `kill.c:627` through `kill_wait()` at `kill.c:640` — so a survival is
  a **rule-reading** defect, judged against the reading of `contract.md:97` that rule 1 names only
  an in-scope `sending SIG…to process` line, an escalation line, or `oomd_notices` > 0 as positive
  evidence, a reading the upstream source supports. **No L1 ruling on these two counters exists**,
  and none is claimed: the amendments contain none, and the wave-2 report must not say otherwise.
* **Declared survivors.** M31, M33 and M35 are expected to survive D1 by construction; a report that
  lists them as killed is wrong, and one that lists them as surviving with the reason is correct.
  M35 is seen by D9 once `error` is exempted on the error path.
* **Known limit of the subset-pinning convention.** The cases pin dotted paths, not whole objects,
  so an output carrying an extra key is invisible to every case; the only full-object pins are the
  whole-block null pins of `c06`, `c07`, `c08`, `c29`. That is the convention the round-25 fixture
  already uses and the cases file declares it, so it is a detector limit, not a defect of the tool
  or of the case file. D9 covers it.

## Coordination

* Sent the case seat the list of discriminating inputs my battery needs; it answered with the
  freeze tip, the case-id mapping and the pin map (its own report §9). I read neither the cases
  file nor the tool.
* The case seat corrected my D9 twice — the `error` exemption on the error path, and the
  vocabulary rule scoped to `earlyoom.state` — and re-anchored the cases file; the kill.c source
  seat supplied the source reading on `kill failed:` and `low memory!` and the reachability
  distinction. All corrections are folded in above and in `mutants.md` §1.1, §1.2 and §5,
  including the two miscounts I made and corrected (M40's apparent survival, and the hit lists that
  omitted the byte-array cases).

## Tooling

No package was installed or upgraded by this seat. Used, all pre-installed: `curl 8.23.0` (fetching
the upstream `v1.9.0` files), `python3 3.14.8` (JSON handling of the GitHub tree listing and the
targeted case scans), `jaq 3.1.1` (the `jq` front end present on this host), `git` read-only.
Reason for the fetch: the contract quotes the grammar but not the exact spacing of the upstream
percent format, and the width-5 padding of ` 5.00%` is what makes three of the mutants meaningful.

## Files written by this seat

* `/fast/scratch/hyaku/mori-r26/MutCaseDesign/mutants.md` (scratch, per the item)
* `/fast/scratch/hyaku/mori-r26/MutCaseDesign/src/` (upstream copies fetched for quoting)
* `.ufo/waves/round-26/w1/MutCaseDesign.md` (this report)

No lane commit, no ref update, no sibling-repo write.
