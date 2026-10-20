# LiveSurfaceRecipe — journalctl argv surface and safe latest-anchor recipe

Seat: `MoriR16.LiveSurfaceRecipe` (scout, leaf). Target: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Read time: 2026-10-20. Baseline HEAD `b83edc6ee3db6822382ab673d7e6e984e420f22f` (`git rev-parse`); `git status --porcelain`
observed only; nothing in the worktree was edited except this report.

Read-time state: `tools/mori-journal-window.py` and `tools/mori-round16-regressions.py` were **absent** when this seat
read (`ls -la tools/`). This report is therefore contract-level argv/recipe evidence, not a code review. Wave 2 reviews
the delivered code.

Disclosure (L1 no-probe rule): no live journal query, no measurement/probe loop, no background job, no synthetic or
fixture run, no build/test/gate/smoke/formatter. `journalctl` was invoked only as `journalctl --version` and
`journalctl --help` (explicitly assigned; both open no journal). Other reads were static: `man journalctl`,
`man systemd.journal-fields`, `man timeout`, `/proc/sys/kernel/random/boot_id` content, `ls`/`stat`/`getfacl` of the
journal directory, and `git rev-parse`/`git status`. No `/tmp` writes, no installs, no outside-lane writes.

## 0. Axes

- **A1 argv fidelity** — every token the probe passes is documented, scoped, and non-narrowing.
- **A2 anchor mint correctness** — the anchor is the latest retained record of *this* boot in *that* scope, validated
  strictly, without writing journal state.
- **A3 fail-closed safety** — no token that can silently filter a boot boundary, truncate the stream, mutate a cursor
  file, or emit `MESSAGE`.

## 1. Installed surface

| Fact | Observed |
|---|---|
| Binary | `/usr/bin/journalctl`, `systemd 261 (261.2-1-arch)` |
| Local man | `JOURNALCTL(1)` footer `systemd 261.2`; host `systemd.journal-fields(7)` footer `systemd 261.2` |
| Registry source | S014 is the systemd **262** `latest` page. For the options used here the 261 man quotes agree verbatim with S014; no drift on this surface. |

All options used by the contract appear in `journalctl --help`: `--cursor=`, `--no-tail`, `--quiet`, `--output=`,
`--output-fields=`, `--system`, `--user`, `--boot[=ID]`, `-n`, `--no-pager`. The help also lists the forbidden
surface below, so no token is a typo risk at parse time — a wrong token would be accepted by journalctl and change
meaning, which is why the harness must assert it.

Documented anchors (local 261.2 man, agreeing with S014):

- `-c, --cursor=` — “Start showing entries from the location in the journal specified by the passed cursor.”
- `--after-cursor=` — “Start showing entries from the location in the journal **after** the location specified by the
  passed cursor.”
- `--cursor-file=FILE` — “At the end, write the cursor of the last entry to FILE.”
- `--show-cursor` — “The format of the cursor is private and subject to change.”
- `-b, --boot[=ID]` — “This will add a match for `_BOOT_ID=`.”; empty argument selects the current boot.
- `-k, --dmesg` — “This implies `--boot=0` unless explicitly specified otherwise.”
- `-n, --lines=` — “Show the most recent journal events and limit the number of events shown.” default 10 when bare.
- `--no-tail` — “Show all stored output lines, even in follow mode. Undoes the effect of `--lines=`.”
- `-q, --quiet` — “Suppresses all informational messages … any warning messages regarding inaccessible system
  journals when run as a normal user.”
- `-o json` — “formats entries as JSON objects, separated by newline characters”; duplicate fields become arrays,
  fields over 4096 bytes become `null` (without `--all`), non-UTF8 bytes become numeric arrays.
- `--output-fields=` — for full-field modes “the `__CURSOR`, `__REALTIME_TIMESTAMP`, `__MONOTONIC_TIMESTAMP`, and
  `_BOOT_ID` fields are always printed.”
- `EXIT STATUS` — “On success, 0 is returned; otherwise, a non-zero failure code is returned.”

