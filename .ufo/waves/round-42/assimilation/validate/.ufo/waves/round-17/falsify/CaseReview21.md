# C1 case review — round 17

## Axes and scope

Attacked only `symlinks_never_followed` / `SymlinkIgnore` and `credential_pin_trap_skipped` / `CredentialPinTrap`: symlink traversal, credential-record data minimization, independent expected values, output assertions, and false-green/setup paths. No tool, gate, or selftest was run. The only executed command was the requested read-only manifest count below.

No `lsp` device is mounted: attempting `read xd://lsp` returned `No such tool: xd://lsp`. Therefore no status/references/definition/diagnostics calls were available. Literal grep was used only to locate symbols; findings below are from source reads and retained receipts, not grep as semantic proof.

## Findings

### High — `credential_pin_trap_skipped` does not uphold or verify “skipped unread”

Contract `contract.md:45-46` says non-`message` records, explicitly including `credential_pin`, are skipped unread. The tool instead runs `json.loads(...)` on every line at `tools/mori-seat-terminal.py:354-365` before `_message_view` rejects non-message records at `:207-213`; thus the whole record object and its values are parsed before the type check. The regression gate repeats this pattern: `collect_canaries` reads the file bytes and strict-parses every line before the `type == "message"` filter (`tools/mori-round17-seat-regressions.py:1173-1185`), despite its “skipped unread” claim at `:1146-1153`.

The case’s want at `fixtures/seat/expected.json:1123-1144` asserts only rc, finding, class totals, and the `credential-trap` class. The comparator grades class/totals, not expected values for the other allowed seat fields (`tools/mori-round17-seat-regressions.py:1215-1260`; scalar type-only validation at `:1053-1069`). Its leak-canary scan considers only message records (`:1146-1204`), and its output check is only for canaries collected there (`:1460-1465`). Consequently the retained green result proves correct terminal classification and no observed echoed message canary, but cannot prove the credential record was unread or that its values could not leak through an allowed scalar field. No leak was observed in the retained output; the failure is the explicit no-read contract and a privacy assertion blind spot, not a claim of observed exfiltration.

### Medium — `symlinks_never_followed` misses directory/root symlink traversal; root symlink is followed

The file-symlink negative control is real: `SymlinkIgnore/Link.jsonl` links to `trap.txt`, a valid old error transcript, while the want at `expected.json:1098-1119` permits only the independent regular `real` completion. The retained output scans one file and returns that one completion. However, `linked-dir` links to `real-dir`, whose only listed target is `real-dir/notes.txt:1` (not a `*.jsonl` file), so following that directory link adds no observable seat. The case therefore does not reject a descendant-directory-only traversal regression.

More importantly, the production scanner does not reject a symlink at the `--sessions-dir` root: `tools/mori-seat-terminal.py:416-421` calls `os.path.isdir` and passes that root directly to `os.walk`; there is no `lstat` check for the root. `followlinks=False` protects descended directory links, not the supplied top path. **[INFERENCE]** A symlink supplied as the root is followed and scanned. This case cannot exercise it: its args contain only `--now-ms` (`expected.json:1100-1103`), and the gate creates/uses a real per-case sandbox as `sessions_dir` (`tools/mori-round17-seat-regressions.py:1715-1721`; pack symlinks are rejected at `:615-619`). Thus the exact case passes while the broad contract “never follow symlinks” is not met for a symlink root.

## Case values and retained L1 evidence

- The independent real-file control in `SymlinkIgnore/real.jsonl:1-2` is a version-3 session with one completed message. `Link.jsonl` resolves to `trap.txt`; the trap is a terminal error, so following that file link would add an unexpected seat/dead total. The directory-link target has no `.jsonl`, as above.
- The credential case’s want is non-vacuous: one named completed seat and all eight totals explicitly pinned, not an empty-directory or setup expectation (`expected.json:1123-1144`). Its terminal classification is supported by the message-only selection branch (`mori-seat-terminal.py:207-213,354-365`); however, the separate unread guarantee is not.
- `PINNED_INPUTS.json:13` pins `expected.json` as `b684c63bf3cebe70f24d3d02f3f0df4f63aad3f547a365a3ca1864f5f57cb01f`, matching the read-only `sha256sum`. Both retained L1 manifests report the same expected digest, 81 declared pins verified, no missing/extra/mismatched pins, and `inputs_changed: []`.
- Before: both requested manifest entries are `capability_absent`, `observed: null`; they are not counted as green. After: both are `match`, `ok: true`, `reasons: []`, each with `rc: 0`, `MORI_SEAT_TERMINAL_OK`, `files_scanned: 1`, `seat_count: 1`, `now_ms: 1761000000000`, `completed: 1`, and all other class totals zero. Pack hashes are unchanged before/after and stderr is empty. The retained stdout digests are present for both cases in `evidence/seat-after/run-manifest.json`; per-case stdout is retained under `evidence/seat-after/runs/`.

Read-only count command (rc 0):

```sh
jq -s '[ .[] | [ .cases[] | select(.id == "symlinks_never_followed" or .id == "credential_pin_trap_skipped") ] | {selected: length, statuses: map(.status)} ]' \
  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-before/run-manifest.json \
  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-after/run-manifest.json
```

Output:

```json
[
  {"selected": 2, "statuses": ["capability_absent", "capability_absent"]},
  {"selected": 2, "statuses": ["match", "match"]}
]
```

`readlink` metadata command (rc 0) reported `Link.jsonl -> trap.txt`, `Dangling.jsonl -> missing-target.txt`, and `linked-dir -> real-dir`.

## Residual risk and verification gaps

The `.jsonl` line-range read intended to return only the header of `CredentialPinTrap/credential-trap.jsonl` returned more than the requested line; no protected record contents are reproduced here. The review relies on source, fixture pins, expected values, and retained L1 output for that case. This was a static review only; no selftest or gate rerun was performed. No tool was installed or updated.