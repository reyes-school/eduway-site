"""Shelf hero: original screen-print style cover/spine art for the six EduWay roles,
drawn as inline SVG symbols (so the page font renders all three languages)."""
import html, json
from content_shelf import S, ROLE_IDS, GROUPS

e = lambda s: html.escape(str(s), quote=True)

NAVY, SKY, CREAM, PW = "#0B2A55", "#00AEEF", "#F3EEE3", "#FBF8F1"
VERM, MUST, GREEN, VIOLET = "#E5512B", "#F2B33D", "#1F8A5B", "#5B3FA8"

# bg, text, accent, accent2
PAL = {
    "admin":      (NAVY,      CREAM, SKY,   MUST),
    "manager":    (SKY,       NAVY,  CREAM, VERM),
    "accountant": ("#EDE4D0", NAVY,  GREEN, MUST),
    "teacher":    (VERM,      CREAM, NAVY,  MUST),
    "caregiver":  (MUST,      NAVY,  SKY,   VERM),
    "parent":     (VIOLET,    CREAM, SKY,   MUST),
}
HT = 'fill="url(#shf-ht)"'


def art(rid):
    bg, tx, a, b = PAL[rid]
    if rid == "admin":
        cols = "".join(f'<rect x="{117 + i * 52}" y="605" width="28" height="120" fill="{CREAM}"/>' for i in range(5))
        return f'''<circle cx="237" cy="520" r="150" fill="{a}"/><circle cx="237" cy="520" r="150" {HT}/>
<polyline points="96,452 168,410 226,432 300,362 352,336" fill="none" stroke="{b}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>
<polygon points="384,318 362,354 344,326" fill="{b}"/>
<path d="M82 588 L237 492 L392 588 Z" fill="{CREAM}"/><circle cx="237" cy="556" r="14" fill="{bg}"/>
<rect x="100" y="588" width="274" height="14" fill="{CREAM}"/>{cols}
<rect x="92" y="725" width="290" height="16" fill="{CREAM}"/><rect x="76" y="741" width="322" height="16" fill="{CREAM}"/>
<rect x="40" y="770" width="394" height="4" fill="{a}"/>'''
    if rid == "manager":
        cells = ""
        fills = {(1, 0): b, (3, 1): SKY, (0, 2): NAVY, (2, 2): MUST, (2, 0): NAVY}
        for c in range(4):
            for r in range(3):
                x, y = 125 + c * 56, 490 + r * 64
                if (c, r) in fills:
                    cells += f'<rect x="{x + 7}" y="{y + 7}" width="42" height="50" rx="4" fill="{fills[(c, r)]}"/>'
        grid = "".join(f'<rect x="{125 + c * 56}" y="490" width="3" height="192" fill="{NAVY}"/>' for c in range(1, 4))
        grid += "".join(f'<rect x="125" y="{490 + r * 64}" width="224" height="3" fill="{NAVY}"/>' for r in range(1, 3))
        return f'''<circle cx="237" cy="545" r="165" fill="{CREAM}"/><circle cx="237" cy="545" r="165" {HT}/>
<rect x="107" y="412" width="260" height="290" rx="12" fill="{PW}" stroke="{NAVY}" stroke-width="6"/>
<rect x="107" y="412" width="260" height="64" rx="10" fill="{NAVY}"/>
<rect x="158" y="390" width="14" height="44" rx="7" fill="{b}"/><rect x="302" y="390" width="14" height="44" rx="7" fill="{b}"/>
{grid}{cells}
<circle cx="368" cy="418" r="54" fill="{b}"/>
<path d="M346 442 Q346 398 368 396 Q390 398 390 442 L398 450 L338 450 Z" fill="{NAVY}"/><circle cx="368" cy="458" r="7" fill="{NAVY}"/>
<rect x="40" y="770" width="394" height="4" fill="{NAVY}"/>'''
    if rid == "accountant":
        coins = ""
        for cx, n in ((150, 4), (237, 7), (324, 3)):
            for k in range(n):
                cy = 744 - k * 22
                coins += (f'<ellipse cx="{cx}" cy="{cy + 14}" rx="56" ry="15" fill="#C88A1C" stroke="{NAVY}" stroke-width="3"/>'
                          f'<rect x="{cx - 56}" y="{cy}" width="112" height="14" fill="#D99A25"/>'
                          f'<ellipse cx="{cx}" cy="{cy}" rx="56" ry="15" fill="{b}" stroke="{NAVY}" stroke-width="3"/>')
        zig = " ".join(f"{322 - i * 14},{628 if i % 2 else 640}" for i in range(13))
        lines = "".join(f'<rect x="174" y="{392 + i * 32}" width="{w}" height="9" rx="4" fill="{NAVY}"/>' for i, w in enumerate((120, 88, 130, 70, 104)))
        return f'''<circle cx="237" cy="500" r="150" fill="{a}"/><circle cx="237" cy="500" r="150" {HT}/>
<g transform="rotate(-8 237 500)"><polygon points="152,352 322,352 {zig} 152,640" fill="{PW}" stroke="{NAVY}" stroke-width="4" stroke-linejoin="round"/>
{lines}<rect x="174" y="574" width="126" height="16" rx="3" fill="{b}"/></g>
{coins}<rect x="40" y="770" width="394" height="4" fill="{NAVY}"/>'''
    if rid == "teacher":
        return f'''<circle cx="252" cy="500" r="152" fill="{b}"/><circle cx="252" cy="500" r="152" {HT}/>
<line x1="134" y1="610" x2="104" y2="768" stroke="{NAVY}" stroke-width="12" stroke-linecap="round"/>
<line x1="340" y1="610" x2="370" y2="768" stroke="{NAVY}" stroke-width="12" stroke-linecap="round"/>
<rect x="72" y="398" width="330" height="222" rx="6" fill="{NAVY}" stroke="{CREAM}" stroke-width="10"/>
<text x="104" y="480" font-size="48" font-weight="700" fill="{CREAM}" font-family="Manrope,sans-serif">a²+b²</text>
<path d="M108 548 L134 574 L186 518" fill="none" stroke="{CREAM}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="330" cy="546" r="38" fill="none" stroke="{MUST}" stroke-width="6"/>
<text x="330" y="564" text-anchor="middle" font-size="50" font-weight="800" fill="{MUST}" font-family="Manrope,sans-serif">5</text>
<rect x="360" y="648" width="20" height="14" rx="3" fill="{NAVY}"/>
<circle cx="370" cy="716" r="58" fill="{CREAM}" stroke="{NAVY}" stroke-width="6"/>
<path d="M370 716 L370 678 M370 716 L398 728" stroke="{NAVY}" stroke-width="7" stroke-linecap="round"/>
<rect x="40" y="782" width="394" height="4" fill="{NAVY}"/>'''
    if rid == "caregiver":
        return f'''<circle cx="237" cy="470" r="132" fill="{CREAM}"/><circle cx="237" cy="470" r="132" {HT}/>
<path d="M368 434 Q350 470 366 520 Q372 560 360 600" fill="none" stroke="{NAVY}" stroke-width="3"/>
<ellipse cx="368" cy="390" rx="36" ry="44" fill="{b}"/><polygon points="362,432 374,432 368,442" fill="{b}"/>
<g transform="rotate(-4 239 538)"><rect x="180" y="480" width="118" height="118" rx="8" fill="{b}"/>
<text x="239" y="572" text-anchor="middle" font-size="86" font-weight="800" fill="{CREAM}" font-family="Manrope,sans-serif">C</text></g>
<g transform="rotate(-7 175 668)"><rect x="110" y="603" width="130" height="130" rx="8" fill="{NAVY}"/>
<text x="175" y="702" text-anchor="middle" font-size="92" font-weight="800" fill="{CREAM}" font-family="Manrope,sans-serif">A</text></g>
<g transform="rotate(6 306 672)"><rect x="246" y="612" width="120" height="120" rx="8" fill="{a}"/>
<text x="306" y="702" text-anchor="middle" font-size="86" font-weight="800" fill="{NAVY}" font-family="Manrope,sans-serif">B</text></g>
<rect x="40" y="748" width="394" height="5" fill="{NAVY}"/>'''
    if rid == "parent":
        bars = "".join(f'<rect x="{184 + i * 24}" y="{650 - h}" width="15" height="{h}" rx="3" fill="{VIOLET if i < 4 else SKY}"/>' for i, h in enumerate((40, 58, 48, 76, 96)))
        return f'''<circle cx="237" cy="530" r="152" fill="{a}"/><circle cx="237" cy="530" r="152" {HT}/>
<path d="M118 700 C76 668 74 626 102 624 C114 624 118 634 118 636 C118 634 122 624 134 624 C162 626 160 668 118 700 Z" fill="{VERM}" transform="rotate(-12 118 660)"/>
<rect x="152" y="378" width="170" height="344" rx="26" fill="{NAVY}"/>
<rect x="164" y="408" width="146" height="284" rx="12" fill="{CREAM}"/><rect x="212" y="390" width="50" height="8" rx="4" fill="{CREAM}"/>
<circle cx="194" cy="444" r="16" fill="{b}"/><rect x="218" y="438" width="64" height="11" rx="5" fill="{NAVY}"/>
<text x="180" y="530" font-size="40" font-weight="800" fill="{NAVY}" font-family="Manrope,sans-serif">98%</text>
<rect x="180" y="544" width="110" height="7" rx="3" fill="{NAVY}" fill-opacity=".25"/>{bars}
<rect x="264" y="430" width="156" height="60" rx="30" fill="{b}"/>
<circle cx="295" cy="460" r="18" fill="{NAVY}"/><path d="M286 460 L293 467 L305 453" fill="none" stroke="{CREAM}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="322" y="453" width="78" height="13" rx="6" fill="{NAVY}"/>
<rect x="40" y="770" width="394" height="4" fill="{a}"/>'''
    return ""


