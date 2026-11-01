# Round 64 — mori (L1 MoriR64, first on-host freshness sweep + Windows runway capability)

author: mori L1 (MoriR64)
round: 64
date: 2026-10-31
entering: `6e70931d`

## Fresh start (r59–r61 rejected closures re-read; what was ruled out)

The §7 digests name r59/r60/r61 `rejected-honest-stop`; the fleet MANIFEST
records rounds 62 and 63 `admitted` — the state is noted here and the
fresh-start duty was performed on the three listed rounds as bound.
Spot-checks run this round (receipt
`.ufo/waves/round-64/evidence/freshstart-spotchecks-r64.txt`):

- the r61 honest stop re-derived from the frozen counter at the r61 data tip:
  `python .ufo/waves/round-61/count-c2.py 986d4b46…` → `C2=unmet` with all 14
  `quote_words:` anchors listed, rc 1 — same verdict the r61 closure reached.
- r59/r60 cited evidence `git cat-file -e` PRESENT at
  `986d4b46…:.ufo/waves/round-59/evidence/control-c2-do-nothing.txt` and
  `b3c25613…:.ufo/waves/round-60/evidence/c2-at-freeze.txt`; both revisions
  `merge-base --is-ancestor` of refs/heads/master, rc 0 each.

Ruled out as r64 claims, and why: (1) re-declaring entry-claims-class depth
on the r59/r60 instruments — the met-flip counterexamples stand on frozen
bytes; (2) scalar score moves — no closure states a new number and no lane
convention licenses an L1-authored scalar; (3) claims resting on the old
Linux host's live surfaces (journalctl, cgroupfs, `/proc/pressure`, tmux,
`df`-on-`/tmp`) — absent here, honestly `unavailable`, never zero; (4) SKILL.md
gate-registry row edits — parsed and baseline-bound by the reconciler, L0
class. The declared pair C1+C2 is each unreachable by a do-nothing round
(`.ufo/waves/round-64/evidence/controls-r64.txt`).

## Carry-ins from the r63 non-author closure (all six discharged)

1. D1 → `corpus/lessons/round-63.md` mistake 5 relocated from the
   `## Assimilation` tail to `## Mistakes` verbatim, with a correction note
   naming the misfiling and the round that fixed it.
2. D2 → a second after-state selftest run committed alongside the first: one
   receipt, both runs, identical tallies
   (`.ufo/waves/round-64/evidence/selftests-rerun-and-guard-argv-r64.txt`).
3. D3 → the same receipt prints the full argv of every invocation, including
   the guard's `--expect 14`.
4. D4 → correction recorded here and in LOG/SCORECARD: the r63 report's
   "the lane's first Microsoft Learn rows" is imprecise — S241
   (learn.microsoft.com ja-jp Azure OOM page, opened 2026-10-24) predates
   r63; S572/S573 are the lane's first en-us Windows Server troubleshoot /
   Windows-commands rows. The wording is corrected where cited forward; the
   frozen report bytes are the orchestrator's.
5. D5 → noted, not fought: the two r63 tools landed mode 100644 because the
   treecommit helper pins that mode for new blobs — the working tree's
   executable bit cannot reach the index through it. Immaterial on this host
   (`python tools/…` invocation; shebangs inert at 100644), recorded as a
   POSIX-portability limitation of the lane's commit path.
6. D6 → census wording corrected in LOG and lesson (this file's predecessor
   paragraph): the fleet root's `<lane>-shokunin` entries are NTFS junctions
   to the lane repos, so the validator reads the lane's live working tree —
   no lagging clone exists. Host inspection: `dir /AL` junction listing,
   `fsutil reparsepoint` negative on the enclosing dirs. No measured value
   changes (67efdb79 precision-correction precedent).

## Gate

Two sources opened this round, both fetched with `curl -sS -m 60 -L` into
scratch, pinned byte-identical into `corpus/evidence/sources-r64/` (S574
sha256 `d52b00df…`, S575 sha256 `0d3c8d30…`); duplicate sweep before opening
(QUALITY 155): `grep -c "globalmemorystatusex" corpus/SOURCES.md` → 0 and
`grep -c "getdiskfreespaceexw" corpus/SOURCES.md` → 0 at the pre-open tip, no
reconciliation needed.

