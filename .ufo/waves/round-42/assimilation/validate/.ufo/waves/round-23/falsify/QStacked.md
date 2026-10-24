# QStacked — falsification of sealed C2 case `CaseStacked`

**Seat:** `MadoR22-2.QStacked` (leaf member; no subagent dispatch)
**Scope:** exactly one fixture-mode execution of the sealed case `CaseStacked`; real mode never invoked.
**Verdict:** **MATCH** — the sealed expectation is reproduced exactly (exit, finding_id, and the ordered six-field tuple).

---

## 1. Provenance (byte identities)

| Artifact | Path | SHA-256 |
|---|---|---|
| Tool (candidate executable) | `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py` | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` |
| Tool git blob at pin `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` | — | `439ff4c1a68fc4f98182c6b855b3b4c790286851` (identical to working copy) |
| Sealed case file | `.ufo/waves/round-23/frozen/quota-cases/CaseStacked.json` | `b45f3485c170a88f75abcf8746315caf031331c4cf92b4943847f7433bf980d0` |
| Case git blob at pin `f3dc07c0…` | — | `f790b6c09816bdfa1b7ce712d4b7bacdd7b2397c` (identical to working copy) |
| Executed fixture (`case["fixture"]`, verbatim) | `/fast/scratch/hyaku/mori-r23/QStacked/fixture.json` | `4dc3579d0b1543dbe4dfd28f9eeacdc8b37eaaf2ee5d5e024db28898f4ef8947` |
| stdout | `/fast/scratch/hyaku/mori-r23/QStacked/stdout.txt` | `9195b65c0b5e3c2f97f45e10c4fd10ce3d812bb48594d7600eaca16b2cfc5ed8` |
| stderr | `/fast/scratch/hyaku/mori-r23/QStacked/stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty) |

Pinned production is `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` (an ancestor of lane HEAD `6eb889c0…`); the tool blob is byte-identical at both revisions, and the frozen case file is byte-identical to its pinned-commit blob. **No case, expectation, oracle or tool byte was edited.** The expectation was read only.

## 2. Source derivation actually used

* `preseal-amendment.md:50-54` — mount resolution: longest component-prefix selection remains, **but if ANY covering mountpoint occurs more than once, refuse classification** as `unknown` / `n/a` / `ambiguous_overmount`, `fstype=null`, `mount_point=null`, `device_check=not_checked`; the stack order must not be guessed from line order or reusable mount IDs.
* `preseal-amendment.md` (final pre-seal clarifications) — the extra parent-ID refusal; and `quota_option_keys=[]` / `btrfs_qgroups_mode=null` on a no-cover/ambiguous/mismatch-preempted row.
* `contract.md:120-134` — verdict precedence: no setup error, no enabled path, one unknown path ⇒ exit 2 `QUOTA_STATE_UNKNOWN`.
* Selected implementation: `tools/mori-quota-surface.py` — `resolve_mount()` (duplicate-covering-mountpoint refusal at lines 439-440, parent-ID refusal at 443-461), `evaluate()` (513-559), `classify()` (487-511), `load_fixture()` (695-772), `verdict()` (561-568), `main()` (1894-1920).

Fixture shape: five mountinfo lines; two of them carry mount point `/data` — mount ID 31 (xfs, super options `rw,inode64,logbufs=8,logbsize=256k,noquota`, device `259:2`, parent 23) and mount ID 44 (tmpfs, super options `rw,size=4194304k,inode64,usrquota`, device `0:58`, parent 31). Requested path `/data` (realpath `/data`, `st_dev 0:58`). Covering mountpoints are `/` (ext4, ID 23) and `/data` **twice** ⇒ the duplicate refusal applies; no super options of either `/data` line may be parsed for this path.

## 3. The one execution

Fixture mode only (`--fixture`); no `--path`, no `--selftest`, no real mode.

