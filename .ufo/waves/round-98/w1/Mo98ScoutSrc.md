# Mo98ScoutSrc — independent source re-open, mori round 98 w1

Scope: re-open the four C1 sources, verify pinned copies, anchors, quotes (word counts), teaches cells, and independently check namespaces(7) §/proc/sys/user. All work unprivileged (uid 1000), no sudo, no sysctl changes, no namespaces created. Scratch /fast/scratch/hyaku/mori-r98/Mo98ScoutSrc was used and removed. Fetches: curl 8.23.0, plain GET, 2026-11-05T21:35:29Z–21:35:30Z.

## 1. Live re-open — URL, UTC access, status, bytes, sha256, pinned equality

| row | URL | UTC access | HTTP | bytes | sha256 (live) | live == pinned |
|---|---|---|---|---|---|---|
| S629 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/sysctl/user.rst | 2026-11-05T21:35:29Z | 200 | 2564 | 2a83137d76138cd8355fa6d63d0200f8a92b01aa73880c6567f81b819eb7207a | YES |
| S630 | https://man7.org/linux/man-pages/man2/unshare.2.html | 2026-11-05T21:35:29Z | 200 | 25450 | bc19c6eb79eeca98f99357c724615b87e6ede1cf8eeaa7846c432e2d2f47972a | YES |
| S631 | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/proc_ns.h | 2026-11-05T21:35:29Z | 200 | 2004 | 63376480b58e72b13c36b69daf536a089a2af558544863e9e2f1fe37e7ffd537 | YES |
| S632 | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/uapi/linux/nsfs.h | 2026-11-05T21:35:29Z | 200 | 3843 | da2a23c34182dec8b65bf8be116e169d0970f68907024e00c6ada4c846c04d65 | YES |

All four live sha256 values equal the pinned copies byte-for-byte (cmp exit 0) AND equal `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 600deb7ed2695f54b289cf5b6c3931e0fa9c8bb3:corpus/evidence/sources-r98/<file> | sha256sum` — so pinned == committed landing bytes == live upstream. SOURCES row hashes match exactly.

Extra fetch (not a pinned row; scratch only): namespaces.7.html — 2026-11-05T21:35:29Z, HTTP 200, 25329 bytes, sha256 f8e08716df1f4afdf05b22e11b010e14f47311eb92f0a948fedbb95099c36aa7.

## 2. SOURCES.md rows S629–S632: anchor lines, quote, teaches

