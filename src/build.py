#!/usr/bin/env python3
"""EduWay static site generator.  Usage:  python3 build.py <output_dir>

Edit the CONFIG block below (domain, contacts, prices), then rebuild.
Content lives in content_uz.py / content_ru.py / content_en.py.
"""
import json, os, sys, shutil, html, datetime, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content_uz import T as UZ
from content_ru import T as RU
from content_en import T as EN

# ───────────────────────── CONFIG (placeholders — replace before launch) ─────────────────────────
SITE = "https://eduway-site-weld.vercel.app"  # production domain, no trailing slash (change when a custom domain is added)
PHONE = "+998 77 007 76 56"          # shown on the site
PHONE_TEL = "+998770077656"
TELEGRAM = ""                         # e.g. "eduway_uz" (without @)
EMAIL = ""                            # e.g. "info@eduway.uz" (also receives demo form via mailto)
INSTAGRAM = ""                        # full URL, optional
ADDRESS = {"uz": "Oʻzbekiston", "ru": "Узбекистан", "en": "Uzbekistan"}
TODAY = datetime.date.today().isoformat()
# ─────────────────────────────────────────────────────────────────────────────────────────────────

LANGS = [UZ, RU, EN]
PREFIX = {"uz": "/", "ru": "/ru/", "en": "/en/"}
HREFLANG = {"uz": "uz", "ru": "ru", "en": "en"}
CASE_SLUG = "steam-plaza/"
CONTACT_ID = {"uz": "narxlar", "ru": "ceny", "en": "pricing"}  # lead form = pricing section
e = lambda s: html.escape(str(s), quote=True)

ICONS = {
 "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
 "check": '<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
 "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>',
 "wallet": '<path d="M20 12V8H6a2 2 0 0 1 0-4h12v4"/><path d="M4 6v12a2 2 0 0 0 2 2h14v-4"/><path d="M18 12a2 2 0 0 0 0 4h4v-4z"/>',
 "spark": '<path d="M12 3l1.9 5.8L20 11l-6.1 2.2L12 19l-1.9-5.8L4 11l6.1-2.2z"/><path d="M19 3v4M17 5h4"/>',
 "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
 "bell": '<path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.7 21a2 2 0 0 1-3.4 0"/>',
 "msg": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
 "trophy": '<path d="M8 21h8M12 17v4M7 4h10v5a5 5 0 0 1-10 0z"/><path d="M17 5h3v2a3 3 0 0 1-3 3M7 5H4v2a3 3 0 0 0 3 3"/>',
 "news": '<path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2zm0 0a2 2 0 0 1-2-2v-9h4"/><path d="M18 14h-8M15 18h-5M10 6h8v4h-8z"/>',
 "food": '<path d="M3 2v7c0 1.1.9 2 2 2h2a2 2 0 0 0 2-2V2M6 2v20M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3zm0 0v7"/>',
 "branch": '<path d="M3 21h18M5 21V8l7-5 7 5v13"/><path d="M9 21v-6h6v6"/>',
 "lock": '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
 "users": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
 "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>',
 "list": '<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
 "globe": '<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 0 1 4 10 15 15 0 0 1-4 10 15 15 0 0 1-4-10 15 15 0 0 1 4-10z"/>',
 "save": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/>',
 "tick": '<path d="M20 6L9 17l-5-5"/>',
 "circle-check": '<circle cx="12" cy="12" r="10"/><path d="M8 12l3 3 5-6"/>',
 "menu": '<path d="M3 6h18M3 12h18M3 18h18"/>',
 "arrow": '<path d="M5 12h14M13 5l7 7-7 7"/>',
 "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
 "send": '<path d="M22 2L11 13M22 2l-7 20-4-9-9-4z"/>',
 "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 6l-10 7L2 6"/>',
 "x": '<path d="M18 6L6 18M6 6l12 12"/>',
 "pin": '<path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
}
def ic(name, cls=""):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"{(" class=%s" % cls) if cls else ""}>{ICONS[name]}</svg>'

def url(T, case=False):
    return SITE + PREFIX[T["lang"]] + (CASE_SLUG if case else "")

def ids(T):
    return [a[1:] for a, _ in T["nav"]]  # features, roles, brand, case, pricing, faq

def contact_items(T):
    out = []
    if PHONE:
        inner = f'<a href="tel:{e(PHONE_TEL)}">{e(PHONE)}</a>' if PHONE_TEL else e(PHONE)
        out.append(f'<li>{ic("phone")}<span>{inner}</span></li>')
    if TELEGRAM:
        out.append(f'<li>{ic("send")}<a href="https://t.me/{e(TELEGRAM)}" rel="noopener">@{e(TELEGRAM)}</a></li>')
    if EMAIL:
        out.append(f'<li>{ic("mail")}<a href="mailto:{e(EMAIL)}">{e(EMAIL)}</a></li>')
    out.append(f'<li>{ic("pin")}<span>{e(ADDRESS[T["lang"]])}</span></li>')
    return "\n".join(out)

