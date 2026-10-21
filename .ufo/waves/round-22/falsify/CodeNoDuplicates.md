# CodeNoDuplicates — round-22 falsification (static)

**Scope:** `no_duplicates` (`tools/mori-retention-reconcile.py:36-41`) and its direct call contracts: `parse` (:43-47), its call sites in `check` (:161, :171, :172, :190), and the exception mapping that carries hook/parse errors to exit codes (:277-283).

**Method:** static reads only. No executions, builds, tests, linters, installs, edits, delegation, or git mutation. Shipping source read in full. Stdlib read from `/usr/lib/python3.14/json/` (`__init__.py` 248-275, 339-352; `decoder.py` 70-127, 137-219, 351-364; `scanner.py` 5-7, 73). Frozen wording from `contract.md:11,13,15,19` and `denominator-correction.md:7`. No committed receipt, policy, allowlist, or matched text was opened.

## Summary

- `no_duplicates` (:36-41): no defect. Bounded no-finding N1.
- `parse` (:43-47): two findings.
  - L1: admits lone surrogate code points, producing identities that can never match git paths or scanned text. One silent fail-open chain.
  - L2: `MemoryError` escapes to exit 1, which collides with MISMATCH.
- Call sites (:161, :171, :172, :190): no bypass; each result is type-gated. N2.
- Out-of-lane, incidental, not audited: O1 (`raw_unallowlisted` undercount), O2 (plaintext excluded identities).

## L1 — `parse` admits lone surrogates; identities built from them cannot match (low to medium; silent)

Sites:
- :45 `json.loads(data, …)` receives raw blob bytes. Stdlib `loads` decodes with `s.decode(detect_encoding(s), 'surrogatepass')` (`__init__.py:347`), so encoded surrogates are accepted.
- Escapes such as `\ud800` yield unpaired code points (`decoder.py:120-125`; `chr(uni)` at :125).
- Contrast: git paths decode `strict` (:79); scanned text decodes `errors='replace'` (:149). Neither can produce U+D800-U+DFFF. Any parsed identity string containing a surrogate therefore never equals a path or scanned line.

Consumers that accept such strings silently:
- `must` set: `policy_rules` :102-105 accepts any non-empty str. Used at :205 (`row['path'] in must`) and :213 (`routed`).
- Class regex: `re.compile` at :99 accepts surrogate-bearing patterns. `expression.search` at :151 never matches text from :149.

Counterexample L1-a (inert class; JSON escape only, no surrogatepass needed): a `classes` entry with `"regex":"\ud800"` passes :99 and contributes zero hits on every scan.

Counterexample L1-b (fail-open chain, traced):
- Policy `must_redact_paths` entry written as CESU-8 bytes `dir/\xed\xa0\xbd\xed\xb8\x80.txt` (encodes U+1F600). `parse` yields `'dir/\ud83d\ude00.txt'`.
- Tracked file `dir/😀.txt` (valid UTF-8) has a class hit. An allowlist row exists for that same path with the matching `(class, line_sha256)`.
- :205 `'dir/😀.txt' in must` is False. :206 marks it allowed. `unallowed=[]`. :214 `retention_code=0`. :215 `RETENTION_CLEAN`. :233 exit 0 when the receipt agrees.
- Intended semantics (entry spelled as valid UTF-8): :205 True, forbidden, exit 1.
- Silent only if the producer's receipt encodes the same decode. A producer with a strict decode yields exit 1 MISMATCH. The reconciler uses the same stdlib decode, so shared misdecoding is not detectable by design.

Counterexample L1-c (identity aliasing; no current effect): object `{"😀"(F0 9F 98 80): 1, "<ED A0 BD ED B8 80>": 2}` yields two distinct keys and no `duplicate_json_key`. No consumed key is non-ASCII (N1), so no current consumer is affected.

Contract basis: `contract.md:13` (required field/type/schema inconsistencies fail closed); `contract.md:19` R17 (malformed JSON returns 2). The frozen text does not state an encoding rule; the defect is that `parse` admits identity-bearing strings that are unmatchable by construction. Background: RFC 8259 §8.1 requires UTF-8 for exchanged JSON (cited from spec knowledge, not fetched).

Fix locus (not implemented): :45 (strict UTF-8 decode and/or reject surrogate code points after parse), or :99 and :102-104.

Trigger: requires a committed policy containing surrogate-encoded bytes or lone `\uD8xx`-style escapes. The committed policy was not opened (lane bounds).

## L2 — `MemoryError` escapes `parse` and `main`, exit 1 (low)

