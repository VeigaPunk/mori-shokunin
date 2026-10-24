# KnowledgeSeatTerminal — round 17 scoped findings (C1 knowledge entry draft)

Seat: `MoriR17.KnowledgeSeatTerminal-5` (scribe, leaf member, no subagent dispatch). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`, entering tip `24526ea9617cd020fee16c28fe4d4a2789dc28cb`. Scope: draft only. Nothing was written to `corpus/knowledge/`, `corpus/SOURCES.md`, or any tool path.

## Observed in this seat

| # | Action | Result |
|---|---|---|
| 1 | read `.ufo/waves/round-17/contract.md` (full) | C1 interface, classes, field list, exit codes, limits read at lines 9-67 |
| 2 | read `corpus/knowledge/journal-cursor-window-r16.md:1-15` | header shape: line 1 `source:`, line 2 `verified-at:`, line 3 `recheck:`, line 5 H1 title |
| 3 | read `.ufo/waves/round-17/wave1-context.txt` | binding rules read: no transcript content, no journal queries, no `/tmp`, no VCS writes, leaf member |
| 4 | grep `S041\|S043` across lane | hits only in `.ufo/waves/round-17/wave1-dispatch.json` and `wave1-spec.json` (task text). No corpus row. |
| 5 | grep `S04[0-9]` in `corpus/SOURCES.md` | S039 (line 45), S040 (line 46) only. **S041 and S043 are absent.** |
| 6 | glob `.ufo/waves/round-17/build/` | only `swarm-registry.json`. No sibling `SrcRfc6585` / `SrcZaiErrorCodes` report had landed at read time. |
| 7 | glob `corpus/knowledge/` | 25 notes plus `.gitkeep`; the r16 note's section layout read at lines 1-136 (`## Claim`, `## Evidence`, `## [INFERENCE]`, `## [UNKNOWN]`, `## Not claimed`, `## What it changes for mori`, `## Delivery paths this cannot see`, `## Source-registry state`) |

Commands run: only read, grep, glob. No URL was opened. No transcript, journal, or tool was run. No install or update was performed (none needed).

## Draft entry — `corpus/knowledge/seat-terminal-status-r17.md`

```
source: S041 (provisional; planned row, not yet in corpus/SOURCES.md) — https://www.rfc-editor.org/rfc/rfc6585 section 4, "429 Too Many Requests"; quote pending the SrcRfc6585 gate, not verified by this seat. S043 (provisional; planned row, not yet in corpus/SOURCES.md) — Z.AI API error-code documentation, https://docs.z.ai/api-reference/api-code, codes 1302 and HTTP 429; quote pending the SrcZaiErrorCodes gate, not verified by this seat. Lane interface (not an external source): .ufo/waves/round-17/contract.md, section C1.
verified-at: 2026-10-20 — read statically: .ufo/waves/round-17/contract.md; corpus/knowledge/journal-cursor-window-r16.md lines 1-15 (header shape); corpus/SOURCES.md (S041 and S043 absent at read time). No external URL was opened for this entry. No transcript was read and no tool was run.
recheck: `curl -fsSL https://www.rfc-editor.org/rfc/rfc6585.txt | grep -n '429 Too Many Requests'` and `curl -fsSL https://docs.z.ai/api-reference/api-code | grep -n '1302'` — both strings are placeholders [INFERENCE]; replace them with the verbatim gate quotes of S041 and S043 when those rows land.

# Seat terminal status from OMP transcripts — last observed class, seat counts, no content — round 17

## Claim

`tools/mori-seat-terminal.py` (C1) classifies each OMP seat transcript in a sessions directory by its last `message` record within a bounded file tail. Each seat gets one of seven classes: `completed`, `aborted`, `dead_rate_limit`, `dead_quota`, `dead_error_other`, `incomplete`, `unavailable`. The tool tallies the classes per seat-name prefix and per provider/model. It detects and reports only. It never edits, resumes, or re-routes a seat, and it emits no message text, content, or usage.

The entry supports one narrow statement: for the transcripts present in a given directory at scan time, the tool reports the last state each file shows, as seat counts. It does not establish why a seat ended, whether it will resume, or how many incidents it represents.

## Classification

Reading rules (contract C1):

- Walk the directory recursively for regular files named `*.jsonl`. Do not follow symlinks. Above `--max-files` (default 20000), stop with rc2 `MORI_SEAT_TERMINAL_SETUP reason=too-many-files`.
- Read at most the last `--max-tail-bytes` (default 262144) of each file. If the read did not start at byte 0, drop the first, possibly partial, line. Parse each line as JSON and skip lines that fail.
- Consider only records with `type == "message"` and a dict `message`. Every other record type is skipped unread.
- The terminal record is the last such message in the tail.

Classes, in test order:

| Class | Terminal record shape |
|---|---|
| `completed` | role `assistant`, `stopReason == "stop"` |
| `aborted` | role `assistant`, `stopReason == "aborted"` |
| `dead_rate_limit` | role `assistant`, `stopReason == "error"`, and `errorStatus == 429` or `errorMessage` contains `429`, `rate_limit`, `Rate limit`, `RATE_LIMITED`, or `resource_exhausted` |
| `dead_quota` | `stopReason == "error"`, not rate-limit, and `errorMessage` contains `quota`, `usage limit`, `402`, or `credits` |
| `dead_error_other` | any other `stopReason == "error"` |
| `incomplete` | terminal role `toolResult` or `user`, or assistant with another stopReason (e.g. `toolUse`) |
| `unavailable` | no parseable message record in the tail, or unreadable file |

