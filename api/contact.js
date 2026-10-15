// Vercel serverless function: POST /api/contact
// Sends the website's quote/contact form to the UX Labs Pro inbox through Resend.
//
// Environment variables (set in Vercel → Project → Settings → Environment Variables):
//   RESEND_API_KEY  (required)  your Resend API key
//   CONTACT_TO      (optional)  where inquiries go            — default: hello@uxlabs.pro
//   CONTACT_FROM    (optional)  the sender, on a domain verified in Resend
//                               — default: "UX Labs Pro Website <hello@uxlabs.pro>"
// RESEND_TO / RESEND_FROM (or CONTACT_TO_EMAIL / CONTACT_FROM_EMAIL) are accepted as alternative names.

const env = (...names) => names.map((n) => process.env[n]).find((v) => v && String(v).trim());

const LIMITS = { name: 120, email: 200, phone: 40, service: 80, message: 5000 };
const SERVICES = ['', 'Custom Web Design', 'Website Development', 'SEO & Optimization', 'Website Maintenance'];

const escapeHtml = (s) =>
  String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const oneLine = (s) => String(s).replace(/[\r\n]+/g, ' ').trim();
const isEmail = (s) => /^[^\s@<>()[\],;:"]+@[^\s@<>()[\],;:"]+\.[^\s@<>()[\],;:"]{2,}$/.test(s);

async function readBody(req) {
  if (req.body && typeof req.body === 'object') return req.body;
  if (typeof req.body === 'string') return JSON.parse(req.body || '{}');
  const chunks = [];
  for await (const c of req) chunks.push(c);
  const raw = Buffer.concat(chunks).toString('utf8');
  return raw ? JSON.parse(raw) : {};
}

module.exports = async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ ok: false, error: 'Method not allowed' });
  }

  let body;
  try { body = await readBody(req); } catch { return res.status(400).json({ ok: false, error: 'Invalid request' }); }

  // Spam trap: real visitors never see or fill this field.
  if (body.company) return res.status(200).json({ ok: true });

  const data = {};
  for (const k of Object.keys(LIMITS)) data[k] = typeof body[k] === 'string' ? body[k].trim() : '';
  data.name = oneLine(data.name); data.email = oneLine(data.email); data.phone = oneLine(data.phone);

  if (!data.name || !data.email || !data.message) return res.status(400).json({ ok: false, error: 'Please fill in your name, email and message.' });
  if (!isEmail(data.email)) return res.status(400).json({ ok: false, error: 'Please enter a valid email address.' });
  for (const [k, max] of Object.entries(LIMITS)) {
    if (data[k].length > max) return res.status(400).json({ ok: false, error: 'One of the fields is too long.' });
  }
  if (!SERVICES.includes(data.service)) data.service = '';

  const apiKey = env('RESEND_API_KEY');
  if (!apiKey) {
    console.error('[contact] RESEND_API_KEY is not set');
    return res.status(500).json({ ok: false, error: 'Email is not configured yet.' });
  }
  const to = env('CONTACT_TO', 'RESEND_TO', 'CONTACT_TO_EMAIL') || 'hello@uxlabs.pro';
  const from = env('CONTACT_FROM', 'RESEND_FROM', 'CONTACT_FROM_EMAIL') || 'UX Labs Pro Website <hello@uxlabs.pro>';

  const rows = [
    ['Name', data.name],
    ['Email', data.email],
    ['Phone', data.phone || '—'],
    ['Interested in', data.service || 'Not sure yet'],
  ];
  const html = `<!doctype html><html><body style="margin:0;padding:24px;background:#fdf0f7;font-family:Arial,Helvetica,sans-serif;color:#2f1030">
  <table role="presentation" width="100%" style="max-width:600px;margin:0 auto;background:#ffffff;border-radius:16px;overflow:hidden;border:1px solid #f5d9e8">
    <tr><td style="padding:22px 28px;background:linear-gradient(95deg,#ec3a97,#9d47ea);color:#ffffff">
      <div style="font-size:12px;letter-spacing:2px;text-transform:uppercase;opacity:.85">New website inquiry</div>
      <div style="font-size:22px;font-weight:bold;margin-top:4px">${escapeHtml(data.name)}</div>
    </td></tr>
    <tr><td style="padding:22px 28px">
      <table role="presentation" width="100%" style="font-size:14px;line-height:1.5">
        ${rows.map(([k, v]) => `<tr><td style="padding:6px 0;width:130px;color:#7d5a76;vertical-align:top">${k}</td><td style="padding:6px 0;font-weight:bold">${
          k === 'Email' ? `<a href="mailto:${escapeHtml(v)}" style="color:#9d47ea">${escapeHtml(v)}</a>` : escapeHtml(v)}</td></tr>`).join('')}
      </table>
      <div style="margin-top:18px;padding:16px 18px;background:#fbf4fa;border-radius:12px;font-size:15px;line-height:1.6;white-space:pre-wrap">${escapeHtml(data.message)}</div>
      <p style="margin:18px 0 0;font-size:12px;color:#7d5a76">Reply to this email to answer ${escapeHtml(data.name)} directly.</p>
    </td></tr>
  </table></body></html>`;
  const text = `New website inquiry\n\n${rows.map(([k, v]) => `${k}: ${v}`).join('\n')}\n\nMessage:\n${data.message}\n`;

  try {
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${apiKey}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from,
        to: to.split(',').map((s) => s.trim()).filter(Boolean),
        reply_to: data.email,
        subject: `New inquiry from ${data.name}${data.service ? ` — ${data.service}` : ''}`,
        html,
        text,
      }),
    });
    if (!r.ok) {
      console.error('[contact] Resend error', r.status, await r.text());
      return res.status(502).json({ ok: false, error: 'We could not send your message right now.' });
    }
    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('[contact] Request failed', err);
    return res.status(502).json({ ok: false, error: 'We could not send your message right now.' });
  }
};
