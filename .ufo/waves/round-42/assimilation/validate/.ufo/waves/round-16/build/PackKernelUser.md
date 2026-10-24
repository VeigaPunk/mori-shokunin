# PackKernelUser — round-16 fixture pack report

Seat: `MoriR16.PackKernelUser` (leaf executor). No runs executed; pack is
data only for `tools/mori-round16-regressions.py` (owner: WindowHarness).

## Files changed

- `.ufo/waves/round-16/fixtures/KernelUser.json` (new, 4 cases)
- `.ufo/waves/round-16/build/PackKernelUser.md` (this report)

## Source verification (before writing)

Verified the exact catalog id bytes in `tools/mori-census.sh` (HEAD
`c13df48`-era working tree, file `tools/mori-census.sh` size 223560):

- `tools/mori-census.sh:1032` `JOURNAL_ID_KERNEL_OOM=fe6faa94e7774663a0da52717891d8ef` — kernel OOM unit notice (topic id confirmed byte-exact)
- `tools/mori-census.sh:1033` `JOURNAL_ID_OOMD=d989611b15e44c9dbf31e3c81256e4ed`
- `tools/mori-census.sh:1034` `JOURNAL_ID_COREDUMP=fc2e22bc6ee647b6b90729ab34a250b1`
- r15 positive predicates, `tools/mori-census.sh:976-984`:
  - `positive_kernel_oom`: fe6faa94 records
  - `positive_unit_oom`: d9b373ed + `UNIT_RESULT=="oom-kill"`
  - `positive_unit_signal`: d9b373ed + `UNIT_RESULT=="signal"`
  - `positive_process_sigkill`: 98e32220 + `EXIT_CODE=="killed"` + scalar `EXIT_STATUS` `"9"`/`9`
- Window query field set per spec: `__CURSOR,_BOOT_ID,MESSAGE_ID,UNIT_RESULT,EXIT_CODE,EXIT_STATUS` — no `MESSAGE` anywhere in the pack.

## Cases (all scope `user`, anchor `mori-journal-anchor-v1`, boot `aaaa…a` ×32)

| id | scenario | records after anchor | expected |
|---|---|---|---|
| `kernuser_oom_before_anchor_only` | A kernel-OOM notice at/before the anchor cursor exists only as the anchor record itself; nothing newer | 0 | rc0 `MORI_JOURNAL_WINDOW_OK`, `positive_kernel_oom=0` |
| `kernuser_oom_after_anchor_single` | Anchor record carries the *wrong* (oomd) id; exactly one kernel-OOM notice lands after | 1 | rc0 OK, `positive_kernel_oom=1` |
| `kernuser_oom_fanout_after_anchor` | Two kernel-OOM unit notices after the anchor (one kernel kill fans out to multiple unit notices — notices, not victims) | 2 | rc0 OK, `positive_kernel_oom=2` |
| `kernuser_non_oom_ids_after_anchor_never_kernel_positive` | OOM at the anchor, then only oomd + coredump ids after; `positive_kernel_oom` must stay a real 0 | 2 | rc0 OK, all four positive counts 0 |

Every emitted line carries `__CURSOR`, `_BOOT_ID`, `MESSAGE_ID`; first line
replays the exact anchor cursor + boot; all later cursors are unique valid
scalars on the same boot. `stderr=""`, `returncode=0` throughout.

## Evidence

- Pack parses cleanly; per-case `records_after_anchor` recomputed from the
  embedded JSONL matches `want.records_after_anchor` (4/4 verified by a local
  consistency check, not the harness — no harness/tool run performed).
- No live journal, network, or credential access; no /tmp use; no commits.

## Risks / blockers

- Schema assumption: `__CURSOR` values are opaque printable scalars; used
  `s=kern;u=cursor-anchor;`-style strings (within the ≤4096 no-control-char
  bound). If WindowHarness defines a stricter cursor grammar, adjust only the
  literal strings — case semantics unchanged.
- Cases assume `--cursor=<anchor>` is inclusive (first record replays the
  anchor and is dropped per spec), so "before anchor" is represented by the
  anchor record itself rather than a pre-anchor line the wrapper cannot emit.
- None blocking; no coordination sent (no schema conflict found).

Report: .ufo/waves/round-16/build/PackKernelUser.md
