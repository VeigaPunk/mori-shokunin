source: S588 (learn.microsoft.com — Troubleshoot unexpected reboots using
system event logs; pinned copy
`corpus/evidence/sources-r73/S588.html` sha256
aef06f304d2ce0856f30ad7281d0d252b4fa1bc56e5b5a47e1259a8b7f447531, 58472
bytes, opened 2026-11-02; pre-row duplicate sweep receipted BEFORE the fetch
in `.ufo/waves/round-73/evidence/source-s588-r73.txt`)
verified-at: 2026-11-02 (round 73; claims below are line-located against the
pinned S588 copy and machine-verified by the r72 anchor-checker — PASS
items=2 with the able-to-fail label-mutation arm FAIL rc 1, both in
`.ufo/waves/round-73/evidence/boot-anchor-live-r73.txt`; the live read-only
XPath demonstration is receipted in the same file, counts only)
recheck: 180d, or when a re-fetch of the page changes its sha256 against the
pinned copy

# The Windows boot-anchor event surface (round 73)

Scope: detection and report only, counts and shapes only. This entry grounds
the anchor candidate for the events-context pairing's standing limit
`boot_binding=none events_window=recent-200-not-boot-scoped`
(`.ufo/waves/round-71/evidence/events-context-live-r71.txt`): a
boot-scoped event window needs an anchor record that says when the current
boot's log began. The Linux-host census anchors on retained journal anchors;
this host has no journal (PROVINCE Round-62 host note), and the registered
uptime probe returns `boot_identity=absent` (S582 K-boundary). The System
event log itself records a clean-boot marker. Claims (K1–K4, line-located in
the pinned S588 copy):

- **K1** — `S588.html:758` — "Event IDs 12, 13, 6005, and 6009 can show the reboot history and frequency of a computer." (17 words): the page's reboot-history section names the event-id set a boot-anchor read filters on.
- **K2** — `S588.html:787-789` — the 6005 record row: provider `EventLog` (`:788`), "The Event log service was started." (`:789`, 6 words): the clean-boot marker this entry nominates as the anchor candidate; a most-recent-record XPath query for it runs on this host read-only and locates it (receipt rc 0, counts only).
- **K3** — `S588.html:798` — the reboot-types section (event IDs 13, 41, 1074, 6008, 6009): the normal-versus-unexpected-boot classification is a SEPARATE section, unopened this round beyond the heading — the anchor candidate claims presence and queryability only, never boot CAUSE.
- **K4** — the anchor candidate is a CANDIDATE: nothing landed in
  `tools/mori-events-context-win.py` this round; the pairing's receipt line
  still reads `boot_binding=none events_window=recent-200-not-boot-scoped`
  until a round lands (and able-to-fails) the boot-scoped window against
  this anchor.

Limits (declared): 6005 marks the event-log service start, not the kernel
boot instant, and not boot CAUSE (that is K3's unopened section and stays
outside this entry); an unclean shutdown may leave a different marker
sequence — a 6005-anchored window is a clean-boot window, and this entry
claims nothing about dirty boots. Counts and shapes only: no record text,
no timestamps, no computer or user names ever print (the receipt prints rc
and line counts). Boundaries: the query is read-only (`wevtutil qe` through
the same child posture the registered host-events probe uses); no write,
clear, export or reconfigure; boot-state diagnosis stays tsukuroi/operator
(PROVINCE refuses); fleet-liveness verdicts stay with the census gates — an
anchor record is context, not a liveness judgment.