# ───────────────────────── JSON-LD ─────────────────────────
def org_ld():
    o = {"@type": "Organization", "@id": SITE + "/#org", "name": "EduWay", "alternateName": "EduWay Education Platform",
         "url": SITE + "/", "logo": {"@type": "ImageObject", "url": SITE + "/assets/img/eduway-logo.png", "width": 480, "height": 136},
         "description": UZ["answer_a"], "areaServed": {"@type": "Country", "name": "Uzbekistan"},
         "knowsLanguage": ["uz", "ru", "en"]}
    same = [x for x in [("https://t.me/" + TELEGRAM) if TELEGRAM else "", INSTAGRAM] if x]
    if same: o["sameAs"] = same
    cp = {"@type": "ContactPoint", "contactType": "sales", "availableLanguage": ["Uzbek", "Russian", "English"], "areaServed": "UZ"}
    if PHONE_TEL: cp["telephone"] = PHONE_TEL
    if EMAIL: cp["email"] = EMAIL
    if PHONE_TEL or EMAIL: o["contactPoint"] = [cp]
    return o

def home_ld(T):
    L, u = T["lang"], url(T)
    graph = [org_ld(),
      {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "EduWay", "publisher": {"@id": SITE + "/#org"},
       "inLanguage": ["uz", "ru", "en"]},
      {"@type": "WebPage", "@id": u + "#webpage", "url": u, "name": T["meta_title"], "description": T["meta_desc"],
       "inLanguage": L, "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#software"},
       "primaryImageOfPage": SITE + "/assets/img/og-" + L + ".png", "dateModified": TODAY,
       "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["#answer h2", "#answer p"]}},
      {"@type": "SoftwareApplication", "@id": SITE + "/#software", "name": "EduWay", "applicationCategory": "EducationalApplication",
       "applicationSubCategory": "School management system", "operatingSystem": "iOS, Android, Web",
       "description": T["answer_a"], "inLanguage": ["uz", "ru"], "publisher": {"@id": SITE + "/#org"},
       "featureList": [f[1] for f in T["feats"]], "screenshot": [SITE + "/assets/img/app-parent-green.webp", SITE + "/assets/img/web-dashboard.webp"]},
      {"@type": "Product", "@id": SITE + "/#product", "name": "EduWay — white-label school platform", "brand": {"@type": "Brand", "name": "EduWay"},
       "description": T["brand_lead"], "image": SITE + "/assets/img/og-" + L + ".png", "category": "School management software"},
      {"@type": "Service", "@id": u + "#launch", "name": T["launch_h2"], "serviceType": "White-label school platform setup",
       "provider": {"@id": SITE + "/#org"}, "areaServed": "UZ",
       "description": " ".join(f"{w}: {t}." for w, t, _ in T["launch"])},
      {"@type": "FAQPage", "@id": u + "#faq", "inLanguage": L,
       "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in T["faq"]]},
    ]
    return {"@context": "https://schema.org", "@graph": graph}

def case_ld(T):
    L, u = T["lang"], url(T, True)
    return {"@context": "https://schema.org", "@graph": [
      org_ld(),
      {"@type": "Article", "@id": u + "#article", "headline": T["c_h1"], "description": T["c_desc"], "inLanguage": L,
       "url": u, "mainEntityOfPage": u, "image": [SITE + "/assets/img/web-dashboard.webp", SITE + "/assets/img/app-parent-green.webp"],
       "datePublished": "2026-11-20", "dateModified": TODAY, "author": {"@id": SITE + "/#org"}, "publisher": {"@id": SITE + "/#org"},
       "about": [{"@type": "EducationalOrganization", "name": "Steam Plaza"}, {"@id": SITE + "/#software"}]},
      {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": T["c_crumb_home"], "item": url(T)},
        {"@type": "ListItem", "position": 2, "name": T["c_crumb"], "item": u}]},
    ]}

# ───────────────────────── layout ─────────────────────────
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def _ver(rel):
    """Cache-busting version for immutable-cached assets (content hash)."""
    for base in ("site", "dist"):
        fp = os.path.join(_ROOT, base, rel.lstrip("/"))
        if os.path.exists(fp):
            return rel + "?v=" + hashlib.md5(open(fp, "rb").read()).hexdigest()[:10]
    return rel
CSS_URL = _ver("/assets/css/site.css")
JS_URL = _ver("/assets/js/site.js")

def head(T, title, desc, canon, alts, ld, og_img):
    L = T["lang"]
    alt_links = "\n".join(f'<link rel="alternate" hreflang="{HREFLANG[l]}" href="{h}">' for l, h in alts.items())
    alt_links += f'\n<link rel="alternate" hreflang="x-default" href="{alts["uz"]}">'
    og_alt = "\n".join(f'<meta property="og:locale:alternate" content="{X["locale"]}">' for X in LANGS if X is not T)
    return f'''<!doctype html>
<html lang="{L}" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<link rel="canonical" href="{canon}">
{alt_links}
<meta name="theme-color" content="#0B2A55">
<meta name="author" content="EduWay">
<meta property="og:type" content="website">
<meta property="og:site_name" content="EduWay">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(title)}">
<meta property="og:locale" content="{T["locale"]}">
{og_alt}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{og_img}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/icon-32.png">
<link rel="apple-touch-icon" href="/assets/img/icon-180.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/manrope-latin.woff2" as="font" type="font/woff2" crossorigin>
{'<link rel="preload" href="/assets/fonts/manrope-cyrillic.woff2" as="font" type="font/woff2" crossorigin>' if L == "ru" else ''}
<link rel="stylesheet" href="{CSS_URL}">
<link rel="alternate" type="text/plain" title="LLM summary" href="/llms.txt">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False, separators=(",", ":"))}</script>
</head>
<body>
<a class="skip" href="#main">{e(T["skip"])}</a>
'''

