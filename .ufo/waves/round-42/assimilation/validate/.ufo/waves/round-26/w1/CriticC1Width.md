# CriticC1Width — round 26 wave 1, attack on C1 (freshness)

Seat: MoriR26.CriticC1Width (critic, leaf). Date 2026-10-22. Read-only in the lane; the only lane
write is this file. Sandbox: `/fast/scratch/hyaku/mori-r26/CriticC1Width/sb` (a `git clone
--no-hardlinks` of the lane; variant commits exist only there). No tool installed or upgraded. No
upstream source opened (every claim below is a lane path, a sibling path or a command), so no
URL, sha256 or quote rows. No journal `MESSAGE` text read or copied.

## Verdict

C1 is a fixable defect, not a tradeoff the judge must reject. The counter is both too loose and
too strict for the statement:

- Too loose: it reaches `stale_present=0, r26_entry=present` without any correction (paraphrase
  plus an uncited stub), and `stale_present=0` with the stale text moved, wrapped or emphasised,
  from the wrong working directory, or on a bad revision.
- Too strict: an honest, fully dated rewrite that keeps the 2026-10-19 command and its output, and
  a true README statement about systemd-oomd, keep `stale_present=2`.
- Narrower than the stale set: three more stale earlyoom statements in the r12 entry are outside
  the frozen list. A rewrite that clears only the four phrases leaves them standing.

The smallest safe correction needs no change to the frozen list. Run the counter safely, give the
writer seat two wording rules, and have closure re-derive predicates P1 to P6 (below) from text
the statement already contains.

## Counterexamples (sandbox, each a commit on a 248408f5 base; commands re-run 2026-10-22)

`count.sh` is the contract counting command with only the repository path made a parameter. It
reads the frozen phrase bytes, sha256 `c072b20a…63a55f6`, which equal blob `02b7ed18` at
`28b0494`. `c1-closure.sh` is the draft below. Both scripts live in the sandbox directory above.

| Variant | What it does | Contract counter | Closure draft |
|---|---|---|---|
| `248408f5` | entering tip | `stale_present=4 r26_entry=absent` | FAIL |
| `v-paraphrase` 7524bcf | stale meaning kept: "are not active", ASCII `->`, "Neither service unit is active", "not running on this host"; stub r26 with `source: S999`, `verified-at: never` | **`stale_present=0 r26_entry=present`** | FAIL (P3, P4, P5, P6) |
| `v-emphasis-wrap` 3b97333 | same words; F1 broken across a line, F2 and F3 wrapped in `**` or `*`, F4 with a double space | **`stale_present=0`** | FAIL (P1 folded = 4) |
| `v-move-delete` 9957bf8 | r12 file renamed byte-for-byte to `userspace-oom-killers-host-r12.md`; README row 34 dropped | **`stale_present=0`** | FAIL (P1 target gone, P2 moved phrase) |
| `v-narrow` 5c5cffe | the four phrases correctly rewritten as dated past tense, nothing else changed | **`stale_present=0`** | FAIL (P3: three residuals) |
| `v-truthful` 795b6c5 | correct rewrite: F2 kept verbatim inside a dated record; README says "systemd-oomd inactive on this host, earlyoom active since 2026-10-22" | **`stale_present=2`** (false negative) | FAIL (P1 = 2; same rule as the contract) |
| `v-good` 2a19556 | v-narrow plus the residuals reworded, an r26 index row, a new mined `S114` row, and an r26 entry holding the provenance trio and the live readings | `stale_present=0 r26_entry=present` | **PASS**, exit 0 |

Contract-command failure modes outside the sandbox (run against the real lane):

- Wrong working directory. From `/tmp`, under both `bash` and `sh`, the relative redirect
  `< .ufo/waves/round-26/c1-phrases.txt` fails. The loop body never runs and the command prints
  `stale_present=0` at **248408f5** with exit 0. Only the `r26_entry=absent` line betrays it. The
  `git -C` path is absolute but the phrase-file path is relative, so the anchoring is mixed.
- Bad revision. `R=deadbeef` makes `git grep -q` exit 128. The `&&` treats that as "absent", so
  the command prints `stale_present=0`.
- Working-tree input. The loop reads the phrase file from the working tree, not from the frozen
  blob at `28b0494`. Editing that file, or saving it without a final newline (which silently drops
  F4 from `while read`), changes the count. The receipt `evidence/c1-before.txt:2` records
  neither the working directory nor the phrase-file hash.