Rate-limit is tested before quota, so a 429 that mentions quota counts as rate-limit.

Per-seat fields: `seat`, `prefix`, `class`, `provider`, `model`, `error_status` (int or null), `retry_exhausted` (errorMessage starts with `Retry budget exhausted`), `retries` (N from `after N retries`, else null), `error_code` (digits of a `(type=NNNN)` token, else null). `error_code` is an uninterpreted digit string. The tool does not map it to a vendor meaning.

Exit codes: 0 = scan complete and zero `dead_*`; 1 = scan complete and at least one `dead_*` (finding `MORI_SEAT_TERMINAL_DEAD`); 2 = setup or unavailable directory (finding `MORI_SEAT_TERMINAL_SETUP`).

Motivating observation (from the round context, not measured by this entry): Z.AI seats ended with `429 ... (type=1302)` and `Retry budget exhausted after 10 retries`.

## Evidence

- Class names, record fields, parse rules, and exit codes come from the lane interface `.ufo/waves/round-17/contract.md`, C1. They describe what the tool is specified to do. They are not measured behaviour of the delivered tool.
- The rate-limit status meaning (429 as "Too Many Requests") is the subject of S041 (RFC 6585 section 4, provisional). The entry relies on S041 only for that meaning.
- The Z.AI meaning of code 1302 and of HTTP 429 in that vendor's docs is the subject of S043 (provisional). If S043 is rejected or does not show 1302, the entry's claims about 1302 must be removed. The tool is unaffected: it keys on `errorStatus`, on error-message tokens, and on the digit string.

## [INFERENCE]

- A Z.AI `429 ... (type=1302)` seat will classify as `dead_rate_limit`, because `errorStatus` is 429 or the message contains `429`. Not tested against real transcripts.
- Substring tokens such as `429`, `credits`, or `402` can match unrelated text in `errorMessage`. A false `dead_*` class is possible. Not measured.

## [UNKNOWN]

- Whether OMP transcript records always carry `errorStatus` on a 429. Not observed.
- Whether a terminal record can fall outside the default 256 KiB tail on long transcripts. If it does, the seat reads as `unavailable` or as an earlier class. Not measured.
- Whether OMP's record shape is stable across versions. No version field is read or checked.

## Not claimed

- **Last observed state, not final.** A `dead_*` class is the last state the file shows. It is not proof that the session will never resume. A later write can change the class on the next scan.
- **Seats, not incidents.** Dead counts are seat files in the directory. One seat is one count. Several seats failing for one upstream event are several counts. The tool does not group them.
- **Prefixes are naming conventions.** The prefix is the text before the first `.` in the seat id. `--prefix` filters by that string. It does not authenticate who wrote the file or which lane it belongs to.
- **Unversioned transcript schema.** The classifier matches `type`, `message.role`, `message.stopReason`, `message.errorStatus`, and `errorMessage` tokens. OMP can change these shapes without notice, and there is no version check. A change shows up as misclassification or `unavailable`.
- **Exit 0 is not a health statement.** `unavailable` and `incomplete` seats do not set exit 1. Exit 0 means a complete scan with zero `dead_*`. Read `totals`.
- **No content.** `errorMessage` text, content, and usage are never emitted. The classes are derived from them and are not reported as text.
- **Symlinked seats are absent.** Seats reached only through a symlink are not scanned.
- **No live state.** This entry was drafted without reading any transcript, journal, or host state.

## What it changes for mori

- Gives L1 a read-only count of seats whose last state is rate-limit or quota death, per prefix and per provider/model, without reading content.
- Changes no routing, retry, or resume behaviour. C1 is detection only.

## Source-registry state

S041 and S043 are not in `corpus/SOURCES.md` at the time of this draft. Before this entry is committed, each must either land as a mined row with a verbatim gate quote, or be removed from the `source:` line and from the claims that depend on it.
```

## Findings for L1 (from the contract and the draft)

1. **S041 and S043 are unregistered.** `corpus/SOURCES.md` has S039 and S040 only (lines 45-46). S041 and S043 are planned sibling rows (SrcRfc6585, SrcZaiErrorCodes). Neither report had landed at read time. The entry cites them as provisional only.
2. **Contract sentence is garbled.** `contract.md` lines 60-61 read: "Then exactly one stderr-free summary line on stdout is NOT allowed — the JSON is the only stdout." The draft follows the reading that the JSON document is the only stdout output. L1 should fix the sentence before the tool is built.
3. **Exit-code gap.** A scan with only `unavailable` or `incomplete` seats and no `dead_*` returns exit 0. A caller reading only the exit code would read a healthy directory. The draft states this as a limit; L1 may want the contract to say it too.
4. **Substring false-positive risk** [INFERENCE]: tokens such as `429`, `credits`, `402`, and `quota` are matched as bare substrings of `errorMessage`. Word-boundary matching would reduce false `dead_*` classes. This is a design question for L1, not a claim.
5. **Tail window** [UNKNOWN]: the 256 KiB default tail may not reach the terminal record on very long transcripts. This is untested. The regression fixtures should include one long-tail case if the gate allows it.

## Out of scope

- No write to `corpus/knowledge/seat-terminal-status-r17.md`. The instruction was "Put the draft in your report only."
- No edit to `corpus/SOURCES.md`, `corpus/README.md`, the lane checkout, `MANIFEST.json`, `.ufo/state`, or any sibling lane.
- No transcript read. No journal query. No `/tmp` write.
