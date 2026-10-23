# RevSupS212S213 — re-open S212 (stat.rst) and S213 (iostats.rst)

Reviewer: `mori-r36-w2-RevSupS212S213-23`. Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin` (read-only); landed tip `bf0df77fee4b6ef54a90aea09335c7617f125151`, round base `6bd57097`. Leaf member: no subagent dispatch.

Attack: S212/S213 SOURCES rows + their pinned copies. Verify (a) both v7.2 tag-pinned URLs fetch and each copy sha256-equals the fetched body; (b) the S212 anchor quotes (17-value line, 512-byte sector) and S213 anchor quotes (cumulative-monotonic fields, reset conditions) are contiguous and ≤25 words in the fetched bodies; (c) the `supersedes S180/S181` form follows CORPUS rule 2. FAIL on any mismatch.

## 1. Row extraction (tip vs round base)

Command (scratch only; lane untouched):

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 6bd57097:corpus/SOURCES.md > /fast/scratch/hyaku/mori-r36/RevSupS212S213/base-SOURCES.md
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin show bf0df77fee4b6ef54a90aea09335c7617f125151:corpus/SOURCES.md > /fast/scratch/hyaku/mori-r36/RevSupS212S213/tip-SOURCES.md
```

Row-set diff (Python row parser over the extracted files):

```
S180 in_base= True in_tip= True identical_base_tip= True
S181 in_base= True in_tip= True identical_base_tip= True
S212 in_base= False in_tip= True
S213 in_base= False in_tip= True
```

S212/S213 are **new** rows between base and tip (append-only additions); S180/S181 are byte-identical between base and tip (no in-place edit). Tip rows (from `tip-SOURCES.md`):

```
| S212 | Linux block-device stat file documentation v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/block/stat.rst | docs | A | the v7.2 /sys/block/<dev>/stat format: the 17-value line, the 512-byte sector unit, completion-time counting and the tick fields | Documentation/block/stat.rst:2-5,21-22,71-73,75-80; tag v7.2 | supersedes S180 — The stat file is one line of 17 decimal values; its sector counts use the standard 512-byte sector, not a device or filesystem block size, and grow when an I/O completes; the millisecond wait values can rise faster than 1000 per second when several requests wait. | mined | 2026-10-23 | on-release | corpus/knowledge/disk-write-rate-r33.md |
| S213 | Linux I/O statistics fields documentation v7.2 (tag-pinned counterpart of the docs.kernel.org page in S033) — https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/iostats.rst | docs | A | the v7.2 iostats field semantics: which fields are cumulative, when they reset, how field 10 grows, and the sysfs/procfs equivalence | Documentation/admin-guide/iostats.rst:22,33-36,75-76; tag v7.2 | supersedes S181 — All fields except field 9 are cumulative monotonic counters; they reset at boot, on device reattachment or reinitialisation, or on counter overflow; field 10 grows while field 9 is nonzero; /proc/diskstats and /sys/block/<dev>/stat carry the same 17 statistics. | mined | 2026-10-23 | on-release | corpus/knowledge/disk-write-rate-r33.md |
```

## 2. Fetch + copy sha256 equality

Fetched the **exact row URLs** (v7.2 tag-pinned raw github URLs), copied the committed lane copies into scratch, hashed both:

```
$ cp /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r36/S212.src ./S212.copy
$ cp /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r36/S213.src ./S213.copy
$ curl -fsSL --retry 4 --retry-delay 5 -o stat.rst 'https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/block/stat.rst'
$ curl -fsSL --retry 4 --retry-delay 5 -o iostats.rst 'https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/iostats.rst'
$ sha256sum S212.copy S213.copy stat.rst iostats.rst
4c35b795a518ceefea985f11e53b51f71d58fc99bf5a0920ca3738f13c90cb2e  S212.copy
166bdc8fd4ee9e53bcb86804e0d22d50c89314dcfc1a248814b0069300034124  S213.copy
4c35b795a518ceefea985f11e53b51f71d58fc99bf5a0920ca3738f13c90cb2e  stat.rst
166bdc8fd4ee9e53bcb86804e0d22d50c89314dcfc1a248814b0069300034124  iostats.rst
$ wc -c stat.rst iostats.rst
 4315 stat.rst
 8592 iostats.rst
```

