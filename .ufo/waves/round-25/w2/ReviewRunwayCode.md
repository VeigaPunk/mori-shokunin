# ReviewRunwayCode: review of tools/mori-job-runway.py at the lane tip

Seat: MoriR25.ReviewRunwayCode (leaf; no subagents, no background jobs). Round 25, wave 2 (falsify).
Reviewed: lane HEAD `07a31ae`; tool blob `239dd8eb` (690 lines, 25,410 bytes). Tool history: `09f55b6` (landed),
`9a3d511` (A2 abstentions and co-evolved supplementary cases), `fbecc59` (selftest zero-case and expect checks).
The working tree equals HEAD for `tools/`. Every run was in a private copy (`git archive HEAD tools`), never in the lane.

## Verdict

- **BROKEN against A2 (the abstention rule).** A2 requires the tool to abstain on forms it cannot read the way omp does.
  The tool still returns a number, or `RUNWAY_DEFAULT` with exit 0, for YAML that Bun 1.4.3 reads differently, and it still
  returns `set` for files Bun refuses to parse (the defect class A2 names). Bun 1.4.3 is the parser omp embeds (`Bun v1.4.3`
  and `Bun.YAML.parse(await Bun.file(net()).text())` found in the omp bytes). Findings F1 and F2, both High.
- **HELD for the declared frozen after-value.** `python3 -I -B tools/mori-job-runway.py --selftest` prints
  `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21`, exit 0 (also from `/tmp`). `cases.json` is blob `48df844a` at `7634be75` and at HEAD.
  The co-evolved `supplementary-cases.json` (blob `82cca1cb`) prints `PASS 18/18` (not counted).
- **HELD for rules 2 to 6 on every verdict the code produces for the inputs I probed.** The clamp and default patterns
  (lines 113 to 117) match the contract text. The effective and verdict logic (lines 436 to 471) matches rules 4 and 5.
  The output keys (lines 476 to 494) match rule 6. Live readout on this host (bytes only): configured 200, clamp found 100
  (1 site), setting_default found 100 (1 site), effective 100, `RUNWAY_CLAMPED`, exit 1. Crash paths are F4.
- **WEAKENED for rule 7 and the `--cases` flag.** `--cases ""` silently runs the frozen cases (F3). Malformed cases files crash
  with exit 1, which is the code for `RUNWAY_CLAMPED` (F4).
- **Read-only guarantees: HELD.** The tool has no process execution (no `subprocess`, `Popen`, `os.system`, `os.exec*`,
  `os.spawn*`). Its only writes are lines 549, 551 and 556, inside the selftest temp directory (`_materialize` is called only at
  line 582, inside the block at line 581). `shutil.which("omp")` (line 617) resolves a path and never runs it.
- **Memory on a 256 MB binary: HELD with a caveat (F10).** No anonymous memory growth. The scan maps the whole file, so peak RSS
  is about 267 MB, all file-backed and reclaimable. Real omp: 0.30 s. Adversarial 256 MB input: 1.9 to 2.3 s (linear; no
  catastrophic backtracking).

## Severity scale used

High: a binding contract rule is wrong on a reachable input. Medium: wrong exit or verdict semantics, a hang or crash on operator
input, or a letter-level rule violation that yields a false number. Low: documentation, design, or a safe-direction deviation.
Nit: cosmetic or dead code.

## Findings

