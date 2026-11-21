// Vercel serverless function: receives the "Get a price" lead form and forwards it to Telegram.
// Required env vars (Vercel → Project → Settings → Environment Variables):
//   TELEGRAM_BOT_TOKEN — token from @BotFather
//   TELEGRAM_CHAT_ID   — chat/group id that receives leads (e.g. -1001234567890)
const LIMIT = { name: 80, phone: 20, school: 120, city: 60, lang: 2, page: 80 };
const hits = new Map(); // best-effort per-instance rate limit

const clean = (v, n) => String(v ?? "").replace(/[\u0000-\u001f\u007f]/g, " ").trim().slice(0, n);
const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  // One-time setup helper: while TELEGRAM_CHAT_ID is not set, GET /api/lead?setup=1 lists the chats
  // that have written to the bot, so the owner can copy the right chat id. Disabled once the id is set.
  if (req.method === "GET" && String(req.url || "").includes("setup=1")) {
    const t = process.env.TELEGRAM_BOT_TOKEN;
    if (!t) return res.status(200).json({ step: "TELEGRAM_BOT_TOKEN is not set yet" });
    if (process.env.TELEGRAM_CHAT_ID) return res.status(404).json({ error: "disabled" });
    try {
      const r = await fetch(`https://api.telegram.org/bot${t}/getUpdates`);
      const j = await r.json();
      const chats = {};
      for (const u of j.result || []) {
        const c = (u.message || u.channel_post || u.my_chat_member || {}).chat;
        if (c) chats[c.id] = c.title || [c.first_name, c.last_name].filter(Boolean).join(" ") || c.username || c.type;
      }
      return res.status(200).json({ hint: "Write /start to the bot, then reload. Copy the id into TELEGRAM_CHAT_ID.", chats });
    } catch (e) { return res.status(502).json({ error: "telegram" }); }
  }
  if (req.method !== "POST") { res.setHeader("Allow", "POST"); return res.status(405).json({ error: "method" }); }

  const ip = String(req.headers["x-forwarded-for"] || "").split(",")[0].trim() || "?";
  const now = Date.now(), list = (hits.get(ip) || []).filter((t) => now - t < 10 * 60e3);
  if (list.length >= 5) return res.status(429).json({ error: "rate" });
  list.push(now); hits.set(ip, list);

  let b = req.body;
  if (typeof b === "string") { try { b = JSON.parse(b); } catch { b = {}; } }
  b = b || {};
  if (b.website) return res.status(200).json({ ok: true }); // honeypot: silently drop bots

  const f = Object.fromEntries(Object.entries(LIMIT).map(([k, n]) => [k, clean(b[k], n)]));
  const digits = f.phone.replace(/\D/g, "");
  if (!f.name || !f.school || !f.city || digits.length < 9 || digits.length > 15) {
    return res.status(400).json({ error: "invalid" });
  }

  const token = process.env.TELEGRAM_BOT_TOKEN, chat = process.env.TELEGRAM_CHAT_ID;
  if (!token || !chat) { console.error("lead: Telegram env vars missing", f); return res.status(503).json({ error: "not_configured" }); }

  const text = [
    "🆕 <b>EduWay — yangi lead (narx soʻrovi)</b>",
    `👤 Ism: ${esc(f.name)}`,
    `📞 Telefon: ${esc(f.phone)}`,
    `🏫 Maktab: ${esc(f.school)}`,
    `📍 Shahar: ${esc(f.city)}`,
    `🌐 Til: ${esc(f.lang || "-")} · Sahifa: ${esc(f.page || "/")}`,
  ].join("\n");

  try {
    const r = await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ chat_id: chat, text, parse_mode: "HTML", disable_web_page_preview: true }),
    });
    if (!r.ok) { console.error("lead: telegram", r.status, await r.text()); return res.status(502).json({ error: "telegram" }); }
    return res.status(200).json({ ok: true });
  } catch (e) {
    console.error("lead: fetch failed", e);
    return res.status(502).json({ error: "network" });
  }
};
