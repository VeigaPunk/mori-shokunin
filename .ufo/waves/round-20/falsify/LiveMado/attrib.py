#!/usr/bin/env python3
"""LiveMado: (1) seat-attribution of every present report by its header; (2) tool A->B byte delta.

(1) For each present member, read the first 400 bytes of its report and look for a
    `MadoR<round>.<Name>` seat id. A present report whose seat id names another member or another
    round is a false-present candidate. Reports without a seat id are counted, not judged.
(2) Byte accounting of the tool change observed between 07:45:51 (28261 bytes, used by the committed
    fleet scan and scan.json) and 08:04:26 (28797 bytes). Prints the lines that the change inserted.
"""
import csv
import os
import re
import collections

BASE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SCR = BASE + "/.ufo/waves/round-20/falsify/LiveMado"
TOOL = BASE + "/tools/mori-wave-settlement.py"
SEAT = re.compile(rb"MadoR(\d+)\.([A-Za-z0-9_]+)")


def attribution():
    with open(SCR + "/members-live.tsv", newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t", quoting=csv.QUOTE_NONE))
    present = [r for r in rows if r["live_status"] == "present"]
    ok = 0
    no_header = []
    mismatch = []
    seat_round_hist = collections.Counter()
    for r in present:
        rel = r["report_rel"]
        match = re.match(r"\.ufo/waves/round-(\d+)/w\d", rel)
        path_round = int(match.group(1))
        with open(os.path.join(LANE, rel), "rb") as stream:
            head = stream.read(400)
        seats = SEAT.findall(head)
        if not seats:
            no_header.append(rel)
            continue
        for rnd, name in seats[:1]:
            seat_round_hist[int(rnd) == path_round] += 1
        if any(name.decode() == r["name"] and int(rnd) == path_round for rnd, name in seats):
            ok += 1
        else:
            mismatch.append([rel, r["name"], [(int(rnd), name.decode()) for rnd, name in seats[:2]]])
    print("ATTR present", len(present), "header-verified-match", ok, "no-seat-header", len(no_header),
          "mismatch", len(mismatch))
    print("ATTR first-seat round equals path round:", dict(seat_round_hist))
    print("ATTR mismatches:", mismatch[:40])
    print("ATTR no-header sample:", no_header[:12])
    print("ATTR no-header per wave:", dict(collections.Counter(re.match(r".*/round-(\d+)/(w\d)", p).group(0)
                                                             for p in no_header)))


def tool_delta():
    src = open(TOOL, "rb").read()
    lines = src.split(b"\n")
    inserted_idx = list(range(47, 50)) + list(range(527, 531))
    print("DELTA total bytes now", len(src), "| 28797 expected now; 28261 at 07:45:51 (from earlier ls)")
    for i in inserted_idx:
        print("DELTA line %d: %r" % (i + 1, lines[i]))
    inserted = sum(len(lines[i]) + 1 for i in inserted_idx)
    print("DELTA inserted bytes (candidate block)", inserted, "| size minus block =", len(src) - inserted)


if __name__ == "__main__":
    attribution()
    tool_delta()
