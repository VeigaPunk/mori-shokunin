# Falsification report — seat QXfsAccountingOnly (mori round 23, C2)

Scope: falsify the **sealed C2 case `CaseXfsAccountingOnly.json`** against the pinned production
quota probe, in **fixture mode only**. One case, one tool, one lane report.
No production, frozen-case or oracle byte was edited.

- Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`
- Seat scratch (sole scratch root): `/fast/scratch/hyaku/mori-r23/QXfsAccountingOnly/`
- Receipt: `.ufo/waves/round-23/falsify/QXfsAccountingOnly/scan.json`
  (sha256 `7e6e32bf055c023efc71d598ff3706024af2b249ff5770723631cc24e3c526bf`, 8990 bytes)
- Production pin: `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c`
- Expectation seal: `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687`

## 1. Bytes under test (measured)

| Artifact | Path | sha256 | Bytes |
|---|---|---|---|
| Sealed case | `.ufo/waves/round-23/frozen/quota-cases/CaseXfsAccountingOnly.json` | `e03c414b1625518c5bb88171e53e5584c72ea1d5f7e54e2bed5873600f3ba135` | 8035 |
| Candidate executable | `tools/mori-quota-surface.py` | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` | 66644 |
| Sealed oracle (semantics reused, not executed as a suite) | `.ufo/waves/round-23/oracle-quota.py` | `f1f4a027728180436fc5161171b0f6ad4ca4176229b5240aabb33e3f2af36bec` | 25391 |
| My fixture copy | `…/mori-r23/QXfsAccountingOnly/fixture.json` | `0df50da4e22ff5df6dba7de7b151d19044bb319a04532be2fea23be72449737a` | 964 |

- The case hash equals the `frozen/seal-manifest.json` entry for that path
  (`sha256 e03c414b…, bytes 8035`) → the bytes tested are the **sealed** bytes.
- `git show f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c:tools/mori-quota-surface.py` hashes identically
  to the working-tree file → the candidate executed is the **pinned production** bytes, not a local edit.
- `json.load(my fixture.json) == case["fixture"]` → True (semantic copy only; the sealed case file is untouched).

## 2. Axes (named before measuring)

- **A1 byte identity** — sealed case bytes, pinned production tool bytes, oracle bytes.
- **A2 execution bound** — fixture-only, one child at a time, 384 MiB AS, 15 s timeout, argv preserved.
- **A3 primary verdict** — exit code, `finding_id`, and the **ordered six-field tuples**
  `(path, fstype, mount_point, quota_state, enforcement, basis)`.
- **A4 primary/supplementary separation** — the six-field denominator is scored alone; `device_check`,
  `quota_option_keys`, `btrfs_qgroups_mode` are reported **separately** and never widen the denominator.
- **A5 output minimisation** — no mount source, no option value, no UUID, no path outside the fixture.
- **A6 host-read containment** — fixture mode must not consult host mount/sysfs state.
- **A7 claim honesty** — this seat's result must not be presented as wave-level C2 admission, and must not
  excuse the expected strict red elsewhere.

## 3. Method (exact invocation)

```
cp case["fixture"] -> /fast/scratch/hyaku/mori-r23/QXfsAccountingOnly/fixture.json
timeout 15 prlimit --as=402653184 -- python3 -I \
  /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py \
  --fixture /fast/scratch/hyaku/mori-r23/QXfsAccountingOnly/fixture.json
```

`argv` as executed: `python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py --fixture /fast/scratch/hyaku/mori-r23/QXfsAccountingOnly/fixture.json`.
Real mode (`--path`, default fleet root + `/tmp`) was **never** invoked; no host quota interface
(quotactl/ioctl, `btrfs qgroup`, `xfs_quota`, `repquota`, mount) was touched; no qgroup/mode was read.

Comparison used the **sealed oracle's own per-case functions** (`evaluate_case`, `supplementary_checks`,
`leakage_hits`) applied to the captured stdout. The oracle `main()` was **not** run, so no other case
and no real control was executed by this seat.

## 4. Observations (measured)

Execution: exit **1**, stderr empty (0 bytes), stdout 990 bytes,
stdout sha256 `a612fc63e644364fa01762b4910be3cee38c1fa0513fcedba82fa9a47406b28c`, elapsed 0.070 s
(well inside the 384 MiB / 15 s bound; no timeout, no AS failure).

Observed JSON (verbatim, one line, sorted keys):

```json
{"df_covers_quota":false,"exit_code":1,"finding_id":"QUOTA_ENABLED","limits":"…","paths":[{"basis":"xfs_quota_option","btrfs_qgroups_mode":null,"device_check":"match","enforcement":"accounting_only","fstype":"xfs","mount_point":"/srv/xfsacct","path":"/srv/xfsacct/data","quota_option_keys":["pqnoenforce","uqnoenforce"],"quota_state":"enabled"}],"schema":"mori-quota-surface-v1"}
```

