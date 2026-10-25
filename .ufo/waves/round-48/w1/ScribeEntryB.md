# ScribeEntryB — independent C2 entry draft and first falsifiers

## Behavior

Independently opened and normalized all four frozen source copies. The embedded Python verification below reports all four expected SHA-256 values matched; it then checked 13 distinct candidate quote spans, each 6–25 whitespace-delimited words and an exact substring of that source's normalized copy. The claims table is the candidate entry spine. Rows use frozen intended IDs S479–S482; the registry rows are not present yet at the frozen lane tip, so C2 eligibility for those IDs remains UNVERIFIED until L1 lands corresponding SOURCES.md rows with the required mined/opened/used-by metadata.

The table deliberately separates explicit quota-off accounting from a zero/empty usage reading; records the documented over-quota write failure and Linux EDQUOT number; notes the full-filesystem scan's potential time cost; and names per-user/per-group/per-project quota scope. No conclusion that an observed zero usage means quotas are disabled is made.

| claim | source | quote |
|---|---|---|
| [INFERENCE] XFS limit enforcement being off is distinct from using its quota subsystem as an accounting mechanism; this is not a zero-usage signal. | S479 | `XFS filesystems with limit enforcement turned off can be used as an effective disk usage accounting system` |
| [INFERENCE] An over-quota write failure is evidence of an enforced limit, not evidence that a quota is disabled. | S479 | `The quota subsystem warns users when they exceed their allotted limit` |
| An editor write can fail in an over-quota situation. | S479 | `a write fails because of an over quota situation` |
| XFS can scan the full filesystem even when quota is not enabled; this scan may take a long time. | S479 | `This command can be used even when filesystem quota are not enabled, as it is a full-filesystem scan` |
| Quota limits can be scoped per user, group, or project on a filesystem. | S480 | `can be used to set per-user, per-group, and per- project limits on the amount of disk space used on a filesystem` |
| Each user or group can have a soft and hard limit for a filesystem. | S480 | `For each user and/or group, a soft limit and a hard limit can be set for each filesystem` |
| When a soft-limit grace period expires, that limit is treated as a hard limit. | S480 | `at a time; after this, the soft limit counts as a hard limit` |
| A quotactl ESRCH condition can mean quotas are not turned on for the filesystem, unlike zero usage. | S480 | `No disk quota is found for the indicated user. Quotas have not been turned on for this filesystem` |
| Linux defines EDQUOT as errno 122, “Quota exceeded”; an implementation should match the symbolic errno rather than parse prose. | S481 | `#define EDQUOT 122 /* Quota exceeded */` |
| A non-quota errno can be distinguished from EDQUOT; this macro is adjacent in the same Linux UAPI header. | S481 | `#define ENOMEDIUM 123 /* No medium found */` |
| The NAS example's failing dd output names a disk-quota error; it is a concrete error-string example, not a universal errno mapping. | S482 | `dd: closing output file '/data/1G.txt': Disk quota exceeded` |
| The vendor example writes a known payload to a mounted directory using dd. | S482 | `kubectl exec -it nas-sts-0 -- dd if=/dev/zero of=/data/20G.txt bs=1M count=20000` |
| The vendor describes directory quota support for a NAS subdirectory mounted by subPath. | S482 | `CSI 组件支持为通用型 NAS 存储卷的子目录设置配额限制。使用 subPath 方式挂载 NAS 子目录时，可启用目录配额功能，限制子目录容量，提升资源利用率。` |

### Boundaries

These sources describe Linux/XFS quota interfaces and one vendor's NAS procedure; they do not establish that every filesystem, kernel, NAS client, mount, or container runtime exposes identical semantics. The quota-off accounting statement is specific to XFS. The quotactl error text is not an instruction to infer state from errno alone without checking the operation and arguments. The vendor's human-readable `Disk quota exceeded` example does not identify the host syscall errno. A scan that may take a long time is not bounded by these sources. The copied documents were frozen and hash-checked; their current upstream state was not revalidated.

[INFERENCE] A future read-only probe should distinguish explicit quota enablement/accounting state from usage values and should avoid turning this note into a quota mutation or full-filesystem scan. The excerpts do not specify a universal, safe probe for zero usage.

### Delivery paths this cannot see

This note cannot see quota state on a particular host, mounted filesystems not represented in a probe's inputs, per-directory NAS control-plane values, write failures not captured by the chosen observation path, or quotas configured after the snapshot. It does not authorize quota changes, test writes, or remediation. A successful read of usage does not prove enforcement is enabled; absence of a quota error does not establish that writes are unconstrained.

## Gates and first falsifiers

- **Observed source-copy gate:** the source-copy hashes and quote-substring/word-count script below passed for the four files.
- **Registry gate:** UNVERIFIED. At frozen `HEAD=4387cf94b69ddce455051a1ff38e93795c2e6cde`, `corpus/SOURCES.md` ends at S478, so S479–S482 registry metadata (including `used-by`) is not yet observable there. This report does not claim C2=met.
- **C2 counter:** UNVERIFIED; the candidate is embedded in this report and was not written to the production entry path or scored as a landed entry.
- **First falsifier:** if an admitted source row's final URL/opened date/status/used-by does not match the cited quote source and this entry path, the row fails P-C2 regardless of quote validity. If the normalized frozen copy lacks any quoted span or a span falls outside 6–25 words, the quoted row fails.

