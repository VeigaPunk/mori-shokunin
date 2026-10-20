# ContextCheck17 — round-17 wave-spec context gate (build)

Scope: extend the round-16 static context gate with the four round-17 clauses, in the assigned
clone only. Deliverable file:
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/ContextCheck17/tools/mori-round17-context-check.py`
(clone at base `24526ea9617cd020fee16c28fe4d4a2789dc28cb`; 810 lines; sha256
`4bb17c3759f80b02f8426686ea60f4960be822aee8869b942460cadaa7bab2ae`). No lane file other than this
report was written; no VCS mutation was run anywhere.

## Interface kept from round 16

Same CLI (`--spec PATH`, `--selftest`), same finding ids (`CONTEXT_OK` / `CONTEXT_MISSING` /
`CONTEXT_SETUP`), same rc contract (0 / 1 / 2), same one-JSON-object stdout discipline, same
subprocess selftest. Verified mechanically by importing both modules with
`PYTHONDONTWRITEBYTECODE=1` and comparing the clause tables:

```
r16 ids: ['no_broadcast_exact_id', 'lane_report_resolution', 'no_verification_permission',
          'pacman_pause', 'credential_prohibition', 'write_scope', 'no_live_journal_queries',
          'no_tmp_probe_outputs']
r17 ids: [... same 8 ..., 'no_fleet_root_writes', 'no_background_jobs', 'no_vcs_mutation',
          'transcript_fields_only']
order preserved: True
r16 clause definitions byte-identical: True
new ids: ['no_fleet_root_writes', 'no_background_jobs', 'no_vcs_mutation', 'transcript_fields_only']
```

`clauses_checked` is now 12; a `clause_ids` list was added to the graded payload
(`...:419-420`) — additive only, no key removed.

## New clauses (all after the r16 block, in item order)

Each new clause is two groups: a *mention* group and a *binding* group, so naming without a rule
(or a rule about something else) does not satisfy it.

- `no_fleet_root_writes` (`...:250-269`): the fleet root must be named **as the fleet root**, and
  the path must be `/home/vgpnk/Projects/shokunin` — a lane path below it does not count
  (`(?!/mori)(?![\w-])` lookahead). The rule must bind a write verb (or `misroot`) to the fleet
  root name or path. Prose such as "a seat file at the fleet root is a misroot violation" counts.
- `no_background_jobs` (`...:271-291`): mention of `background job(s)` / `long-lived process(es)` /
  `host service(s)`, plus a prohibition bound to at least one of them.
- `no_vcs_mutation` (`...:293-318`): a git mutation verb (`git add|commit|push|pull|reset|checkout|
  switch|stash|rebase|merge|clean|tag|cherry-pick`), a jj mutation verb (`jj metaedit|abandon|
  rebase|squash|...`), `VCS mutation`, `mutating jj` or `git/jj writes`, plus a prohibition bound
  to one of them.
- `transcript_fields_only` (`...:320-336`): reads must be limited to named record fields
  (`read only the ... fields`, `field-limited`, `limited to ... fields`) **and** printing
  `content` / `errorMessage` must be forbidden. Either half alone fails.

Window semantics. A plain same-line window (`[^\n]{0,n}`) let a ban from the previous sentence bind
to the next sentence's mention — this was observed, not hypothetical: on a mutated copy of the real
one-line context, `no_background_jobs` still passed because the `/tmp` sentence
("... is forbidden for every seat.") sat within 60 characters of "Background jobs". The helper
`_ss(n)` (`...:113-119`) keeps the window on one line but ends it at a sentence-final period
(a period followed by whitespace), while still allowing dots inside paths (`~/.omp`, `agent.db`,
`contract.md`). It is used by all four prohibition groups. The r16 clause bodies were left exactly
as they were.

## Selftest (executed, rc 0)

Command, run inside the clone with scratch confined to it:

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/ContextCheck17
TMPDIR=$PWD/.scratch PYTHONDONTWRITEBYTECODE=1 python3 tools/mori-round17-context-check.py --selftest
```

stdout (verbatim), exit 0:

```
{"arms": 29, "claims_runtime_prevention": false, "clauses_checked": 12, "finding_id": "SELFTEST_OK", "static_only": true}
```

29 arms: 3 positive shapes (context key, nested `taskCall.context`, top-level string document),
1 single-line positive, 12 drop-one-clause negatives (one per clause, each asserting exactly that
clause is missing and no sibling is), 4 near-miss negatives and 4 single-line near-miss negatives
for the round-17 clauses (mention kept, prohibition replaced by a permission), absent-context,
weak-second-context, no-spec-echo (sentinel must not appear in stdout), invalid JSON, missing file.
The near-miss and single-line arms exist because both failure modes were reachable: a clause whose
two groups collapse into one loose pattern, and a window that spans sentences on a one-line context.