- The command's exit code is always the exit code of `echo`, so a pass can only be read from
  stdout.

## Does `git grep -F` behave as assumed for F2? Yes.

At 248408f5, every phrase matches exactly one line: F1 at r12:6, F2 at r12:14, F3 at r12:18 and
F4 at `corpus/README.md:34` (all rc=0). The F2 bytes read from the file are
`…2e7365727669636560 20 e28692 20 60696e61637469766560`, so the arrow is UTF-8 `e2 86 92`.
`git grep -F` matches it as bytes: with `LC_ALL=C`, `POSIX` and `C.UTF-8` the count is 4 each,
and `-P` or `-c grep.patternType=perl` also give 1. The backticks are safe because the pattern
reaches git through the variable `"$p"`, so the shell performs no command substitution. git
2.56.0, locale en_US.UTF-8. Two residual hazards remain. Pasting F2 literally inside double
quotes would run the backticks as a command. A phrase that starts with `-` would be read as an
option, so the closure draft passes `-e`. F2 is also defeated by any arrow variant (`->`, `⟶`):
the counter is byte-exact, while QUALITY 77 requires whitespace folding and emphasis removal
(`corpus/QUALITY.md:349-354` at 248408f5).

## Is the statement wider than its counter? Yes, on five points.

Statement: `contract.md:21-24`. Counter: `contract.md:35-38`.

1. "contradict the committed round-26 capture". At `28b0494`, `evidence/` holds only
   `c1-before.txt`, `c2-before.txt` and `retention-scan-base.txt` (directory listing), so no host
   capture is committed. The counter never reads a capture.
2. "none of the four phrases remains". The counter is scoped per file, so moving the text escapes
   it (v-move-delete), and it is per line and byte-exact, so wrapping escapes it (v-emphasis-wrap).
3. "a superseding entry … whose `source:` line cites at least one SOURCES row opened in round 26".
   The counter runs only `cat-file -e`, and the `S999` stub passes. "Opened in round 26" cannot
   be read from the `opened` column: at 248408f5, 24 of 113 rows already carry `2026-10-22`
   (histogram: 34/14/41/24 for 10-19/10-20/10-21/10-22). It needs an id set difference against
   248408f5, whose highest id is `S113`.
4. "rewritten as dated past-tense records that name the superseding entry; not shadowed by a
   banner" (`contract.md:42-44`). Nothing checks this, and deletion passes.
5. "four … present-tense statements that … killers are inactive". F2 is a command and its output,
   which has no tense, and F4 is a fragment of a table cell. F1, F3 and F4 say "both", but only
   the earlyoom half is stale: `systemctl is-active systemd-oomd.service` still prints `inactive`
   and `is-enabled` prints `disabled` (live, 2026-10-22). That half-truth is why v-truthful fails.

The counter is also narrower than the stale set. At 248408f5 the r12 entry has three more stale
earlyoom statements outside the list. All three are still present at v-narrow:

- r12:3, the `recheck:` expected output `… 1; 2; inactive; inactive; 0; 0`. Re-run live, the two
  `systemctl` reads print `inactive` and **`active`**. A re-verification recipe that now fails is
  exactly what the freshness axis exists to catch.
- r12:14, `` `systemctl is-enabled earlyoom.service` → `not-found` ``. Live, it prints `enabled`.
- r12:18, "earlyoom's service unit is not found". Live, `LoadState=loaded`.

