import html, pathlib
from playwright.sync_api import sync_playwright

root = pathlib.Path(__file__).parent
shots = [
    ("1", "docker --version"),
    ("2", "dir"),
    ("3", "docker build -t pyspark-demo ."),
    ("4", "docker images pyspark-demo"),
    ("5", "docker run --rm pyspark-demo"),
    ("6", 'docker run --rm -v "${PWD}:/app" pyspark-demo python -c "import pyspark,sys;print(...)"'),
]
tpl = """<body style="margin:0;background:#1e1e1e"><div style="font:14px Consolas,monospace;color:#ddd;
padding:16px;width:880px;white-space:pre-wrap"><div style="color:#6a9955">PS C:\\...\\pyspark&gt; <span style="color:#fff">{cmd}</span></div>{out}</div></body>"""
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 912, "height": 200})
    for n, cmd in shots:
        out = (root / f"{n}.txt").read_text(encoding="utf-8-sig", errors="replace")
        pg.set_content(tpl.format(cmd=html.escape(cmd), out=html.escape(out)))
        pg.locator("body > div").screenshot(path=str(root / f"step{n}.png"))
    b.close()
