# R48ExecLiveRefetch — live re-fetch of the six entry sources (round 48, w2 falsify)

**Attacked:** freshness of `corpus/knowledge/quota-observability-r48.md` at landed tip
`e4dfff32d4f97c7ef250e9a7538fa75d4f284492` — the six URLs named by its `source:` lines S479–S484 and
the 15 table quotes against the live pages, with a browser User-Agent.

**Verdict: HOLDS.** All six URLs answered **HTTP 200**; five of six live bodies are **byte-identical**
to the committed copies under `corpus/evidence/sources-r48/`, and the sixth (S482, Aliyun) differs in
**38 bytes confined to an A+ tracking beacon token**, with the rest of the normalised text identical.
**All 15 quotes still occur in their live page** under `count-c2.normalise` (15/15 live, 15/15 in the
committed copy). No quote drift, no dead link, no page-identity break. One observation, not a break:
the S482 copy is the only unpinned-in-`freeze-sha256.txt` body that moves between fetches, and it is
already declared as such in the entry's Boundaries.

This is a freshness probe of the cited pages. It does not re-judge C2 (`count-c2.py` is the predicate)
and does not test whether each claim follows from its quote.

## Method and receipts

Seat leaf; no subagent dispatch tool is exposed to this seat, so the single allowed labrat probe was
**not used** and every check below was run directly. No tool was installed or upgraded (nothing
needed; `curl 8.23.0`, `Python 3.14.8`). No `pacman`. All scratch under
`.scratch/r48w2-R48ExecLiveRefetch/`; the only non-scratch file written is this report.

- UA used verbatim for every request:
  `Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36`
- `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecLiveRefetch`
- Fetch wall clock: `2026-10-25T22:36:29Z` … `2026-10-25T22:36:33Z` (`date -u`), one GET per URL, no
  `-L` needed (every response was a direct 200), no `--compressed` (so bytes are comparable to the
  plain-fetch committed copies), `--max-time 90`; per-URL stderr files were empty (`S479.err` … `S484.err`, 0 bytes).
- Fetch command (loop over the six URLs; `code=$(curl -sS -A "$UA" -o "$S/$name" -w '%{http_code}' --max-time 90 "$url" 2>"$S/$sid.err")`), exit 0.
- Live bodies saved to `.scratch/r48w2-R48ExecLiveRefetch/live/{xfs_quota.8.html,quotactl.2.html,errno.h,aliyun-nas-quota.html,arch-mips-errno.h,arch-sparc-errno.h}`.
- Committed copies read with `git -C <lane> show e4dfff32…:corpus/evidence/sources-r48/<name>` (read-only
  git) and hashed with `sha256sum` on the working-tree files; both agreed.

## 1. Six sources: HTTP code and sha256 (live vs committed copy)

| S-id | copy | HTTP | live bytes | live sha256 | committed sha256 | identical |
|---|---|---|---|---|---|---|
| S479 | `xfs_quota.8.html` | 200 | 33702 | `6375e40e9c0e950d78b38edbe9b7e7fdf5868d55be07040d4a029c552c437d5f` | `6375e40e9c0e950d78b38edbe9b7e7fdf5868d55be07040d4a029c552c437d5f` | **yes** |
| S480 | `quotactl.2.html` | 200 | 17114 | `0d4ab273503d078ee0d9765c616b5082514e7d86e2c6a6b16c70cb7fba8b6ee8` | `0d4ab273503d078ee0d9765c616b5082514e7d86e2c6a6b16c70cb7fba8b6ee8` | **yes** |
| S481 | `errno.h` | 200 | 5826 | `66a5ad60566fdd62e41701bcfc42bfeca5e5696ad1d47d78981575e0c51622be` | `66a5ad60566fdd62e41701bcfc42bfeca5e5696ad1d47d78981575e0c51622be` | **yes** |
| S482 | `aliyun-nas-quota.html` | 200 | 117506 | `8bf5dd9e7e6c90829c098d744da0a6cc6b8da34c1084ad2ec0ad0c1a8c8d68cc` | `747fef1bcc8c6d6c18908f4534879922bebdaece1a476831d48be93c4e22719f` | **no** (see §2) |
| S483 | `arch-mips-errno.h` | 200 | 5970 | `006286df7ccd50a0740612ecb1fed94714373770f60c63fa72b262a685f0966a` | `006286df7ccd50a0740612ecb1fed94714373770f60c63fa72b262a685f0966a` | **yes** |
| S484 | `arch-sparc-errno.h` | 200 | 5717 | `530c3cc2c8e69cee8f9e3722c0050b99bf9c798e93f50363e24a186c75f091d6` | `530c3cc2c8e69cee8f9e3722c0050b99bf9c798e93f50363e24a186c75f091d6` | **yes** |

Committed-copy hashes agree with the pins the round froze in two places: the four `count-c2.COPIES`
digests (`evidence/freeze-sha256.txt`) for S479–S482, and the digest printed in each SOURCES row's
scope cell for S483 (`006286df…`) and S484 (`530c3cc2…`). The `sha256sum` run over all six working-tree
copies reproduced those values exactly, so the copies measured here are the frozen ones.

