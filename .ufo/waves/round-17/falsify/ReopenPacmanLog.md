# ReopenPacmanLog — fresh attack on SOURCES row S048 (pacman.conf(5) LogFile)

Seat: `MoriR17.ReopenPacmanLog-4`, wave 2, leaf scout. Assigned row: **S048** only.
Producer this attack is subject to: L1 `MoriR17` (planner and sole integrator); no admission
verdict is claimed here. This is a fresh re-open, not an independent closure.

- URL attacked: https://man.archlinux.org/man/pacman.conf.5 (row `source`), plus its canonical
  raw artifact https://man.archlinux.org/man/pacman.conf.5.en.raw.
- Access date: **2026-10-20** (fresh fetch by this seat, not replayed from the wave-1 receipt).
- Registry row attacked: `corpus/SOURCES.md:54`; lesson gate row: `corpus/lessons/round-17.md:54`
  (access-date header `:42`, census sentence `:56-58`); opening receipt re-read, not trusted as
  evidence: `.ufo/waves/round-17/build/SrcPacmanLog.md:1-34`.

## 1. Fresh fetch and located quote

Commands (lane root, this seat):

```
curl -sS -L -o /dev/null -w 'http=%{http_code} bytes=%{size_download} url=%{url_effective}\n' \
  https://man.archlinux.org/man/pacman.conf.5
# rc0 -> http=200 bytes=28242 url=https://man.archlinux.org/man/pacman.conf.5
curl -sS -L https://man.archlinux.org/man/pacman.conf.5.en | sha256sum
# rc0 -> 75f404eae751475bd8f9c867fb166d87ca0339644e05df8df0df766f2f172e92
curl -sS -L https://man.archlinux.org/man/pacman.conf.5.en.raw | nl -ba   # rc0
pacman --version | head -3                                               # rc0, Pacman v7.1.0 - libalpm v16.0.1
man -P cat 5 pacman.conf | grep -n -A4 'LogFile ='                       # rc0, local lines 79-82
```

Observed locations:

- Raw roff (`pacman.conf.5.en.raw`): metadata at `:1-10` — `.\" Date: 2026-10-15`,
  `.\" Source: Pacman 7.1.0`; `.TH "PACMAN\&.CONF" "5" "2026\-10\-15" "Pacman 7\&.1\&.0"`.
  Section `OPTIONS` at `:78`. Directive and paragraph at `:123-126`:
  `\fBLogFile =\fR /path/to/log/file` /
  `Overrides the default location of the pacman log file\&. The default is` /
  `/var/log/pacman\&.log\&. This is an absolute path and the root directory is not prepended\&.`
- Rendered English HTML: `OPTIONS` at `:99`, `LogFile` at `:134`, description at `:135-137`.
  Version footer `Pacman 7.1.0` at `:442`; page title `:8`.
- Local `man -P cat 5 pacman.conf`: same paragraph at lines `79-82`, i.e. the anchor's
  "local manual" cross-check is real, and the installed pacman is the same 7.1.0.

The lesson quote at `corpus/lessons/round-17.md:54` is the rendered sentence:

> Overrides the default location of the pacman log file. The default is /var/log/pacman.log.

It is a contiguous verbatim substring of raw `:125-126` after roff `\&.` rendering; whitespace-split
count is **13 words** (≤25). The row uses curly outer quotation marks only (U+201C/U+201D); the
inner text is ASCII and contains no backslash-escaped quotes, so unlike S041/S042/S044 the
byte-transcription class defect D1 of sibling reports does **not** recur here
(`grep -o '^| S048 ' corpus/SOURCES.md` → one occurrence; row has 11 cells, 407 bytes).

The quoted passage is the first two sentences of a three-sentence paragraph; the third sentence
("This is an absolute path and the root directory is not prepended.") is omitted. The quote is
still contiguous and compliant; the omission matters only for N1 below.

## 2. Field-by-field verdict on `corpus/SOURCES.md:54`