## Real-spec run (read-only), rc 0

```
python3 tools/mori-round17-context-check.py \
  --spec /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/wave1-spec.json
```

stdout (verbatim, one line), exit 0, stderr 0 bytes:

```
{"claims_runtime_prevention": false, "clause_ids": ["no_broadcast_exact_id", "lane_report_resolution", "no_verification_permission", "pacman_pause", "credential_prohibition", "write_scope", "no_live_journal_queries", "no_tmp_probe_outputs", "no_fleet_root_writes", "no_background_jobs", "no_vcs_mutation", "transcript_fields_only"], "clauses_checked": 12, "contexts": 1, "finding_id": "CONTEXT_OK", "spec_sha256": "6969eb19533ea65428c1e950271d91482a21a204f947e248c6db405b3907a416", "static_only": true}
```

The spec SHA matches the earlier eight-clause result recorded in
`.ufo/waves/round-17/evidence/context-check-wave1.json` (same `6969eb19...`), so this graded the
same corrected spec, now against 12 clauses instead of 8.

## Falsifiers beyond the selftest

1. Mutation of the real spec, one clause at a time (each replacement string asserted to occur
   exactly once before writing; mutated specs written under the clone's `.scratch/`). Each run
   used `--spec .scratch/mut-<clause>.json`:

   | clause | replacement (prohibition → permission) | rc | missing |
   |---|---|---|---|
   | `no_fleet_root_writes` | "You may write notes under the fleet root /home/vgpnk/Projects/shokunin as needed." | 1 | `["no_fleet_root_writes"]` |
   | `no_background_jobs` | "Background jobs are allowed; long-lived processes and host services are fine." | 1 | `["no_background_jobs"]` |
   | `no_vcs_mutation` | "Git add, git commit, git stash and a mutating jj command are allowed," | 1 | `["no_vcs_mutation"]` |
   | `transcript_fields_only` | "may read whatever fields they like; content and errorMessage text may be printed." | 1 | `["transcript_fields_only"]` |

   The `no_background_jobs` row failed (rc 0, `CONTEXT_OK`) before the `_ss` fix and passes after
   it; the other three bit on the first attempt. Each mutation leaves every other clause green, so
   the four clauses are independent and none is satisfied by its neighbours' text.

2. r16 positive context fed to the r17 checker (r16 module imported read-only; its
   `_selftest_context()` written to `.scratch/r16-positive-context.json`): rc 1,
   `missing == ["no_fleet_root_writes", "no_background_jobs", "no_vcs_mutation",
   "transcript_fields_only"]` — the retained r16 clauses still pass on a context that predates
   them, and the four additions are not vacuous.

3. CLI contract: no arguments → rc 2 `CONTEXT_SETUP reason=spec_required`; `--selftest --spec x`
   → rc 2 `CONTEXT_SETUP reason=selftest_takes_no_spec`; unreadable spec → rc 2
   `CONTEXT_SETUP reason=spec_unreadable`. All stdout-only, single JSON object each.

## Limits (unchanged in kind from r16)

Advisory presence check only: it cannot stop a seat from broadcasting, writing at the fleet root,
starting background jobs, mutating git/jj, or printing transcript content, and every payload
carries `claims_runtime_prevention: false`. It does not detect a context that states a clause and
then contradicts it, and it cannot credit anaphora — a context saying "The fleet root is
`/home/vgpnk/Projects/shokunin`. Never write there." is reported as missing
`no_fleet_root_writes`, because the gate demands the write ban be bound to the fleet-root name or
path, not to "there". The r16 clauses keep their original non-sentence-bounded windows; only the
four round-17 clauses use `_ss`. Near-miss arms exist only for the round-17 clauses.

## Tools and installs

None. Only the distribution `python3` (3.14.8) was used; no pacman/uv/npm/cargo activity, no
network access, no downloads. No background jobs, no journal queries, no `/tmp` writes.

## Mutations and writes

- Wrote: the tool above (clone), this report (lane), scratch fixtures under
  `<clone>/.scratch/` (`mut-*.json` ×4, `r16-positive-context.json`, `spec-run.stdout`,
  `spec-run.stderr`, `cli-*.out`); selftest `mkdtemp` trees were created under that `.scratch/`
  and removed afterwards.
- No git/jj command of any kind was run for state change; no `git add/commit/stash/checkout/
  switch/reset/pull/push`, no `jj` mutation. `git status --porcelain` in the clone shows only
  `?? .scratch/` and `?? tools/mori-round17-context-check.py`.