Response headers (second GET, same UA, bodies discarded; `-D -`):

```
S479  HTTP 200  Server: Apache/2.4.58 (Ubuntu)  Last-Modified: Thu, 08 Oct 2026 17:39:35 GMT  ETag: "83a6-65d57b70ec3c0"  Content-Length: 33702  Content-Type: text/html
S480  HTTP 200  Server: Apache/2.4.58 (Ubuntu)  Last-Modified: Thu, 08 Oct 2026 17:39:35 GMT  ETag: "42da-65d57b70ec3c0"  Content-Length: 17114  Content-Type: text/html
S481  HTTP 200  content-type: text/plain; charset=utf-8  etag: "5cd6e5f8…"  x-cache: HIT  content-length: 5826
S482  HTTP 200  server: Tengine/Aserver  content-type: text/html;charset=UTF-8  (no Last-Modified, no Content-Length)
S483  HTTP 200  content-type: text/plain; charset=utf-8  etag: "e4882caf…"  x-cache: HIT  content-length: 5970
S484  HTTP 200  content-type: text/plain; charset=utf-8  etag: "93901754…"  x-cache: HIT  content-length: 5717
```

`Last-Modified` on the two man7 pages (2026-10-08) is older than the 2026-10-25 copies and the live
bytes equal the copies, so no man-page content moved between the freeze fetch and this re-fetch.

## 2. S482 (Aliyun): what actually differs

- Same length (117506 bytes both), different digest.
- 38 differing byte offsets, all inside one contiguous region starting at byte 47002.
- The whole difference is the A+ tracking beacon's per-request `trid`/`asid` values:
  copy `…trid=213e053517929606271031590e14da&asid=AQAAAABzaN5qJ7KcaQAAAABgLWgnOov7Hg==…`
  vs live `…trid=213e018117929677155433151ec829&asid=AQAAAAAjhN5qdp9OZgAAAAD77kvojabFdQ==…`.
- Under `count-c2.normalise` the two texts differ in **one span, chars 10970–11034**, and
  `cn[:10970] == ln[:10970]` and `cn[11035:] == ln[11035:]` are both true — i.e. the entire page
  text outside that beacon token is identical, not merely similar.
- Content counts are equal live vs copy: `Disk quota exceeded` 2/2, `dd: closing output file` 2/2,
  `配额管理` 13/13, `subPath` 5/5. The doubled counts match the entry's Boundaries note that the
  page embeds its body twice (rendered text + JSON).
- Visible-text-only view (script/style blocks removed, then the same normalise): normalised length
  6264, and every S482 quote occurs there at least once — so the three S482 quotes are in the
  rendered page, not only in the embedded JSON payload.

So "Aliyun bytes may differ; the quotes should not" is exactly what was observed: bytes differ only
by a session token, quotes are stable.

## 3. The 15 quotes against the live page

Checker: `.scratch/r48w2-R48ExecLiveRefetch/check_live.py` — imports the frozen
`.ufo/waves/round-48/count-c2.py` via `importlib` and calls **its** `normalise()`, `parse_claims()`,
`split_cells()`, `sources_row()` and `SPAN` (no re-implementation), maps each row's S-id to its URL
through `corpus/SOURCES.md` at `e4dfff32…`, and tests `quote in normalise(live_body)`. Exit 0;
`SUMMARY rows=15 live_located=15 copy_located=15`.

| # | S-id | words | live | copy | live occurrences | quote (abridged) |
|---|---|---|---|---|---|---|
| 1 | S479 | 8 | yes | yes | 1 | `XFS distinguishes between quota accounting and limit enforcement.` |
| 2 | S479 | 14 | yes | yes | 1 | `Quota accounting must be turned on at the time of mounting the XFS filesystem.` |
| 3 | S479 | 13 | yes | yes | 1 | `XFS filesystems perform quota accounting whether the user has quota limits or not.` |
| 4 | S479 | 17 | yes | yes | 1 | `XFS filesystems with limit enforcement turned off can be used as an effective disk usage accounting system` |
| 5 | S479 | 17 | yes | yes | 1 | `limits are never enforced on the superuser (nor are they enforced for group and project ID zero)` |
| 6 | S479 | 25 | yes | yes | 1 | `If a user's usage reaches the hard limit, further requests for space … fail with the "Quota exceeded" (EDQUOT) error.` |
| 7 | S479 | 25 | yes | yes | 1 | `This command can be used even when filesystem quota are not enabled, as it is a full-filesystem scan …` |
| 8 | S480 | 21 | yes | yes | 1 | `can be used to set per-user, per-group, and per- project limits on the amount of disk space used on a filesystem` |
| 9 | S480 | 13 | yes | yes | 1 | `at a time; after this, the soft limit counts as a hard limit` |
| 10 | S480 | 18 | yes | yes | 1 | `No disk quota is found for the indicated user. Quotas have not been turned on for this filesystem.` |
| 11 | S480 | 17 | yes | yes | 1 | `quotactl_fd () instead works on the mount point, which avoids this limitation and is simpler to use` |
| 12 | S481 | 7 | yes | yes | 1 | `#define EDQUOT 122 /* Quota exceeded */` |
| 13 | S482 | 8 | yes | yes | 2 (1 visible-only) | `dd: closing output file '/data/1G.txt': Disk quota exceeded` |
| 14 | S482 | 8 | yes | yes | 2 (1 visible-only) | `CSI 组件支持为通用型 NAS 存储卷的子目录设置配额限制。使用 subPath 方式挂载 NAS 子目录时，可启用目录配额功能…` |
| 15 | S482 | 7 | yes | yes | 4 (2 visible-only) | `然后单击 配额管理 。在 配额管理 页面，单击目录对应的 管理配额 可查看详细信息。` |