- S574 GlobalMemoryStatusEx function (sysinfoapi) —
  https://learn.microsoft.com/en-us/windows/win32/api/sysinfoapi/nf-sysinfoapi-globalmemorystatusex
  — opened 2026-10-31 — quote (`S574.html:829`): "Retrieves information about
  the system's current usage of both physical and virtual memory." (13 words).
- S575 GetDiskFreeSpaceExW function (fileapi) —
  https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getdiskfreespaceexw
  — opened 2026-10-31 — quote (`S575.html:854`): "If per-user quotas are
  being used, this value may be less than the total number of free bytes on a
  disk." (21 words).

Both rows land `mined`, used-by `corpus/knowledge/runway-win-r64.md`
(K1–K8 line-located; self-verified 9/9 probe hits at the cited lines). C2 is
the sourced claim.

reject sample: none met — no source rejections this round; the fresh-start
rule-outs above are the round's reject-class decisions.

Census (validator): start receipt
`.ufo/waves/round-64/evidence/census-start-r64.txt` (this host, 2026-10-31,
rc 0, tolerated W04 duplicate-URL class) → end receipt
`.ufo/waves/round-64/evidence/census-end-r64.txt` (rc 0). SOURCES row count
346 → 348 (S574+S575) is counted in the lane repo by
`grep -c "^| S" corpus/SOURCES.md`, a separate instrument from the validator
rc; the validator reads the lane's live working tree through the fleet root's
junction (D6 wording above — D6's corrected sentence applies to this round's
receipts as well).

## Mistakes

1. class: transport graded as semantics — the drift selftest's round-37
   `huge_cap` arm streamed 4 MiB fixture bodies over loopback HTTP; on this
   host that transport resets or stalls bodies from tens of KiB upward
   (non-deterministically; raw TCP streams the same bytes fine, and no proxy
   is configured), so the arm graded the host's security layer, not the cap,
   and the standing selftest was red here (`FAIL (5/6)` on entering v1
   bytes). captured-by: the instrument's own selftest run before any sweep
   receipt was scored (`evidence/drift-selftest-before-v1-win-r64.txt`).
   fix: v1.1 measures the transport (`_loopback_stream_cap`, two consecutive
   successes, bounded budget) and scales the pair to it, with the frozen
   `FETCH_MAX_BYTES = 4 * 1024 * 1024` literal folded into the arm's pass
   condition — the host limit is disclosed on the PASS line and the cap
   semantics stay asserted (the r37 cap-kill mutation still fails exactly
   this arm).
2. class: probe run under concurrent load — the v1.1 after-receipt's first
   run recorded `transport_cap=0` (every size failing) while the before
   receipt's 4 MiB loopback streaming was still running in another process;
   the probe passed standalone afterwards. captured-by: comparing the failed
   receipt against a standalone probe run, then re-taking the receipt as the
   sole heavy process. fix: the after receipt was re-taken clean and its
   header discloses the load condition; a selftest receipt is valid only for
   the load conditions it names.
3. class: large shell append silently truncated — the SCORECARD round section
   was appended with a long heredoc that warned "delimited by end-of-file"
   and cut the final sentence mid-thought; the write "succeeded" with a
   shorter file. captured-by: reading the landed tail and grepping the
   section's landmarks (header, both claim rows' verdicts, capability row)
   before commit. fix: the tail completed by a follow-up edit; every large
   append gets a post-write landmark check in this lane.
4. class: quote word-count asserted without counting (same family as the r62
   "(14 words)" miscount) — the S575 row's quote was first written "(20
   words)"; counting gives 21. captured-by: the round's pre-commit self-check
   against the r62 mistake class. fix: corrected to 21 before commit; counts
   are counted, not estimated.

## Wave

None — no dispatch surface on this host (carried disclosure; the mori
round-62 L0 line stands open, routed around, never treated as answered).
Round 64 ran L1-only over committed bytes; no wave-based evidence is claimed.

## Assimilation

considerthese mined (2026-10-19…2026-10-26, all eight files; no newer file
exists): the 2026-10-26 suggestion 1 (split env/stale mismatch classes) was
already implemented by r51's pin-check v5; suggestion 3 (re-execute what
closures only evidence-verify) was partially executed by r63's re-capture and
again this round (the r61 counter re-derived, the drift sweep re-run rather
than cited). No still-unimplemented proposal adopted this round.
Assimilation: none — shokuknow unreachable.
