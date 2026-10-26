# Mo49SentCopies — security and hygiene review of corpus/evidence/sources-r49/

Seat: Mo49SentCopies (sentinel, leaf). Lane: mori-shokunin. Round 49, wave w1.
Frozen contract read first: `.ufo/waves/round-49/contract.md` (freeze `0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115`).
Claim surface: C2's four committed source copies and the own-work receipt.

Author date: 2026-10-25 (lane tip at read: `0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115`).
Nothing in the lane was edited. No pacman, no mutating git/jj, no subagent. All reads and scans were read-only;
no lane tool was run for this seat (no TMPDIR scratch directory was created — no tool needed one).

## Files in scope

| file | bytes | sha256 (observed) |
|---|---|---|
| `corpus/evidence/sources-r49/host-journal-reach.txt` | 3026 | `be3952cb6fdac6d6ced15a9a0092447db80fe699221b8478970bb402a558eb12` |
| `corpus/evidence/sources-r49/journalctl.1.html` | 87375 | `75440570fb1f71859229ca88fed0a6764b2057c7dd90651701b3d022a5649722` |
| `corpus/evidence/sources-r49/journald.conf.5.html` | 39204 | `b4a9b53e3e53dc5384bfffeb777218ced4c91712b0222b71405146ab470bc340` |
| `corpus/evidence/sources-r49/systemd-journald.service.8.html` | 28143 | `a7b443568865bb09f45d1ec83f3a8ad0e6a158d4e2cd21053e72499eb5f51212` |

## 1. sha256 pins — PASS

Pins read from `count-c2.py:36-45` (`COPIES`), compared three ways:

```
$ sha256sum corpus/evidence/sources-r49/journald.conf.5.html corpus/evidence/sources-r49/systemd-journald.service.8.html corpus/evidence/sources-r49/journalctl.1.html corpus/evidence/sources-r49/host-journal-reach.txt
b4a9b53e3e53dc5384bfffeb777218ced4c91712b0222b71405146ab470bc340  .../journald.conf.5.html
a7b443568865bb09f45d1ec83f3a8ad0e6a158d4e2cd21053e72499eb5f51212  .../systemd-journald.service.8.html
75440570fb1f71859229ca88fed0a6764b2057c7dd90651701b3d022a5649722  .../journalctl.1.html
be3952cb6fdac6d6ced15a9a0092447db80fe699221b8478970bb402a558eb12  .../host-journal-reach.txt
EXIT=0
```

Committed-at-freeze bytes (`git show 0df17b7b…:corpus/evidence/sources-r49/<f> | sha256sum`) print the same four
digests, and `git status --porcelain corpus/evidence/sources-r49/` is empty — worktree, index and freeze commit
agree, so the contract's `git show <freeze>:<path>` fallback is not needed. All four are `100644` blobs
(`git ls-files -s`), regular files, no symlinks, no `.gitattributes`, therefore no clean/smudge filter or LFS
pointer can stand in for the bytes the counter reads.

## 2. Size against the 1 MiB named-directory rule — PASS, none need explicit naming

`scripts/hyaku/lane-addendum.md:226-228` states that a named directory commits like `git add <dir>` and that
*new files over 1 MiB inside it are skipped with a warning*. Observed sizes:

```
$ stat -c '%n %s' corpus/evidence/sources-r49/* | awk ...
host-journal-reach.txt 3026 bytes (0.003 MiB) ok
journalctl.1.html      87375 bytes (0.083 MiB) ok
journald.conf.5.html   39204 bytes (0.037 MiB) ok
systemd-journald.service.8.html 28143 bytes (0.027 MiB) ok
$ du -sh corpus/evidence/sources-r49/   ->  160K
```

Largest file is 87,375 bytes = 0.083 MiB, 12× under the cap. **No file in this directory needs to be named
explicitly for the size rule**, and all four are already named individually by `count-c2.py`'s `COPIES` pins
(`SRC_DIR + "<name>"`), so the C2 arm never depends on directory expansion.

