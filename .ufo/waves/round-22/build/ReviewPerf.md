# ReviewPerf — proposed scan algorithm: repeated reads, copy cost, ordering

Seat: MoriR22.ReviewPerf (reviewer, leaf). Scope: performance review of the proposed
tracked-blob scan algorithm for `tools/mori-retention-reconcile.py` (contract line 13:
"frozen policy R-class regex matching over every tracked blob at measured_revision",
parity with `_scan_git_revision`/`_blob_hits` in `tools/mori-retention-gate.py`).
Detection/report only. No runs, no measurements claimed; all cost statements are
structural analysis of the read pipeline.

## Algorithm as proposed (parity baseline)

1. `git cat-file --batch-check` to resolve `rev^{commit}` (1 process).
2. `git ls-tree -r -z --full-tree <commit>` (1 process), NUL-split entries.
3. For every `blob` entry: `git cat-file blob <oid>` — **one subprocess per blob**.
4. Per blob: `b"\0" in data` skip → `decode("utf-8", errors="replace")` →
   `text.split("\n")` → per line, per policy class `regex.search` → on match
   `sha256(line.encode("utf-8"))`, emit `(path, line, class, line_sha256)`.

## Finding F1 (medium, perf) — per-blob `cat-file` is the dominant needless repeated read

The scan spawns N `git cat-file` processes for N tracked blobs. Each spawn re-opens
the repository, re-initializes the object lookup machinery, and pays fork/exec plus
pipe setup to return one blob. For a real tree (hundreds–thousands of blobs) this is
O(N) process overhead on top of the unavoidable O(total bytes) read — pure waste,
since Git offers a framing mode that reads the identical set in one process.

### One bounded improvement (only)

Replace step 3 with a **single `git cat-file --batch` process**:

- Feed object ids on stdin in the same ls-tree iteration order; `--batch` answers
  sequentially in request order, so hit ordering is unchanged and stays
  deterministic.
- Parse each `<oid> <type> <size>` header, read exactly `size` bytes plus the
  trailing LF. Same bytes, same NUL-skip/decode/split/hash pipeline afterward;
  zero semantic change to hit identity or the R03/R04 partitions.
- A `<oid> missing` reply maps to the existing `git_read_failed`-style setup error
  (exit 2, sanitized) — same failure surface as a non-zero `cat-file` exit today.
- Duplicate oids (same content, two paths) are requested twice and returned twice —
  identical to today's repeated `cat-file blob`.
- Symlink (mode 120000) entries remain `blob` type in ls-tree and are scanned as
  content exactly as now; gitlinks (160000) are already excluded by
  `kind != b"blob"`. Do **not** use `--batch-all-objects`: it scans every object in
  the ODB, not the tree membership — wrong set, strictly more reads.

Bonus inside the same bound: the single ls-tree already yields blob oids for the
policy/allowlist paths at the measured revision, so the R15/R16 "bytes at input
revision must equal bytes at target revision" check can compare object ids
(git oid equality ⇔ byte equality) harvested from that same listing — no extra
`git show <rev>:<path>` reads at all. Input-revision bytes are still read once for
SHA-256 provenance (R24) and regex compilation, as required.

Expected effect (structural, unmeasured): process spawns for the blob phase go
O(N)→O(1); read set, ordering, and per-blob peak memory are identical. No axis
regresses; contract parity text ("read via Git blobs", "split newline exactly as
existing retention gate") is untouched since it constrains content semantics, not
subprocess count.

## Observations — checked, no finding

- **Memory/copy per blob:** bytes → one full `str` → `split("\n")` line list is ~3×
  blob size peak. Contract-pinned: `split("\n")` semantics (a trailing newline yields
  a phantom empty final line that regexes like `.*` *can* match; `splitlines()` would
  drop it and silently change hit enumeration/numbering). Not a defect; do not
  "optimize" to `splitlines` or byte-splitting.
- **Per-line hashing:** `line.encode("utf-8")` runs only inside `regex.search` hits —
  non-matching lines are not re-encoded. Hashing must stay on the replaced-text
  encode, never raw bytes (LegacyFrozen/SrcRejectHash parity evidence).
- **Deterministic ordering:** `ls-tree -r --full-tree` order is git's canonical
  raw-byte tree order (dirs sort as `name/`); iterating it is fully deterministic.
  Hit-list order = (tree order, line number, policy class order). Receipt comparison
  is multiset/identity-based (Counter-style), so blob order is not correctness-load-
  bearing — but `--batch` preserves it anyway.
- **Repeated reads elsewhere:** resolving `rev` once (batch-check), one ls-tree, and
  one blob pass cover the whole scan; receipt/policy/allowlist input-rev reads are
  single-shot. The only repeated-read defect found is F1.

## Residual risk / verification gaps

- No candidate implementation exists yet to re-check against; the recommendation is
  for ImplReconcile's pipeline shape. L1 should confirm the `--batch` framing parser
  (header parse, size-prefixed read, `missing` arm) at integration review.
- `--batch` request-order sequencing is documented git behavior; the framing parse
  is order-independent regardless (headers carry the oid), so a hypothetical
  reordering degrades to a deterministic-ordering nit, not a correctness bug.
- No timing was run or asserted (wave rules forbid execution); spawn-count and
  memory claims are complexity arguments over the read pipeline.

## Tooling

Nothing installed; read-only seat needed no tools beyond builtins.