| Field | Row value | Verdict |
|---|---|---|
| id/source | `S048`; `pacman.conf(5) LogFile — https://man.archlinux.org/man/pacman.conf.5` | **agree.** One occurrence, 11 cells, IDs contiguous S001–S048, next unused after S047; URL resolves 200 today. |
| kind | `docs` | **agree.** Official manual page. |
| tier | `A` | **agree.** Contract v1 (`/home/vgpnk/Projects/shokunin/CORPUS.md:93-97`) admits official docs as A; same convention as S014/S015/S027/S039/S040. The manual is authoritative for the LogFile default/override scope. |
| scope | `package action-log location and override` | **agree, narrow.** Page documents the pacman log location and override; "action" is grounded by the page's own `UseSyslog` wording ("Log action messages", raw `:229-233`). Root interaction is outside the row's scope (N1). |
| anchor | `LogFile directive; pacman v7.1.0 local manual, live page opened 2026-10-20` | **agree on content; under-specified per contract wording (N2).** Version is real: raw metadata `Pacman 7.1.0`, local pacman v7.1.0, live footer 7.1.0. The directive is unique on the page and locatable (one `LogFile` occurrence, raw `:123`). The anchor does not name `OPTIONS` or a line. |
| teaches | `The default action log is /var/log/pacman.log and LogFile overrides it; this location documentation does not promise actor attribution in each record.` | **agree, with the semantic boundary in N4.** First clause is exactly raw `:125-126`. Second is an absence-of-documentation claim: the page's only logging directives are `LogFile` (raw `:123-126`) and `UseSyslog` (raw `:229-233`); neither states record fields or an actor/uid. `DownloadUser` (raw `:266-269`) mentions "the user running pacman" for downloads only, not log attribution. |
| status | `queued` | **agree.** Contract v1 (`CORPUS.md:103-104`): queued = opened, worth mining; no knowledge entry cites it (see §3). |
| opened | `2026-10-20` | **agree.** Today; fresh fetch 200. |
| recheck | `on-release` | **agree.** URL serves the current Arch pacman man page (not a version-pinned permalink); the anchor's v7.1.0 is the pin, so on-release is the right cadence. |
| used-by | `—` | **agree.** No knowledge entry or lesson rests on S048's fact. Lesson `:54` is the row definition, `:56-58` a census mention, not a use. |

## 3. Used-by / status links and the dependency question

- `grep -rn 'S048' corpus/knowledge/` → **0 hits**; `grep -rln -i 'pacman' corpus/knowledge/` →
  **0 files**. So there is no knowledge entry that cites S048, and the dependency test is
  negative by construction: S048 is **not decorative** (nothing pretends it supports a claim)
  and **not load-bearing** (no admitted entry changes if it is rejected).
- The only round text that names the default log path is the cross-domain section
  `corpus/lessons/round-17.md:90` ("`build/PacmanTxnToday.md` locates `/var/log/pacman.log:2462`").
  That report reads the file directly (`build/PacmanTxnToday.md:3-5`) and never cites S048; the
  lesson does not cite S048 there either. So the location fact is observed, not sourced from
  this row.
- Status/used-by consistency was also checked against the census: `corpus/SOURCES.md` now has
  48 rows, statuses `mined=25 / queued=22 / rejected=1`, tiers `A=45/B=2/C=1`; the entering
  commit `24526ea` had `40` rows with `19/20/1` and `37/2/1` —
  `.ufo/waves/round-17/evidence/source-count.json` stdout reproduces exactly that. Existing
  rows S001–S040 are byte-identical between `24526ea` and `273aa74` (`git show` line diff rc0),
  so the lesson's "No existing status, recheck or used-by cell changes" (`:56-58`) holds.
- `build/CriticFrontier.md:152-154` already declares S042/S048 "fine as `queued` with `—`" and
  not counted toward the sourced-claim requirement. That matches the observed links.

Consequence for L1: S048 satisfies the registry shape and the lesson gate; it supplies no
evidence for C1/C2/C3. If L1 intended it to ground the pacman cross-domain narrative, that
citation is absent, but `queued` makes the absence declared rather than concealed.

## 4. Defects and limitations

**No material falsifier.** Every immutable cell matches the live page and the local manual.
The following are limitations, not row falsifications.

