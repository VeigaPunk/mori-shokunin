# Mo53SentC2Hostile — hostile-input fuzz of `tools/mori-commit-runway.py` (C2, round 53 w1)

Seat: sentinel, C2 tool attack. Lane: mori-shokunin. Entering contract `f4da3fd4`, data commit `2a4213bf`.
Every read below is absolute; nothing under the lane was written except this report. Scratch
`/fast/scratch/hyaku/mori-r53/Mo53SentC2Hostile/` (removed at the end); `disk-guard.sh status` rc=0 before the
run (`/fast/scratch/hyaku` 25 % used, 607.1 G free, `/tmp` 4 %, 123.4 G free). One corpus read, no clone, no
network. Host reads: none in this seat except the tool's own default run (read-only).

## Axes (godspeed)

1. **fail-closed** — every malformed input either yields one JSON object with `COMMIT_UNKNOWN`/exit 2 or is
   rejected in text mode with a message; never a traceback, never a wrong-but-plausible verdict.
2. **contract fidelity** — the docstring's malformed clause and the frozen interface (`--meminfo`, `--vm-dir`,
   `--cpu-present`, `--page-kb`, `--selftest`) versus observed behaviour.
3. **blast radius of a defect** — is it reachable from a reading seat that only controls the three path
   arguments, or only from a hand-written `--cases` file?
4. **remediation cost for the L1** — lines touched under the round-53 "tool may be corrected" rule.

## What was fuzzed

The landed bytes, not the worktree guess: `git show 2a4213b:tools/mori-commit-runway.py | sha256sum` =
`80cb169650bf02578439703bc006173aab7b759ff9cf57337611b27164676156` = `sha256sum tools/mori-commit-runway.py`
(identical); fixtures likewise `cea8045192babe3017a2682c17a1647e73c597eaf0330a27643858577cc43b63` on both.
Interpreter `Python 3.14.8` (the int/str guard of CPython ≥ 3.11 is therefore in force). Baselines on the
unmodified tool: `--selftest` → `MATCHER: rejected 23/23 corrupted expectations` /
`MORI_COMMIT_RUNWAY_SELFTEST: PASS 23/23`, rc=0; the live read → mode 0, `commit_limit_kb 47583772`
== `limit_recomputed_kb`, `verdict COMMIT_HEURISTIC`, rc=0.

Method: a driver (`fuzz.py`, in scratch) materialises a complete valid input set around each hostile element so
one variable moves at a time, invokes
`python3 -I -B /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-commit-runway.py <args>` with
`cwd=$TMPDIR`, and records rc, the parsed JSON, and whether stderr contains a traceback. A case "passes" only if
stdout is exactly one JSON object with `schema=mori-commit-runway-v1` and a verdict in
{COMMIT_OK, COMMIT_HEURISTIC, COMMIT_UNLIMITED, COMMIT_LOW, COMMIT_UNKNOWN} whose exit code equals the counter's
frozen map (unknown=2, low=1, other=0), and no traceback appears. Base fixture: `MemTotal 16000000 kB`,
`SwapTotal 2000000 kB`, `CommitLimit 14000000 kB` (= recompute), `Committed_AS 8000000 kB`, `Hugetlb 0`,
`overcommit_memory 2`, ratio 75, kbytes 0, reserves 65536/131072, `present 0-3` → `COMMIT_OK`, band 62496.

## Table 1 — the 68 cases of the main sweep (input → verdict/exit)

`clean` = one JSON object (or selftest text) with rc matching the verdict, no traceback. `TRACEBACK` = rc 1,
empty or non-JSON stdout, `Traceback (most recent call last)` on stderr.

