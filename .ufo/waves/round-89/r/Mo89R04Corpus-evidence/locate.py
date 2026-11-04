"""Count quote occurrences in rendered (tag-stripped, entity-decoded, whitespace-collapsed) text."""
import hashlib, html, re, sys
from html.parser import HTMLParser


class T(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip = [], 0

    def handle_starttag(self, tag, a):
        if tag in ("script", "style"):
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip -= 1

    def handle_data(self, d):
        if not self.skip:
            self.out.append(d)


def norm(s):
    s = s.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    return re.sub(r"\s+", " ", s)


JOBS = [
    ("S607", "f/S607.1.html", ["All characters from the comment beginner to end of line are ignored"]),
    ("S609", "f/S609.1.html", ["This string manipulation may change the meaning of a path that contains symbolic links."]),
    ("S610", "f/S610.1.html", ["When called with -c command, it executes the Python statement(s) given as command.",
                               "all consecutive arguments will end up in sys.argv"]),
    ("S611", "f/S611.1.html", ["If the previous character was part of a word, the current character shall be appended to that word.",
                               "If the current character is a '#', it and all subsequent characters up to, but excluding, the next <newline> shall be discarded as a comment."]),
]
for extra in sys.argv[1:]:
    sid, path, q = extra.split("|", 2)
    JOBS.append((sid, path, [q]))
for sid, path, quotes in JOBS:
    raw = open(path, "rb").read()
    p = T(); p.feed(raw.decode("utf-8", "replace"))
    text = norm("".join(p.out))
    for q in quotes:
        n = text.count(norm(q))
        i = text.find(norm(q))
        ctx = text[max(0, i - 90):i] if i >= 0 else ""
        print(f"{sid} sha256={hashlib.sha256(raw).hexdigest()[:16]} count={n} quote={q!r}")
        print(f"   preceding-context: ...{ctx!r}")
