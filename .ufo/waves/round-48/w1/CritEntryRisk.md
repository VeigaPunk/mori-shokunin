# CritEntryRisk — pre-attack on C2's quote-located blind spot (round 48, wave 1)

Seat: CritEntryRisk. Lane: mori-shokunin. Leaf seat, no subagents dispatched.
Report-only; nothing in the lane repo was mutated (fixture proof below lives in a temp repo).

## 1. What the counter checks vs what it does not

`count-c2.py` (frozen) per row checks: 3 cells, claim ≥ 5 tokens, source cell is one
`S[0-9]{3,}` id, exactly one backticked quote, quote 6–25 whitespace-collapsed tokens,
quote unique in the table, quote occurs as a substring of the *normalised* committed copy
(`normalise`: strip `<…>` → space, unescape entities, collapse whitespace), and the sourced
row exists with `mined` / opened `2026-10-25` / entry in `used-by`, URL among the four frozen
URLs. It never checks that the **claim cell entailed by the quote** — the contract's named
limit ("It does not check that the claim cell follows from the quote", contract §C2).

Result: a quote can be *located* (passes the counter) while the claim states something the
quote contradicts, scopes away, or never mentions. Six pairs below demonstrate, each built
only from the four committed copies. Verified locally:

| copy | sha256 (matches frozen pin) |
|---|---|
| xfs_quota.8.html | 6375e40e…437d5f ✓ |
| quotactl.2.html | 0d4ab273…b6ee8 ✓ |
| errno.h | 66a5ad60…c51622be ✓ |
| aliyun-nas-quota.html | 747fef1b…e22719f ✓ |

Empirical proof in §3: the frozen counter prints `C2=met` for an entry whose eight rows
include all six rejected pairs.

## 2. Six claim/quote pairs the counter scores as located and met, but a careful reader rejects