- S629 — VERDICT supported. Anchors verified: intro lines 14-16 hold claim-1 text; lines 24-29 hold the two creation-charging paragraphs (quote-3 at 24-25, continuing line 26; quote-4 at 28-29, continuing 30-31); max_user_namespaces section header at line 74 (underline 75, blank 76), its sentence "The maximum number of user namespaces that any user in the current user namespace may create." at lines 77-78 (16 words). Teaches cell (cap for each user inside the reader's namespace + nested charging + runway reading) is backed by lines 77-78, 28-31 and 33-34 ("This recursive counting of created objects ensures that creating a user namespace does not allow a user to escape their current limits.").
  - Caveat (no fault): the identical sentence recurs at lines 83-84 under max_uts_namespaces (upstream copy-paste quirk; namespaces(7) raw lines 291-292 says "uts namespaces" for that file, so the user.rst uts entry is the odd one out). Anchor lines 74-78 select the right instance; a bare substring search would hit both.
- S630 — VERDICT supported. Third ENOSPC entry exactly at raw lines 252-256 (header 252 "<b>ENOSPC </b>(since Linux 4.9)", body 253-256); quote "doing so would have caused the limit defined by the corresponding file in /proc/sys/user to be exceeded." (17 words) located in tag-stripped text, spanning raw 254-256 with `<i>` around /proc/sys/user. Colophon line 400: "Linux man-pages 6.19 2026-02-08 unshare(2)" matches the row's version claim. Teaches cell (namespace-limit ENOSPC signature, not a full disk) supported; hedged "can be".
  - Note: a different ENOSPC entry at raw line 244 ("since Linux 4.9; beforehand EUSERS") fires on the CLONE_NEWUSER nesting-depth limit — same errno, different cause. The knowledge entry's reading rules attribute ENOSPC to the /proc/sys/user limit and never name the nesting-depth path. Minor gap, no claim is falsified by it.
- S631 — VERDICT supported. Quote "PROC_USER_INIT_INO = USER_NS_INIT_INO," (3 words; source has tabs before/around `=`) exact at line 44, inside the initial-inode enum (lines 41-48). Teaches cell ("fixed, kernel-defined inode … tell the initial namespace from created ones by the link's inode number alone") goes one step beyond the file's own text (the file only names the constant), but is confirmed empirically on this host: `stat -Lc %i /proc/self/ns/user` → 4026531837.
- S632 — VERDICT supported. Quote "USER_NS_INIT_INO = 0xEFFFFFFDU," (3 words; tabs in source) exact at line 50, inside `enum init_ns_ino` (starts line 47). 0xEFFFFFFD = 4026531837 (computed). Host corroboration: `readlink /proc/self/ns/user` → `user:[4026531837]`.

## 3. Knowledge claim rows (corpus/knowledge/userns-runway-r98.md)

| claim | located (pinned lines) | words | verdict |
|---|---|---|---|
| 1 files in /proc/sys/user set per-user per-userns limits | S629 14-16 | **29 > 25** | supported text; **quote over the ≤25-word rule → needs-amend** |
| 2 max_user_namespaces = per-user cap in reader's userns | S629 74-78 (quote 77-78) | 16 | supported |
| 3 creation charged to creator user, checked in its userns | S629 24-25 (+26) | 23 | supported |
| 4 charge also to enclosing-ns creators (nested counting) | S629 28-29 (+30-31, 33-34) | 22 | supported |
| 5 limit hit ⇒ ENOSPC (since Linux 4.9) | S630 252-256 (quote 254-256) | 17 | supported |
| 6 PROC_USER_INIT_INO = USER_NS_INIT_INO | S631 44 exact | 3 | supported |
| 7 USER_NS_INIT_INO = 0xEFFFFFFD = 4026531837 | S632 50 exact | 3 | supported |

Claim 1 needs-amend detail: support is intact — S629 lines 14-16 read "The files in this directory can be used to override the default / limits on the number of namespaces and other objects that have / per user per user namespace limits." Suggested ≤25-word trim (20 words, same support): "override the default limits on the number of namespaces and other objects that have per user per user namespace limits".

## 4. namespaces(7) §"The /proc/sys/user directory" — independent cross-check (raw lines of live HTML; section starts line 249)

- 299-300: "The values exposed by these files are the limits for the user namespace in which the opening process resides." (19 words) — confirms the entry's "limit for the namespace the reader runs in".
- 302-303: "The limits are per-user.  Each user in the same user namespace can create namespaces up to the defined limit." (19 words) — confirms per-user reading.
- 319-320: "When a namespace is created, the object is also accounted against ancestor namespaces." (13 words) — confirms the nested-charging reading (claim 4).
- 311-312: "Upon encountering these limits, clone(2) and unshare(2) fail with the error ENOSPC." (12 words) — confirms the ENOSPC signature (claim 5 / reading rules).
- 314-316: "For the initial user namespace, the default value in each of these files is half the limit on the number of threads that may be created (/proc/sys/kernel/threads-max)" — confirms the Observed note: 245730/2 = 122865.

No contradiction: the knowledge entry's per-user / nested-charging / ENOSPC reading is independently confirmed by namespaces(7).

## 5. Host corroboration (read-only /proc, as uid 1000, no sudo)

- `readlink /proc/self/ns/user` → `user:[4026531837]`
- `stat -Lc %i /proc/self/ns/user` → `4026531837`
- `/proc/sys/user/max_user_namespaces` → `122865`; `/proc/sys/kernel/threads-max` → `245730`

## 6. Summary verdicts

S629 supported · S630 supported · S631 supported · S632 supported · knowledge claims 2-7 supported · knowledge claim 1 needs-amend (quote 29 words > 25; support intact at S629:14-16; trim suggested above) · namespaces(7) confirms the entry's readings.

Unrun checks: tools/mori-userns-runway.py, count-c1.py, count-c2.py, controls (not in my scope); no user namespace created (not needed); user_namespaces(7)/clone(2) not fetched (out of scope).
