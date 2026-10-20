# TranscriptTailBounds — round 17 scoped findings (C1 default tail vs real transcripts)

Seat: `MoriR17.TranscriptTailBounds-5` (scout, leaf member, no subagent dispatch). Lane:
`/home/vgpnk/Projects/shokunin/mori-shokunin`, entering tip `24526ea9`. Scope: measurement and
falsification of the C1 `--max-tail-bytes` default (262144) against the real OMP transcript
corpus. Nothing was edited; no VCS operation; no `/tmp` write; no journal query; no install.

Question: for every `*.jsonl` under `~/.omp/agent/sessions/-Projects-shokunin/`, what is the
byte distance from EOF to the start of the last `message` record, and how many files exceed
262144 (so their terminal record cannot be parsed under the default tail)?

## Observed in this seat

| # | Action | Result |
|---|---|---|
| 1 | read `.ufo/waves/round-17/contract.md` | C1 read rule at `contract.md:35-36`: last `--max-tail-bytes` (default 262144), else drop first (possibly partial) line; terminal record = last `message` record in the tail (`contract.md:48`); `unavailable` at line 50 |
| 2 | `find` over the corpus | 5085 regular `*.jsonl`, **0 symlinks** named `*.jsonl`, 15 top-level session dirs, 4.09 GB total (`sum` of `stat` sizes) |
| 3 | stable tail scan, all files (chunked bottom-up walk, 64 KiB doubling, size-stability retry) | 5084 files with a parseable `type=message` record; 1 file with none (785 B, final record `thinking_level_change`) |
| 4 | independent whole-file scan of 11 over-threshold files + 600 random files with mtime > 30 min | 611/611 offsets identical to the chunked scan; 0 mismatches |
| 5 | first cross-check that mixed live files | 10 apparent mismatches; all were files that **grew** between the two reads (append-only), verified by differing sizes; no algorithm disagreement |

Commands (all read-only; run from `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin`):

- `find . -type f -name '*.jsonl' | wc -l` → `5085`, rc 0; `find . -type l -name '*.jsonl' | wc -l` → `0`, rc 0.
- `python3 - <<'PY' … PY` stable tail scan of all 5085 files (chunked, `os.walk(followlinks=False)`), rc 0 — 11 over-threshold, 1 no-message.
- `python3 - <<'PY' … PY` whole-file cross-check (11 over + 600 inactive random), rc 0 — 0 mismatches.
- `grep -n … contract.md`, `ls .ufo/waves/round-17/build/` — read-only, rc 0.

Python 3.14.8; stdlib only. No tool install or update was needed or performed.

## Distribution (n = 5084 files with a last message record)

Distance = `file_size − byte_offset(first byte of the last message record's line)`. Measured
2026-10-20, one stable snapshot per file (size re-checked before and after each read; 0 files
changed during their own read).

| distance from EOF (bytes) | files |
|---:|---:|
| 256 – 511 | 15 |
| 512 – 1 023 | 388 |
| 1 024 – 2 047 | 214 |
| 2 048 – 4 095 | 1 219 |
| 4 096 – 8 191 | 1 855 |
| 8 192 – 16 383 | 1 062 |
| 16 384 – 32 767 | 179 |
| 32 768 – 65 535 | 71 |
| 65 536 – 131 071 | 44 |
| 131 072 – 262 143 | 26 |
| **262 144 – 524 287** | **11** |
| ≥ 524 288 | 0 |

- min 409; p50 5 495; p75 8 554; p90 12 727; p95 20 026; p99 99 495; p99.9 309 838; **max 464 592**.
- **count(distance > 262 144) = 11** (0.216 % of the 5084 measured; 11/5085 of all files).
- count(distance == 262 144) = **0**; largest distance still inside the default window = 255 096,
  i.e. a clean 7 048-byte margin below the boundary. The default does not sit on a cliff.
- 4609 of 5084 files are larger than 262 144 and therefore read as a partial tail; 1 file has no
  message record at all and is correctly `unavailable` by design (`contract.md:50`).

The last record of 4857 files is a `custom` `session_exit` marker (239 B in each of the 11
over-threshold files), so the terminal message normally sits one short record before EOF;
median distance is dominated by the size of the final assistant message, not by trailing
records.

## The 11 files over the default (all missed under 262144)

Each row: distance to last message start / file size / final message line bytes / true terminal class.

| # | seat (path under the sessions dir) | dist | file size | last msg line | class |
|---:|---|---:|---:|---:|---|
| 1 | `2026-10-19T20-36-43-523Z_01a155e1…/W2RoundKagi/W2RoundKagi.Critic-3.jsonl` | 464 592 | 1 651 323 | 464 352 | completed |
| 2 | `…/W2RoundMado-8/W2RoundMado-8.R12Critic-3.jsonl` | 362 718 | 1 832 798 | 362 478 | completed |
| 3 | `…/W2RoundGameDev3d/W2RoundGameDev3d.R108PreCritic-5.jsonl` | 356 538 | 1 223 887 | 356 298 | completed |
| 4 | `…/W2RoundTabi/W2RoundTabi.TabiCritic2.jsonl` | 342 913 | 1 329 785 | 342 673 | completed |
| 5 | `…/W2RoundSouji-8/W2RoundSouji-8.R12Critic.jsonl` | 314 272 | 1 726 619 | 314 032 | completed |
| 6 | `…/KaikokuSourcesR13/KaikokuSourcesR13.SourceCritic.jsonl` | 309 838 | 929 299 | 309 598 | completed |
| 7 | `…/W2RoundTameshi/W2RoundTameshi.Critic-3.jsonl` | 302 461 | 2 690 950 | 302 221 | completed |
| 8 | `…/W2RoundChousa/W2RoundChousa.R24Planner-2.jsonl` | 287 570 | 2 123 339 | 287 330 | completed |
| 9 | `…/W2RoundKama/W2RoundKama.KamaCritic.jsonl` | 287 138 | 2 927 188 | 286 898 | completed |
| 10 | `…/W2RoundGameDev3d/W2RoundGameDev3d.R108Planner-5.jsonl` | 270 810 | 2 140 685 | 270 570 | completed |
| 11 | `…/W2RoundGameDev2d/W2RoundGameDev2d.R105Critic.jsonl` | 267 833 | 1 170 115 | 267 593 | completed |