Sibling files that point at the superseded entry (reference drift, not stale text):
`PROVINCE.md:53` and `corpus/README.md:341` cite `userspace-oom-killers-r12.md:10-15` as the
first FR10 evidence, and `SKILL.md:30` cites r12. Each rule ("an inactive killer is
`unavailable (inactive)`") is still true, but every pointer should name r26 once r12 is
superseded. That is PROTOCOL's sweep of `corpus/README.md`, `SKILL.md` and `knowledge/`
(`/home/vgpnk/Projects/shokunin/PROTOCOL.md:363-364`). Dated records stay as they are:
`evidence/drift-r12-20261019T2204Z-classification.md:53-54`, `lessons/round-12.md:105` and
`LOG.md:685`.

## Can the counter reach 0 without the knowledge being corrected? Yes, three ways.

- Deleting: covered by v-move-delete; deleting the file outright behaves the same.
- Paraphrasing: v-paraphrase.
- Moving or reformatting: v-move-delete and v-emphasis-wrap.

The closure draft closes deleting, moving, wrapping and emphasis. Paraphrase is only partly
closed: P3 to P6 demand positive, correct content. Even so, a writer could leave "are not active"
in r12 next to a correct r26 entry, and no fixed-string predicate sees that. The residual needs a
non-author read of every sentence in r12 that states host state.
QUALITY 77 (`corpus/QUALITY.md:353-354`) says "a statement a critic named explicitly gets its own
named correction row". This report names r12:3, r12:14 and r12:18, so each needs its own
correction row.

## Is freshness the right axis? Yes, but only with a live re-check.

`AXES.md:14`: "skill claims re-verified against live surfaces; stale items flagged or fixed",
signal "Each round LOG entry includes a re-verification result". C1 fixes a stale item, which fits.
But the declared counter never touches a live surface. It measures whether text is absent from
committed bytes, which is the QUALITY 77 correction-sweep property. Without P6 (the r26 readings
reproduced by a live `systemctl` read at closure), C1 is a corpus-hygiene move scored as
freshness. Two related cautions:

- `SCORECARD.md:13` holds freshness at 5 for the red round-10 drift pin. C1 does not touch the pin
  and must not be read as moving it.
- Separability (`AXES.md:29-31`): the r26 `recheck:` must use plain `systemctl`, not
  `tools/mori-oom-killers.py`. Otherwise C1 cannot be verified without C2 having landed.

## Learning-claim rule and sourced-claim rule: both unmet as counted

- Learning, quality trend (`/home/vgpnk/Projects/shokunin/LEARNING.md:34`): it counts as
  improved when "a weaker entry is superseded by a stronger one, or stale entries re-verify". It
  is **harmed** when "an entry is found false or stale and left unmarked". v-narrow passes the
  counter but leaves r12:3, r12:14 and r12:18 stale and unmarked, so quality reads harmed and the
  round cannot be admitted (`AXES.md:33-35`, "no axis is harmed"). The counter cannot tell the two
  outcomes apart.
- Superseding entry: `CORPUS.md:162-165` says a new entry opens with `source:`, `verified-at:` and
  `recheck:`, and `source:` cites its `S###` row. The counter checks none of these; the stub with
  `verified-at: never` passed.
- Sourced claim (`PROTOCOL.md:141-142`, its evidence cites an `S###` row; `CORPUS.md:110-116`
  rule 1, a row is written only after opening the source in that round and gated with URL, date
  and a quote of at most 25 words). The counter does not check it. P5 below re-derives it: an id
  new since 248408f5, `mined`, with `used-by` naming r26. The lesson gate row is left to the
  sourced-claim reviewer.
- Duplicate authority: tsukuroi already records the fact. "The supplementary read-only capture
  shows `earlyoom.service` active and enabled on this host." (`tsukuroi-shokunin` at 157ee255,
  `corpus/knowledge/memory-pressure-r25.md:40-41`). mori's `PROVINCE.md:66` gives systemd-unit
  diagnosis to tsukuroi. The r26 entry should frame its readings as an availability snapshot for
  the fleet-facing rule (as r12:8 did) and cite tsukuroi:40-41. It must never become a second
  authority on unit state.

## Tightest wording the counter supports

```text
C1 (as counted): at revision R, with the counting command run from the lane root and the phrase
file read from its frozen blob 02b7ed18 at 28b0494 (sha256 c072b20a…63a55f6), git grep -F finds,
for none of the four (file, phrase) pairs, a line of that file at R containing the phrase byte for
byte (stale_present 4 at 248408f5 → 0 at R), and the path
corpus/knowledge/userspace-oom-killers-r26.md exists at R.
```

The counter supports nothing about correction, dating, sourcing, supersession or contradiction of
a capture. Under this wording C1 would be a text-removal claim, and on its own it cannot earn
`freshness: improved`.

## Wording that the counter plus the closure predicates support (recommended)