def header(T, alts, on_home=True):
    L = T["lang"]; P = PREFIX[L]
    base = "" if on_home else P
    links = "".join(f'<a href="{base}{T["nav"][i][0]}">{e(T["nav"][i][1])}</a>' for i in (0, 1, 2, 3, 6, 4))
    mlinks = "".join(f'<li><a href="{base}{a}">{e(n)}</a></li>' for a, n in T["nav"])
    langs = "".join(f'<a href="{alts[X["lang"]].replace(SITE, "")}" hreflang="{X["lang"]}" lang="{X["lang"]}"{" aria-current=\"true\"" if X is T else ""} title="{X["name"]}">{X["short"]}</a>' for X in LANGS)
    cta = f'{base}#{CONTACT_ID[L]}'
    return f'''<div class="ann"><a href="{P}{CASE_SLUG}">{e(T["ann"])} <span>{e(T["ann_link"])} ›</span></a></div>
<header class="hdr">
<div class="pill">
<a class="logo" href="{P}" aria-label="EduWay"><img src="/assets/img/eduway-logo.png" alt="EduWay — Education Platform" width="113" height="32"></a>
<nav class="nav" aria-label="{e(T["menu"])}">{links}</nav>
<div class="hdr-r">
<div class="lang" aria-label="Language">{langs}</div>
<a class="btn btn-primary btn-sm" href="{cta}">{e(T["mobile_cta"])}</a>
<button class="burger" type="button" aria-expanded="false" aria-controls="mnav" aria-label="{e(T["menu"])}"><span></span><span></span></button>
</div>
</div>
</header>
<div class="mnav" id="mnav" hidden>
<ul>{mlinks}</ul>
<div class="mnav-foot"><div class="lang">{langs}</div><a class="btn btn-primary btn-lg" href="{cta}">{e(T["mobile_cta"])}</a><a class="mnav-tel" href="tel:{e(PHONE_TEL)}">{e(PHONE)}</a></div>
</div>
'''

def footer(T):
    L = T["lang"]; P = PREFIX[L]
    nav = "".join(f'<li><a href="{P}{a}">{e(n)}</a></li>' for a, n in T["nav"][:3])
    comp = f'<li><a href="{P}{CASE_SLUG}">{e(T["ftr_case"])}</a></li>' + "".join(f'<li><a href="{P}{a}">{e(n)}</a></li>' for a, n in T["nav"][4:])
    langs = "".join(f'<li><a href="{PREFIX[X["lang"]]}" hreflang="{X["lang"]}" lang="{X["lang"]}">{X["name"]}</a></li>' for X in LANGS)
    return f'''<footer class="ftr">
<div class="wrap">
<div class="cols">
<div><img src="/assets/img/eduway-logo.png" alt="EduWay" width="113" height="32" loading="lazy"><p>{e(T["ftr_about"])}</p></div>
<div><h3>{e(T["ftr_product"])}</h3><ul>{nav}</ul></div>
<div><h3>{e(T["ftr_company"])}</h3><ul>{comp}</ul></div>
<div><h3>{e(T["ftr_contact"])}</h3><ul class="cinfo">{contact_items(T)}</ul><ul class="flangs">{langs}</ul></div>
</div>
<div class="bottom"><span>© <span id="year">{datetime.date.today().year}</span> EduWay. {e(T["ftr_rights"])}</span><a href="/llms.txt">llms.txt</a></div>
</div>
</footer>
<a class="mcta" href="{PREFIX[L]}#{CONTACT_ID[L]}">{e(T["mobile_cta"])}</a>
<script src="{JS_URL}" defer></script>
</body>
</html>
'''

def phone(img, alt, cls, eager=False):
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<div class="phone {cls}"><img src="/assets/img/{img}.webp" alt="{e(alt)}" width="600" height="1298" {load} decoding="async"></div>'

