source: S060 (SLSA Provenance v1.0 and in-toto ResourceDescriptor digest), S062 (RFC 8785 JSON Canonicalization Scheme); lane format `.ufo/waves/round-18/frozen/c3-ledger-format.json`
verified-at: 2026-10-21, sources opened by `.ufo/waves/round-18/build/Src{SlsaProvenance,Rfc8785}.md`
recheck: `python3 tools/mori-dispatch-ledger.py verify --repo . --rev <rev> --ledger .ufo/waves/round-18/wave1-attempts.json`; `mkdir -p .scratch && TMPDIR=$PWD/.scratch python3 tools/mori-dispatch-ledger.py --selftest` (TMPDIR must not be under /tmp)

# Dispatch attempts bound to their payload

Wave settlement is mori's surface; a wave's dispatch history is only evidence if each
attempt names exactly what was sent. SLSA provenance records digests of the artifacts a build resolved, and a descriptor with a
`digest` "is assumed to refer to an immutable resource or artifact" (S060); mori applies the same idea to task-call attempts: every
attempt row carries the SHA-256 and byte length of the committed payload, written before
the call and completed with the observed result (`started`, `partial`, `refused` with the
exact refusal text).

## Rules

| Check | Bound when | Unbound / failed when |
|---|---|---|
| payload identity | digest and bytes equal the recomputation from the committed dispatch file | digest missing (all round-17 legacy rows), mismatched, or file absent |
| ledger shape | attempts contiguous from 1, time non-decreasing | gaps, decreasing time |
| settlement | exactly one `started`/`partial` row and it is last | none, two, or not last; any `result` outside refused/started/partial (`RESULT_INVALID`) |
| started count | `started_ids` equals `tasks_count` for `started` | mismatch |

## Limits

- The payload identity is `json.dumps(sort_keys=True, separators=(',',':'),
  ensure_ascii=False)`; it is stable inside CPython for string-only payloads but is **not**
  RFC 8785 canonical (UTF-16 key order, number text, duplicate names differ; S062, round-18
  SrcRfc8785). Re-hash with the same implementation, never across languages.
- A row is *bound* (digest matches) independently of whether the *ledger* is clean: a
  refused-only ledger has bound rows and still fails settlement (`STARTED_MISSING`).
- The ledger proves the committed payload equals what the L1 hashed; it cannot prove the
  task tool received those bytes, nor that an unlogged attempt never happened
  (round-18 CriticC3Operability). Dispatching from the kernel with the payload loaded from
  the committed file narrows, but does not close, that gap.
- Before (round-17 legacy receipts) and after (round-18 ledgers) are different attempt
  populations: this is a capability acquisition with failure-capable selftests, not a
  same-population improvement.
