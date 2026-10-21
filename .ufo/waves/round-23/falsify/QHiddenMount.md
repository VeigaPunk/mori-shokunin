# QHiddenMount — falsification of sealed C2 case `SupplementHiddenMount`

Seat: `MadoR22-2.QHiddenMount` (read-only falsifier, wave 23, lane `mori-shokunin`).
Scope: the single sealed C2 fixture-mode case `SupplementHiddenMount.json` and nothing else.
Receipt: `.ufo/waves/round-23/falsify/QHiddenMount/scan.json` (sha256 `f0b5f9a05ea7cfaafa78588f9fe35a55978032d56b26f413ade9627a329eca7f`).
Scratch: `/fast/scratch/hyaku/mori-r23/QHiddenMount/` (fixture.json, stdout.txt, stderr.txt).

**Verdict: MATCH.** The production tool at pinned revision `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c`
reproduces the sealed expectation of this case exactly — exit, `finding_id` and the ordered
six-field tuple — and every sealed supplementary check the oracle applies to this case passes.
No expected byte was edited; no defect found in this case's rule path.

---

## 1. Inputs read (no writes outside the seat report/receipt/scratch)

| Artifact | Path | sha256 |
|---|---|---|
| Sealed case | `.ufo/waves/round-23/frozen/quota-cases/SupplementHiddenMount.json` | `d1a3a4c66008fcdefec47839d9393f1c971ebc6630d96b94c399038378187824` |
| Same bytes, author lane | `.ufo/waves/round-23/cases-supplemental/SupplementHiddenMount.json` | identical (`d1a3a4c6…`) |
| Case blob at seal `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687` | `git show 22772c1:…/SupplementHiddenMount.json` | identical (`d1a3a4c6…`) |
| Case blob at production `f3dc07c0…` | `git show f3dc07c0:…/SupplementHiddenMount.json` | identical (`d1a3a4c6…`) |
| Production tool | `tools/mori-quota-surface.py` | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` (blob at `f3dc07c0` identical) |
| Sealed oracle | `.ufo/waves/round-23/oracle-quota.py` | `f1f4a027728180436fc5161171b0f6ad4ca4176229b5240aabb33e3f2af36bec` |
| Seal manifest entry | `.ufo/waves/round-23/frozen/seal-manifest.json:198-202` | `d1a3a4c6…`, 7496 bytes |
| Case decision | `.ufo/waves/round-23/frozen/case-decisions.json:249-256` | `primary: false` — discovery guard, counted in the supplemental population |

Ancestry: `git merge-base --is-ancestor 22772c10f6e3c1d8d3fe1b72083a6194e9f4e687 f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` → true.
The quota production path is absent at the seal commit (`git show 22772c1:tools/mori-quota-surface.py` → no such path), so the expectation was sealed before the implementation existed.

Derivation/amendment read for this case: `contract.md` (C2 mount-resolution and verdict clauses),
`preseal-amendment.md` (C2 final rules, final pre-seal clarifications, real-mode safety correction),
and the case's own `rationale` (parent-ID clause derivation from the `CriticContractC2` D2 shape, kernel
sources S079/S080/S082/S084). The selected quota implementation read: `tools/mori-quota-surface.py`
(`parse_mountinfo` :311-353, `covering_mounts` :407-419, `resolve_mount` :421-462, `classify` :498-511,
`evaluate` :513-560, `load_fixture` :695-772, `payload` :774-795).

## 2. The one execution performed

Fixture-mode only. Real mode was never invoked; no other case was invoked; one child process total.

```
TMPDIR=/fast/scratch/hyaku/mori-r23/QHiddenMount/ \
  timeout -k 2 15 prlimit --as=402653184 --cpu=15 \
  python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py \
    --fixture /fast/scratch/hyaku/mori-r23/QHiddenMount/fixture.json