Discrepancy noted while checking (not a defect in this directory): the implemented guard in
`scripts/hyaku/jj-lane.sh:638` is 10 MiB on *named files* (`--allow-large`), and `grep -c 1048576
scripts/hyaku/jj-lane.sh` = 0 — the documented 1 MiB directory skip has no matching code in the helper I read.
Not this seat's file to fix; recorded for the closure.

## 3. Machine-id masking in the receipt — PASS

`grep -c -F "$(tr -d '\n' < /etc/machine-id)"` per file (the id itself is not reproduced here):

```
host-journal-reach.txt:           0
journalctl.1.html:                0
journald.conf.5.html:             0
systemd-journald.service.8.html:  0
```

Same count for the upper-case form: 0 in all four. The receipt substitutes the placeholder `MACHINE_ID` in both
journal lines that embed the journal directory (`/run/log/journal/MACHINE_ID`, `/var/log/journal/MACHINE_ID`),
matching the report convention. The 16-hex prefixes of the id: 0 occurrences. The receipt is 98 lines, max line
length 124, ends with `\n`, and contains no percent-encoded or entity-encoded blob that could hide the id
(`(%[0-9A-Fa-f]{2}){4,}` → no match).

## 4. Credential material, tokens, cookies, private URLs, `op://` — PASS

Two passes over all four files (regex, then manual read of the 98-line receipt):

```
$ grep -n -iE 'op://|BEGIN [A-Z ]*PRIVATE KEY|password[[:space:]]*[:=]|passwd[[:space:]]*[:=]|api[_-]?key|secret[[:space:]]*[:=]|token[[:space:]]*[:=]|cookie|set-cookie|session[_-]?id|authorization:|bearer |sk-[A-Za-z0-9]{10}|gh[pousr]_[A-Za-z0-9]{10}|github_pat_|AKIA[0-9A-Z]{12}|xox[baprs]-|://[^/[:space:]]+:[^/[:space:]]+@' *.html host-journal-reach.txt
(no output)
$ grep -oE '(https?://(localhost|127\.0\.0\.1|10\.[0-9.]+|192\.168\.[0-9.]+|172\.(1[6-9]|2[0-9]|3[01])\.[0-9.]+)[^ "]*|[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}|([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2})' *.html host-journal-reach.txt
(no output)
```

All outbound URLs are public documentation hosts, in anchor text only: `man7.org` (19), `systemd.io` (7),
`uapi-group.org`, `eprint.iacr.org`, `developer.mozilla.org`, `pcre.org`, `linux.die.net`,
`tools.ietf.org`, `code.jquery.com` (see finding 2), plus relative manual-page links. No `op://`, no userinfo in
any URL, no email address, no MAC address, no private-range URL.

Absolute host paths are limited to generic system paths required by the claim — `/etc/systemd/journald.conf`,
`/etc/systemd/journald.conf.d/size.conf`, `/var/log/journal`, `/run/log/journal`, `/run`, `/dev/console`,
`/usr/`. No `/home/<user>`, `/Users/`, `/root`, `/tmp`, `/opt`, `/srv`, `/mnt`, `/media`, no repository path,
and the lane user name does not appear (`grep -nE "$(id -un)|/home/" host-journal-reach.txt` matches only the
`#RateLimitBurst=10000` default line, which is the substring `1000`). This is informational, not a finding.

## 5. Executable content in the HTML copies — two `<script>` per file, no SRI, no CSP

Every tag class that can execute on open was enumerated:

| vector | result |
|---|---|
| `<script>` | **2 per file** (see below) |
| inline script body (`<script>…</script>`) | 0 |
| `<iframe>` `<frame>` `<frameset>` `<object>` `<embed>` `<applet>` | 0 |
| `<meta http-equiv="refresh">` | 0 |
| `on*=` event-handler attributes | 0 |
| `javascript:` URL | 0 |
| `data:` URL | 0 |
| `<svg>` / `<math>` (foreign content) | 0 |
| `ping=` | 0 |
| `integrity=` / `crossorigin` / `Content-Security-Policy` | 0 |
| `<link>` (external stylesheet) | 0 |
| `<img>` / `src=` other than the two scripts | 0 |
| `@import` / `url(` in the inline `<style>` | 0 |
| `eval(`, `fromCharCode`, `atob(`, `btoa(`, `new Function`, `document.cookie`, `localStorage`, `WebSocket`, `XMLHttpRequest`, `fetch(` | 0 |
| long base64-ish runs (`[A-Za-z0-9+/]{80,}`) | 0 |
| HTML comments (`<!--…`) | 0 |
| `file://`, `wget`, `curl/`, `ETag`, `Last-Modified`, `localhost` | 0 |