def lead_section(T):
    L = T["lang"]
    incl = "".join(f'<li>{ic("tick")}<span>{e(x)}</span></li>' for x in T["price_incl"])
    return f'''<section class="lead-sec" id="{CONTACT_ID[L]}" aria-labelledby="price-h">
<div class="wrap">
<div class="head center"><p class="kicker">{e(T["price_eyebrow"])}</p><h2 id="price-h">{e(T["price_h2"])}</h2><p class="sub">{e(T["price_lead"])}</p></div>
<div class="lead-grid">
<div class="lead-side">
<ul class="ticks">{incl}</ul>
<ul class="cinfo">{contact_items(T)}</ul>
</div>
<form class="lead-form" id="leadForm" action="/api/lead" method="post" data-sending="{e(T["f_sending"])}" novalidate>
<input type="hidden" name="lang" value="{L}">
<input type="hidden" name="page" value="">
<div class="hp" aria-hidden="true"><label>Website<input name="website" tabindex="-1" autocomplete="off"></label></div>
<fieldset class="seg"><legend class="sr">{e(T["f_type"])}</legend>
<label><input type="radio" name="type" value="school" checked><span>{e(T["f_type_school"])}</span></label>
<label><input type="radio" name="type" value="partner"><span>{e(T["f_type_partner"])}</span></label>
</fieldset>
<label>{e(T["f_name"])}<input name="name" autocomplete="name" maxlength="80" required></label>
<label>{e(T["f_phone"])}<input name="phone" type="tel" autocomplete="tel" inputmode="tel" placeholder="+998 __ ___ __ __" maxlength="20" minlength="9" required></label>
<label>{e(T["f_school"])}<input name="school" autocomplete="organization" maxlength="120" required></label>
<label>{e(T["f_city"])}<input name="city" autocomplete="address-level2" maxlength="60" required></label>
<button class="btn btn-primary btn-lg" type="submit">{e(T["f_send"])}</button>
<small>{e(T["f_note"])}</small>
<div class="form-ok" id="formOk" role="status" tabindex="-1">{e(T["f_ok"])}</div>
<div class="form-err" id="formErr" role="alert">{e(T["f_err"])} <a href="tel:{e(PHONE_TEL)}">{e(PHONE)}</a></div>
</form>
</div>
</div>
</section>
'''

