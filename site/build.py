"""Build the study website from the lesson Markdown files.

Usage:  python site/build.py            -> writes the site to _site/
        python site/build.py --out DIR  -> writes it somewhere else

Needs the `markdown` and `pymdown-extensions` packages (pip install markdown pymdown-extensions).
"""
import argparse
import html
import re
import shutil
from pathlib import Path

import markdown

REPO = "vadfr4/CFD-ML"
GITHUB = f"https://github.com/{REPO}"
ROOT = Path(__file__).resolve().parent.parent
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,500'
         '&family=Public+Sans:wght@400;600&display=swap">')

esc = html.escape


KATEX = "https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/"
MATH = (f'<link rel="stylesheet" href="{KATEX}katex.min.css">'
        f'<script defer src="{KATEX}katex.min.js"></script>'
        f'<script defer src="{KATEX}contrib/auto-render.min.js" onload="renderMathInElement(document.body,'
        '{delimiters:[{left:\'\\\\[\',right:\'\\\\]\',display:true},{left:\'\\\\(\',right:\'\\\\)\',display:false}],'
        'ignoredClasses:[\'no-math\']})"></script>')


def md(text):
    return markdown.markdown(
        text.strip(),
        extensions=["tables", "fenced_code", "md_in_html", "pymdownx.arithmatex"],
        extension_configs={"pymdownx.arithmatex": {"generic": True}},
    )


def page(title, body, depth=0, reading=False):
    up = "../" * depth
    cls = "page reading" if reading else "page"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
{FONTS}
<link rel="stylesheet" href="{up}style.css">
{MATH if reading else ""}
</head>
<body>
<div class="{cls}">
{body}
</div>
</body>
</html>
"""


def top_nav(depth=0, crumbs=None):
    up = "../" * depth
    left = f'<a class="brand" href="{up}index.html">CFD-ML</a>'
    if crumbs:
        left = '<div class="crumbs">' + left + "".join(
            f'<span aria-hidden="true">/</span><a href="{up}{href}">{esc(t)}</a>' for t, href in crumbs) + "</div>"
    return f"""<header class="top">
{left}
<nav><a href="{up}resources.html">Resources</a><a href="{GITHUB}">GitHub</a></nav>
</header>"""


def sections(text):
    """Split a lesson file into {heading: body} plus the title and goal."""
    title = re.search(r"^# (.+)$", text, re.M).group(1).strip()
    goal = re.search(r"\*\*Goal:\*\*\s*(.+)", text)
    parts = {}
    for m in re.finditer(r"^## (.+?)\n(.*?)(?=^## |\Z)", text, re.S | re.M):
        parts[m.group(1).strip()] = m.group(2).strip()
    return title, (goal.group(1).strip() if goal else ""), parts


def is_empty(body):
    return not body or all(line.strip() in ("", "-") for line in body.splitlines())


def load():
    subjects = []
    for d in sorted(p for p in ROOT.iterdir() if p.is_dir() and re.match(r"\d\d-", p.name)):
        readme = (d / "README.md").read_text(encoding="utf-8")
        name = readme.splitlines()[0].lstrip("# ").strip()
        intro = readme.split("\n\n")[1].strip() if "\n\n" in readme else ""
        lessons = []
        for f in sorted(d.glob("[0-9][0-9]-*.md")):
            title, goal, parts = sections(f.read_text(encoding="utf-8"))
            topics = re.findall(r"^- \[([ xX])\] (.+)$", parts.get("Topics", ""), re.M)
            lessons.append(dict(file=f, title=title, goal=goal, parts=parts,
                                topics=[(c.lower() == "x", t) for c, t in topics],
                                href=f"{d.name}/{f.stem}.html", src=f"{d.name}/{f.name}"))
        subjects.append(dict(folder=d.name, num=str(int(d.name[:2])), name=name, intro=intro, lessons=lessons))
    return subjects


def build_index(subjects, out):
    total = sum(len(s["lessons"]) for s in subjects)
    first = subjects[0]["lessons"][0]["href"]
    items = []
    for s in subjects:
        lessons = "".join(
            f'<li><a href="{l["href"]}" data-key="{l["src"]}" data-topics="{len(l["topics"])}">{esc(l["title"])}</a></li>'
            for l in s["lessons"])
        items.append(f"""<li class="subject" id="s{s['folder'][:2]}">