| # | input element | verdict | exit | result |
|---|---|---|---|---|
| A00 | control: valid mode-2 set | COMMIT_OK | 0 | clean |
| A00b | control: Committed_AS 13990000 (inside band) | COMMIT_LOW | 1 | clean |
| A01 | meminfo empty file | COMMIT_UNKNOWN | 2 | clean (`meminfo: missing MemTotal,…`, 13 reading fields null) |
| A02 | meminfo whitespace-only | COMMIT_UNKNOWN | 2 | clean |
| A03 | `MemTotal: -16000000 kB` | COMMIT_UNKNOWN | 2 | clean |
| A04 | `MemTotal: 2**70 kB` | COMMIT_LOW | 1 | clean (`batch_pages 2147483647`, band 3.4e10) |
| A05 | leading spaces before `MemTotal:`, trailing spaces | COMMIT_UNKNOWN | 2 | clean |
| A06 | meminfo CRLF line ends | COMMIT_OK | 0 | clean |
| A07 | `16000000 KB` (upper-case unit) | COMMIT_UNKNOWN | 2 | clean |
| A08 | `MemTotal:\t16000000\tkB` | COMMIT_UNKNOWN | 2 | clean |
| A09 | the four required lines in reverse order | COMMIT_OK | 0 | clean |
| A10 | duplicate `Committed_AS` | COMMIT_UNKNOWN | 2 | clean (`appears twice`) |
| A11 | `Hugetlb` absent (optional) | COMMIT_OK | 0 | clean |
| A12 | 5000-digit `MemTotal` | — | 1 | **TRACEBACK** `ValueError: Exceeds the limit (4300 digits)…` |
| A13 | 4301-digit `MemTotal` (one past the limit) | — | 1 | **TRACEBACK** same |
| A14 | Arabic-Indic digits, UTF-8 bytes | COMMIT_UNKNOWN | 2 | clean (ASCII decode rejects) |
| A15 | NUL byte inside the `MemTotal` line | COMMIT_UNKNOWN | 2 | clean |
| A16 | `16000000kB` (no space) | COMMIT_UNKNOWN | 2 | clean |
| A17 | `+16000000` | COMMIT_UNKNOWN | 2 | clean |
| A18 | `16000000.0` | COMMIT_UNKNOWN | 2 | clean |
| A19 | `MemTotal` without colon | COMMIT_UNKNOWN | 2 | clean |
| B01 | `overcommit_memory` empty | COMMIT_UNKNOWN | 2 | clean |
| B02 | `overcommit_memory` = `-1` | COMMIT_UNKNOWN | 2 | clean |
| B03 | `overcommit_memory` = `2\n3` | COMMIT_UNKNOWN | 2 | clean |
| B04 | `overcommit_memory` = `2\r\n` | COMMIT_OK | 0 | clean |
| B05 | `overcommit_memory` = `  2  ` | COMMIT_OK | 0 | clean |
| B06 | `overcommit_memory` = `\t2\t` | COMMIT_OK | 0 | clean |
| B07 | `overcommit_memory` = `2**70` | COMMIT_UNKNOWN | 2 | clean (`is not a known policy`) |
| B08 | `overcommit_kbytes` = 5000 digits | — | 1 | **TRACEBACK** same ValueError |
| B09 | `overcommit_memory` = `3` | COMMIT_UNKNOWN | 2 | clean |
| B10 | `overcommit_memory` = `0x2` | COMMIT_UNKNOWN | 2 | clean |
| B11 | `overcommit_memory` = Arabic-Indic `2` | COMMIT_UNKNOWN | 2 | clean |
| B12 | `overcommit_ratio` = `2**70` | COMMIT_OK | 0 | clean (`limit_mismatch` finding) |
| C01 | `present` = `0-` | COMMIT_UNKNOWN | 2 | clean |
| C02 | `present` = `,` | COMMIT_UNKNOWN | 2 | clean |
| C03 | `present` = `00-03` | COMMIT_OK | 0 | clean (counted 4) |
| C04 | `present` empty | COMMIT_UNKNOWN | 2 | clean |
| C05 | `present` = `0-2,` | COMMIT_UNKNOWN | 2 | clean |
| C06 | `present` = `5-3` | COMMIT_UNKNOWN | 2 | clean |
| C07 | `present` = 5000 digits | — | 1 | **TRACEBACK** same ValueError |
| C08 | `present` = `0-3\r\n` | COMMIT_OK | 0 | clean |
| C09 | `present` = `0-1000000000` | COMMIT_LOW | 1 | clean, band 8000000016000000008 kB |
| C10 | `present` = `0-2,1-3` | COMMIT_OK | 0 | clean, cpus 6 (overlap double-counted) |
| C11 | `present` = Arabic-Indic `0-3` | COMMIT_UNKNOWN | 2 | clean |
| C12 | `present` = `0 -3` | COMMIT_UNKNOWN | 2 | clean |
| D01 | `--page-kb 0` | COMMIT_UNKNOWN | 2 | clean |
| D02 | `--page-kb -4` | COMMIT_UNKNOWN | 2 | clean |
| D03 | `--page-kb 3` | COMMIT_UNKNOWN | 2 | clean |
| D04 | `--page-kb 2**70` | COMMIT_LOW | 1 | clean, band 1.51e23 |
| D05 | `--page-kb` 5000 digits | COMMIT_UNKNOWN | 2 | clean (argparse `invalid int value`) |
| D06 | `--page-kb 2**200` | COMMIT_LOW | 1 | clean, band 2.06e62 |
| D07 | `--page-kb ""` | COMMIT_UNKNOWN | 2 | clean |
| D08 | `--page-kb ٤` (Arabic-Indic 4) | COMMIT_OK | 0 | clean, accepted as 4 |
| E01 | `--bogus` | COMMIT_UNKNOWN | 2 | clean (`usage: unrecognized arguments`) |
| E02 | `--meminfo` with no value | COMMIT_UNKNOWN | 2 | clean |
| E03 | meminfo path absent | COMMIT_UNKNOWN | 2 | clean |
| E04 | meminfo path is a directory | COMMIT_UNKNOWN | 2 | clean |
| E05 | `--vm-dir` is a regular file | COMMIT_UNKNOWN | 2 | clean |
| E06 | cpu-present path absent | COMMIT_UNKNOWN | 2 | clean |
| E12 | `--meminfo /dev/null` | COMMIT_UNKNOWN | 2 | clean |
| E13 | `--cpu-present /dev/null` | COMMIT_UNKNOWN | 2 | clean |
| E15 | meminfo chmod 000 | COMMIT_UNKNOWN | 2 | clean (`unreadable (Permission denied)`) |
| E07 | `--selftest --cases` absent | text FAIL | 1 | clean (no traceback) |
| E08 | `--selftest --cases` malformed JSON | text FAIL | 1 | clean (`cannot load cases`) |
| E09 | `--cases` case with `page_kb: 0` but incomplete vm set | text FAIL | 1 | clean (fails on the absent vm file first) |
| E10 | `--cases` case with `id: ../../escape`, incomplete | text FAIL | 1 | clean output — **but wrote outside the temp root** (see F3) |
| E11 | `--cases` case without `expect` | — | 1 | **TRACEBACK** `KeyError: 'expect'` |
| E14 | `--cases` `cases: ["nope"]` | — | 1 | **TRACEBACK** `TypeError: string indices must be integers` |

