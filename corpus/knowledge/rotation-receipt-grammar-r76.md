verified-at: 2026-11-02 (round 76; the S591 clock claims below are line-located
against the pinned copy and machine-verified — PASS items=2 with the able-to-fail
arm FAIL rc 1 in the same receipt; no live fetch is a capture body — the serving
pins S241/S581/S589/S590 are the instrument's objects and stand from their own rows)
recheck: 180d
source: S591 (learn.microsoft.com — Acquiring high-resolution time stamps, Win32
sysinfo; pinned copy `corpus/evidence/sources-r76/S591.html` sha256
233893693810754dbd4122a9a43320596a381e179a38ade6636e294d2dbffc1c, 106427 bytes,
opened 2026-11-02; duplicate sweep receipted BEFORE the fetch in
`.ufo/waves/round-76/evidence/source-s591-r76.txt` — no registry row is the
Microsoft QPC guidance page (S589's row only mentions the Windows
QueryPerformanceCounter note inside the Python time page, located-unopened there);
resolved page `<title>` checked before the pin per the r75 lesson's rule; both
located-line anchors machine-verified by the r72 anchor-checker — PASS items=2 rc 0,
able-to-fail mislocation arm FAIL rc 1, `.ufo/waves/round-76/evidence/s591-anchor-check-r76.txt`).
Supporting rows the grammar reads: S589 (the schedule's monotonic clock and its
differences-only validity; the docs' Windows note `:529`), S590 (the Challenge
action's token-update mechanism, anchor-checked r75), S581/S586 (the documented
immunity-time scale), S241 (the observed serving and the compare pin).

# Reading rotation-schedule receipts (round 76): the r70–r75 grammar, distilled

Scope: detection and report only, counts and shapes only. Round 75's planned head (a):
the three-session series and the r74 instrument contract, distilled into the grammar a
reader applies to any `ROTATION_SCHEDULE` receipt — landed as the SKILL.md end-section
decision table (the registry home, append-only) with this entry as its prose ground.
Claims (S1–S5):

- **S1** — per-window classes are SESSION observations, not clock laws. `rotated=yes`
  at window W means the per-response positions moved (or the body changed) WITHIN W in
  ONE session; across the three landed sessions (r70/r74/r75) no stated window was yes
  every time and the two YESes landed at different windows (91 s, 304 s). The only
  stable reading so far is the 31 s window staying no ×3. A reader who derives "every W"
  from one yes has left the grammar.
- **S2** — `rotated=no` means not-observed-in-this-window-this-session; the r75
  single-state session (one body state across all six legs) shows a session can hold no
  rotation at ANY stated window, so all-no is a real outcome, not an instrument failure.
  `rotated=unavailable` is a named dead leg / child setup / unparseable summary /
  timeout — never zero, never a page-state verdict.
- **S3** — the clock leg is now grounded at BOTH layers: the Python docs' invariant
  (cannot go backwards, unaffected by system clock updates, differences-only validity —
  S589 `:524-527`, the Windows note `:529`) and, NEW this round, the vendor's QPC
  guidance for THIS host's receipts: "Yes. QPC does not go backward."
  (`S591.html:918`, 6 words) and "is completely independent of the system time and
  UTC." (`:863`, 9 words). A receipt reader on the Windows workspace host therefore
  knows both WHAT the clock guarantees (S589) and WHICH calls realize it there and what
  the vendor guarantees about them (S591). The instrument still prints differences only.
- **S4** — the scale leg stays S581/S586: the stated windows 31/91/304 bracket the
  documented 300 s challenge minimum/default, so a yes below 300 s reads as
  per-response rotation, not token-TTL expiry; the mechanism leg stays S590
  (a solve updates the token timestamp `:138`, the client resubmits with the UPDATED
  token `:144`). Neither leg decides a TTL value — the three-session series is the
  honest boundary, and widening windows mid-series makes a new experiment (r75 ruled
  out).
- **S5** — receipt hygiene: `window_s_computed` is the children's own as-of-stamp
  arithmetic (QUALITY 161) and may read ±1 s by design; `wall_s` (429 s in both
  instrument runs) is informational; stdout carries counts/shapes/stamps/sha-prefixes
  only; capture bodies are scratch session artifacts, never pinned content.

Limits (declared): this entry adds no session, no window, no instrument byte and no
TTL decision; it organizes what r70–r75 landed. Three sessions bound nothing
statistically. A receipt is the lane's own observation posture on a public vendor page
through the registered child — never a fleet-health or liveness finding, never a census
surface. Boundaries: the vendor's bot management stays the vendor's; the SKILL.md
end-section table is the teachable form and its `## SKILL:905`-pinned prefix is
byte-identical to the entering tip (`8e2875446f8e629a3cc9d8270e7ea29a15c7b590b49558def2df3b8e99c78826`
over the entering 1327 lines).
