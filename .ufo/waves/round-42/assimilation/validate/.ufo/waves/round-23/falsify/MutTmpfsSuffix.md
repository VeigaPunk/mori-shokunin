# MutTmpfsSuffix — bogus tmpfs `_hardlimit` suffix

## Scope and axes

- Challenged axis: **C2 coverage**, specifically the negative boundary of tmpfs's recognized quota-option vocabulary. Guard axes: calibration (retain the baseline red) and integrity (exact byte restoration).
- Production/base pin: `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c`; expectation seal: `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687`.
- Actual separate, shallow, no-hardlink clone: `/fast/scratch/hyaku/mori-r23/MutTmpfsSuffix/clone`, branch `round23/MutTmpfsSuffix`. Its observed HEAD was the required production pin. No lane index, refs, production source, frozen case, expectation or oracle was edited.
- Authority: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/preseal-amendment.md:72-76` preserves only quota/usrquota/grpquota and four documented hardlimit keys; arbitrary `_hardlimit` suffixes are insufficient. Read the contract, amendment, original/corrected tmpfs case, frozen decisions and `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-23.md`. S084's retained source lists the four names; S086 emits those same four names. This probe tests the rejected broad-suffix implementation, not a contract change.

## Mutant and expected detector

One behavior-bearing line changed at line 507 of `/fast/scratch/hyaku/mori-r23/MutTmpfsSuffix/clone/tools/mori-quota-surface.py`:

```python
# Pristine/restored
        if keys & TMPFS_QUOTA_KEYS:
# Mutant
        if keys & TMPFS_QUOTA_KEYS or any(key.endswith("_hardlimit") for key in keys):