Totals: 68 cases; 58 valid JSON; 4 text-mode successes; **6 tracebacks**; 0 exit-code/verdict mismatches among
the 58 JSON outputs; 1 verdict differing from this seat's expectation (D08, F6). The seat's named families all
land as required: empty files A01/B01/C04, unicode digits A14/B11/C11 (rejected at the ASCII decode), negatives
A03/B02/D02, `2**70` A04/B07/D04, spaces A05/B05/B06, CRLF A06/B04/C08, `KB` A07, tabs A08/B06, reversed meminfo
A09, cpulists `0-` / `,` / `00-03` C01/C02/C03, `2\n3` B03 — except the integer-width family (F1).

## Table 2 — `--selftest --cases` shape probes (9 further inputs, all tracebacks)

Each case file is otherwise well formed (`meminfo`, full `vm`, `present 0-3`, `page_kb 4`, `expect_exit 0`,
`expect {"verdict":"COMMIT_OK"}`), one field mutated.

| probe | mutation | exit | stderr last line |
|---|---|---|---|
| S1 | `page_kb: 0` (complete vm set) | 1 | `ZeroDivisionError: division by zero` |
| S2 | `page_kb: "4"` | 1 | `TypeError: unsupported operand type(s) for //: 'int' and 'str'` |
| S3 | two cases with `id: "dup"` | 1 | `FileExistsError: [Errno 17] File exists: '…/mori-commit-runway-…/dup/vm'` |
| S4 | `expect` is a list | 1 | `AttributeError: 'list' object has no attribute 'items'` |
| S5 | `id: 7` (int) | 1 | `TypeError: join() argument must be str, bytes, or os.PathLike object, not 'int'` |
| S6 | `cases` is an object, not a list | 1 | `TypeError: string indices must be integers, not 'str'` |
| S7 | `vm: {"overcommit_memory": 2}` | 1 | `TypeError: write() argument must be str, not int` |
| S8 | `present: 4` | 1 | `TypeError: write() argument must be str, not int` |
| S9 | `meminfo: 5` | 1 | `TypeError: write() argument must be str, not int` |
| S10 | `TMPDIR=/proc/self/nonexistent` | 0 | none — tempfile falls back, `PASS 23/23` (not a defect; note it writes elsewhere than `$TMPDIR`) |

