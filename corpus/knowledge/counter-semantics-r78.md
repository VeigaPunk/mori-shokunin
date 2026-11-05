verified-at: 2026-11-02 (round 78; the S593 claims below are line-located against the
pinned copy and machine-verified; the association table's two `<td>` counter-name cells
are located at their exact lines)
recheck: 180d
source: S593 (learn.microsoft.com — Memory Performance Information, Windows desktop
legacy archive; pinned copy `corpus/evidence/sources-r78/S593.html` sha256
7eb834fc1450f8f93d94e11cd66c4c7a84049631ca1b1032ffbb3019ff6a9bac, 48532 bytes, opened
2026-11-02; duplicate sweep receipted BEFORE the fetch in
`.ufo/waves/round-78/evidence/source-s593-r78.txt` — no registry row is this class of
page: 0 rows carry the URL, "PerfOS" or the WMI class name; four wrong-URL candidates
fetched and rejected as 404 before the located page was found; resolved page `<title>`
checked before the pin per the r75 lesson rule; all five located-line anchors
machine-verified by the r72 anchor-checker — PASS items=5 rc 0, able-to-fail mislocation
arm FAIL rc 1, `.ufo/waves/round-78/evidence/s593-anchor-check-r78.txt`).
Supporting rows the entry reads: S592 (the typeperf command reference — the transport
the probe executes), S574 (the GlobalMemoryStatusEx function — the r64 probe's
one-struct API read), S572 (the exhaustion-event semantics — the r63 ground the K4
inference rested on).

# The vendor's own counter-name association (round 78): what S593 adds to the counter surface

Scope: detection and report only, counts and shapes only. Round 78 lands the r77 C2
instrument in committed bytes (the D77-1 recovery) and closes the ground gap that entry
declared: `counter-win-r77.md` K4 grounded the counter OBJECT only indirectly — the
paths were live-enumerated (K3) and the commit-pair quantity was doc-LINKED through
S572's exhaustion-event semantics. S593 is the vendor page that associates memory
object performance counters with the memory-manager structures by name:

- **K1** — `S593.html:720` — "The following table associates memory object performance
  counters with the data returned by the memory performance functions in the" (19
  words; the sentence continues through three linked structure names on the same line,
  so the located contiguous span ends at "the", recorded as such in the row): the page
  is a vendor association table, not prose the lane interprets — the mapping below is
  the vendor's, read off the table cells.
- **K2** — `S593.html:750` + `:756` — the counter-name cells "Committed Bytes" and
  "Commit Limit" (2 words each, under the column header "Memory object counter (unless
  otherwise noted)", `:730`, 6 words): the two names the probe reads
  (`\Memory\Committed Bytes`, `\Memory\Commit Limit`) are the vendor's memory-object
  counter names. The K4 object ground no longer rests only on the S572 exhaustion
  inference — the names are vendor-stated on this page.
- **K3** — the same table's structure column links Commit Limit to
  MEMORYSTATUSEX.ullTotalPageFile AND PERFORMANCE_INFORMATION.CommitLimit: the r64
  probe's one-struct read (S574) and the r77 counter read (S592's command) are the SAME
  quantity family by the vendor's own table — vendor-stated, not lane-inferred. The two
  registered reads remain distinct surfaces (an API struct vs a PDH counter path);
  S593 relates them, it does not merge them.
- **K4** — named absence: Pages/sec is NOT on this page (the table has no rate-counter
  row; the page's grep surface carries no Pages/sec line). The paging rate's semantics
  stay exactly as landed in `counter-win-r77.md` K5 — an OS-computed per-second figure
  over typeperf's own collection interval, live-verified by the round-77 receipts. No
  rate claim is manufactured from this page.

Limits (declared): S593 is a previous-versions ARCHIVE page (v=vs.85) — it describes a
legacy documentation surface; its association table is the vendor's record of the
counter-to-structure mapping, and the 180d recheck cell governs its drift watch. The
page associates names and structures; it defines neither thresholds nor causes — no
diagnosis, alerting or baseline claim is grounded here (the FR8/FR12 boundaries carry
unchanged). The association is Windows-version-annotated (the table's Task Manager
columns split by Windows Server release); this entry claims nothing about non-server
SKUs. The second live session this round
(`.ufo/waves/round-78/evidence/counter-win-live-r78.txt`, AVAILABLE surfaces=4 ok=4
samples=2 rc 0 at the landed bytes) is a separate reading — never a series (K6 of
`counter-win-r77.md`).

Boundaries: this entry edits no instrument byte, adds no counter path, and changes no
registered probe; the probe's redaction and write-scope posture is unchanged
(counter-win-r77.md). Coverage-map: deepens the Windows-host resource-runway arm's
GROUND (the commit pair's names and their structure linkage are now vendor-stated);
the surface roster itself is unchanged.
