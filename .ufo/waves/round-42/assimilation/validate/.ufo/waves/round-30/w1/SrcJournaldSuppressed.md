# SrcJournaldSuppressed — C1 frontier source row (journald suppression notice)

Leaf source seat, mori round 30 wave 1. Scope: one SOURCES.md row for journald's rate-limit suppression
message, one Gate line, one excerpt file body under `corpus/evidence/sources-r30/`, and a verified reject for
every candidate opened and rejected. Nothing in the lane was written except this report; no tool source line,
tool output or fixture text is copied here.

## Behavior — what was opened, how

Every candidate was fetched with `curl -fsSL` from the scratch dir
`/fast/scratch/hyaku/mori-r30/MoriR30.SrcJournaldSuppressed/`; access times are `date -u +%FT%TZ`. The four
v262 files and both v257/v233 files were fetched twice and the two sha256 values agreed byte for byte
(`*.refetch` files in scratch). GitHub's tree API refused a directory listing (HTTP 403, rate limit), so
"which file carries the string at v262" rests on direct fetches and greps of the named paths, not on a full
listing — stated as a limit below.

| opened | result |
|---|---|
| `v262/src/journal/journald-manager.c` | HTTP 200, 101383 B, sha256 `428dc830…b5d6780a`-family — **admitted** |
| `v262/src/journal/journald-server.c` | HTTP 404, 14 B body "404: Not Found", sha256 `d5558cd4…033512ed` |
| `v262/src/journal/journald-rate-limit.c` | HTTP 200, 6167 B, `dfe42099…1b5d6780a` — `grep -c Suppressed` = 0 |
| `v262/src/journal/journald-native.c` | HTTP 200, 22950 B, `226a4c01…9bd3521` — `grep -c Suppressed` = 0 |
| `v262/man/journald.conf.xml` | HTTP 200, 32708 B, `ed71e38d…908f87f2` — `grep -ci suppress` = 0 |
| `v257/src/journal/journald-server.c` | HTTP 200, 118599 B, `0c1bb73b…aca21cd3` — `%i` at :1304 |
| `v252/src/journal/journald-server.c` | HTTP 200, 101129 B, `d9519978…57388aad` — `%i` at :1143 |
| `v249/src/journal/journald-server.c` | HTTP 200, 95661 B, `3478a46c…ec8466ac` — `%i` at :1107 |
| `v233/src/journal/journald-server.c` | HTTP 200, 77853 B, `1434afcf…4a066bde` — `%u` at :1181 |
| `v262/src/journal/journald-socket.c` | not fetched; already a URL inside S154 (`corpus/SOURCES.md:160`) |

Duplicate check before drafting: `grep -c journald-manager.c corpus/SOURCES.md` prints `0`, so this URL is not
yet carried by any row; the only `src/journal/` URL in the registry is `journald-socket.c` inside S154.

## Findings

1. **The stated literal is not the v262 form.** At v262 the notice is
   `LOG_MESSAGE("Suppressed %i messages from %s", rl - 1, c->unit)` (`src/journal/journald-manager.c:1294`):
   `%i`, with the dropped count `rl - 1` and the unit name as the argument. The `%u` spelling with a `path`
   argument is the v233 form (`v233/src/journal/journald-server.c:1181`). The entry and SKILL rows must quote
   `%i`; a "corrected" `%u` breaks both the source claim and the excerpt match (the word count is 9 either way).
2. **Guard and count.** The notice is written only when `if (rl > 1)` (`:1291`), i.e. at least two messages were
   dropped, and the number printed is `rl - 1` (`:1294`, and `N_DROPPED` at `:1295`) — so the printed count is
   the number dropped, one less than the rate limiter's return.
3. **Emitter is journald.** The call at `:1292` is journald's own `manager_driver_message`, inside
   `manager_dispatch_message`, tagged `SD_MESSAGE_JOURNAL_DROPPED_STR` (`:1293`). The unit name appears as a
   format argument, not as the writer, so the line is journald's report about the unit's stream.
4. **`journald-server.c` is gone at v262 (404).** The file exists at v257 (`:1302-1306`, same call shape but
   `server_driver_message`) and at v252/v249; v262 hosts the code in `journald-manager.c`. Any v262-anchored row
   must use the new path.