## 2. Canonical window argv (exact)

```
<journalctl> --user|--system \
  --cursor=<anchor.cursor> \
  --no-tail \
  --quiet \
  --output=json \
  --output-fields=__CURSOR,_BOOT_ID,MESSAGE_ID,UNIT_RESULT,EXIT_CODE,EXIT_STATUS \
  --no-pager
```

Rules:

1. **One** scope flag, exactly matching the validated anchor/`--scope`. Omitting both makes journalctl show “all
   messages that the user can see”, mixing scopes.
2. `--cursor=` **attached with `=`**, as one argv element, `shell=False`. Attached form is safe for any opaque cursor
   (no leading-`-` option confusion, no word splitting). The cursor is the only non-mutating way to supply the start
   position: `--cursor-file` writes state.
3. **No `-b`/`--boot`, no `-k`.** The boot boundary must stay visible. `-b` adds a `_BOOT_ID=` match, so a window
   that crosses a reboot would silently lose the foreign-boot record and report a same-boot subset as the window.
   The contract's refusal on a foreign-boot record is only possible because the query does not filter it.
4. `--no-tail` is the only documented “all stored lines” switch. It removes dependence on any tail default or an
   implied `--lines=`. It does not bound bytes or time; `--timeout`/`--max-bytes` do that in the wrapper.
5. `--quiet` keeps informational lines and the non-root “not seeing messages from other users and the system” hint
   out of stderr. It does **not** prove access; an unreadable scope can yield rc0 with empty stdout, which the
   contract refuses as empty capture. Stderr silence is not access proof.
6. `--output=json` (long form; `-o json` is identical). `json-pretty`, `json-sse`, `json-seq` are not JSONL-per-line
   for this parser; `short*`, `verbose`, `export`, `cat` include `MESSAGE` text.
7. `--output-fields=` is the exact six-field string, no spaces. `MESSAGE` is never requested. The two timestamp
   fields always arrive in addition (documented); the parser must tolerate a four-key minimum record
   (`__CURSOR`, `_BOOT_ID`, `__REALTIME_TIMESTAMP`, `__MONOTONIC_TIMESTAMP`) and treat the class fields as optional
   per record.
8. `--no-pager` is the **one token beyond the contract list**. It is output-neutral when stdout is a pipe; census
   already passes it (`tools/mori-census.sh:1190`). Recommendation: add it, and have the harness allow exactly this
   extra token in its argv assertions. Without this allowance a correct implementation fails a strict six-token
   equality check.
9. No positional arguments. journalctl treats bare words as `FIELD=value` match filters; a stray match word narrows
   the window without a boot/scope error.
10. `--journalctl PATH` is the **executable path** (argv[0] for the child). It is never forwarded as a journalctl
    option. The child gets `stdin=DEVNULL`; env should drop `SYSTEMD_LOG_LEVEL` and set `SYSTEMD_PAGER=` (empty) so
    pager/log-level inheritance cannot change the capture.

## 3. Option verdict table

