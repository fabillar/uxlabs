p='index.html'; s=open(p,encoding='utf-8').read()
a=s.index('<!-- ===== Services ===== -->'); b=s.index('<!-- ===== Process')
cards=[('sv-c1','design','Custom Web Design','Custom<br>Web Design','Modern, beautiful designs tailored to your brand.'),
       ('sv-c2','dev','Website Development','Website<br>Development','Fast, secure, and scalable websites built to perform.'),
       ('sv-c3','seo','SEO &amp; Optimization','SEO &amp;<br>Optimization','Help your business get found and grow online.'),
       ('sv-c4','maint','Website Maintenance','Website<br>Maintenance','Keep your website secure, updated, and running smoothly.')]
items='\n'.join(f'''      <a class="sv-card {c} reveal" href="#contact" data-service="{svc}" style="--d:{.04+i*.06:.2f}s">
        <span class="sv-icon"><img src="assets/service-{ic}.png" alt="" width="320" height="320" loading="lazy"></span>
        <h3>{t}</h3>
        <p>{d}</p>
        <span class="sv-bar" aria-hidden="true"></span>
        <span class="sv-more">Learn More <span class="sv-go"><svg class="ic"><use href="#i-arrow"/></svg></span></span>
      </a>''' for i,(c,ic,svc,t,d) in enumerate(cards))