5. **Independent corroboration, not a source row.** `.ufo/waves/round-26/w1/CriticC2Width.md:238` already cites
   the same file and the same line 1294 in a report; that is a report citation, not a registry row. My row is
   the first registry entry for this URL.
6. **Attribution limit (do not over-read the excerpt).** The excerpt window is `:1291-1296`. The stronger
   attribution fields — `SYSLOG_IDENTIFIER=systemd-journald` at `:1217` and `_TRANSPORT=driver` at `:1219` — sit
   75 lines above it and are **outside** the excerpt. If the entry wants that attribution sentence, it needs a
   second row or a wider excerpt; I recommend not quoting it from this one.
7. **Fit with A2-01.** The rule family A2-01 in `tools/fixtures/mori-oom-killers/cases-a2.json` already keys on a
   notice in exactly this journald form, so this row grounds the rule's upstream shape without restating any
   case.
8. **Landing order.** `used-by` names `corpus/lessons/round-30.md` and
   `corpus/knowledge/earlyoom-invocation-scope-r30.md`; neither exists at this tip, so the SOURCES census
   "missing:" check (`CORPUS.md`, SOURCES census) prints both until they land. Land the row after them, or
   accept that census line red in between.
9. **Id.** `S15x` resolves to **S156**: `S155` is the highest existing id (`corpus/SOURCES.md:161`, verified by
   `grep -oE '^\| *S[0-9]{3,}' | sort -V | tail -3`). If another wave-1 source seat takes S156, keep the row,
   the Gate line and the excerpt filename consistent (all three carry the id; the excerpt is `S156.txt`).
10. **Retention.** A new file under `corpus/evidence/` is a new path; the round-18 allowlist
    (`corpus/evidence/retention-allowlist.json`) has no `sources-r30` row, so the L1 must confirm the scan
    metric does not rise (contract "No-harm check").

## Ready-to-paste — SOURCES.md row (id S156 = placeholder `S15x` resolved)

| S156 | systemd v262 journald per-unit rate-limit suppression notice — https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-manager.c | code | A | the suppression notice systemd-journald writes when its per-unit rate limit drops a unit's messages, at the v262 release tag only: the `rl > 1` guard, the emitter call, the `Suppressed %i messages from %s` wording with the count `rl - 1` and the unit name, and the SD_MESSAGE_JOURNAL_DROPPED_STR and N_DROPPED tags; not the rate-limit algorithm or its pools (src/journal/journald-rate-limit.c), not the pre-split src/journal/journald-server.c copy of the same code, not any host configuration, not the reader's own detection of such a line | src/journal/journald-manager.c:1290-1296 (notice inside `manager_dispatch_message`, emitted through `manager_driver_message` at :1292); tag v262 = annotated tag 1f7dffaf714cc4488159c498b7a17cf34c5a96d5 peeled to commit 8cc40e0c5e9234bf45084751ac53b1fbfe70b492; HTTP 200 on 2026-10-22; 101383 B sha256 428dc8308d5caf70faee074e87888264c3708aa8e24c6069854790b952a7ffa2 | systemd-journald itself writes the dropped-message notice naming the unit and the count of messages it dropped, so a `Suppressed N messages from <unit>` line is journald's report about the unit's stream, never a line the unit wrote. | mined | 2026-10-22 | on-release | corpus/lessons/round-30.md, corpus/knowledge/earlyoom-invocation-scope-r30.md |

## Ready-to-paste — Gate line (round-30 lesson `## Gate`)

| S156 | https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-manager.c | 2026-10-22T21:13:19Z | `428dc8308d5caf70faee074e87888264c3708aa8e24c6069854790b952a7ffa2` | `:1294` (9 words): "LOG_MESSAGE(\"Suppressed %i messages from %s\", rl - 1, c->unit)," | admit, A, mined |

## Ready-to-paste — excerpt file body `corpus/evidence/sources-r30/S156.txt`

Byte-exact draft at `/fast/scratch/hyaku/mori-r30/MoriR30.SrcJournaldSuppressed/S156.excerpt-draft.txt`
(field separator after each line number is a TAB; source whitespace kept verbatim; the range stops at `:1296`
because `:1297` is blank).