<div class="subject-head"><span class="num">{s['num']}</span><h3>{esc(s['name'])}</h3><span class="hours">{len(s['lessons']) * 2} hours</span></div>
<ul class="lessons">{lessons}</ul>
</li>""")
    body = f"""{top_nav()}
<section class="intro">
<h1>Learning CFD, then machine learning for it</h1>
<p class="lead">A self-study plan in {total} lessons. Each one fits a two-hour sitting: half an hour of theory, a hands-on build, and a few minutes of notes. Start at the top and work down; the later subjects train on data from the earlier ones.</p>
<p class="progress" id="progress" hidden></p>
<div><a class="button" id="start" href="{first}">Start the first lesson</a></div>
</section>
<section class="plan">
<h2>The plan</h2>
<ol class="subjects">
{''.join(items)}
</ol>
</section>
<footer>Kept on <a href="{GITHUB}">GitHub</a>. Notes live in each lesson file.</footer>
<script>
(function () {{
  var links = document.querySelectorAll(".lessons a"), done = 0, next = null;
  function read(k) {{ try {{ return localStorage.getItem(k); }} catch (e) {{ return null; }} }}
  links.forEach(function (a) {{
    var n = +a.dataset.topics, ticked = 0;
    for (var i = 0; i < n; i++) if (read("cfdml:" + a.dataset.key + ":" + i) === "1") ticked++;
    if (n && ticked === n) {{
      done++;
      var s = document.createElement("span"); s.className = "done"; s.textContent = "done";
      a.parentNode.appendChild(s);
    }} else if (!next) next = a;
  }});
  if (done) {{
    var p = document.getElementById("progress");
    p.textContent = done + " of " + links.length + " lessons done.";
    p.hidden = false;
    if (next) {{
      var b = document.getElementById("start");
      b.href = next.getAttribute("href"); b.textContent = "Continue: " + next.textContent;
    }}
  }}
}})();
</script>"""
    (out / "index.html").write_text(page("CFD-ML study plan", body), encoding="utf-8")


def build_lessons(subjects, out):
    flat = [(s, l) for s in subjects for l in s["lessons"]]
    for i, (s, l) in enumerate(flat):
        p = l["parts"]
        n_in = s["lessons"].index(l) + 1
        topics = "".join(
            f'<label for="t{j}"><input id="t{j}" type="checkbox" data-i="{j}"{" checked" if c else ""}>'
            f'<span>{markdown.markdown(t)[3:-4]}</span></label>'
            for j, (c, t) in enumerate(l["topics"]))
        resources = p.get("Resources", "").replace(
            "(README.md#resources)", f"({GITHUB}/tree/main/{s['folder']}#resources)")
        edit = f"{GITHUB}/edit/main/{l['src']}"
        build_md = p.get("Build", "")
        nb = l["file"].with_suffix(".ipynb")
        if nb.exists():
            build_md = build_md.split("\n\n- Exercise notebook")[0]
            folder = s["folder"]
            build_md += (f"\n\nOpen [the exercise notebook]({GITHUB}/blob/main/{folder}/{nb.name}) in Jupyter and fill in the gaps. "
                         f"Then compare with [the solution]({GITHUB}/blob/main/{folder}/solutions/{nb.name}).")

        def notes(name):
            body = p.get(name, "")
            if is_empty(body):
                return f'<p class="empty">Nothing yet. <a href="{edit}">Write it on GitHub</a>.</p>'
            return md(body)

        h2 = lambda t: f'<h2 style="font-family: var(--sans)">{esc(t)}</h2>'
        rendered = []
        for name, body_md in p.items():
            if name == "Session plan":
                continue
            if name == "Topics":
                rendered.append(f'<section class="section">{h2("What to cover")}<div class="topics" data-key="{l["src"]}">{topics}</div></section>')
            elif name == "Build":
                rendered.append(f'<section class="section well">{h2("Build")}{md(build_md)}</section>')
            elif name == "Resources":
                rendered.append(f'<section class="section">{h2("Read and watch")}{md(resources)}</section>')
            elif name in ("Notes", "Open questions"):
                rendered.append(f'<section class="section">{h2(name)}{notes(name)}</section>')
            else:
                rendered.append(f'<section class="section">{h2(name)}{md(body_md)}</section>')
        sections_html = "\n".join(rendered)
        plan = ("Two hours: 30 minutes reading the theory, 75 on the example and the build, 15 for the check questions and notes."
                if "Theory" in p else "Two hours: 30 minutes of theory, 75 building, 15 for notes.")

        prev_link = next_link = ""
        if i > 0:
            ps, pl = flat[i - 1]
            prev_link = f'<a href="../{pl["href"]}"><span>Previous</span>{esc(pl["title"])}</a>'
        if i + 1 < len(flat):
            ns, nl = flat[i + 1]
            next_link = f'<a class="next" href="../{nl["href"]}"><span>Next</span>{esc(nl["title"])}</a>'

        body = f"""{top_nav(1, [(s['name'], 'index.html#s' + s['folder'][:2])])}