html=f'''<!-- ===== Services ===== -->
<section class="services" id="services">
  <span class="deco sv-blob a" aria-hidden="true"></span><span class="deco sv-blob b" aria-hidden="true"></span><span class="deco sv-blob c" aria-hidden="true"></span>
  <svg class="sp" viewBox="0 0 24 24" aria-hidden="true" style="left:4%;top:8%;--s:22;--c:#ec3a97;--dl:0s;--dur:3.2s"><use href="#sparkle"/></svg>
  <svg class="sp xm" viewBox="0 0 24 24" aria-hidden="true" style="left:44%;top:6%;--s:14;--c:#ffb020;--dl:0.8s;--dur:2.7s"><use href="#sparkle"/></svg>
  <svg class="sp" viewBox="0 0 24 24" aria-hidden="true" style="left:2%;top:58%;--s:16;--c:#9d47ea;--dl:1.0s;--dur:3.0s"><use href="#sparkle"/></svg>
  <svg class="sp" viewBox="0 0 24 24" aria-hidden="true" style="left:97%;top:66%;--s:22;--c:#ec3a97;--dl:0.2s;--dur:3.3s"><use href="#sparkle"/></svg>
  <svg class="sp xm" viewBox="0 0 24 24" aria-hidden="true" style="left:12%;top:96%;--s:18;--c:#9d47ea;--dl:0.6s;--dur:3.4s"><use href="#sparkle"/></svg>
  <i class="sd xm" aria-hidden="true" style="left:41%;top:12%;--s:9;--c:#c9a6ff;--dl:0.3s;--dur:2.7s"></i>
  <div class="wrap">
    <div class="sv-head">
      <div class="sv-copy reveal">
        <span class="sv-pill">Our Services</span>
        <h2>Everything you need to create a <span class="grad">powerful online presence.</span></h2>
        <p>From design to development and beyond, we provide end-to-end website solutions to help your business grow and stand out online.</p>
      </div>
      <div class="sv-art reveal" style="--d:.1s"><img src="assets/services-hero.webp" alt="UX Labs Pro designer building a website on a laptop" width="1100" height="669" fetchpriority="low" loading="lazy"></div>
    </div>
    <div class="sv-grid">
{items}
    </div>
  </div>
</section>

'''
s=s[:a]+html+s[b:]
ca=s.index('/* ---------- Services ---------- */'); cb=s.index('/* ---------- Process ---------- */')
css=r'''/* ---------- Services ---------- */
.services{ padding-block:clamp(48px,7vw,90px) clamp(48px,6vw,80px); }
.services .wrap{ max-width:1360px; }
.services .sv-blob{ z-index:-1; }
.services .sv-blob.a{ left:-10%; top:22%; width:clamp(220px,26vw,380px); aspect-ratio:.95; border-radius:58% 42% 50% 50% / 46% 56% 44% 54%; background:linear-gradient(160deg, color-mix(in srgb, var(--lavender) 40%, transparent), color-mix(in srgb, var(--pink) 18%, transparent)); animation:jello-c 12s ease-in-out -3s infinite; }
.services .sv-blob.b{ right:-6%; top:4%; width:clamp(260px,34vw,520px); aspect-ratio:1.2; border-radius:44% 56% 60% 40% / 52% 40% 60% 48%; background:radial-gradient(circle at 45% 45%, color-mix(in srgb, var(--lavender) 34%, transparent), color-mix(in srgb, var(--pink) 16%, transparent) 70%, transparent 74%); animation:jello-a 13s ease-in-out -6s infinite; }
.services .sv-blob.c{ right:-5%; bottom:2%; width:clamp(160px,18vw,260px); aspect-ratio:1.1; border-radius:62% 38% 42% 58% / 40% 60% 40% 60%; background:linear-gradient(200deg, color-mix(in srgb, var(--purple) 20%, transparent), color-mix(in srgb, var(--lavender) 34%, transparent)); animation:jello-b 10s ease-in-out -2s infinite; }
/* two-column intro: copy left, illustration right */
.sv-head{ display:grid; grid-template-columns:minmax(0,1fr) minmax(0,1.05fr); align-items:center; gap:clamp(20px,4vw,60px); margin-bottom:clamp(26px,3.6vw,48px); }
.sv-copy{ display:flex; flex-direction:column; align-items:flex-start; gap:clamp(14px,1.8vw,22px); }
.sv-pill{ display:inline-flex; align-items:center; gap:10px; padding:9px 20px; border-radius:999px; font-size:clamp(11px,1.1vw,13px); font-weight:700; letter-spacing:.22em; text-transform:uppercase; color:var(--purple);
  background:color-mix(in srgb, var(--lavender) 18%, var(--card)); }
.sv-pill::before{ content:""; width:7px; height:7px; border-radius:50%; background:var(--magenta); }
.sv-copy h2{ font-size:clamp(32px,4.2vw,58px); font-weight:800; letter-spacing:-.035em; line-height:1.08; text-wrap:balance; }
.sv-copy h2 .grad{ background:linear-gradient(95deg,#ec3a97 0%,#c147d6 50%,#9d47ea 100%); -webkit-background-clip:text; background-clip:text; color:transparent; padding-right:.04em; -webkit-box-decoration-break:clone; box-decoration-break:clone; }
.sv-copy p{ font-size:clamp(15px,1.5vw,19px); line-height:1.65; max-width:44ch; color:color-mix(in srgb, var(--text) 72%, var(--text-dim)); }
.sv-art img{ width:100%; height:auto; filter:drop-shadow(0 20px 30px rgba(var(--shadow),.18)); animation:pf-bob 6s ease-in-out infinite; }
/* service cards */
.sv-grid{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:clamp(16px,1.8vw,26px); position:relative; z-index:1; }
.sv-card{ position:relative; display:flex; flex-direction:column; align-items:flex-start; padding:clamp(22px,2.2vw,34px) clamp(20px,2.2vw,34px) clamp(22px,2vw,30px); border-radius:26px;
  background:linear-gradient(165deg, color-mix(in srgb, var(--card) 92%, transparent), color-mix(in srgb, var(--acc) 9%, var(--card))); border:1.5px solid color-mix(in srgb, var(--acc) 16%, transparent);
  box-shadow:0 26px 50px -32px rgba(var(--shadow),.45); color:var(--text);
  transition:opacity .8s var(--ease) var(--d,0s), transform .8s var(--ease) var(--d,0s), translate .45s var(--ease), box-shadow .45s var(--ease), border-color .45s var(--ease); }
.sv-card:hover{ translate:0 -6px; border-color:color-mix(in srgb, var(--acc) 40%, transparent); box-shadow:0 36px 60px -30px rgba(var(--shadow),.6); }
.sv-icon{ position:relative; align-self:center; width:min(190px,78%); aspect-ratio:1.25; display:flex; align-items:center; justify-content:center; margin-bottom:clamp(8px,1vw,14px); }
.sv-icon::before{ content:""; position:absolute; left:50%; top:50%; width:78%; aspect-ratio:1; translate:-50% -50%; border-radius:50%; background:color-mix(in srgb, var(--acc) 13%, transparent); }
.sv-icon img{ position:relative; width:86%; height:auto; transition:transform .5s var(--ease); }
.sv-card:hover .sv-icon img{ transform:scale(1.06) rotate(-3deg); }
.sv-card h3{ font-size:clamp(20px,1.75vw,27px); font-weight:800; letter-spacing:-.02em; line-height:1.18; margin-bottom:10px; }
.sv-card p{ font-size:clamp(14px,1.15vw,16.5px); line-height:1.6; color:color-mix(in srgb, var(--text) 70%, var(--text-dim)); flex:1; max-width:26ch; }
.sv-bar{ width:48px; height:4px; border-radius:4px; background:var(--acc); margin:clamp(18px,1.8vw,26px) 0 clamp(16px,1.6vw,22px); }
.sv-more{ display:inline-flex; align-items:center; gap:16px; font-weight:600; font-size:clamp(15px,1.2vw,17px); }
.sv-go{ width:50px; height:50px; border-radius:50%; display:flex; align-items:center; justify-content:center; color:var(--acc); background:color-mix(in srgb, var(--acc) 15%, var(--card)); transition:background .3s, color .3s, transform .35s var(--ease); }
.sv-go .ic{ width:20px; height:20px; stroke-width:2.4; }
.sv-card:hover .sv-go{ background:var(--acc); color:#fff; transform:translateX(4px); }
.sv-c1{ --acc:#ec3a97; } .sv-c2{ --acc:#4d7bff; } .sv-c3{ --acc:#f5a524; } .sv-c4{ --acc:#9d47ea; }
@media (max-width:1100px){ .sv-grid{ grid-template-columns:repeat(2,minmax(0,1fr)); } .sv-icon{ width:min(170px,60%); } }
@media (max-width:820px){ .sv-head{ grid-template-columns:1fr; } .sv-copy{ align-items:center; text-align:center; } .sv-copy p{ margin-inline:auto; } .sv-art{ max-width:560px; margin-inline:auto; width:100%; } }
@media (max-width:520px){ .sv-grid{ grid-template-columns:1fr; } .sv-card{ align-items:center; text-align:center; } .sv-card p{ margin-inline:auto; } }
@media (prefers-reduced-motion: reduce){ .sv-art img{ animation:none; } .sv-card, .sv-icon img{ transition:none; } }

'''
s=s[:ca]+css+s[cb:]
s=s.replace('.services .deco.blob-r{ animation:jello-b 12s ease-in-out -2s infinite; }\n','')
open(p,'w',encoding='utf-8',newline='').write(s); print('ok')