Every quote is unique in its page (count 1 for S479/S480/S481; the S482 multi-counts are the same
sentence appearing in both the rendered body and the embedded JSON, plus a repeated breadcrumb/step
phrase for #15 — not a second, different sentence). Quote lengths stay inside the counter's 6–25-word
window (7–25). Live and copy agree on every one of the 15, so the copies are a faithful snapshot of
what the pages say today.

## 4. The entry's own `recheck:` lines, executed literally against the live bodies

| recheck line | expected | observed | exit |
|---|---|---|---|
| `grep -c 'Quota exceeded'` on S479 | 1 | `1` | 0 |
| `grep -c 'No disk quota is found for the indicated user'` on S480 | 1 | `1` | 0 |
| `grep -cE 'EDQUOT[[:space:]]+122'` on S481 | 1 | `1` | 0 |
| `grep -c 'Disk quota exceeded'` on S482 | "1 or more" | `2` | 0 |
| mips/sparc loop, `grep -E 'EDQUOT'` | mips 1133, sparc 69 | `#define EDQUOT 1133 /* Quota exceeded */` / `#define EDQUOT 69 /* Quota exceeded */` | 0 |

Line anchors asserted by the entry and the SOURCES rows are live at the stated lines:

```
$ sed -n '107p' live/errno.h          -> #define EDQUOT  122  /* Quota exceeded */
$ sed -n '131p' live/arch-mips-errno.h -> #define EDQUOT 1133 /* Quota exceeded */
$ sed -n '43p'  live/arch-sparc-errno.h -> #define EDQUOT 69  /* Quota exceeded */
```

## 5. What this establishes, and what it does not

Establishes (observed today, 2026-10-25T22:36Z, browser UA):
- every `source:` URL in the entry resolves 200 and still serves the cited material;
- five copies are byte-identical to live, and the sixth differs only in a beacon token;
- all 15 quotes are present in the live pages under the counter's own normalisation, with the same
  word sequence as in the copies;
- the `recheck:` one-liners in the entry still return their documented values;
- the S483/S484 line/constant anchors still hold on the live raw headers.

Does not establish:
- that any claim cell follows from its quote (that is the reviewer's check, and `count-c2.py` names
  the same limit);
- that the live page is what it was on 2026-10-25 when the copies were made for the two man7 pages —
  inferred only from `Last-Modified: 2026-10-08` plus byte equality, not from a dated archive
  [INFERENCE for the "unchanged since freeze" part];
- anything about this host's filesystem quota state (no quota command was run; the entry's
  read-only boundary is respected);
- the two boundary rows S483/S484 are outside the claims table, so "15 quotes" does not cover them;
  their constants were checked only as line anchors above;
- the RHEL 9 Japanese PDF named by the staged entry — not re-fetched by this seat (the contract
  already records HTTP 403 for a plain and a browser UA on 2026-10-25 and keeps it out of the claim).

**UNVERIFIED:** no archive.today / Wayback comparison was made; no second fetch was made through a
different egress or with `--compressed`; the Aliyun page was not rendered in a browser to confirm
that the visible DOM matches the HTML's rendered text (the visible-only check above is an HTML-text
proxy).

## 6. Observations for the reviewer (not breaks)

1. `count-c2.py` pins only the four URLs in `COPIES`; the S483/S484 copies are pinned only by the
   sha256 written inside their SOURCES rows, and `freeze-sha256.txt` lists neither. Both matched the
   live body today, so nothing is wrong now, but a drift on those two would not be caught by the
   counter — the named limits of P-C2 do not mention it, and this seat reports it as a limit.
2. The S482 body is the one page whose bytes move per request (tracking token). The entry already
   declares this in Boundaries ("the quotes are stable, the file hash is not"), and today's fetch
   confirms the declaration precisely: 38 bytes, one beacon token, everything else identical.
3. No redirect, no rate-limit, no auth challenge was encountered on any of the six URLs; all six
   answered on the first GET.

## 7. Risks and blockers

None blocking. Nothing outside `.scratch/r48w2-R48ExecLiveRefetch/` and this report was written;
no tracked file was passed to an edit tool; no git write, no jj mutation, no pacman.