def _fit(text, size, maxw, k=0.7):
    est = len(text) * size * k
    return f' textLength="{maxw}" lengthAdjust="spacingAndGlyphs"' if est > maxw else ""


def cover(rid, n, L):
    bg, tx, a, b = PAL[rid]
    name, sub = S[L]["roles"][rid][:2]
    words = name.upper().split(" ")
    lines = [" ".join(words)] if len(name) <= 10 or len(words) == 1 else [words[0], " ".join(words[1:])]
    longest = max(len(x) for x in lines)
    fs = min(84, int(406 / (longest * 0.7)))
    t = ""
    y = 100 + fs
    for ln in lines:
        t += f'<text x="34" y="{y}" font-size="{fs}" font-weight="800" letter-spacing="-1" fill="{tx}"{_fit(ln, fs, 406)}>{e(ln)}</text>'
        y += int(fs * 0.98)
    subc = a if rid not in ("manager", "accountant") else (NAVY if rid == "manager" else GREEN)
    if rid == "teacher":
        subc = CREAM
    sfs = min(17, round(404 / (len(sub) * .8), 1))
    t += f'<text x="36" y="{y + 6}" font-size="{sfs}" font-weight="700" letter-spacing="1.4" fill="{subc}"{_fit(sub.upper(), sfs, 404, .8)}>{e(sub.upper())}</text>'
    return f'''<symbol id="shf-cv-{rid}" viewBox="0 0 474 900"><rect width="474" height="900" fill="{bg}"/>
<g font-family="Manrope,sans-serif">
<text x="34" y="56" font-size="15" font-weight="800" letter-spacing="3.5" fill="{tx}">EDUWAY</text>
<text x="440" y="56" text-anchor="end" font-size="15" font-weight="700" letter-spacing="2.5" fill="{tx}">{S[L]["role"]} {n:02d}</text>
<rect x="34" y="72" width="406" height="2.5" fill="{tx}"/>{t}</g>
{art(rid)}
<g font-family="Manrope,sans-serif"><rect x="34" y="806" width="406" height="2.5" fill="{tx}"/>
<text x="34" y="852" font-size="14" font-weight="700" letter-spacing="2.2" fill="{tx}">{S[L]["platforms"]}</text>
<rect x="368" y="826" width="72" height="34" fill="none" stroke="{tx}" stroke-width="2.5"/>
<text x="404" y="850" text-anchor="middle" font-size="17" font-weight="800" letter-spacing="1.5" fill="{tx}">EDU</text></g>
<rect width="474" height="900" fill="url(#shf-wear)"/></symbol>'''


