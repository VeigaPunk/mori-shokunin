# S172 — man-pages 6.20 PR_SET_NAME.2const (source scout report)

Seat: MoriR31.SrcManPrSetName. Question: do the saved bytes carry that a process can set
its own comm to an arbitrary 16-byte string, so a name match is not identity?

## 1. Fetch

| field | value |
|---|---|
| URL | https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man2const/PR_SET_NAME.2const?h=man-pages-6.20 |
| access time (UTC) | 2026-10-22T23:43:03Z (recorded `date -u +%FT%TZ` immediately before the fetch) |
| HTTP | 200, no redirect (`curl -w '%{url_effective}'` returned the same URL) |
| bytes | 1889 (81 lines) |
| saved unchanged | /fast/scratch/hyaku/mori-r31/SrcManPrSetName/S172.src |
| sha256 | f2ac57cc826943dcd5bc71feea9859099014bc59767b21eafad44a7325be558a |
| content type | `text/troff; charset=us-ascii` (`file -i`); first line `.\" Copyright, Guillem Jover <guillem@hadrons.org>` (S172.src:1) |
| fallback needed? | no — the primary `man/man2const/PR_SET_NAME.2const` path answered at the man-pages-6.20 tag, so `man/man2/prctl.2` was not used |

Command run: `curl -sSL --fail -m 60 -o S172.src -w 'HTTP:%{http_code} SIZE:%{size_download}\n' '<URL>'`
→ `HTTP:200 SIZE:1889`.

Re-fetch stability: a second independent fetch of the same URL at 2026-10-22T23:47Z hashed
`f2ac57cc826943dcd5bc71feea9859099014bc59767b21eafad44a7325be558a` again (`curl … | sha256sum`),
so the C1 counter's measurement-time re-fetch check (.ufo/waves/round-31/count-c1.py:172-174)
should pass on the same URL.

Tag cross-check (observed, not saved): `curl -sSL --fail -m 60 '<prctl.2 at the same tag>' | sed -n '88,94p'`
prints `.B PR_SET_NAME` at line 90 and `.B PR_GET_NAME` at line 92, so man-pages 6.20 carries
both the prctl(2) NAME entries and this separate man2const page.

## 2. Located quotes (verbatim from the saved bytes)

Quotes are the file bytes of each span; roff macros that share the span are inside the quotes.
Line numbers below are from `grep -n` on S172.src. The C1 counter compares whitespace-normalised
text (`norm`, .ufo/waves/round-31/count-c1.py:47 and :171), so a multi-line span written in the
Gate row with single spaces between the lines is still found in the committed copy.

**Q1 — S172.src:26-29 (21 words).** `grep -n 'Set the name of the calling thread'` → 27.

```
.B PR_SET_NAME
Set the name of the calling thread,
using the value in the location pointed to by
.IR name .
```

Fact it supports: the name is set by the calling thread for itself from a caller-supplied
buffer — comm is a self-asserted label, with no target pid and no cross-process write.

**Q2 — S172.src:34-35 (19 words).** `grep -n 'exceeds 16 bytes, the string is silently truncated'` → 35.

```
If the length of the string, including the terminating null byte,
exceeds 16 bytes, the string is silently truncated.
```

Fact it supports: comm holds at most 16 bytes including the null, and anything longer is
silently truncated (S172.src:31-33 also states "The name can be up to 16 bytes long" and ties
the limit to `TASK_COMM_LEN` in `include/linux/sched.h`), so distinct programs can present the
same comm string and two long names can collide after truncation.

**Q3 — S172.src:53-57 (11 words).** `grep -n 'is an invalid address'` → 57.

```
.SH ERRORS
.TP
.B EFAULT
.I name
is an invalid address.
```

Fact it supports: the only documented failure for PR_SET_NAME is EFAULT (bad address); no
EPERM, EACCES or capability check is documented (`grep -ci 'EPERM\|EACCES\|privileg\|CAP_\|uid\|owner' S172.src` → 0), so the page gives no basis for treating comm as a protected or
privileged field. [INFERENCE] "any process can set its own name" follows from self-set plus the
absence of a permission error; the page itself never uses the word "arbitrary" and never says
"a name match is not identity".

Corroborating line, not quoted in the Gate row to stay within three: S172.src:60-63 records that
the attribute is likewise readable at `/proc/self/task/<tid>/comm` (the file `pickle` compares
against when it greps `comm`), and S172.src:43-46 says it is the same attribute set by
`pthread_setname_np(3)`.

## 3. Ready-to-paste rows

Gate row (one physical line; rewrap only at the ` \| ` escapes, never inside a quote):