- :46 catches `(ValueError,UnicodeError,RecursionError)`. :279 catches `(OSError,UnicodeError,ValueError,TypeError,KeyError,RecursionError)`. `MemoryError` is in neither.
- Counterexample: a committed receipt, policy, or allowlist blob whose `json.loads` exhausts memory (for example, a flat array of tens of millions of elements under an address-space limit). The exception escapes `main`; :281 never prints; :283 `raise SystemExit(main())` does not catch it. The interpreter exits 1 with a traceback.
- Exit 1 is RETENTION_RECONCILIATION_MISMATCH (`contract.md:15`). The contract requires exit 2 with a sanitized code for unreadable input (`contract.md:15`).
- Inconsistent with the RecursionError handling on the same clause (:46).
- Reachability: allocation failure only, so low likelihood. [INFERENCE] CPython raises MemoryError on allocation failure.

## N1 — `no_duplicates` (:36-41): no defect

- Hook contract: stdlib calls the hook with the ordered pair list for each closed object (`decoder.py:140-141, 156-157, 213-214`). No `try` wraps the hook. The only narrow excepts in the path are IndexError, StopIteration, ValueError, and KeyError (`decoder.py` :65, :106, :113, :183, :188, :196, :235, :254, :362). `Invalid` therefore propagates unchanged.
- Runtime path: `_json.cpython-314-x86_64-linux-gnu.so` is present in `lib-dynload`, so the C scanner is used (`scanner.py:5-7, 73`). Its C source is not on disk. C-path propagation is [INFERENCE] from the pure-Python reference.
- Scope: every closed object is hooked. `obj` is per call (:37), so duplicate detection is per object. The same key in sibling objects is legal and allowed.
- Identity: `key not in obj` (:39) is code-point equality on decoded keys. Escaped and literal forms collide correctly (`"\u0073chema"` vs `"schema"`). The only bypass is surrogate aliasing (L1-c). Every key `check` consumes is an ASCII literal: policy `schema, classes, id, regex, must_redact_paths, non_author_paths_glob` (:92-104); allowlist `rows, path, class, line_sha256, reason, rule` (:108-112); wrapper and receipt names (:162-193); hit `path, line, class, line_sha256` (`HIT_FIELDS`, :22). Bounded: no consumed-field bypass.
- Error: `Invalid` (:24) is not a `ValueError`, so :46 does not remap it. :277 emits fixed `duplicate_json_key`, exit 2. No key text is echoed.
- `require` (:27-28) raises explicitly, not via `assert`, so it survives `python -O`.
- Cost: one dict per object, O(1) per key. Each document is decoded once (:161, :171, :172, :190). Not material.

## N2 — direct call contract of `parse` at call sites

- The only validating decode in the file is :45. Other `json.` uses are :249-256 and :281 (`json.dumps` for fixtures and output), and :263 (selftest `json.loads` of the tool's own output). `json.dumps` cannot emit duplicate keys, and :263 is not a validation path. Verified by enumerating every `json.` match.
- Gates after each call: :162 `isinstance(wrapper, dict)`; :92 policy dict gate; :108-109 `allow_rows` dict-then-list gate; :190 `isinstance(receipt, dict)`.
- Parsed bytes are input-revision blobs. Policy and allowlist equality at the measured revision is byte-compared (:169-170) before any parsed result is used.
- No JSON read in `check` bypasses `parse`.

## Out-of-lane (incidental; not audited; not in the lane verdict)

- O1: :212 builds `unallowed` from `scanner` (:210, non-author removed). :227 emits `'raw_unallowlisted': len(unallowed)`. Counterexample: one raw hit in a non-author path that is not allowlisted gives `scanner=[]`, so `raw_unallowlisted=0`, while the raw population has one unallowlisted hit. `contract.md:13` lists `raw_unallowlisted` as a distinct field; `denominator-correction.md:7` forbids inferring it by subtraction. Expected: computed over `hits` minus `allowed_keys`.
- O2: :233 emits `policy_excluded_hits`, `raw_hits`, and `scanner_hits` with plaintext `path`. `contract.md:13` says "digest-only identities" for policy-excluded hits. If that clause survived the correction, any non-author hit prints its repo path. Not matched text.

## Verification gaps

- No runtime execution (wave rule). Every counterexample is a static trace. L1 must confirm post-integration if runtime evidence is wanted.
- The selftest (:260-261) has four arms: base, mismatch, `../` path, unknown flag. None reaches `no_duplicates`, `duplicate_json_key`, surrogate input, or MemoryError.
- Committed policy, allowlist, and receipt bytes were not opened. Whether L1 applies to the real policy is unknown.
- Stdlib read is Python 3.14. Other interpreter versions were not checked.

## Tooling

No installs or updates performed.

Report: .ufo/waves/round-22/falsify/CodeNoDuplicates.md