### Reproduction script and observed result

Command: `python3 - <<'PY'` (executed in the Python eval tool; absolute source paths are embedded below). Exit code: 0. Output: `COPY_SHA256 matched=4/4` and `QUOTE_CHECK rows=13 unique=13 located=13 word_range=6-25 PASS`.

```python
import hashlib, html, os, re

root = "/home/vgpnk/Projects/shokunin/mori-shokunin"
src_dir = root + "/corpus/evidence/sources-r48"
expected = {
    "xfs_quota.8.html": "6375e40e9c0e950d78b38edbe9b7e7fdf5868d55be07040d4a029c552c437d5f",
    "quotactl.2.html": "0d4ab273503d078ee0d9765c616b5082514e7d86e2c6a6b16c70cb7fba8b6ee8",
    "errno.h": "66a5ad60566fdd62e41701bcfc42bfeca5e5696ad1d47d78981575e0c51622be",
    "aliyun-nas-quota.html": "747fef1bcc8c6d6c18908f4534879922bebdaece1a476831d48be93c4e22719f",
}
def normalise(text):
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text)

copies = {}
for name, digest in expected.items():
    raw = open(os.path.join(src_dir, name), "rb").read()
    assert hashlib.sha256(raw).hexdigest() == digest, name
    copies[name] = normalise(raw.decode("utf-8", "surrogateescape"))

quotes = [
    ("S479", "xfs_quota.8.html", "XFS filesystems with limit enforcement turned off can be used as an effective disk usage accounting system"),
    ("S479", "xfs_quota.8.html", "The quota subsystem warns users when they exceed their allotted limit"),
    ("S479", "xfs_quota.8.html", "a write fails because of an over quota situation"),
    ("S479", "xfs_quota.8.html", "This command can be used even when filesystem quota are not enabled, as it is a full-filesystem scan"),
    ("S480", "quotactl.2.html", "can be used to set per-user, per-group, and per- project limits on the amount of disk space used on a filesystem"),
    ("S480", "quotactl.2.html", "For each user and/or group, a soft limit and a hard limit can be set for each filesystem"),
    ("S480", "quotactl.2.html", "at a time; after this, the soft limit counts as a hard limit"),
    ("S480", "quotactl.2.html", "No disk quota is found for the indicated user. Quotas have not been turned on for this filesystem"),
    ("S481", "errno.h", "#define EDQUOT 122 /* Quota exceeded */"),
    ("S481", "errno.h", "#define ENOMEDIUM 123 /* No medium found */"),
    ("S482", "aliyun-nas-quota.html", "dd: closing output file '/data/1G.txt': Disk quota exceeded"),
    ("S482", "aliyun-nas-quota.html", "kubectl exec -it nas-sts-0 -- dd if=/dev/zero of=/data/20G.txt bs=1M count=20000"),
    ("S482", "aliyun-nas-quota.html", "CSI 组件支持为通用型 NAS 存储卷的子目录设置配额限制。使用 subPath 方式挂载 NAS 子目录时，可启用目录配额功能，限制子目录容量，提升资源利用率。"),
]
seen = set()
for sid, name, quote in quotes:
    q = re.sub(r"\s+", " ", quote).strip()
    assert 6 <= len(q.split()) <= 25, (sid, quote)
    assert q in copies[name], (sid, name, quote)
    assert q not in seen, (sid, quote)
    seen.add(q)
print(f"COPY_SHA256 matched={len(expected)}/{len(expected)}")
print(f"QUOTE_CHECK rows={len(quotes)} unique={len(seen)} located={len(seen)} word_range=6-25 PASS")
```

## Provenance and touched surfaces

- **Report path:** `.ufo/waves/round-48/w1/ScribeEntryB.md` (this report only).
- **Inputs read:** frozen contract and v3 spec; C2 checker; all four `corpus/evidence/sources-r48/` copies; `corpus/SOURCES.md`; tooling rules at `/home/vgpnk/.omp/agent/RULES.md`.
- **Read-only facts:** source-copy SHA-256 values matched frozen checker pins. `git rev-parse HEAD` returned `4387cf94b69ddce455051a1ff38e93795c2e6cde`; the observed registry tail included S477/S478 and not S479–S482.
- **Scratch only:** `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ScribeEntryB/` contains normalized copies used during quote selection; it is not an entry or candidate tool.
- **No install/update:** none.
- **Out of scope / not done:** no production source, registry, tool, log, scorecard, frozen contract, C1 calibration, host state, fleet repo, or sibling lane was changed; no C2 counter run; no live-source fetch; no quota operation; no commit or jj mutation. Other worktree changes were visible (including `M tools/mori-pin-check.py` and many untracked scratch/report paths); they were treated as user/sibling work and left untouched.