All 11 share one shape: the final assistant message is a single 261–454 KiB line (all
`role=assistant`, `stopReason=stop`), followed by the 239-byte `custom`/`session_exit` record.
All are historical seats in the `2026-10-19T20-36-43-523Z_01a155e1…` session; none is a live
today-seat. Prefix tally of the misses: `W2RoundGameDev3d` 2; `W2RoundKagi`,
`W2RoundMado-8`, `W2RoundTabi`, `W2RoundSouji-8`, `KaikokuSourcesR13`, `W2RoundTameshi`,
`W2RoundChousa`, `W2RoundKama`, `W2RoundGameDev2d` 1 each.

## Consequence under the C1 default (observed, not inferred)

For a file larger than the tail, the tool drops the first line of the window unconditionally
(`contract.md:35-36`). A record is therefore parsed only when its line starts strictly after
`size − 262144`, i.e. distance < 262144. When the last message starts at or before the window
start, no complete message record can exist in the tail: every earlier message starts even
earlier, and the window can only hold the dropped partial final line plus trailing non-message
records. The tool then has no terminal message record and must emit `unavailable` — it cannot
promote an older message to "terminal", so a **stale misclassification is impossible** for
this failure mode.

Emulated on the 11 files: all 11 → `unavailable`; none → `dead_*`, none → `completed`.

- False dead findings: **0**. The motivating detection (zai 429 seat deaths) is not degraded by
  the default: 0 of the 11 misses is any `dead_*`.
- Coverage loss: 11 of 5083 seats with a message record lose their true `completed` class,
  i.e. **99.784 %** of terminal records remain classifiable; 5072 completed/other classes stay
  correct. `unavailable` is an honest degradation required by the contract's own class list.
- The misses are systematic, not random: they are exactly critic/planner seats with very long
  final reports. [INFERENCE] Future long-final-message seats (critics, planners, source scribes)
  are the population at risk, so the default's blind spot is biased toward high-output seats.

## Tail-size trade-off (same 5084-file snapshot)

| `--max-tail-bytes` | files missed | bytes read | vs. corpus |
|---:|---:|---:|---:|
| 65 536 | 81 | — | — |
| 131 072 | 37 | — | — |
| **262 144 (contract default)** | **11** | 1.29 GB | 32 % of 4.09 GB |
| 327 680 | 4 | 1.59 GB | 39 % |
| 393 216 | 1 | 1.87 GB | 46 % |
| 458 752 | 1 | 2.12 GB | 52 % |
| 524 288 | 0 | 2.35 GB | 58 % |

Exact byte counts at 262144/327680/393216/458752/524288: 1 292 763 589 / 1 588 918 722 /
1 866 292 771 / 2 122 808 255 / 2 354 995 930. Full corpus 4 092 815 654 B.

## Live-corpus caveats for C1

- Transcripts are live and append-only in every observation here: 119 files grew between two
  scans ~1 minute apart (all mtime < 30 min); 295 files have mtime < 30 min and 4245 were
  modified on 2026-10-20. No shrink was observed. A terminal class is therefore only the state
  at scan time, as the contract's required `--help` limit already states.
- 1 of 5085 files has no `message` record at all (785 B, records end at `thinking_level_change`):
  C1 must floor it at `unavailable`, not error.
- `--max-files` default 20000 vs 5085 files: no pressure; recursion depth and file count are
  safe at today's corpus size. 0 symlinks, so the no-follow rule loses nothing here.

## Remaining unknowns

- Whether OMP's own compaction ever rewrites a transcript shorter: not observed in this window
  (only growth), so [INFERENCE] unverified.
- Whether the 11 huge final messages are one record or several concatenated: measured as a single
  JSON line each (line length = distance − 239), so single records; content not inspected.
- Behavior on unreadable files (permission/I-O errors) was not exercised; C1 maps them to
  `unavailable` by contract.

## Verdict for the L1

The 262144 default **validates** for C1's stated purpose: dead-rate-limit detection loses no
seat on this corpus (0/11 misses are `dead_*`), no stale or false-dead class is possible under
the read rule, and 99.78 % of terminal records are classifiable. The default's blind spot is
exactly long-final-message seats (11 historical critic/planner seats; EOF-to-last-message
distances 267 833–464 592, i.e. 262–454 KiB final message lines), which degrade honestly to
`unavailable`. If full terminal coverage is wanted, the smallest
tested value with zero misses is 524288 (+82 % read bytes, 2.35 GB vs 1.29 GB); 393216 leaves
one miss. This is evidence only; the choice stays with the integration owner.
