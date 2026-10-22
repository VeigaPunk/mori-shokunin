# SrcUnitActiveEnter — frontier source row for C1 (systemd `ActiveEnterTimestampMonotonic`)

Seat: scribe, leaf (no subagents, no background jobs). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Writes: this report and `/fast/scratch/hyaku/mori-r30/SrcUnitActiveEnter/` only. No git/jj writes, no unit
or process action, no pacman, nothing installed.

## 1. Result in one line

The assigned candidate URL is already inside `corpus/SOURCES.md:128` (row S122), so it is rejected as a
duplicate and the row is drafted from the four code files that carry the same fact
(`src/core/unit.c`, `src/core/dbus-unit.c`, `src/shared/bus-get-properties.h`, `src/basic/time-util.c`,
all at tag v262). The duplicate reject is verified, not asserted: the document does carry the fact.

## 2. Everything opened this round (fetch record)

| url | http | accessed (UTC) | sha256 of bytes fetched | outcome |
|---|---|---|---|---|
| `https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit.c` | 200 | 2026-10-22T21:12:18Z | `47e98d394462e05bf4bc0be2d1105fa8c21044cc9f5ebf00464f1742a92efcb7` | admit (row primary) |
| `https://raw.githubusercontent.com/systemd/systemd/v262/src/core/dbus-unit.c` | 200 | 2026-10-22T21:12:17Z | `47f461aeb70722ae7fb02f9b89ffd12db1639b7750a02e218dc27747f4cd9d0d` | admit (property table) |
| `https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/bus-get-properties.h` | 200 | 2026-10-22T21:15:23Z | `ddbbac057692f7f4edb3278a5df9c80af6ce8b7046f93bfc37595287ca0d2753` | admit (`BUS_PROPERTY_DUAL_TIMESTAMP`) |
| `https://raw.githubusercontent.com/systemd/systemd/v262/src/basic/time-util.c` | 200 | 2026-10-22T21:12:18Z | `373dac1568e2bfc8e295e05e86e577f5444f6048a53d91c04b1fad68eb257f52` | admit (`dual_timestamp_now`, `CLOCK_MONOTONIC`) |
| `https://raw.githubusercontent.com/systemd/systemd/v262/man/org.freedesktop.systemd1.xml` | 200 | 2026-10-22T21:12:17Z | `59cfeea5144e169369ee81f2b797fe9eb63ec18cb6aa918c2e66a7d5218117ca` | **reject — duplicate URL (S122)** |
| `https://raw.githubusercontent.com/systemd/systemd/v262/src/basic/time-util.h` | 200 | 2026-10-22T21:12:18Z | `45e934d294f2ff0ca92cc7f1fcede1ef92862d20b276e305282cec5f3cba37e6` | **reject — duplicate URL (S154)** |
| `https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/bus-get-properties.c` | 200 | 2026-10-22T21:12:18Z | `06755221460fbdb8ad7bacbb2d1c34dbea8fc6cc3061e12f9bdc0c408a666071` | reject — no usec getter body |
| `https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/bus-util.h` | 200 | 2026-10-22T21:12:36Z | `145076586e534df103db9e73d70f65e0ec4b98642607a3c96e23d6088e9b508f` | reject — no macro, no property |
| `https://raw.githubusercontent.com/systemd/systemd/v262/src/core/dbus-util.h` | 200 | 2026-10-22T21:12:37Z | `7dac128023d62dd73ab4e0825c177eb8fc0b3175df3dcd91f798710b713a98fe` | reject — no macro, no property |
| `https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit.h` | 200 | 2026-10-22T21:12:37Z | `563a8180f79038ddc28d267cd971c902bd6c1df438ac92cee6e0a6612b8e1eca` | reject — field declaration only |
| `https://raw.githubusercontent.com/systemd/systemd/v262/src/libsystemd/sd-bus/bus-util.h` | 404 | 2026-10-22T21:12:37Z | `d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed` (the 404 body) | reject — HTTP 404 |
| `https://github.com/systemd/systemd/archive/refs/tags/v262.tar.gz` | 200 | 2026-10-22T21:13:09Z | `6aa77506c0644aa67f940a48e3d3a7368601f787e4f249139516d353f107bcab` (19038647 bytes) | locator only, not a row |

