# ReviewOomdWording — the oomd xattr row and the round-26 low wording defects

Seat: MoriR27.ReviewOomdWording (leaf; no subagents; no background jobs).
Date: 2026-10-22. Lane: /home/vgpnk/Projects/shokunin/mori-shokunin, HEAD `5fa0a00`;
`corpus/knowledge/userspace-oom-killers-r26.md` is clean in the working tree
(`git status --porcelain` and `git diff --stat` on that path both empty), so all entry line
numbers below are current HEAD line numbers. The prior review
(`.ufo/waves/round-26/w2/ReviewEntryOomdFacts.md`) was against tip `16935e24` (271 lines); where
its numbers differ from mine I say so (its "113" is my 112-113; its "162" is my 162).

## 1. Method

- All systemd sources fetched by ordinary curl 8.23.0 from the public raw URLs at tag `v262`,
  accessed 2026-10-22, into `/fast/scratch/hyaku/mori-r27/ReviewOomdWording/`. sha256:
  - `src/oom/oomd-util.c` — `2e94450aa337dd7d2062f2730e46e22ac00fc2c3195c11654047ddcaba487e7a` (927 lines). Identical to the blob the round-26 reviewer hashed (prefix `2e94450a`), so its citations carry over byte-for-byte.
  - `man/systemd.resource-control.xml` — `d57641df40e45811403de91e55059b6a8f7506c6812a85cbe9c6ba22900587d8` (1890 lines). Note: this file is NOT at `man/resource-control.xml` at v262 (404); it is at `man/systemd.resource-control.xml`.
  - `man/journalctl.xml` — `d54bbede45d5b1e3dc856da9624649ef8cb0829731597c212be303a76a1edbdd` (1205 lines).
  - `man/systemd.journal-fields.xml` — `ff1c00abcc8b60f3bc8243edc241f8c72da2c9249ff0e69a0286d356aad93335` (695 lines).
  - `docs/JOURNAL_EXPORT_FORMATS.md` — `207a646c067be133ff711f039bb2997a706bc5c146b7db6aa0f0350997b25543` (178 lines).
  - `src/oom/oomd.c` (`d674980745dcbe30…`) and `src/oom/oomd-manager.c` (`052f19b36d54997b…`), fetched only to confirm no other oomd file writes the two xattrs (§2).
- Every quote is verbatim with its line number; quotes are at most 25 words.
- No installs or upgrades were needed (curl 8.23.0 present). No pacman, no units touched, no
  signals, no writes outside this report and my scratch dir.

## 2. The decision-table row (entry line 198)

Current row, `corpus/knowledge/userspace-oom-killers-r26.md:198`:

```
| the `user.oomd_ooms` / `user.oomd_kill` cgroup attributes | systemd-oomd's own accounting of its kill attempts and killed pids | a durable event history: the attributes live and die with the cgroup path |
```

Source facts (systemd v262, `src/oom/oomd-util.c`):

- `user.oomd_ooms` is incremented by exactly 1 per kill attempt, **before** the kill is attempted:
  line 269 `r = increment_oomd_xattr(ctx->path, "user.oomd_ooms", 1);` — so an attempt that
  subsequently fails is still counted. The only early exit before it is skipping oomd's own
  cgroup (lines 261-266).
- `user.oomd_kill` is incremented by the number of processes killed, and only when that number
  is known and non-zero: line 303 `if (n_pids_killed == 0)`, line 305
  `else if (n_pids_killed != UINT64_MAX) {`, line 306
  `r = increment_oomd_xattr(ctx->path, "user.oomd_kill", n_pids_killed);`. `UINT64_MAX` is the
  "unknown" sentinel (line 254), used when the kernel-interface kill path does not report a count.
- The value written is a decimal counter, never a pid: `increment_oomd_xattr` reads the current
  value, parses it with `safe_atou64`, adds, and writes the sum back — line 72
  `xsprintf(buf, "%"PRIu64, curr_count + num_procs_killed);` followed by `cg_set_xattr` (line 73).
  The killed pids themselves live only in a local set that is sized (`set_size`) and freed; no pid
  is serialized anywhere.