| Option | Verdict | Documented basis / why |
|---|---|---|
| `--user` / `--system` (exactly one) | ALLOW | Source selection; one scope per window. |
| `--cursor=<cursor>` | ALLOW | Inclusive start; the anchor record is expected first, which is the retention proof. |
| `--no-tail` | ALLOW | “Show all stored output lines”; defeats an injected/implied `--lines=`. |
| `--quiet` | ALLOW | Keeps informational/access-warning text out of stderr; not an access proof. |
| `--output=json` | ALLOW | One JSON object per line. |
| `--output-fields=<six>` | ALLOW | Field-limited projection; `MESSAGE` excluded. |
| `--no-pager` | ALLOW (recommended) | Output-neutral for pipes; tty safety. |
| `--after-cursor=` | FORBID | Exclusive: skips the anchor before it can be checked; missing anchor becomes indistinguishable from a clean window. |
| `--cursor-file=` | FORBID | Writes the last cursor to FILE at exit: cursor-state mutation, forbidden by contract. |
| `--show-cursor` | FORBID | Format private; prints a non-JSON `-- cursor: …` line that breaks JSONL; `-n1 --show-cursor` in short mode prints the entry's `MESSAGE`. |
| `-b` / `--boot` | FORBID in window | Adds a `_BOOT_ID=` match; filters the boot boundary the contract must observe. (Used only by the optional mint variant, §4.3.) |
| `-k` / `--dmesg` | FORBID | Implies `--boot=0` and adds `_TRANSPORT=kernel`; narrows scope and hides the boot boundary. |
| `-n` / `--lines` | FORBID in window | Truncates to the newest N; and `--no-tail` “undoes the effect of `--lines=`”, so mixing them is order-dependent and undocumented. |
| `-f` / `--follow` | FORBID | Never terminates; turns the probe into a streaming read. |
| `-r` / `--reverse` | FORBID | Reverses order; the “first record is the anchor, every later record follows” protocol needs forward order. |
| `-g` / `--grep` | FORBID | Filters on `MESSAGE=` (and implies `--reverse` with a bare `-n`); narrowing plus MESSAGE semantics. |
| `-S/--since`, `-U/--until` | FORBID | Time filtering silently drops retained records. |
| `-p/--priority`, `--facility` | FORBID | Adds `PRIORITY=`/facility matches; narrowing. |
| `-t/--identifier`, `-T`, `-u/--unit`, `--user-unit`, `--invocation`, `-I` | FORBID | Unit/identifier matches; narrowing. |
| `-m/--merge` | FORBID | Interleaves all available journals, including remote ones; mixes scopes. |
| `-M/--machine`, `-D/--directory`, `-i/--file`, `--root`, `--image`, `--namespace` | FORBID | Redirects the source; a window must read the one local scope. Test redirection is via `--journalctl PATH`, not journalctl itself. |
| `-a/--all` | FORBID | Removes the 4096-byte `null` cap and enlarges capture; not needed for the six fields. |
| other `-o` modes | FORBID | `MESSAGE` text (short/verbose/export/cat) or non-JSONL framing (`json-pretty`, `json-sse`, `json-seq`). |
| `--vacuum-*`, `--rotate`, `--sync`, `--flush`, `--setup-keys`, `--update-catalog`, `--verify`, `--list-*`, `--fields`, `--field`, `--disk-usage`, `--header`, `--relinquish-var` | FORBID | Administrative/mutating or non-record output; `--rotate`/`--vacuum-*` also destroy the anchor. |

## 4. Safe latest-anchor recipe

The probe never mints an anchor. The anchor is an explicit operator input; this recipe produces one without reading
`MESSAGE`, without writing journal state, and without a live probe in this round.

### 4.1 Canonical mint (mirrors the window's boot rule)

Canonical form — **no `-b`**, `-n 1`, boot decided by the `_BOOT_ID` field against `/proc`:

```
journalctl --user|--system -n 1 --no-pager --quiet \
  --output=json --output-fields=__CURSOR,_BOOT_ID
```

Why no `-b` in the mint (same reason as the window):

- `-b` is a match filter, and the man documents an “empty offset” equivalence caveat (`-0`/last-boot vs current-boot)
  that only resolves cleanly on a normal local store. The mint should not depend on it.
- `-n 1` returns the newest retained record in the scope. If that record is from an older boot, the scope has no
  current-boot records, and the `/proc` comparison refuses — which is the correct outcome (no stale anchor).
- One authoritative boot source (`/proc/sys/kernel/random/boot_id`) is easier to audit than a filter plus a check.

Then validate, in this order, and refuse on the first failure:

| # | Condition | Result |
|---|---|---|
| 1 | journalctl rc ≠ 0 | no anchor (unavailable) |
| 2 | journalctl stderr non-empty | no anchor (a corrupt/wedged read is not a position) |
| 3 | stdout empty, or more than one non-empty line | no anchor |
| 4 | line is not a JSON object | no anchor |
| 5 | `_BOOT_ID` missing, `null`, array, or not `^[0-9a-f]{32}$` | no anchor |
| 6 | `_BOOT_ID` ≠ dashless-lowercase `/proc/sys/kernel/random/boot_id` | no anchor (stale/foreign boot) |
| 7 | `__CURSOR` missing, `null`, array, empty, > 4096 chars, or containing a control/non-ASCII byte | no anchor |
| 8 | all pass | emit `mori-journal-anchor-v1` with the observed `_BOOT_ID` and `__CURSOR` verbatim |

The capture will also contain `__REALTIME_TIMESTAMP` and `__MONOTONIC_TIMESTAMP` (always-printed). Accept four keys;
do not assert a two-key set.

### 4.2 Bounded mint snippet (no temp files, separate streams)

`subprocess.run` with separate pipes and a timeout gives rc/stderr/line-count without shell composition:

```python
import json, re, subprocess
from pathlib import Path

FIELDS = "__CURSOR,_BOOT_ID"       # mint needs only these two (timestamps arrive anyway)
CURSOR_RE = re.compile(r"^[\x20-\x7e]{1,4096}$")

def current_boot_id() -> str:
    raw = Path("/proc/sys/kernel/random/boot_id").read_text(encoding="ascii").strip()
    return raw.replace("-", "").lower()

def mint(scope: str) -> dict:
    if scope not in ("user", "system"):
        raise ValueError("scope")
    boot = current_boot_id()
    argv = ["/usr/bin/journalctl", f"--{scope}", "-n", "1", "--no-pager", "--quiet",
            "--output=json", f"--output-fields={FIELDS}"]
    try:
        p = subprocess.run(argv, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, timeout=10, check=False)
    except subprocess.TimeoutExpired as e:
        raise RuntimeError("timeout") from e
    if p.returncode != 0 or p.stderr:
        raise RuntimeError("capture")
    if not p.stdout.endswith(b"\n") or p.stdout.count(b"\n") != 1:
        raise RuntimeError("line-count")
    rec = json.loads(p.stdout.decode("utf-8"))
    if not isinstance(rec, dict):
        raise RuntimeError("shape")
    b = rec.get("_BOOT_ID")
    if type(b) is not str or re.fullmatch(r"[0-9a-f]{32}", b) is None or b != boot:
        raise RuntimeError("boot")
    c = rec.get("__CURSOR")
    if type(c) is not str or CURSOR_RE.fullmatch(c) is None:
        raise RuntimeError("cursor")
    return {"schema": "mori-journal-anchor-v1", "scope": scope, "boot_id": b, "cursor": c}
```

Notes:

- `json.loads` of a duplicated field is already an array (journalctl encodes non-unique fields as arrays), so the
  scalar type checks cover duplicate `__CURSOR`; `_BOOT_ID` is journal-added/trusted.
- Write the returned object only as an explicit operator step: same-directory temp + `os.replace`, mode `0600`.
  Default location `$XDG_RUNTIME_DIR/mori/anchor-<scope>.json` (`/run/user/1000` here, mode `0700`). The runtime dir
  is cleared at logout/reboot, so an anchor cannot silently outlive its boot; losing it is the safe direction.
  If the probe later runs from a system unit under another uid, use a root-owned `0600` path instead.
- Never write the raw cursor into committed evidence; receipts record `anchor_sha256` and `boot_id` only.

### 4.3 Optional `-b` variant (not recommended, still correct if the check is kept)

`journalctl --<scope> -b -n 1 …` narrows to the current boot. It is acceptable only with the same `/proc` equality
check, because the man's “empty offset” sentence leaves `-b` vs “last boot” equivalent only on a normal local store.
It buys nothing over §4.1 and adds a documented caveat; use it only if a reviewer explicitly wants the journal-side
filter visible.

### 4.4 Traps (each has a concrete failure mode)

1. **`-n` + `--no-tail` mixed.** `--no-tail` “undoes the effect of `--lines=`”; whether the earlier or later option
   wins is not documented. Capture uses `-n 1` alone; the window uses `--no-tail` alone. Never both.
