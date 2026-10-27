# Round 57 — FR5 observability cross-check

**Scope:** read-only cross-check of FR5 and the round-56 driver-liveness probe; no code, host, or git/jj changes. Frozen predicates were read first (`.ufo/waves/round-57/contract.md:17-25`).

## Finding — watchdog-log continuity across rotation/truncation remains outside Core (LOW; candidate surface)

FR5's current boundary is degraded pid-probe visibility and the fact that argv-substring matches do not establish daemon identity (`PROVINCE.md:48`; mirrored at `corpus/README.md:345`). The round-56 probe adds strict per-event lane facts, malformed/other-line classification, and state-entry shapes; it explicitly says it reads current log lines and `*.round` entry shapes (`tools/mori-driver-liveness.py:32-40,201-237`; `corpus/knowledge/driver-liveness-r56.md:16-25,60-75`). The existing census watchdog arm already reports current log availability and mtime age (`tools/mori-census.sh:725-736`), but neither inspected implementation compares a current log with a previous file identity, byte offset, or retained anchor. A targeted source search for `watchdog.log` rotation/truncation, `copytruncate`, inode, or continuity found no matching implementation in `tools/` or `corpus/` (apart from unrelated generic inode-source material).

**Counterexample to historical completeness:** suppose the log once contained a matching `launch mori round=56` and `complete mori round=56`, but is then replaced/truncated and the currently readable file contains only the launch line. The reader sees only the current file (`mori-driver-liveness.py:209-222`), then reports that parsed line as current `in_flight`/`unclosed` evidence (`:172-173`). It has no observation that the prior close was discarded; an identical current file produced without any prior history yields the same report. Thus the current output is not evidence of complete retained event history. This is a distinct, bounded observability candidate—detecting a changed/truncated log generation or explicitly reporting no continuity guarantee—not a defect against the frozen C1 claim, which is expressly about log-shape facts and does not claim history completeness.

**Verdict:** a plausible surface genuinely outside current Core measurement, but not evidence that the frozen C1 predicate failed. Keep as a candidate only; no change to FR5, contract, or predicates proposed.

## Evidence commands / paths

- `PROVINCE.md:48`; `corpus/README.md:345,800`.
- `tools/mori-driver-liveness.py:32-40,91-102,164-176,201-237`.
- `tools/mori-census.sh:725-736`.
- `corpus/knowledge/driver-liveness-r56.md:16-25,60-75`.
- Read-only search: regex `(watchdog.log.*(rotat|truncat|continuity)|(rotat|truncat).*watchdog.log|copytruncate|inode|log rotation)` over `tools/` and `corpus/`; no rotation/continuity implementation hit.

Report: .ufo/waves/round-57/w1/Mo57MutationTester35.md
