measured 2026-10-23T07:55:54Z

# ReJudgeRow13r — re-judge of row 13r, `corpus/knowledge/disk-write-rate-r33.md` (§Round-34 revision) at 8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3

judged-sha256: ca489eb41140024e95641a53c7df0ae15f755a4e0a507b9f353bfec1b415f9f6
(sha256 of `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 8d56809…:corpus/knowledge/disk-write-rate-r33.md`; `sha256sum` on the extract.)

## Rule (quoted word for word from the round-33 contract)

> A row is supported only when the quotes located in the committed copies of the sources it cites state every fact its
> observation and reading cells assert, and its verdict cell follows from that reading without any further fact; a row
> any part of which is not so stated is unsupported, including a row the judge would accept only with a caveat or
> through a source the row does not cite.

(verbatim at `.ufo/waves/round-33/contract.md:46-49`, prefaced "Judge rule R-J (frozen…)" at :44.)

## Row 13r under judgment

File line 79 of the entry at the revision (`*79` in the table under `## Round-34 revision` at line 65):

- Observation: `Lane fact: `tools/mori-census.sh:1869-1871,1879-1894,1907-1908` labels its value an average since boot and computes field 10 (sectors written) × 512 / uptime seconds`
- Reading: `Sectors written is a cumulative counter (S181.src:33-34,64-65); counters other than field 9 reset at boot, on device reattachment or reinitialisation, or when the underlying counter overflows, and readers should detect and handle resets when comparing snapshots (S181.src:34-37)`
- Verdict: `Call the census value a since-boot average only if none of those resets happened after boot, and never report it as the current write rate`
- Sources cell: `S181; lane fact `tools/mori-census.sh``

Copies opened at 8d56809: `corpus/evidence/sources-r33/S181.src` (committed copy, 187 lines) and `tools/mori-census.sh` (committed lane file, 4744 lines).

## Observation facts — located quotes in `tools/mori-census.sh` at 8d56809

- O1 "labels its value an average since boot": `:1868-1870` — "# counters, so the only rate derivable without a sampling interval is the / # AVERAGE SINCE BOOT — reported with that name and never as an instantaneous / # rate." (contiguous; states the reported name). Reinforcing but uncited: emitted key `io_avg_since_boot` at `:1974`, header comment `:71-72`.
- O2 "computes field 10 (sectors written) × 512 / uptime seconds":
  - `:1887-1889` — "# field 10 of a diskstats line = sectors written (field 8 is writes completed); / # 512 bytes per sector is the counter's unit, not an assumption about the / # device's physical sector size." (contiguous)
  - `:1892` — `sectors=$(printf '%s\n' "$line" | awk '{print $10}' || true)` (extracts field 10)
  - `:1894` — `printf '%sBps' "$((sectors * 512 / up_s))"` (× 512 ÷ up_s)
  - `:1907-1908` — `up_raw=$(read_file "$UPTIME_FILE"); up_raw=${up_raw%% *}; up_raw=${up_raw%%.*}` / `if is_int "$up_raw" && [ "$up_raw" -gt 0 ]; then up_s=$up_raw; fi` (up_s = uptime value)
  - "seconds" is additionally stated by `/${up_s}s` at `:1958` and implied by `Bps` at `:1894`; the `UPTIME_FILE=/proc/uptime` default at `:312` sits outside the cited spans — informative only, not load-bearing.
- No observation fact `missing`.

## Reading facts — located quotes in committed `S181.src` (iostats.rst)

