import subprocess, re, html, pathlib

REPO = pathlib.Path(__file__).resolve().parent.parent
DOCS = [
    ("syllabus",   "The Syllabus",   "42 weeks, 85 films",        "sabbatical-film-syllabus.md"),
    ("watch",      "Where to Watch", "streaming availability",     "where-to-watch.md"),
    ("comparison", "Comparison",     "vs. 11 university syllabi",  "syllabus-comparison.md"),
]

def convert(md):
    out = subprocess.run(
        ["pandoc", str(REPO/md), "-f", "markdown", "-t", "html5", "--no-highlight"],
        capture_output=True, text=True, check=True).stdout
    # drop the leading <h1> (it becomes the doc title in the UI)
    out = re.sub(r'^\s*<h1[^>]*>.*?</h1>', '', out, count=1, flags=re.S)
    return out

def slugify(s, seen={}):
    s = re.sub(r'<[^>]+>', '', s)
    s = html.unescape(s)
    s = re.sub(r'[^\w\s-]', '', s).strip().lower()
    s = re.sub(r'[\s_-]+', '-', s)
    n = seen.get(s, 0); seen[s] = n+1
    return s if n == 0 else f"{s}-{n}"

sections, navs = [], []
for key, label, blurb, md in DOCS:
    body = convert(md)
    # give every h2 an id and collect for the nav
    items = []
    def tag(m):
        txt = m.group(2)
        sid = slugify(f"{key}-{txt}")
        items.append((sid, re.sub(r'<[^>]+>', '', txt)))
        return f'<h2 id="{sid}">{txt}</h2>'
    body = re.sub(r'<h2[^>]*>(.*?)</h2>', lambda m: tag(re.match(r'()(.*)', m.group(1))), body, flags=re.S)
    sections.append(f'<section class="doc" id="doc-{key}" data-doc="{key}">{body}</section>')
    links = "\n".join(f'<a class="navlink" href="#{i}">{html.escape(t)}</a>' for i, t in items)
    navs.append(f'<div class="navgroup" data-doc="{key}"><div class="navhead">{html.escape(label)}'
                f'<span class="navblurb">{html.escape(blurb)}</span></div>{links}</div>')

tabs = "\n".join(
    f'<button class="tab{" active" if i==0 else ""}" data-doc="{k}">{html.escape(l)}</button>'
    for i,(k,l,_,_) in enumerate(DOCS))

CSS = """
:root{--bg:#faf8f5;--panel:#f2ede6;--ink:#1f1d1b;--muted:#6b6560;--accent:#7a2e2e;
--rule:#ddd5ca;--code:#eee8e0;--max:44rem}
@media(prefers-color-scheme:dark){:root{--bg:#161514;--panel:#1e1c1a;--ink:#e8e4de;
--muted:#9b938a;--accent:#c98b7e;--rule:#332f2b;--code:#26231f}}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);
font:16px/1.65 "Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;
-webkit-font-smoothing:antialiased}
#wrap{display:flex;min-height:100vh;align-items:flex-start}
aside{position:sticky;top:0;height:100vh;overflow-y:auto;flex:0 0 19rem;
background:var(--panel);border-right:1px solid var(--rule);padding:1.5rem 1.1rem 3rem}
.brand{font:600 1.05rem/1.3 ui-sans-serif,-apple-system,"Segoe UI",Roboto,sans-serif;
color:var(--accent);margin-bottom:.15rem}
.brandsub{font:400 .74rem/1.4 ui-sans-serif,-apple-system,sans-serif;color:var(--muted);
margin-bottom:1.2rem}
.tabs{display:flex;flex-direction:column;gap:.25rem;margin-bottom:1.4rem}
.tab{all:unset;cursor:pointer;padding:.42rem .6rem;border-radius:5px;
font:500 .82rem/1.3 ui-sans-serif,-apple-system,sans-serif;color:var(--muted)}
.tab:hover{background:rgba(122,46,46,.08);color:var(--ink)}
.tab.active{background:var(--accent);color:#fff}
.navgroup{display:none}.navgroup.show{display:block}
.navhead{display:none}
.navlink{display:block;padding:.3rem .6rem;border-left:2px solid transparent;
font:400 .79rem/1.4 ui-sans-serif,-apple-system,sans-serif;color:var(--muted);
text-decoration:none;margin-bottom:.05rem}
.navlink:hover{color:var(--ink);border-left-color:var(--accent)}
.navlink.current{color:var(--accent);border-left-color:var(--accent);font-weight:600}
main{flex:1;min-width:0;padding:3rem 3rem 6rem;display:flex;justify-content:center}
.inner{width:100%;max-width:var(--max)}
.doc{display:none}.doc.show{display:block}
.doctitle{font:700 2rem/1.2 ui-sans-serif,-apple-system,sans-serif;color:var(--accent);
margin:0 0 1.8rem}
h2{font:700 1.28rem/1.3 ui-sans-serif,-apple-system,sans-serif;color:var(--accent);
margin:2.6rem 0 .2rem;padding-top:1.4rem;border-top:1px solid var(--rule);scroll-margin-top:1.5rem}
h2:first-of-type{border-top:none;padding-top:0;margin-top:0}
h3{font:600 .95rem/1.4 ui-sans-serif,-apple-system,sans-serif;color:var(--muted);
margin:.2rem 0 1.2rem;letter-spacing:.02em}
h4{font:600 .93rem/1.4 ui-sans-serif,-apple-system,sans-serif;margin:1.8rem 0 .5rem}
p{margin:0 0 1rem}
ul,ol{margin:0 0 1.1rem;padding-left:1.3rem}
li{margin-bottom:.45rem}
li>em:first-child{font-style:italic}
strong{font-weight:600}
hr{border:none;border-top:1px solid var(--rule);margin:2.2rem 0}
a{color:var(--accent)}
blockquote{margin:1.2rem 0;padding-left:1rem;border-left:2px solid var(--rule);
color:var(--muted);font-style:italic}
code{background:var(--code);padding:.1em .35em;border-radius:3px;font-size:.87em}
table{width:100%;border-collapse:collapse;margin:1.2rem 0;
font:400 .84rem/1.5 ui-sans-serif,-apple-system,sans-serif}
th{text-align:left;font-weight:600;border-bottom:1.5px solid var(--rule);
padding:.5rem .55rem;color:var(--muted);font-size:.78rem;letter-spacing:.03em;
text-transform:uppercase}
td{padding:.5rem .55rem;border-bottom:1px solid var(--rule);vertical-align:top}
tr:hover td{background:rgba(122,46,46,.045)}
.pdflink{display:inline-block;margin-bottom:1.6rem;padding:.32rem .7rem;
border:1px solid var(--rule);border-radius:5px;text-decoration:none;
font:500 .76rem ui-sans-serif,-apple-system,sans-serif;color:var(--muted)}
.pdflink:hover{border-color:var(--accent);color:var(--accent)}
#menu{display:none}
@media(max-width:860px){
  #wrap{display:block}
  aside{position:static;height:auto;width:100%;flex:none;border-right:none;
  border-bottom:1px solid var(--rule)}
  main{padding:1.6rem 1.2rem 4rem}
  .navgroup{display:none!important}
}
@media print{
  aside{display:none}main{padding:0}.doc{display:block!important}
  .pdflink,.tabs{display:none}
  h2{page-break-after:avoid}table,li{page-break-inside:avoid}
}
"""

