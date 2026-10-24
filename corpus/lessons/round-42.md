# Round 42 — lesson (L1 Kimi fresh mori-r42)

Round: 42 · entering `9de7323de482699743619cfa2ee444e7418421e3` · LOG.md
round-42 entry · report `.ufo/reports/round-42/mori.md`.

## Gate

Assimilation (addendum item 10), theme "the OOM evidence chain below the
journal" (FR1/FR13), package `shokuknow/merge/mori/`, opened read-only:

- Candidates considered: 3 (oom-evidence-loss-r38, oom-victim-context-r41,
  oom-tracing-tracepoints-r42).
- Admitted: 2 — `oom-evidence-loss-r38.md` (FR1; runtime-layer lossy link;
  all five cited sources re-fetched 2026-10-24) and `oom-victim-context-r41.md`
  (FR1/FR13; abstract-level victim-context claim).
- Rejected: 1 — `oom-tracing-tracepoints-r42.md`: only source S268 (VOR PDF)
  unreachable from this host (ieeexplore HTTP 202 + 0 bytes; OpenAlex reports
  no repository fulltext); reason recorded with flip condition in
  `.ufo/waves/round-42/assimilation/refused-oom-tracing.md`. Refused, not
  weakened.

New rows (all opened/re-opened this round, quotes located; copies under
`corpus/evidence/sources-r42/`):

- S232 — https://gihyo.jp/article/2026/03/linux_containers-0061 — accessed
  2026-10-24 — located quote (節「メモリコントローラの状態通知」):
  "pollの場合はreventsにセットされるPOLLPRIやPOLLERRビットをチェックすることでメモリに関するイベントが受け取れます"
  (html line ~25427; POLLPRI count 4).
- S233 — https://gihyo.jp/article/2024/08/linux_containers-0056 — accessed
  2026-10-24 — located anchor (節「メモリ使用の制限値」memory.high 小節):
  worked example "memory.highに制限値128MBを追加" with a 256MB stressor and
  no OOM record in the transcript, beside the 節「OOM処理の充実」dmesg
  example "[ 1845.213445] stress-ng invoked oom-killer: gfp_mask=…" (html).
- S234 — iSulad supervisor.c @5a79e5e2 — accessed 2026-10-24 — located quote
  (container_supervisor_add_exit_monitor, under ENABLE_OOM_MONITOR):
  "ret = epoll_loop_add_handler(&g_supervisor_descr, oom_handler_info->oom_event_fd, oom_"
  (copy `S234.c`, anchor count 3).
- S235 — openEuler 24.03 LTS whitepaper PDF — accessed 2026-10-24 — located
  quote (p.27「约束限制」): "由于 cgroup oom 会同时触发容器 cgroup 路径删除，若
  iSulad 对 oom 事件处理发生在 cgroup 路径删除之后，iSulad 则 无法成功捕捉容器
  oom 事件" (pdftotext, count 1; sha256 byte-identical to the pin).
- S241 — MS Learn JA KB 4010058 — accessed 2026-10-24 — located anchor
  (節「診断」): diagnosis-at-detection-time guidance with `ms.translationtype:
  MT` declared in metadata (html, 診断 count 3).
- S262 — doi 10.1109/TSC.2026.3698682 — accessed 2026-10-24 via the
  publisher-deposited OpenAlex record — located quote (abstract): "Our study
  shows that Linux cgroups and the default Out-of-Memory (OOM) mechanism
  lack sufficient container context when selecting victim processes."
  (copy `S262.oa.json`).
- S347 — https://docs.python.org/3/library/ast.html#ast.walk — accessed
  2026-10-24 — located quote (§ast.walk): "Recursively yield all descendant
  nodes in the tree starting at node (including node itself), in no
  specified order." (copy `S347.html`).

Rows touched old→new: none (append-only; no status/recheck/used-by cell of a
prior row changed). Search log: bounded search = the package's OOM-theme
candidates (3 identified, 2 screened in after re-grounding, 1 excluded for
an unreachable source; stop: theme saturated at 2 admits within the 1–3
cap). Collision check: reg 231 ids (S001–S231) vs staged 115 (S232–S346) →
0 collisions; the 0–3-space indented-row guard proven on a scratch fixture
that the column-zero pattern misses (`assimilation/guard/`). Transformation:
staged rows normalized to fleet schema (escaped-pipe sweep parenthetical
removed from S232 teaches; S262 recheck prose → `180d` with the prose kept
in this Gate; opened cells → 2026-10-24; used-by = exactly the admitted
entries); mirror validated rc=0 (`assimilation/validate-receipt.txt`) before
the append. Quarantine register slice (3 rows, all prose-class "could not be
fetched"): S244 not cited by any admitted entry — not appended, hand-check
attempt not run (no adoption depends on it); S262 hand-checked PRESENT via
OpenAlex (adopted); S268 hand-checked ABSENT (entry refused). Spot-check
(non-author, LEARNING.md): pending — the hyaku closure session is the
non-author of record; this Gate records lane-side decisions only.

considerthese/2026-10-24.md (operator-authored, read-only): one unimplemented
proposal mined — "Keep a cumulative survivor ledger" → QUALITY 114, cited
there. No other proposal was implemented; the file was not edited.

## Mistakes

| # | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M1 | landing (near-miss) | this round's L1 began designing the v5 checker from the v4 bytes before inspecting the inherited `.ufo/waves/round-42/` tree, which already held the frozen contract, counters, fixtures and discriminator receipts | none | inspect untracked same-round trees before rebuilding; the inherited freeze was adopted after re-verification (counters re-run, pins hash-checked) — the fix's able-to-fail evidence is the control receipts this round re-ran (`control-c2-before.txt`, `control-c3-before.txt` reproduced unmet before any data) |
| M2 | reference-drift | first scratch-mirror census run emitted false E11 "missing used-by" findings because `sources-census.sh validate --file` resolves used-by paths against the caller's cwd, not the file's tree | CORPUS.md census clause (run from the lane root) | re-ran from the mirror root after copying every referenced surface; rc=0; the false-positive run is retained in the wave tree as the red-before witness |
| M3 | stale-premise | the staged S262 row's recheck command (`aaron papers fetch … -m s2`) no longer resolves (Semantic Scholar now answers "DOI not in Semantic Scholar"); the campaign's 2026-10-23 receipt is not re-runnable | QUALITY freshness discipline (a recheck must re-verify) | re-grounded on the OpenAlex deposited-abstract record; row S262 and the adopted entry now carry a recheck that ran green on 2026-10-24 (`grep -c 'lack sufficient container context'` → 1) |