2. **`--show-cursor`.** Private format, non-JSON trailer, and `-n1 --show-cursor` in default short output prints the
   entry's `MESSAGE`. The anchor must come from `__CURSOR` in `-o json`, not from that line.
3. **`--cursor-file`.** Writes the cursor at exit; forbidden by the no-mutation contract and leaves a raw cursor file.
4. **Parsing the cursor.** `__CURSOR` is opaque and the private format can change; it must not be split into
   sequence/boot/time components. Boot comes from `_BOOT_ID`.
5. **rc0 + empty stderr as access proof.** False under `-q` (S014 suppresses inaccessible-journal warnings). The
   empty-capture refusal and the anchor-first rule are the guards.
6. **Combining `-b` with the window.** Turns a cross-boot stream into a silent same-boot subset; see §2 rule 3.
7. **Hardcoded boot id.** Read `/proc` at each mint; the value is a dashed UUID and must be dash-stripped and
   lowercased. Observed at read time: `430d3038-1859-49e6-82cf-5fc475d1b3d0` → journal form
   `430d3038185949e682cf5fc475d1b3d0` (do not hardcode; this changes at the next boot).
8. **Interactive shells may shadow `timeout`.** On this host an unqualified `timeout` resolved to a shell
   function (a direct `--version` produced a clap-style error), while `/usr/bin/timeout` is coreutils 9.11. Use the
   absolute path or let Python bound the child.
9. **`--output-fields` is not a `MESSAGE` filter for the process's own reads.** The claim is limited to the captured
   stream: `MESSAGE` is not in the projection, so it is not on stdout.

## 5. Wrapper / fixture argv contract

The harness passes `--journalctl <wrapper>`; the wrapper receives the canonical argv above and replays the case's
stdout/stderr/rc. What wrappers should assert (parse tokens, do not substring the whole line):

- exactly one of `--user`/`--system`, equal to the case's `scope`;
- `--cursor=` present, attached, and equal to the anchor's cursor; no `--after-cursor`;
- `--output-fields=` exactly `__CURSOR,_BOOT_ID,MESSAGE_ID,UNIT_RESULT,EXIT_CODE,EXIT_STATUS`, no `MESSAGE` token;
- `--no-tail`, `--quiet`, `--output=json` present; `--no-pager` allowed (recommended in the implementation);
- absent: `-b`/`--boot`, `-k`, `-n`, `-f`, `-r`, `-g`, `--since`, `--until`, `-p`, `--facility`, `-t`, `-T`, `-u`,
  `--user-unit`, `--invocation`, `-I`, `-m`, `-M`, `-D`, `-i`, `--root`, `--image`, `--namespace`, `-a`,
  `--cursor-file`, `--show-cursor`, admin commands, and any positional `FIELD=value` word;
- one invocation for non-SETUP cases; zero for SETUP cases; the wrapper's stdin is `/dev/null`.

Integration notes for the harness author:

- If argv equality is pinned as a string, pin the six-field order above and allow `--no-pager`; otherwise a correct
  implementation fails on token order/pager and a wrong one that reorders fields fails only cosmetically.
- Wrappers see the raw cursor in argv (residual: readable from `/proc/<pid>/cmdline` while the child runs). That is
  the non-mutating source of truth; do not add a `--cursor-file` shortcut to hide it.
- The wrapper's own stdout is the case's `stdout`; it must not echo argv to stdout (an argv echo would leak the
  cursor into the stream the canary checks inspect).

## 6. Field projection and predicate sufficiency (argv-adjacent)

The six requested fields are exactly sufficient for the r15 predicates and the continuity checks:

| Need | Fields used |
|---|---|
| anchor continuity | `__CURSOR`, `_BOOT_ID` |
| `positive_kernel_oom` | `MESSAGE_ID` = `fe6faa94e7774663a0da52717891d8ef` |
| `positive_unit_oom` | `MESSAGE_ID` = `d9b373ed55a64feb8242e02dbe79a49c` + `UNIT_RESULT` exactly `oom-kill` |
| `positive_unit_signal` | same `MESSAGE_ID` + `UNIT_RESULT` exactly `signal` |
| `positive_process_sigkill` | `MESSAGE_ID` = `98e322203f7a4ed290d09fe03c09fe15` + `EXIT_CODE` exactly `killed` + `EXIT_STATUS` scalar `9` |

