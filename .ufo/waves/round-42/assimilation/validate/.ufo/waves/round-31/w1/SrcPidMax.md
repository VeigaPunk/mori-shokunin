# S173 — Linux v7.2 `Documentation/admin-guide/sysctl/kernel.rst` (source scout report)

Seat: MoriR31.SrcPidMax. Question: do the saved bytes carry that `pid_max` means PIDs wrap and are
reused, so a pid alone is not identity over time?

Short answer: the bytes carry the **wrap** and the **bounded range** verbatim; they never use the
words "reuse" or "identity" (`grep -c -i` → 0 each). Admit is scoped to the wrap mechanism, and the
identity conclusion must be marked as drawn from it, not quoted from it.

## 1. Fetch

| field | value |
|---|---|
| URL | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/sysctl/kernel.rst |
| access time (UTC) | 2026-10-22T23:43:06Z (recorded `date -u +%FT%TZ` immediately before the fetch, same command) |
| HTTP | 200, no redirect (`curl -w` returned `code=200 effective=https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/sysctl/kernel.rst size=58820`) |
| bytes | 58820 (1736 lines); content type `text/plain; charset=utf-8` (`file -i`) |
| saved unchanged | /fast/scratch/hyaku/mori-r31/SrcPidMax/S173.src |
| sha256 | `e9baf759b3eac6b58d893638280e9924fec46a8814169b224bbf9ae7f7fd4a32` |
| challenge scan | 0 hits for `<!doctype`, `<html`, `captcha`, `cloudflare` (`grep -c -i`) — real RST, not a challenge page |
| identity check | refetch at 2026-10-22T23:44:15Z is byte-identical (`cmp -s` clean, same sha256, same 58820 bytes) — the counter's own refetch-and-hash step will pass |
| document identity | S173.src:1-3 `=====` / `Documentation for /proc/sys/kernel/` / `=====`; S173.src:5 `.. See scripts/check-sysctl-docs to keep this up to date` |

## 2. Located quotes (verbatim from the saved bytes)

Line numbers are from `awk 'NR==n{print NR"|"$0}'` and `grep -n` on S173.src.

### Q1 — S173.src:1084-1085 (21 words, `wc -w`)

> PID allocation wrap value.  When the kernel's next PID value
> reaches this value, it wraps back to a minimum PID value.

(The gap after `value.` is two spaces in the file; the counter collapses whitespace runs
(`norm`, count-c1.py:42-43), so the pasted row matches either way.)

Fact it supports: the kernel allocates PIDs from a wrapping counter, so on reaching `pid_max` the
next number comes from the bottom of the range again — a number seen at one time can be handed out
later to a different process. This is the source's own statement of the mechanism; the step to "not
identity" is [INFERENCE] and must not be attributed to the quote.

### Q2 — S173.src:1086 (9 words, `wc -w`)

> PIDs of value ``pid_max`` or larger are not allocated.

Fact it supports: the number space is bounded, so reuse is structural (a finite set of numbers
against an unbounded stream of forks), not a rare collision.

### Q3 — S173.src:1092-1093 (17 words, `wc -w`), section `ns_last_pid` (heading S173.src:1089)

> The last pid allocated in the current (the one task using this sysctl lives in) pid namespace.

Fact it supports: allocation resumes from one advancing per-namespace cursor, so the numbers a probe
sees are issued by that cursor in sequence and re-enter the low range after the wrap; two probes at
different times can legitimately see the same number for different processes.

