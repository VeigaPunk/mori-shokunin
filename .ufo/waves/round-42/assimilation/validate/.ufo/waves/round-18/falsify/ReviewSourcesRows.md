# Scoped review — SOURCES rows S049–S063

## Axes reviewed
Table shape; kind/tier distinction; status vocabulary; `used-by` paths; rejected-row explanations; duplicate URLs; Bounded search 9 completeness.

## Findings (severity order)

### P2 — Bounded search 9 lacks a complete search record

`CORPUS.md:126-128` requires the search note to state identified/screened/included/excluded counts, exclusion reasons, and a stop rationale. `corpus/SOURCES.md:98` gives the question, date, eight scribe reports, and names 9 admitted and 6 rejected rows (counts from the listed IDs), but “opened 15 references and screened one alternative each” does not distinguish the identified and screened populations or say whether the alternatives are included in the 15. It gives no stop rationale. It gives the scope explanation for S054; other exclusion reasons are in the rejected rows, not in the search note. This leaves the search-log record incomplete/ambiguous against rule 5.

### P2 — S054 does not use the required rejected-row form or give a flip condition

The rejected-row contract is `REJECTED: <reason>; flip: <what would change the verdict>` (`CORPUS.md:101-104`). S054 records the scope reason and L1 disposition in `corpus/SOURCES.md:60`, but its `teaches` cell does not use that form and names no condition that would change the rejection. The other rejected rows S055, S057, S059, S061, and S063 include a rejection reason and flip condition (`corpus/SOURCES.md:61,63,65,67,69`).

### P2 — Source anchors omit the required content revision on S049, S053, and S059

`CORPUS.md:99-100` requires an exact location plus a revision (version, commit, or publication date). S049 records no page revision; the cited MkDocs Material version is generator metadata, and its source note explicitly says the content version is unknown (`corpus/SOURCES.md:55`; `.ufo/waves/round-18/build/SrcOwaspLogging.md:9,57`). S053 says the page modified date was not observed and the source note labels “current docs” as an inference (`corpus/SOURCES.md:59`; `.ufo/waves/round-18/build/SrcOtelSensitiveData.md:44-45`). S059 gives reader line numbers but no Git documentation revision in the row, although the source note observed Git 2.56.0 and its 2026-09-28 documentation date (`corpus/SOURCES.md:65`; `.ufo/waves/round-18/build/SrcGitRevList.md:9-11`).

## Checks that passed

- **Shape and IDs:** S049–S063 are sequential rows with the registry's 11 columns; validation emitted no malformed-row or duplicate-ID error. The header is at `corpus/SOURCES.md:5-6`.
- **Kind, tier, status:** reviewed values use the contract vocabularies (`CORPUS.md:91-97,103-106`). Community S055 is tier C, not A; tier-C S057/S059/S061/S063 are rejected, not mined. S053 is queued with `used-by` `—`; the other admitted rows are mined.
- **`used-by`:** validator reported no missing path. I also confirmed the cited source IDs in the mined entries: `corpus/knowledge/evidence-minimization-r18.md:1` cites S049–S052, `corpus/knowledge/freeze-order-r18.md:1` cites S056/S058, and `corpus/knowledge/dispatch-ledger-r18.md:1` cites S060/S062.
- **Rejected reasons:** S055, S057, S059, S061, and S063 each state a reason and a flip condition in their `teaches` cells (`corpus/SOURCES.md:61,63,65,67,69`); only S054 is incomplete as noted above.
- **Duplicate URLs:** no duplicate URL warning names S049–S063. The validator's only W04 warnings are for existing S035 and S037 across scopes, outside this review's row range.

## Census requested

Command executed (read-only):

```sh
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
```

Output:

```text
mori	W04	S035 duplicate url raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in across scopes
mori	W04	S037 duplicate url www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html across scopes
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
```

Exit code: **0**. The maintained validator defines W04 as a cross-scope warning, while duplicate URL+scope is E04 (`scripts/sources-census.sh:24-33`).

## Residual risk and verification gaps

- No LSP device/server was exposed in the mounted tools, so LSP status/references/definition/diagnostics were unavailable. Literal grep was used only to locate candidate rows/references; findings above are based on direct reads of the contract, rows, and cited knowledge entries.
- External source contents were not independently reopened in this scoped contract review; claim-to-source accuracy is outside the checks reported here.
- No tools were installed or updated.