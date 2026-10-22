# ReopenS160 — contract A1 residual F3 (S160 re-fetch, hash, excerpt diff, Gate quotes, teaches support)

**Verdict: agree.** S160's admit Gate line, its excerpt and its sha256 all re-derive from the live v262 bytes: a fresh fetch returns the identical full-file sha256, all 39 excerpt lines match line-for-line, both Gate quotes are verbatim at the labelled lines and both `(N words)` labels are exact. One caveat, not a defect: the Gate quotes witness only two of the three clauses in the SOURCES `teaches` cell; the third clause is carried by the row's companion paths, which I fetched and found true.

Seat: MoriR30.ReopenS160. Lane tip measured: `ad0f04745ced2194e58c22a0d6b38131bee3e230`. All lane reads via `git show`/plain file reads; no lane writes outside this file.

## 1. Live re-fetch (observed)

Command (scratch dir `/fast/scratch/hyaku/mori-r30-w2/MoriR30.ReopenS160/`):

```
curl -sS -o journalctl.c -w 'HTTP=%{http_code} SIZE=%{size_download} TIME=%{time_total}\n' \
  https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journalctl.c
```

- URL: `https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journalctl.c` (exactly S160's URL)
- HTTP status: **200**; size `47020` bytes; `time_total 0.334376`
- Access time: **2026-10-22T22:02:39Z** (`date -u` immediately after the fetch returned)
- `wc -l`: `1139`
- `sha256sum`: `285b3d0c1217b9a3be90dca2ed4591eb8cf0192e2d3c75f303df3c5f18d5d0ab`

## 2. Hash agreement (observed)

Computed `285b3d0c1217b9a3be90dca2ed4591eb8cf0192e2d3c75f303df3c5f18d5d0ab` equals, character for character:

- excerpt header `corpus/evidence/sources-r30/S160.txt:3` (`sha256: 285b3d0c…d5d0ab`);
- Gate admit line `corpus/lessons/round-30.md:138` (fourth cell, backticked 64-hex).

The authored access time (`2026-10-22T21:12:34Z`, in both `S160.txt:4` and `round-30.md:138`) is ~50 min before mine, so the bytes are stable across two independent fetches, not a one-shot artifact. The excerpt header's `url:` (`S160.txt:2`) is the same URL, and `lines: 509-547` (`S160.txt:5`) matches the 39 rows present.

## 3. Every excerpt line against the fetched bytes (observed)

Method: parse each `<n><TAB><text>` row of `S160.txt`, compare `text` for exact equality (no trimming, no collapse) with `fetched[n-1]`.

- rows parsed: **39** (exactly one TAB per row; no blank or malformed rows)
- range: first `509`, last `547`, contiguous — **no gaps**
- **mismatches: 0**

Spot anchors that the Gate and the row cite, all equal to the fetched bytes: `journalctl.c:512` `OPTION_FULL(OPTION_OPTIONAL_ARG, 'b', "boot", "ID",`; `:513` `"Show current boot or the specified boot"):`; `:514-517` `arg_boot = true; / arg_boot_filter = true; / arg_boot_id = SD_ID128_NULL; / arg_boot_offset = 0;`; `:543` `OPTION('u', "unit", "UNIT", "Show logs from the specified unit"):`; `:544` `r = strv_extend(&arg_system_units, opts.arg);`.

Independent confirmation that the constructs are real, not invented: `grep -n` over the fetched file finds `OPTION_FULL` at `:512` (3 occurrences total), `arg_boot_id = SD_ID128_NULL` at `:508`, `:516`, `:929`, and `option_parser_peek_next_arg` at `:358`, `:531`, `:675`.

## 4. The two Gate quotes: verbatim and word count (observed)

Checks per contract A1 4c (`contract.md:142-144`): locator `` `[file]:L[-M]` ``, then `(N words)`, then a double-quoted string; `wc -w` ≤ 25 and equals N; only `\"`, `\|`, `\\` are unescaped.

Quote 1 — `journalctl.c:514-517` (12 words):
"arg_boot = true; arg_boot_filter = true; arg_boot_id = SD_ID128_NULL; arg_boot_offset = 0;"
- whitespace-collapsed concatenation of fetched lines 514-517 == quote: **true**
- whitespace-collapsed quote strictly inside the collapsed region: **true**
- `wc -w` = **12**; label = **12**; ≤25: **true**

Quote 2 — `journalctl.c:543-544` (13 words):
"OPTION('u', \"unit\", \"UNIT\", \"Show logs from the specified unit\"): r = strv_extend(&arg_system_units, opts.arg);"
- after unescaping `\"` → `"`, collapsed concatenation of fetched 543-544 == quote: **true**
- `wc -w` = **13**; label = **13**; ≤25: **true**

So C1 condition 4's sub-requirements for S160 (`contract.md:39-42`) hold at these bytes: one `admit` line, 64-hex sha256, ≥1 located quote, excerpt header naming the same URL and sha256, quoted text verbatim within the labelled lines. `grep -n S160 corpus/lessons/round-30.md` shows only one `admit` Gate line (`:138`); `:139` (man/journalctl.xml) and `:140` (shared/journal-util.c) are `reject`, so no second admitted URL competes for the id.

## 5. Is the SOURCES `teaches` sentence supported by the quoted lines? (clause by clause)

The `teaches` cell of `corpus/SOURCES.md:166` has three clauses. Two are inside the quoted lines; the third is not, and is covered only by the row's `anchor` cell, which cites companions by path.

1. "`-b/--boot` takes an optional descriptor and, with none, enables the boot filter with a null boot id and zero offset (help: `Show current boot or the specified boot`)" — **supported.** `:514-517` (quoted) set `arg_boot = true`, `arg_boot_filter = true`, `arg_boot_id = SD_ID128_NULL`, `arg_boot_offset = 0`; `:512-513` (in the excerpt, in the row's anchor `:512-517`, but not inside the Gate's quoted span) give `OPTION_OPTIONAL_ARG` and the help text. The Gate quote is the shared initialization both branches start from; the "with none" reading is confirmed by the `else` arm at `:527-540`, whose only mutation is when a peeked next word parses as a descriptor.
2. "`-u/--unit` appends its value to the system-unit filter list" — **supported** by `:543-544` (quoted): `OPTION('u', …)` then `strv_extend(&arg_system_units, opts.arg)`.
3. "how the filter stage resolves a null boot id with zero offset, in the default open with no `--directory`/`--file`/`--root`, to the running machine's boot id and then adds a boot-id match plus a conjunction, and how the unit list becomes unit-name matches over the `SYSTEM_UNITS` fields" — **not in the quoted lines**; it is true, verified independently against the companions the row names:

   - `journalctl-util.c:89` `int journal_acquire_boot(…)`; `:100-101` condition `arg_boot_offset == 0 && sd_id128_is_null(arg_boot_id) && !arg_directory && !arg_file && !arg_file_stdin && !arg_root`; `:102` `id128_get_boot_for_machine(arg_machine, &arg_boot_id)`; `:125` `arg_boot_id = boot_id;` — fetched now, HTTP 200, sha256 `a2385abed40d6417c8bf3acb308010a803ad0105bc72b6053054a8ad2797c64b`.
   - `journalctl-filter.c:62` `static int add_boot(…)`; `:72` `add_match_boot_id(j, arg_boot_id)`; `:76` `sd_journal_add_conjunction(j)` — the "boot-id match plus a conjunction". `:94` `journal_add_unit_matches(…)`; `:123`, `:142` `add_matches_for_unit_full(j, flags, u)`; `:136` `get_possible_units(j, SYSTEM_UNITS_FULL, …)`; `:203` `add_units` and `:214` passes `arg_system_units` — fetched now, HTTP 200, sha256 `480f7a03040c0ddc93b1b65c0b49d6f0e8a4a377ee1b94168655132dcfd72f48`.
   - `journalctl-util.h:9-12` defines `SYSTEM_UNITS` as `_SYSTEMD_UNIT`, `UNIT`, `OBJECT_SYSTEMD_UNIT` — fetched now, HTTP 200, sha256 `5d5d172fcac2f59d48dc1349062fd23a1dbea328a008a7e141f693f5ee2310e5`.

   Consequence for the entry's prose: `corpus/knowledge/earlyoom-invocation-scope-r30.md:1` ("`-b` with no argument selects the current boot", cites `journalctl.c:512-517,543-546`) and `:27` ("for the current boot and `-u` appends the unit match", cites `journalctl.c:514-517,543-544`) assert a consequence that needs the `journalctl-util.c:89-129` link; the row documents that link in its anchor cell, but the Gate quote alone does not witness it. Only the `journalctl.c` line spans may be short for a reader who checks the Gate quote in isolation.

## 6. Nits (no action requested from me; none is a fabrication)

- The `teaches` exclusion list "no `--directory`/`--file`/`--root`" omits `arg_file_stdin` (covered in spirit by `--file=-`) and does not mention that `--machine` is still handled by passing `arg_machine` into `id128_get_boot_for_machine` (`journalctl-util.c:102`). The "default open" phrasing is accurate; the enumeration is only partial.
- The anchor cell was not part of my assigned contract check; I verified it here only to decide whether clause 3's claim is true. It is.

## 7. Limits of this report

- Ran: the curl fetch, `sha256sum`, `wc -l`, the 39-line exact diff, the verbatim/word-count checks (scripted in scratch), three companion fetches, and the `grep` line locators cited above. Nothing ran against a live host unit or journal.
- Not run (so not a pass): `count-c1.sh`, `check-blind-wave.sh`, the tool fixture, any build or lint, any other row's Gate line. Contract A1 4b's URL-novelty clause for S160 (no row below S156 carries this URL) was not exercised here.
- Tooling: no install or update was needed; nothing was installed. `pacman` was not touched.
- Privacy: this report contains no OMP setting, session id, uid/pid, unit name, journal MESSAGE text or earlyoom configuration value. Scratch files under `/fast/scratch/hyaku/mori-r30-w2/MoriR30.ReopenS160/` hold only public systemd source and the extracted row text.
