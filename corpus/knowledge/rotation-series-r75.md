verified-at: 32132cfb (2026-11-02 (round 75; the S590 mechanism claims below are line-located)
against the pinned copy and machine-verified — PASS items=3 with the able-to-fail arm
FAIL rc 1; the series observations are the three committed session receipts cited
per-line in
`.ufo/waves/round-75/evidence/rotation-series-comparison-r75.txt`)
recheck: 180d, or when a fresh session of the stated schedule classifies a window
differently than the series predicts a new observation should be recorded here
(append-only)
source: S590 (docs.aws.amazon.com — CAPTCHA and Challenge action behavior, the AWS WAF
developer guide page the S579 pin's own topic tree locates; pinned copy
`corpus/evidence/sources-r75/S590.html` sha256
8bff4311b27061c944059a4300564347a3c04c6870b88198fa0b4dd0755037fa, 19812 bytes,
opened 2026-11-02; duplicate sweep receipted BEFORE the fetch in
`.ufo/waves/round-75/evidence/source-s590-sweep-r75.txt` — three plausible slugs probed
HTTP 200 but resolved to the guide-index frame and were rejected; both located-line
anchors machine-verified by the r72 anchor-checker — PASS items=3 rc 0, able-to-fail
mislocation arm FAIL rc 1, `.ufo/waves/round-75/evidence/s590-anchor-check-r75.txt`).
Supporting rows the series reads: S589 (the schedule's monotonic clock), S580/S581
(the token-clock scale and its documented immunity times), S241 (the observed serving
and the compare pin).

# The rotation-recurrence series (round 75): three sessions of the stated schedule

Scope: detection and report only, counts and shapes only. Round 74's instrument made
the r70 hand-run session re-runnable; this round runs the SECOND instrument session in
a fresh process and lands the series as knowledge. The stated windows are unchanged
(31,91,304 s) so the sessions stay comparable; the compare pin, UA posture and URL are
byte-identical postures. Claims (S1–S5):

- **S1** — three sessions, three different per-window classifications. r70
  (2026-11-01T19:57–20:07Z, hand-run): 31s=no, 91s=YES, 304s=no. r74
  (2026-11-02T07:55–08:02Z, instrument): 31s=no, 91s=no, 304s=YES. r75
  (2026-11-02T10:29–10:36Z, instrument, fresh process): 31s=no, 91s=no, 304s=no. Every
  per-window datum is quoted from a committed receipt in the comparison receipt.
- **S2** — no stated window classified rotated=yes in EVERY session; each YES occurred
  in exactly one session, at DIFFERENT windows (91s in r70, 304s in r74). The
  per-window classification is not a stable function of the stated window: the honest
  three-session answer is that rotation-class events appear within the 91–304 s scale
  in two of three sessions, at unpredictable windows. The 31s window stayed no across
  all three sessions — the only stable reading so far (three observations, not a law).
- **S3** — body states: every session saw state(s) the others did not (r70
  e4bf924c…/6e7b906d…; r74 3e0ece81…/5d88b3cc…; r75 34353de6… across all six legs).
  r75 is the first single-state session — a session can contain no rotation at ANY
  stated window — so a per-session all-no row is a real outcome, not an instrument
  failure; the serving's state set is not stable across sessions (K5 of
  rotation-schedule-r74.md extended).
- **S4** — mechanism layer (NEW ground, S590): the schedule's per-response arm observes
  the token-update machinery. A challenge interstitial's successful solve "updates the
  token with the challenge solve timestamp" (`S590.html:138`, 9 words) and "the script
  resubmits the original web request using the updated token" (`:144`, 11 words) — so
  a `per-response>0`/`same-bytes=false` window is consistent with a challenge solve
  landing inside the observation window. The expired-token path
  (`:78`, fragment, 9 words) blocks and serves the challenge interstitial; a valid
  token passes like a Count action (no challenge, no rotation). The receipts still
  decide no TTL value and no vendor verdict (the S580/S581 boundary is intact: the
  documented machinery and scale are theirs).
- **S5** — stamp resolution, within design: `window_s_computed=31,91,304` exactly in
  both instrument sessions. Each computed window derives from the children's own
  `as-of=` stamps at 1-second resolution and may read one second off the stated value
  (QUALITY 161: the caller computes the gap) — an observed ±1 s is design behavior,
  not drift; neither instrument session has shown one yet (the r74 closure's window-s=
  305-class note is carried here as the design bound).

Limits (declared): three sessions bound nothing statistically — they make the
recurrence question a SERIES, not an answer; the series decides no TTL, no mechanism
for the serving's state churn, and no verdict on the vendor's bot management. The
instrument compares only WITHIN a run (K5 of rotation-schedule-r74.md); cross-session
comparison is a reading of committed receipts, never a re-use of capture bodies
(deleted at round end, sha prefixes travel on the receipt lines). Boundaries: the
schedule is the lane's own observation posture on a public vendor page through the
registered child; stdout carries counts, shapes, stamps and sha prefixes only; the
vendor's bot management stays the vendor's; no liveness verdict, not a census surface.