(`corpus/knowledge/journal-positive-evidence-r15.md` §2; spellings S038. The full field/trust truth table is the
FieldDocs lane — not duplicated here.)

Consequences for parsing the projection:

- A record without a class field is still a valid window record; it is simply not a positive. Absence is not `null`
  and not zero. [INFERENCE: the man documents `--output-fields` and the three JSON encoding exceptions, not an
  explicit “absent keys are omitted” sentence. A parser that treats a missing key as a non-match is safe under either
  encoding.]
- `null` (field over 4096 bytes) and arrays (duplicate fields, non-UTF8 bytes) are non-scalar by construction and
  must invalidate the record for the window, matching the r15 rule.
- `EXIT_CODE`/`EXIT_STATUS` are emitted by the service manager (`src/core/unit.c`, S036) and are not documented in
  the installed 261 `systemd.journal-fields(7)` page (observed: that page has no `EXIT_CODE` entry). The names are
  still valid journal fields and journalctl projects them when present.
- The two always-printed timestamp fields are address metadata, not `MESSAGE`; a record-shape test that demands a key
  set equal to the six requested names contradicts the man page.

## 7. Host observations (static metadata only; no record read)

- Persistent journal enabled: `/var/log/journal/432d02b544a5459ebbff9c42ec68334d/` contains active `system.journal`
  and `user-1000.journal` (plus rotated/archived files); `/run/log/journal` is empty. The man says `--user` “only
  works if persistent logging is enabled”, so user scope is structurally available on this host.
- ACLs at read time: `system.journal` has `group:wheel:r--`; `user-1000.journal` has `user:vgpnk:r--` and
  `group:wheel:r-x`. The invoking uid 1000 is in `wheel`. Both scopes are readable without root here; this does not
  turn `-q` into an access proof, and the empty-capture refusal still applies.
- `user-1000.journal` mtime was 2026-10-20 05:52, after the boot start indicated by the boot-id file mtime
  (2026-10-19 22:48) — current-boot user records exist in that file [file metadata only; no record parsed].
- The active file names carry no boot id; rotated names embed an older boot id (`c55f7dd7…`), distinct from the
  current `430d3038…`. This is why the mint compares the `_BOOT_ID` *field*, never a file name.

## 8. Residual unknowns

- CLI behavior of `--cursor=` when the cursor is absent or aliased (S039/S040 describe the libsystemd API; the
  `journalctl` CLI path is undocumented). The exact-first-record refusal covers both outcomes; the recipe names no
  cause for a mismatch.
- Whether this host's journalctl emits any stderr for ordinary scope reads under `-q` (not measured).
- Whether `--output-fields` omits absent keys (inferred; parser is safe either way).
- The order interaction of `-n` and `--no-tail` (undocumented; avoided by never combining).
- Cursor alias frequency and vacuum timing (not measured).
- Whether `timeout` shadowing by an interactive shell function is present in other environments; the absolute path
  avoids it.
- `tools/mori-journal-window.py` and the r16 harness were absent at read time, so none of this is verified against
  the delivered implementation.

## 9. Claims not made

- No live window, anchor, count, or record was produced or measured in this lane.
- No completeness, victim, emitter, alarm, severity, drift, or fleet claim.
- No census cutover, no cursor-state mutation, no anchor advance, no tool install/update.
- No prediction of gate or selftest tallies.

## 10. Tooling record

- None installed or updated. Tools read/used: `/usr/bin/journalctl` (help/version only), local man pages
  (`journalctl`, `systemd.journal-fields`, `timeout`), coreutils `timeout` 9.11 presence check, `jq` presence check,
  `getfacl`/`stat`/`ls`, `git rev-parse`/`git status`.