```
argv: /usr/bin/prlimit --as=402653184 /usr/bin/timeout -s KILL 15 \
      /usr/bin/python3 -I \
      /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py \
      --fixture /fast/scratch/hyaku/mori-r23/QStacked/fixture.json
env:  TMPDIR=/fast/scratch/hyaku/mori-r23/QStacked
cwd:  /fast/scratch/hyaku/mori-r23/QStacked
```

* **exit status: 2**
* **stderr: empty**
* **stdout (verbatim):**

```json
{"df_covers_quota":false,"exit_code":2,"finding_id":"QUOTA_STATE_UNKNOWN","limits":"no per-user, per-group or per-project limit or usage is read. no NFS or server-side quota and no overlay or fuse quota is covered. a visible btrfs qgroups directory does not imply that any limit is set. an ext2/ext3/ext4 quota feature in the superblock is unobservable without privileged tools. sysfs and mountinfo races during quota enable, disable or remount are not excluded. df capacity percentages never cover quota exhaustion (FR2 / EDQUOT). QUOTA_DISABLED is not a capacity or health verdict; ENOSPC can coexist. the btrfs qgroups mode attribute is never read, so btrfs_qgroups_mode is null in real mode.","paths":[{"basis":"ambiguous_overmount","btrfs_qgroups_mode":null,"device_check":"not_checked","enforcement":"n/a","fstype":null,"mount_point":null,"path":"/data","quota_option_keys":[],"quota_state":"unknown"}],"schema":"mori-quota-surface-v1"}
```

Limits applied: address space 384 MiB (`--as=402653184`), timeout 15 s with KILL, one child at a time, Python isolated (`-I`). No build, test, linter or formatter was run. Scratch lives only under `/fast/scratch/hyaku/mori-r23/QStacked/` (no `/tmp`).

## 4. Comparison — primary six-field tuple (ordered)

| # | field | expected | actual | match |
|---|---|---|---|---|
| 0 | `path` | `/data` | `/data` | ✅ |
| 0 | `fstype` | `null` | `null` | ✅ |
| 0 | `mount_point` | `null` | `null` | ✅ |
| 0 | `quota_state` | `unknown` | `unknown` | ✅ |
| 0 | `enforcement` | `n/a` | `n/a` | ✅ |
| 0 | `basis` | `ambiguous_overmount` | `ambiguous_overmount` | ✅ |

* `exit`: expected 2 — actual **2** ✅
* `finding_id`: expected `QUOTA_STATE_UNKNOWN` — actual **`QUOTA_STATE_UNKNOWN`** ✅
* path count: expected 1 — actual 1 ✅
* primary tuple match: **true**; field mismatches: **{}**

**Supplementary metadata (scored separately, never folded into the primary denominator):** `device_check=not_checked`, `quota_option_keys=[]`, `btrfs_qgroups_mode=null` — consistent with the sealed rationale's supplementary expectations and with the amendment's "preempted row carries no option keys and no mode".

## 5. Falsification analysis — is the match load-bearing?

The match is not an artifact of a coincidental code path; the case discriminates three distinct rules.

