from pathlib import Path
import base64, html, re, shutil, zipfile
from PIL import Image

ROOT=Path('/mnt/data/github-readme-package'); A=ROOT/'assets'; F=ROOT/'fonts'
BLUE='#247bff'; CRIM='#ff354f'; NAVY='#070b16'; OFF='#f4f6fb'; MUTED='#a8b2c8'; PANEL='#0c1221'

def b64(path): return base64.b64encode(Path(path).read_bytes()).decode()
ID=b64(A/'id.png'); POINT=b64(A/'right_pointing.png'); DISP=b64(F/'NotoSans-Black.woff2'); MONO=b64(F/'NotoMono-Regular.woff2')

def svg_wrap(body,w=1200,h=560, extra_defs=''):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">
<defs>
<style><![CDATA[
@font-face{{font-family:NotoDisplay;src:url(data:font/woff2;base64,{DISP}) format('woff2');font-weight:900}}
@font-face{{font-family:NotoMono;src:url(data:font/woff2;base64,{MONO}) format('woff2');font-weight:400}}
:root{{color-scheme:dark}} .display{{font-family:NotoDisplay,Arial,sans-serif;font-weight:900}} .mono{{font-family:NotoMono,monospace}} .off{{fill:{OFF}}} .muted{{fill:{MUTED}}}
.card{{fill:{PANEL};stroke:#263149;stroke-width:1}} .hair{{stroke:url(#hair);stroke-width:1}} .grid{{stroke:#1a2337;stroke-width:1;opacity:.45}} .blue{{fill:{BLUE}}} .crim{{fill:{CRIM}}}
@media (prefers-reduced-motion:reduce) {{ .anim{{animation:none!important}} }}
]]></style>
<linearGradient id="hair" x1="0" x2="1"><stop stop-color="{BLUE}"/><stop offset=".55" stop-color="#6aa4ff"/><stop offset="1" stop-color="{CRIM}"/></linearGradient>
<linearGradient id="bluefade" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{BLUE}" stop-opacity=".22"/><stop offset="1" stop-color="{CRIM}" stop-opacity=".05"/></linearGradient>
<pattern id="dots" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="#fff" opacity=".07"/></pattern>
{extra_defs}</defs>{body}</svg>'''

def grid(w,h):
    s=[]
    for x in range(0,w,60): s.append(f'<path d="M{x} 0V{h}" class="grid"/>')
    for y in range(0,h,60): s.append(f'<path d="M0 {y}H{w}" class="grid"/>')
    return ''.join(s)

def img(data,x,y,w,h,preserve='xMidYMid meet'):
    return f'<image href="data:image/png;base64,{data}" x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="{preserve}"/>'

# HERO
body=f'''<rect width="1200" height="560" rx="28" fill="{NAVY}"/><rect width="1200" height="560" rx="28" fill="url(#dots)"/>{grid(1200,560)}
<rect x="34" y="34" width="1132" height="492" rx="24" fill="url(#bluefade)" opacity=".55"/>
<path d="M54 470H1146" class="hair"/>
<text x="72" y="86" class="mono muted" font-size="17">// PROFILE.README / 08·OCT·2026</text>
<text x="72" y="142" class="mono" fill="{BLUE}" font-size="20">HELLO, WORLD.</text>
<g class="anim"><text x="70" y="236" class="display off" font-size="92" letter-spacing="-3">NILAMANI</text><text x="74" y="325" class="display" fill="{CRIM}" font-size="92" letter-spacing="-3">KUNDU</text><rect x="70" y="343" width="570" height="8" rx="4" fill="{BLUE}"><animate attributeName="width" values="0;570" dur="1.1s" begin="0s" fill="both"/></rect></g>
<text x="74" y="392" class="mono off" font-size="19">WEB · BACKEND · AI/ML · PROBLEM SOLVING</text>
<text x="74" y="424" class="mono muted" font-size="16">I build practical web applications, backend systems and AI/ML projects.</text>
<g class="anim"><animateTransform attributeName="transform" type="translate" values="0 30;0 0" dur=".9s" begin="0s" fill="both"/><rect x="74" y="452" width="205" height="42" rx="21" fill="{BLUE}"/><text x="176" y="479" text-anchor="middle" class="mono" fill="white" font-size="15">BUILD · LEARN · SHIP</text></g>
<g class="anim"><animateTransform attributeName="transform" type="translate" values="0 -20;0 0" dur="1s" begin="0s" fill="both"/>{img(ID,770,55,335,395)}<circle cx="1010" cy="86" r="7" fill="{CRIM}"/><circle cx="1032" cy="86" r="7" fill="{BLUE}"/><text x="770" y="475" class="mono off" font-size="16">● JHARSUGUDA · INDIA</text><text x="770" y="501" class="mono muted" font-size="14">Python · Flask · React · MySQL · AI/ML</text></g>
<rect x="70" y="28" width="1060" height="2" fill="url(#hair)"/>
'''
(ROOT/'assets/hero.svg').write_text(svg_wrap(body,1200,560),encoding='utf-8')

# ABOUT
slides=[
('01','BUILD','Web applications with Python, Flask, JavaScript, React and MySQL.','From farmer marketplaces to society management, I like turning real problems into usable software.'),
('02','EXPLORE','Machine learning, AI applications, backend systems and APIs.','HealthSence AI and syllabus-aware learning work are part of my exploration into practical AI.'),
('03','LEARN','DSA, problem solving, cleaner architecture and stronger engineering habits.','The goal is simple: keep learning, build more ambitious projects and become a stronger software engineer.')]
slide_groups=[]
for i,(n,t,lead,desc) in enumerate(slides):
    delay=i*4
    base_opacity='1' if i==0 else '0'
    start='1' if i==0 else '0'
    slide_groups.append(f'''<g opacity="{base_opacity}" transform="translate(0 8)"><animate attributeName="opacity" keyTimes="0;.08;.92;1" values="{start};1;1;0" dur="12s" begin="{delay}s" repeatCount="indefinite"/><animateTransform attributeName="transform" type="translate" values="0 8;0 0;0 0;0 -8" keyTimes="0;.08;.92;1" dur="12s" begin="{delay}s" repeatCount="indefinite"/><text x="565" y="150" class="mono" fill="{BLUE}" font-size="15">ABOUT / {n}</text><text x="565" y="194" class="display off" font-size="45">{t}</text><text x="565" y="236" class="mono off" font-size="17">{html.escape(lead)}</text><text x="565" y="270" class="mono muted" font-size="15">{html.escape(desc)}</text></g>''')
bar=[]
for i in range(3):
    x=565+i*185; bar.append(f'<rect x="{x}" y="320" width="165" height="5" rx="2.5" fill="#263149"/><rect x="{x}" y="320" width="165" height="5" rx="2.5" fill="{BLUE}"><animate attributeName="width" values="0;165" dur="4s" begin="{i*4}s" repeatCount="indefinite"/></rect>')
body=f'''<rect width="1200" height="500" rx="28" fill="{NAVY}"/><rect width="1200" height="500" rx="28" fill="url(#dots)"/>{grid(1200,500)}<path d="M50 52H1150" class="hair"/>
<text x="64" y="94" class="mono muted" font-size="16">// ABOUT / THREE THINGS I CARE ABOUT</text>
<g class="card"><rect x="64" y="122" width="450" height="310" rx="24"/><text x="94" y="164" class="mono" fill="{CRIM}" font-size="14">CAPABILITIES</text><text x="94" y="210" class="display off" font-size="38">BUILD WITH</text><text x="94" y="255" class="mono muted" font-size="16">Python · Flask · JavaScript</text><text x="94" y="282" class="mono muted" font-size="16">React · HTML/CSS · MySQL</text><text x="94" y="309" class="mono muted" font-size="16">REST APIs · Machine Learning</text><path d="M94 347H470" class="hair"/><text x="94" y="382" class="mono off" font-size="14">REAL PROBLEMS → REAL SOFTWARE</text><text x="94" y="408" class="mono muted" font-size="13">AgriConnect · Society-Pro · HealthSence AI</text></g>
<g class="card"><rect x="536" y="122" width="600" height="310" rx="24" fill="#0a1020"/>{''.join(slide_groups)}{''.join(bar)}</g>
'''
(ROOT/'assets/about-life.svg').write_text(svg_wrap(body,1200,500),encoding='utf-8')

# STACK
chips=['HTML5','CSS3','JavaScript','React','Python','Flask','MySQL','Git','GitHub','Scikit-learn','FastAPI','REST APIs']
chip_svg=[]
for i,c in enumerate(chips):
    x=70+(i%4)*150; y=410+(i//4)*42
    chip_svg.append(f'<rect x="{x}" y="{y}" width="132" height="30" rx="15" fill="#101a2d" stroke="#273652"/><text x="{x+66}" y="{y+20}" text-anchor="middle" class="mono off" font-size="12">{c}</text>')
# Orbit icon/label tiles
orbit_items=[('JS',0,150),('PY',120,90),('RE',240,150),('FL',60,245),('SQL',180,245),('AI',300,245)]
orbits=[]
for j,(label,dx,dy) in enumerate(orbit_items):
    orbits.append(f'<g transform="translate({dx} {dy})"><circle r="27" fill="#0d172a" stroke="{BLUE if j%2==0 else CRIM}"/><text y="6" text-anchor="middle" class="display" fill="{OFF}" font-size="15">{label}</text></g>')
body=f'''<rect width="1200" height="520" rx="28" fill="{NAVY}"/><rect width="1200" height="520" rx="28" fill="url(#dots)"/>{grid(1200,520)}<path d="M50 52H1150" class="hair"/><text x="64" y="95" class="mono muted" font-size="16">// STACK / THE TOOLS I USE TO SHIP</text>
<g transform="translate(100 110)"><ellipse cx="280" cy="155" rx="280" ry="92" fill="none" stroke="#263149" stroke-width="2" transform="rotate(-12 280 155)"/><ellipse cx="280" cy="155" rx="230" ry="72" fill="none" stroke="#263149" stroke-width="2" transform="rotate(28 280 155)"/><ellipse cx="280" cy="155" rx="180" ry="55" fill="none" stroke="#263149" stroke-width="2" transform="rotate(72 280 155)"/><g class="anim"><animateTransform attributeName="transform" type="rotate" from="0 280 155" to="360 280 155" dur="18s" repeatCount="indefinite"/></g>{''.join(orbits)}<circle cx="280" cy="155" r="52" fill="#101a2d" stroke="url(#hair)" stroke-width="2"/><text x="280" y="150" text-anchor="middle" class="display off" font-size="22">STACK</text><text x="280" y="174" text-anchor="middle" class="mono muted" font-size="12">BUILD · DEBUG</text></g>
<text x="575" y="128" class="display off" font-size="42">TECH CHIPS</text>{''.join(chip_svg)}
<text x="70" y="500" class="mono muted" font-size="13">Custom typographic marks are used here to keep the SVG fully self-contained and network-free.</text>'''
(ROOT/'assets/stack.svg').write_text(svg_wrap(body,1200,520),encoding='utf-8')

# ID DASHBOARD
body=f'''<rect width="1200" height="540" rx="28" fill="{NAVY}"/><rect width="1200" height="540" rx="28" fill="url(#dots)"/>{grid(1200,540)}<path d="M50 52H1150" class="hair"/><text x="64" y="95" class="mono muted" font-size="16">// VERIFIED GITHUB SNAPSHOT / 08·OCT·2026</text>
<g transform="translate(90 110)"><path d="M220 0V34" stroke="#8994a9" stroke-width="5"/><rect x="207" y="28" width="26" height="18" rx="4" fill="#aab3c2"/><circle cx="220" cy="53" r="13" fill="#b8c1cf" stroke="#677389"/><g class="anim"><animateTransform attributeName="transform" type="rotate" values="-5 220 58;4 220 58;-2 220 58;1 220 58;0 220 58" keyTimes="0;.28;.52;.74;1" dur="2.4s" begin="0s" fill="both"/><g transform="translate(90 54)"><rect width="390" height="355" rx="24" fill="#111a2b" stroke="#39455e"/><rect x="0" y="0" width="390" height="62" rx="24" fill="#17233a"/><rect x="0" y="38" width="390" height="24" fill="#17233a"/><text x="26" y="38" class="mono off" font-size="14">NILAMANI KUNDU / GITHUB</text>{img(ID,28,82,160,142)}<text x="210" y="105" class="display off" font-size="27">11</text><text x="210" y="126" class="mono muted" font-size="12">PUBLIC REPOS</text><text x="210" y="162" class="display off" font-size="27">1</text><text x="210" y="183" class="mono muted" font-size="12">STARS</text><text x="28" y="250" class="mono off" font-size="13">FOLLOWERS  0</text><text x="28" y="275" class="mono off" font-size="13">FOLLOWING  1</text><text x="28" y="305" class="mono" fill="{BLUE}" font-size="12">PUBLIC REPOS / FEATURED</text><text x="28" y="329" class="mono muted" font-size="11">Agrreconnect_web</text><text x="28" y="348" class="mono muted" font-size="11">my_portfolio</text><text x="28" y="367" class="mono muted" font-size="11">HealthMate-AI</text><rect x="28" y="386" width="334" height="3" rx="1.5" fill="#263149"/><rect x="28" y="386" width="190" height="3" rx="1.5" fill="{BLUE}"><animate attributeName="x" values="28;170;28" dur="3s" repeatCount="indefinite"/></rect><text x="28" y="410" class="mono" fill="{CRIM}" font-size="10">DATA SOURCE: PUBLIC GITHUB PROFILE</text><text x="28" y="430" class="mono muted" font-size="9">No unverified commit / PR / issue counts shown.</text><path d="M28 455H362" stroke="#33415d"/><g opacity=".22"><rect x="20" y="60" width="350" height="380" fill="url(#hair)" transform="translate(-180 0) rotate(12 200 200)"><animateTransform attributeName="transform" type="translate" values="-240 0;240 0;-240 0" dur="5s" repeatCount="indefinite"/></rect></g></g></g></g>
<text x="585" y="164" class="display off" font-size="48">PUBLIC METRICS</text><text x="585" y="205" class="mono muted" font-size="16">Verified from the visible GitHub profile.</text><g class="card"><rect x="585" y="235" width="500" height="175" rx="22"/><text x="620" y="280" class="mono" fill="{BLUE}" font-size="13">PROFILE</text><text x="620" y="310" class="mono off" font-size="15">Repositories ........ 11</text><text x="620" y="337" class="mono off" font-size="15">Stars ................ 1</text><text x="620" y="364" class="mono off" font-size="15">Followers ............ 0</text><text x="620" y="391" class="mono off" font-size="15">Following ............ 1</text></g>
<text x="585" y="448" class="mono muted" font-size="13">Snapshot date: 08 Oct 2026 · source: github.com/Nilamani77</text>'''
(ROOT/'assets/id-dashboard.svg').write_text(svg_wrap(body,1200,540),encoding='utf-8')

# CONNECT
body=f'''<rect width="1200" height="560" rx="28" fill="{NAVY}"/><rect width="1200" height="560" rx="28" fill="url(#dots)"/>{grid(1200,560)}<path d="M50 52H1150" class="hair"/><text x="64" y="94" class="mono muted" font-size="16">// CONNECT / LET'S BUILD SOMETHING USEFUL</text>
<g class="anim"><animateTransform attributeName="transform" type="translate" values="-20 0;0 0" dur="1s" begin="0s" fill="both"/>{img(POINT,50,110,455,390)}</g>
<g><text x="555" y="148" class="display off" font-size="48">LET'S CONNECT.</text><text x="558" y="180" class="mono muted" font-size="15">Open to collaboration, web projects, backend work and AI/ML.</text>
<g class="card"><rect x="555" y="215" width="560" height="62" rx="20"/><circle cx="585" cy="246" r="16" fill="#111827" stroke="{BLUE}"/><text x="585" y="251" text-anchor="middle" class="display off" font-size="13">GH</text><text x="615" y="251" class="mono off" font-size="15">github.com/Nilamani77</text><path d="M1070 246h22l-8 -6m8 6l-8 6" stroke="{BLUE}" fill="none" stroke-width="2"><animate attributeName="opacity" values=".3;1;.3" dur="1.2s" repeatCount="indefinite"/></path></g>
<g class="card"><rect x="555" y="291" width="560" height="62" rx="20"/><circle cx="585" cy="322" r="16" fill="#111827" stroke="{CRIM}"/><text x="585" y="327" text-anchor="middle" class="display off" font-size="12">IN</text><text x="615" y="327" class="mono off" font-size="14">linkedin.com/in/nilamani-kundu-8924bb259</text></g>
<g class="card"><rect x="555" y="367" width="560" height="62" rx="20"/><circle cx="585" cy="398" r="16" fill="#111827" stroke="{BLUE}"/><text x="585" y="403" text-anchor="middle" class="display off" font-size="12">IG</text><text x="615" y="403" class="mono off" font-size="15">instagram.com/nilamani_77</text></g>
<g class="card"><rect x="555" y="443" width="560" height="62" rx="20"/><circle cx="585" cy="474" r="16" fill="#111827" stroke="{CRIM}"/><text x="585" y="479" text-anchor="middle" class="display off" font-size="11">@</text><text x="615" y="479" class="mono off" font-size="15">nilamanikundu2@gmail.com</text></g></g>
<text x="65" y="526" class="mono muted" font-size="12">Links are rendered below this image in README for GitHub clickability.</text>'''
(ROOT/'assets/connect.svg').write_text(svg_wrap(body,1200,560),encoding='utf-8')

# LICENSES
(ROOT/'LICENSES.md').write_text('''# Embedded asset licenses\n\n## Noto Sans / Noto Mono\nThe embedded `NotoSans-Black.woff2` and `NotoMono-Regular.woff2` fonts are from the Noto font family and are distributed under the SIL Open Font License 1.1.\n\nSource: https://github.com/notofonts/noto-fonts\nLicense text: https://openfontlicense.org/\n\nThe SVGs embed the converted WOFF2 data directly so they make no network requests.\n\n## Icons\nThe stack uses compact typographic labels rather than externally loaded icon files. No third-party icon asset is fetched at runtime.\n''',encoding='utf-8')

# README
readme='''<div align="center">\n\n<img src="assets/hero.svg?v=1" alt="Nilamani Kundu animated profile hero" width="100%" />\n\n</div>\n\n## About\n\n<img src="assets/about-life.svg?v=1" alt="About and interests carousel" width="100%" />\n\n## Stack\n\n<img src="assets/stack.svg?v=1" alt="Technology stack orbit graphic" width="100%" />\n\n## GitHub ID Dashboard\n\n<img src="assets/id-dashboard.svg?v=1" alt="Verified GitHub metrics dashboard" width="100%" />\n\n**Verified snapshot:** 08 October 2026. Public profile data shown above is limited to metrics visible on the public GitHub profile; unknown commit, PR and issue totals are intentionally omitted.\n\n## Featured Projects\n\n| Project | Focus | Stack |\n|---|---|---|\n| [AgriConnect](https://github.com/Nilamani77/Agrreconnect_web) | Farmer-to-consumer e-commerce and product management | Python · Flask · HTML/CSS · JavaScript · MySQL |\n| [Society-Pro](https://github.com/Nilamani77) | Residential society management, authentication and administration | Python · Flask · HTML/CSS · JavaScript · MySQL |\n| [HealthSence AI](https://github.com/Nilamani77) | Machine-learning health risk prediction | Python · Scikit-learn · Flask · MySQL |\n\n## Connect\n\n<img src="assets/connect.svg?v=1" alt="Connect section with pointing character" width="100%" />\n\n<div align="center">\n\n[GitHub](https://github.com/Nilamani77) · [LinkedIn](https://www.linkedin.com/in/nilamani-kundu-8924bb259/) · [Instagram](https://www.instagram.com/nilamani_77/) · [Email](mailto:nilamanikundu2@gmail.com)\n\n</div>\n\n---\n\n<sub>Built with SVG + SMIL/CSS, embedded Noto fonts, and the supplied transparent portraits. No contribution-city section. No external runtime assets.</sub>\n'''
(ROOT/'README.md').write_text(readme,encoding='utf-8')

# preview HTML
(ROOT/'preview.html').write_text('''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Nilamani Kundu README Preview</title><style>body{margin:0;background:#070b16;color:#f4f6fb;font-family:Arial,sans-serif}main{max-width:1200px;margin:auto;padding:24px}section{margin:0 0 28px}img{display:block;width:100%;height:auto;border-radius:18px;box-shadow:0 20px 70px #0008}</style></head><body><main>'''+''.join(f'<section><img src="assets/{n}" alt="{n}"></section>' for n in ['hero.svg','about-life.svg','stack.svg','id-dashboard.svg','connect.svg'])+'''</main></body></html>''',encoding='utf-8')

# copy a plain-text SVG font license notice inside package
# remove TTF files from upload package to keep it lean; WOFF2 are the requested embedded fonts.
for t in F.glob('*.ttf'): t.unlink()

# Zip
zip_path=ROOT.parent/'Nilamani_GitHub_Profile_README_2026.zip'
if zip_path.exists(): zip_path.unlink()
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for p in ROOT.rglob('*'):
        if p.is_file(): z.write(p,p.relative_to(ROOT.parent))
print(zip_path)
