# ReopenS156 — contract A1 residual (F3) for source S156

**Verdict: agree — no defect.** The re-fetched bytes reproduce the recorded sha256 exactly, all 73 excerpt
lines match the fetched line of the same number, all three located Gate quotes are verbatim with correct
`(N words)` labels, and the SOURCES `teaches` sentence is supported.

Scope: S156 only (`systemd v262 src/shared/bus-print-properties.c`). F3 wording attacked:
`.ufo/waves/round-30/contract.md:153-155` ("re-fetch every S156+ URL, recompute sha256 of the full bytes and
diff each excerpt line against the fetched line of the same number; any mismatch is reported as a C1 defect").

## 1. Independent re-fetch (access time, status, digest)

Command (from `/fast/scratch/hyaku/mori-r30-w2/ReopenS156`):

```sh
date -u +%Y-%m-%dT%H:%M:%SZ
curl -sS -o s156-fetch.c -w 'http_code=%{http_code} size=%{size_download} url=%{url_effective}\n' \
  https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/bus-print-properties.c
date -u +%Y-%m-%dT%H:%M:%SZ
sha256sum s156-fetch.c ; wc -l s156-fetch.c
```

Output, verbatim:

```
2026-10-22T22:02:39Z
http_code=200 size=17973 url=https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/bus-print-properties.c
2026-10-22T22:02:39Z
b56aa781be9c29b610156925030d3c4ab720c0ad73d57907d230ca3047302f2a  s156-fetch.c
484 s156-fetch.c
```

- Access time: **2026-10-22T22:02:39Z** (same second before and after the transfer).
- HTTP status: **200**; `url_effective` equals the requested URL, so no redirect was followed.
- Full-body sha256: **`b56aa781be9c29b610156925030d3c4ab720c0ad73d57907d230ca3047302f2a`**, 17,973 bytes,
  484 newline-terminated lines.
- Tag identity: `git ls-remote https://github.com/systemd/systemd 'refs/tags/v262*'` →
  `1f7dffaf714cc4488159c498b7a17cf34c5a96d5 refs/tags/v262` /
  `8cc40e0c5e9234bf45084751ac53b1fbfe70b492 refs/tags/v262^{}` — identical to the tag/peel recorded in
  `corpus/SOURCES.md:162` ("annotated tag 1f7dffaf… peeled to commit 8cc40e0c…"). The tag has not moved.

## 2. sha256 agreement across the three artifacts

| Artifact | Location | sha256 | equal to fetch |
|---|---|---|---|
| excerpt header | `corpus/evidence/sources-r30/S156.txt:3` | `b56aa781…302f2a` | yes |
| lesson Gate admit row | `corpus/lessons/round-30.md:114` (4th cell) | `b56aa781…302f2a` | yes |
| SOURCES anchor cell | `corpus/SOURCES.md:162` (6th cell) | `b56aa781…302f2a` | yes |

Also reproduced from `corpus/SOURCES.md:162` (anchor cell): size `17,973 B`, `484 lines`, `HTTP 200`.
Byte-for-byte equality was checked with `==` on the full 64-hex strings, not a prefix match.
URL and `accessed:` (2026-10-22T21:12:07Z) are identical strings in the excerpt header and the Gate row.

## 3. Excerpt line diff — every labeled line

Parsed `corpus/evidence/sources-r30/S156.txt` as `<id>|<url>|<sha256>|<accessed>|<lines>|` header plus
`<n><TAB><text>` rows, then compared each row to `s156-fetch.c` line `n` (1-based) as exact Python string
equality:

```
hdr sha match: True
excerpt rows: 73 first 16 last 426
strictly increasing: True
MISMATCHES: 0
```

Contiguous labeled ranges: **16–28, 106–134, 183–197, 411–426** (73 rows over a 411-line span; 338 lines of
the declared `lines: 16-426` selector are elided between blocks). Overlap with the claims at issue: the
predicate (`:19-24`), the UINT64 branch head (`:109-134`) and the fallback (`:183-197`) are all present and
byte-identical. No mismatch to list.

Caveat, not a defect under F3 (F3 diffs labeled lines, and each labeled line matches): the excerpt is partial.
A reader of `S156.txt` alone cannot see `:135-182`, which is where `RestrictNamespaces` (`:135`), `MountFlags`
(`:153`), the capability pair (`:162`), `CPUWeight` (`:171`) and the weight/[not-set] chain (`:174-182`) sit
(fetched bytes, `awk 'NR>=135 && NR<=182'`).

## 4. Gate quotes — verbatim and `(N words)` labels

Row `corpus/lessons/round-30.md:114`, quote cell, unescaped per A1 4c (`\|`→`|`, `\"`→`"`, `\\`→`\`) and
compared to the fetched line; `wc -w` on the unescaped literal:

| Located quote | Label | `wc -w` | label ok | verbatim |
|---|---|---|---|---|
| `bus-print-properties.c:19` | 5 | 5 | yes | equal to the stripped fetched line 19 |
| `bus-print-properties.c:23` | 4 | 4 | yes | substring of fetched line 23, equal after `strip()` |
| `bus-print-properties.c:194` | 5 | 5 | yes | substring of fetched line 194, equal after `strip()` |

Quotes as unescaped: `bool bus_property_is_timestamp(const char *name) {` ;
`return endswith(name, "Timestamp") ||` ; `bus_print_property_valuef(name, expected_value, flags, "%"PRIu64, u);`.
All three are ≥3 words, satisfying the A1 4c per-id minimum. No wording differs from the fetched bytes.

## 5. Is the SOURCES `teaches` sentence supported?

Table header `corpus/SOURCES.md:5`: `id | source | kind | tier | scope | anchor | teaches | status | opened |
recheck | used-by` — so `teaches` is the 7th field of row `corpus/SOURCES.md:162`:

> A uint64 property whose name ends in `Monotonic` is not recognised by the `Timestamp` suffix test, contains
> no `USec`, and reaches the printer's final integer branch, so a zero-valued `ActiveEnterTimestampMonotonic`
> is printed as the bare decimal `0` rather than a formatted date.

Clause by clause, against the fetched bytes (`s156-fetch.c`) and the excerpt:

| Clause | Evidence | Verdict |
|---|---|---|
| uint64 property | `:109 case SD_BUS_TYPE_UINT64: {` (excerpt row 109) | supported for a uint64-typed property |
| ends in `Monotonic` fails the suffix test | `:23 return endswith(name, "Timestamp") \|\|` + `:24 STR_IN_SET(… "NextElapseUSecRealtime", "LastTriggerUSec", "TimeUSec", "RTCTimeUSec")` (rows 23, 24); checked: `"ActiveEnterTimestampMonotonic".endswith("Timestamp")` = False and it is not in that four-name set | supported |
| contains no `USec` | `:129 else if (strstr(name, "USec"))` (row 129); checked: `"USec" in "ActiveEnterTimestampMonotonic"` = False | supported |
| reaches the final integer branch | chain `:116`, `:126`, `:129`, `:132`, `:135`, `:153`, `:162`, `:171`, `:174-182`, `:186-188`, `:191-192`, `:193 else`, `:194`; every earlier arm is `streq`/`STR_IN_SET`/`startswith`/`endswith` on names the property does not match, or additionally requires `u == USEC_INFINITY`/`CGROUP_*`/`UINT64_MAX` while `u == 0` | supported (rows 109-134, 183-197 in the excerpt; 135-182 verified from the fetched bytes) |
| prints bare decimal `0`, not a date | `:194 bus_print_property_valuef(… "%"PRIu64, u)` yields `0` for `u == 0`; the only date path is `:116-121 FORMAT_TIMESTAMP`, not entered | supported |

So: **supported**, by the excerpt's labeled lines and by the fetched bytes. Under the strictest reading —
"supported by the three located Gate quotes alone" (`:19`, `:23`, `:194`) — clause 3's `USec` exclusion
(`:129`) and the intervening branch order are outside the quoted set. A1 4c only requires one ≥3-word quote
per counted id, and the SOURCES anchor cell does cite `:109-121`, `:129`, `:193-194`, so this is a precision
note, not a C1 defect.

## 6. Bounds, tooling, unknowns

- Writes: this report plus scratch under `/fast/scratch/hyaku/mori-r30-w2/ReopenS156/` only. No subagents,
  no background jobs, no lane commits, no jj, no signals, no unit or `/etc` interaction, no host journal read.
  Git in the lane was read-only (`log`, `ls-remote` from scratch).
- Tooling: nothing installed or upgraded today; `curl`, `python3`, `git`, `sha256sum`, `wc` were already
  present. No pacman transaction was run.
- Remaining unknowns: (a) whether `ActiveEnterTimestampMonotonic` is declared uint64 and actually routed into
  this printer lives in the companion `systemctl-show.c` cited by path only at `corpus/SOURCES.md:162`; that
  file was not re-fetched for this item [INFERENCE, outside the assigned S156 question]; (b) the manager-side
  reason an unset stamp reads 0 is excluded by S156's own scope cell ("not why the manager reports 0"), so it
  is neither supported nor contradicted here.
- Confidence: high on §1–§4 (byte-level, two independent hashes, exact line equality); high on §5.