| ID | Severity | Lines (tool unless noted) | Finding |
|---|---|---|---|
| F1 | High | 281, 285, 291-292, 295, 336-344 | Valid YAML that defines `async.maxJobs` is read as "no maxJobs". Output is `RUNWAY_DEFAULT`, exit 0, effective 100, while omp reads 50. A2 abstention rule broken. |
| F2 | High | 137-139, 298-300, 310, 334-336, 262-264, 283-284 | Stray or deeper lines under `maxJobs`, and an `async:#c` header, give `set` with exit 0 for files Bun refuses (A2's named defect class, still reachable). A continuation line gives a number where omp reads a string. |
| F3 | Medium | 517-521 (519) | `--cases ""` is silently replaced by the frozen cases. `--selftest --cases ""` prints `PASS 21/21`, exit 0. |
| F4 | Medium | 366, 575-586, 666-690 (684) | Uncaught exceptions exit 1, which is `RC_CLAMPED`. Reproduced: a 4301-digit `maxJobs` value; cases files shaped `[]`, `{"cases":"abc"}`, `{"cases":[1]}`, or a non-dict `expect`. |
| F5 | Medium | 221-238 (227-228), 384-404 (393), 397-398, 415-428 (420-425) | No file-type or size guard. `--config /dev/zero` exhausts memory. A FIFO (config or binary) or `/dev/zero` (binary) hangs. Contract says `unreadable` for paths that cannot be read as a file. |
| F6 | Medium | 251, 138, 152, 155, 186, 205, 213, 262, 298, 337, 358 | Python `strip()` and `splitlines()` treat NBSP, U+2028, U+0085, U+000B, U+000C and U+001C as whitespace or breaks. Rule 1 says `malformed` for any value that is not a plain integer. Some inputs give a false number. |
| F7 | Low | supplementary `note`; docstring 73-74 | Shipped text overclaims. "Every form the tool cannot read the way omp reads it is an abstention" and "`RUNWAY_UNKNOWN` is never a false number" are both false at the tip (F1, F2, F6). |
| F8 | Low | 235-238 | A config path whose parent is a regular file reports `unreadable` (`ENOTDIR`). Rule 1 says `absent` when the file does not exist. Safe direction: exit 2. |
| F9 | Low | 401-402, 420-425, 486 | Three separate passes over the binary (two regex scans, then a hash). `binary_sha256` is not taken from the same mapping the scans read. |
| F10 | Low | 401-402 | The mmap scan makes the whole binary resident (peak RSS about 267 MB, file-backed). Design note, not a correctness defect. |
| F11 | Nit | 508-511 (510) | The second `_cases_path` candidate resolves to the same file as the first. Dead branch. |
| F12 | Nit | 612-613, 656-660, 670-672 | `_UsageError` is never raised, so the `except` at 670 is dead. `_emit_error` output (keys `error` and `verdict`) differs in shape from rule 6. |
| F13 | Nit | 673-674 | `--selftest` silently ignores `--config` and `--binary`. Should be a usage error, as `--cases` is without `--selftest` (675-677). |
| F14 | Nit | 620, 683 | Default binary path is `realpath`; explicit `--binary` is `abspath`. Harmless; unify. |

## Finding detail

### F1 (High). Valid YAML that sets `async.maxJobs` is read as "no maxJobs"

Evidence (tool run in the private copy on the config text shown; Bun 1.4.3 read of the same text):

| Config text | Tool state, verdict, exit | Bun 1.4.3 (omp's parser) |
|---|---|---|
| `async:` / `  {maxJobs: 50}` | absent, `RUNWAY_DEFAULT`, 0 | 50 |
| `async:` / `  !!str maxJobs: 50` | absent, `RUNWAY_DEFAULT`, 0 | 50 |
| `&a async:` / `  maxJobs: 50` | absent, `RUNWAY_DEFAULT`, 0 | 50 |
| `  async:` / `    maxJobs: 50` / `  other: 1` (indented root) | absent, `RUNWAY_DEFAULT`, 0 | 50 |
| `{async: {maxJobs: 50}}` | absent, `RUNWAY_DEFAULT`, 0 | 50 |

Probe (`harness/diff_vs_bun.py`, 307 generated configs): 72 are FALSE_ABSENT. 62 come from the unrecognised header spellings
`&a async:` (H4, 31 configs) and `"\x61sync":` (H9, 31 configs). 10 come from child or root forms under plain headers:
`{maxJobs: 50}`, `!!str maxJobs`, `&a maxJobs` and `"max\u004aobs"` (each under two headers, 8 configs), the flow root, and the
indented root.

Root cause: the header test (285) and the child filter (336-344) recognise only the literal spellings. Any other child key is
skipped silently. Line 342 returns `malformed` only when the normalised key is exactly `maxJobs`. Line 281 skips indented root lines.

Contract: A2 says "The tool must abstain on forms it cannot read the way omp does", and that `RUNWAY_UNKNOWN` is never a false
number. The docstring (74-75) says an abstention is always the safe direction. Note: the indented-root case follows rule 1's literal
"column 0" wording. A2's principle requires abstention there, so the rule text needs a matching amendment.

Likelihood: low (valid but unusual YAML). Impact: exit 0 reports the default cap while omp uses a lower one.

Smallest fix:
1. Return `malformed` when a column-0 line starts with one of `& ! * { [ ? % " '`, or when the first non-comment line of the file is indented.
2. In the async block, return `malformed` when a direct child does not start with a plain key (`[A-Za-z_][A-Za-z0-9_.-]*[ \t]*:` followed by a space or the end of the line). This covers `&`, `!`, `{`, quotes and `- `.
3. Add the five forms above as supplementary cases with `verdict: RUNWAY_UNKNOWN`, `exit: 2`.

### F2 (High). Stray lines under `maxJobs`, and an `async:#c` header, produce numbers for files Bun refuses

Evidence (tool CLI output, then Bun on the same text):

- `async:` / `  maxJobs: 50` / `     extra: 1` (five-space stray line). Tool: `set 50`, `RUNWAY_AS_CONFIGURED`, exit 0. Bun: `YAML Parse error: Unexpected token`.
- `async:` / `  maxJobs: 50` / NBSP-only line / `  x: 1`. Tool: `set 50`, exit 0. Bun: parse error. (Line 310 and the blank test at 137-139 treat an NBSP-only line as blank.)
- `async:#c` / `  maxJobs: 50`. Tool: `set 50`, exit 0 (line 299 accepts a `#` directly after `async:`). Bun: `YAML Parse error: Multiline implicit key`.
- `async:` / `    foo: 1` / `  maxJobs: 50` (shallow `maxJobs` after a deeper first child). Tool: absent, `RUNWAY_DEFAULT`, exit 0. Bun: parse error.
- `async:` / `  maxJobs: 5` / `    0` (continuation line). Tool: `set 5`, exit 0. Bun reads the string `"5 0"`. Rule 1 says `malformed` for any non-integer value.

Probe totals: 21 NUMBER_ON_PARSE_ERROR (14 are the `async:#c` header variants; 4 are deeper duplicate or extra lines under
`maxJobs`; plus the NBSP-only case, the five-space stray line and the U+2028 case) and 15 DEFAULT_ON_PARSE_ERROR (including the
shallow-line case and the tab-indented root).

Root cause: lines 334-336 skip every block line whose indentation differs from the first child's ("Deeper (or oddly indented)
lines are not direct children"). Lines 298-300 accept `async:#c`. A2 names `set` for a file omp refuses to load as the defect
class it was written to remove, and requires abstention on forms the tool cannot read the way omp does.

Likelihood: a stray non-comment line under `maxJobs` is uncommon but a plausible typo; the header and NBSP cases are rarer.

Smallest fix:
1. In the block loop, a non-comment line whose indentation is not the child indentation is `malformed`, unless it is deeper than a direct child whose value is empty (a nested mapping).
2. A non-comment line deeper than a direct `maxJobs:` line is `malformed` (continuation or invalid YAML).
3. Lines 298-300: after `async:`, accept only end of line or whitespace before a `#`; otherwise `malformed`.
4. Blank tests use the F6 fix (no Unicode whitespace).

### F3 (Medium). `--cases ""` runs the frozen cases silently

Evidence: `python3 -I -B tools/mori-job-runway.py --selftest --cases ""` prints `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21`, exit 0.
Cause: `_resolve_cases` tests truthiness (line 519), so an empty string falls through to the frozen file (line 521).
A supplementary run with an unset shell variable therefore reports the frozen result.
Smallest fix: `if cases_override is not None:` (an empty path then resolves to a directory and fails with `FAIL 0/0`, exit 2).

### F4 (Medium). Uncaught exceptions exit 1, which is the `RUNWAY_CLAMPED` code

Evidence (exit codes observed):
- A `maxJobs` value of 4301 digits: `ValueError: Exceeds the limit (4300 digits) for integer string conversion` from line 366, exit 1. (The 4300-digit value parses.)
- `--selftest --cases` on files `[]` (fails at line 575), `{"cases":"abc"}` (fails at line 580), `{"cases":[1]}` (line 580) and `{"cases":[{"id":"Q1","expect":"notdict"}]}` (line 587, where `expect.get` runs): `AttributeError`, exit 1 each.
- `main` (666-690) has no guard around `evaluate` (line 684).

Contract: rule 5 gives exit 1 to `RUNWAY_CLAMPED`. Gates that read exit codes would act on a crash as a clamp.
Smallest fix:
1. Line 366: catch `ValueError` and return `malformed`.
2. In `_selftest` after line 569: check that the document is a dict, `cases` is a list of dicts, each `expect` is a dict, and each `config` is null, a string, or `{"dir": true}`. Otherwise print `FAIL` lines and return 2.
3. In `main`, wrap `evaluate` in a broad `try`; on error print the rule-6-shaped JSON with `RUNWAY_UNKNOWN` and return 2.

### F5 (Medium). No file-type or size guard on the read paths

Evidence (exit codes observed, private copy):
- `--config /dev/zero --binary omp` under `ulimit -v 1048576`: `MemoryError`, exit 1. Line 228 (`handle.read()`) has no size limit.
- `--config <FIFO>`: killed by `timeout` at 5 s, exit 124. `open` at line 227 blocks.
- `--binary /dev/zero`: killed at 10 s, exit 124. The size is 0, so the clamp reports `absent` (397-398), then `_sha256` loops forever (420-425).
- `--binary <FIFO>`: killed at 5 s, exit 124. `open` at line 393 blocks.

Contract: rules 1 and 2 say `unreadable` for a path that cannot be read as a file.
Smallest fix: `os.stat` and `stat.S_ISREG` before opening; open with `os.O_NONBLOCK`; for the config, read at most 1 MiB plus one byte and treat more as `unreadable`.

### F6 (Medium). Unicode whitespace and line breaks

Evidence (tool state and Bun read of the same text):
- `async:\u2028  maxJobs: 50`: tool `set 50`, exit 0 (line 251 splits at U+2028). Bun: no `maxJobs`, so omp uses its default.
- `  \u00a0maxJobs: 50` (NBSP before the key, under `async:`): tool `set 50`, exit 0 (line 337 strips the NBSP). Bun: the key is `\u00a0maxJobs`, so omp has no `maxJobs` (probe H1/C9, H2/C9).
- `maxJobs: 50\x85`: tool `set 50`. Bun string `"50\x85"`. A JavaScript number conversion gives NaN.
- `maxJobs: 50\x1c`: tool `set 50`. Bun string.
- `maxJobs: 50` followed by NBSP, form feed or vertical tab: tool `set 50`. Bun string. JavaScript's number conversion trims these, so the number happens to match, but rule 1 still says `malformed`.

Cause: `str.strip()` at lines 138, 152, 155, 186, 205, 213, 262, 298, 337 and 358, and `text.splitlines()` at line 251. YAML 1.2 breaks lines only on CR, LF and CRLF, and strips only space and tab.
Smallest fix: split on CRLF, CR and LF only; strip only `" \t"`; return `malformed` for C0 controls other than tab, DEL, U+0085, U+2028 and U+2029.

### F7 (Low). Overclaims in shipped text

- `tools/fixtures/mori-job-runway/supplementary-cases.json`, field `note`: "Every form the tool cannot read the way omp reads it is an abstention."
- `tools/mori-job-runway.py` docstring lines 74-75: "`RUNWAY_UNKNOWN` is never a false number".

Both are false at the tip (F1, F2, F6).
Smallest fix: reword now, or keep the sentences and land F1, F2 and F6 with their reproducers as cases.

### F8 (Low). `ENOTDIR` reports `unreadable`

Evidence: `--config notadir/config.yml` where `notadir` is a regular file: `configured {state: unreadable}`, `RUNWAY_UNKNOWN`, exit 2.
Cause: lines 235-238 map every `OSError` except `ENOENT` to `unreadable`.
Smallest fix: map `errno.ENOTDIR` to `absent` too (rule 1's wording), or document the deviation. Safe direction either way.

### F9 (Low). Three passes, and the hash is not from the scanned bytes

Lines 401-402 (clamp scan), the second `_binary_sites` call from line 478 (default scan), and 420-425 (`_sha256`, called from line 486) each open or map the file. If the binary changes between passes, the output mixes two versions.
Smallest fix: one `open`, one `mmap`; run both regexes and `hashlib.sha256(mapped)` on that one mapping.

### F10 (Low). Memory design on a 256 MB binary

Measured in-process (`/proc/self/status` VmHWM, read inside the child):
- Real omp: VmHWM 268,940 kB; RssAnon stays about 8 MB; runtime 0.30 s.
- Synthetic 256 MB binary (random bytes, sites planted near the end): VmHWM 268,956 kB; runtime 0.29 to 0.37 s.
- Adversarial 256 MB binary (2,000-digit runs after each clamp prefix): VmHWM 266,988 kB; clamp scan 1.89 s; full run about 2.2 s. Linear in size.

The peak is file-backed and reclaimable. Mapping the whole file (401-402) is the reason. A chunked scanner with an overlap window would bound RSS.
Truncating the file during a scan could raise SIGBUS [INFERENCE: not run].
Smallest fix (optional): chunked scan with overlap, or document the peak.

### Nits

- F11: line 510 resolves to the same file as line 509 (`script_dir/..` is the repo root, so both give `tools/fixtures/...`). Delete it.
- F12: `_UsageError` (612) is never raised; `except _UsageError` (670) is dead. `_emit_error` (656) serves only the `--cases` misuse path. Delete the class or raise it.
- F13: lines 673-674 return before checking `--config` and `--binary`. Make them a usage error.
- F14: line 620 uses `realpath`; line 683 uses `abspath`. Pick one.

## Checks that held (evidence)

- **Rules 2 and 3 patterns.** Lines 113-115 and 117 match the contract text. On the real binary: clamp `found`, 100, 1 site; setting_default `found`, 100, 1 site; `binary_sha256` `85d9daf3a05fc76e8cd425ae1904eb576af8d21cc85fcf4690742626e07ccfa4`.
- **Rules 4 and 5.** `_effective` (436-455) and `_verdict` (458-471) match the contract table. Checked by reading and by the live run (configured 200, effective 100, `RUNWAY_CLAMPED`, exit 1). Usage errors exit 2 (argparse).
- **Rule 6.** Keys in `evaluate` (474-497) match the contract.
- **Rule 7 core.** Frozen 21/21; supplementary 18/18; from `/tmp` 21/21 (path resolution correct). `--cases` on a directory, on a nonexistent file, or without `--selftest`: exit 2 with a clear message.
- **A2 forms the contract enumerates.** These abstain as written (probe IDs in brackets): quoted or spaced `async` ([H5], [H6]); duplicate top-level `async` ([F5]); merge key `<<` ([C30]); complex key `?` ([C29]); `---` and `...` ([F9], [F10]); `#` without a space after a value ([C23]); quoted value ([C21]); block scalar ([C33], [C34]); tab in the async block ([C28]); inline `async: {...}` ([F2]); duplicate `maxJobs` ([X7]). BOM and CRLF read correctly ([W1], [W2]).
- **Read-only.** `grep -nE "subprocess|os\.system|Popen|os\.exec|os\.spawn"` on the tool: no matches. Write-capable calls (grep for `open(...,"w")`, `os.mkdir`, `os.remove`, `json.dump`): lines 549, 551, 556 only, all inside `_materialize`. `_materialize` is called only at line 582, inside `tempfile.TemporaryDirectory` (581).
- **Never runs omp.** Confirmed by the grep above. The live readout reads the omp bytes only.

## Residual risk and verification gaps

- **What omp does when Bun throws on its config** (refuse to start, fall back to defaults, or crash) is not verified. The NUMBER_ON_PARSE_ERROR and DEFAULT_ON_PARSE_ERROR classes rest on A2's clause, not on observed omp behaviour. [INFERENCE]
- **omp was never executed.** Bun 1.4.3 was used as the parser on the same text. The embedded `Bun.YAML.parse` call and the `Bun v1.4.3` string were found by reading the binary as bytes.
- **Probe coverage is a sample, not exhaustive.** 307 configs: 280 header by child combinations (7 header spellings, 40 child forms), 24 named extras, and 3 document wrappers (BOM, CRLF, `---`). FALSE counts are lower bounds.
- **Probe input path.** The probe feeds JavaScript strings. omp reads with `Bun.file(...).text()`. The BOM and CRLF cases agree, but the decoding path was not compared byte for byte.
- **Python version.** The 4300-digit limit (F4) was reproduced on the host's Python 3.14.8 only. Older Pythons may not reproduce it.
- **Not run:** permission-denied and symlink-loop paths; character devices other than `/dev/zero`; sockets; re-deriving each of the 21 frozen expected values by hand (they pass); the pressure tool and other tools; any mutation tests (not assigned to this seat).
- **Memory measurement caveat.** `ru_maxrss` read from child processes showed 537 MB, inherited from my harness process's own peak. I discarded it. Figures above are VmHWM read inside the child.
- **Default config path.** `~/.omp/agent/config.yml` is the contract's default. I did not re-derive omp's config path from the binary (`config.yml` appears 29 times in the bytes; not resolved).

## Tooling record

- Installed or updated: nothing. Read `~/.omp/agent/RULES.md` first. Host tools used as found: `/usr/bin/python3` 3.14.8; `~/.local/bin/bun` 1.4.3 (the same version omp embeds); `git` read-only subcommands only (`log`, `rev-parse`, `show --stat`, `archive`); `timeout`, `ulimit`, `mkfifo`.
- Private copy (tools from HEAD, plus `harness/`): `/fast/scratch/hyaku/mori-r25/w2-ReviewRunwayCode`. The 512 MB synthetic and adversarial binaries were removed; the copy is now about 1.7 MB. The harness is kept there for the main agent to re-run.

## Reproduce (private copy)

```
cd /fast/scratch/hyaku/mori-r25/w2-ReviewRunwayCode
python3 -I -B tools/mori-job-runway.py --selftest                                              # PASS 21/21
python3 -I -B tools/mori-job-runway.py --selftest --cases tools/fixtures/mori-job-runway/supplementary-cases.json  # PASS 18/18
python3 -I -B tools/mori-job-runway.py --selftest --cases ""                                   # PASS 21/21 (F3)
python3 -I -B harness/diff_vs_bun.py                                                           # total 307, needs bun 1.4.3
```

## Hand-off to main

- After fixes, rerun: the frozen 21 (unchanged), the supplementary file, and `harness/diff_vs_bun.py` (expect zero FALSE_SET and zero FALSE_ABSENT outside the enumerated A2 forms).
- Decide the indented-root rule (F1) and the continuation rule (F2), and amend the contract text to match A2's principle. The tool currently follows rule 1's literal wording there.
- C2 after-value: held. A2 abstention rule: not held as written until F1 and F2 land.