<article class="prose">
<div class="lesson-head">
<p class="muted" style="font-family: var(--sans); font-size: 15px">Lesson {n_in} of {len(s['lessons'])} in {esc(s['name'])}</p>
<h1 style="font-family: var(--sans)">{esc(l['title'])}</h1>
<p class="lead">{esc(l['goal'])}</p>
<p class="muted" style="font-family: var(--sans); font-size: 15px">{plan}</p>
</div>
{sections_html}
<p class="muted" style="font-family: var(--sans); font-size: 15px">Ticks are saved in this browser only. <a href="{edit}">Edit this lesson on GitHub</a> to keep notes for good.</p>
<nav class="pager" aria-label="Lessons" style="font-family: var(--sans)">{prev_link}{next_link}</nav>
</article>
<script>
(function () {{
  var box = document.querySelector(".topics"), key = "cfdml:" + box.dataset.key + ":";
  box.querySelectorAll("input").forEach(function (c) {{
    try {{ var v = localStorage.getItem(key + c.dataset.i); if (v !== null) c.checked = v === "1"; }} catch (e) {{}}
    c.addEventListener("change", function () {{
      try {{ localStorage.setItem(key + c.dataset.i, c.checked ? "1" : "0"); }} catch (e) {{}}
    }});
  }});
}})();
</script>"""
        target = out / l["href"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page(f"{l['title']} | CFD-ML", body, depth=1, reading=True), encoding="utf-8")


def build_resources(out):
    text = (ROOT / "RESOURCES.md").read_text(encoding="utf-8")
    text = re.sub(r"^# .+\n", "", text)
    body = f"""{top_nav()}
<section class="intro"><h1>Books, videos and papers</h1>
<p class="lead">Everything the lessons point to, in one list. Each lesson links the exact chapter or video to use.</p></section>
<div class="doc">{md(text)}</div>"""
    (out / "resources.html").write_text(page("Resources | CFD-ML", body), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "_site"))
    out = Path(ap.parse_args().out)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    shutil.copy(ROOT / "site" / "style.css", out / "style.css")
    (out / ".nojekyll").write_text("")
    subjects = load()
    build_index(subjects, out)
    build_lessons(subjects, out)
    build_resources(out)
    print(f"Built {sum(len(s['lessons']) for s in subjects)} lessons into {out}")


if __name__ == "__main__":
    main()