JS = """
const tabs=[...document.querySelectorAll('.tab')];
const docs=[...document.querySelectorAll('.doc')];
const groups=[...document.querySelectorAll('.navgroup')];
function show(k){
  tabs.forEach(t=>t.classList.toggle('active',t.dataset.doc===k));
  docs.forEach(d=>d.classList.toggle('show',d.dataset.doc===k));
  groups.forEach(g=>g.classList.toggle('show',g.dataset.doc===k));
  document.querySelector('aside').scrollTop=0;
  window.scrollTo(0,0);
  try{localStorage.setItem('sf-doc',k)}catch(e){}
}
tabs.forEach(t=>t.onclick=()=>show(t.dataset.doc));
// deep links: switch to whichever doc owns the target section
document.querySelectorAll('.navlink').forEach(a=>{
  a.onclick=e=>{const g=a.closest('.navgroup'); if(g) show(g.dataset.doc);};
});
let start='syllabus';
try{const s=localStorage.getItem('sf-doc'); if(s&&document.getElementById('doc-'+s))start=s;}catch(e){}
if(location.hash){const el=document.querySelector(location.hash);
  const d=el&&el.closest('.doc'); if(d)start=d.dataset.doc;}
show(start);
if(location.hash){const el=document.querySelector(location.hash); if(el)setTimeout(()=>el.scrollIntoView(),60);}
// highlight nav on scroll
const heads=[...document.querySelectorAll('h2[id]')];
const io=new IntersectionObserver(es=>{
  es.forEach(en=>{ if(!en.isIntersecting) return;
    document.querySelectorAll('.navlink.current').forEach(n=>n.classList.remove('current'));
    const l=document.querySelector('.navlink[href="#'+CSS.escape(en.target.id)+'"]');
    if(l){l.classList.add('current');}
  });
},{rootMargin:'-10% 0px -80% 0px'});
heads.forEach(h=>io.observe(h));
"""

PDFS = {"syllabus":"sabbatical-film-syllabus.pdf","watch":"where-to-watch.pdf",
        "comparison":"syllabus-comparison.pdf"}
titled = []
for (key,label,blurb,md), sec in zip(DOCS, sections):
    sec = sec.replace('>', f'><h1 class="doctitle">{html.escape(label)}</h1>'
        f'<a class="pdflink" href="{PDFS[key]}">Download PDF &#8599;</a>', 1)
    titled.append(sec)

out = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>A Sabbatical in Film</title>
<style>{CSS}</style></head><body>
<div id="wrap">
<aside>
  <div class="brand">A Sabbatical in Film</div>
  <div class="brandsub">42 weeks &middot; 24 Aug 2026 &ndash; 4 Jul 2027<br>85 core films</div>
  <div class="tabs">{tabs}</div>
  {"".join(navs)}
</aside>
<main><div class="inner">{"".join(titled)}</div></main>
</div>
<script>{JS}</script>
</body></html>"""

(REPO/"index.html").write_text(out, encoding="utf-8")
print("wrote index.html:", len(out), "bytes")
