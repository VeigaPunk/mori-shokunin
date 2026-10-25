# RevCountC2Code — counter review

## Findings

- **Medium — SOURCES parser rejects valid indented table rows.** `sources_row` (count-c2.py:94-98) only matches 0–3 leading spaces, while `parse_table` itself accepts any indentation. Reproducer:
  ```text
  python3 -c 'import importlib.util; p=".ufo/waves/round-47/count-c2.py"; s=importlib.util.spec_from_file_location("c",p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); print(m.sources_row("    | S475 | x |", "S475"))'
  output: None (exit 0)
  ```
  A correctly populated S475 row indented by four spaces is treated as absent, causing false `source_row` failure. This is a robustness defect, not a false-green.

- **Low — `--repo` / `--entry` option parsing can raise uncaught IndexError.** Each `while option in args` immediately reads `args[i+1]` without checking presence. Reproducer: `python3 .ufo/waves/round-47/count-c2.py HEAD --entry` exits nonzero with traceback rather than the advertised `C2_SETUP usage`/setup exit 2. Same for `--repo`. Values with leading `-` also consumed as paths, resulting in misleading revision handling. This affects malformed CLI invocation only.

## Checked, no defect reproduced

- `parse_events` supports multi-line `__field` arguments: tested a declaration with type and field name on separate lines; output `{'x': {'pid'}}` (exit 0). `__array` and `__string` use the same extraction patterns for the field-name position and appear covered by the regex structure; no concrete failing reproducer found.
- `parse_table` stops after a blank line once data rows exist, so a later table is not merged; this is consistent with parsing the first relevant contiguous table. Reproducer with a second table after a blank yielded only the first row.
- `git_reader` returns `None` for git show nonzero status; subprocess startup/timeout exceptions are not caught inside the reader and could traceback under exceptional invocation. No concrete environmental failure tested.

## Verification

- Command: `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47-RevCountC2Code python3 .ufo/waves/round-47/count-c2.py --selftest`
- Output: `C2_SELFTEST pass=13 fail=0`; exit 0.
- No tools installed/updated.