- These are the only writers: `increment_oomd_xattr` is called only at lines 269 and 306, and a
  grep of `src/oom/oomd.c` and `src/oom/oomd-manager.c` at v262 finds no occurrence of
  `oomd_ooms`, `oomd_kill` or `increment_oomd_xattr`.
- Main text (lines 147-149) says "kill accounting is the `user.oomd_ooms` and `user.oomd_kill`
  cgroup attributes plus a `Killed` D-Bus signal" — that sentence makes no pid claim and needs no
  change.

Exact corrected wording (old -> new, unique substring of line 198):

```
OLD: systemd-oomd's own accounting of its kill attempts and killed pids
NEW: systemd-oomd's own accounting: a count of kill attempts and a count of processes killed; no pid is stored
```

The third cell ("a durable event history: the attributes live and die with the cgroup path") is
untouched; the xattr-lifetime claim was not re-verified here (the round-26 reviewer marked the
same direction `[INFERENCE]`, entry line 199).

## 3. Verification of the round-26 low wording defects

Verdicts for section 3 of `.ufo/waves/round-26/w2/ReviewEntryOomdFacts.md` ("Findings by
severity", items 1-6; item 7 is "Unverified", not a wording defect, and stays with its author).

### 3.1 Holds — O10, "killed pids" (then line 198, still line 198)

Verified directly against `oomd-util.c` (§2 above): both attributes are decimal counters; no pid
is stored. Pair in §2. **Holds.**

### 3.2 Holds — O2, the `auto` paraphrase omits the ancestor clause (lines 146-147)

Entry lines 146-147: "`auto` is the upstream default and means the cgroup's data is not actively
used for monitoring and detection." Source, `man/systemd.resource-control.xml` (v262):
line 1529 "will act on this unit's cgroups. Defaults to auto." — default confirmed; lines 1545
"will not actively use this cgroup's data for monitoring and detection" — first half confirmed;
lines 1546-1548 "a unit with auto can still be a candidate for systemd-oomd to terminate" when an
ancestor cgroup has one of the properties set to `kill` — this clause is missing from the entry.
**Holds.** Exact pair (unique substring of line 147):

```
OLD: is not actively used for monitoring and detection.
NEW: is not actively used for monitoring and detection; an `auto` unit can still be a kill candidate when an ancestor has `kill`.
```

### 3.3 Holds — O14, the set is labelled "earlyoom's records" (then 113/162; now 112, 162, and also 165)

`man/journalctl.xml` (v262): lines 322-323 — for `-u`, "a match is added for messages from the
unit … along with additional matches for messages from systemd and messages about coredumps";
lines 1168-1171 give the exact expansion:

```
_SYSTEMD_UNIT=name.service
+ UNIT=name.service _PID=1
+ OBJECT_SYSTEMD_UNIT=name.service _UID=0
+ COREDUMP_UNIT=name.service _UID=0 MESSAGE_ID=fc2e22bc6ee647b6b90729ab34a250b1
```

So the `-u earlyoom.service` result set is wider than earlyoom's own records, and the entry
itself proves the point by counting "systemd's own unit-start record" inside the 13 (lines
163-164). Pairs (each old string is unique in the entry):

```
OLD (line 162): holds 13 earlyoom records:
NEW (line 162): holds 13 `-u earlyoom.service` records:

OLD (line 165): holds 252 earlyoom records,
NEW (line 165): holds 252 `-u earlyoom.service` records,
```

plus the definition site, combined with O17 below. **Holds** (the 252 site is my addition for
consistency; the round-26 reviewer listed only 112 and 162).

### 3.4 Holds — O17, receipt time not stated (then 113-115; now 112-116)

`man/systemd.journal-fields.xml` (v262), lines 659-660: `__MONOTONIC_TIMESTAMP` is "The monotonic
time (CLOCK_MONOTONIC) at the point in time the entry was received by the journal in
microseconds". Receipt time, not write time — so a line written before the bound but received
after it counts as inside, and the entry does not say so. **Holds** (low, precision). Exact pair,
combined with the O14 fix at the definition site (unique substring spanning lines 112-113):

```
OLD: earlyoom's records for one invocation are the lines whose `__MONOTONIC_TIMESTAMP` is at or above the unit's `ActiveEnterTimestampMonotonic`;
NEW: the `-u earlyoom.service` set for one invocation is the lines whose `__MONOTONIC_TIMESTAMP` (journal receipt time) is at or above the unit's `ActiveEnterTimestampMonotonic`;
```

### 3.5 Does not hold as a defect — O5, the `Killed` signal's interface (line 148)

The facts verify: `oomd-util.c` lines 313-319 emit the signal on path `/org/freedesktop/oom1`,
interface `org.freedesktop.oom1.Manager`, name `Killed`, signature `"ss"`; and the emission sits
outside the zero/unknown guards (lines 303-309), so it fires on any kill attempt that does not
hard-fail, even when zero processes were killed (line 321 returns
`n_pids_killed > 0 && n_pids_killed != UINT64_MAX`). But the entry says only "plus a `Killed`
D-Bus signal" (line 148): it names no interface and never ties the signal to a killed-process
count, so no entry wording is contradicted. **Does not hold as a defect** — the round-26
reviewer's own O5 row said as much ("the interface is not named"). Optional, not required:
"plus a `Killed` D-Bus signal" -> "plus a `Killed` D-Bus signal on `org.freedesktop.oom1.Manager`"
if the planner wants the interface on the record.

### 3.6 Does not hold — O19, byte-array trigger vs contract wording (round-26 contract line 76)

The cited fact verifies: `docs/JOURNAL_EXPORT_FORMATS.md` (v262) line 145 "A field that contains
non-printable or non-UTF8 is serialized as a number array instead." — the array trigger is wider
than invalid UTF-8. But the contract wording ("A `MESSAGE` that is a byte array in journal JSON is
decoded as UTF-8 with replacement", `.ufo/waves/round-26/contract.md:76`, same rule carried in
the entry's recheck line 3) states a decoding rule for whatever arrays occur and makes no claim
about the trigger, exactly as the round-26 reviewer concluded ("trigger-neutral, so no tool
defect follows"). **Does not hold** — nothing to correct; the round-26 contract is also landed
history, so even a stylistic preference there is not actionable as an entry edit.

## 4. Summary

| Item | Verdict | Action |
|---|---|---|
| Row 198 "killed pids" (O10) | holds | pair in §2 |
| `auto` ancestor clause (O2) | holds | pair in §3.2 |
| "earlyoom records" label (O14) | holds | pairs in §3.3 (sites 112/162/165) |
| receipt time (O17) | holds | pair in §3.4 (merged with O14 at 112) |
| `Killed` interface (O5) | facts hold, no defect | optional wording in §3.5 |
| byte-array trigger (O19) | does not hold | none |

All four holding defects are wording/omission only; none overturns a claim in the entry.

## 5. Residual risk and verification gaps

- The xattr-lifetime claim (entry line 199, third cell of the row) was not re-verified here; it
  was already marked `[INFERENCE]` by the round-26 reviewer.
- The d989611b emitter (round-26 O7) remains unlocated; unchanged by this seat.
- `ActiveEnterTimestampMonotonic`'s own stamping path (unit.c) was not re-read; the round-26
  reviewer's reading stands unverified-by-me but uncontradicted.
- I did not re-run host journal counts; none of the six items depends on them.

## 6. Tooling record

- Used, not installed: curl 8.23.0 (source fetches), sha256sum/wc/grep (scratch only),
  `git status`/`git diff`/`git rev-parse` read-only in the lane.
- Installed or upgraded: none.
- Writes: this report only; scratch under `/fast/scratch/hyaku/mori-r27/ReviewOomdWording/`.
