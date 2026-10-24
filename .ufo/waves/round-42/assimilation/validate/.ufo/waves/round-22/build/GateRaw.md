# GateRaw — `_blob_hits` Unicode / newline / binary semantics parity audit

Seat: MoriR22.GateRaw (read-only scout). Scope: `tools/mori-retention-gate.py` plus the two artifacts it directly references (`.ufo/waves/round-18/frozen/c1-policy.json`, `.ufo/waves/round-18/gate-snapshots/retention/retention.json`). No tests, selftests, builds, or Python probes were executed; nothing below is a measured pass count. Statements tagged [INFERENCE] are from documented CPython / Git behaviour, not observed in this wave.

## Provenance (observed)

| Item | Value |
|---|---|
| Gate file SHA-256 (worktree, clean vs HEAD) | `cf0896a2ea36f169c9e900c58eefe7e2a900a4c9d67f849f753f4631d8ab829e` |
| Lane HEAD at read time | `e825c7fe6ee3ce7fce397c6c4db9c075960beee7` (not the contract's entering `77a5bbe8…`; L1 should rebind) |
| Frozen policy `c1-policy.json` SHA-256 | `db06e9810bbfd243fb0a753a46960573df39083ea90174ce463cf2a0ab523128` |
| Frozen snapshot pin | `55fcdd71…a00e8` (constant `SNAPSHOT_PINS`, not recomputed here) |

## Exact semantics of `_blob_hits` (observed, lines 89–103)

1. **Binary rule:** `if b"\0" in data: return []` over the *whole raw blob*. No 8000-byte window, no `.gitattributes`, no other heuristic.
2. **Decode:** `data.decode("utf-8", errors="replace")` on the whole blob. Plain `utf-8` (a UTF-8 BOM stays as U+FEFF in line 1), not `utf-8-sig`, not `surrogateescape`, not `ignore`.
3. **Line split:** `text.split("\n")`, numbered from 1. It is not `splitlines()`. `\r`, `\x0b`, `\x0c`, `\x1c`–`\x1e`, U+0085, U+2028, and U+2029 all stay inside the line. A trailing `\n` produces a final empty line (line count = number of `\n` + 1). An empty blob is one empty line 1.
4. **Match:** for each line, in policy class order, `expression.search(line)` on a **str** pattern compiled with no flags. This gives Unicode `\s`, `\w`, `\d`, and `\b`, and IGNORECASE folding if a pattern sets it. Each (line, class) pair yields at most one hit, however many matches the line has.
5. **Identity digest:** `sha256(line.encode("utf-8"))`. This hashes the *replaced* text, not the raw line bytes, and excludes the `\n` while keeping any `\r`.
6. **Caller rules (`_scan_git_revision`, lines 177–204):** the tree comes from `ls-tree -r -z --full-tree <commit>`, and only entries with `kind == blob` are scanned. Mode `120000` (symlink target text) and `100755` **are scanned**, while `160000` is skipped. Content comes from raw `cat-file blob <oid>`: no `--filters`, no textconv, no CRLF conversion. Paths are `path_bytes.decode("utf-8", errors="replace")`. Hit order is ls-tree order, then line, then class order.
7. **Snapshot caller (`frozen_run`, line 370):** it uses the same `_blob_hits` with the JSON `path` string as-is, so it has the same content semantics and no path decoding.

## Parity requirements for the independent reconciler

A reimplementation is byte-identical only if it does all of the following:

- Skip the blob when `b"\x00" in raw` anywhere. Using `git grep -I`, `git diff --numstat`, or any first-8000-byte check diverges.
- Decode the whole blob as UTF-8 with Python `errors="replace"`. Splitting the raw bytes on `b"\n"` and then decoding each line separately is equivalent, because 0x0A is never part of a valid multibyte sequence, so it always ends a maximal invalid subpart [INFERENCE].
- Hash `decoded_line.encode("utf-8")`, never the raw line bytes. The two differ for every line containing invalid UTF-8.
- Use `str.split("\n")`, keep `\r`, and keep the trailing empty segment.
- Compile the regex as `re.compile(str_regex)` with no added flags and match with `.search`. A bytes pattern, `re.ASCII`, `re.fullmatch`/`re.match`, or another engine (RE2, Oniguruma, `git grep -P`) diverges.
- Read blobs with `cat-file blob` (or `--batch`) by object ID, and scan symlink blobs. The contract's "committed symlink input is rejected" applies to the receipt, policy, and allowlist *inputs*, not to tree members.
- Decode paths with UTF-8 `errors="replace"`, and only from `-z` output. Non-`-z` output C-quotes non-ASCII paths.
- Compare hits as a multiset (`Counter`), not as an ordered list or a set.

## Findings (risk, not defects in the existing gate)

**F1: Contract conflict between R19 and the gate's real output (high).** The gate can legitimately emit two *identical* hit tuples. Two tree paths whose raw bytes differ only in invalid UTF-8 (for example `p\xff.txt` and `p\xfe.txt`) both decode to `p\ufffd.txt`. If they contain the same matching line, they produce the same `(path, line, class, line_sha256)`. A malformed tree with a duplicate entry does the same. R19 says "duplicate hit reject 2", so a faithful receipt from the gate would be rejected as a setup failure. L1 has to choose one of two approaches:
- Accept a receipt duplicate when the independent recomputation has the same multiplicity, and treat any other multiplicity difference as exit 1 (mismatch).
- Keep exit 2, but under a distinct, documented error code such as `duplicate_hit_identity`, and state that it is a known-unrepresentable population.

**F2: The identity is not injective on raw bytes (medium).** Different raw lines produce the same `line_sha256` whenever they differ only in invalid bytes (`R22EDGE\xff` and `R22EDGE\xfe` both become `R22EDGE\ufffd`). The allowlist key `(path, class, line_sha256)` has no line number (lines 235, 261), so one allowlist row allows:
- every identical line in that path, and
- every lossy-equivalent line in that path.

The reconciler's allowlist partition has to use the same line-free key to match the gate. A raw-byte digest would split these hits apart and report false mismatches.

**F3: Path equality is evaluated after lossy decoding (low to medium).** `must_redact_paths`, `non_author_paths_glob` (via `fnmatch`), and the round-22 "exactly the supplied policy path" exclusion all compare against the replaced path string. Any non-UTF-8 tree path that decodes to the same string as the policy path would also be excluded. The reconciler should reject a `--policy` path containing U+FFFD. Alternatively, it can match the excluded path on raw `ls-tree` bytes and report any collision as a setup error.

**F4: The NUL rule is a coverage hole that parity faithfully reproduces (informational).** Skipped content includes:
- any UTF-16 or UTF-32 text (these always contain NUL for ASCII characters), and
- any text blob with a single stray NUL anywhere, even past byte 8000.

These blobs add 0 to the raw denominator. Agreement on this point is not evidence of absence and does not justify `privacy_clearance`. The existing selftest covers only the basic NUL skip (`binary-skip` arm, line 536). Nothing in it covers CRLF, invalid UTF-8, Unicode separators, a BOM, an empty blob, a non-UTF-8 path, or a symlink blob.

**F5: Unicode regex classes in the real frozen policy (medium, parity-relevant).** The frozen policy's regex constructs are summarized here; no regex text is reproduced.
- R2 and R4 use `\s`. Under str patterns, `\s` also matches NBSP U+00A0, U+0085, U+2028, and `\x1c`–`\x1f`. A bytes or ASCII engine treats `C2 A0` as non-space, so the same line gives a different hit or miss.
- R3, R8, and R9 use `\b`. Under str patterns, a neighbouring accented letter (for example `é`) is a word character, so there is no boundary. An ASCII engine sees a boundary, which flips the result.
- No class uses `$` or inline flags, so the CRLF `$`-anchor trap (`X$` does not match `X\r`) is theoretical for the frozen policy. It is still live for any future policy.
- CRLF always changes the digest (`\r` is hashed).

**F6: Replacement count is decoder-specific (medium if anyone ports the code).** CPython's maximal-subpart replacement turns `\xf0\x80\x80` into three U+FFFD, `\xed\xa0\x80` (a surrogate) into three, `\xc0\x80` (overlong) into two, and a truncated `\xe2\x82` at EOF into one [INFERENCE]. Rust `from_utf8_lossy` and WHATWG `TextDecoder` follow the same Unicode recommendation [INFERENCE]. Run-collapsing replacement such as Go's `bytes.ToValidUTF8`, and `errors="ignore"`, produce different digests. The reconciler should stay in CPython and use the same call.

## Edge fixture (specification and generator, NOT executed)

This is a synthetic marker policy; the frozen policy and its classes are not used. Expected digests are given as formulas, so the generator computes them instead of quoting values that were never measured here. Fixture Git repositories may only be created by writer executors in their own `.scratch/round22/<seat>/` clone directories.

Policy (`mori-retention-policy-v1`):

| id | regex (JSON-unescaped) | probes |
|---|---|---|
| `E` | `R22EDGE` | plain search |
| `D` | `R22EOL$` | `$` versus `\r` |
| `Z` | `\A\Z` | empty line, trailing-newline segment, empty blob |
| `S` | `R22[^\s]+SP` | Unicode `\s` (NBSP) |
| `B` | `\bR22WB` | Unicode `\b` |
| `K` | `(?i)r22f[a-z]` | documented IGNORECASE non-ASCII folds (U+212A Kelvin sign, U+017F long s); the `f` keeps it off every other member |

The policy has `must_redact_paths: []` and `non_author_paths_glob: []`.

Tree members (raw bytes) and expected gate hits as `(path, line, class, sha256 input bytes)`:

| # | path (bytes) | mode | content (Python bytes literal) | expected hits |
|---|---|---|---|---|
| 1 | `edge/crlf.txt` | 100644 | `b"R22EDGE\r\nR22EOL\r\nR22EOL\n"` | (1,E,`b"R22EDGE\r"`), (3,D,`b"R22EOL"`), (4,Z,`b""`). Line 2 has no D hit. |
| 2 | `edge/invalid.txt` | 100644 | `b"R22EDGE\xff\nR22EDGE\xfe\n"` | (1,E,`b"R22EDGE\xef\xbf\xbd"`), (2,E,same bytes), (3,Z,`b""`). This is the F2 collision. |
| 3 | `edge/repl-count.txt` | 100644 | `b"R22EDGE\xf0\x80\x80"` | (1,E,`b"R22EDGE" + b"\xef\xbf\xbd"*3`). No trailing newline, so no Z hit. |
| 4 | `edge/nul-late.txt` | 100644 | `b"R22EDGE\n" + b"A"*9000 + b"\x00"` | none (whole-blob NUL skip; Git's 8000-byte heuristic would call it text) |
| 5 | `edge/utf16.txt` | 100644 | `"R22EDGE\n".encode("utf-16")` | none (NUL bytes) |
| 6 | `edge/separators.txt` | 100644 | `"R22EDGE\u2028x\x85y\x0cR22EOL\n".encode("utf-8")` | (1,E,whole line 1 UTF-8), (1,D,same), (2,Z,`b""`). `splitlines()` would yield four lines. |
| 7 | `edge/bom.txt` | 100644 | `b"\xef\xbb\xbfR22EOL"` | (1,D,`b"\xef\xbb\xbfR22EOL"`). Decoding with `utf-8-sig` would change the digest. |
| 8 | `edge/empty.txt` | 100644 | `b""` | (1,Z,`b""`), digest `e3b0c442…b855` |
| 9 | `edge/nbsp.txt` | 100644 | `"R22a\u00a0bSP\nR22abSP".encode("utf-8")` | (2,S,`b"R22abSP"`). Line 1 has no S hit under str `\s` but would hit in a bytes/ASCII engine. |
| 10 | `edge/wordb.txt` | 100644 | `"éR22WB\n-R22WB".encode("utf-8")` | (2,B,`b"-R22WB"`). Line 1 has no B hit under Unicode `\b` but would hit in an ASCII engine. |
| 11 | `edge/fold.txt` | 100644 | `"R22F\u212a\nR22F\u017f".encode("utf-8")` | (1,K,UTF-8 of line 1), (2,K,UTF-8 of line 2), per the documented CPython IGNORECASE rule |
| 12 | `edge/link` | 120000 | blob `b"R22EDGE-target"` | (1,E,`b"R22EDGE-target"`). Symlink blobs are scanned. |
| 13 | `edge/p\xff.txt` | 100644 | `b"R22EDGE"` | (1,E,`b"R22EDGE"`) at path `edge/p\ufffd.txt` |
| 14 | `edge/p\xfe.txt` | 100644 | `b"R22EDGE"` | an **identical** tuple to #13. This is the F1 R19 conflict. |

Expected gate totals, derived by hand and not measured: `hits` = 3+3+1+0+0+3+1+1+1+1+2+1+1+1 = **19**. This includes one fully duplicated tuple (#13/#14) and one same-path same-digest pair (#2). Allowlist sub-arm: one row `(edge/invalid.txt, E, sha256(b"R22EDGE\xef\xbf\xbd"))` must move **both** #2 E hits to allowlisted. Expected `metric` is 19 without that row and 17 with it.

Arms to derive:
- **G1:** the gate on this tree and the reconciler on the same tree agree as a multiset (R01/R04 shape).
- **G2:** flip the reconciler to a raw-byte digest, `splitlines`, a bytes regex, an 8000-byte NUL window, `utf-8-sig`, or symlink exclusion. Each change must produce exit 1 against a genuine receipt (mutation seeds for MutantPlan).
- **G3:** the #13/#14 receipt exercises the F1 decision.
- **G4:** for R22, a NUL blob that contains markers contributes 0.

Fixture-building notes:
- Members #12–#14 cannot come from `write_bytes` + `git add` portably. Build the tree with `git hash-object -w --stdin` per blob, then `git mktree -z` with raw path bytes, then `git commit-tree`. `_run_git_fixture` (lines 398–418) only covers regular files.
- Run with `GIT_CONFIG_GLOBAL=/dev/null` and `GIT_CONFIG_NOSYSTEM=1`, as the gate selftest does, so `core.autocrlf` cannot rewrite #1.

Generator sketch (for a writer seat; not run here):

```python
import hashlib
E = lambda b: hashlib.sha256(b).hexdigest()
FFFD = "\ufffd".encode("utf-8")
expected = [
    ("edge/crlf.txt", 1, "E", E(b"R22EDGE\r")), ("edge/crlf.txt", 3, "D", E(b"R22EOL")), ("edge/crlf.txt", 4, "Z", E(b"")),
    ("edge/invalid.txt", 1, "E", E(b"R22EDGE" + FFFD)), ("edge/invalid.txt", 2, "E", E(b"R22EDGE" + FFFD)), ("edge/invalid.txt", 3, "Z", E(b"")),
    ("edge/repl-count.txt", 1, "E", E(b"R22EDGE" + FFFD * 3)),
    ("edge/separators.txt", 1, "E", E("R22EDGE\u2028x\x85y\x0cR22EOL".encode())),
    ("edge/separators.txt", 1, "D", E("R22EDGE\u2028x\x85y\x0cR22EOL".encode())),
    ("edge/separators.txt", 2, "Z", E(b"")),
    ("edge/bom.txt", 1, "D", E(b"\xef\xbb\xbfR22EOL")),
    ("edge/empty.txt", 1, "Z", E(b"")),
    ("edge/nbsp.txt", 2, "S", E(b"R22abSP")),
    ("edge/wordb.txt", 2, "B", E(b"-R22WB")),
    ("edge/fold.txt", 1, "K", E("R22F\u212a".encode())), ("edge/fold.txt", 2, "K", E("R22F\u017f".encode())),
    ("edge/link", 1, "E", E(b"R22EDGE-target")),
    ("edge/p\ufffd.txt", 1, "E", E(b"R22EDGE")), ("edge/p\ufffd.txt", 1, "E", E(b"R22EDGE")),
]
assert len(expected) == 19
```

## Remaining unknowns

- Every [INFERENCE] item (CPython replacement counts, IGNORECASE folds, Git's 8000-byte heuristic, Git tree ordering) needs to be confirmed by L1's post-integration run of the fixture. None of it was executed in this seat.
- Whether the r21 measured tree actually contains non-UTF-8 paths, NUL blobs that carry markers, CRLF lines, or NBSP/accented neighbours was not checked. That requires a tree scan, which is outside this seat's bounds.
- The F1 resolution (multiplicity-aware acceptance versus a distinct setup code) is an L1 design decision.

No tools were installed or updated.
