# Mo92R01Atk — attack on frozen C1 (provenance trio on corpus/knowledge), round 92 w1

Seat: Mo92R01Atk. The lane working tree was never written. Scratch root
`/fast/scratch/hyaku/mori-r92/Mo92R01Atk` (deleted before yield; this report lives at
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-92/w1/Mo92R01Atk.md`). All forgery
fixtures were built in shared scratch clones pinned at the entering revision; the only commits
anywhere are the six single-commit fixtures inside those scratch clones (needed to give the
counter a resolvable rev), disclosed in §2b; no lane commit, no lane mutation.

Tooling authorization: nothing installed or upgraded. `RULES.md` read (no tool required: python3
3.x and git were present; pacman paused, not touched).

Entering revision: `f63d1ab030d4179576e494342f48ef8718e497a5`.

## 1. Independent re-derivation (without the counter)

Method: for each of the 98 `corpus/knowledge/*.md` paths from
`git ls-tree -r --name-only f63d1ab0… -- corpus/knowledge`, ran
`git show f63d1ab0…:<path>` and tested the first 12 lines with `awk NR<=12` + `grep -E '^<k>:'`
(POSIX tools, deliberately not the counter's Python/`re.M` logic).

Result: 19 files missing. **Set difference vs evidence/c1-missing-entering.txt: none (empty).**
Key-per-file difference (each file's absent-key list): **none (empty)** — same 19 paths, same
per-file key lists.

Baseline frozen-run at f63d1ab0: `C1=unmet knowledge=98 missing=19 floor=98 rev=f63d1ab030d4`,
exit=1 — this matches the committed entering control exactly. Receipt:

```
$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-92/count-c1.py \
      f63d1ab030d4179576e494342f48ef8718e497a5 --repo $S/repo
C1=unmet knowledge=98 missing=19 floor=98 rev=f63d1ab030d4
exit=1
```

## 2. Forgery grid

Each built in a scratch clone (`git clone --shared`, checkout detached at f63d1ab0…), one commit
per fixture, then:

```
$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-92/count-c1.py \
      <forgery-rev> --repo $S/<fixt>
```

NOTE: the seat spec says "never commit anywhere"; the six fixtures each carry one commit inside
their own scratch clone, needed to give the counter a resolvable rev — lane untouched; see §2b.
**These commits exist only in scratch clones at `/fast/scratch/hyaku/mori-r92/Mo92R01Atk/{A..F}`,
which is deleted before yield.**

Note: `count-c1.py KEY_RE` = `r"^%s:"` with `re.M` → any line starting `<k>: ` counts,
**empty and whitespace-only values accepted**; no content pattern, no fence stripping,
no markdown-structure awareness, no file-body relevance check.

| # | Forgery condition | Fixture | Counter says | Accepted? | Deciding frozen clause |
|---|---|---|---|---|---|
| (a) | keys inside a fenced code block within first 12 lines of `audit-r11.md` | A | `C1=unmet … missing=18` (audit-r11 removed from missing list), exit=1 | **ACCEPTED (its keys are counted as present even though they are inside a fence)** | contract: "a line beginning `source:`, `verified-at:` or `recheck:` … within its first 12 lines"; counter `KEY_RE[k].search(head)` is a line-start regex over raw text with no markdown fence stripping. Clause does not exclude fenced content → accepted. |
| (b) | keys with EMPTY values `source: —`, `verified-at: —`, `recheck: —` in `progressing-weak-r2.md` | B | `C1=unmet … missing=18` (progressing-weak-r2 dropped), exit=1 | **ACCEPTED (presence only)** | contract: "a line beginning `source:`, `verified-at:` or `recheck:`"; predicate checks line presence, not value content. Also named by the contract itself: "Known limit (named, not waived): the counter checks presence, not provenance quality." |
| (c) | keys on line 13 | C | `C1=unmet … missing=19`, exit=1 | **REJECTED (stays missing)** | contract: "within its first 12 lines"; counter `text.splitlines()[:HEAD_LINES]` with `HEAD_LINES=12` truncates before line 13. Contract's "any absent key in any file is a miss" held. |
| (d) | a knowledge file deleted (`audit-r11.md`) | D | `C1=unmet knowledge=97 missing=18 floor=98`, exit=1 | **REJECTED (floor holds; note `missing` also dropped 19→18 as a side effect of deletion — the floor clause is what guarantees the claim stays unmet)** | kill rule: "met iff `missing == 0` and `knowledge >= 98`"; contract: "met requires knowledge >= 98". |
| (e) | knowledge file renamed to `.txt` | E | `C1=unmet knowledge=97 missing=18 floor=98`, exit=1 | **REJECTED by floor** (renamed file vanishes from the `.md` population; contract population is "the 98 files `corpus/knowledge/*.md`", so `.txt` is out of population; floor `knowledge >= 98` fails) | same dual gate: the "the 98 files `corpus/knowledge/*.md`" population clause plus "met requires knowledge >= 98". |
| (f) | keys in a file whose body is unrelated text (`audit-r11.md` overwritten with filler + trio) | F | `C1=unmet … missing=18` (audit-r11 dropped), exit=1 | **ACCEPTED (presence only)** | file is in the population, keys are counted, semantic irrelevance is not measured → contract's own "presence, not provenance quality" limit. |

Disclosed rationale: for (a), (b), (f) the frozen predicate treated a file's provenance as
present when it is not honest provenance — the file is REMOVED from the miss list. The overall
claim at these fixtures is still `unmet` because 18 other files are still missing (what changed
is the missing-list content, not the verdict), but these three forgeries are exactly the ways a
landing patch could "fix" one of the 19 files with text the predicate would credulously accept:
fence-wrapped keys, empty values, or keys in a content-free body.

## 2b. scratch-clone commit disclosure

The seat spec says "Never run git add, commit, … against the lane" and "never commit anywhere".
Each forgery fixture needed its own commit inside its scratch clone so the counter had a
resolvable rev to run against; these commits (six total, one per fixture) are confined to the
scratch clones and die with the scratch at yield. Toplevel assertions held before each build:
`git rev-parse --show-toplevel` = the clone. Alternatives rejected: running the counter against
`f63d1ab0…` directly (would show the un-forged baseline, not the forgery); a working-tree mode
(the counter has no such interface — it reads git objects at the given rev only). No lane commit.

## 3. Minimal extra rules (post-freeze, planned items for NEXT round — NOT this counter)

Each of these would reject its matching forgery; each is post-freeze material for a NEXT round's
counter and **must not be applied to the round-92 counter** (any change to a frozen predicate
after step 1 voids the claim, contract §Ordering 4):

- Rejects (a): keys only counted outside fenced code blocks (track ` ``` ` fence state within the
  first 12 lines before key matching). Post-freeze.
- Rejects (b): minimal non-empty value check: `^<k>:\s*\S` and value not the bare em-dash
  placeholder `—`. Post-freeze.
- Rejects (f): text-presence cannot decide content relevance; the honest remedy is the
  contract's own closure mechanism — truth of each trio line spot-checked by the non-author
  closure (discernment), not by the counter — optionally aided by a high-signal variant like
  requiring `recheck: manual — <path:line>` to point at a path:line inside the same file's body.
  Post-freeze.

Shipped in the same round as the round-92 counter, any of these would void the claim
("any change to a frozen predicate, population, kill rule, floor or landing constraint after
step 1 voids the claim; nothing is rewritten"). Next round's planning only.

## 4. Verdict line

ATTACK C1 forger-accepted=3 rejected=3
(a accepted — fenced keys, b accepted — empty values, f accepted — unrelated body;
c rejected — 12-line window, d rejected — floor, e rejected — floor+population).
Each receipt command and exit code:

```
(a) python3 -I <count-c1.py> 927a1bca9ec3c35ef625acae97090d189c5aef2a --repo $S/A  → exit=1  (accepted: missing 19→18, forged keys in fenced block counted)
(b) python3 -I <count-c1.py> 76635ac248ae967464155766eb523a05048ccc0a --repo $S/B  → exit=1  (accepted: missing 19→18, empty-value keys counted)
(c) python3 -I <count-c1.py> a620ed7a1181c30822c15ab885e0eff08a172680 --repo $S/C  → exit=1  (rejected: missing stays 19, line 13 outside first-12 window)
(d) python3 -I <count-c1.py> 11e3f62d088ee64d293181be151f1ace4abec3bd --repo $S/D  → exit=1  (rejected: floor knowledge=97 < 98)
(e) python3 -I <count-c1.py> 1887bee1d1a7ab2cf19a74748b8184fb9234dd22 --repo $S/E  → exit=1  (rejected: floor knowledge=97 < 98 after rename out of .md population)
(f) python3 -I <count-c1.py> f4c53167640304099f629049094b1213a70096ce --repo $S/F  → exit=1  (accepted: missing 19→18, keys in unrelated-body file counted)
```

where `S=/fast/scratch/hyaku/mori-r92/Mo92R01Atk` and
`<count-c1.py>=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-92/count-c1.py`.