Together: a pid number match across two observations is not evidence of the same process, and the
page gives no method to tell a reissued number from the original (no start time, no boot id, no
namespace id is discussed there — those are other seats' sources).

## 3. Ready-to-paste rows

Gate row for `corpus/lessons/round-31.md` (one https URL, 64-hex sha in backticks, three
`(N words): "quote"` items, last cell starts `admit`):

```
| S173 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/sysctl/kernel.rst | 2026-10-22T23:43:06Z | `e9baf759b3eac6b58d893638280e9924fec46a8814169b224bbf9ae7f7fd4a32` | `kernel.rst:1084-1085` (21 words): "PID allocation wrap value.  When the kernel's next PID value reaches this value, it wraps back to a minimum PID value."; `kernel.rst:1086` (9 words): "PIDs of value ``pid_max`` or larger are not allocated."; `kernel.rst:1092-1093` (17 words): "The last pid allocated in the current (the one task using this sysctl lives in) pid namespace." | admit, A, mined |
```

SOURCES row for `corpus/SOURCES.md` (column order copied from SOURCES.md:5, 11 columns):

```
| S173 | Linux kernel parameters — /proc/sys/kernel/ pid_max allocation wrap v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/sysctl/kernel.rst | docs | A | the pid_max and ns_last_pid entries of the /proc/sys/kernel/ documentation: the allocation wrap at pid_max back to a minimum PID value, the statement that PIDs of value pid_max or larger are not allocated, and that the next pid is allocated starting from the pid namespace's last allocated pid; these wrap semantics only, not the pid_max default or the PID_MAX_LIMIT ceiling, not reuse detection and not any probe procedure | pid_max:1081-1086; ns_last_pid:1089-1094; tag v7.2; sha256 e9baf759b3eac6b5 | PID numbers come from a bounded, wrapping allocator, so after the wrap a number is handed out again: a matched pid number is not identity over time (the page states the wrap; the identity conclusion is drawn from it), and the page offers no way for a probe to tell a reissued number from the original. | mined | 2026-10-22 | on-release | corpus/knowledge/watchdog-identity-r31.md |
```

Suggested decision-table row (4 cells, no inner pipes; adapt the verdict wording to the entry's own
vocabulary — the counter needs exactly `len(row) == len(header)` and `S173` in the sources cell):

```
| A pid number matched across two observations, with no start-time or boot-id comparison | The allocator is bounded by pid_max and wraps back to a minimum PID value, so a number is handed out again after the wrap (`kernel.rst:1084-1086`) | not identity — the number match cannot separate the original process from a later holder of the same number | S173 |
```

Copy for the L1 (the counter compares this file's sha256 to the Gate sha and checks every quote is
contained in it, count-c1.py:154-156):

```sh
mkdir -p corpus/evidence/sources-r31
cp /fast/scratch/hyaku/mori-r31/SrcPidMax/S173.src corpus/evidence/sources-r31/S173.src
sha256sum corpus/evidence/sources-r31/S173.src   # expect e9baf759b3eac6b58d893638280e9924fec46a8814169b224bbf9ae7f7fd4a32
```

### Format check with the counter's own parser

Validated by importing `count-c1.py` and calling its functions on the rows above (not a re-typed
parser):

- `cells(gate_row)` → 6 cells, last one `admit, A, mined` (`startswith('admit')` true); exactly one
  cell starts `https://`; the single backticked 64-hex sha equals `sha256sum S173.src`; 3 quotes
  parsed, word counts 21/9/17, each `norm()`-contained in the saved copy.
- SOURCES row parses to 11 columns; the suggested decision row to 4 cells whose sources cell
  resolves to `S173`.
- `cells()` strips one outer pipe on each side before splitting (count-c1.py:34-38), so the binding
  trailing-pipe row shape is safe; a naive `split('|')` would have made the last cell empty and the
  row invisible as an admit. The frozen control fixture at rev `9d91f953` reproduces `admits=1`
  under the same parser, so the shape is the one the receipt was scored with.

## 4. Decision

**Admit**, scoped to the wrap mechanism. Reasons, checked against the assignment's reject tests:

- The fact's first clause is carried verbatim: "it wraps back to a minimum PID value"
  (S173.src:1085), plus the bound "PIDs of value ``pid_max`` or larger are not allocated"
  (S173.src:1086). Reuse follows from the wrap the page itself describes.
- The fact's last clause ("a pid alone is not identity over time") is **not** a sentence in the
  page: `grep -c -i reuse` → 0, `grep -c -i identity` → 0, `grep -ci recycl` → 0. The row's
  `teaches` and any entry reading built on it must label that step as inference. If the L1 prefers
  quotes-only rows, keep the id for the wrap/bound cells and let a code source (S164/S167, other
  seats) carry the identity claim.
- The page does not state `pid_max`'s default or ceiling: no `PID_MAX_LIMIT`, no `4194304`, and the
  only `32768` in the file is a taint bit (S173.src:1558, "(K) kernel has been live patched"). Do
  not source a numeric ceiling from S173.
- No 404 and no challenge page: HTTP 200, 58820 bytes, RST with the `check-sysctl-docs` marker
  (S173.src:5).
- Not a duplicate: `grep -n 'sysctl' corpus/SOURCES.md` → no matches; `grep -n 'S173'` → no
  matches; `grep -n 'admin-guide'` matches only docs.kernel.org pages (S002, S033) and other v7.2
  docs paths (S077, S083, S092, S094) — none is this URL. 24 SOURCES.md lines contain the
  `https://raw.githubusercontent.com/torvalds/linux/v7.2` prefix, none with `sysctl/kernel.rst`
  (`grep -c` on the prefix, then `grep -n 'sysctl'` → 0).
- Format fit: one https URL, one 64-hex backticked sha, three quotes of 21/9/17 words (all ≤ 25 by
  `wc -w`), each present in the saved bytes after whitespace collapse (checked in Python with the
  counter's `norm`), no `"`, `|` or `\` inside any quote so no escaping is needed.

Remaining unknowns: none for this id. Whether the fleet watchdog's own probe would survive a wrap
is a probe-design question (start time from `/proc/<pid>/stat`, boot id), owned by other seats, not
by S173.

## Bounds and tooling

- Files written: this report and `/fast/scratch/hyaku/mori-r31/SrcPidMax/{S173.src,access-time.txt}`.
  No lane file written besides this report; no unit started or signalled; no pacman run. Read-only
  git only, outside the lane: `git -C /fast/scratch/hyaku/mori-r31/c1-controls status/log` plus the
  `git show` calls the imported counter makes against that same sandbox; nothing in the lane or the
  fleet repo touched, `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` unset on my own git calls.
- No tool installed or updated; nothing needed one. `curl 8.23.0`, `Python 3.14.8`, `sha256sum 0.8.0`,
  `file`, `grep`, `awk`, `wc`, `cmp`, `od` were already present.
- Processes: every command bounded by `timeout` and `curl -m 60`; nothing left running.
- Privacy: no uid, real pid, unit name, journal text, settings value or session path in this report.

Report: .ufo/waves/round-31/w1/SrcPidMax.md
