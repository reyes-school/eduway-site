# EduWay — marketing veb-sayti

Statik sayt (HTML + CSS + JS, freymvorksiz). 3 til: oʻzbekcha (asosiy, `/`), ruscha (`/ru/`), inglizcha (`/en/`).

## Tuzilma
- `site/` — tayyor statik sayt
- `api/lead.js` — lead formani Telegram'ga yuboruvchi funksiya
- `src/build.py` — generator. Matnlar: `src/content_uz.py`, `content_ru.py`, `content_en.py`

## Sozlash (src/build.py → CONFIG)
- `SITE` — domen (hozir `https://eduway.uz`), `PHONE` — +998 77 007 76 56, `TELEGRAM`, `EMAIL`
- Matnni oʻzgartirgach: `npm run build:site` (yoki `python3 src/build.py site`, Pillow kerak) va commit qiling

## Lead forma (Narxni bilish)
Forma `POST /api/lead` ga yuboradi (`api/lead.js`, Vercel funksiyasi) va leadni Telegram'ga joʻnatadi.
Vercel → Project → Settings → Environment Variables:
- `TELEGRAM_BOT_TOKEN` — @BotFather bergan token
- `TELEGRAM_CHAT_ID` — leadlar tushadigan chat/guruh ID
Oʻzgaruvchilar qoʻshilgach, Redeploy qiling.

## Joylash
GitHub repo Vercel'ga import qilinadi: Framework = Other, build yoʻq, output = `site` (vercel.json'da yozilgan). Har push avtomatik deploy boʻladi.

## Lokal koʻrish
`cd site && python3 -m http.server 8000` → http://localhost:8000

## SEO / GEO / AEO
- Har sahifada: title, description, canonical, hreflang (uz/ru/en + x-default), Open Graph, Twitter card
- JSON-LD: Organization, WebSite, WebPage (+speakable), SoftwareApplication, Product, Service, FAQPage; keys sahifasida Article + BreadcrumbList
- `sitemap.xml` (hreflang bilan), `robots.txt` (AI botlarga ruxsat), `llms.txt`, `site.webmanifest`, OG rasmlar (3 tilda)
- “EduWay nima?” qisqa javob bloki, 12 ta savol-javob, semantik HTML (bitta h1, landmark’lar, ARIA tabs)
- Tezlik: shriftlar oʻzimizda (woff2), rasmlar WebP + lazy-load, JS ~4 KB, CSS ~15 KB