The two script tags are identical in all three files and sit at the very start of `<body>`:

```
$ grep -n -o '<script[^>]*>' *.html
journalctl.1.html:1:<script src="https://code.jquery.com/jquery-3.7.1.min.js">
journalctl.1.html:1:<script src="../nav.js">
journald.conf.5.html:1:<script src="https://code.jquery.com/jquery-3.7.1.min.js">
journald.conf.5.html:1:<script src="../nav.js">
systemd-journald.service.8.html:1:<script src="https://code.jquery.com/jquery-3.7.1.min.js">
systemd-journald.service.8.html:1:<script src="../nav.js">
$ grep -abo '<script' <file> | head -1     # journalctl 184, journald.conf 187, systemd-journald.service 198
```

They are part of the fetched upstream bytes (DocBook `Vsnapshot` template), not an injection into the copy — but
they are now committed lane content that executes if the file is opened, and they carry no text the C2 counter
can use: `count-c2.py:60` drops `<script|style>` blocks before matching, so removing them changes no quote.

Control characters and confusables: `host-journal-reach.txt` and `systemd-journald.service.8.html` are free of
C0/C1, zero-width, bidi-override (U+202A-U+202E, U+2066-U+2069, U+061C) and line/paragraph-separator
characters; `journalctl.1.html` has 8 and `journald.conf.5.html` 2 NBSP (U+00A0) and nothing else. NBSP is
collapsed by `normalise()`'s `\s+` rule, so it cannot smuggle a visually different quote past the counter, and
there is no RLO that could reorder a quoted span on screen.

## 6. Receipt command hygiene — read-only, no privilege, no mutation

```
$ grep -n '^\$ ' corpus/evidence/sources-r49/host-journal-reach.txt
4:  journalctl --disk-usage
8:  journalctl --system --disk-usage
12: journalctl --user --disk-usage
16: systemd-analyze cat-config systemd/journald.conf
75: stat -c '%n %s bytes mtime %y' /etc/systemd/journald.conf.d/size.conf
79: findmnt -no FSTYPE /run
83: findmnt -no FSTYPE /var/log/journal
86: ls -A /run/log/journal
89: journalctl --list-boots --no-pager
95: journalctl -b 0 -u systemd-journald --no-pager -q -g 'Journal .* is .*max'
```

`grep -E 'sudo|systemctl|vacuum|rotate|--flush|--sync'` over those ten headings: no match. Consistent with the
header claim (`no vacuum, rotate or config change was run`). `-q` (quiet) and `-g` semantics are as the
committed `journalctl.1.html` defines them.

---

## Findings

### F1 — MED — `corpus/evidence/sources-r49/host-journal-reach.txt:96,97` — live hostname committed, while the machine id on the same two lines is masked

The receipt masks `MACHINE_ID` in both journald lines but leaves the hostname in the syslog preamble of the same
two lines (`grep -c -F "$(uname -n)"` → 2). The hostname is a stable host identifier of the same class as the
machine id that the report rule redacts, and it is the only occurrence of that string anywhere under `corpus/`
(`grep -rl -F "$(uname -n)" corpus/` → `corpus/evidence/sources-r49/host-journal-reach.txt` only). No prior
committed corpus file carries a hostname in journal format (`grep -rl 'systemd-journald\[' corpus/` returns only
this receipt), so this is a new disclosure class, not a reproduced convention.