def spine(rid, n, L):
    bg, tx, a, b = PAL[rid]
    name = S[L]["roles"][rid][0].upper()
    fs = 42 if len(name) <= 12 else 36
    num_fill = bg if rid != "caregiver" else NAVY
    return f'''<symbol id="shf-sp-{rid}" viewBox="0 0 142 840"><rect width="142" height="840" fill="{bg}"/>
<g font-family="Manrope,sans-serif">
<circle cx="71" cy="88" r="40" fill="{a if rid != 'teacher' else MUST}"/>
<text x="71" y="98" text-anchor="middle" font-size="27" font-weight="800" fill="{num_fill}">{n:02d}</text>
<rect x="24" y="148" width="94" height="3" fill="{tx}"/>
<text transform="translate({71 - fs * 0.36:.1f} 178) rotate(90)" font-size="{fs}" font-weight="800" letter-spacing="1" fill="{tx}"{_fit(name, fs, 446, .74)}>{e(name)}</text>
<rect x="24" y="642" width="94" height="3" fill="{tx}"/>
<text transform="translate(65 664) rotate(90)" font-size="14" font-weight="800" letter-spacing="3" fill="{tx}">EDUWAY</text>
<rect x="34" y="770" width="74" height="40" fill="none" stroke="{tx}" stroke-width="2.5"/>
<text x="71" y="797" text-anchor="middle" font-size="17" font-weight="800" letter-spacing="1.2" fill="{tx}">EDU</text></g>
<rect width="142" height="840" fill="url(#shf-edge)"/><rect width="142" height="840" fill="url(#shf-wear)"/></symbol>'''