The tarball was fetched only to find where `BUS_PROPERTY_DUAL_TIMESTAMP` is defined (the per-file fetches of
`src/shared/bus-util.h` and `src/core/dbus-util.h` do not contain it); it is not a candidate row. The 404 body
sha `d5558cd4…` equals the sha round 29 recorded for the same 404 body (`corpus/lessons/round-29.md:56,59`).

## 3. The given candidate is a duplicate (verified)

`grep -n -F "v262/man/org.freedesktop.systemd1.xml" corpus/SOURCES.md` returns line 128 only, row S122,
which lists this URL among four and whose `scope` cell already names `ActiveEnterTimestampMonotonic`.
The document does carry the fact, at `man/org.freedesktop.systemd1.xml:2783-2784` (CLOCK_REALTIME and
CLOCK_MONOTONIC 64-bit microsecond timestamps, "entered the active state") and at `:2789-2790`
("The fields are 0 in case such a transition has not yet been recorded on this boot."). So the reject
reason is duplicate URL, never "does not carry the fact".

## 4. Drafted SOURCES.md row (ready to paste; `S15x` placeholder)

Next free id at the entering tip is S156 (`grep -o "^| S[0-9]\{3\} " corpus/SOURCES.md | sort -u | tail -1`
prints `| S155 `; S156 and S157 are absent). Replace `S15x` with the id the C1 author allocates.

```
| S15x | systemd v262 unit `ActiveEnterTimestamp` pair and its `active_enter_timestamp` stamp — https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit.c ; https://raw.githubusercontent.com/systemd/systemd/v262/src/core/dbus-unit.c ; https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/bus-get-properties.h ; https://raw.githubusercontent.com/systemd/systemd/v262/src/basic/time-util.c | code | A | what `ActiveEnterTimestampMonotonic` reads at the v262 release tag: the `Monotonic` sibling that `BUS_PROPERTY_DUAL_TIMESTAMP` generates from the `active_enter_timestamp` dual stamp, `unit_notify()` copying `dual_timestamp_now()` into that field on the state-change edge into active or reloading, the helper's `CLOCK_MONOTONIC` microsecond half, and the `malloc0`-zeroed `Unit` that keeps the field 0 until such an edge; not this host's unit values or a live `systemctl show`, not `CLOCK_MONOTONIC` behavior across suspend, not the journal's `__MONOTONIC_TIMESTAMP` (S122), not the prose sentence at `man/org.freedesktop.systemd1.xml:2789` (that document is S122's) | `src/core/unit.c:103` (`u = malloc0(size);`), `:2766` (`dual_timestamp_now(&u->state_change_timestamp);`), `:2773-2774` (the copy into `active_enter_timestamp`); `src/core/dbus-unit.c:974`; `src/shared/bus-get-properties.h:103-105` and `:13` (the getter is a NULL cast); `src/basic/time-util.c:76-84` (`:80` the monotonic half); tag v262 | `ActiveEnterTimestampMonotonic` is the monotonic half of a unit's `active_enter_timestamp`, refreshed only on the edge into active or reloading, and a `malloc0`-zeroed unit keeps it 0 until that edge happens. | mined | 2026-10-22 | on-release | corpus/lessons/round-30.md, corpus/knowledge/earlyoom-invocation-scope-r30.md |
```

No cell contains `|`. `used-by` paths match the C1 contract's named surfaces.

## 5. Gate lines for `corpus/lessons/round-30.md` (wave-context format)

One admit line, then one reject line per opened-and-rejected candidate.