```
id: S156
url: https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-manager.c
sha256: 428dc8308d5caf70faee074e87888264c3708aa8e24c6069854790b952a7ffa2
accessed: 2026-10-22T21:13:19Z
lines: 1291-1296

1291	                if (rl > 1)
1292	                        manager_driver_message(m, c->pid,
1293	                                              LOG_MESSAGE_ID(SD_MESSAGE_JOURNAL_DROPPED_STR),
1294	                                              LOG_MESSAGE("Suppressed %i messages from %s", rl - 1, c->unit),
1295	                                              LOG_ITEM("N_DROPPED=%i", rl - 1));
1296	        }
```

## Ready-to-paste — reject Gate lines (one per candidate opened and rejected)

| S156 | https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-server.c | 2026-10-22T21:13:19Z | `d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed` | body line 1 (3 words): "404: Not Found" | reject, HTTP 404 at v262 — the path serves no file at the tag, and the notice is carried by src/journal/journald-manager.c:1290-1296 at the same tag |
| S156 | https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-rate-limit.c | 2026-10-22T21:13:19Z | `dfe42099dd8adb3d6c1ad663b8a5a9b8d6550147b6932f65f71fed11b5d6780a` | `:28` (2 words): "unsigned suppressed;" | reject, does not carry the fact — the file holds the per-priority pools and the dropped counter, and `grep -c Suppressed` on the fetched bytes prints 0 |
| S156 | https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-native.c | 2026-10-22T21:13:19Z | `226a4c01562a972261f0ed0c8238b27447d318e368341a7100476260d9bd3521` | `:288` (8 words): "manager_dispatch_message(m, iovec, n, MALLOC_ELEMENTSOF(iovec), context, tv, priority, object_pid);" | reject, does not carry the fact — the native entry point hands the parsed record to the manager, and `grep -c Suppressed` on the fetched bytes prints 0 |
| S156 | https://raw.githubusercontent.com/systemd/systemd/v262/man/journald.conf.xml | 2026-10-22T21:13:19Z | `ed71e38df308227a94aca77b0840742b2c6ec49c1e43c2376d4aa135908f87f2` | (0 matches) | reject, does not carry the fact — `grep -ci suppress` on the fetched bytes prints 0, so the page documents the limit without the notice wording |
| S156 | https://raw.githubusercontent.com/systemd/systemd/v257/src/journal/journald-server.c | 2026-10-22T21:13:19Z | `0c1bb73b71e9f8331378f55e4e2d35990a48fae2c95607e93bd9ddb6aca21cd3` | `:1304` (9 words): "LOG_MESSAGE(\"Suppressed %i messages from %s\", rl - 1, c->unit)," | reject, wrong version — the row is scoped to v262, and v262 carries the same line at journald-manager.c:1294, so this path adds no v262 evidence |
| S156 | https://raw.githubusercontent.com/systemd/systemd/v252/src/journal/journald-server.c ; https://raw.githubusercontent.com/systemd/systemd/v249/src/journal/journald-server.c | 2026-10-22 (fetch not timestamped; sha256 printed once) | `d9519978462b65c8cd0bb76a2230183aa25ed901b610027e1b8e670557388aad` (101129 B) ; `3478a46c01486eec3ee92dee131510df8436dc7099d9ec88fd53a346ec8466ac` (95661 B) | `:1143` / `:1107` (9 words): "LOG_MESSAGE(\"Suppressed %i messages from %s\", rl - 1, c->unit)," | reject, wrong version — both tags already spell %i and only locate the pre-split file, so neither can be the v262 anchor |
| S156 | https://raw.githubusercontent.com/systemd/systemd/v233/src/journal/journald-server.c | 2026-10-22 (fetch not timestamped; sha256 printed once) | `1434afcf28771525c7e77f0c1fe7fe84dd71933803b59e182e3f37454a066bde` (77853 B) | `:1181` (9 words): "LOG_MESSAGE(\"Suppressed %u messages from %s\", rl - 1, path)," | reject, wrong version and stale form — v233 substitutes a path and prints %u, while v262 prints %i with the unit name, so citing it would misstate the v262 message |
| S156 | https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-socket.c | 2026-10-22 (grep only; URL not fetched) | — | `corpus/SOURCES.md:160` shows this URL inside row S154 | reject, duplicate URL already carried by S154 |