| id | fetched body | bytes | sha256 (fetched) | lane copy | sha256 (copy) | equal |
|---|---|---|---|---|---|---|
| S212 | `stat.rst` | 4315 | `4c35b795…cb2e` | `corpus/evidence/sources-r36/S212.src` | `4c35b795…cb2e` | YES |
| S213 | `iostats.rst` | 8592 | `166bdc8f…4124` | `corpus/evidence/sources-r36/S213.src` | `166bdc8f…4124` | YES |

Both copies are byte-identical to the live fetched tag-pinned bodies. Glob over `corpus/evidence/sources-r36/` shows exactly one copy per id (`S212.src`, `S213.src`) — no stale decoy copies for these ids; the copies are `fresh` (byte-equal) under the C1 drift byte-behavior.

## 3. Anchor quotes: contiguous and ≤25 words

Normalized fetched bodies (whitespace runs → single space). For each attacked claim, the minimal contiguous source span grounding it was located and word-counted.

### 3.1 S212 — stat.rst (`Documentation/block/stat.rst:2-5,21-22,71-73,75-80`)

Body lines (numbered read of the fetched file):

```
21:The stat file consists of a single line of text containing 17 decimal
22:values separated by whitespace.  The fields are summarized in the
71:discarded from this block device.  The "sectors" in question are the
72:standard UNIX 512-byte sectors, not any device- or filesystem-specific
73:block size.  The counters are incremented when the I/O completes.
79:waited on this block device.  If there are multiple I/O requests waiting,
80:these values will increase at a rate greater than 1000/second; for
```

| claim | contiguous source span (normalized) | contiguous | words |
|---|---|---|---|
| 17-value line | `The stat file consists of a single line of text containing 17 decimal values` | in | 14 ≤25 |
| 512-byte sector | `the standard UNIX 512-byte sectors, not any device- or filesystem-specific block size` | in | 12 ≤25 |
| completion-time counting | `The counters are incremented when the I/O completes.` | in | 8 ≤25 |
| tick fields | `If there are multiple I/O requests waiting, these values will increase at a rate greater than 1000/second` | in | 17 ≤25 |

Anchor ranges all contain their quotes: 21-22 (17-value line), 71-73 (sector unit + completion), 75-80 (ticks; text at 78-80), 2-5 (title/intro). PASS.

### 3.2 S213 — iostats.rst (`Documentation/admin-guide/iostats.rst:22,33-36,75-76`)

Body lines (numbered read of the fetched file):

```
22:Both files contain the same 17 statistics. ``/sys/block/<device>/stat``
33:All fields are cumulative, monotonic counters, except for field 9, which
34:resets to zero as I/Os complete. The remaining fields reset at boot, on
35:device reattachment or reinitialization, or when the underlying counter
36:overflows. Applications reading these counters should detect and handle
75:Field 10 -- # of milliseconds spent doing I/Os (unsigned int)
76:    This field increases so long as field 9 is nonzero.
```

| claim | contiguous source span (normalized) | contiguous | words |
|---|---|---|---|
| cumulative-monotonic fields | `All fields are cumulative, monotonic counters, except for field 9` | in | 10 ≤25 |
| reset conditions | `reset at boot, on device reattachment or reinitialization, or when the underlying counter overflows` | in | 14 ≤25 |
| field 10 grows | `This field increases so long as field 9 is nonzero` | in | 10 ≤25 |
| same 17 statistics | `Both files contain the same 17 statistics` | in | 7 ≤25 |