- R1 "Sectors written is a cumulative counter": `:33-34` — "All fields are cumulative, monotonic counters, except for field 9, which / resets to zero as I/Os complete." plus `:64-65` — "Field  7 -- # of sectors written (unsigned long) / This is the total number of sectors written successfully." (contiguous; identifies sectors written and its cumulative monotonicity; "Field 7" is iostats numbering per the entry's own note that S181 numbers from 1 after the name).
- R2 reset list + reader duty: `:34-37` — "The remaining fields reset at boot, on / device reattachment or reinitialization, or when the underlying counter / overflows. Applications reading these counters should detect and handle / resets when comparing stat snapshots." (contiguous, 4 lines; states every element: boot / reattachment / reinitialization / overflow / detect-and-handle. `reinitialization` vs the row's `reinitialisation` is a spelling variant — same fact.)
- No reading fact `missing`.

## Verdict cell — follows with no further fact

- Clause 1 "call … a since-boot average only if none of those resets happened after boot": reading states the counter is cumulative and resets at boot/reattachment/reinitialization/overflow; therefore it covers the whole time since boot only when no listed reset happened after boot — a direct consequence, no extra fact.
- Clause 2 "never report it as the current write rate": the cited lane copy states the value is "AVERAGE SINCE BOOT — reported with that name and never as an instantaneous rate" (`:1869-1870`), and the reading shows it is one cumulative counter over the whole uptime window, not a two-reading delta; an average over the window is not the current rate. No further fact needed. Consistent with `spotcheck.md:101`, which classifies the row-13 verdict as a "write-rate decision".

## SKILL.md:816-818 at 8d56809 — still hold under 13r

- `:816` (cites rows 2, 4, 13): "…the since-boot average is never the current rate" — identical to 13r's clause 2; 13r only adds the no-reset-after-boot guard, a strengthening, not a contradiction. Holds.
- `:817` (cites row 3 + Host observation): partition-vs-disk totalling rule reinstated verbatim in 3r's verdict; the dm-N clause rests on the unchanged Host observation. Holds.
- `:818` (cites rows 5, 6, 7): unchanged field-5 row plus 6r/7r verdicts carrying the same semantics (approximate busy share, never percent). Holds.
- Matches `spotcheck.md:229-230`: "Entry rows 3, 6, 7, 13 are unsupported… `SKILL.md:816-818` rest on these rows."

## Audit of .ufo/waves/round-34/wa/JudgeRow13r.md

1. `:5` judged-sha256 `ca489eb4…f9f6` — agree (recomputed identical).
2. `:6` "8d56809 is an ancestor of HEAD" — agree (`merge-base --is-ancestor` exit 0); quoted fd25213 subject "…before dispatch" agrees (`git log -1 fd25213`); HEAD has since moved to `ff33407…`, consistent with its earlier measurement.
3. `:8,:10-13` rule quoted verbatim from `contract.md:47-50` — agree (byte-identical to `:46-49` quote block; location line numbers agree).
4. `:15` "row at file line 79", "section at line 65" — agree (grep `*79`; line 65 is the `## Round-34 revision` header).
5. `:17-20` row cells and sources cell quoted verbatim — agree (byte-match against file line 79).
6. `:27-33` observation quotes at census `:1869`, `:1870-1871`, `:1887-1889`, `:1892`, `:1894`, `:1907-1908` — agree (all located verbatim at those lines at 8d56809).
7. `:35` "no observation fact missing" — agree.
8. `:40-43` reading quotes at S181 `:33-34`, `:64-65`, `:34-37` — agree (verbatim).
9. `:43` "reinitialization vs reinitialisation is a spelling variant; Applications reading… vs readers is a synonym — same facts stated" — agree.
10. `:45` "no reading fact missing" — agree.
11. `:49` verdict-follows reasoning, incl. clause 2 resting on the cited average-vs-instantaneous observation — agree.
12. `:53` routed-defect claim: spotcheck §3.1 quote "the observation is a fact about tools/mori-census.sh; S181 has no census, uptime or average text" and §8 item 2 quote — agree (verbatim at `spotcheck.md:97` and `:229`; paraphrase accurate).
13. `:59` process notes (counter not re-run; row read as single line) — agree; consistent, not load-bearing.
14. `:61` VERDICT supported — agree.

AUDIT: agree 14 / disagree 0

## Tooling and containment

- Installed/updated nothing (pacman transactions paused host-wide; git used read-only, commands `timeout`-bounded).
- Scratch copies only under `/fast/scratch/hyaku/mori-r34/a3-ReJudgeRow13r/` (dwr33.md, S181.src, mori-census.sh, SKILL.md, spotcheck.md — all `git show` extracts at 8d56809).
- Report path per trailer; no lane writes, no git/jj mutation, no subagents or background jobs.

VERDICT: row 13r: supported