Primary comparison (ordered six-field tuples):

| | expected (sealed case) | observed | match |
|---|---|---|---|
| exit | 1 | 1 | yes |
| finding_id | `QUOTA_ENABLED` | `QUOTA_ENABLED` | yes |
| tuple 1 | `("/srv/xfsacct/data","xfs","/srv/xfsacct","enabled","accounting_only","xfs_quota_option")` | identical | yes |

`evaluate_case()` → `primary_ok: True`, `headline {exit_match: true, finding_match: true, paths_match: true}`,
`reason: None`.

Supplementary metadata — **observed only, not scored**: the sealed case carries **no**
`supplementary_expected` block (case keys: `expected, fixture, id, rationale, scenario, schema, sources`),
so nothing supplementary is asserted against expectation. Observed: `device_check="match"`,
`quota_option_keys=["pqnoenforce","uqnoenforce"]`, `btrfs_qgroups_mode=null`. The oracle's *generic*
supplementary checks that do not need a sealed expectation all pass (10/10, 0 unmet): schema,
exit consistency, allowed/exact output key set, error token, path key set, `df_covers_quota:false`,
limits text, **no_leakage** (canary hit list empty: no mount source, no UUID, no option value echoed).

Static re-derivation of the same row (independent of the tool, from the sealed rationale + the amendment):
mount points `/`, `/home`, `/run`, `/tmp`, `/srv/xfsacct` each occur once → no `ambiguous_overmount`;
longest cover of `/srv/xfsacct/data` is `/srv/xfsacct` (mount 251, parent 33) and the longest strictly
shorter cover is `/` (mount 33) → parent 33 == ancestor 33 → no parent refusal; fstype `xfs`,
`259:3` == path `st_dev 259:3` → `device_check match` (no preemption); super-option keys
`rw, inode64, logbufs, logbsize, uqnoenforce, pqnoenforce` → no `noquota`, no enforced key, one
accounting-only key → `enabled / accounting_only / xfs_quota_option`; single enabled row → exit 1
`QUOTA_ENABLED`. The observed row is exactly this.

Host-read containment (static, source-level): `probe_fixture()` → `load_fixture()` opens exactly one
file (the fixture, line 697). `/proc/self/mountinfo` (line 660), `os.stat` of probed paths (line 668)
and `/sys/fs/btrfs` reads (`scan_btrfs_sysfs`, lines 571–633) are reachable only from
`probe_real()`/`real_inputs()`. The fixture's decoy btrfs/tmpfs lines therefore exercise mount
resolution only, as claimed.

## 5. Findings by severity

**Blocking / major / minor: none for this case.** The sealed C2 case `CaseXfsAccountingOnly` is
reproduced exactly by the pinned production tool: exit, `finding_id` and the ordered six-field tuple
all match the sealed expectation; no expected byte was edited; no leakage; no host read.

Low-severity observations (recorded, not acted on — they concern the sealed artefacts, not this seat):

1. *Supplementary metadata is unscored for this case.* The sealed case has no `supplementary_expected`,
   so `device_check`, `quota_option_keys` and `btrfs_qgroups_mode` are asserted by nothing. Their
   observed values are consistent with the re-derivation, but that consistency is my own check, not a
   sealed requirement. The primary denominator (27 original-derived cases) stays untouched.
2. *The `xfs_quota_option` basis token is shared* by the enforced and the accounting-only xfs rows;
   only the `enforcement` field separates them. A wrong `enforcement` value would still be caught, but
   the basis token alone is not discriminating — relevant to any future variant of this case.
3. *The accounting-only path depends on the exact `XFS_NOENFORCE_KEYS` spelling set*
   (`uqnoenforce,gqnoenforce,pqnoenforce,qnoenforce`). This fixture exercises two of the four
   (`uqnoenforce`, `pqnoenforce`); `gqnoenforce`/`qnoenforce` are not exercised by this case.