Anchor lines all contain their quotes: 22 (same 17 statistics), 33-36 (cumulative/reset), 75-76 (field 10). PASS.

## 4. `supersedes S180/S181` form and superseded rows

CORPUS rule 2 (fleet `/home/vgpnk/Projects/shokunin/CORPUS.md:116-118`): *"Append-only. Only `status`, `recheck` and `used-by` change in place… A correction is a new row whose `teaches` opens `supersedes S0NN —`."*

- S212 teaches cell opens `supersedes S180 —` ✓ (form `supersedes S### —`, em dash; verified `opens_supersedes_SNNN_emdash= True`).
- S213 teaches cell opens `supersedes S181 —` ✓.
- Superseded rows S180/S181 are untouched — byte-identical between round base `6bd57097` and tip `bf0df77` (row-set diff, §1) and still present at tip (not deleted). The S180/S181 debt predates the round; the supersession is recorded by the new rows (S212/S213), not by editing them.

Note: the frozen C2 real arm ran at rev 6bd57097 (per P-C2 and `evidence/c2-after.txt`), before S212/S213 existed, so it does not list S180/S181 as superseded; that is consistent with the receipt's `superseded=[S069,S182,S193]` and does not bear on these rows.

## 5. Findings

No defects found. All attacked properties hold:

1. S212 copy sha256 == fetched body of the exact v7.2 tag-pinned row URL — PASS.
2. S213 copy sha256 == fetched body of the exact v7.2 tag-pinned row URL — PASS.
3. S212 anchor quotes (17-value line, 512-byte sector, completion-time counting, tick fields) contiguous, 14/12/8/17 words ≤25 — PASS.
4. S213 anchor quotes (cumulative-monotonic fields, reset conditions, field 10, same 17 statistics) contiguous, 10/14/10/7 words ≤25 — PASS.
5. `supersedes S180/S181` form matches CORPUS rule 2; S180/S181 untouched byte-for-byte across the round; S212/S213 are append-only additions — PASS.

Observations (non-defects, recorded for completeness):
- O1: S212 teaches paraphrases the source ("one line of 17 decimal values" for "consists of a single line of text containing 17 decimal values"; "standard 512-byte sector" for "standard UNIX 512-byte sectors"; "grow when an I/O completes" for "The counters are incremented when the I/O completes"; "rise faster than 1000 per second" for "increase at a rate greater than 1000/second"). Each claim maps 1:1 to a contiguous anchored span; no invented content.
- O2: S213 teaches uses British spelling `reinitialisation` where the source has `reinitialization`, and `on counter overflow` for the source's `when the underlying counter overflows` (paraphrase). The same-verified spans use the source's own wording; quote material remains semantically verbatim.
- O3: S213's last clause (`/proc/diskstats and /sys/block/<dev>/stat carry the same 17 statistics`) is grounded at line 22 with the two file names established at lines 5-6 and 16-20; the minimal contiguous span is the line-22 sentence.

## Verification gaps / residual risk

- Single-point fetch: both bodies fetched once each at review time; a network-level cache/ETag artifact cannot be fully excluded, but copy equality with the committed bytes plus the line-anchor matches is strong evidence.
- S180/S181 "untouched" verified across base→tip; their older in-round-35 history was not re-audited here (out of scope).
- Word counts count the minimal contiguous source span per claim; the teaches cell's full prose (including framing) is longer, as is normal for a superseder teaches.

## VERDICT: PASS

No defect found in S212/S213 SOURCES rows, their copies, anchor quotes, supersedes form, or superseded-row state.

Commands observed (all read-only): `git show` at both revs; `curl -fsSL` fetches of the exact row URLs; `sha256sum`; numbered `read` of both fetched bodies; Python row-set diff and quote-contiguity/word-count normalization. No lane file edited; scratch only under `/fast/scratch/hyaku/mori-r36/RevSupS212S213/`. No tool installed (no installs recorded).