```
| S15x | https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit.c (with src/core/dbus-unit.c, src/shared/bus-get-properties.h and src/basic/time-util.c at the same tag) | 2026-10-22T21:12:18Z | `47e98d394462e05bf4bc0be2d1105fa8c21044cc9f5ebf00464f1742a92efcb7` | `:2766` (1 word): "dual_timestamp_now(&u->state_change_timestamp);"; `:2773-2774` (7 words): "if (!UNIT_IS_ACTIVE_OR_RELOADING(os) && UNIT_IS_ACTIVE_OR_RELOADING(ns)) u->active_enter_timestamp = u->state_change_timestamp;" | admit, code, mined |
| S15x | https://raw.githubusercontent.com/systemd/systemd/v262/man/org.freedesktop.systemd1.xml | 2026-10-22T21:12:17Z | `59cfeea5144e169369ee81f2b797fe9eb63ec18cb6aa918c2e66a7d5218117ca` | `:2789-2790` (17 words): "The fields are 0 in case such a transition has not yet been recorded on this boot." | reject, duplicate URL already carried by S122 (corpus/SOURCES.md:128 lists this URL and its scope names `ActiveEnterTimestampMonotonic`); the document does carry the fact at :2783-2784 and :2789-2790 |
| S15x | https://raw.githubusercontent.com/systemd/systemd/v262/src/basic/time-util.h | 2026-10-22T21:12:18Z | `45e934d294f2ff0ca92cc7f1fcede1ef92862d20b276e305282cec5f3cba37e6` | `:110-113` (12 words): "static inline bool dual_timestamp_is_set(const dual_timestamp *ts) { return timestamp_is_set(ts->realtime) || timestamp_is_set(ts->monotonic); }" | reject, duplicate URL already carried by S154 (corpus/SOURCES.md:160); the zero-means-unset convention here is corroboration only |
| S15x | https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/bus-get-properties.c | 2026-10-22T21:12:18Z | `06755221460fbdb8ad7bacbb2d1c34dbea8fc6cc3061e12f9bdc0c408a666071` | `grep -n "int bus_property_get_usec"` over the v262 tree returns nothing; `src/shared/bus-get-properties.h:13` defines the name as `((sd_bus_property_get_t) NULL)` | reject, does not carry the fact: no usec property getter is implemented in this file |
| S15x | https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/bus-util.h | 2026-10-22T21:12:36Z | `145076586e534df103db9e73d70f65e0ec4b98642607a3c96e23d6088e9b508f` | `grep -n "DUAL_TIMESTAMP"` returns nothing; the file is 73 lines of bus transport and registration declarations | reject, does not carry the fact: the dual-timestamp property macro is at `src/shared/bus-get-properties.h:103` |
| S15x | https://raw.githubusercontent.com/systemd/systemd/v262/src/core/dbus-util.h | 2026-10-22T21:12:37Z | `7dac128023d62dd73ab4e0825c177eb8fc0b3175df3dcd91f798710b713a98fe` | `grep -n "DUAL_TIMESTAMP"` returns nothing; the file holds `BUS_DEFINE_SET_TRANSIENT*` macros | reject, does not carry the fact: no `ActiveEnterTimestamp` and no dual-timestamp property macro |
| S15x | https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit.h | 2026-10-22T21:12:37Z | `563a8180f79038ddc28d267cd971c902bd6c1df438ac92cee6e0a6612b8e1eca` | `:313` (2 words): "dual_timestamp active_enter_timestamp;" | reject, carries the field declaration and the :311-315 comment only: no property mapping, no clock call, no zero rule |
| S15x | https://raw.githubusercontent.com/systemd/systemd/v262/src/libsystemd/sd-bus/bus-util.h | 2026-10-22T21:12:37Z | `d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed` | body line 1 (3 words): "404: Not Found" | reject, HTTP 404 at v262 — the header is `src/shared/bus-util.h`, which carries no dual-timestamp macro either |
```