4. *Stale self-description of the shipped production file (provenance, low).*
   `tools/mori-quota-surface.py` (production, `e4857413…`) opens with the docstring of the **v3
   candidate**: `"""mori-quota-surface-v3.py — …"""`, "This is the round-23 pre-seal amendment
   candidate", "authored alongside `mori-quota-surface.py` (the original, unaltered) and
   `mori-quota-surface-v2.py`". In the production tree this is factually stale on two counts: the
   shipped file *is* `mori-quota-surface.py` (so "the original, unaltered" is a different file, the
   v1 preserved at `build/ImplQuota/mori-quota-surface.py`, `6b553154…`), and production is **not
   byte-equal** to the preserved v3 candidate `build/ImplQuota/mori-quota-surface-v3.py`
   (`5199e97b…`) — the delta is 4 change groups / 31 diff lines: the `classify()` result unpack
   (`(state, enforcement, basis), mode`), stricter fixture path validation (`paths` must be
   non-empty; a path entry must have exactly `path/realpath/st_dev`), `limits` emitted as one joined
   string instead of a list, and two added selftest arms (`setup-empty-path-population`,
   `setup-extra-path-record-key`). None of these four changes is mentioned in the shipped file's own
   docstring, so a reviewer diffing production against the preserved candidate sees an undocumented
   delta. **No effect on this case** (all four changes are upstream of the classifier table and the
   fixture-path shape my case uses), but it weakens the "same-identity rerouting" audit trail from
   the sealed candidate to production. Not acted on: the file is production, outside this seat's
   write scope.
5. *Canonical runtime is unambiguous (verified, no finding).* The measure driver pins
   `QUOTA_REL = 'tools/mori-quota-surface.py'` and the oracle takes `--tool`; the only other copies
   are preserved evidence under `.ufo/waves/round-23/build/ImplQuota/` and a stale `tools/__pycache__/`
   entry. There is exactly one runtime path for the frozen cases, so the bytes I executed are the
   bytes the wave measures.

## 6. Residual risk and verification gaps

- **Wave-level C2 remains UNPROVABLE at 29/30.** The strict red is `CaseEscapedSpace`
  (`evidence/frozen-contradiction.json`: selected mount 43 vs shorter cover 42 ⇒ the sealed rule
  demands `unknown / ambiguous_overmount`, the frozen expectation demands an enabled row). That case
  is **not** mine; this seat neither excuses it nor re-runs it. My pass is one of the 29, and it
  changes nothing about the strict target.
- **The quota selftest arm is a different arm.** `evidence/quota-selftest-corrected.json` (49/49) is the
  co-evolved selftest fixture input; `--selftest` was **not** executed by this seat (reading a selftest
  is not permission to run it) and is not used as evidence here. It is likewise not evidence for the
  frozen `CaseXfsAccountingOnly`.
- **"No host read in fixture mode" is a source-code argument, not a syscall trace.** No `strace` run was
  authorised for this seat; a traced execution would upgrade this from static to observed evidence.
- **Fixture-mode determinism was checked across two hashed runs only** (identical stdout sha256); the
  two earlier executions of the same case produced the same 990-byte stdout but were overwritten before
  hashing (disclosure below).
- **The frozen expectation is itself contested in this wave** for a sibling case; if the L1 team
  re-seals any C2 case bytes, the hash anchor in this receipt must be re-checked before reuse.

## 7. Disclosures / deviations

- **Executions: four** sequential single-child executions of the *same* fixture-mode case (one at a
  time, never concurrent). The first attempt used `/usr/bin/time`, which is **not installed** on this
  host (`/usr/bin/time` → command not found, exit 127) and therefore executed nothing. The bash tool
  runs commands under `set -e`, so the first two runs aborted the surrounding script at the tool's
  exit 1 (the tool's own verdict) — the run itself succeeded and wrote its output; the wrapper then
  reported "exit code 1". The last two runs captured the exit code explicitly (`|| rc=$?`) and wrote
  `run-meta.txt` (argv, exit 1, timeout 15, `--as=402653184`, elapsed 0.070 s).
- **No tool was installed or updated** by this seat (no pacman/uv/npm/cargo transaction; the tooling
  directive had nothing to do here — `prlimit`, `timeout`, `python3` 3.14.8 were already present).
- **One scratch artefact cleaned up:** importing the sealed oracle to reuse its per-case functions
  created `.ufo/waves/round-23/__pycache__/oracle-quota.cpython-314.pyc`; I removed that directory
  immediately, restoring the lane to its entry state. The pre-existing
  `.ufo/waves/round-22/frozen/__pycache__/` and `tools/__pycache__/` were left untouched.
- **No writes** outside my two assigned lane paths (this report and my `scan.json` receipt) and my seat
  scratch directory. No production, frozen-case, oracle, driver, ledger or index file was touched; no
  `git add/commit/push`, no mutating `jj`, no `agent://all` broadcast.

## 8. Verdict

`CaseXfsAccountingOnly` — **PASS**. Pinned production tool `e4857413…` reproduces the sealed
expectation exactly (exit 1, `QUOTA_ENABLED`, one ordered six-field tuple
`/srv/xfsacct/data · xfs · /srv/xfsacct · enabled · accounting_only · xfs_quota_option`) under the
sealed oracle's own per-case semantics, in fixture mode, within the 384 MiB / 15 s bound, with
byte-identical stdout across executions, no leakage and no host read. This is a per-case result only;
it neither admits C2 nor disturbs the expected strict red in `CaseEscapedSpace`.