Exploit path: a reader who wants to correlate this lane's host with any other published journal or `journalctl`
snippet gets an exact host label plus the boot window (`2026-10-25 13:36:19`-`20:43:03 -03`) and the drop-in
mtime; the machine id alone was already redacted, so the redaction pass was mechanical (one regex) rather than
considered.
Impact: de-anonymization of the lane host in a public corpus artifact; no credential, no access.
Smallest remediation: replace the hostname with `HOST` on lines 96-97 (both lines are inside the `-g` capture;
see F4 for that command). Because the copies are pinned by sha256 in the frozen `count-c2.py`, the corrected
receipt needs a re-pin — which the contract forbids after a seat has scored, so the L1 must either accept the
hostname as a named limit in the entry or re-freeze the receipt and its pin.

### F2 — MED — `journalctl.1.html`, `journald.conf.5.html`, `systemd-journald.service.8.html` (byte 184/187/198) — the committed copies fetch and execute remote third-party JavaScript when opened

Each copy begins `<body>` with `<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>` and has no
`integrity=` (SRI) and no CSP meta. Opening the copy as an HTML document — the natural way for a wave-2 reviewer
to "re-open every row against the page text" (`contract.md`, C2 named limits) — executes whatever
`code.jquery.com` serves for that path today, in the file's origin.

Exploit path: CDN compromise, DNS/TLS interception with a trusted CA, or a mirror in front of the CDN substitutes
the jQuery payload; the reviewer's browser runs it in a `file://` context, which in Firefox can read files in the
document's own directory — i.e. the other three copies and anything else committed beside them.
Impact: remote code execution in the browser of the person verifying the claim; the counting path itself is safe
(`count-c2.py` reads bytes, and `normalise()` drops script blocks).
Smallest remediation: strip the two `<script>` tags from the committed copies before re-pinning (they contribute
no quotable text), or keep the copies as extracted text (`.txt`) next to the byte-exact HTML kept out of the
commit. If the bytes must stay exact, add a `README` line in `corpus/evidence/sources-r49/` telling readers not
to open the HTML in a browser and to read it with `grep`/`sed` instead.

### F3 — MED — `../nav.js` in the three copies resolves to `corpus/evidence/nav.js`, a lane-owned path that has never existed

The second script tag is relative: from
`file://…/mori-shokunin/corpus/evidence/sources-r49/<page>.html` it resolves to
`file://…/mori-shokunin/corpus/evidence/nav.js`. That file does not exist
(`ls corpus/evidence/nav.js` → No such file; `git log --all -- corpus/evidence/nav.js` → empty; `git ls-files |
grep nav.js` → empty), so today the tag is a 404. But the directory is lane-writable and inside the round's
commit scope, so any future commit of `corpus/evidence/nav.js` — by any seat, in any round — turns three inert
copies into loaders for lane-authored JavaScript that runs with `file://` privileges as soon as a reviewer opens
one.

Exploit path: a seat (or anyone with commit access to `corpus/evidence/`) adds `nav.js`; a reviewer opens a copy
to check a quote; the lane-authored script runs in the reviewer's browser and can read sibling files.
Impact: the copies' safety silently depends on the absence of a file nobody is watching; the dependency is
invisible because the missing file produces no error a reviewer would see.
Smallest remediation: same as F2 (remove the tags). If the tags stay, add `corpus/evidence/nav.js` to the
lane's ignore list and a guard that fails if it ever appears — otherwise the copies are one `git add` away from
being an injection point.

### F4 — HIGH (claim provenance) — `corpus/evidence/sources-r49/host-journal-reach.txt:95` — the receipt is captured with a MESSAGE grep, which the frozen S351 flip condition excludes

Line 95 is `journalctl -b 0 -u systemd-journald --no-pager -q -g 'Journal .* is .*max'`, and the lane's own
committed copy defines that filter as a MESSAGE-field match:

```
$ grep -o '.\{0,200\}--grep.\{0,300\}' corpus/evidence/sources-r49/journalctl.1.html
<code class="option">-g</code>, --grep=  Filter output to entries where the <code class="varname">MESSAGE=</code> field matches the …
```

`contract.md` states the S351 flip this claim is built on as "the public --vacuum-size= sentence plus a committed
read-only disk-usage receipt, **and no MESSAGE grep**", and repeats "no MESSAGE grep" in the C2 paragraph. Lines
96-97 — the `Runtime Journal … is 8M, max 64M` and `System Journal … is 45M, max 256M` lines, the only evidence
for the host's effective ceilings — exist in the receipt solely because of that `-g` MESSAGE grep.