# ───────────────────────── pages ─────────────────────────
def home(T):
    L = T["lang"]; I = ids(T); CID = CONTACT_ID[L]
    alts = {X["lang"]: url(X) for X in LANGS}
    out = head(T, T["meta_title"], T["meta_desc"], url(T), alts, home_ld(T), f"{SITE}/assets/img/og-{L}.png")
    out += header(T, alts)
    notes = "".join(f'<li>{ic("tick")}{e(c)}</li>' for c in T["hero_note"])
    stats = "".join(f'<div class="stat"><b>{e(n)}</b><span>{e(l)}</span></div>' for n, l in T["stats"])
    values = "".join(f'<article class="val rv"><span class="vnum">0{i+1}</span><h3>{e(a)}</h3><p>{e(b)}</p></article>' for i, (a, b) in enumerate(T["values"]))
    tabs = "".join(f'<button role="tab" id="tab-{r[0]}" aria-controls="panel-{r[0]}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{e(r[1])}</button>' for i, r in enumerate(T["roles"]))
    panels = ""
    for i, (rid, name, title, items, img, alt) in enumerate(T["roles"]):
        wide = img.startswith("web")
        w, h = (1440, 900) if wide else (600, 1298)
        lis = "".join(f'<li>{ic("tick")}<span>{e(x)}</span></li>' for x in items)
        panels += f'''<div class="panel" role="tabpanel" id="panel-{rid}" aria-labelledby="tab-{rid}"{"" if i == 0 else " hidden"}>
<div><h3>{e(title)}</h3><ul class="ticks">{lis}</ul></div>
<div class="shot{" wide" if wide else ""}"><img src="/assets/img/{img}.webp" alt="{e(alt)}" width="{w}" height="{h}" loading="lazy" decoding="async"></div>
</div>'''
    bitems = "".join(f'<li>{ic("circle-check")}<div><b>{e(a)}</b> {e(b)}</div></li>' for a, b in T["brand_items"])
    sw = [("#16a34a", "#e8f6ec", "Green"), ("#0077cc", "#e6f2fb", "Blue"), ("#0B2A55", "#e7edf6", "Navy"), ("#7c3aed", "#f1eafe", "Violet"), ("#dc2626", "#fdecec", "Red"), ("#ea8a00", "#fdf2e0", "Orange")]
    swb = "".join(f'<button type="button" style="background:{c}" data-c="{c}" data-s="{s}" aria-pressed="{"true" if i == 0 else "false"}" aria-label="{n}"></button>' for i, (c, s, n) in enumerate(sw))
    nav4 = "".join(f"<span>{e(x)}</span>" for x in T["mock_nav"])
    f = T["feats"]
    small = "".join(f'<article class="tile rv"><div class="ico">{ic(k)}</div><h3>{e(a)}</h3><p>{e(b)}</p></article>' for i, (k, a, b) in enumerate(f) if i not in (1, 3))
    small += "".join(f'<article class="tile num-tile rv"><b>{e(n)}</b><p>{e(l)}</p></article>' for n, l in T["stats"][1:3])
    bento = f'''<article class="tile big rv"><div><div class="ico">{ic(f[1][0])}</div><h3>{e(f[1][1])}</h3><p>{e(f[1][2])}</p></div><div class="tile-img phone-crop"><img src="/assets/img/app-teacher.webp" alt="{e(T["roles"][1][5])}" width="600" height="1298" loading="lazy" decoding="async"></div></article>
<article class="tile big dark rv"><div><div class="ico">{ic(f[3][0])}</div><h3>{e(f[3][1])}</h3><p>{e(f[3][2])}</p></div><div class="tile-img"><img src="/assets/img/web-reports.webp" alt="{e(T["shots_web"][1])}" width="1440" height="900" loading="lazy" decoding="async"></div></article>
{small}'''
    cmp_b = "".join(f'<li>{ic("x")}<span>{e(a)}</span></li>' for a, _ in T["compare"])
    cmp_a = "".join(f'<li>{ic("tick")}<span>{e(b)}</span></li>' for _, b in T["compare"])
    sec = "".join(f'<div class="sec-item rv"><div class="ico">{ic(k)}</div><h3>{e(a)}</h3><p>{e(b)}</p></div>' for k, a, b in T["sec"])
    facts = "".join(f'<div><b>{e(a)}</b><span>{e(b)}</span></div>' for a, b in T["case_facts"])
    steps = "".join(f'<li class="rv"><span class="when">{e(w)}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>' for w, t, d in T["launch"])
    slots = "".join(f'<div class="plogo slot"><span>{e(T["partner_slot"])}</span></div>' for _ in range(3))
    faq = "".join(f'<details class="rv"{" open" if i == 0 else ""}><summary><h3>{e(q)}</h3></summary><p>{e(a)}</p></details>' for i, (q, a) in enumerate(T["faq"]))
    out += f'''<main id="main">
<section class="hero" aria-labelledby="h1">
<div class="wrap">
<p class="kicker">{e(T["hero_eyebrow"])}</p>
<h1 id="h1">{T["hero_h1"]}</h1>
<p class="sub">{e(T["hero_lead"])}</p>
<div class="cta-row center"><a class="btn btn-primary btn-lg" href="#{CID}">{e(T["mobile_cta"])}</a><a class="link-more" href="#{I[1]}">{e(T["hero_cta2"])} ›</a></div>
<ul class="notes">{notes}</ul>
</div>
<div class="stage">
<div class="browser"><div class="bar"><i></i><i></i><i></i></div><img src="/assets/img/web-dashboard.webp" alt="{e(T["shots_web"][0])}" width="1440" height="900" fetchpriority="high" decoding="async"></div>
{phone("app-parent-green", T["alt_parent_green"], "p1", True)}
{phone("app-parent-violet", T["alt_parent_violet"], "p2", True)}
</div>
</section>

<section class="answer-sec" aria-labelledby="answer-q">
<div class="wrap">
<div class="answer" id="answer"><h2 id="answer-q">{e(T["answer_q"])}</h2><p>{e(T["answer_a"])}</p></div>
<div class="stats">{stats}</div>
</div>
</section>

<section class="values" aria-labelledby="val-h">
<div class="wrap">
<div class="head center"><p class="kicker">{e(T["value_eyebrow"])}</p><h2 id="val-h">{e(T["value_h2"])}</h2></div>
<div class="val-grid">{values}</div>
</div>
</section>

<section class="brand-sec" id="{I[2]}" aria-labelledby="brand-h">
<div class="wrap">
<div class="head center"><p class="kicker">{e(T["brand_eyebrow"])}</p><h2 id="brand-h">{e(T["brand_h2"])}</h2><p class="sub">{e(T["brand_lead"])}</p></div>
<div class="brand">
<ul class="checks">{bitems}</ul>
<div class="builder">
<p class="builder-t">{e(T["builder_title"])}</p>
<label for="schoolName">{e(T["builder_name"])}</label>
<input type="text" id="schoolName" placeholder="{e(T["builder_ph"])}" maxlength="28" autocomplete="off">
<p class="builder-l">{e(T["builder_color"])}</p>
<div class="swatches">{swb}</div>
<div class="mock" id="mock" aria-live="polite">
<div class="mock-top"><div class="mock-logo" id="mockInit">{e(T["builder_default"][0])}</div><div><b id="mockName">{e(T["builder_default"])}</b><small>{e(T["mock_role"])}</small></div></div>
<h4>{e(T["mock_hello"])}</h4>
<div class="mock-row"><div class="mock-tile"><small>{e(T["mock_att"])}</small><b>100%</b></div><div class="mock-tile"><small>{e(T["mock_avg"])}</small><b>5,0</b></div><div class="mock-tile"><small>{e(T["mock_rank"])}</small><b>1/13</b></div></div>
<div class="mock-btn">{e(T["mock_btn"])}</div>
<div class="mock-nav">{nav4}</div>
</div>
</div>
</div>
</div>
</section>

<section class="gray" id="{I[0]}" aria-labelledby="feat-h">
<div class="wrap">
<div class="head center"><p class="kicker">{e(T["bento_eyebrow"])}</p><h2 id="feat-h">{e(T["bento_h2"])}</h2><p class="sub">{e(T["feat_lead"])}</p></div>
<div class="bento">{bento}</div>
</div>
</section>

<section id="{I[1]}" aria-labelledby="roles-h">
<div class="wrap">
<div class="head center"><p class="kicker">{e(T["roles_eyebrow"])}</p><h2 id="roles-h">{e(T["roles_h2"])}</h2><p class="sub">{e(T["roles_lead"])}</p></div>
<div class="tabs" role="tablist" aria-label="{e(T["roles_h2"])}">{tabs}</div>
{panels}
</div>
</section>

<section class="gray" aria-labelledby="cmp-h">
<div class="wrap">
<div class="head center"><p class="kicker">{e(T["compare_eyebrow"])}</p><h2 id="cmp-h">{e(T["compare_h2"])}</h2></div>
<div class="compare">
<div class="cmp before rv"><h3>{e(T["compare_before"])}</h3><ul>{cmp_b}</ul></div>
<div class="cmp after rv"><h3>{e(T["compare_after"])}</h3><ul>{cmp_a}</ul></div>
</div>
<div class="cta-row center" style="margin-top:40px"><a class="btn btn-primary btn-lg" href="#{CID}">{e(T["mobile_cta"])}</a></div>
</div>
</section>

<section class="black" aria-labelledby="sec-h">
<div class="wrap">
<div class="head center"><p class="kicker">{e(T["sec_eyebrow"])}</p><h2 id="sec-h">{e(T["sec_h2"])}</h2><p class="sub">{e(T["sec_lead"])}</p></div>
<div class="sec-grid">{sec}</div>
</div>
</section>

<section id="{I[3]}" aria-labelledby="case-h">
<div class="wrap">
<div class="case-card">
<div class="case-txt">
<p class="kicker">{e(T["case_eyebrow"])}</p>
<img class="case-logo" src="/assets/img/steam-plaza-logo.webp" alt="Steam Plaza" width="240" height="125" loading="lazy">
<h2 id="case-h">{e(T["case_h2"])}</h2>
<p class="sub">{e(T["case_lead"])}</p>
<div class="facts">{facts}</div>
<a class="link-more" href="{PREFIX[L]}{CASE_SLUG}">{e(T["case_more"])} ›</a>
</div>
<div class="case-phones">
{phone("app-teacher", T["roles"][1][5], "p1")}
{phone("app-award", T["c_gal"][1][1], "p2")}
</div>
</div>
</div>
</section>

<section class="gray" id="{I[6]}" aria-labelledby="partners-h">
<div class="wrap">
<div class="head center"><p class="kicker">{e(T["partners_eyebrow"])}</p><h2 id="partners-h">{e(T["partners_h2"])}</h2><p class="sub">{e(T["partners_lead"])}</p></div>
<div class="partners">
<div class="plogo"><img src="/assets/img/steam-plaza-logo.webp" alt="Steam Plaza" width="240" height="125" loading="lazy"><span>Steam Plaza</span></div>
{slots}
</div>
<div class="pprog rv"><div><h3>{e(T["partner_prog_h3"])}</h3><p>{e(T["partner_prog_p"])}</p></div><a class="btn btn-dark btn-lg" href="#{CID}" data-type="partner">{e(T["partner_cta"])}</a></div>
</div>
</section>

<section aria-labelledby="launch-h">
<div class="wrap">
<div class="head center"><p class="kicker">{e(T["launch_eyebrow"])}</p><h2 id="launch-h">{e(T["launch_h2"])}</h2></div>
<ol class="steps">{steps}</ol>
<p class="note">{ic("tick")} {e(T["launch_note"])}</p>
</div>
</section>

<section id="{I[5]}" aria-labelledby="faq-h">
<div class="wrap">
<div class="head center"><p class="kicker">{e(T["faq_eyebrow"])}</p><h2 id="faq-h">{e(T["faq_h2"])}</h2></div>
<div class="faq">{faq}</div>
</div>
</section>

{lead_section(T)}
</main>
'''
    out += footer(T)
    return out