Quote text is byte-exact from the normalised copy (probe `probe.py`/`probe2.py`,
scratch `r48-CritEntryRisk/`); `words` = `split(" ")` token count (the counter's metric);
`located` = substring hit in the normalised committed copy.

### P1 — claim stronger than the quote (overclaim)
- Claim cell: `Once a user crosses the soft limit, XFS immediately fails their next write with 'Quota exceeded'.`
- Source: xfs_quota.8.html (new S-id ≥ S479, renumbering pending).
- Quote cell: `` `warns users when they exceed their allotted limit, but allows some extra space for current work` `` — 16 words, located at offset 3172 (QUOTA OVERVIEW).
- Why the counter passes: quote present, length ok, unique, row provenance ok.
- Why a reader rejects: the quote *itself* says extra space is allowed beyond the soft limit;
  the failure claim belongs to the hard limit, stated in the next paragraph ("If a user's
  usage reaches the hard limit, further requests … fail with the 'Quota exceeded'
  (EDQUOT) error").
- One-line reviewer check: *Read the two sentences after the quote in the same section — does
  the quoted behavior (warning + grace) match the claim (immediate failure)?*

### P2 — quote from a negation context
- Claim cell: `quotactl() returns ESRCH when a user has exceeded their quota.`
- Source: quotactl.2.html (new S-id ≥ S479).
- Quote cell: `` `No disk quota is found for the indicated user. Quotas have not been turned on for this filesystem.` `` — 18 words, located at offset 3524 (ERRORS, ESRCH).
- Why the counter passes: located, length ok, provenance ok.
- Why a reader rejects: the quote says the opposite — ESRCH is the *no-quota-configured*
  observation ("have not been turned on"), not the exceeded state; the staged entry itself
  uses this quote to distinguish "no quota" from "zero usage".
- One-line reviewer check: *Does the quote assert the state the claim says it signals, or a
  denial of that state?*

### P3 — example-scoped quote generalized into a rule
- Claim cell: `When a write fails due to quota, a user can always recover by writing to /tmp.`
- Source: xfs_quota.8.html (new S-id ≥ S479).
- Quote cell: `` `write the file to some other filesystem (perhaps to a file on /tmp ) where the user's quota has not been exceeded` `` — 22 words, located at offset 5768 (QUOTA OVERVIEW, "Surviving When the Quota Limit Is Reached").
- Why the counter passes: located, length ok, provenance ok.
- Why a reader rejects: the quoted remedy is conditional — "where the user's quota has not
  been exceeded" — and is one editor-workaround *example* ("A third possibility…"), not a
  guarantee; `/tmp` may itself be quota-bound or full. The claim upgrades an example into an
  always-rule and drops the condition.
- One-line reviewer check: *Is the quote describing one conditional workaround, and does the
  claim preserve the condition?*

### P4 — claim about another filesystem
- Claim cell: `btrfs project quotas are administered through quotactl()'s XFS Quota Manager operations.`
- Source: quotactl.2.html (new S-id ≥ S479).
- Quote cell: `` `For XFS filesystems making use of the XFS Quota Manager (XQM), the above operations are bypassed` `` — 16 words, located at offset 2749 (DESCRIPTION).
- Why the counter passes: located, length ok, provenance ok.
- Why a reader rejects: the quoted sentence scopes the Q_X* operations to **XFS**
  filesystems with XQM; the claim applies them to btrfs. The page's own names
  (`xfs_quota`, XQM, `Q_X…`) mark the filesystem.
- One-line reviewer check: *Does the source sentence name the filesystem the claim targets,
  or a different one?*

### P5 — Linux claim from a vendor product page
- Claim cell: `Linux NFS clients enforce subdirectory quota limits natively through the kernel.`
- Source: aliyun-nas-quota.html (new S-id ≥ S479).
- Quote cell: `` `CSI 组件支持为通用型 NAS 存储卷的子目录设置配额限制。使用 subPath 方式挂载 NAS 子目录时，可启用目录配额功能，限制子目录容量，提升资源利用率。` `` — 8 tokens (CJK runs count as single tokens), located at offset 1071 (page metadata/interpage JSON; same sentence appears in the body shortdesc).
- Why the counter passes: located in the committed copy, 8 tokens, provenance ok.
- Why a reader rejects: the source is an Alibaba Cloud **product guide for its own NAS
  service and CSI plugin** (Kubernetes helper), not Linux or NFS kernel behavior — the
  "native Linux kernel" claim is unsupported by a vendor-product page. The staged entry's
  own boundaries treat S479/S481 as "other products' quota semantics", not Linux facts.
- One-line reviewer check: *Is the source a Linux/kernel authority, or a vendor product page
  describing its own service?*

### P6 — number taken from an example (manifest/comment), not a normative statement
- Claim cell: `NAS directory quotas default to 20 Gi per volume; the CSI plugin cannot expand beyond that.`
- Source: aliyun-nas-quota.html (new S-id ≥ S479).
- Quote cell: `` `storageClassName: "alicloud-nas-quota-sc" resources: requests: storage: 20Gi` `` — 6 tokens, located at offset 14057 (example PVC manifest in the body).
- Why the counter passes: located, 6 tokens (floor), provenance ok.
- Why a reader rejects: `20Gi` is an illustrative request size in an example manifest (the
  same example later expands 20Gi → 30Gi); nothing in the page declares a default quota size
  or forbids expansion. The number is lifted from an example, not from a normative statement;
  the inline comments in the same code block describe expansion as enabled (`# 开启目录配额功能，允许动态卷扩容。`).
- One-line reviewer check: *Is the number a declared default/limit in the text, or a sample
  value in an example manifest?*

## 3. Empirical proof: frozen counter meets on an entry containing all six rejected pairs

Fixture repo (temp, `mktemp -d`, `git init`, toplevel verified before first commit):
byte-exact copies of the four frozen sources, `corpus/SOURCES.md` with synthetic mined rows
opened 2026-10-25, and `corpus/knowledge/quota-observability-r48.md` with 8 rows — six
attack pairs (P1–P6) plus two honest pairs (hard-limit sentence; accounting/enforcement
separation).

Command (TMPDIR = lane scratch):

```
$ TMPDIR=.../.scratch/r48-CritEntryRisk python3 .../count-c2.py HEAD --repo $D \
    --entry corpus/knowledge/quota-observability-r48.md
C2=met claims=8 located=8 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=107becdef5e43e2667e7999dc60cd9ff97755c31
rc=0
```

Six of the eight "met" rows are semantically rejected pairs. This is the strongest local
counterexample to the predicate's located-quote check as a proxy for claim support.

## 4. Quirks a wave-2 reviewer should also watch

- **Token = whitespace run**: a CJK-only sentence with no spaces is *one* token (too short);
  P5 passes because English terms supply spaces. "6–25 words" does not mean English words.
- **Located ≠ live**: the copies are dated (2026-10-25); the counter does not check today's
  page (named limit).
- **Uniqueness is table-local**: the same quote could reappear across *other* entries.
- **Sources floor counts distinct URLs**, so one bad claim per source still passes if three
  sources are used.

## 5. Smallest safe correction (for wave 2, not for the counter)

Keep the counter as the mechanical floor (it is frozen; a change after seats score would be a
rule change). Add a wave-2 human reviewer pass with the one-line checks above as the minimum
checklist, plus one cheap mechanical pre-screen per row: flag quotes whose claim shares fewer
than ~1 significant noun/verb with the quote, or where the quote contains negation markers
(`not`, `cannot`, `never`, `尚未`, `未`) while the claim is affirmative. Record any survivors
as limits per the contract's named-limits clause.

## 6. Evidence log

- Read: `contract.md`, `v3-spec.md`, `count-c2.py` (all lines), staged entry
  `quota-observability-r38.md`, `corpus/SOURCES.md` (rows/columns), all four committed copies,
  `evidence/control-c2-donothing.txt`.
- Ran (all read-only on the lane; TMPDIR = lane scratch): `probe.py`, `probe2.py`
  (replicate `normalise`, verify pins + quote location + token counts); `grep` for `S479+`
  rows in lane SOURCES → *no matches* (rows are integrated by L1; final ids ≥ S479, staged
  S477-S482 collide with lane S477/S478 and are renumbered by document); frozen `count-c2.py`
  against the temp fixture repo → `C2=met …` (output above).
- Tooling: no installs/updates were needed (operator RULES.md read; nothing to record).
- UNVERIFIED: the exact final S-id per URL (depends on L1 renumbering) — the pairs reference
  URLs and use `Sid ≥ S479`; the counter's provenance/`used-by` half will only be satisfiable
  after L1 adds the rows, which the contract commits to.