1. **Against the original contract (last-line-wins stack resolution).** [INFERENCE from source reading; not executed — the seat is limited to one fixture-mode invocation of this sealed case.] Line order would select the tmpfs line (ID 44, device `0:58` ⇒ device_check `match`, super options carry `usrquota` ⇒ `enabled`/`enforced`/`tmpfs_quota_option`), producing exit 1 `QUOTA_ENABLED` — exactly the withdrawn pre-amendment expectation preserved in `.ufo/waves/round-23/cases-proposed/CaseStacked.json` (`exit 1`, `QUOTA_ENABLED`, `tmpfs_quota_option`). The observed exit 2 / `QUOTA_STATE_UNKNOWN` therefore proves the **amendment** rule, not the pre-amendment rule, governs this path.
2. **Against a missing duplicate refusal.** [INFERENCE from source reading.] Without the duplicate check, `resolve_mount`'s equal-length tie-break keeps the *earlier* `/data` line (xfs, `259:2`), whose device differs from the fixture `st_dev 0:58` ⇒ `device_mismatch`, i.e. the same exit and finding_id but a **different basis**. The six-field tuple still separates the two, so the case pins the refusal mechanism, not merely the verdict.
3. **Rule independence.** The amendment's extra parent-ID refusal (preseal-amendment.md, final pre-seal clarifications) would independently refuse the *tmpfs* choice (parent 31 known in the snapshot and ≠ the longest strictly shorter cover `/` ID 23) but would **not** refuse the *earlier xfs* choice (parent 23 == ancestor ID 23). Therefore the duplicate-covering-mountpoint rule is the load-bearing rule here; the two rules are complementary, not redundant.
4. **No special-casing.** The tool source contains no case id, no fixture literal and no `/data` string; the refusal is produced by the generic `len(points) != len(covered)` test over covering mounts (`tools/mori-quota-surface.py:439-440`).
5. **No host reads in fixture mode.** `probe_fixture` → `load_fixture` opens only the fixture file (`:697`); the `/proc/self/mountinfo` open (`:660`) and the sysfs reads (`:633`) are reachable only from `real_inputs`, which fixture mode never calls. No quota interface (`quotactl`, `btrfs qgroup`, `xfs_quota`, `repquota`, mount) was touched by this execution.
6. **No leakage.** The stdout row carries no mount source, no option value, no UUID, and no decoy btrfs record content; the refused row's `quota_option_keys` is empty, so neither `usrquota` nor `noquota` is echoed.
7. **Determinism.** The same fixture was executed twice under the same limits (canonical argv as recorded above; a first run with `timeout -k 2 15 prlimit --as=… --cpu=15 --nofile=256` produced byte-identical stdout and stderr). Both runs: exit 2, identical digests.

## 6. Findings

* **No defect found in the observed behaviour of `CaseStacked`.** The sealed expectation is reproduced exactly; primary six-field tuple, exit code and finding_id all match, and the supplementary metadata is consistent and separately reported.
* The case is discriminating (see §5.1-§5.3): it would fail against the pre-amendment stack-order rule and against a missing duplicate refusal. It is not a vacuous green.

## 7. Residual risk and verification gaps (explicit, not excusing anything)

* **[GAP]** The counterfactual arms in §5.1-§5.3 were **not executed**; they are source-level readings of `resolve_mount`/`evaluate`. This seat's authorization covers one fixture-mode invocation of this sealed case, so no mutated-tool arm was run. The empirical discrimination therefore rests on the observed match plus a static trace, not on an executed negative control.
* **[RISK]** `CaseEscapedSpace` was **not** executed by this seat (it is owned by seat `QEscapedSpace`); the frozen strict-red contradiction is neither excused nor re-litigated here. This seat's result is from a separate fixture, a separate invocation and a separate scratch tree with no shared state, so it neither supports nor clears that red.
* **[RISK]** Fixture mode exercises only the synthetic path. Real-mode behaviour (btrfs `qgroups/enabled` reading, `realpath`/`stat` inputs) remains unverified by this seat and by this case; the frozen default real control is a separate arm.
* **[OPEN DEBT, unchanged]** Four unallowlisted inherited hits (raw 95 / allowlisted 86 / non-author 5), original permission control RED 11/12, two unknown dispositions, baseline acceptance blocked, `privacy_clearance=false`. Nothing in this falsification changes those. Probe visibility/accounting consistency is not clearance, health or admission.

## 8. Tooling / installs

No packages were installed, updated or upgraded by this seat (no `pacman`, `uv`, `cargo` or `npm` transaction). Only `python3`, `prlimit` and `timeout` from the base system were used; all three are stock Arch packages and were already present.

## 9. Receipt

`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/QStacked/scan.json` (schema `mori-r23-falsification-receipt-v1`; fields: `argv`, `exit_code`, `stdout`/`stdout_sha256`, `stderr`/`stderr_sha256`, `given`, `actual`, `comparison`, `verdict`, `tool_sha256`, `tool_git_blob_at_pin_f3dc07c`, `case_sha256`, `fixture_sha256`, `determinism`, `falsification_notes`, `prohibitions_observed`).

Report: .ufo/waves/round-23/falsify/QStacked.md