```

This is an applicable mutation: it incorrectly enables tmpfs for an unrecognized suffix key while leaving recognized options and the output-key allowlist unchanged.

Created exactly one separately labelled discovery case, `/fast/scratch/hyaku/mori-r23/MutTmpfsSuffix/DiscoveryTmpfsBogusHardlimit.json`, outside the frozen case directory. Its synthetic fixture is:

```json
{"schema":"mori-quota-fixture-v1","mountinfo":"1 0 0:52 / / rw - tmpfs tmpfs rw,bogus_hardlimit=123\n","paths":[{"path":"/r23/bogus-suffix","realpath":"/r23/bogus-suffix","st_dev":"0:52"}],"device_links":{},"btrfs_sysfs":{}}
```

Its pre-run discovery expectation was exit `0`, `QUOTA_DISABLED`, with the primary tuple `(/r23/bogus-suffix, tmpfs, /, disabled, n/a, tmpfs_quota_options_absent)`. Supplementary wants were `device_check=match`, `quota_option_keys=[]`, `btrfs_qgroups_mode=null`. These are new discovery wants only; no sealed want was changed or supplemented.

## Bounded detector actually exercised

The same `/fast/scratch/hyaku/mori-r23/MutTmpfsSuffix/detector.py` and identical argv ran on pristine, mutant and restored bytes. Each phase used one Python child, sequentially executing all 30 unchanged frozen fixtures and the one discovery fixture. Each call was the production `main(["--fixture", fixture_path])`, capturing actual stdout, stderr and returned exit. The unchanged sealed oracle's `evaluate_case` and supplementary predicates judged those outputs in-process. The oracle CLI/driver itself was **not** invoked, and nothing called real mode or selftest.

The child was launched through `/usr/bin/prlimit --as=402653184 --cpu=15 -- /usr/bin/python3 -B ...`, with a separate 15-second `subprocess.run` wall timeout. Both inherited resource limits were recorded inside the child. `TMPDIR=/fast/scratch/hyaku/mori-r23/MutTmpfsSuffix`; bytecode writes were disabled. The full absolute argv is retained in the identity receipt. Phase durations were approximately 0.055s, 0.065s and 0.065s; no timeout or child stderr occurred.

Seal-to-pin read-only Git comparison for the oracle and all 30 frozen cases returned exit 0. The detector did not modify either; its oracle SHA-256 stayed `f1f4a027728180436fc5161171b0f6ad4ca4176229b5240aabb33e3f2af36bec` in every phase.

## Actual outputs

| Population / observation | Pristine | Mutant | Restored |
|---|---:|---:|---:|
| Frozen primary original-derived cases | 26/27 | 26/27 | 26/27 |
| Frozen source-review supplemental cases | 3/3 | 3/3 | 3/3 |
| **Frozen headline, original denominator** | **29/30** | **29/30** | **29/30** |
| Frozen supplementary assertions unmet | 0 | 0 | 0 |
| Separate discovery case | 1/1 | 0/1 | 1/1 |
| Discovery supplementary assertions unmet | 0 | 0 | 0 |
| Discovery tool exit | 0 | 1 | 0 |
| Whole detector exit | 1 | 1 | 1 |

All 30 frozen case outputs, exit codes, stderr, headline comparisons and supplementary outcomes were identical across the three phases. The sole frozen unmet case remained `CaseEscapedSpace.json`, retained unchanged. Its known topology conflict was not excluded, relabelled, rewritten or special-cased: chosen43/parent33 conflicts with the shorter covering `/srv`42, so the sealed rule requires unknown while its frozen expectation wants enabled.

The discovery's actual differing fields were:

| Field | Pristine | Mutant | Restored |
|---|---|---|---|
| `finding_id` | `QUOTA_DISABLED` | `QUOTA_ENABLED` | `QUOTA_DISABLED` |
| `exit_code` | 0 | 1 | 0 |
| `quota_state` | `disabled` | `enabled` | `disabled` |
| `enforcement` | `n/a` | `enforced` | `n/a` |
| `basis` | `tmpfs_quota_options_absent` | `tmpfs_quota_option` | `tmpfs_quota_options_absent` |

In all three discovery outputs: `fstype=tmpfs`, `mount_point=/`, `device_check=match`, `quota_option_keys=[]`, `btrfs_qgroups_mode=null`, `df_covers_quota=false`, and schema `mori-quota-surface-v1`. The mutant failed all three discovery headline comparisons (`exit_match`, `finding_match`, `paths_match`); supplementary checks still passed. Full actual JSON stdout is retained for every case and phase in the bounded result receipt.

## Verdict

- **Finite frozen oracle boundary: not covered by these 30 cases.** The mutant changed the new bogus-key case but changed no frozen output or verdict. Every one of the 29 baseline-passing controls survived the mutant.
- **Frozen suite-level mutation verdict: INCONCLUSIVE**, because pristine already fails `CaseEscapedSpace`. Its pre-existing exit 1 is not a killed mutant and is not evidence of a healthy suite. Strict C2 remains **UNPROVABLE at 29/30**, with the original denominator and failure preserved.
- **Separately labelled discovery detector: KILLED.** Its pristine control passed, the applied mutation produced the wrong enabled classification, and the restored control passed. This is additional post-seal falsification evidence, not a replacement oracle or a revised sealed denominator.

## Restoration and identities

SHA-256 of the complete scratch quota source:

| State | SHA-256 |
|---|---|
| Before | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` |
| Mutant | `e3adc07fb87dd40b0168a638c88fa7035a66acc5c2bd024406a3c5326c019b00` |
| Restored | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` |

The single edited line was reversed immediately after the mutant run. The restored detector observed the exact original source hash, and all 31 restored outputs/exits/stderr matched their pristine controls exactly. Independent before/after `sha256sum` observations of production also returned that same original hash. Production remained untouched.

Every frozen case digest stayed identical across phases. Their oracle-order combined SHA-256 was `3323f4246ee637dd030138db330e7125d9775cf1a35a5e6be357fc596818a0e8`. Detector source SHA-256 was `7c3c63b6d676f04c7c8ca8ebf9c859b3a7e4120cc6163926459614d415abbb96` in every phase. The archived mutant source's complete byte hash equals the hash observed by the mutant detector.

## Retained evidence and limits

Only small scoped mutant source, a synthetic discovery fixture, identity/argv receipts and bounded outputs were archived; no Git history was archived:

- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/MutTmpfsSuffix/mutant-mori-quota-surface.py` — 66,695 bytes, exact mutant hash above.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/MutTmpfsSuffix/discovery-fixture.json` — exact executed fixture bytes, SHA-256 `eb8775e5e19aa6d66d8dcdb52b8f33c3f2549e0385dc564c138f3f7e6c15568e`.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/MutTmpfsSuffix/argv-hashes.json` — exact argv, resource bounds, per-case identities, mutation and restoration comparisons.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/MutTmpfsSuffix/probe-result.json` — 209,553 bytes; SHA-256 `7e5d5c77cb64db474ca0b6990af7d6a63a6185eccb764b8c9c905c1c73a924d7`; actual outputs and predicate results for all three phases.

No builds, linters, formatters, full driver, public selftest, C1 detector, host quota reads, mounts, privileged commands, session/transcript reads or sibling writes were performed. Existing Python 3.14.8 and prlimit from util-linux 2.42.4 were used; no tools were installed or updated. C1 is not remeasured by this C2-only probe. The corrected co-evolved selftest arm is not frozen `CaseEscapedSpace`. Four inherited unallowlisted hits, original permission RED11/12, two unknown dispositions, blocked baseline acceptance and `privacy_clearance=false` remain unchanged. This is author-lane falsification advice, not closure, clearance, health or promotion authority.