## 6. Excerpt file body (save as `corpus/evidence/sources-r30/S15x.txt`)

Primary URL only, contiguous range with three lines of context each side of the quoted lines
(2766 and 2773-2774); header `sha256` equals the row's primary sha.

```
id: S15x
url: https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit.c
sha256: 47e98d394462e05bf4bc0be2d1105fa8c21044cc9f5ebf00464f1742a92efcb7
accessed: 2026-10-22T21:12:18Z
lines: 2763-2777

2763	
2764	        /* Update timestamps for state changes */
2765	        if (!MANAGER_IS_RELOADING(m)) {
2766	                dual_timestamp_now(&u->state_change_timestamp);
2767	
2768	                if (UNIT_IS_INACTIVE_OR_FAILED(os) && !UNIT_IS_INACTIVE_OR_FAILED(ns))
2769	                        u->inactive_exit_timestamp = u->state_change_timestamp;
2770	                else if (!UNIT_IS_INACTIVE_OR_FAILED(os) && UNIT_IS_INACTIVE_OR_FAILED(ns))
2771	                        u->inactive_enter_timestamp = u->state_change_timestamp;
2772	
2773	                if (!UNIT_IS_ACTIVE_OR_RELOADING(os) && UNIT_IS_ACTIVE_OR_RELOADING(ns))
2774	                        u->active_enter_timestamp = u->state_change_timestamp;
2775	                else if (UNIT_IS_ACTIVE_OR_RELOADING(os) && !UNIT_IS_ACTIVE_OR_RELOADING(ns))
2776	                        u->active_exit_timestamp = u->state_change_timestamp;
2777	        }
```

Line 2763 is blank; the separator after each line number is a TAB (`cat -A` shows `2763^I$`).

## 7. Privacy scan of the excerpt

`awk 'NR>=2762 && NR<=2778' unit.c | grep -n -E "@|[0-9]{4,}|vgpnk|host|\.slice|user-"` prints nothing.
No uid, no `user@<digits>`, no `user-<digits>.slice`, no host name, no e-mail address, no host unit name,
no `/etc/default/earlyoom` value. All lines are upstream generic C.

## 8. Known limits

- One excerpt file carries one contiguous range of one file. The zero-default half of the fact is anchored at
  `src/core/unit.c:103` (`u = malloc0(size);`) and `src/basic/time-util.c:76-84` is anchored at `:80`, but
  neither is inside the excerpted range, so neither appears in a Gate quote. If the C1 author's counter
  requires the zero rule itself to be quoted, the alternative range is `src/core/unit.c:96-110` quoting
  `:103` — it cannot be combined with the `:2763-2777` range in one excerpt file.
- The prose statement of the zero rule exists upstream only in `man/org.freedesktop.systemd1.xml:2789`, whose
  URL is S122's; this row therefore carries the rule as code behaviour (zero-initialized `Unit`, assignment
  only on the edge), not as a quoted sentence.
- `.ufo/waves/round-30/count-c1.sh` is not present at the entering tip (the directory holds `contract.md`,
  `rule-text.md`, `evidence/`, `w1/`, `wave1-*.json`), so the Gate and excerpt shapes above follow the
  wave-context text and the round-29 precedent (`corpus/lessons/round-29.md:55-60`) and were not validated
  against the counter.
- The four admit URLs are one row; only the first (unit.c) is excerpted. If the counter demands a Gate quote
  per URL, this row is a miss and should be reported as one, not fixed by inventing an excerpt.
- Word counts above were computed with Python `len(s.split())` on the exact strings (1, 7, 17, 12, 2, 3); the
  wave-context says `wc -w`, which agrees on these ASCII strings.

## 9. Tools

None installed or updated. Only `curl`, `sha256sum`, `grep`, `awk`, `sed`, `tar`, `python3` (already present)
were used.