## Table 3 — extra probes

| probe | command | result |
|---|---|---|
| 4300-digit `MemTotal` (limit boundary) | `--meminfo fz/extra/mi4300 …` | COMMIT_OK path absent, `COMMIT_LOW` rc=1, clean; 4301 digits is the first failing width |
| 2 MB single junk line, no newline | `--meminfo fz/extra/mibig …` | `COMMIT_UNKNOWN` rc=2, 0.05 s — regex tail is not quadratic |
| 2 MB run of digits in the value | `--meminfo fz/extra/mibig2 …` | **TRACEBACK** in 0.08 s (same F1) |
| UTF-8 BOM before `MemTotal` | `--meminfo fz/extra/mibom …` | `COMMIT_UNKNOWN` rc=2 (`unreadable (UnicodeDecodeError)`) |
| real symlink loop | `ln -s ../extra/loop fz/extra/loop` | `COMMIT_UNKNOWN` rc=2, note `unreadable (Too many levels of symbolic links)` |
| FIFO with no writer | `--meminfo fz/extra/fifo …` under `timeout 3` | **blocked**, `timeout` rc 124, no output (F7) |
| `Hugetlb` > `MemTotal` | `Hugetlb: 99999999999 kB`, mode 2 | `COMMIT_LOW` rc=1, `limit_recomputed_kb -74988000000`, findings `limit_mismatch, inside_band` — no crash, drift visible |
| committed fixtures sanity | `cases.json` | 23 cases, ids unique, `page_kb` ∈ {4, 64}, longest digit run 8 — none of the landed fixtures can reach F1 |

## Evidence (literal)

F1, meminfo surface:

```
$ cd /fast/scratch/hyaku/mori-r53/Mo53SentC2Hostile && TMPDIR=$PWD/tmp \
  python3 -I -B /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-commit-runway.py \
    --meminfo fz/A12-5000digits/meminfo --vm-dir fz/A12-5000digits/vm --cpu-present fz/A12-5000digits/present
Traceback (most recent call last):
  File "/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-commit-runway.py", line 316, in <module>
    sys.exit(main())
  File ".../mori-commit-runway.py", line 310, in main
    out, code = evaluate(a.meminfo, a.vm_dir, a.cpu_present, page_kb)
  File ".../mori-commit-runway.py", line 146, in evaluate
    mi = parse_meminfo(_read(meminfo_path))
  File ".../mori-commit-runway.py", line 107, in parse_meminfo
    vals[key] = int(kb.group(1))
ValueError: Exceeds the limit (4300 digits) for integer string conversion: value has 5000 digits; use
sys.set_int_max_str_digits() to increase the limit
rc=1
```

F1, vm surface (tail): `File ".../mori-commit-runway.py", line 133, in parse_vm_value / return int(t)` →
same `ValueError`, rc=1. F1, cpulist surface (tail): `line 122, in parse_cpulist /
a, b = int(lo), int(hi) if hi else int(lo)` → same `ValueError`, rc=1.

