# Assimilation refusals — round 43

Theme admitted: what `journalctl --disk-usage` counts (one entry, S470).

## Reject: journal-reach-at-ceiling-r46.md

Reason: the entry cites S414, a `file://` campaign note under
`/home/vgpnk/Projects/shokuknow`, and its recheck greps kernel `MESSAGE`
text (`Killed process`). This lane did not re-open that note as a source,
and a MESSAGE grep is outside the MESSAGE-free journal boundary. The
man-page vacuum sentence on the same page is not adopted through this entry.

Flip: a later round re-opens only the public `--vacuum-size=` sentence,
cites a committed `journalctl --disk-usage` receipt, and does not cite the
campaign note or a MESSAGE grep.

## Reject: failed-scope-keeps-limit-r50.md

Reason: the entry's recheck is `systemctl --user reset-failed` after
creating a scope. That is host service mutation. Province is detection and
report only.

Flip: a later round reads `MemoryMax` of an already-failed scope with
`systemctl show` only, creates nothing, and does not call `reset-failed`,
with the public `systemd.scope(5)` page re-opened by that round.

## S268

Not re-admitted. `curl -sI` of the stampPDF URL on 2026-10-24 returned
HTTP 418, `content-type: text/html`, content-length 15410. No committed
PDF. The r42 refusal stands.