def case(T):
    L = T["lang"]
    alts = {X["lang"]: url(X, True) for X in LANGS}
    out = head(T, T["c_title"], T["c_desc"], url(T, True), alts, case_ld(T), f"{SITE}/assets/img/og-{L}.png")
    out += header(T, alts, on_home=False)
    secs = ""
    for h, ps in T["c_sections"]:
        if len(ps) > 1:
            secs += f'<h2>{e(h)}</h2><ul>' + "".join(f"<li>{e(p)}</li>" for p in ps) + "</ul>"
        else:
            secs += f'<h2>{e(h)}</h2><p>{e(ps[0])}</p>'
    mods = "".join(f'<li>{e(m)}</li>' for m in T["c_mods"])
    rows = "".join(f'<tr><th scope="row">{e(a)}</th><td>{e(b)}</td></tr>' for a, b in T["c_tech"])
    gal_ph = "".join(f'<figure><img src="/assets/img/{i}.webp" alt="{e(c)}" width="600" height="1298" loading="lazy" decoding="async"><figcaption>{e(c)}</figcaption></figure>' for i, c in T["c_gal"] if i.startswith("app"))
    gal_web = "".join(f'<figure><img src="/assets/img/{i}.webp" alt="{e(c)}" width="1440" height="900" loading="lazy" decoding="async"><figcaption>{e(c)}</figcaption></figure>' for i, c in T["c_gal"] if i.startswith("web"))
    out += f'''<main id="main">
<div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="{PREFIX[L]}">{e(T["c_crumb_home"])}</a></li><li aria-current="page">{e(T["c_crumb"])}</li></ol></nav></div>
<section style="padding-top:32px">
<div class="wrap">
<article class="prose">
<div class="case-logo"><img src="/assets/img/steam-plaza-logo.webp" alt="Steam Plaza" width="240" height="125"></div>
<h1>{e(T["c_h1"])}</h1>
<p class="lead">{e(T["c_lead"])}</p>
<div class="facts">{"".join(f'<div><b>{e(a)}</b><span>{e(b)}</span></div>' for a, b in T["case_facts"])}</div>
{secs}
<h2>{e(T["c_mod_h2"])}</h2><ul>{mods}</ul>
<h2>{e(T["c_tech_h2"])}</h2>
<div class="table-wrap"><table class="table"><tbody>{rows}</tbody></table></div>
</article>
<h2 style="margin-top:56px">{e(T["c_gal_h2"])}</h2>
<div class="shots" style="grid-template-columns:repeat(auto-fit,minmax(200px,1fr))">{gal_ph}</div>
<div class="shots" style="margin-top:20px">{gal_web}</div>
</div>
</section>
<section class="alt"><div class="wrap head center" style="margin-bottom:0">
<h2>{e(T["c_cta_h2"])}</h2><p class="lead">{e(T["c_cta_p"])}</p>
<div class="cta-row" style="justify-content:center"><a class="btn btn-primary" href="{PREFIX[L]}#{CONTACT_ID[L]}">{e(T["demo"])} {ic("arrow")}</a></div>
</div></section>
</main>
'''
    out += footer(T)
    return out