F2, `--cases` shapes: `--selftest --cases fz/noexpect.json` →
`line 229, in _mismatches / for key, want in case["expect"].items() / KeyError: 'expect'`, rc=1, stdout empty;
`--selftest --cases fz/strcase.json` → `line 208, in _materialise / d = os.path.join(root, case["id"]) /
TypeError: string indices must be integers, not 'str'`, rc=1, stdout empty.

F3, traversal write (complete case, so the selftest *succeeds* while writing outside its root):

```
$ python3 -I -B …/mori-commit-runway.py --selftest --cases fz/trav2.json   # case id "../../escape2"
MATCHER: rejected 1/1 corrupted expectations
MORI_COMMIT_RUNWAY_SELFTEST: PASS 1/1
rc=0
$ ls -la escape2 escape2/vm     # $TMPDIR/mori-commit-runway-*/../../
-rw-r--r-- 1 vgpnk vgpnk 140 meminfo      -rw-r--r-- 1 vgpnk vgpnk 4 present
vm/: admin_reserve_kbytes overcommit_kbytes overcommit_memory overcommit_ratio user_reserve_kbytes
$ ls -la tmp                    # the mkdtemp root was removed; the escaped tree survives
total 0
```

Absolute `id` behaves the same because `os.path.join(root, "/abs/path")` discards `root`
(`--selftest --cases fz/trav3.json` with `id: /fast/scratch/…/abs-escape` → `PASS 1/1`, rc=0, tree written at
`abs-escape/`). Note `E10` in table 1 is the same escape with an incomplete case: the tree is still created, then
the case fails on the absent vm file.

Fail-closed sample (A01): `rc=2`, `{"verdict":"COMMIT_UNKNOWN", …}`, all 13 reading fields `null`,
`findings []`, `notes ["meminfo: missing MemTotal,SwapTotal,CommitLimit,Committed_AS"]`.

## Findings

1. **HIGH — F1: any numeric field wider than 4300 digits aborts the frozen reading interface with a traceback.**
   `tools/mori-commit-runway.py` lines 107 (`parse_meminfo`), 122 (`parse_cpulist`), 133 (`parse_vm_value`):
   `int()` on a digit string raises `ValueError: Exceeds the limit (4300 digits)…` on CPython ≥ 3.11 (host
   3.14.8) and `evaluate()` catches only `InputError`. Result: rc 1, empty stdout, no JSON — a contract
   violation of the docstring's "Anything required missing, unreadable or malformed … `COMMIT_UNKNOWN`, exit 2"
   and of the seat's "never a traceback". Reachable through all three frozen path arguments (`--meminfo` any
   required/optional line, `--vm-dir` any of the five files, `--cpu-present`), e.g. a truncated/garbled or
   hostile file; not reachable from the 23 landed fixtures (longest digit run 8). Exploit path: a seat or reader
   pointed at a corrupt meminfo gets rc 1 and no verdict instead of `COMMIT_UNKNOWN`, so a wrapper that keys on
   the JSON breaks. Smallest remediation for the L1 (data, not counter): wrap the three conversions in
   `try/except ValueError -> raise InputError(...)`, and cap the accepted width (≥ 20 digits is already
   impossible for an unsigned long) so the tool stays fail-closed rather than growing unbounded bignums.
2. **HIGH — F2: the `--selftest --cases` file is trusted; eleven malformed shapes traceback.**
   `_materialise` (207–222), `_mismatches` (225–238), `selftest` (246–276) index `case["id"]`, `case.get("vm")`,
   `case.get("present")`, `case.get("page_kb")` and `case["expect"]` without validation and `os.makedirs` without
   `exist_ok`. Inputs S1–S9, E11, E14 → rc 1, stdout empty, `ZeroDivisionError` / `FileExistsError` /
   `AttributeError` / `TypeError` / `KeyError`. This option is outside the frozen interface and no round-53
   receipt uses it, so C2's 80/80 is untouched; it is nonetheless a user-facing option (`--help` documents it)
   and the only place the tool writes to disk. Remediation: one shape guard per case (`isinstance(case, dict)`,
   `case.get("expect")` dict, `page_kb` positive int, `id` a single path segment) → `FAIL <id>: malformed case`,
   exit 1, no traceback.