```

- `fixture.json` is `case["fixture"]` copied into the seat scratch with the oracle's own staging
  serialization (`json.dumps(fixture, indent=2, sort_keys=True) + "\n"`,
  `oracle-quota.py:450-456`): sha256 `a79ba4122e07004478a3c4bff42ec235717656584caab812a6c341e5332bd97f`,
  1047 bytes — byte-identical to the fixture the sealed measure driver staged
  (`evidence/measure4/c2-after-observed.json`, `fixture_sha256 a79ba41…`).
- Python 3.14.8, cwd and `TMPDIR` inside the seat scratch, address-space cap 384 MiB, 15 s wall/CPU cap.
- argv recorded verbatim in the receipt; stdout 949 bytes sha256 `017debcdcc42f969c7f295541d95124b58ee8038dfd48a23959961786c091133`; stderr 0 bytes.

## 3. Given vs actual

| Field | Given (sealed expectation) | Actual (measured) | Match |
|---|---|---|---|
| exit | 2 | 2 | yes |
| `finding_id` | `QUOTA_STATE_UNKNOWN` | `QUOTA_STATE_UNKNOWN` | yes |
| `path` | `/home/x/y/z` | `/home/x/y/z` | yes |
| `fstype` | `null` | `null` | yes |
| `mount_point` | `null` | `null` | yes |
| `quota_state` | `unknown` | `unknown` | yes |
| `enforcement` | `n/a` | `n/a` | yes |
| `basis` | `ambiguous_overmount` | `ambiguous_overmount` | yes |
| stderr | (empty) | empty | yes |

Ordered six-field tuple (path, fstype, mount_point, quota_state, enforcement, basis):

- expected: `('/home/x/y/z', None, None, 'unknown', 'n/a', 'ambiguous_overmount')`
- observed: `('/home/x/y/z', None, None, 'unknown', 'n/a', 'ambiguous_overmount')`

Evaluation used the sealed oracle's own `evaluate_case` (`oracle-quota.py:300-347`) applied to the
measured stdout and exit: `ok=True`, headline `exit_match/finding_match/paths_match` all true, no reason.
The case file carries **no** `supplementary_expected` key, so it contributes zero scored supplementary
metadata rows; the generic sealed supplementary checks that apply to it are 9/9 pass:
`schema`, `exit_consistency`, `output_keys_allowed`, `output_key_set`, `error_token`, `path_key_set`,
`df_covers_quota`, `limits_text`, `no_leakage` (canary scan over the fixture's UUIDs, mount sources,
`key=value` option tokens and distinctive device basenames → no hits).

## 4. Primary vs supplementary separation

- **Primary (scored six-field denominator):** exit + `finding_id` + ordered six-field tuples. This case
  contributes exactly one case row. It is a **supplemental discovery case**
  (`frozen/case-decisions.json`: `"primary": false`, "Source-review discovery guard before candidate
  inspection/result"), so it is counted in the 3-case discovery population, never inside the
  27 original-derived primary denominator. It does not widen or redefine that denominator.
- **Supplementary (reported apart, never folded in):** observed per-row metadata is
  `device_check="not_checked"`, `quota_option_keys=[]`, `btrfs_qgroups_mode=null` — exactly the
  amendment's requirement for a preempted row (`preseal-amendment.md:123-124`). The case file does not
  assert these, so they are reported here as separate, unsealed-against metadata that nonetheless
  matches the amendment.

## 5. Which rule actually fired (rule attribution, independently traced)

The fixture's four mountinfo lines: id 1 `/` (btrfs, parent 1), id 65 `/home` (btrfs, parent 1),
id 70 `/home/x/y` (btrfs, parent 65), id 80 `/home/x` (tmpfs with `usrquota`, parent 65).
Path `/home/x/y/z`, realpath identical, `st_dev 0:46`.

- Covering mounts for the resolved path: `/` (1), `/home` (65), `/home/x` (80), `/home/x/y` (70) — all
  four mount points are distinct, so the **duplicate-covering-mountpoint refusal does not apply**; the
  case genuinely isolates the parent-ID clause.
- Longest cover → id 70 at `/home/x/y`; strictly shorter covers → `/` (1), `/home` (65), `/home/x` (80);
  longest strictly shorter → id 80 at `/home/x`.
- Chosen mount's printed parent id = 65, which **is present** in the snapshot (so it is not "unknown
  topology") and **is not** the id of the longest strictly-shorter cover (80). The parent-ID consistency
  refusal therefore fires: `unknown / n/a / ambiguous_overmount`, `fstype=null`, `mount_point=null`,
  `device_check=not_checked`. The chosen mount is not the root, so the "root has no shorter cover"
  escape does not apply.
- Classification is never reached: the filesystem table, the btrfs `qgroups_enabled` rows and the
  device check are all bypassed; the fixture's `usrquota` tmpfs line and both btrfs UUIDs are inert.
  The tool does **not** use the path's `st_dev` equality (which happens to equal the tmpfs line's
  `0:46`) to infer stack order — resolution precedes the device check and the row is refused.
- Verdict precedence (contract.md:132-134): no setup error, no `enabled` path, one `unknown` path →
  exit 2 `QUOTA_STATE_UNKNOWN`. Matches.
- Implementation correspondence: `resolve_mount` (`tools/mori-quota-surface.py:421-462`) implements the
  amendment clause exactly as written — duplicate mount point → refuse; else longest cover; else if the
  chosen mount's parent id is in the snapshot and differs from the longest strictly-shorter cover's id
  → refuse. The two escape hatches (parent id absent; chosen mount is the root) are implemented as
  "no refusal" and are inapplicable here.

The tool's own `--selftest` (49 arms, `evidence/quota-selftest-corrected.json`) carries separate arms
`parent-id-refusal` (`:1402`) and `parent-id-consistent` (`:1430`) (`tools/mori-quota-surface.py:1402-1460`). The sealed
case exercises a *different and stronger* shape than the selftest arm: there the parent id 25 points at
a mount (`/other`) that is not an ancestor of the probed path at all, whereas here the parent id 65 is a
real covering ancestor (`/home`) that is merely not the longest shorter cover (a newer tmpfs mounted on
a plain ancestor directory hides the older nested btrfs mount). The case therefore adds coverage the
tool's selftest does not have, rather than duplicating it.

## 6. Leakage and scope checks

- Output carries exactly `{schema, finding_id, exit_code, paths, df_covers_quota, limits}`; the single
  path row carries exactly the nine documented keys.
- No mount source, no option value, no UUID, no option key (`usrquota`, `noquota`…), no device basename
  (`sdb`, `dm-0`) and no `st_dev` appears in the stdout. The only occurrence of the string `btrfs` is
  inside the fixed `limits` boundary text, not fixture-derived.
- `df_covers_quota=false`; `limits` non-empty. `error` token absent (not a setup error).

## 7. Findings, residual risk, verification gaps

**Findings against this case: none.** The sealed expectation, the amendment's clause, and the
production implementation agree; no defect, no leak, no off-contract output was observed in this case's
path.

Residual risk and limits of this falsification (not defects, not admissions):

1. **Conservatism costs coverage.** A path under a plain ancestor directory that later received its own
   mount is always reported `unknown/ambiguous_overmount`, even when the kernel's live device for that
   path is unambiguous. The probe will not report a visible `usrquota` tmpfs at `/home/x` for
   `/home/x/y/z` in this topology. This is the sealed rule's intent, but it means "unknown" here is a
   deliberate non-observation, not an absence of quota configuration.
2. **The refusal is a source-derived consistency check, not topology proof.** The parent-id field is
   printed by the kernel and is not a stack-order oracle; the rule refuses rather than guesses. The
   implementation's `known` set contains every mount id in the snapshot, so an id reused across the
   snapshot (not possible in a kernel mount table) would weaken the check — out of scope for real
   mountinfo.
3. **Fixture-mode only.** Real mode was not exercised here (per seat scope), so the real-mode
   equivalence of the refusal path is unverified in this receipt; the real-mode path shares
   `resolve_mount`, but the real readset differences (no `qgroups/mode` read) are outside this case.
4. **Single-sample, deterministic tool.** The tool is deterministic and the case is a single fixture;
   no statistical claim is made. No mutation/arm was run in this seat, so the falsification here is
   "expected vs actual on the sealed bytes", not "the rule is unreachable by accident" — though the
   independent trace in §5 shows which clause fires and that the duplicate-mountpoint rule cannot be
   responsible for this row.

**CaseEscapedSpace (not my seat, not excused).** I did not execute `CaseEscapedSpace`; my seat executed
exactly one case. To be explicit and not to excuse it: the frozen contradiction recorded at
`.ufo/waves/round-23/evidence/frozen-contradiction.json` stands unchanged — the sealed expectation for
`CaseEscapedSpace` is exit 1 `QUOTA_ENABLED` with the selected mount id 43 / parent id 33 and a
longest strictly-shorter cover of id 42 at `/srv`, while the rule as sealed requires
`unknown/n/a/ambiguous_overmount` and the tool produces exit 2 `QUOTA_STATE_UNKNOWN`. That is a
**mismatch, reported as a mismatch**: the frozen bytes stay unchanged, no special case, exclusion,
relabel or rewrite is proposed, and the strict C2 coverage target therefore remains **UNPROVABLE at
29/30**. This seat's passing case does not narrow, excuse or offset that red. The quota selftest arm
(49/49 in `evidence/quota-selftest-corrected.json`) is a separate, co-evolved fixture arm and is not
this case.

## 8. Reproduction (exact)

```bash
mkdir -p /fast/scratch/hyaku/mori-r23/QHiddenMount
cd /fast/scratch/hyaku/mori-r23/QHiddenMount
python3 - <<'PY'
import json
case = json.load(open("/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/frozen/quota-cases/SupplementHiddenMount.json"))
open("fixture.json","w").write(json.dumps(case["fixture"], indent=2, sort_keys=True) + "\n")
PY
TMPDIR=$PWD/ timeout -k 2 15 prlimit --as=402653184 --cpu=15 \
  python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py \
    --fixture $PWD/fixture.json > stdout.txt 2> stderr.txt; echo "exit=$?"
# exit=2; stdout: one JSON object, finding_id QUOTA_STATE_UNKNOWN,
# path row ("/home/x/y/z", null, null, "unknown", "n/a", "ambiguous_overmount")
```

## 9. Tooling

No tool was installed, updated or upgraded in this seat; no pacman transaction, no service restart, no
background job, no subagent dispatch. Only `git show/log/rev-parse/status/merge-base` (read-only) was
used on the lane repository; no `git add/commit/push`, no `jj` mutation, no write to the fleet root, to
the lane's production/frozen/oracle bytes, or to any sibling path. Writes were confined to
`.ufo/waves/round-23/falsify/QHiddenMount.md`, `.ufo/waves/round-23/falsify/QHiddenMount/scan.json` and
`/fast/scratch/hyaku/mori-r23/QHiddenMount/`. No live quota/host read of any kind was performed (no
`quotactl`, `btrfs qgroup`, `xfs_quota`, `repquota`, mount, or real-mode probe).