def sprite(L):
    defs = '''<defs>
<pattern id="shf-ht" width="8" height="8" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.6" fill="#000" fill-opacity=".17"/></pattern>
<linearGradient id="shf-edge" x1="0" x2="1"><stop offset="0" stop-color="#000" stop-opacity=".28"/><stop offset=".14" stop-color="#000" stop-opacity="0"/><stop offset=".84" stop-color="#fff" stop-opacity=".06"/><stop offset="1" stop-color="#000" stop-opacity=".3"/></linearGradient>
<linearGradient id="shf-wear" x1="0" y1="0" x2=".3" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".1"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".12"/></linearGradient>
<filter id="shf-inkf" x="-50%" y="-50%" width="200%" height="200%"><feTurbulence type="fractalNoise" baseFrequency=".011" numOctaves="3" seed="7" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="120" xChannelSelector="R" yChannelSelector="G"/></filter>
</defs>'''
    syms = "".join(cover(r, i + 1, L) + spine(r, i + 1, L) for i, r in enumerate(ROLE_IDS))
    return f'<svg class="shf-sprite" aria-hidden="true" focusable="false" width="0" height="0">{defs}{syms}</svg>'


def data(L):
    s = S[L]
    return {
        "open": s["open"], "role": s["role"], "of": s["of"], "items": s["items"],
        "roles": [{"id": r, "g": GROUPS[r], "name": s["roles"][r][0], "sub": s["roles"][r][1],
                   "sum": s["roles"][r][2], "list": s["roles"][r][3]} for r in ROLE_IDS],
    }


