# SrcShowZeroStamp — frontier source row: a never-set `ActiveEnterTimestampMonotonic` prints as `0`

Seat: leaf source scribe, mori round 30, wave 1. Scope: one `corpus/SOURCES.md` row (C1's sourced claim), its Gate
lines, its excerpt body, and a verified reject for the man-page candidate. Writes: this report only, plus scratch under
`/fast/scratch/hyaku/mori-r30/SrcShowZeroStamp/`. No lane file, index, jj state or fleet file was written.

## Fact as verified

`systemctl show` iterates the `GetAll` reply with `bus_message_print_all_properties(reply, print_property, …)`
(`src/systemctl/systemctl-show.c:2405`, fetched 2026-10-22T21:12:38Z). Its own uint64 case tests
`bus_property_is_timestamp(name)` and otherwise `break`s (`systemctl-show.c:1222-1234`), i.e. returns 0; the shared
dispatcher then runs the shared printer whenever the callback returned 0 (`src/shared/bus-print-properties.c:421-422`).
That printer formats a uint64 as a date only when the name ends in `Timestamp` or is one of four `USec` exception names
(`:19-25`), as a timespan when the name contains `USec` (`:129`), and otherwise prints the bare decimal `"%PRIu64`
(`:193-194`). `ActiveEnterTimestampMonotonic` ends in `Monotonic`, contains no `USec` substring and matches none of the
domain-specific names, so it reaches the final integer branch: a zero value renders as
`ActiveEnterTimestampMonotonic=0` — bare decimal, never a date.

Boundary: this row explains the *rendering*. Why the manager reports 0 for a never-set stamp is not established here
(see [INFERENCE] below); the row's scope cell says so.

## Ready-to-paste Registry row (append after S155, `corpus/SOURCES.md`)

```md
| S156 | systemd v262 shared property printer `src/shared/bus-print-properties.c`, with the `systemctl show` call site `src/systemctl/systemctl-show.c` at the same tag — https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/bus-print-properties.c ; https://raw.githubusercontent.com/systemd/systemd/v262/src/systemctl/systemctl-show.c | code | A | the name-based rendering of D-Bus property values at the v262 release tag: the `bus_property_is_timestamp()` suffix test (`Timestamp` ending plus four `USec` exception names), the UINT64 branch order (timestamp, `ManagedOOMMemoryPressureDurationUSec`, `USec` timespan, `CoredumpFilter`, `RestrictNamespaces`, `MountFlags`, capabilities, cgroup and limit names) and the final `%PRIu64` fallback, the callback-returns-0 hand-off to that printer, and the `systemctl show` callback that declines every non-timestamp uint64; not why the manager reports 0 for a never-set stamp, not `format_timestamp()` output for zero, not the D-Bus interface definition of the properties, not `busctl`, not this host | bus-print-properties.c:19-25 (`bus_property_is_timestamp`, `endswith(name, "Timestamp")` plus the four `USec` exceptions), :109-121 (UINT64 timestamp branch, `FORMAT_TIMESTAMP`), :129 (`strstr(name, "USec")`), :193-194 (final `"%"PRIu64` fallback), :419-422 (callback result 0 selects `bus_print_property`); systemctl-show.c:1222-1234 (its own UINT64 case tests the same predicate and breaks otherwise), :2405 (`bus_message_print_all_properties(reply, print_property, …)`); tag v262 = annotated tag 1f7dffaf714cc4488159c498b7a17cf34c5a96d5 peeled to commit 8cc40e0c5e9234bf45084751ac53b1fbfe70b492 (`git ls-remote`, 2026-10-22); bus-print-properties.c 17,973 B sha256 b56aa781be9c29b610156925030d3c4ab720c0ad73d57907d230ca3047302f2a, 484 lines, HTTP 200 at 2026-10-22T21:12:07Z; systemctl-show.c 121,458 B sha256 88291f8249d6a86a8bf1f8fc7dc0527e76cfa2d0d6fc07ec54bf09911eaf299a, 2 634 lines, HTTP 200 at 2026-10-22T21:12:38Z | A uint64 property whose name ends in `Monotonic` is not recognised by the `Timestamp` suffix test, contains no `USec`, and reaches the printer's final integer branch, so a zero-valued `ActiveEnterTimestampMonotonic` is printed as the bare decimal `0` rather than a formatted date. | mined | 2026-10-22 | on-release | corpus/lessons/round-30.md, corpus/knowledge/earlyoom-invocation-scope-r30.md |
```

Column check: 11 cells in the Registry shape (`SOURCES.md:7`); no `|` inside any cell — the predicate is paraphrased
rather than pasted, because the literal line 23 carries a `||` token that would split a Markdown cell.

## Gate lines for `corpus/lessons/round-30.md` `## Gate`

```md
| S156 | https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/bus-print-properties.c | 2026-10-22T21:12:07Z | `b56aa781be9c29b610156925030d3c4ab720c0ad73d57907d230ca3047302f2a` | `:19` (5 words): "bool bus_property_is_timestamp(const char *name) {" | admit, A, mined |
| S156 | https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/bus-print-properties.c | 2026-10-22T21:12:07Z | `b56aa781be9c29b610156925030d3c4ab720c0ad73d57907d230ca3047302f2a` | `:121` (4 words): "bus_print_property_value(name, expected_value, flags, FORMAT_TIMESTAMP(u));" | admit, A, mined |
| S156 | https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/bus-print-properties.c | 2026-10-22T21:12:07Z | `b56aa781be9c29b610156925030d3c4ab720c0ad73d57907d230ca3047302f2a` | `:130` (5 words): "bus_print_property_value(name, expected_value, flags, FORMAT_TIMESPAN(u, 0));" | admit, A, mined |
| S156 | https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/bus-print-properties.c | 2026-10-22T21:12:07Z | `b56aa781be9c29b610156925030d3c4ab720c0ad73d57907d230ca3047302f2a` | `:422` (8 words): "r = bus_print_property(name, expected_value, value_type, value_contents, m, flags);" | admit, A, mined |
| S156 | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemctl.xml | 2026-10-22T21:12:07Z | `caca7b87ae3bc8730b070a38d814c698acf82c596df9cb47a58fc7510c7b765c` | `:328` (6 words): "By default, empty properties are suppressed." | reject, does not carry the fact: the `show` entry documents property selection and empty suppression only; the fetched 3 118-line page has 0 occurrences of `Monotonic`, `TimestampMonotonic` and `ActiveEnter` (grep -c, each 0), and no sentence on how an unset uint64 timestamp renders — that is a code fact carried by this row's printer URL |
```

Word counts were taken with `wc -w` on the exact quoted strings (5, 4, 5, 8, 6). Every quoted line lies inside the
excerpt body below (bands 16-28, 106-134, 183-197, 411-426). No Gate quote contains a `|` token or an embedded double
quote, so each Gate row keeps six cells; the final integer fallback (`:193-194`, which does contain `"%"PRIu64`) is not
Gate-quoted but is carried verbatim in the excerpt band 183-197 and named in the row anchor.

## Excerpt file body — write as `corpus/evidence/sources-r30/S156.txt`

Header followed by the exact lines, `<line number><TAB><text verbatim>`; bands are 16-28, 106-134, 183-197, 411-426
(four quoted regions with three context lines each side). Header `lines: 16-426` labels the span.

```text
id: S156
url: https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/bus-print-properties.c
sha256: b56aa781be9c29b610156925030d3c4ab720c0ad73d57907d230ca3047302f2a
accessed: 2026-10-22T21:12:07Z
lines: 16-426

16	#include "strv.h"
17	#include "time-util.h"
18	
19	bool bus_property_is_timestamp(const char *name) {
20	        assert(name);
21	
22	        /* Trust me, this naming convention is ironclad. Except for these three. Okay four. Well... */
23	        return endswith(name, "Timestamp") ||
24	                        STR_IN_SET(name, "NextElapseUSecRealtime", "LastTriggerUSec", "TimeUSec", "RTCTimeUSec");
25	}
26	
27	int bus_print_property_value(const char *name, const char *expected_value, BusPrintPropertyFlags flags, const char *value) {
28	        assert(name);
106	                return 1;
107	        }
108	
109	        case SD_BUS_TYPE_UINT64: {
110	                uint64_t u;
111	
112	                r = sd_bus_message_read_basic(m, type, &u);
113	                if (r < 0)
114	                        return r;
115	
116	                if (bus_property_is_timestamp(name))
117	                        /* RTCTimeUSec should always be displayed in UTC, consistent with timedatectl status */
118	                        if (streq(name, "RTCTimeUSec"))
119	                                bus_print_property_value(name, expected_value, flags, FORMAT_TIMESTAMP_STYLE(u, TIMESTAMP_UTC));
120	                        else
121	                                bus_print_property_value(name, expected_value, flags, FORMAT_TIMESTAMP(u));
122	
123	                /* Managed OOM pressure default implies "unset" and use the default set in oomd.conf. Without
124	                 * this condition, we will print "infinity" which implies there is no limit on memory
125	                 * pressure duration and is incorrect. */
126	                else if (streq(name, "ManagedOOMMemoryPressureDurationUSec") && u == USEC_INFINITY)
127	                        bus_print_property_value(name, expected_value, flags, "[not set]");
128	
129	                else if (strstr(name, "USec"))
130	                        bus_print_property_value(name, expected_value, flags, FORMAT_TIMESPAN(u, 0));
131	
132	                else if (streq(name, "CoredumpFilter"))
133	                        bus_print_property_valuef(name, expected_value, flags, "0x%"PRIx64, u);
134	
183	                                             "MemoryHigh", "MemoryMax",
184	                                             "MemorySwapMax", "MemoryZSwapMax", "MemoryLimit") &&
185	                          u == CGROUP_LIMIT_MAX) ||
186	                         (endswith(name, "TasksMax") && u == UINT64_MAX) ||
187	                         (startswith(name, "Limit") && u == UINT64_MAX) ||
188	                         (startswith(name, "DefaultLimit") && u == UINT64_MAX))
189	
190	                        bus_print_property_value(name, expected_value, flags, "infinity");
191	                else if (STR_IN_SET(name, "IPIngressBytes", "IPIngressPackets", "IPEgressBytes", "IPEgressPackets") && u == UINT64_MAX)
192	                        bus_print_property_value(name, expected_value, flags, "[no data]");
193	                else
194	                        bus_print_property_valuef(name, expected_value, flags, "%"PRIu64, u);
195	
196	                return 1;
197	        }
411	                                return r;
412	
413	                        char value_type;
414	                        const char *value_contents;
415	                        r = sd_bus_message_peek_type(m, &value_type, &value_contents);
416	                        if (r < 0)
417	                                return r;
418	
419	                        if (func)
420	                                r = func(name, expected_value, value_type, value_contents, m, flags);
421	                        if (!func || r == 0)
422	                                r = bus_print_property(name, expected_value, value_type, value_contents, m, flags);
423	                        if (r < 0)
424	                                return r;
425	                        if (r == 0) {
426	                                if (FLAGS_SET(flags, BUS_PRINT_PROPERTY_SHOW_EMPTY) && !expected_value)
```

## Candidates opened, outcomes, digests

| url | opened (UTC) | bytes / sha256 | outcome |
|---|---|---|---|
| `…/v262/src/shared/bus-print-properties.c` | 2026-10-22T21:12:07Z, HTTP 200 | 17 973 B, `b56aa781be9c29b610156925030d3c4ab720c0ad73d57907d230ca3047302f2a` | **admitted** as S156, primary row URL and excerpt subject |
| `…/v262/src/systemctl/systemctl-show.c` | 2026-10-22T21:12:38Z, HTTP 200 | 121 458 B, `88291f8249d6a86a8bf1f8fc7dc0527e76cfa2d0d6fc07ec54bf09911eaf299a` | admitted as the row's second URL (call site); not the excerpt subject, so it contributes no Gate quote |
| `…/v262/man/systemctl.xml` | 2026-10-22T21:12:07Z, HTTP 200 | 165 132 B, `caca7b87ae3bc8730b070a38d814c698acf82c596df9cb47a58fc7510c7b765c` | rejected (Gate line above); reason verified by grep, not asserted |

Duplicate pre-check, run before fetching: `grep -c "bus-print-properties.c" corpus/SOURCES.md` = 0,
`grep -c "man/systemctl.xml"` = 0, `grep -c "systemctl-show.c"` = 0. Neither named candidate was already a row, so the
duplicate-URL reject class did not apply; the man page was rejected on content instead.

## Verification actually run

- Fetch and digest: `curl -sS -o <file> -w '%{http_code}' -L <url>` for each of the three URLs, then `sha256sum` and
  `wc -c` (`200` ×3; digests above). Access time from `date -u +%FT%TZ` at fetch.
- Revision: `git ls-remote https://github.com/systemd/systemd refs/tags/v262` → `1f7dffaf714cc4488159c498b7a17cf34c5a96d5`
  `refs/tags/v262` (annotated tag; the peeled commit `8cc40e0c…` is the one S153/S154 already record for the same tag).
  Read-only network query; no repo was cloned or mutated.
- Reject evidence: `grep -c "Monotonic" systemctl.xml` → 0; `grep -c "TimestampMonotonic"` → 0;
  `grep -c "ActiveEnter"` → 0; `wc -l` → 3 118. The `show` entry is `systemctl.xml:322-346`; its nearest statements are
  "By default, empty properties are suppressed" (`:328`) and "To select specific properties to show, use
  `--property=`" (`:329-330`).
- Excerpt privacy scan: `grep -cEi 'uid|user@|user-[0-9]|@|vgpnk' excerpt.txt` → **0**. No uid, `user@<digits>`,
  `user-<digits>.slice`, host name or e-mail address appears in the excerpt; the `UID` branch of the printer
  (`:220-226`) was deliberately left out of the excerpt bands.
- Word counts: `wc -w` on each quoted string (5, 4, 5, 8, 6); all ≤25.

## [INFERENCE] and known limits

- [INFERENCE] The zero value itself. The printer receives a uint64 from the manager; that a never-set
  `ActiveEnterTimestampMonotonic` arrives as 0 is not shown by the two files in this row (it would need the
  `org.freedesktop.systemd1.Unit` property getter and the zeroed `dual_timestamp` member). The row's scope cell says so
  and the teaches sentence stays on the rendering. A C1 table row that treats 0 as "never entered active since boot"
  must cite its own support for that meaning; this source row does not carry it.
- No live `systemctl show` was run on this host; no unit name, uid or configured value is reproduced here.
- The excerpt covers the first row URL only. If the C1 counter (`count-c1.sh`, not present in the lane at this writing:
  `.ufo/waves/round-30/` holds `contract.md`, `evidence/`, `rule-text.md`, `w1/`, `wave1-*.json`) requires a digest per
  listed URL, a second excerpt file for `systemctl-show.c` would need its own header with the digest above.
- `S156` is the next free id (highest present: S155, `corpus/SOURCES.md:161`); the assignment's `S15x` placeholder is
  resolved to it so the row satisfies C1's "S156 or higher" clause. Reassign if the Registry seat took S156 meanwhile.

## Bounds compliance

- No git or jj writes anywhere; only `git ls-remote` (no clone needed).
- No pacman transaction, no downgrade, no service restart, no process signalled. Tools installed/updated: none.
- Only `/fast/scratch/hyaku/mori-r30/SrcShowZeroStamp/` (three fetched files, `excerpt.txt`) and this report were
  written. No writer-readable place received tool source or tool output; this report quotes upstream systemd source
  only.
- Finished within the 30-minute bound.

## What Main/BuildCountC1 must do with this

1. Append the row above to `corpus/SOURCES.md` after line 161 (S155).
2. Paste the Gate lines into the round-30 lesson's `## Gate` table.
3. Write the excerpt body to `corpus/evidence/sources-r30/S156.txt` exactly as fenced (tabs, not spaces).
