# Mo99RevC1 — C1 code review: `tools/mori-userns-runway.py` sudo-log grammar (round 99, w1)

Scope: `git -C mori-shokunin diff 73308ff6… 5013f0be… -- tools/mori-userns-runway.py SKILL.md corpus/SOURCES.md corpus/knowledge/sudo-log-grammar-r99.md` (453 tool lines + docs). Worktree tool bytes == landing bytes (sha256 4ef3108f… both, HEAD = 5013f0be). Method: source-faithfulness read (S635/S636/S633/S634 pinned copies) + 26 CLI edge runs + module-level probes. Classification per seat spec; severity = impact on the C1 claim as written.

## Findings

**F1 · defect-in-claimed-scope · medium — `>|` mis-tokenized as a pipe; a real write is silently missed.**
`shell_tokens` OPS lacks `>|` (POSIX 2.7.2 noclobber-override operator, present in the pinned S634, raw lines 4799-4800: "the `>|` redirection operator shall override this noclobber option"). `>` then op `|`: the target word becomes the next pseudo-command's argv, no redirect recorded.
`--journal jB.txt` line `…COMMAND=/usr/bin/sh -c 'echo 0 >| /proc/sys/vm/swappiness'` → output `SYSCTL_WRITES n=0 keys=0 userns_zero=0`, **rc 0** (no setup line). A shell executes this as a write to vm.swappiness.

**F2 · defect-in-claimed-scope · medium — backslash-<newline> continuation not removed; redirect target corrupted → real write silently missed.**
POSIX 2.2.3 (S634): `\` before `<newline>` is a line continuation (both removed). `shell_tokens` appends the `<newline>` into the word (probe: `"echo 0 >\\\n/proc/sys/x"` → token `('w', '\n/proc/sys/x', True)`), so the target no longer starts with `/proc/sys/`. Tool docstring claims "newlines as in POSIX XCU 2.2/2.3".
`--journal jB.txt` line `…COMMAND=/usr/bin/sh -c 'echo 0 >\\#012/proc/sys/user/max_user_namespaces'` → `SYSCTL_WRITES n=0 …`, **rc 0**.

**F3 · defect-in-claimed-scope · low — here-doc body read as commands → false write.**
`<<` tokenizes as two `<` ops (delimiter word consumed as an input file), then body lines are parsed as real commands.
`--journal jD.txt`: `…COMMAND=/usr/bin/sh -c 'cat << EOF#012echo 0 > /proc/sys/user/max_user_namespaces#012EOF'` → `SYSCTL_WRITE ts=… pid=41 key=user.max_user_namespaces value=0 via=sh-echo`, `SYSCTL_WRITES n=1 keys=1 userns_zero=1`, rc 1. Reality: `cat << EOF` writes nothing. Knowledge "Limits" says here-documents are "not expand[ed]", which does not warn that body text is reported as attributed writes (ts/pid/key/value).

**F4 · defect-in-claimed-scope · low — `#040` (sudo's escape of a space in the command path) decodes corruptly.**
S635 new_logline line ~199 escapes the command path with `LBUF_ESC_CNTRL|LBUF_ESC_BLANK`, so a path space is `#040` (4-char form; `escape()` gives 4 chars for 0o10–0o77). `unescape_cntrl` branch 2 guards `d[0] in "123"` and `int(d[:2],8) < 0o40`, so `#040` falls to the 1-digit branch: probe `unescape_cntrl("/opt/my#040tool")` → `'/opt/my\x040tool'` (should be `'/opt/my tool'`). No write-detection delta observed (a spaced path never basename-matches sysctl/sh/tee; jB pid28 → rc 0), but the tool docstring's "sudo escapes nothing printable" is false for the path, and the inverse is not faithful for this sudo-produced class. Silent (no unparsed).

**F5 · defect-in-claimed-scope · low (comment-only) — tool docstring example contradicts its own code.**
`unescape_cntrl` docstring: "`#071` is a literal". Probe: `unescape_cntrl("a#071b")` → `'a\x071b'` — it decodes (BEL + `1`), consistently with the knowledge Limits note that literal `#0`+digit decodes. Same branch structure as F4.

**F6 · defect-in-claimed-scope · low — exit-suffix regex fires inside a quoted argument; the accept event is silently dropped.**
`scan_journal` tests `EXIT_SUFFIX_RE.search` on the raw command before classify, unquoted-context-unaware.
`--journal jE.txt`: `…COMMAND=/usr/bin/echo 'x ; EXIT=0'` → `SYSCTL_WRITES n=0 keys=0 userns_zero=0`, **rc 0** (no unparsed). The whole line is skipped as an exit event; a write in such a command would be lost without any setup line. Contrived arg shape.

**F7 · documented-limit (undocumented) · info — an empty argument is invisible in sudo's rendering.**
sudo renders `tee '' /proc/sys/x` and `tee /proc/sys/x` identically (`''` for an empty arg emits nothing between two spaces; eventlog.c:206-210). jF: `…COMMAND=/usr/bin/tee  /proc/sys/vm/swappiness` → `key=vm.swappiness value=- via=tee`, rc 1, while `tee '' <file>` in reality fails to open and writes nothing. Over-reporting (conservative) direction; no parser can distinguish. Not in knowledge Limits.

