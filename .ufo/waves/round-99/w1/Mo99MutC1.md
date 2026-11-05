# Mo99MutC1 — mutation test: `tools/mori-userns-runway.py` vs frozen `count-c1.py`

Seat: Mo99MutC1 (mori r99 w1, mutation-tester). Date: 2026-11-05. Landing `5013f0be8ac9e7fce3c08b680e43cf9cbd49620d`; entering `73308ff6e5c933f53498e9501ef95917b0ef7171`; freeze `462cef1cc637de4c6e993aefd00ed9df32895984`.

## Method

- Landing tree exported read-only: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin archive 5013f0be8ac9e7fce3c08b680e43cf9cbd49620d | tar -x -C $S/base`. Baseline tool sha256 `4ef3108f171dc5fa0b42c8dc1cf4f374cb223ab0bb9411c1e992e255e46abc0b`.
- 37 single-point mutants, one tree each: `shutil.copytree(base, symlinks=True, copy_function=os.link)`, tool file `os.unlink`ed then rewritten (base inode untouched; sha re-verified after all runs). Every mutation pattern matched exactly once in the pristine file (asserted before writing).
- Detector per mutant, twice: `python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-99/count-c1.py --root <mutant tree> --work $S/work/<mutant>-s<N> --seed 7` and `--seed 8` (TMPDIR=$S). 74 mutant runs + 2 baselines. SURVIVED = `C1=met` on both seeds.
- Every survivor was probed with a distinguishing journal line (or fake-/proc fixture) run through base and mutant tool; the four claimed-equivalent survivors additionally ran a 27-shape corpus plus the full incident capture `journal-incident-r99.txt` with byte-identical output and rc.

## Baseline (pristine landing)

```
seed 7: rc=0 C1=met cases_ok=60/60 seed=7 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
seed 8: rc=0 C1=met cases_ok=60/60 seed=8 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
```

## Verdicts (37 mutants)

| # | mutant | area | sha256 (mutated tool) | seed 7 | seed 8 | failing cases | killer check(s) | classification |
|---|--------|------|----------------------|--------|--------|---------------|-----------------|----------------|
| 1 | `esc-177-off` | unescape_cntrl #0177 branch | `c1625772d195fa0e…` | met 60/60 | met 60/60 | - | - | equivalent (B1) |
| 2 | `esc-2digit-off` | unescape_cntrl 2-digit branch | `0762e6cf45fd403f…` | unmet | unmet | W7-sudo-escape-0, W7-sudo-escape-1, W7-sudo-escape-2 | selftest,battery | killed |
| 3 | `esc-2digit-bound` | unescape_cntrl 2-digit bound 0o40→0o20 | `cbe81bbe77c85c1b…` | met 60/60 | met 60/60 | - | - | equivalent (B2) |
| 4 | `esc-1digit-off` | unescape_cntrl 1-digit branch | `e414a5be7ae6a4df…` | met 60/60 | met 60/60 | - | - | GAP G1 |
| 5 | `split-unesc-dropped` | split_cmd unescape_cntrl call | `66a41645d9391ed1…` | unmet | unmet | W7-sudo-escape-0, W7-sudo-escape-1, W7-sudo-escape-2 | selftest,battery | killed |
| 6 | `split-quote-mode-off` | split_cmd quoted-arg mode | `01ef2a4efb09139e…` | unmet | unmet | R1-quoted-0, R1-quoted-1, R1-quoted-2, R2-comment-0, R2-comment-1, R2-comment-2, S1-short-format-0, S1-short-format-1, S1-short-format-2, W2-sh-echo-0, W2-sh-echo-1, W2-sh-echo-2, W3-tee-a-0, W3-tee-a-1, W3-tee-a-2, W4-sh-sysctl-0, W4-sh-sysctl-1, W4-sh-sysctl-2, W6-printf-fd-0, W6-printf-fd-1, W6-printf-fd-2, W7-sudo-escape-0, W7-sudo-escape-1, W7-sudo-escape-2, W8-continued-0, W8-continued-1, W8-continued-2 | selftest,battery,incident | killed |
| 7 | `split-unterminated-no-raise` | split_cmd unterminated-quote raise | `9df42b15047443fa…` | unmet | unmet | S3-truncated-0, S3-truncated-1, S3-truncated-2 | selftest,battery | killed |
| 8 | `split-backslash-off` | split_cmd backslash unescape | `7eec427f095d3053…` | met 60/60 | met 60/60 | - | - | GAP G2 |
| 9 | `split-quoted-none-false` | split_cmd quoted=None→False | `43a20a31dad074d4…` | met 60/60 | met 60/60 | - | - | equivalent (B3) |
| 10 | `exit-suffix-never` | EXIT_SUFFIX_RE never-match | `dc46f899a4a5da87…` | unmet | unmet | R4-exit-event-0, R4-exit-event-1, R4-exit-event-2 | selftest,battery | killed |
| 11 | `exit-suffix-exit-only` | EXIT_SUFFIX_RE drops SIGNAL | `7ae04b24291f69d5…` | met 60/60 | met 60/60 | - | - | GAP G3 |
| 12 | `tok-comment-off` | shell_tokens comment skip | `dfa8cb182c63abf4…` | unmet | unmet | R2-comment-0, R2-comment-1, R2-comment-2 | selftest,battery | killed |
| 13 | `tok-dquote-off` | shell_tokens double-quote grouping | `e9cbf3f6ed392b27…` | unmet | unmet | R1-quoted-0, R1-quoted-1, R1-quoted-2 | selftest,battery | killed |
| 14 | `tok-glued-fd-no-pop` | shell_tokens glued fd pop | `2455c8281345427b…` | met 60/60 | met 60/60 | - | - | GAP G4 |
| 15 | `tok-ops-gt-first` | shell_tokens OPS order > before >> | `2e24626aacb2e34f…` | unmet | unmet | W6-printf-fd-0, W6-printf-fd-1, W6-printf-fd-2 | battery | killed |
| 16 | `tok-single-quote-self-find` | shell_tokens single-quote find(i) | `58fefb7e56bb61b1…` | met 60/60 | met 60/60 | - | - | GAP G5 |
| 17 | `echo-flag-E-off` | echo_value -E flag skip | `9c4fa7b1919b0853…` | met 60/60 | met 60/60 | - | - | GAP G6 |
| 18 | `echo-value-include-exe` | echo_value scans exe | `59e5bba1e9c1605a…` | unmet | unmet | S1-short-format-0, S1-short-format-1, S1-short-format-2, W2-sh-echo-0, W2-sh-echo-1, W2-sh-echo-2, W3-tee-a-0, W3-tee-a-1, W3-tee-a-2, W6-printf-fd-0, W6-printf-fd-1, W6-printf-fd-2, W7-sudo-escape-0, W7-sudo-escape-1, W7-sudo-escape-2, W8-continued-0, W8-continued-1, W8-continued-2 | selftest,battery,incident | killed |
| 19 | `sysctl-pattern-no-skip` | sysctl_writes -r/--pattern skip | `ee70b9df8ae0cd53…` | unmet | unmet | R3-pattern-0, R3-pattern-1, R3-pattern-2 | selftest,battery | killed |
| 20 | `sysctl-f-alias-off` | sysctl_writes -f alias | `8dc2bd5c40d76625…` | met 60/60 | met 60/60 | - | - | GAP G7 |
| 21 | `sysctl-pfile-glued-off` | sysctl_writes glued -pFILE/-fFILE | `f758330a9c812844…` | unmet | unmet | - | selftest | killed |
| 22 | `sysctl-system-off` | sysctl_writes --system | `8f3d44a07cd6cd3a…` | met 60/60 | met 60/60 | - | - | GAP G8 |
| 23 | `cw-tee-prefix-loose` | command_writes tee /proc/sys prefix | `d0b9698fc1b369d1…` | met 60/60 | met 60/60 | - | - | GAP G9 |
| 24 | `cw-nested-depth-1` | command_writes nesting depth<3→<1 | `27b26e777c1b60b9…` | met 60/60 | met 60/60 | - | - | GAP G10 |
| 25 | `cw-via-sh-echo-off` | command_writes via= label | `940e6782fe548220…` | met 60/60 | met 60/60 | - | - | DETECTOR GAP G11 |
| 26 | `cw-redir-lt-recorded` | script_writes '<' recorded as write | `6c4be53917e9e5cf…` | met 60/60 | met 60/60 | - | - | GAP G12 |
| 27 | `scan-cont-replace` | scan_journal continuation replace-not-append | `038fb04b47059957…` | unmet | unmet | W8-continued-0, W8-continued-1, W8-continued-2 | selftest,battery | killed |
| 28 | `scan-cont-marker-short` | scan_journal continuation marker | `6acfdc4802961965…` | met 60/60 | met 60/60 | - | - | GAP G13 (+crash) |
| 29 | `scan-orphan-ignored` | scan_journal orphan continuation | `e354816c5bcb6fdb…` | met 60/60 | met 60/60 | - | - | GAP G14 |
| 30 | `scan-unknown-ts-skip` | scan_journal unknown-ts unparsed | `926e672be2ee5fd0…` | unmet | unmet | S2-unknown-ts-0, S2-unknown-ts-1, S2-unknown-ts-2 | battery | killed |
| 31 | `scan-unparsed-swallow` | scan_journal Unparsed swallow | `e3704052f1f402bf…` | unmet | unmet | S3-truncated-0, S3-truncated-1, S3-truncated-2 | battery | killed |
| 32 | `report-exit2-off` | journal_report exit-2 branch | `42ec3e309162b803…` | unmet | unmet | S2-unknown-ts-0, S2-unknown-ts-1, S2-unknown-ts-2, S3-truncated-0, S3-truncated-1, S3-truncated-2 | selftest,battery | killed |
| 33 | `ts-short-day-2digit` | TS_SHORT_RE day \d{1,2}→\d\d | `8345825ad8d3047d…` | met 60/60 | met 60/60 | - | - | GAP G15 |
| 34 | `runway-clamp-off` | runway clamp max(…,0) | `cced79b46d94f809…` | unmet | unmet | runway-00-over, runway-01-over, runway-02-zero, runway-03-any, runway-04-any | selftest,battery | killed |
| 35 | `runway-init-counted` | runway init-inode filter | `5febaea5a0efe9f7…` | unmet | unmet | runway-00-over, runway-01-over, runway-02-zero, runway-03-any, runway-04-any, runway-05-any, runway-06-any, runway-07-any, runway-08-any, runway-09-any, runway-10-any, runway-11-any | selftest,battery,live | killed |
| 36 | `runway-low-le` | runway low boundary <→<= | `8d5c4dabc15ac032…` | met 60/60 | met 60/60 | - | - | GAP G16 |
| 37 | `classify-guard-off` | classify empty-argv guard | `f1b8a3dc6cda5698…` | met 60/60 | met 60/60 | - | - | equivalent (B4) |

Full sha256 values and raw counter final lines for every run are in the appendix. Mutation score: **17/37 killed (46%)**, 4 equivalent survivors, 16 gap survivors. Verdicts identical on seed 7 and seed 8 for all 37 mutants (runway-clamp-off failed a different case subset per seed, same verdict).

## Equivalent survivors (proofs + differential test)

- **`esc-177-off`** — corpus diffs=0 over 2 comparison runs each (27-shape corpus + full incident). Proof B1: the only reachable input is the literal `#0177`; the deleted branch would emit DEL, the fall-through 2-digit branch emits `\x0f` plus literal `7`. Both land a control char (mutant: plus a stray digit) inside the same shell word: never an operator, quote, `#` word-start, ECHO-class exe, or SAFE_VALUE match — key/value/via/count/rc unchanged on every input.
- **`esc-2digit-bound`** — corpus diffs=0 over 2 comparison runs each (27-shape corpus + full incident). Proof B2: for `#020`–`#037` the narrowed bound makes the escape fall to the 1-digit branch, emitting `\x02`/`\x03` plus a stray digit in the same word slot; as in B1 the word stays non-operator/non-quote/non-`#`/non-ECHO and fails SAFE_VALUE identically, so the output cannot differ.
- **`split-quoted-none-false`** — corpus diffs=0 over 2 comparison runs each (27-shape corpus + full incident). Proof B3: `quoted` is set to `None` only at the quote-close and read only in boolean contexts (`if quoted:`, `if quoted and c == "'"`); `False` is falsy exactly like `None`, so every branch takes the same path.
- **`classify-guard-off`** — corpus diffs=0 over 2 comparison runs each (27-shape corpus + full incident). Proof B4: for `argv == []`, `command_writes([], [], None, 0)` computes `exe = ""`, iterates no redirs, matches no exe branch, returns `[]` — identical to the removed guard; `unwrap([])` is also `[]`.