def notfound():
    T = UZ
    alts = {X["lang"]: url(X) for X in LANGS}
    o = head(T, "404 — " + T["nf_title"], T["nf_p"], url(T), alts, {"@context": "https://schema.org", **org_ld()}, f"{SITE}/assets/img/og-uz.png")
    o = o.replace('content="index, follow, max-image-preview:large, max-snippet:-1"', 'content="noindex"')
    o += header(T, alts, on_home=False)
    o += f'''<main id="main"><section><div class="wrap head center">
<h1>404</h1>
<p class="lead">{e(UZ["nf_p"])}<br>{e(RU["nf_p"])}<br>{e(EN["nf_p"])}</p>
<div class="cta-row" style="justify-content:center"><a class="btn btn-primary" href="/">{e(UZ["nf_btn"])}</a><a class="btn btn-ghost" href="/ru/">{e(RU["nf_btn"])}</a><a class="btn btn-ghost" href="/en/">{e(EN["nf_btn"])}</a></div>
</div></section></main>'''
    return o + footer(T)

# ───────────────────────── SEO files ─────────────────────────
def sitemap():
    xs = []
    for case_ in (False, True):
        for T in LANGS:
            alts = "".join(f'<xhtml:link rel="alternate" hreflang="{X["lang"]}" href="{url(X, case_)}"/>' for X in LANGS)
            alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{url(UZ, case_)}"/>'
            xs.append(f'<url><loc>{url(T, case_)}</loc><lastmod>{TODAY}</lastmod>{alts}</url>')
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(xs) + "\n</urlset>\n"

def robots():
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User", "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot-Extended", "YandexBot", "Bingbot"]
    s = "# EduWay — all content is public; AI assistants and search engines are welcome.\nUser-agent: *\nAllow: /\n\n"
    s += "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots)
    return s + f"Sitemap: {SITE}/sitemap.xml\n"

def llms():
    T = UZ; E = EN
    contacts = [f"- Phone: {PHONE_TEL}" if PHONE_TEL else "", f"- Telegram: https://t.me/{TELEGRAM}" if TELEGRAM else "", f"- Email: {EMAIL}" if EMAIL else ""]
    contacts = "\n".join(c for c in contacts if c) or "- Contact: see the demo request form on the website"
    feats = "\n".join(f"- {a}: {b}" for _, a, b in E["feats"])
    roles = "\n".join(f"- {r[1]}: " + "; ".join(r[3]) for r in E["roles"])
    faq = "\n\n".join(f"### {q}\n{a}" for q, a in E["faq"])
    return f"""# EduWay

> {E["answer_a"]}

EduWay (EduWay Education Platform) is a white-label school management SaaS from Uzbekistan. Every client school gets its own branded version: the school's logo, colors, name and domain, plus a separate iOS and Android app in the App Store and Google Play under the school's name. The platform interface and PDF reports are in Uzbek (Latin) and Russian. Launch takes about 10 business days.

## Pages
- [EduWay — home (Uzbek)]({url(UZ)}): {UZ["meta_desc"]}
- [EduWay — home (Russian)]({url(RU)}): {RU["meta_desc"]}
- [EduWay — home (English)]({url(EN)}): {EN["meta_desc"]}
- [Steam Plaza case study (Uzbek)]({url(UZ, True)}): {UZ["c_desc"]}
- [Steam Plaza case study (Russian)]({url(RU, True)}): {RU["c_desc"]}
- [Steam Plaza case study (English)]({url(EN, True)}): {EN["c_desc"]}

## Key facts
- Product type: school and kindergarten management platform (SaaS), white-label
- Platforms: Web, Android, iOS (one codebase)
- Roles: principal/owner, manager, accountant, teacher, parent — each with its own dashboard and permissions
- Multi-branch: several branches per organisation, each with a school and kindergarten section
- Languages: Uzbek (Latin) and Russian (interface and PDF reports)
- Security: AES-256-GCM encryption of files and personal fields, scrypt password hashing, brute-force lockout, rate limiting, audit log, HTTPS/HSTS, strict CSP, daily backups; hosting in Uzbekistan is possible
- Launch: ~10 business days (discovery, branding and setup, data import, staff training)
- Pricing: calculated individually per school — request a quote via the form on the website (name, phone, school, city); all modules and support included
- First client: Steam Plaza (2 branches, school + kindergarten, 5 roles, Web + Android + iOS)

## Roles
{roles}

## Features
{feats}

## FAQ
{faq}

## Contact
{contacts}
- Region: Uzbekistan
"""

