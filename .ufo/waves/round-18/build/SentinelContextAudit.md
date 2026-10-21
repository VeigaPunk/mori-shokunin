# Round 18 shared-context audit

## Scope and method

Compared the shared context supplied to this seat with the procedural defects at `corpus/lessons/round-17-verifier-spotcheck.md:303-320` (V1–V3, V5–V14, and L1 authorization) and routed defect 3 at `:403-407`. Read the round-18 contract first, then its named frozen inputs (`c1-policy.json`, `c1-population.json`, `c2-register.json`, and `c3-ledger-format.json`). The classifications below ask whether the shared context itself supplies a concrete pre-action boundary, not whether later behavior proves compliance. Context quotations are from the shared prompt and contain no private values.

Ran the requested read-only command, with the exit status captured:

```text
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-round17-context-check.py --help
exit=0
```

It reports options `--spec PATH` and `--selftest`, and describes itself as a static/advisory gate with no runtime prevention. Neither option was run; in particular, the checker was not run on this report. No tools were installed or updated.

## Per-item findings

| Item | Boundary assessment | Shared-context clause and finding |
|---|---|---|
| V1 | **Concrete** | “Lane reads use only `git -C ... show|log|ls-tree|ls-files|cat-file|rev-list|diff-tree|grep` (never plain git status in the lane: it can refresh the index); never run jj against the lane.” This precludes lane `jj status`/`diff`/snapshot invocations and non-allowlisted lane reads, and explicitly excludes plain lane `git status`. |
| V2 | **Concrete** | “no VCS mutation anywhere: never git add/commit/stash/checkout/switch/reset/pull/push/fetch/tag and never a mutating jj command” plus “always with `git -C <sandbox>`” for the narrow selftest exception. Ad hoc repository writes are barred; sandbox git operations are scoped to the stated selftest and must be rooted at the sandbox. |
| V3 | **Concrete** | “never read, copy, or print credentials, agent.db, oauth or auth files, server.token, credential_pin records or other token/session material.” The separate transcript rule prohibits seat transcript reads and limits any unavoidable read to the named metadata projection. This applies irrespective of whether a copy is ignored or tracked. |
| V5 | **Concrete** | “Never write probe outputs, downloads or scratch to `/tmp`” and “write only your report file; an executor additionally writes only inside its exact assigned clone.” These are explicit destination restrictions covering the accidental out-of-scope file and scratch/output writes. |
| V6 | **Concrete** | “an executor may run only its own item's tool and selftest inside its own clone with `TMPDIR=.../.scratch`,” together with the explicit ban on scratch under `/tmp`. This addresses selftests that might otherwise ignore the caller's temporary-directory setting by forbidding the out-of-scope destination. |
| V7 | **Concrete** | “Sole exception: an executor's own `--selftest` may create and commit to throwaway sandbox repos under its own `$TMPDIR`, always with `git -C <sandbox>` …” and the clone-only write scope delimit both where the sandbox may live and how its git commands are rooted; additional mutations outside that exception are prohibited by “no VCS mutation anywhere.” |
| V8 | **Concrete** | “never copy into any report or file … any session-record field value.” This excludes reason/kind values even if their contents are generic rather than secret. |
| V9 | **Concrete** | “never copy … operator OMP configuration values (routing aliases, model assignments, fallback chains, config line numbers), or any session-record field value”; it also says not to open the listed OMP config and session paths. This directly bounds both config overread/retention and retry/session-value retention. |
| V10 | **Concrete** | “never read, copy, or print credentials … or other token/session material” and “No seat reads OMP transcripts this wave; should one be unavoidable, read only the record fields type, customType and message.role.” This is a pre-action field-projection rule, not permission to parse a full record and discard fields afterward. |
| V11 | **Concrete** | The privacy clause bars copying “content or excerpts of other sessions' transcripts or tool-output logs, session directory or file identities,” and explicitly says not to open the session store, Documents, shell history, or sudoers paths. It covers the named private-source reads and retained actor-trace material. |
| V12 | **Weak / partial** | “Lane reads use only `git -C ...`” and “never run jj against the lane” constrain lane operations, but the context does not expressly forbid a read-only `jj config path`/config query outside that lane or reading the user's jj config. The OMP-config prohibition is not a jj-config prohibition. Thus the lane-specific boundary is useful but does not close the user-config-read part of V12. |
| V13 | **Concrete** | “any session-record field value” is a blanket prohibition; it covers numeric retry/timestamp values as well as textual values, not merely secret credentials or key names. |
| V14 | **Concrete** | The context explicitly says “never plain git status in the lane: it can refresh the index” and limits lane reads to the named `git -C` command allowlist. This directly prevents the cited plain-status action. |
| L1 broad selftest authorization | **Concrete** | “a selftest's existence is not permission to run it. Run only the read-only commands your item names; an executor may run only its own item's tool and selftest inside its own clone with `TMPDIR=.../.scratch`.” The separate selftest exception is executor-owned and limited to its throwaway sandbox. This does not authorize arbitrary seats or unrelated selftests. |

V4 and V15 were not in the requested audit set.

## Routed defect 3 and wave-2 context gaps

The context substantially carries the requested concrete VCS, scratch, and field-projection boundaries. The remaining actionable gap is V12: add a direct pre-action prohibition on invoking `jj` for config-path discovery and on reading repository/user jj configuration; keep permitted lane reads limited to the existing Git allowlist.

The routed closure also cautions that prose is not runtime prevention and a clean final state is not historical conformance. Those caveats are not stated explicitly in the shared context being audited. Add a short wave-2 clause making clear that the instructions are not runtime guards and that a clean later worktree/status or absence of artifacts cannot establish past compliance. This avoids treating outcome evidence as proof that a prior prohibited action did not occur.