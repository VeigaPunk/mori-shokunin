# Round 23 output-fence review

Axes reviewed: output confidentiality, caller-path provenance, health/verdict semantics, and oracle leak-detection coverage.

## Conclusion

Static review found no source, UUID, quota-file-value, or non-quota-option value emitted by the inspected production output projection. `path` is copied from the caller/fixture row; `realpath` is used for mount resolution but is not projected. `QUOTA_DISABLED` describes only visible quota-mechanism state, not capacity or health. I found one low-severity blind spot in the sealed oracle's canary generation and one low-severity output-schema documentation mismatch. Neither is evidence of a current production leak.

The reviewed source and oracle files have no committed diff between production pin `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` and `HEAD`, and no worktree diff for those paths. This was a static review; I did not invoke a fixture, selftest, real-mode probe, or host quota read.

## Passes and evidence

- `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py:311-344` parses mount source and super-options into internal `Mount` fields. At `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py:347-371`, super-option values are discarded at the first `=`, and the output option list is the sorted intersection with fixed filesystem-specific key allowlists. Source values, non-quota options, and option values are not copied into the row.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py:513-558` constructs rows from a fixed set of fields. `path` is `row["path"]`; `mount_point` is the selected decoded mount point; `realpath`, mount source, device basename and UUID are not row fields. Preempted paths return empty `quota_option_keys` and null `btrfs_qgroups_mode`. Btrfs classification at `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py:465-484` returns fixed state/basis tokens and an allowlisted mode, not the matched UUID.
- Real-mode sysfs scanning at `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py:571-627` never reads `qgroups/mode`; the mode is intentionally null. `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py:774-804` projects a fixed top-level object and serializes it as JSON. `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py:785-794` uses fixed setup reason tokens rather than including input text.
- The frozen `CaseExt4Journaled` at `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/frozen/quota-cases/CaseExt4Journaled.json:4-39` carries a synthetic quota-file value; its six-field primary expectation does not include metadata fields, so the oracle's full-stdout leak check is the relevant fence. The oracle's `canaries`/`leakage_hits` at `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/oracle-quota.py:110-164` checks full `key=value` tokens and distinctive option values against stdout; `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/oracle-quota.py:291-296` records the result. Its supplementary failures are included in the oracle's final exit decision (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/oracle-quota.py:529-562`).
- The frozen `CaseSymlinkRealpath` at `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/frozen/quota-cases/CaseSymlinkRealpath.json:3-53` pins the caller-given path while selecting classification from the synthetic realpath. This matches production construction of the real row at `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py:665-676` and output projection at `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py:515-516`. The `mount_point` output remains the selected mount's field, as specified by the contract; it is not mislabeled as the caller path.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py:99-117,155-164,561-568` states and implements mechanism-only verdict precedence. The fixed `limits` text explicitly says `QUOTA_DISABLED` is not a capacity or health verdict and that ENOSPC can coexist. No health, clearance, limit, or usage field is projected. This matches `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/knowledge/quota-surface-r23.md:73-85` and the source-derived round-23 lesson at `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-23.md:59-62`.

## Low — oracle canaries omit some source/value spellings

- **Exploit path:** A future output regression could append a raw non-absolute mount-source token, or a bare alphanumeric quota-file value, to the permitted `limits` string. The primary case tuple and output key checks can still match; `limits_text` only requires a nonempty string (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/oracle-quota.py:271-272`). However, `canaries()` only adds mount sources whose raw/decoded spelling starts with `/` (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/oracle-quota.py:125-135`), and only adds a bare option value when `is_distinctive()` finds non-alphanumeric punctuation (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/oracle-quota.py:103-107,136-142`). The full `key=value` option token is checked, but that does not detect a regression that emits only an alphanumeric value.

**Impact:** This is a test-coverage false negative, not a leak in the inspected production implementation. The oracle can report no leakage for those fixture spellings even though the contract prohibits echoing any mount source or option value.

**Smallest remediation:** Extend the sealed synthetic canaries with a distinctive non-absolute source and an alphanumeric-only quota-file value, and make the canary assertion cover those bare strings. Also compare `limits` with its fixed expected text so it cannot become an unvalidated carrier for input metadata. Keep canary values synthetic.

## Low — setup-error output shape is underdocumented in the tool docstring

- **Evidence:** The tool docstring says stdout contains exactly the six ordinary top-level fields at `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py:91-107`; `setup_payload()` also adds `error` at `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py:785-794`. The oracle documentation explicitly permits this optional setup-only token at `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/oracle-quota.py:32-35`, and the amendment requires a fixed token only for an unstatable path at `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/preseal-amendment.md:79-80`.

**Exploit path:** A downstream consumer that follows the production docstring's “exactly” claim may reject otherwise valid `QUOTA_SETUP` output, while a consumer following the oracle contract accepts it.

**Impact:** Contract/documentation ambiguity for setup errors; no dynamic input is included by the inspected `setup_payload` path.

**Smallest remediation:** Clarify the tool docstring that `QUOTA_SETUP` may add the fixed-token `error` field and keeps `paths: []`; do not remove the required output token or widen it to exception/input text.

Report: `.ufo/waves/round-23/falsify/ReviewOutputFence.md`