```
| S172 | https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man2const/PR_SET_NAME.2const?h=man-pages-6.20 | 2026-10-22T23:43:03Z | `f2ac57cc826943dcd5bc71feea9859099014bc59767b21eafad44a7325be558a` | `PR_SET_NAME.2const:26-29` (21 words): ".B PR_SET_NAME Set the name of the calling thread, using the value in the location pointed to by .IR name ."; `PR_SET_NAME.2const:34-35` (19 words): "If the length of the string, including the terminating null byte, exceeds 16 bytes, the string is silently truncated."; `PR_SET_NAME.2const:53-57` (11 words): ".SH ERRORS .TP .B EFAULT .I name is an invalid address." | admit, A, mined |
```

Note for the L1: the row must stay one physical line, and the quotes contain no `"` or `|`, so no
escaping is needed. It satisfies the C1 counter's Gate checks as written: one admit row for S172
whose last cell starts with `admit` (.ufo/waves/round-31/count-c1.py:144-146), an `https://` cell
(:151), a backticked 64-hex sha256 (:152), three quotes in `(N words): "..."` form each with
`len(q.split()) <= 25` (:153), the same sha at re-fetch (:173), and every quote present in
`corpus/evidence/sources-r31/S172.src` after whitespace normalisation (:171). Copy
/fast/scratch/hyaku/mori-r31/SrcManPrSetName/S172.src to that path unchanged to satisfy the copy
check; its sha256 is the one in the row.

SOURCES row (11 columns, order taken from corpus/SOURCES.md:5):

```
| S172 | man-pages 6.20 PR_SET_NAME and PR_GET_NAME operations page (man/man2const/PR_SET_NAME.2const at the man-pages-6.20 tag) — https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man2const/PR_SET_NAME.2const?h=man-pages-6.20 | docs | A | the documented contract of PR_SET_NAME only: the calling thread names itself from a caller-supplied buffer, the name is at most 16 bytes including the terminating null and longer strings are silently truncated, the same attribute is readable at /proc/self/task/<tid>/comm and settable through pthread_setname_np(3), and the only documented error is EFAULT; not the kernel implementation and not a statement that equal names imply identity | `PR_SET_NAME.2const:26-29` (self-set name); `:31-35` (16-byte limit, silent truncation); `:43-46` (same attribute as pthread_setname_np); `:53-57` (ERRORS lists EFAULT only); `:60-63` (/proc/self/task/<tid>/comm); man-pages-6.20 tag; sha256 f2ac57cc826943dcd5bc71feea9859099014bc59767b21eafad44a7325be558a; 1 889 bytes, 81 lines | A comm match is not an identity test: the process writes its own max-16-byte name and over-long names are silently truncated, so two different programs can wear the same comm string and a pgrep or /proc scan cannot tell the fleet watchdog from an impostor by name alone. | mined | 2026-10-22 | on-release | corpus/knowledge/watchdog-identity-r31.md |
```

## 4. Decision

**admit.** Reasons, each checked against the saved bytes:

- The bytes carry the mechanism, not just a mention: self-set name (26-29), 16-byte cap with
  silent truncation (31-35), and an ERRORS list whose sole entry is EFAULT (53-57). A reader
  deciding whether a pid probe identifies the fleet watchdog gets exactly the failure mode a
  name match has.
- Not a 404 and not a challenge page: HTTP 200, no redirect, 1889 bytes of real roff with the
  upstream copyright and SPDX header (S172.src:1-7), and the file parses as the PR_SET_NAME
  page (`.TH PR_SET_NAME 2const`, S172.src:7).
- Not already registered: `grep -n 'PR_SET_NAME\|prctl.2\|man2const' corpus/SOURCES.md` returns
  nothing, and the only `man-pages.git/plain` row in the registry is S149
  (corpus/SOURCES.md:155, the two oom_score proc pages) — a different path. `grep -n '| S172 '`
  on corpus/SOURCES.md returns nothing; the highest id present is S160, so S172 is free.

Caveat the L1 should weigh: the page is a contract page, so the sentence "a name match is not
identity" is the reader's conclusion from the 16-byte self-set field, not a sentence in the
bytes. If the Gate wording demands a source that says the words "not identity", this row does
not supply it; it supplies the three facts that force it. The kernel-side enforcement (silent
truncation at `set_task_comm`, TASK_COMM_LEN) belongs to S163/S164, not here.

## Bounds and tooling

- Wrote only this report and `S172.src` under /fast/scratch/hyaku/mori-r31/SrcManPrSetName/.
  No git or jj command run; no lane file written; no unit started or signalled; no pacman run.
- No tool installed or updated; nothing needed one. curl (host), `sha256sum`, `file`, `grep`,
  `sed`, `wc` already present.
- Processes: each command bounded (`curl -m 60`), nothing left running.
- Privacy: no uid, real pid, unit name, journal text, settings value or session path in this
  report; the placeholder `<tid>` is copied from the page.