```text
C1: at the landed tip, under QUALITY 77 folding (whitespace folded, * and _ removed), the four
frozen phrases are absent from their files, which still exist; F1 and F3 appear nowhere in
corpus/knowledge, corpus/README.md, SKILL.md or PROVINCE.md; the three critic-named r12 fragments
(r12:3 recheck output, r12:14 is-enabled not-found, r12:18 unit not found) are absent; r12 and its
README row name userspace-oom-killers-r26.md and README carries an r26 index row; the r26 entry
opens with source:, verified-at: 2026-10-22 and recheck:, cites on source: at least one
corpus/SOURCES.md row whose id is absent at 248408f5 and is mined with used-by naming the entry,
and states earlyoom 1.9.0 and the four systemctl is-active/is-enabled readings for earlyoom and
systemd-oomd that a live read reproduces at closure.
```

Writer-seat rules the frozen counter imposes. They are achievable, as v-good shows.

- (a) Do not keep F2 verbatim even inside a dated record. Write "returned `inactive` on
  2026-10-19", not "→".
- (b) The README must not write "inactive on this host", even for the true systemd-oomd half.
- (c) Use r12's own `` `systemctl …` → `value` `` form for the r26 readings, because P4 and P6
  match that form.

## Closure predicates P1–P6 (draft, tested on all seven variants above)

```bash
#!/usr/bin/env bash
# C1 closure predicates: c1-closure.sh <repo> <rev> [--live]; exit 0 pass, 1 fail, 2 setup error
set -u
G=${1:?repo}; R=${2:?rev}; LIVE=${3:-}
BASE=248408f5b6610a85bcbdebe7ac0b4fa7ed51422a
FREEZE=28b0494004fe1f064544224eca56dd42605db384
PSHA=c072b20af5d5eb36978f5ca1f57db05b04c5071902c07109a01a7c53863a55f6
O=corpus/knowledge/userspace-oom-killers-r12.md
E=corpus/knowledge/userspace-oom-killers-r26.md
g() { git -C "$G" "$@"; }
g rev-parse -q --verify "$R^{commit}" >/dev/null || { echo "setup: bad revision $R"; exit 2; }
PH=$(g show "$FREEZE:.ufo/waves/round-26/c1-phrases.txt") || { echo "setup: no frozen phrase blob"; exit 2; }
[ "$(printf '%s\n' "$PH" | sha256sum | cut -c1-64)" = "$PSHA" ] || { echo "setup: phrase blob hash differs"; exit 2; }
fold() { tr -s '[:space:]' ' ' | tr -d '*_'; }
has() { g show "$R:$1" 2>/dev/null | fold | grep -q -F -e "$(printf '%s' "$2" | fold)"; }
fail=0; bad() { echo "FAIL $*"; fail=1; }
n=0                                                   # P1 frozen phrases, folded, file must exist
while IFS='|' read -r f p; do
  g cat-file -e "$R:$f" 2>/dev/null || { bad "P1 target file gone: $f"; continue; }
  has "$f" "$p" && n=$((n+1))
done <<<"$PH"
echo "P1 folded_stale_present=$n"; [ "$n" -eq 0 ] || bad "P1 frozen phrase still present"
while IFS= read -r -d '' path; do                     # P2 long phrases moved anywhere
  for p in "On this host both services are inactive" "Both service units are inactive"; do
    has "$path" "$p" && bad "P2 moved phrase in $path: $p"
  done
done < <(g ls-tree -r -z --name-only "$R" -- corpus/knowledge corpus/README.md SKILL.md PROVINCE.md)
for p in "\`systemctl is-enabled earlyoom.service\` → \`not-found\`" "earlyoom's service unit is not found" "inactive; inactive; 0; 0"; do
  has "$O" "$p" && bad "P3 residual stale fragment in r12: $p"   # P3 critic-named residuals
done
g cat-file -e "$R:$E" 2>/dev/null || bad "P4 r26 entry absent"   # P4 positive supersession
has "$O" "userspace-oom-killers-r26.md" || bad "P4 r12 does not name r26"
g show "$R:corpus/README.md" 2>/dev/null | grep -F '| `knowledge/userspace-oom-killers-r12.md` |' | grep -q -F 'userspace-oom-killers-r26.md' || bad "P4 README r12 row does not name r26"
g show "$R:corpus/README.md" 2>/dev/null | grep -q -F '| `knowledge/userspace-oom-killers-r26.md` |' || bad "P4 README has no r26 index row"
for p in "\`systemctl is-active earlyoom.service\` → \`active\`" "\`systemctl is-enabled earlyoom.service\` → \`enabled\`" "\`systemctl is-active systemd-oomd.service\` → \`inactive\`" "earlyoom 1.9.0"; do
  has "$E" "$p" || bad "P4 r26 lacks: $p"
done
hdr=$(g show "$R:$E" 2>/dev/null | head -3)          # P5 provenance trio + round-26 mined row
printf '%s\n' "$hdr" | sed -n 1p | grep -q '^source: ' || bad "P5 line 1 not source:"
printf '%s\n' "$hdr" | sed -n 2p | grep -q '^verified-at: 2026-10-22' || bad "P5 line 2 not verified-at: 2026-10-22"
printf '%s\n' "$hdr" | sed -n 3p | grep -q '^recheck: ' || bad "P5 line 3 not recheck:"
ids() { awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}'; }
new=$(comm -13 <(g show "$BASE:corpus/SOURCES.md" | ids | sort -u) <(g show "$R:corpus/SOURCES.md" 2>/dev/null | ids | sort -u))
cited=$(printf '%s\n' "$hdr" | sed -n 1p | grep -o -E '\bS[0-9]{3,}\b' | sort -u)
ok=0
for id in $(comm -12 <(printf '%s\n' "$new") <(printf '%s\n' "$cited")); do
  g show "$R:corpus/SOURCES.md" | awk -F'|' -v id="$id" -v e="$E" 'NF==13 {i=$2; s=$9; gsub(/[[:space:]]/,"",i); gsub(/[[:space:]]/,"",s); if (i==id && s=="mined" && index($12, e)) f=1} END {exit !f}' && ok=$((ok+1))
done
echo "P5 round26_rows_cited_and_mined=$ok"; [ "$ok" -ge 1 ] || bad "P5 no round-26 mined SOURCES row cited on source:"
if [ "$LIVE" = --live ]; then                         # P6 live re-verification (freshness)
  for u in earlyoom.service systemd-oomd.service; do
    a=$(systemctl is-active "$u"); e=$(systemctl is-enabled "$u" 2>/dev/null)
    has "$E" "\`systemctl is-active $u\` → \`$a\`" || bad "P6 r26 disagrees with live is-active $u=$a"
    has "$E" "\`systemctl is-enabled $u\` → \`$e\`" || bad "P6 r26 disagrees with live is-enabled $u=$e"
  done
fi
[ "$fail" -eq 0 ] && echo "C1_CLOSURE: PASS" || echo "C1_CLOSURE: FAIL"
exit "$fail"
```

