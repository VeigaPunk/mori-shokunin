# S235's anchor sha256 is transposed; the row is not rewritten

source: S349 — https://www.openeuler.org/whitepaper/openEuler%2024.03%20LTS%20%E6%8A%80%E6%9C%AF%E7%99%BD%E7%9A%AE%E4%B9%A6.pdf — docs, tier A, committed copy corpus/evidence/sources-r42/S235.pdf, opened 2026-10-24
verified-at: 2026-10-24
recheck: 180d

The S235 registry row still says the committed PDF is byte-identical to sha256
ending `a30cda99`. The file `corpus/evidence/sources-r42/S235.pdf` and the
knowledge entry that cites it carry `a30dca99`. This row records the correction.
The S235 teaches cell is not rewritten. The round-42 closure re-derived the
same transposition and routed it here.
