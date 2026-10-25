# ScribeRowQuotactl — S480 row draft (round 48 w1)

Seat: ScribeRowQuotactl (leaf — no subagent dispatch). Task: draft the lane SOURCES.md row
for `https://man7.org/linux/man-pages/man2/quotactl.2.html` as id S480, same schema and rules
as the other row scribes (11 columns, no `|` in cells, status `mined`, opened 2026-10-25,
recheck `180d`, used-by `corpus/knowledge/quota-observability-r48.md`).

## Observed evidence (command + output + exit code)

1. Committed source copy read:
   `corpus/evidence/sources-r48/quotactl.2.html` (absolute:
   `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r48/quotactl.2.html`).
   `sha256sum` → `0d4ab273503d078ee0d9765c616b5082514e7d86e2c6a6b16c70cb7fba8b6ee8`
   (exit 0). This matches the frozen `COPIES` entry in `.ufo/waves/round-48/count-c2.py:39-40`
   (committed copy `quotactl.2.html`) — entropy 0.
2. Live fetch with a browser User-Agent (`curl` exit 0):
   ```
   curl -sS -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36" -o .../quotactl-live.html -w "HTTP %{http_code} bytes=%{size_download}\n" https://man7.org/linux/man-pages/man2/quotactl.2.html
   HTTP 200 bytes=17114
   ```
3. Live vs committed copy: `cmp` → identical (exit 0; byte-for-byte, so the frozen sha256
   also matches the live page fetched on 2026-10-25).
4. Page revision text (footer / COLOPHON, both committed and live):
   - footline: `Linux man-pages 6.19  2026-06-05  quotactl(2)` (raw line 229 of the copy).
   - COLOPHON: "This page was obtained from the tarball man-pages-6.19.tar.gz fetched from
     ⟨https://mirrors.edge.kernel.org/pub/linux/docs/man-pages/⟩ on 2026-09-09."
   So the man-pages release is **6.19**; the page date is 2026-06-05.
5. Located quote grounding `teaches` (18 words, ≤25):
   `No disk quota is found for the indicated user. Quotas have not been turned on for this filesystem.`
   - Present in the committed copy under `ERRORS` → `ESRCH` (raw lines 170-171:
     `<b>ESRCH  </b>No disk quota is found for the indicated user.  Quotas have ...`).
   - Verified present after the counter's normalisation (tags stripped, entities decoded,
     whitespace collapsed) via `python3` check → `quote_present: True | wordcount: 18`.
   - Same quote present in the live bytes (identical file).
6. Access date: 2026-10-25 (live fetch performed 2026-10-25).
7. Registry state: current `corpus/SOURCES.md` registry ends at S478 (line 257); no S479/S480
   rows exist yet (grep for `S480` matches only older-round archives: round-44/45/47 staged-id
   and renumber maps, none in the current registry). S480 is free.
8. Tooling: no tool installed or upgraded (used only `curl` and `python3`, both pre-existing);
   nothing to record under the operator tooling rule.

## Draft row (one line, fenced — for the L1 to integrate)

```
| S480 | quotactl(2) — https://man7.org/linux/man-pages/man2/quotactl.2.html | docs | A | the quotactl(2) syscall surface for filesystem quota manipulation and its error return: soft and hard limits, per-user/group/project operation types, and ESRCH when quotas are not enabled | ERRORS > ESRCH (committed copy lines 170-171); man-pages 6.19, page dated 2026-06-05, tarball man-pages-6.19.tar.gz fetched 2026-09-09, live page fetched 2026-10-25 with a browser user agent | quotactl returns ESRCH when no disk quota is found for the indicated user and quotas have not been turned on for that filesystem, giving hosts a direct signal that quota accounting is off. | mined | 2026-10-25 | 180d | corpus/knowledge/quota-observability-r48.md |
```

Constraint check (11 columns, no `|` inside any cell): id `S480`; source names the URL among the four frozen URLs in count-c2.py; kind `docs`; tier `A`;
scope limits the row to the syscall surface and error return; anchor locates the quote and records revision/access provenance; teaches contains the ≤25-word located quote; status `mined`; opened `2026-10-25`; recheck `180d`; used-by names the C2 entry.

## Gate

Admit **S480** (quotactl(2), man-pages 6.19) as `mined`, tier A, opened 2026-10-25, recheck
180d, used-by `corpus/knowledge/quota-observability-r48.md`. Grounding: the ESRCH quote is the
page's own wording distinguishing "no quota record" from "quotas not turned on", which is the
detection-relevant fact for FR2 filesystem-quota observability; it is located at ERRORS > ESRCH
(lines 170-171) and occurs verbatim in the committed copy (and in the byte-identical live page).
The frozen sha256 of the committed copy holds. No credential material or private URLs appear in
this report. All evidence above was directly observed; nothing is UNVERIFIED.
