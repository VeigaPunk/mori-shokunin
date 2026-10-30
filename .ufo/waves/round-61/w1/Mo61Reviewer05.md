# Mo61Reviewer05 — C2 no-false-negative audit

Axes: contract fidelity, benign-edit invariance, evidence reproducibility. Frozen controls/counters were not edited. Recommendation only; no admission or saturation claim.

## Finding (medium): undocumented five-word minimum rejects a contract-valid quote

`contract.md:64-68` requires a byte-located quote of **at most** 25 words and at least eight distinct bytes; it imposes no five-word minimum. Frozen `count-c2.py:136-139` additionally requires `5 <= wordcount(q)`, before location validation. Consequently a legitimate short source line is rejected.

Isolated measurement receipt, using the unchanged frozen `measure()` and default floor 40:

```text
positive control:
C2=met pointers=47 rows=47 same=0 moved=0 changed=47 quotes_ok=47 spans_ok=47 sources=6 failed=none rev=scratch-files-no-git

replace only the psi.c:1712 row with:
| psi.c:1712 | same | - | `if (psi_enable) {` |

C2=unmet pointers=47 rows=47 same=0 moved=0 changed=46 quotes_ok=46 spans_ok=46 sources=6 failed=quote_words:psi.c:1712 rev=contract-valid-short-quote
```

The replacement is an exact substring at `corpus/evidence/sources-r61/psi.c:1712`, has three words and **14 distinct bytes**, and stays distinct from the other 46 quotes. It satisfies the frozen quote contract yet flips `met`. This is a counter false negative, not a proposed counter/contract amendment. The available scribe draft independently contains this row at `w1/Mo61ScribePsi1.md:94`.

## Requested benign mutations

All mutations were independent against the same synthetic counter-positive control, with unchanged source pointers, pins, registry binding, provenance, and default floor 40:

| Mutation | Result | Interpretation |
|---|---|---|
| Reverse the 47 complete ledger rows | met, 47/47 quotes | Row-order invariant holds. |
| Fix prose `recieve` → `receive` outside the table | met, 47/47 quotes | Prose-typo invariant holds. |
| Rewrap one quote across a physical newline | unmet, 46 rows | Physical-line parser drops the row. |
| Add whitespace padding outside that quote's backticks | met, 47/47 quotes | Contract-preserving cell whitespace remains accepted. |

Exact output for each passing mutation (only diagnostic revision label is synthetic):

```text
C2=met pointers=47 rows=47 same=0 moved=0 changed=47 quotes_ok=47 spans_ok=47 sources=6 failed=none rev=scratch-files-no-git
```

Rewrapped row anchor: `cgroup-v2.rst:1066-1081`; its isolated positive-control quote changed from:

```text
This is the authoritative documentation on the design, interface and
```

to:

```text
This is the authoritative documentation
on the design, interface and
```

Observed:

```text
C2=unmet pointers=47 rows=46 same=0 moved=0 changed=46 quotes_ok=46 spans_ok=46 sources=6 failed=rows_missing:cgroup-v2.rst:1066-1081;rows_ne_pointers rev=scratch-files-no-git
```

Cause: `count-c2.py:119-122` splits the ledger into physical lines before `ROW.match`; `ROW` at lines 41-43 requires the full quote and closing table cell on the same line. **This is not independently a frozen-contract defect:** the specified ledger row is one physical Markdown table row, and its quote must remain a byte substring, not merely the same whitespace-normalized words. Do not classify arbitrary internal quote reflow as harmless under this contract. The padding control exercises genuinely benign whitespace instead.

## Method and evidence limits

- Contract read first. No installed tools, production edits, git/jj mutations, clone, commits, registry writes, or other-runtime invocation.
- `xd://lsp` was requested but returned `No such tool`; semantic definition/reference/diagnostic requests were unavailable. Findings use direct frozen source inspection and measured Python behavior, not grep as semantic proof.
- Counter SHA-256: `82d0fee6124685f8a50f93550f3665703a33dce644948958db642a77d5aec2d8`.
- Scratch: `/fast/scratch/hyaku/mori-r61/Mo61Reviewer05`; `TMPDIR` set there. The disk guard printed `/tmp 97.5G`, `/var/tmp 533.9G`, scratch `342.9G` free; its directory-consumer scan timed out at 30 seconds. No ENOSPC occurred.
- To honor the reviewer's VCS-mutation prohibition, this was **not** a committed scratch-clone CLI test. Python imported the frozen counter using `importlib.util.spec_from_file_location`; only `cat(repo, rev, path)` was temporarily replaced with a scratch-file reader. `measure(repo, rev, FLOOR_DEFAULT)` and `fmt()` were unchanged. Reported exit-equivalents derive from `ok`; they are not child-process exit claims.
- Positive control construction: enumerate all 47 actual pointers from `system-pressure-r24.md`; for each pointer select the first unused single source line in its own pinned file with 5–25 words, at least eight distinct bytes, no backtick or pipe; emit a `changed` row with that line's actual location. Add the provenance trio and six synthetic SOURCES binding rows. This is a deliberately synthetic validator-positive fixture, **not** a truthful upstream-change ledger or a registry validation. All six real pinned copies were used unmodified. Short-quote replacement was applied only after this fixture measured met.
- The baseline/prose/reversal/reflow/padding variants were materialized under the seat's scratch, measured independently, and then removed. All small receipts required for the finding are preserved above.

Actual committed CLI command exercised:

```sh
env TMPDIR=/fast/scratch/hyaku/mori-r61/Mo61Reviewer05 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/count-c2.py 7370a731abcafc4c803111de7c22cd6264d63be1 --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch /fast/scratch/hyaku/mori-r61/Mo61Reviewer05
```

```text
C2=unmet pointers=47 rows=0 same=0 moved=0 changed=0 quotes_ok=0 spans_ok=0 sources=0 failed=entry_absent rev=7370a731abcafc4c803111de7c22cd6264d63be1
exit=1
```

## Residual risk / verification gaps

No complete accepted ledger was available: the production `*r61*` knowledge-entry search returned none; the only `*Psi*` report available was `Mo61ScribePsi1.md`, containing 41 rows. Its rows measured 28 valid quotes with 13 `quote_words` failures, six missing anchors, and `sources_floor`/`rows_ne_pointers` under an isolated synthetic registry binding. The source-row executor also records the missing six-row registry draft at `Mo61ExecSourcesRows.md:5`.

Thus **the requested integrated-draft met-to-met confirmation remains unverified**. The evidence establishes two benign invariants on a positive measurement control and one concrete contract false negative; it does not certify the eventual ledger or committed after-state. Main should run the frozen CLI at the integrated revision with `--scratch` and the default floor, and repeat the two contract-preserving mutations against that exact ledger if an authorized committed fixture is available. No counter changes are recommended within this freeze.