**F8 · out-of-scope · info — interleaved same-pid continuations misjoin.**
`scan_journal` joins a continuation to the pid's most recent open COMMAND; a capture that reorders same-pid parts (impossible from sudo's syslog writer: parts are emitted back-to-back within one `do_syslog_sudo` call, S635:1011-1045) would splice text. jG (pid 71: part1, another command, continuation) → `n=1 userns_zero=1` + `SYSCTL_WRITES_SETUP unparsed=1`, rc 2 — fail-closed direction.

## Claims verified holding (exact outputs)

- Self-test: `python3 tools/mori-userns-runway.py --selftest` → `MORI_USERNS_RUNWAY_SELFTEST: PASS (19 cases)`, rc 0 (claim: 19 cases).
- Full r99 capture: `--journal .ufo/waves/round-99/evidence/journal-incident-r99.txt` → six `SYSCTL_WRITE` lines (05:14:52 v=0 sh-echo; 05:14:54 v=10000 sysctl; 05:16:04 v=15638 sysctl; 05:16:04 v=15638 sh-echo; 05:22:02 v=0 sh-echo; 05:42:18 v=122865 sysctl), `SYSCTL_WRITES n=6 keys=1 userns_zero=2`, **rc 1**, no setup line — matches contract (d) and SKILL row pin.
- r98 capture: same six writes + `SYSCTL_WRITES_SETUP unparsed=1`, **rc 2** — matches the disclosed fail-closed behavior exactly.
- split_cmd faithful for the claimed classes: quoted space args, `\'`, `\\`, `#011`, `#012`, `#017`, `#0177` (jB pid21-23, jC → n=2 rc 1 keys redacted `?`, no unparsed; probes `#011`→`\t`, `#0177`→`\x7f`, `'a\'b c'`→`a'b c`), exit-suffix stripping of genuine ` ; EXIT=`/` ; SIGNAL=` tails, mid-word-literal `'` (path/arg without leading quote).
- Continuation join: joins across 10 far-apart interleaved pid lines (jA pid15 → `key=user.max_user_namespaces value=0`, rc 1, no unparsed); a continuation landing after an exit-event first part dedupes correctly (jA pid16/17 → exactly one userns write); orphan continuation fails closed (selftest journal-continued-broken; jG).
- Timestamps: `short-iso` and default `short` both parse incl. single-digit padded day (`Nov  5 05:22:02` → `ts=Nov-05_05:22:02`); unknown shapes fail closed (selftest journal-unparsed).
- Exit codes: missing input file → `SYSCTL_WRITES_SETUP FileNotFoundError` rc 2; `--journal-live` without `--since/--until` → rc 2; no-write → 0; ≥1 write → 1; unparsed ⇒ 2 even with events (selftest, jG).
- `2>&1` (fd pop, no bogus arg; write + `2>&1` correct, jA pid11), bash `&>` detected via sh-redirect value `-` (jA pid12), `$( )` inner redirect detected with `?`-redacted key/value (jA pid13), `a#b` literal + word-initial `#` comment discarded (jA pid14, jB pid27), `env`/NAME=value unwrap and nested `sysctl -w` inside `-c` detected (selftest j5).
- Registry row (SKILL.md:1460) vs behavior: verdict map (0/1/2 semantics, `via=sysctl/sysctl-load/sh-echo/sh-redirect/tee`), "PASS (19 cases)", both capture pins — all match observed output. In-place row edit disclosed in the appended round-99 note ✓.
- SOURCES.md S633-S636 rows: quotes/line-refs re-verified in pinned copies (eventlog.c:202/208/223/1042, lbuf.c:145/162-163, escape() 111-141, append_esc_v1 143-200, S633 raw 112-116 `-p/--load` & 134-136 `-r/--pattern`, S634 raw 104 single-quote rule & 303-304 `#` rule) — all match. Knowledge claim table matches tool and sources. "25 sudo lines failed the (r98) POSIX splitter": `grep "COMMAND=" journal-incident-r99.txt | grep -c "#0\|\\'"` → **25** ✓.
- `#0`-literal ambiguity and mid-word continuation cut are documented in knowledge Limits ✓; JSON/`@cee` logs and sudo_logsrvd excluded ✓.

## Residual risk and verification gaps

- Unrun: `count-c1.py`/`count-c2.py` battery runs at either revision (other seats); runway-mode m03 mutation controls; any live `journalctl` invocation (I ran file/scanner paths only).
- The counter's 60-case battery does not exercise `>|`, backslash-newline continuations, here-doc bodies, `#040` paths, or quoted ` ; EXIT=` args — so C1's measured 60/60 is unaffected by F1-F6; the exposure is the claim sentence, not the measurement.
- F1/F2/F6 fail open (silent rc 0) — the only false-negative classes found; everything else found fails closed or over-reports.

VERDICT C1 needs-amend: the measured battery/incident/registry/source claims hold as run, but "reads a `sh -c` script as POSIX words/quotes/comments/operators (S634)" is falsified in scope by F1 (`>|`, an operator defined in the pinned S634) and F2 (backslash-<newline>, XCU 2.2.3), both silent false negatives, plus F3/F6; document these classes in knowledge Limits (and SKILL row) or fix `shell_tokens`/`scan_journal` before the claim sentence is reused.