## Battery / detector gaps (16 surviving mutants, each with a verified distinguishing input)

None of these inputs is planted by the 16 journal families or the 12 runway cases at seeds 7/8, so the frozen battery scores each mutant `C1=met 60/60`:

- **G1 `esc-1digit-off`** — sudo line: `COMMAND=/usr/bin/sh -c '#07 echo 0 > /proc/sys/user/max_user_namespaces'` — with the 1-digit branch `#07` decodes to BEL (plain word); without it the literal `#07` at word start becomes a comment (XCU 2.3) and swallows the write.
  - input: `T h sudo[1]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/sh -c '#07 echo 0 > /proc/sys/user/max_user_namespaces'`
  - base rc=1: `SYSCTL_WRITE ts=T pid=1 key=user.max_user_namespaces value=- via=sh-redirect ⏎ SYSCTL_WRITES n=1 keys=1 userns_zero=0`
  - mut  rc=0: `SYSCTL_WRITES n=0 keys=0 userns_zero=0`
- **G2 `split-backslash-off`** — sudo line: `COMMAND=/usr/bin/sh -c 'echo 0 > /proc/sys/vm.swappiness\\x'` (raw `\\` = sudo-escaped literal backslash). Base decodes to `\` and shell-tokens it away → key `vm.swappinessx`; mutant keeps `\\` → key `?`.
  - input: `T h sudo[2]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/sh -c 'echo 0 > /proc/sys/vm.swappiness\\x'`
  - base rc=1: `SYSCTL_WRITE ts=T pid=2 key=vm.swappinessx value=0 via=sh-echo ⏎ SYSCTL_WRITES n=1 keys=1 userns_zero=0`
  - mut  rc=1: `SYSCTL_WRITE ts=T pid=2 key=? value=0 via=sh-echo ⏎ SYSCTL_WRITES n=1 keys=1 userns_zero=0`
- **G3 `exit-suffix-exit-only`** — sudo line: `COMMAND=/usr/bin/sysctl -w user.max_user_namespaces=0 ; SIGNAL=KILL`. `SIGNAL=` exit events are never planted (R4 uses `EXIT=` only); the mutant classifies the exit event, double-counting the write and inventing a `SIGNAL=KILL` sysctl write.
  - input: `T h sudo[3]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/sysctl -w user.max_user_namespaces=0 ; SIGNAL=KILL`
  - base rc=0: `SYSCTL_WRITES n=0 keys=0 userns_zero=0`
  - mut  rc=1: `SYSCTL_WRITE ts=T pid=3 key=user.max_user_namespaces value=0 via=sysctl ⏎ SYSCTL_WRITE ts=T pid=3 key=SIGNAL value=KILL via=sysctl ⏎ SYSCTL_WRITES n=2 keys=2 userns_zero=1`
- **G4 `tok-glued-fd-no-pop`** — sudo line: `COMMAND=/usr/bin/sh -c 'echo 0>/proc/sys/user/max_user_namespaces'` (glued fd digits). Base pops the fd digit → `value=-`; mutant treats `0` as echo's argument → `value=0`, flipping `userns_zero`.
  - input: `T h sudo[4]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/sh -c 'echo 0>/proc/sys/user/max_user_namespaces'`
  - base rc=1: `SYSCTL_WRITE ts=T pid=4 key=user.max_user_namespaces value=- via=sh-echo ⏎ SYSCTL_WRITES n=1 keys=1 userns_zero=0`
  - mut  rc=1: `SYSCTL_WRITE ts=T pid=4 key=user.max_user_namespaces value=0 via=sh-echo ⏎ SYSCTL_WRITES n=1 keys=1 userns_zero=1`
- **G5 `tok-single-quote-self-find`** — sudo line: `COMMAND=/bin/sh -c 'echo \'x > /proc/sys/user/max_user_namespaces'` — unterminated single quote inside the `-c` script (the r98 dropped-continuation shape). Base fails closed (rc 2, `unparsed=1`); mutant silently tokenizes and emits a write (rc 1): a fail-closed regression the battery cannot see.
  - input: `T h sudo[15]:    u : PWD=/x ; USER=root ; COMMAND=/bin/sh -c 'echo \'x > /proc/sys/user/max_user_namespaces'`
  - base rc=2: `SYSCTL_WRITES n=0 keys=0 userns_zero=0 ⏎ SYSCTL_WRITES_SETUP unparsed=1`
  - mut  rc=1: `SYSCTL_WRITE ts=T pid=15 key=user.max_user_namespaces value=x via=sh-echo ⏎ SYSCTL_WRITES n=1 keys=1 userns_zero=0`
- **G6 `echo-flag-E-off`** — sudo line: `COMMAND=/usr/bin/sh -c 'echo -E 0 > /proc/sys/user/max_user_namespaces'`. `-[neE]+` flags are never planted; mutant returns `-E` as the echo value.
  - input: `T h sudo[5]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/sh -c 'echo -E 0 > /proc/sys/user/max_user_namespaces'`
  - base rc=1: `SYSCTL_WRITE ts=T pid=5 key=user.max_user_namespaces value=0 via=sh-echo ⏎ SYSCTL_WRITES n=1 keys=1 userns_zero=1`
  - mut  rc=1: `SYSCTL_WRITE ts=T pid=5 key=user.max_user_namespaces value=-E via=sh-echo ⏎ SYSCTL_WRITES n=1 keys=1 userns_zero=0`
- **G7 `sysctl-f-alias-off`** — sudo line: `COMMAND=/usr/bin/sysctl -f /etc/sysctl.d/x.conf` — the `-f` alias of `-p`/`--load` is never planted.
  - input: `T h sudo[6]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/sysctl -f /etc/sysctl.d/x.conf`
  - base rc=1: `SYSCTL_WRITE ts=T pid=6 key=file:/etc/sysctl.d/x.conf value=- via=sysctl-load ⏎ SYSCTL_WRITES n=1 keys=1 userns_zero=0`
  - mut  rc=0: `SYSCTL_WRITES n=0 keys=0 userns_zero=0`
- **G8 `sysctl-system-off`** — sudo line: `COMMAND=/usr/bin/sysctl --system` — never planted.
  - input: `T h sudo[7]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/sysctl --system`
  - base rc=1: `SYSCTL_WRITE ts=T pid=7 key=system value=- via=sysctl-load ⏎ SYSCTL_WRITES n=1 keys=1 userns_zero=0`
  - mut  rc=0: `SYSCTL_WRITES n=0 keys=0 userns_zero=0`
- **G9 `cw-tee-prefix-loose`** — sudo line: `COMMAND=/usr/bin/sh -c 'echo 0 | tee /proc/sys'` — `/proc/sys` without trailing slash; mutant emits a write with `key=?` (rc 0→1).
  - input: `T h sudo[8]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/sh -c 'echo 0 | tee /proc/sys'`
  - base rc=0: `SYSCTL_WRITES n=0 keys=0 userns_zero=0`
  - mut  rc=1: `SYSCTL_WRITE ts=T pid=8 key=? value=0 via=tee ⏎ SYSCTL_WRITES n=1 keys=1 userns_zero=0`
- **G10 `cw-nested-depth-1`** — sudo line: `COMMAND=/bin/sh -c 'sh -c \'echo 0 > /proc/sys/user/max_user_namespaces\''` — shell inside shell (depth 2); the battery nests only once (W4).
  - input: `T h sudo[9]:    u : PWD=/x ; USER=root ; COMMAND=/bin/sh -c 'sh -c \'echo 0 > /proc/sys/user/max_user_namespaces\''`
  - base rc=1: `SYSCTL_WRITE ts=T pid=9 key=user.max_user_namespaces value=0 via=sh-echo ⏎ SYSCTL_WRITES n=1 keys=1 userns_zero=1`
  - mut  rc=0: `SYSCTL_WRITES n=0 keys=0 userns_zero=0`
- **G11 `cw-via-sh-echo-off`** — DETECTOR gap, not a sudo-line gap: the mutant rewrites every `via=sh-echo` to `via=sh-redirect` (observable in `SYSCTL_WRITE` lines) yet scores 60/60 — `got_writes()` parses only `key`/`value`, the summary check ignores `via`, and the selftest compares `(summary, rc)` only. No frozen check asserts the `via=` field.
  - input: `T h sudo[10]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/sh -c 'echo 0 > /proc/sys/user/max_user_namespaces'`
  - base rc=1: `SYSCTL_WRITE ts=T pid=10 key=user.max_user_namespaces value=0 via=sh-echo ⏎ SYSCTL_WRITES n=1 keys=1 userns_zero=1`
  - mut  rc=1: `SYSCTL_WRITE ts=T pid=10 key=user.max_user_namespaces value=0 via=sh-redirect ⏎ SYSCTL_WRITES n=1 keys=1 userns_zero=1`
- **G12 `cw-redir-lt-recorded`** — sudo line: `COMMAND=/usr/bin/sh -c 'echo 0 < /proc/sys/user/max_user_namespaces'` — `<` redirections are never planted; mutant records them as writes (rc 0→1).
  - input: `T h sudo[11]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/sh -c 'echo 0 < /proc/sys/user/max_user_namespaces'`
  - base rc=0: `SYSCTL_WRITES n=0 keys=0 userns_zero=0`
  - mut  rc=1: `SYSCTL_WRITE ts=T pid=11 key=user.max_user_namespaces value=0 via=sh-echo ⏎ SYSCTL_WRITES n=1 keys=1 userns_zero=1`
- **G13 `scan-cont-marker-short`** — sudo line: `T h sudo[12]:    u : (command continued)` (continuation with empty rest). The mutant does not merely mis-score — it **crashes**: `IndexError: list index out of range` at `rest = line.split(" : (command continued) ", 1)[1]` (process exit 1, traceback on stderr). The counter has no crash-tolerance family; a crash inside a planted case would score RUN_ERROR, but no family drives this path.
  - input: `T h sudo[12]:    u : (command continued)`
  - base rc=0: `SYSCTL_WRITES n=0 keys=0 userns_zero=0`
  - mut  rc=1: `<crash> IndexError: list index out of range at scan_journal rest= line.split(...)[1] (traceback on stderr)`
- **G14 `scan-orphan-ignored`** — sudo line: `T h sudo[13]:    u : (command continued) /proc/sys/x` alone in the capture (orphan continuation). Base fails closed (rc 2, `unparsed=1`); mutant ignores it (rc 0).
  - input: `T h sudo[13]:    u : (command continued) /proc/sys/x`
  - base rc=2: `SYSCTL_WRITES n=0 keys=0 userns_zero=0 ⏎ SYSCTL_WRITES_SETUP unparsed=1`
  - mut  rc=0: `SYSCTL_WRITES n=0 keys=0 userns_zero=0`
- **G15 `ts-short-day-2digit`** — sudo line: `Nov  5 05:22:02 h sudo[14]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/sysctl -w user.max_user_namespaces=0` — single-digit day, classic syslog shape. S1 always emits `%02d`, so the battery never plants it; the mutant fails closed on every such line.
  - input: `Nov  5 05:22:02 h sudo[14]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/sysctl -w user.max_user_namespaces=0`
  - base rc=1: `SYSCTL_WRITE ts=Nov-05_05:22:02 pid=14 key=user.max_user_namespaces value=0 via=sysctl ⏎ SYSCTL_WRITES n=1 keys=1 userns_zero=1`
  - mut  rc=2: `SYSCTL_WRITES n=0 keys=0 userns_zero=0 ⏎ SYSCTL_WRITES_SETUP unparsed=1`
- **G16 `runway-low-le`** — fake-/proc fixture: limit=10, two non-initial ns links, `--low 8` (runway == low == 8). Base `state=ok` rc 0; mutant `state=low` rc 1. The 12 runway cases never sample the `runway == low` boundary at seeds 7/8.
  - input: `--proc fixture limit=10 used=2 --low 8 (runway==low==8)`
  - base rc=0: `USERNS_RUNWAY limit=10 used_lb=2 pids=3 unreadable=0 runway=8 low=8 state=ok`
  - mut  rc=1: `USERNS_RUNWAY limit=10 used_lb=2 pids=3 unreadable=0 runway=8 low=8 state=low`

## Nuances on killed mutants

- `sysctl-pfile-glued-off` is killed **only by the selftest** (case `journal-more-writes`, `-p/etc/sysctl.d/y.conf`): the battery itself has no glued `-pFILE` family; check (a) carries it.
- `tok-ops-gt-first` is killed **only by the battery's `(key, value)` assertion** (W6): the selftest's summary-only comparison cannot see the corrupted echo value (`-` instead of the planted value) — the selftest does not pin per-write values.
- Fail-closed mutations are caught: unknown-timestamp skip by S2, `Unparsed` swallow by S3, exit-2 removal by S2+S3 — the fail-closed core is well defended.
- `registry=met` and `sourced=met` on **all 74 mutant runs**; `live=ok` everywhere except `runway-init-counted` (which also breaks the live cross-check). The registry audit does not pin the tool body (masked comparison), so C1's registry/sourced checks are insensitive to tool-body mutations.

## Detector-level conclusions

1. The frozen battery's grammar core is well defended: every quote/escape/exit-event/continuation/timestamp/sysctl-form mutation that changes write extraction on planted shapes is killed (17/37), identically on two seeds.
2. Sixteen specific regression classes pass the frozen counter (list above). Strongest: G5 (fail-closed lost on unterminated script quote — the incident class this round is about), G13 (crash on empty-rest continuation), G3 (`SIGNAL=` exit events), G7/G8 (`-f`/`--system`), G15 (single-digit-day short timestamps), G11 (`via=` unchecked anywhere).
3. Candidate battery amendments (coverage findings only, not contract changes): families for `SIGNAL=` exit events, `sysctl -f`/`--system`/`--load=F`, glued fd redirection, `echo -E`, double nesting, `<` redirection, empty-rest and orphan continuations, unterminated script quote, 1-digit escape at word start, single-digit-day short timestamps, one `via=` assertion, and a runway case at `runway == low`.

## Restoration / hygiene

- Pristine base tree untouched: tool sha256 re-checked after all 76 counter runs = `4ef3108f171dc5fa0b42c8dc1cf4f374cb223ab0bb9411c1e992e255e46abc0b` (matches pre-run). Mutants lived only in `$S/mut-*`.
- Lane repo touched only by read-only `git archive`; no git/jj mutation, no sudo, no sysctl/host changes, no edits to tools/, corpus/, SCORECARD.md, contract, counters or receipts.
- Checks NOT run: `--journal-live` path (needs system journalctl), count-c2.py (other seats' scope), controls-r99.py re-run (frozen receipt), mutations to non-tool files.

## Appendix: raw counter final lines and sha256

```
BASE           s7 rc=0 C1=met cases_ok=60/60 seed=7 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
BASE           s8 rc=0 C1=met cases_ok=60/60 seed=8 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
esc-177-off    s7 rc=0 C1=met cases_ok=60/60 seed=7 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
esc-177-off    s8 rc=0 C1=met cases_ok=60/60 seed=8 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
esc-2digit-off s7 rc=1 C1=unmet cases_ok=57/60 seed=7 selftest=fail live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=selftest,battery
esc-2digit-off s8 rc=1 C1=unmet cases_ok=57/60 seed=8 selftest=fail live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=selftest,battery
esc-2digit-bound s7 rc=0 C1=met cases_ok=60/60 seed=7 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
esc-2digit-bound s8 rc=0 C1=met cases_ok=60/60 seed=8 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
esc-1digit-off s7 rc=0 C1=met cases_ok=60/60 seed=7 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
esc-1digit-off s8 rc=0 C1=met cases_ok=60/60 seed=8 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
split-unesc-dropped s7 rc=1 C1=unmet cases_ok=57/60 seed=7 selftest=fail live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=selftest,battery
split-unesc-dropped s8 rc=1 C1=unmet cases_ok=57/60 seed=8 selftest=fail live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=selftest,battery
split-quote-mode-off s7 rc=1 C1=unmet cases_ok=33/60 seed=7 selftest=fail live=ok(limit=122865,used_lb=6,state=ok) incident=fail(rc=2) registry=met sourced=met(S633,S634,S635,S636) checks_failed=selftest,battery,incident
split-quote-mode-off s8 rc=1 C1=unmet cases_ok=33/60 seed=8 selftest=fail live=ok(limit=122865,used_lb=6,state=ok) incident=fail(rc=2) registry=met sourced=met(S633,S634,S635,S636) checks_failed=selftest,battery,incident
split-unterminated-no-raise s7 rc=1 C1=unmet cases_ok=57/60 seed=7 selftest=fail live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=selftest,battery
split-unterminated-no-raise s8 rc=1 C1=unmet cases_ok=57/60 seed=8 selftest=fail live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=selftest,battery
split-backslash-off s7 rc=0 C1=met cases_ok=60/60 seed=7 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
split-backslash-off s8 rc=0 C1=met cases_ok=60/60 seed=8 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
split-quoted-none-false s7 rc=0 C1=met cases_ok=60/60 seed=7 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
split-quoted-none-false s8 rc=0 C1=met cases_ok=60/60 seed=8 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
exit-suffix-never s7 rc=1 C1=unmet cases_ok=57/60 seed=7 selftest=fail live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=selftest,battery
exit-suffix-never s8 rc=1 C1=unmet cases_ok=57/60 seed=8 selftest=fail live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=selftest,battery
exit-suffix-exit-only s7 rc=0 C1=met cases_ok=60/60 seed=7 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
exit-suffix-exit-only s8 rc=0 C1=met cases_ok=60/60 seed=8 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
tok-comment-off s7 rc=1 C1=unmet cases_ok=57/60 seed=7 selftest=fail live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=selftest,battery
tok-comment-off s8 rc=1 C1=unmet cases_ok=57/60 seed=8 selftest=fail live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=selftest,battery
tok-dquote-off s7 rc=1 C1=unmet cases_ok=57/60 seed=7 selftest=fail live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=selftest,battery
tok-dquote-off s8 rc=1 C1=unmet cases_ok=57/60 seed=8 selftest=fail live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=selftest,battery
tok-glued-fd-no-pop s7 rc=0 C1=met cases_ok=60/60 seed=7 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
tok-glued-fd-no-pop s8 rc=0 C1=met cases_ok=60/60 seed=8 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
tok-ops-gt-first s7 rc=1 C1=unmet cases_ok=57/60 seed=7 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=battery
tok-ops-gt-first s8 rc=1 C1=unmet cases_ok=57/60 seed=8 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=battery
tok-single-quote-self-find s7 rc=0 C1=met cases_ok=60/60 seed=7 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
tok-single-quote-self-find s8 rc=0 C1=met cases_ok=60/60 seed=8 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
echo-flag-E-off s7 rc=0 C1=met cases_ok=60/60 seed=7 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
echo-flag-E-off s8 rc=0 C1=met cases_ok=60/60 seed=8 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
echo-value-include-exe s7 rc=1 C1=unmet cases_ok=42/60 seed=7 selftest=fail live=ok(limit=122865,used_lb=6,state=ok) incident=fail(rc=1) registry=met sourced=met(S633,S634,S635,S636) checks_failed=selftest,battery,incident
echo-value-include-exe s8 rc=1 C1=unmet cases_ok=42/60 seed=8 selftest=fail live=ok(limit=122865,used_lb=6,state=ok) incident=fail(rc=1) registry=met sourced=met(S633,S634,S635,S636) checks_failed=selftest,battery,incident
sysctl-pattern-no-skip s7 rc=1 C1=unmet cases_ok=57/60 seed=7 selftest=fail live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=selftest,battery
sysctl-pattern-no-skip s8 rc=1 C1=unmet cases_ok=57/60 seed=8 selftest=fail live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=selftest,battery
sysctl-f-alias-off s7 rc=0 C1=met cases_ok=60/60 seed=7 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
sysctl-f-alias-off s8 rc=0 C1=met cases_ok=60/60 seed=8 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
sysctl-pfile-glued-off s7 rc=1 C1=unmet cases_ok=60/60 seed=7 selftest=fail live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=selftest
sysctl-pfile-glued-off s8 rc=1 C1=unmet cases_ok=60/60 seed=8 selftest=fail live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=selftest
sysctl-system-off s7 rc=0 C1=met cases_ok=60/60 seed=7 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
sysctl-system-off s8 rc=0 C1=met cases_ok=60/60 seed=8 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
cw-tee-prefix-loose s7 rc=0 C1=met cases_ok=60/60 seed=7 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
cw-tee-prefix-loose s8 rc=0 C1=met cases_ok=60/60 seed=8 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
cw-nested-depth-1 s7 rc=0 C1=met cases_ok=60/60 seed=7 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
cw-nested-depth-1 s8 rc=0 C1=met cases_ok=60/60 seed=8 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
cw-via-sh-echo-off s7 rc=0 C1=met cases_ok=60/60 seed=7 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
cw-via-sh-echo-off s8 rc=0 C1=met cases_ok=60/60 seed=8 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
cw-redir-lt-recorded s7 rc=0 C1=met cases_ok=60/60 seed=7 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
cw-redir-lt-recorded s8 rc=0 C1=met cases_ok=60/60 seed=8 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
scan-cont-replace s7 rc=1 C1=unmet cases_ok=57/60 seed=7 selftest=fail live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=selftest,battery
scan-cont-replace s8 rc=1 C1=unmet cases_ok=57/60 seed=8 selftest=fail live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=selftest,battery
scan-cont-marker-short s7 rc=0 C1=met cases_ok=60/60 seed=7 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
scan-cont-marker-short s8 rc=0 C1=met cases_ok=60/60 seed=8 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
scan-orphan-ignored s7 rc=0 C1=met cases_ok=60/60 seed=7 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
scan-orphan-ignored s8 rc=0 C1=met cases_ok=60/60 seed=8 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
scan-unknown-ts-skip s7 rc=1 C1=unmet cases_ok=57/60 seed=7 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=battery
scan-unknown-ts-skip s8 rc=1 C1=unmet cases_ok=57/60 seed=8 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=battery
scan-unparsed-swallow s7 rc=1 C1=unmet cases_ok=57/60 seed=7 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=battery
scan-unparsed-swallow s8 rc=1 C1=unmet cases_ok=57/60 seed=8 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=battery
report-exit2-off s7 rc=1 C1=unmet cases_ok=54/60 seed=7 selftest=fail live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=selftest,battery
report-exit2-off s8 rc=1 C1=unmet cases_ok=54/60 seed=8 selftest=fail live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=selftest,battery
ts-short-day-2digit s7 rc=0 C1=met cases_ok=60/60 seed=7 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
ts-short-day-2digit s8 rc=0 C1=met cases_ok=60/60 seed=8 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
runway-clamp-off s7 rc=1 C1=unmet cases_ok=55/60 seed=7 selftest=fail live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=selftest,battery
runway-clamp-off s8 rc=1 C1=unmet cases_ok=57/60 seed=8 selftest=fail live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=selftest,battery
runway-init-counted s7 rc=1 C1=unmet cases_ok=48/60 seed=7 selftest=fail live=fail incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=selftest,battery,live
runway-init-counted s8 rc=1 C1=unmet cases_ok=48/60 seed=8 selftest=fail live=fail incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=selftest,battery,live
runway-low-le  s7 rc=0 C1=met cases_ok=60/60 seed=7 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
runway-low-le  s8 rc=0 C1=met cases_ok=60/60 seed=8 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
classify-guard-off s7 rc=0 C1=met cases_ok=60/60 seed=7 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
classify-guard-off s8 rc=0 C1=met cases_ok=60/60 seed=8 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-
```

```
sha256 base                       4ef3108f171dc5fa0b42c8dc1cf4f374cb223ab0bb9411c1e992e255e46abc0b  (tools/mori-userns-runway.py @ 5013f0be)
sha256 esc-177-off                c1625772d195fa0e773bf51ab8d01cf07dad831c70797d89b4bc8cbaf4789adc
sha256 esc-2digit-off             0762e6cf45fd403faa0479fc9f6881c17740745a947b29cebd1050f9140cc13b
sha256 esc-2digit-bound           cbe81bbe77c85c1b98ad4253c25cb46fbd58c98ac070c98194e78be1f2ec4132
sha256 esc-1digit-off             e414a5be7ae6a4df042e6fa4be528bf5bdbaa83a1ad618b893a54a1b94ff51b2
sha256 split-unesc-dropped        66a41645d9391ed1c120ef73ed7b12a65c030c78c1522290c7329f9253c67e7a
sha256 split-quote-mode-off       01ef2a4efb09139e59a01dc4b4ebe9681c6e879961a84c3b2e3f5e5a24db18e8
sha256 split-unterminated-no-raise 9df42b15047443faad80093d0c7b27e97ce552f139b5bc75434647fe0632feea
sha256 split-backslash-off        7eec427f095d3053f9f636e467fa2b08b73dfe6b1e4b4a32f8494b6bd4837688
sha256 split-quoted-none-false    43a20a31dad074d404e5f53c2828bb1b3c8b769354f3286f12bbe8e391bd6eb2
sha256 exit-suffix-never          dc46f899a4a5da87e614807aa63cec02e6c2ca4cd95498eb4dd6555d4da0b923
sha256 exit-suffix-exit-only      7ae04b24291f69d5cc18663c1b291ac83312db7e21be92388afbbe6b2cee6c47
sha256 tok-comment-off            dfa8cb182c63abf4501da3f1fa08eb6ca7e18ec259c439808d42c34da74c8c37
sha256 tok-dquote-off             e9cbf3f6ed392b27e82f801d6140a529cdd156b6e5eee84d12b93e1bcd7f4c94
sha256 tok-glued-fd-no-pop        2455c8281345427b6227e62dd629f47437dd0ca71d4450b8294b97faf6a51bb9
sha256 tok-ops-gt-first           2e24626aacb2e34fcf0915cf50ee5fcb9ec6a2aba773cea93899f6f44fd5b81a
sha256 tok-single-quote-self-find 58fefb7e56bb61b19e2c27d0cefc9e35806095f5627bd932043804b0265eb302
sha256 echo-flag-E-off            9c4fa7b1919b085399d94dadaaf1fc8dae177281be565f61eda9215dbda60b1b
sha256 echo-value-include-exe     59e5bba1e9c1605a083a178d8d936d9f939b38b32992585e51cfc123d4982130
sha256 sysctl-pattern-no-skip     ee70b9df8ae0cd53f4636d7d19b95633d11d7c61908b456def8755e430163cbe
sha256 sysctl-f-alias-off         8dc2bd5c40d766256223f408959cad1f502673099a922cad4c2facc449c7eb98
sha256 sysctl-pfile-glued-off     f758330a9c812844f291b59d3b59e3a9012b6dd3063cc2485425380b9cf3b8aa
sha256 sysctl-system-off          8f3d44a07cd6cd3a7963d482b95e29027f412ba43fe4bb07feb055c46f3f08d3
sha256 cw-tee-prefix-loose        d0b9698fc1b369d14fb50daabb6cd68bfc8573bfac90edfd866451809cd3331f
sha256 cw-nested-depth-1          27b26e777c1b60b91c149da0a27e4d41a38c85b9a78c5af023cedc0444ea07b1
sha256 cw-via-sh-echo-off         940e6782fe548220c9edd2c3e1a3d641793de3342b0292c06ce2abc89289d236
sha256 cw-redir-lt-recorded       6c4be53917e9e5cf1db772f58d072e01b4899d9b6bb9f5018443c164217d6a29
sha256 scan-cont-replace          038fb04b470599574165d444566edb8424876fc0ef32fa1ad8b62c4166fa0ef1
sha256 scan-cont-marker-short     6acfdc48029619650f79ff49824c63d7c5b857c7918b05f5dec556cc10cde54d
sha256 scan-orphan-ignored        e354816c5bcb6fdbd07b0107b1e43bf72bf84c3715e49d1f55009ae7a7a80cfb
sha256 scan-unknown-ts-skip       926e672be2ee5fd0b6a7590fdc6daeb98a165bdd3b51bb8accec3f613face994
sha256 scan-unparsed-swallow      e3704052f1f402bfd3b6c2f902c0926cd3ffe66e7609ebe552fb629cb34e04ad
sha256 report-exit2-off           42ec3e309162b80302428fc5fdc5f0b3a2d4eb054fc2aa95183e8a26fb22dc78
sha256 ts-short-day-2digit        8345825ad8d3047de0b909497831a3c1dc408686e11fede1d78ca918b092291d
sha256 runway-clamp-off           cced79b46d94f809f5303dbbe6d5ea635ddef19c9e281d658d0f534d2d3f82d8
sha256 runway-init-counted        5febaea5a0efe9f786867018a533c4d26ab8c33fff062054a6be0939131ef30c
sha256 runway-low-le              8d5c4dabc15ac0321a967198a2d8f1b35f6c35a278e277cbc9aee3a9a6e0adf7
sha256 classify-guard-off         f1b8a3dc6cda56981e078f360448feb36d5c70745f1972fad6d6a22c958b01ea
```

VERDICT C1 holds: no false-met observed — baseline met 60/60 on both seeds; 17/37 mutants killed on both seeds including every grammar-core path; 4 survivors proven equivalent (byte-identical on corpus + incident); 16 survivors are battery coverage gaps with verified distinguishing inputs — candidate amendments for a future battery, not violations of the frozen claim.