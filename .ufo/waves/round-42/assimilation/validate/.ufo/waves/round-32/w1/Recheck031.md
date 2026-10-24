# Recheck031 — S031 (C1 freshness, round 32 attempt 2)

Seat: MoriR32A2.Recheck031. Verdict: **current**.
Scratch: `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck031/`

## 1. Fetch

- id: S031
- url: https://man7.org/linux/man-pages/man7/pipe.7.html
- fetched: `2026-10-23T01:31:21Z` (access time recorded at fetch), curl exit 0, HTTP 200
- redirect: none — `curl -sSL -o /dev/null -w '%{url_effective}'` printed
  `https://man7.org/linux/man-pages/man7/pipe.7.html` with `200`, `size_download 21870`
- bytes saved unchanged: 21870
- sha256: `22809fe16836722f0359b10b59b4c0971cf3edf6ffb26528c41bd1a383f2a58e`
- copy: `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck031/S031.src` (21870 bytes)
- normalised text: `S031.text` (12112 bytes, from `seat-check.py text`)
- page identity: colophon reads `Linux man-pages 6.19 2026-07-10` (S031.text, COLOPHON), matching
  the anchor's "man-pages 6.19".

## 2. Ready-to-paste row

```markdown
| S031 | https://man7.org/linux/man-pages/man7/pipe.7.html | 2026-10-23T01:31:21Z | 22809fe16836722f0359b10b59b4c0971cf3edf6ffb26528c41bd1a383f2a58e | "If all file descriptors referring to the read end of a pipe have been closed"; "a write(2) will cause a SIGPIPE signal to be generated for the calling process" | current |
```

## 3. Quote → teaches-cell bearing

teaches: "When all pipe read ends close, a write generates SIGPIPE; that pipe behavior
explains a producer failure after an early-exiting consumer."
scope: "pipe write behavior when readers close and SIGPIPE generation".

1. `"If all file descriptors referring to the read end of a pipe have been closed"` — the
   precondition clause of the SIGPIPE rule: every read-end descriptor closed (the
   early-exiting-consumer condition). Bearing on scope "readers close". Verbatim match in
   S031.text: `in_copy=True`, 15 words, starts/ends on whole words.
2. `"a write(2) will cause a SIGPIPE signal to be generated for the calling process"` — the
   consequent clause: a write after that close generates SIGPIPE for the writer (the
   producer). Bearing on teaches "a write generates SIGPIPE" and scope "SIGPIPE generation".
   Verbatim match: `in_copy=True`, 14 words.

Together the two quotes are the man page's complete sentence, so the verdict follows: the live
page still states exactly the mechanism the teaches cell asserts, hence `current`. Neither
quote is page furniture, drops a negation, or contains `&`/pipes/typographic characters; both
were copied from `seat-check.py text` output, not the rendered page.

The `used-by` file `corpus/knowledge/verdict-contract-r13.md` quotes this same sentence verbatim
at lines 39-40 ("If all file descriptors referring to the read end of a pipe have been closed,
then a write(2) will cause a SIGPIPE signal to be generated for the calling process"), and
attributes the mechanism in its steps 3-4 (lines 36-40): the `sed` producer gets SIGPIPE and
exits 141 after `grep -Fxq` closes stdin. That is the teaches cell's own claim, still supported
by the live page — no correction needed.

## 4. seat-check output

```
$ timeout 300 python3 .ufo/waves/round-32/seat-check.py row S031 S031.src '"If all file descriptors referring to the read end of a pipe have been closed"; "a write(2) will cause a SIGPIPE signal to be generated for the calling process"'
sha256=22809fe16836722f0359b10b59b4c0971cf3edf6ffb26528c41bd1a383f2a58e
quotes=2 words=[15, 14] in_copy=[True, True]
shared_tokens=['pipe', 'sigpipe', 'write'] topic_ok=True
live_quotes_ok=True
ROW_CHECK=pass (judge R4 and R5 not checked here)
EXIT=0
```

## 5. Drift details

None. Verdict `current`, so no `Round32` correction is drafted.

Adjacent observation (does not change the row): the same page still states the capacity fact the
knowledge file cites at line 37 — "Since Linux 2.6.35, the default pipe capacity is 16 pages"
(S031.text, "Pipe capacity") — and adds the Linux 4.5 soft-limit caveat ("the default pipe
capacity is lower than 16 pages when the pipe-user-pages-soft limit is exceeded"). This nuance
concerns the capacity sentence, not the SIGPIPE sentence the population scope names, so the row
stays `current`.

## Tooling

No installs or updates were made for this seat.