def hero(T, cta_href, more_href, logo_html):
    L = T["lang"]; s = S[L]
    tabs = "".join(f'<button type="button" class="shf-tab lbl" data-g="{g}">{e(n)}</button>' for g, n in s["tabs"])
    seo = "".join(f'<li><b>{e(s["roles"][r][0])}</b> ({e(s["roles"][r][1])}): {e(s["roles"][r][2])}</li>' for r in ROLE_IDS)
    first = s["roles"][ROLE_IDS[0]]
    arrow_l = '<svg width="18" height="10" viewBox="0 0 18 10" fill="none" stroke="currentColor" stroke-width="1.2"><path d="M5 1 L1 5 L5 9M1 5H17"/></svg>'
    arrow_r = '<svg width="18" height="10" viewBox="0 0 18 10" fill="none" stroke="currentColor" stroke-width="1.2"><path d="M13 1 L17 5 L13 9M17 5H1"/></svg>'
    return f'''<section class="shf" id="shf" aria-labelledby="h1">
{sprite(L)}
<div class="shf-intro"><p class="lbl shf-kick">{e(s["kick"])}</p><h1 id="h1">{e(s["h1"])}</h1></div>
<nav class="shf-tabs" aria-label="{e(s["tabs_label"])}"><span class="shf-ind" aria-hidden="true"></span>{tabs}</nav>
<div class="shf-shelf" role="region" aria-label="{e(s["shelf_label"])}"><div class="shf-stage"></div>
<button type="button" class="shf-play" aria-label="{e(s["open_role"])}"><svg width="12" height="12" viewBox="0 0 12 12"><path d="M2 1 L11 6 L2 11Z" fill="currentColor"/></svg></button></div>
<div class="shf-caprow">
<button type="button" class="shf-arr shf-prev" aria-label="{e(s["prev"])}">{arrow_l}</button>
<div class="shf-cap" aria-live="polite">
<div class="shf-m shf-t"><span>{e(first[0])}</span></div>
<div class="shf-m shf-s lbl"><span>{e(first[1])}</span></div>
<div class="shf-m shf-y"><span>{s["role"]} 01 / 06</span></div>
</div>
<button type="button" class="shf-arr shf-next" aria-label="{e(s["next"])}">{arrow_r}</button>
</div>
<div class="shf-foot"><span class="lbl shf-hint">{e(s["hint"])}</span>
<div class="shf-ctas"><a class="btn btn-primary" href="{cta_href}">{e(T["mobile_cta"])}</a><a class="shf-more lbl box" href="{more_href}">{e(s["cta2"])} ›</a></div>
<span class="lbl shf-plat">{s["platforms"]}</span></div>
<ul class="sr">{seo}</ul>
<script type="application/json" id="shf-data">{json.dumps(data(L), ensure_ascii=False)}</script>
</section>
<div class="shf-detail" role="dialog" aria-modal="true" aria-labelledby="shf-dt" tabindex="-1">
<div class="shf-dtop"><button type="button" class="shf-close lbl box">{e(s["close"])}</button><div class="shf-dlogo">{logo_html}</div></div>
<div class="shf-dgrid">
<div class="shf-dtext">
<div class="shf-m"><p class="lbl shf-ds"></p></div>
<div class="shf-m"><h2 class="shf-dh" id="shf-dt"></h2></div>
<div class="shf-m"><p class="lbl shf-dmeta"></p></div>
<div class="shf-m"><p class="shf-dsum"></p></div>
<ul class="shf-dlist"></ul>
<div class="shf-m"><p class="shf-dcred">{e(s["credit"])}</p></div>
<div class="shf-m"><a class="shf-dbtn lbl box" href="{cta_href}">{e(s["cta"])}</a></div>
</div>
<div class="shf-poster"><svg viewBox="0 0 474 900" aria-hidden="true"><defs><mask id="shf-ink" maskUnits="userSpaceOnUse" x="-200" y="-200" width="874" height="1300"><g filter="url(#shf-inkf)">
<circle cx="150" cy="330" r="0" fill="#fff"/><circle cx="340" cy="600" r="0" fill="#fff"/><circle cx="250" cy="120" r="0" fill="#fff"/><circle cx="90" cy="760" r="0" fill="#fff"/><circle cx="400" cy="250" r="0" fill="#fff"/><circle cx="260" cy="860" r="0" fill="#fff"/><circle cx="230" cy="470" r="0" fill="#fff"/>
</g></mask></defs><g mask="url(#shf-ink)"><use class="shf-puse" href="#shf-cv-admin" width="474" height="900"/></g></svg></div>
</div>
</div>
<div class="shf-cursor" aria-hidden="true"><i class="shf-ring"></i><i class="shf-dot"></i><b>{e(s["open"])}</b></div>
'''