3. **MED — F3: arbitrary-path write from a `--cases` case id (path traversal + absolute override).**
   Line 208 `d = os.path.join(root, case["id"])` with `root = tempfile.mkdtemp(...)`; `../../escape2` resolved to
   `$TMPDIR/../escape2` and an absolute id resolved to itself, both outside `root`, both written, both left behind
   after `shutil.rmtree(root)` — while printing `PASS 1/1`, rc 0. Same-uid write only, no privilege boundary
   crossed, and the attacker must supply the cases file, hence MED not HIGH. Remediation: reject ids containing
   `/`, `\` or `..` (and non-str ids) before `os.path.join`.
4. **LOW — F4: no plausibility ceiling on `present` CPUs or `--page-kb`, so impossible inputs produce the alarm
   verdict.** `present: 0-1000000000` → `cpus_present 1000000001`, `band_kb 8000000016000000008`,
   `COMMIT_LOW`/exit 1 (C09); `--page-kb 2**70` / `2**200` pass the power-of-two gate and give `COMMIT_LOW` with
   bands of 1.5e23 / 2.1e62 kB (D04/D06). No crash; the concern is calibration — `COMMIT_LOW` is the only alarm
   surrogate the tool has while FR8 is open, and here it fires from garbage. Worth a ceiling in the same edit as
   F1 (cpus ≤ some multiple of `INT_MAX`, page ≤ 1 MiB), or an explicit note in the docstring.
5. **LOW — F5: overlapping CPU ranges are counted twice.** `0-2,1-3` → `cpus_present 6`, `batch_pages 2604`
   instead of 4/3906 (C10). The kernel's cpumask printing never emits overlaps, so this is an input-shape
   assumption the docstring ("a CPU list such as `0-31` or `0,2-5`") does not state; a hostile or hand-written
   list silently enlarges the band by 50 % instead of `COMMIT_UNKNOWN`.
6. **LOW — F6: non-ASCII decimal digits are accepted on the `--page-kb` argument only.** `--page-kb ٤` →
   `COMMIT_OK`, page 4 (D08), because `argparse`'s `int()` accepts Unicode digits while `_read()` decodes every
   file as ASCII and `parse_vm_value`'s `\d+`/`parse_cpulist`'s `\d` are therefore never reached with non-ASCII
   input in practice. Inconsistent validation; the value is harmless, but the ASCII-only stance is not enforced
   where it is cheapest to enforce (an `re.fullmatch(r"[0-9]+")` before `int` in the argument handling).
7. **LOW — F7: the input files are read whole and without a timeout.** `_read` (84–92) does `f.read()` at line 87 with no
   size cap, and `open()` on a FIFO blocks forever: `--meminfo fz/extra/fifo` under `timeout 3` returned rc 124
   with no output. A 2 GB meminfo would be loaded into memory before the first regex. Operator-chosen path and
   read-only, so LOW; the smallest guard is a `st_size`/`S_ISREG` check in `_read`.

### Round-54 routed item (not a round-53 defect)

The frozen counter `count-c2.py` transforms the same fields with the same unguarded `int()` —
`int(v.group(1))` (line 72), `int(a), int(b)` (line 86), `int(t)` (line 95) — so REF carries the identical
4300-digit exposure [INFERENCE: static reading of the frozen file plus CPython semantics; REF was not executed
with a hostile input, and its 80 fixture legs use ≤ 8-digit values, so C2's `agree=80 disagree=0` is unaffected].
The counters are frozen; this belongs in round 54's mutation/robustness list, not in this round's fix set.

### What this seat did not check

No concurrency, no cgroup or namespace variant, no `/dev/zero` or multi-GB read (deliberately not triggered —
F7 is demonstrated by the FIFO block only), no kernel-semantics check of the batch or band rule (another seat
owns independent recomputation), no REF-versus-kernel recomputation, no mutation of the tool (data correction is
the L1's). The four tracebacks in F1 are the only observations this seat offers that are invisible to the
fixtures; none of them alters the C2 reading of the landed data.

Report: .ufo/waves/round-53/w1/Mo53SentC2Hostile.md
