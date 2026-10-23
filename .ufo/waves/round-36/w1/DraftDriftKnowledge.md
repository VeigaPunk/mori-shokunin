measured 2026-10-23T12:03:37Z
# DraftDriftKnowledge — C1 knowledge-entry draft

## Behavior and artifact
Prepared the requested C1 knowledge entry as a draft for `corpus/knowledge/source-drift-r36.md`; this seat did not write that product path. The complete draft is below. It distinguishes all five per-row states and run-level exit 2, states the interface from the frozen C1 contract, and makes each table action independently actionable under QUALITY 100.

VERDICT: not assessed — this is a knowledge-entry draft; no tool implementation or runtime behavior was tested.

## Provenance and findings
- `.ufo/waves/round-36/contract.md:33-47` gives the exact interface, copy selection, row states, summary and exit behavior. Lines 40-45 distinguish unavailable from drifted; line 42 defines fresh as byte-hash equality; line 47 says exit 2 is setup error and read-only.
- `corpus/QUALITY.md:779-782` requires every decision-table action cell to contain an imperative verb and resolving object, readable without its header.
- `corpus/knowledge/disk-write-rate-r33.md:1-5` and `corpus/knowledge/drift-repin-r20.md:1-12` show the provenance trio at entry start.
- Opened the requested pinned fleet source: https://raw.githubusercontent.com/VeigaPunk/shokunin/6a1dd8ce1a3165a25f9f2b774b21449e0d125c94/CORPUS.md . The opened text includes `## SOURCES.md — where a shokunin learns` and rules requiring opened sources and a grounded `teaches` claim. A search for `S205` in this pinned text returned no matches; the S205 row is therefore not independently visible there. The draft cites S205 and the URL as assigned, without claiming the row itself was present in the opened revision.
- Timestamp command: `timeout 5s date -u +%FT%TZ` → `2026-10-23T12:03:37Z`.

## Gates, touched surfaces, and limits
- Gate evidence: contract and QUALITY text were read; no source-drift tool, test, counter, or runtime check was run. No gate pass is claimed.
- Touched surface: this report only. Proposed product surface: `corpus/knowledge/source-drift-r36.md` (draft below, not written). No scratch files or tool installs.
- Out of scope: tool implementation, judging, integration, and edits to `corpus/SOURCES.md` or the knowledge directory.
- Known limit: the submitted draft is grounded in the frozen C1 interface and the opened pinned fleet contract. The separately drafted S205 registry row and live tool behavior were not observed.
- Artifact path: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/w1/DraftDriftKnowledge.md`.

```DRAFT corpus/knowledge/source-drift-r36.md
source: S205 — fleet `CORPUS.md`, `## SOURCES.md — where a shokunin learns`; https://raw.githubusercontent.com/VeigaPunk/shokunin/6a1dd8ce1a3165a25f9f2b774b21449e0d125c94/CORPUS.md
verified-at: 2026-10-23
recheck: on-release

# Checking source-copy freshness (round 36, C1)

## Decision table

`fresh` proves only byte identity with the committed copy; it does not prove that the row's `teaches` claim is right.

| Tool state | Meaning | Reader action |
|---|---|---|
| `fresh` | SHA-256 of the fetched body equals the newest committed copy. | Recheck the row's `teaches` field against the cited source. |
| `excerpt` | The bytes differ, but the non-empty copy bytes with ASCII whitespace stripped at both ends occur contiguously in the fetched body. | Compare the row's `teaches` field with the fetched body. |
| `drifted` | The copy is neither byte-identical nor a matching excerpt of the fetched body. | Reopen the row's URL and review its `teaches` field against the fetched body. |
| `unavailable` | The GET failed through a connection error, timeout, or non-2xx final status; redirects are followed and the tool may retry. This is an unavailable probe, not drift. | Retry the GET for the row's URL after access is available. |
| `no-copy` | The row has no URL or no copy file; no fetch is made. | Check the row's URL cell and the newest copy under `corpus/evidence/sources-r<N>/`. |
| exit 2 | Run-level setup error: `SOURCES.md` is missing or unreadable; no verdict. | Restore `DIR/corpus/SOURCES.md` or its read permission, then rerun `python3 tools/mori-source-drift.py --root DIR`. |

## Interface

`python3 tools/mori-source-drift.py --root DIR`. Reads `DIR/corpus/SOURCES.md`; a registry row is a line starting `| S` followed by three digits. Its id is the first cell, its URL is the first `http://` or `https://` URL in the second (`source`) cell with trailing `.,;)` stripped. Its copy is the file `DIR/corpus/evidence/sources-r<N>/<id>.<ext>` (any extension) with the highest integer `N`. Per row, in registry order, print one line `<id> <state>`.

Then print `MORI_SOURCE_DRIFT rows=N fresh=a excerpt=b drifted=c unavailable=d no-copy=e`. Exit 0 when `drifted=0`, 1 when any row is drifted, 2 on a setup error (missing or unreadable SOURCES.md). Read-only: no writes.
```