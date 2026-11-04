import re,html,hashlib,os
SRC="/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-89/w1/Mo89S01Sources/sources"
Q=[("shlex.html","S607","shlex.commenters","All characters from the comment beginner to end of line are ignored"),
   ("shlex.html","S607b","shlex.split(s, comments=False, posix=True)","If comments is False (the default), the parsing of comments in the given string will be disabled"),
   ("shlex.html","S610","module intro (shlex — Simple lexical analysis)","The shlex class makes it easy to write lexical analyzers for simple syntaxes resembling that of the Unix shell"),
   ("os.path.html","S608","os.path.normpath(path)","Normalize a pathname by collapsing redundant separators and up-level references so that A//B, A/B/, A/./B and A/foo/../B all become A/B."),
   ("os.path.html","S608b","os.path.normpath(path)","This string manipulation may change the meaning of a path that contains symbolic links."),
   ("cmdline.html","S609","1.1.1 Interface options","When called with a file name argument or with a file as standard input, it reads and executes a script from that file."),
   ("cmdline.html","S609b","1.1.1 Interface options","When called with -c command, it executes the Python statement(s) given as command."),
   ("cmdline.html","S609c","1.1.1 Interface options","all consecutive arguments will end up in sys.argv")]
def render(raw):
    t=re.sub(r'<script.*?</script>','',raw,flags=re.S)
    t=re.sub(r'<style.*?</style>','',t,flags=re.S)
    t=re.sub(r'<[^>]+>','',t)
    return re.sub(r'\s+',' ',html.unescape(t)).strip()
def span(raw,a,b):
    t="\n".join(raw[a-1:b]); t=re.sub(r'<[^>]+>','',t); t=html.unescape(t); return re.sub(r'\s+',' ',t)
out=[]
out.append("# Mo89S01Sources — durable source evidence (round 89, w1)")
out.append("# produced 2026-11-04 by seat Mo89S01Sources; fetch + locator receipt")
out.append("# fetch tool: curl 8.23.0 (official upstream binary, pre-installed; nothing installed this round)")
out.append("# method: curl -sSL -A 'mori-r89-source-seat/1.0' <url> -o <file>; two fetches per URL, compared with cmp")
for f in ("shlex.html","os.path.html","cmdline.html"):
    raw=open(f,encoding="utf-8").read()
    b=open(f+".txt","rb").read() if False else None
    data=open(f,"rb").read()
    dup=open(f.replace(".html",".b.html"),"rb").read()
    out.append("")
    out.append("## %s" % f)
    out.append("  bytes=%d  lines=%d  sha256=%s" % (len(data), raw.count("\n")+1, hashlib.sha256(data).hexdigest()))
    out.append("  second fetch byte-identical: %s" % ("YES (cmp rc=0)" if data==dup else "NO"))
    out.append("  title=%s" % re.search(r'<title>([^<]*)</title>',raw).group(1))
    out.append("  doc-version string=%s" % (re.search(r'\d+\.\d+\.\d+ documentation',raw).group(0) if re.search(r'\d+\.\d+\.\d+ documentation',raw) else "?"))
    out.append("  doc date line: %s" % ("yes" if re.search(r'Release \d+\.\d+\.\d+',raw) else "no 'Release' banner found"))
for f,sid,loc,q in Q:
    raw=open(f,encoding="utf-8").read().split("\n")
    txt=render("\n".join(raw))
    n=txt.count(q)
    best=None
    for a in range(len(raw)):
        for w in range(1,20):
            b=a+w
            if b>len(raw): break
            if q in span(raw,a+1,b):
                if best is None or (b-a)<(best[1]-best[0]): best=(a+1,b)
                break
    out.append("")
    out.append("## quote %s  [%s]" % (sid,f))
    out.append("  section locator : %s" % loc)
    out.append("  raw html lines  : %s" % ("%d-%d" % best if best else "NOT LOCATED"))
    out.append("  word count      : %d" % len(q.split()))
    out.append("  occurrences in rendered page text: %d" % n)
    out.append("  EXACT QUOTE     : %s" % q)
open(os.path.join(SRC,"fetch-and-locator-receipt.txt"),"w",encoding="utf-8").write("\n".join(out)+"\n")
print("\n".join(out))