def manifest():
    return json.dumps({"name": "EduWay — Education Platform", "short_name": "EduWay", "start_url": "/", "display": "standalone",
        "background_color": "#ffffff", "theme_color": "#0B2A55", "lang": "uz",
        "icons": [{"src": "/assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}]}, ensure_ascii=False, indent=1)

def og_images(out):
    from PIL import Image, ImageDraw, ImageFont
    def font(sz, bold=True, L="uz"):
        p = os.path.join(out, "assets/fonts/manrope-%s.woff2" % ("cyrillic" if L == "ru" else "latin"))
        try:
            f = ImageFont.truetype(p, sz)
            f.set_variation_by_axes([800 if bold else 500])
            return f
        except Exception:
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", sz)
    logo = Image.open(os.path.join(out, "assets/img/eduway-logo-white.png")).convert("RGBA")
    logo = logo.resize((380, int(380 * logo.height / logo.width)), Image.LANCZOS)
    ph = Image.open(os.path.join(out, "assets/img/app-parent-green.webp")).convert("RGB")
    ph2 = Image.open(os.path.join(out, "assets/img/app-parent-violet.webp")).convert("RGB")
    titles = {"uz": "Maktabingizning oʻz brendidagi\nraqamli platformasi", "ru": "Цифровая платформа\nпод брендом вашей школы", "en": "A school platform\nunder your own brand"}
    subs = {"uz": "Davomat · baho · uy vazifasi · moliya · iOS, Android, Web", "ru": "Посещаемость · оценки · ДЗ · финансы · iOS, Android, Web", "en": "Attendance · grades · homework · finance · iOS, Android, Web"}
    for L in ("uz", "ru", "en"):
        im = Image.new("RGB", (1200, 630), (11, 42, 85))
        d = ImageDraw.Draw(im)
        for r in range(420, 0, -6):
            a = int(40 * (1 - r / 420))
            d.ellipse((1050 - r, -120 - r, 1050 + r, -120 + r), fill=(11 + a // 2, 42 + a * 2, 85 + a * 3))
        im.paste(logo, (64, 60), logo)
        d.multiline_text((64, 230), titles[L], font=font(54, True, L), fill="white", spacing=10)
        d.text((64, 420), subs[L], font=font(24, False, L), fill=(181, 198, 222))
        d.rounded_rectangle((64, 500, 64 + 330, 556), radius=28, fill=(0, 174, 239))
        d.text((64 + 165, 528), {"uz": "Bepul demo", "ru": "Бесплатное демо", "en": "Free demo"}[L], font=font(26, True, L), fill="white", anchor="mm")
        for i, p in enumerate((ph, ph2)):
            t = p.resize((230, int(230 * p.height / p.width))).crop((0, 0, 230, 470))
            frame = Image.new("RGB", (246, 486), (13, 27, 46)); frame.paste(t, (8, 8))
            mask = Image.new("L", frame.size, 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0) + frame.size, radius=34, fill=255)
            im.paste(frame, (800 + i * 150, 110 + (0 if i else 60)), mask)
        im.save(os.path.join(out, f"assets/img/og-{L}.png"), optimize=True)

def main(out):
    here = os.path.dirname(os.path.abspath(__file__))
    for T in LANGS:
        d = os.path.join(out, PREFIX[T["lang"]].strip("/"))
        os.makedirs(os.path.join(d, "steam-plaza"), exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(home(T))
        open(os.path.join(d, "steam-plaza", "index.html"), "w", encoding="utf-8").write(case(T))
    w = lambda n, s: open(os.path.join(out, n), "w", encoding="utf-8").write(s)
    w("404.html", notfound()); w("sitemap.xml", sitemap()); w("robots.txt", robots()); w("llms.txt", llms()); w("site.webmanifest", manifest())
    og_images(out)
    print("built →", out)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "dist")