This does not break P-C2's mechanical predicate (the counter only requires each quote to occur in a committed
copy), but it breaks the condition the claim states it satisfies, and wave 1 seats have already planned quotes
from those lines: `grep -rln 'is 8M, max 64M\|is 45M, max 256M' .ufo/waves/round-49/w1/` → `Mo49ExecQuotesHost.md`,
`Mo49ScribeEntryA.md`, `Mo49ScribeRowHost.md`, `Mo49ScoutStagedJournal.md`, `Mo49ScribeLogEntry.md`,
`Mo49ScribeQuality.md`. A wave-2 reviewer checking the flip literally will call C2 unmet on its own stated
condition.

Exploit path (non-security analogue): the claim's evidence reaches one step further than the rule it claims to
satisfy, in exactly the way S351 was originally rejected for.
Impact: C2 fails its stated supersede condition at wave 2 while its counter prints `met` — the classic
claim-stronger-than-its-evidence shape.
Smallest remediation: one of — (a) re-capture the ceilings with a non-MESSAGE route (`systemd-analyze cat-config`
already in the receipt plus `stat`/`du` of the journal directories gives the caps without any MESSAGE read) and
re-pin, (b) drop rows that rest on lines 96-97 and let the entry state the ceilings only as configured values,
or (c) amend the claim's flip wording in a lesson, not in the frozen contract.

### F5 — LOW — `corpus/evidence/sources-r49/host-journal-reach.txt:89-92` — two 32-hex boot IDs and PID 1025 are retained

`journalctl --list-boots` keeps both BOOT IDs (`0a3785aa…`, `7ab69ee4…`) and the journald lines keep PID 1025.
Neither is the machine id (both differ from `/etc/machine-id`, which appears 0 times) and neither is a credential,
but a boot ID is a per-boot correlator that links this receipt to any other publication of the same boot's
journal.

Exploit path: cross-correlation only, and only if another artifact publishes the same boot.
Impact: none on its own; it compounds F1.
Smallest remediation: none required. Recorded so the entry's limits are honest about what the receipt identifies.

### F6 — LOW — `corpus/evidence/sources-r49/host-journal-reach.txt:1-2` — the receipt is a curated transcript, and its header does not say so

The header claims a capture at `2026-10-25T20:43:09-03:00` and a read-only session. The body is not a raw
transcript: prompt lines are re-formatted, `[exit N]` markers are appended, the whole `cat-config` dump is pasted
under one command, and the machine id was substituted with `MACHINE_ID` (F1's counterpart edit). Every edit is
either formatting or a redaction, and no edit adds a claim — but an undisclosed redaction weakens the receipt's
standing as raw evidence precisely in the review where its standing is the question.

Exploit path: a wave-2 reviewer treats the paste as contiguous output and infers that the shown configuration was
the host's whole configuration at one instant; the drop-in is shown as a separate file *with* its own command,
so the inference is supportable here, but the receipt does not state its editing rules.
Impact: provenance ambiguity, no false claim observed.
Smallest remediation: one header line in a future receipt (`transcript: command headings, exit markers and
MACHINE_ID substitution added by the seat; no output line edited`).

---

## Scope statement

Checked: sha256 pins (worktree, index, freeze commit), file size against the 1 MiB rule, machine-id and
upper-case variants, credential/token/cookie/session/`op://` patterns, public-versus-private URLs, every
HTML vector that can execute or auto-fetch on open, control/bidi/zero-width characters, absolute host paths,
`sudo`/mutating commands in the receipt, and the receipt's identifier content (hostname, boot IDs, PIDs, paths).
Not checked, out of this seat's surface: whether the committed bytes match what freedesktop.org serves today
(the pins prove freeze integrity only, as the contract already names); the correctness or word counts of the C2
quotes; `SOURCES.md` rows; the C1 tool and counter.

Report: .ufo/waves/round-49/w1/Mo49SentCopies.md
