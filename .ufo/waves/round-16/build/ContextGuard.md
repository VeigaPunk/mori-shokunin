# ContextGuard — round-16 lane report

Seat: `MoriR16.ContextGuard` (executor, leaf — no subagent dispatch)
Assigned file: `tools/mori-round16-context-check.py` (new, sole owned file)

## What was delivered

A small **static** gate `tools/mori-round16-context-check.py` that reads one
wave spec document (`--spec PATH`), collects every string value under a key
literally named `context` (a top-level JSON string is itself the context), and
requires each collected context to explicitly carry eight contract restrictions:

| clause id | required explicit content |
|---|---|
| `no_broadcast_exact_id` | forbid `agent://all` AND require exact seat-id / L1 addressing |
| `lane_report_resolution` | `Report:` trailers bound to a resolved write location (relative-to-root / absolute / report-dir wording) |
| `no_verification_permission` | skip builds/tests/gates wording or selftest-is-not-permission clause |
| `pacman_pause` | host-wide pacman pause declared |
| `credential_prohibition` | credential/auth/agent.db/token/session-material mentioned AND prohibited |
| `write_scope` | writes confined to assigned file + report path |
| `no_live_journal_queries` | explicit ban binding `live` to `journal`/`journalctl` queries/reads (rev2) |
| `no_tmp_probe_outputs` | `/tmp` mentioned AND forbidden for probes/outputs/downloads (rev2) |

### Verdicts (one JSON object on stdout, never echoes spec text — only clause
ids, counts, `spec_sha256`)

- **rc0** `CONTEXT_OK` — every collected context satisfied every clause.
- **rc1** `CONTEXT_MISSING` — `missing: [...]` clause ids absent from ≥1
  context; `context_absent: true` when no `context` string exists at all.
- **rc2** `CONTEXT_SETUP` — spec unreadable / invalid JSON / `--selftest`
  combined with `--spec` / missing `--spec`. A gate misconfiguration, never a
  spec verdict.

### Explicit non-claim

Every payload carries `"claims_runtime_prevention": false` and
`"static_only": true`. This is a presence check over spec text; it does not
prevent runtime violations and does not detect contradiction within a clause.

### Selftest (implemented, NOT executed)

`--selftest` builds spec documents under a fresh `tempfile.mkdtemp` tree and
invokes this CLI as a real subprocess:

- 3 positives (top-level `context`, nested `taskCall.context`, bare string doc) → rc0/`CONTEXT_OK`
- 8 per-clause negatives — each positive fragment is authored to feed only its
  own clause's regex groups, so dropping one must yield rc1/`CONTEXT_MISSING`
  containing exactly that clause id and no other
- absent-context arm → rc1 with all eight clauses + `context_absent`
- second partial context alongside a complete one → rc1 (all-contexts rule)
- invalid JSON and missing file → rc2/`CONTEXT_SETUP`

Each arm asserts rc, `finding_id`, single-JSON stdout, and
`claims_runtime_prevention is false`. Emits `SELFTEST_OK`/`SELFTEST_FAIL`.

## Rev2 — two additional clauses (L1 request, same wave)

L1 directed two more explicit static clauses: `no_live_journal_queries` and
`no_tmp_probe_outputs`, with author modes (selftest arms) auto-extended —
each new fragment is a separate drop arm, now 15 arms total
(3 positives + 8 per-clause drops + 3 setup/absent + 1 missing-file).

Expected wave1 verdict change: the ORIGINAL wave1 context fails
`no_live_journal_queries` — it contains only the selftest-scoped "no
network/live reads" phrasing, which deliberately does NOT satisfy the
clause (the prohibition must bind `live` to `journal` within 20 chars on one
line). `no_tmp_probe_outputs` passes on wave1 ("never use /tmp for deliberate
probes/downloads" already binds the prohibition to /tmp probe writes). So
the gate is expected to report rc1 `CONTEXT_MISSING` with
`missing: ["no_live_journal_queries"]` on the original spec, flipping to
`CONTEXT_OK` only on a corrected context carrying an explicit live-journal
ban — matching L1's red-original / green-corrected plan. Non-claim unchanged:
`claims_runtime_prevention: false` on every payload.

## Design notes / retained evidence

- Follows `tools/mori-round15-regressions.py` conventions: shebang, contract
  docstring, argparse, single stdout JSON, isolated-subprocess selftest,
  rc2 = setup. [INFERENCE: convention reuse, read at tools/mori-round15-regressions.py:1-115,2300-2353]
- Clause regexes are anchored on phrases actually present in the wave
  `context` text (verified against `.ufo/waves/round-16/wave1-spec.json:3`
  and `wave1-dispatch.json:421` `taskCall.context`): "Never agent://all",
  "message ONLY exact seat id or L1 agent://MoriR16", "every `Report:` trailer
  path is relative to … write it at", "skip ALL builds/tests/…", "selftest is
  NOT permission", "ALL pacman transactions PAUSED", "Never read/copy/query/
  change ~/.omp/agent/agent.db*", "All writes ONLY … your exact assigned file
  plus your absolute report path".
- All-contexts rule: when a spec carries multiple `context` strings
  (top-level + `taskCall`), every one must satisfy every clause — a compliant
  shared context cannot shadow an incomplete one.
- No source or fixture files were read for copying, and none were changed;
  no credential/auth file was opened; `agent.db` was never touched.
- `chmod +x` applied by the write tool; shebang `#!/usr/bin/env python3`;
  stdlib only (`argparse, hashlib, json, re, subprocess, sys, tempfile,
  pathlib`) — no installs needed or performed.

## Disclosure (per L1 no-checks clarification)

No deviation. Every prior action in this lane was read-only static review:
`read`, `grep`, directory listings, and `python3` used solely to parse
already-present spec JSON files. No live journalctl query, no gate/test/
build/smoke execution, no background job, no selftest run, no /tmp output,
no outside-lane write. Nothing inadmissible was produced.

## Risks / limits

- Phrase-based: a reworded-but-equivalent context (e.g., "writes confined to"
  without `only`) may yield `CONTEXT_MISSING` — fail-closed by design; a
  false green requires the phrases to appear while meaning the opposite,
  which reviewers must still catch.
- The gate does not see per-seat `items[].prompt` text except when a prompt
  contains a `"context"` key (it doesn't) — by design it checks shared
  contract context only.
- The tool cannot itself verify that a `Report:` clause is *used* at dispatch
  time; it only checks the text is present.

## Blockers

None.

## Suggested L1 checks (not run here)

- `python3 tools/mori-round16-context-check.py --spec .ufo/waves/round-16/wave1-spec.json` → expected rc1 `CONTEXT_MISSING` (`no_live_journal_queries`) on the ORIGINAL spec; rc0 `CONTEXT_OK` after L1's context erratum adds an explicit live-journal ban
- `python3 tools/mori-round16-context-check.py --selftest` → rc0 `SELFTEST_OK` (15 arms)
- Negative smoke: spec missing a clause → rc1 `CONTEXT_MISSING` naming it.

Report: .ufo/waves/round-16/build/ContextGuard.md