**N1 (scope completeness; informational).** The page qualifies the flat default, and the row
does not carry the qualification. `RootDir`'s note (raw `:83-84`, rendered `:104-106`) says:
"If database path or log file are not specified on either the command line or in pacman.conf(5),
their default location will be inside this root path." The same `LogFile` paragraph continues
with the absolute-path rule (raw `:126`). So the row's "default is /var/log/pacman.log" is true
at the default `RootDir` (and on this host: `/etc/pacman.conf` has no `LogFile`, only `[options]`
at `:3`), but it must not be read as root-independent. This matters only to the wave-1 draft,
which did carry the broader clause (`build/SrcPacmanLog.md:24`: "with an absolute path that the
installation root does not prefix"), and to `build/SrcPacmanLog.md:31`, which explains a `-r /mnt`
invocation appearing in the host log by "the man-page rule that the path is absolute regardless
of the installation root". The registered row correctly dropped that clause. The receipt's
example argv is also elided (`…`) and in fact carried `--config=/tmp/pacman.conf.Cab7`, so its
inference is `[INFERENCE]`, not established by this row. No registered claim depends on it.

**N2 (anchor precision; informational).** Contract v1 (`CORPUS.md:99-100`) asks for an exact
section/heading/page/line plus revision. "LogFile directive" is unambiguous (one occurrence)
and v7.1.0 is a real revision, but the enclosing `OPTIONS` section and line are absent. Exact
location confirmed today: raw `:123-126`, rendered `:134-137`, local man `:79-82`. A sharper
anchor would read "OPTIONS, LogFile (raw 123-126); Pacman 7.1.0".

**N3 (unregistered companion; informational).** Wave 1 also opened pacman(8) `--logfile` and put
its quote in the draft gate (`build/SrcPacmanLog.md:14,18`), verified verbatim today at raw
`pacman.8.en.raw:231-233` ("Specify an alternate log file. This is an absolute path, regardless
of the installation root setting.", 16 words; same Pacman 7.1.0, Date 2026-10-15). The registered
row and the lesson gate carry only pacman.conf(5), which is self-consistent. The census's
"included 8 … excluded 0" (`SOURCES.md:81`) is correct if it counts registered references and
treats pacman(8) as an S048-family companion; it would be a ninth opened reference under a
strict distinct-URL reading. No row or claim is wrong.

**N4 (semantic boundary; informational).** The `teaches` clause "does not promise actor
attribution in each record" is about the documentation's silence, not about `pacman.log`'s
record content. Verified: the page has no record schema, uid, or invoker statement; its only
other log directive is `UseSyslog` (destination `/var/log/messages`, raw `:229-233`), and
`DownloadUser`'s "user running pacman" (raw `:268`) is a download privilege. The stronger
actor-absence finding in `build/PacmanTxnToday.md`/`PacmanActorTrace.md` rests on the file sample
and is already labelled inference in its own report. Do not cite S048 as evidence of what the
log does not contain.

**N5 (dependency; no defect).** `used-by —` and `queued` are accurate; the row is inert by
declaration (`CriticFrontier.md:152-154`). No link is missing for a claim that exists.

## 5. Attacked and found sound (no blanket pass)

- URL resolution and content: 200, 28242 bytes, sha256 `75f404ea…`, raw artifact metadata
  Pacman 7.1.0 / 2026-10-15.
- Quote: verbatim contiguous, 13 words, located at OPTIONS/LogFile; no escaped-quote or
  word-count defect.
- Version consistency: raw metadata, HTML footer, installed `pacman --version`, and local man
  all say 7.1.0.
- Tier A, kind `docs`, scope narrowness, status `queued`, opened date, on-release recheck,
  `used-by —`, next-unused ID, 11-cell row.
- Census arithmetic 40→48 / 19→25 / 20→22 / 1→1 and no edits to S001–S040.

## 6. Remaining unknowns

- [UNKNOWN] Whether an independent non-author verifier has re-opened this URL outside an
  L1-dispatched seat. This seat is wave-2 fresh and non-author to the row, but still
  L1-dispatched; that is not outside closure by itself.
- [UNKNOWN] Whether L1 wants the RootDir qualification captured in a future row or a
  supersession; no registry edit was made here.
- [UNKNOWN] Whether the pacman(8) `--logfile` page should be registered as its own row or
  explicitly named as the S048 companion in the lesson; either reading leaves S048 correct.

## 7. Procedure / tooling

- No install or update performed; used existing `curl`, `grep`, `sed`, `awk`, `man`,
  `sha256sum`, `pacman --version`, and read-only `git show`.
- No VCS mutation, no background job, no journal query, no credential/transcript read, no
  `/tmp` or scratch writes, no probe output retained.
- Only this report was written; `corpus/SOURCES.md`, the lesson, knowledge entries, and fleet
  files were not edited.
