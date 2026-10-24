# Recheck002 — C1 recheck of S002 (round 32, wave 1)

Seat: MoriR32A2.Recheck002. Lane repo: /home/vgpnk/Projects/shokunin/mori-shokunin.
No subagents, no background jobs, no tools installed. Only reads, curl, and seat-check.py were run.

## 1. Fetch receipt

| field | value |
|---|---|
| id | S002 |
| population url | https://docs.kernel.org/admin-guide/cgroup-v2.html |
| fetch command | `curl -sSL --fail -m 60 https://docs.kernel.org/admin-guide/cgroup-v2.html -o /fast/scratch/hyaku/mori-r32/Recheck002/S002.src` |
| http status / final URL | `200 https://docs.kernel.org/admin-guide/cgroup-v2.html` (written by `curl -w '%{http_code} %{url_effective}'`); `curl -L -w '%{num_redirects}'` printed `redirects=0` — no redirect, no move |
| accessed (UTC, at fetch) | 2026-10-23T01:31:23Z |
| byte size | 172967 bytes (`ls -l`) |
| sha256 | b478c1bae99899df476d6b4989cbb516f7ca93c5f009cdff64b802bbc24f3d4b |
| scratch copy | /fast/scratch/hyaku/mori-r32/Recheck002/S002.src (bytes saved unchanged; sha256 above recomputed by seat-check.py from this file) |
| normalised text | /fast/scratch/hyaku/mori-r32/Recheck002/S002.txt, 127571 bytes, produced by `python3 .ufo/waves/round-32/seat-check.py text /fast/scratch/hyaku/mori-r32/Recheck002/S002.src` |

Page identity observed in the copy: "The Linux Kernel 7.3.0" in the header, and the source date block "Date : October, 2015 Author : Tejun Heo < tj @ kernel . org >" (normalised offset ~1370). That matches the population anchor's "kernel documentation date 2015-10".

## 2. Ready-to-paste Recheck row

```markdown
| S002 | https://docs.kernel.org/admin-guide/cgroup-v2.html | 2026-10-23T01:31:23Z | b478c1bae99899df476d6b4989cbb516f7ca93c5f009cdff64b802bbc24f3d4b | "Note that all fields in this file are hierarchical"; "Similar to memory.events but the fields in the file are local to the cgroup i.e. not hierarchical"; "oom_kill The number of processes belonging to this cgroup killed by any kind of OOM killer" | current |
```

## 3. Quote-by-quote bearing on the teaches cell

teaches: "Distinguish hierarchical memory.events from memory.events.local; the documented oom_kill count includes processes killed by any kind of OOM killer."

- `"Note that all fields in this file are hierarchical"` — first clause (memory.events is hierarchical). Live normalised text, inside the `memory.events` definition: "Note that all fields in this file are hierarchical and the file modified event can be generated due to an event down the hierarchy." Exact substring of the saved copy (`in_copy=True`), 9 words, starts on "Note", ends on a whole word "hierarchical".
- `"Similar to memory.events but the fields in the file are local to the cgroup i.e. not hierarchical"` — first clause (the local counterpart). This is the entire opening sentence of the `memory.events.local` definition in the live page. 17 words, exact substring, no dropped prefix/negation ("not hierarchical" is quoted intact).
- `"oom_kill The number of processes belonging to this cgroup killed by any kind of OOM killer"` — second clause (any kind of OOM killer). Verbatim entry under `memory.events`, live page: "oom_kill The number of processes belonging to this cgroup killed by any kind of OOM killer." 16 words, exact substring. The phrase "any kind of OOM killer" is preserved, so the quote cannot be read as kernel-only killing.

All three are copied from the `seat-check.py text` output, not from rendered markup. None is page furniture (no nav/category/heading text), and none contains `&`, a pipe, a zero-width character, or a hyphenated line break. The `memory.peak` part of the scope cell is not quoted because the teaches cell does not assert anything about it; it was verified separately in §5.

Verdict `current` follows: every element of the teaches cell is present verbatim on the live page, and no wording changed in a way that matters.

## 4. seat-check output

Command:

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin && timeout 300 python3 .ufo/waves/round-32/seat-check.py row \
  S002 /fast/scratch/hyaku/mori-r32/Recheck002/S002.src \
  '"Note that all fields in this file are hierarchical"; "Similar to memory.events but the fields in the file are local to the cgroup i.e. not hierarchical"; "oom_kill The number of processes belonging to this cgroup killed by any kind of OOM killer"'
```

Output (exit=0):

```
sha256=b478c1bae99899df476d6b4989cbb516f7ca93c5f009cdff64b802bbc24f3d4b
quotes=3 words=[9, 17, 16] in_copy=[True, True, True]
shared_tokens=['cgroup', 'events', 'hierarchical', 'kill', 'killed', 'killer', 'kind', 'local', 'memory', 'processes'] topic_ok=True
live_quotes_ok=True
ROW_CHECK=pass (judge R4 and R5 not checked here)
```

## 5. Drift detail

No drift of any teaches fact. Observed on the live page:

- `memory.events` (raw HTML line 1377) still says the fields "are hierarchical" and points to the local file: "For the local events at the cgroup level see memory.events.local." (line 1384).
- `memory.events.local` (raw HTML line 1420) still says "Similar to memory.events but the fields in the file are local to the cgroup i.e. not hierarchical. The file modified event generated on this file reflects only the local events."
- `oom_kill` (raw HTML line 1410) still says "The number of processes belonging to this cgroup killed by any kind of OOM killer."
- `memory.peak` (raw HTML line 1356) still reads "A read-write single value file which exists on non-root cgroups. The max memory usage recorded for the cgroup and its descendants since either the creation of the cgroup or the most recent reset for that FD." That matches the anchor's `memory.peak` scope (max usage over cgroup and descendants, reset via a write).

Note for the L1 (not a drift verdict): the population anchor's numeric lines are stale against this copy — `memory.peak` is now raw line 1356 (anchor says 1418-1426) and the `memory.events` block spans 1377-1422 (anchor says 1448-1509). The section text itself is unchanged, so this is citation line-number hygiene for the knowledge files that quote `memory.events:1448–1458,1491–1494` (corpus/knowledge/oom-kill-counter-kernel-only-r12.md:12) and `memory.events.local:1505–1509`, not a change in what the page teaches. No Round32 correction is required under the C1 rule (drifted is defined by the teaches cell, which the live page still supports), and I did not draft one.

## 6. Residual unknowns

- Whether the raw line numbers in the anchor ever matched an earlier save could not be checked: no prior copy of this page exists under corpus/evidence (searched with `find corpus/evidence -iname '*cgroup*'`; only corpus/evidence/round-1-cgroup-dispatch.json matched, which is a dispatch receipt, not page bytes). [INFERENCE] They came from a differently paginated render.
- Nothing else open: the fetch succeeded on the first try and needed no retry transcript.