Verification behind each reject (commands run in the scratch dir, output quoted):

- 404: `curl -sS -o journald-server-v262-body.txt -w 'http=%{http_code}' …/v262/src/journal/journald-server.c`
  printed `journald-server.c-v262 http=404`; the body is 14 B, `od -c` shows `4 0 4 : N o t F o u n d` and no
  newline; sha256 `d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed` (the same 404 body hash
  round 29 recorded for a different path, `corpus/lessons/round-29.md:59`).
- rate-limit: `grep -c Suppressed journald-rate-limit.c` → `0`; `journal_ratelimit_test` is declared at
  `journald-rate-limit.h:6` and defined at `journald-rate-limit.c:176`.
- native: `grep -c Suppressed journald-native.c` → `0`; the only `manager_dispatch_message` call is `:288`.
- man page: `grep -ci suppress journald.conf.xml` → `0` on the 32708 B fetched bytes.
- v257/v252/v249/v233: `grep -n Suppressed` found exactly one line in each, at the line numbers quoted; the
  v233 line is the only one spelled `%u`.
- duplicate: `grep -n 'journald-socket.c' corpus/SOURCES.md` prints only `160:` (row S154).

## Gates run here

- Row shape, on the pasted bytes in scratch:
  `awk -F'|' '{print "NF=" NF}' row.txt` → `NF=13`; the `NF!=13` malformed check prints nothing; the frozen
  enum check (tier/status/kind/community-inflation) prints nothing.
- Gate lines: each reject and the admit line give `NF=8` (six cells), the shape used at
  `corpus/lessons/round-29.md:55-65`.
- Quote-in-excerpt: whitespace-collapsed match of the 9-word gate quote against the drafted excerpt lines
  returns only line `1294`; `wc -w` of the exact inner text → `9`.
- Privacy scan of the excerpt draft: `grep -nEi 'uid|user@[0-9]|user-[0-9]+\.slice|@[a-z0-9.-]+\.[a-z]{2,}|host'`
  → no match (exit 1). The six source lines carry no user, host or mail token.
- Tag refs, independent of S153/S154: `git ls-remote https://github.com/systemd/systemd 'refs/tags/v262*'` →
  `1f7dffaf714cc4488159c498b7a17cf34c5a96d5 refs/tags/v262`, `8cc40e0c5e9234bf45084751ac53b1fbfe70b492
  refs/tags/v262^{}` — the peeled commit named in the row's anchor.
- **Not run** (and not claimed): `count-c1.sh` (absent at this tip — BuildCountC1 owns it), the C1 counter
  after landing, the SOURCES census against the lane (row not landed), the retention scan.

## Touched surfaces and out-of-scope

- Written: this report only. Scratch:
  `/fast/scratch/hyaku/mori-r30/MoriR30.SrcJournaldSuppressed/` (`journald-manager.c`, its `.refetch`, the
  other fetched candidates, `row.txt`, `gate.txt`, `rejects.txt`, `S156.excerpt-draft.txt`).
- Not done: no lane git or jj write, no unit start/stop/restart, no signal to any process, no read of
  `/etc/default/earlyoom` or any host unit file, no message to a writer, no copy of tool source or tool output,
  no subagent.
- Tooling: nothing installed or updated this seat.

## Artifact paths

- `.ufo/waves/round-30/w1/SrcJournaldSuppressed.md` (this report)
- `/fast/scratch/hyaku/mori-r30/MoriR30.SrcJournaldSuppressed/S156.excerpt-draft.txt` (excerpt bytes)
- `/fast/scratch/hyaku/mori-r30/MoriR30.SrcJournaldSuppressed/row.txt`, `gate.txt`, `rejects.txt` (paste-ready)
- `/fast/scratch/hyaku/mori-r30/MoriR30.SrcJournaldSuppressed/journald-manager.c` (+ `.refetch`) — admitted bytes
- `/fast/scratch/hyaku/mori-r30/MoriR30.SrcJournaldSuppressed/journald-server-v262-body.txt` — 404 body

Report: .ufo/waves/round-30/w1/SrcJournaldSuppressed.md