Observed runs, with `--live` on 2026-10-22 against the sandbox:

- 248408f5, v-paraphrase, v-emphasis-wrap, v-move-delete, v-narrow and v-truthful each print
  `C1_CLOSURE: FAIL` and exit 1.
- v-good prints `P1 folded_stale_present=0`, `P5 round26_rows_cited_and_mined=1` and
  `C1_CLOSURE: PASS`, and exits 0.
- `deadbeef` prints `setup: bad revision deadbeef` and exits 2.

Live host reads used by P6 and this report:

- `systemctl is-active earlyoom.service systemd-oomd.service` → `active`, `inactive`.
- `is-enabled` → `enabled`, `disabled`.
- `ActiveEnterTimestamp=Thu 2026-10-22 04:55:44 -03`, `LoadState=loaded`.
- `systemctl --version` → `systemd 262 (262-1-arch)`.
- `pacman -Q` (query only) → `earlyoom 1.9.0-1`, `systemd 262-1`.
- `earlyoom -v` → `earlyoom 1.9.0`.

Known limits of the draft:

- P2 deliberately leaves out F4 ("inactive on this host"). It is short and generic, and a correct
  dated r12 sentence can contain it.
- P4 and P6 assume writer rule (c).
- P6 turns red if the operator changes either unit before closure. That is freshness working, but
  the closure run must name its date.

## Impacted axes

- freshness (claimed): the counter can pass with no correction, or fail a correct one.
- calibration (held at 5): a counted pass would overstate what landed.
- adjacency (held at 6): duplicate unit-state authority with tsukuroi r25.
- The no-harm gate, through the LEARNING.md quality trend: stale lines left unmarked.

## Checks for the L1 to run

- Re-run `c1-closure.sh <lane> <landed tip> --live` from any working directory.
- Re-run the contract command from the lane root, with the phrase blob taken from `28b0494`.
- Have a non-author read every host-state sentence in r12 (the paraphrase residual).
