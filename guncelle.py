# Uygulamanın web sürümünü siteye kopyalar: python guncelle.py
# pdfstudio-rn/scripts/build-web.js ile tek dosya web.html üretir, app/index.html olarak koyar
# ve sitedeki araç linklerinin (app/#t/merge gibi) doğrudan o aracı açması için açılış rotasını düzeltir.
import pathlib, subprocess

site = pathlib.Path(__file__).parent
rn = site.parent / "pdfstudio-rn"
subprocess.run(["node", "scripts/build-web.js"], cwd=rn, check=True)

html = (rn / "assets" / "web.html").read_text(encoding="utf8")
reps = [
    ('<link rel="icon" href="data:,">',
     '<link rel="icon" href="../icon.png"><link rel="apple-touch-icon" href="../icon.png">'),
    ('history.replaceState({d:0,r:"home"},"","#home");route();',
     '{const r0=location.hash.slice(1);history.replaceState({d:0,r:"home"},"","#home");'
     'if(r0&&r0!="home")go(r0,true);else route()}'),
]
for old, new in reps:
    if html.count(old) != 1:
        raise SystemExit("Bulunamadı: " + old)
    html = html.replace(old, new)

out = site / "app" / "index.html"
out.parent.mkdir(exist_ok=True)
out.write_text(html, encoding="utf8")
print("app/index.html", round(len(html) / 1e6, 1), "MB")
