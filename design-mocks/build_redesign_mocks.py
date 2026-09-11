"""Build one self-contained HTML file with five redesign directions for mussejusse.com.

Each direction is rendered live in a desktop (1440x1000) and mobile (390x844) stage
using container query units, so the mockups are real HTML/CSS rather than images.
Fonts are embedded as woff2 so the published document needs no network.
"""

from pathlib import Path
import base64
import math

ROOT = Path(__file__).resolve().parent
FONTS = ROOT / "redesign-assets" / "fonts"


def font(name, path, weight="400", style="normal"):
    data = base64.b64encode((FONTS / path).read_bytes()).decode()
    return (
        "@font-face{font-family:'%s';font-style:%s;font-weight:%s;font-display:swap;"
        "src:url(data:font/woff2;base64,%s) format('woff2')}" % (name, style, weight, data)
    )


FONT_CSS = "".join(
    [
        font("Space Grotesk", "SpaceGrotesk.woff2", "300 700"),
        font("Space Mono", "SpaceMono-Regular.woff2", "400"),
        font("Space Mono", "SpaceMono-Bold.woff2", "700"),
        font("DM Serif Display", "DMSerif-Regular.woff2", "400"),
        font("DM Serif Display", "DMSerif-Italic.woff2", "400", "italic"),
        font("Anton", "Anton.woff2", "400"),
        font("Inter", "Inter.woff2", "100 900"),
    ]
)

GH = "https://github.com/MusseJusse"
BS = "https://bsky.app/profile/mussejusse.com"
R = "https://roundest.mussejusse.com"
M = "https://models.mussejusse.com"


def a(url, inner, cls=""):
    c = ' class="%s"' % cls if cls else ""
    return '<a%s href="%s">%s</a>' % (c, url, inner)


GH_LINK = a(GH, "GitHub", "mono")
BS_LINK = a(BS, "Bluesky", "mono")

# ---------------------------------------------------------------- shared stage

STAGE_CSS = """
.canvas{container-type:inline-size;width:100%;overflow:hidden;position:relative;background:#000;box-shadow:inset 0 0 0 1px #26262a}
.site{width:100%;position:relative;overflow:hidden;font-size:1.25cqw;line-height:1.45;-webkit-font-smoothing:antialiased}
.desktop .site{height:69.4444cqw}
.mobile .site{height:216.4103cqw}
.site a{color:inherit;text-decoration:none}
.site a:hover{text-decoration:underline;text-underline-offset:.24em}
.site a:focus-visible{outline:2px solid currentColor;outline-offset:4px}
.site h1,.site h2,.site h3,.site h4,.site p,.site figure,.site pre{margin:0;font-weight:400}
.site ul{margin:0;padding:0;list-style:none}
.site .mono{font-family:"Space Mono",ui-monospace,monospace}
.site .serif{font-family:"DM Serif Display",Georgia,serif}
.site .grotesk{font-family:"Space Grotesk",system-ui,sans-serif}
.site .anton{font-family:"Anton",Impact,sans-serif}
.site .eyebrow{font-family:"Space Mono",monospace;text-transform:uppercase;letter-spacing:.22em}
@keyframes twinkle{0%,100%{opacity:.3}50%{opacity:1}}
@keyframes breathe{0%,100%{opacity:.5;transform:scale(1)}50%{opacity:.95;transform:scale(1.035)}}
@keyframes draw{from{stroke-dashoffset:var(--len,600)}}
@keyframes scanbeam{0%{transform:translateY(-14%)}100%{transform:translateY(114%)}}
@keyframes blink{0%,48%{opacity:1}49%,100%{opacity:0}}
@keyframes meter{0%,100%{transform:scaleY(.2)}50%{transform:scaleY(1)}}
@keyframes sway{0%,100%{transform:translateX(-1.6%) rotate(var(--r,0deg))}50%{transform:translateX(1.6%) rotate(var(--r,0deg))}}
@keyframes bob{0%,100%{transform:translateY(-.5cqw)}50%{transform:translateY(.5cqw)}}
@keyframes rise{0%{transform:translateY(0);opacity:0}12%{opacity:.7}100%{transform:translateY(-46cqw);opacity:0}}
@keyframes flicker{0%,100%{opacity:1}92%{opacity:1}93%{opacity:.72}94%{opacity:1}97%{opacity:.85}98%{opacity:1}}
@media(prefers-reduced-motion:reduce){
  .site *{animation:none!important;transition:none!important}
  .site .draw{stroke-dashoffset:0!important}
  .site [class*="reveal"]{opacity:1!important;transform:none!important}
}
"""

# ---------------------------------------------------------------- A: Observatory

OBS_CSS = """
.obs{background:radial-gradient(130% 90% at 78% 92%,#16214c 0%,#0a1132 32%,#05070f 100%);color:#f1ecdf;padding:3.2cqw 4.6cqw}
.obs .sky{position:absolute;inset:0;background:
  radial-gradient(1.2px 1.2px at 12% 18%,#fff,transparent),
  radial-gradient(1px 1px at 28% 8%,#cfd6f2,transparent),
  radial-gradient(1.4px 1.4px at 44% 22%,#fff,transparent),
  radial-gradient(1px 1px at 61% 12%,#b9c2e6,transparent),
  radial-gradient(1.2px 1.2px at 72% 30%,#fff,transparent),
  radial-gradient(1px 1px at 88% 16%,#d6dcf5,transparent),
  radial-gradient(1px 1px at 8% 44%,#cbd2ee,transparent),
  radial-gradient(1.3px 1.3px at 34% 52%,#fff,transparent),
  radial-gradient(1px 1px at 52% 64%,#c6cdec,transparent),
  radial-gradient(1px 1px at 20% 74%,#e7ebfb,transparent),
  radial-gradient(1.4px 1.4px at 66% 78%,#fff,transparent),
  radial-gradient(1px 1px at 82% 58%,#cdd4f0,transparent),
  radial-gradient(1px 1px at 90% 84%,#dfe4f7,transparent);
  opacity:.85}
.obs .stars{position:absolute;inset:0;background-image:radial-gradient(1px 1px at 50% 50%,#fff,transparent);background-size:11cqw 11cqw;opacity:.18;animation:twinkle 7s ease-in-out infinite}
.obs-top{position:absolute;top:3.2cqw;left:4.6cqw;right:4.6cqw;display:flex;justify-content:space-between;align-items:baseline;z-index:3}
.obs-word{font-size:2.3cqw;letter-spacing:-.01em}
.obs-top nav{display:flex;gap:2.4cqw;font-size:.92cqw;color:#b9c1de}
.obs-name{position:absolute;top:13.4cqw;left:4.6cqw;width:54cqw;z-index:3}
.obs-name .eyebrow{font-size:.82cqw;color:#c9a45f}
.obs-name h1{font-size:7.1cqw;line-height:.99;letter-spacing:-.028em;margin-top:1.8cqw}
.obs-name h1 em{font-style:italic;color:#e8b96a}
.obs-name p{font-size:1.34cqw;line-height:1.5;color:#aab2cf;max-width:32cqw;margin-top:2.4cqw}
.obs-disc{position:absolute;right:-3cqw;top:28cqw;width:40cqw;height:40cqw;border-radius:50%;z-index:2;
  background:
   radial-gradient(6% 6% at 30% 34%,rgba(150,105,45,.5),transparent 70%),
   radial-gradient(8% 8% at 62% 26%,rgba(150,105,45,.42),transparent 70%),
   radial-gradient(10% 10% at 48% 62%,rgba(150,105,45,.35),transparent 70%),
   radial-gradient(5% 5% at 74% 54%,rgba(150,105,45,.4),transparent 70%),
   radial-gradient(circle at 34% 28%,#fff8ea 0%,#f6dda6 40%,#dcac61 70%,#a9762f 100%);
  box-shadow:0 0 11cqw 1.6cqw rgba(240,197,124,.3),inset -3cqw -4cqw 7cqw rgba(120,72,22,.42)}
.obs-disc:before{content:"";position:absolute;inset:-2.4cqw;border-radius:50%;border:.16cqw solid rgba(232,185,106,.4);box-shadow:0 0 5cqw rgba(232,185,106,.22);animation:breathe 9s ease-in-out infinite}
.obs-disc:after{content:"";position:absolute;inset:-6.4cqw;border-radius:50%;border:.1cqw solid rgba(180,196,240,.16)}
.obs-horizon{position:absolute;left:0;right:0;bottom:0;height:24cqw;z-index:1;background:linear-gradient(180deg,transparent,rgba(3,4,12,.72) 52%,#02030a)}
.obs-horizon:before{content:"";position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(232,185,106,.5),transparent)}
.obs-const{position:absolute;top:8cqw;right:4.6cqw;width:25cqw;z-index:3}
.obs-const .cap{display:flex;justify-content:space-between;font-size:.78cqw;color:#c9a45f}
.obs-const svg{width:100%;height:auto;margin-top:.6cqw;overflow:visible}
.obs-const .draw{stroke-dasharray:var(--len);animation:draw 2.4s ease-out both}
.obs-index{position:absolute;left:4.6cqw;bottom:4.4cqw;width:58cqw;display:grid;grid-template-columns:1fr 1fr;gap:3.6cqw;z-index:3}
.obs-index article{border-top:1px solid rgba(241,236,223,.28);padding-top:1.4cqw}
.obs-index .mono{font-size:.76cqw;color:#a9b1cf;letter-spacing:.1em}
.obs-index h3{font-size:2.5cqw;letter-spacing:-.02em;margin:.5cqw 0 .3cqw}
.obs-index p{font-size:1cqw;color:#98a0bf}
.obs-foot{position:absolute;left:4.6cqw;right:4.6cqw;bottom:1.5cqw;display:flex;justify-content:space-between;font-size:.74cqw;color:#7d86a8;z-index:3}
/* mobile */
.mobile .obs{padding:6cqw 6cqw}
.mobile .obs-word{font-size:5cqw}
.mobile .obs-top nav{font-size:2.5cqw;gap:5cqw}
.mobile .obs-name{top:15cqw;left:6cqw;width:88cqw}
.mobile .obs-name .eyebrow{font-size:2.2cqw}
.mobile .obs-name h1{font-size:14.5cqw;margin-top:4cqw}
.mobile .obs-name p{font-size:3.3cqw;max-width:84cqw;margin-top:5cqw}
.mobile .obs-disc{left:5cqw;right:auto;top:104cqw;width:46cqw;height:46cqw}
.mobile .obs-const{top:92cqw;right:5cqw;width:40cqw}
.mobile .obs-const .cap{font-size:2.1cqw}
.mobile .obs-index{left:6cqw;right:6cqw;bottom:16cqw;width:auto;grid-template-columns:1fr;gap:4cqw}
.mobile .obs-index .mono{font-size:2cqw}
.mobile .obs-index h3{font-size:6.6cqw}
.mobile .obs-index p{font-size:3cqw}
.mobile .obs-foot{left:6cqw;right:6cqw;bottom:5cqw;font-size:1.9cqw}
"""

OBS_CONST = """
<svg viewBox="0 0 100 74" role="img" aria-label="Constellation marking the Models catalogue">
  <g stroke="#e8b96a" stroke-width=".3" fill="none" opacity=".85">
    <path class="draw" style="--len:120" d="M12 22 L34 12 L54 27 L45 50 L20 46 Z"/>
    <path class="draw" style="--len:104" d="M54 27 L76 17 L89 38 L70 56 L45 50"/>
    <path class="draw" style="--len:52" d="M12 22 L34 12"/>
  </g>
  <g fill="#fff6e0">
    <circle cx="12" cy="22" r="1.1"/><circle cx="34" cy="12" r="1.5"/><circle cx="54" cy="27" r="1"/><circle cx="45" cy="50" r="1.2"/><circle cx="20" cy="46" r=".9"/>
    <circle cx="76" cy="17" r="1.3"/><circle cx="89" cy="38" r="1"/><circle cx="70" cy="56" r="1.5"/>
  </g>
  <g class="mono" fill="#aab2cf" font-size="4.2">
    <text x="4" y="17">GPT</text><text x="30" y="7">CLAUDE</text><text x="56" y="22">GEMINI</text>
    <text x="75" y="62">LLAMA</text><text x="86" y="34">MISTRAL</text>
  </g>
</svg>
"""

OBS = (
    '<div class="site obs">'
    '<span class="sky" aria-hidden="true"></span><span class="stars" aria-hidden="true"></span>'
    '<header class="obs-top">'
    '<span class="obs-word serif">MusseJusse</span>'
    '<nav>%s %s</nav>'
    "</header>"
    '<div class="obs-name">'
    '<span class="eyebrow">Personal site / experiments</span>'
    "<h1>Always building.<br><em>Never finished.</em></h1>"
    "<p>I'm Musse. I make small things for the web and follow the question until it runs out.</p>"
    "</div>"
    '<div class="obs-disc" aria-hidden="true"></div>'
    '<div class="obs-horizon" aria-hidden="true"></div>'
    '<figure class="obs-const"><figcaption class="cap"><span>Object 02</span><span>Models</span></figcaption>'
    + OBS_CONST
    + "</figure>"
    '<section class="obs-index">'
    '<article><span class="mono">Object 01 / Next.js</span>'
    "<h3>%s</h3><p>Which one is rounder?</p></article>"
    '<article><span class="mono">Object 02 / Astro</span>'
    "<h3>%s</h3><p>A catalogue of every model.</p></article>"
    "</section>"
    '<footer class="obs-foot"><span>MusseJusse / always a work in progress</span><span>N. Latitude, unknown</span></footer>'
    "</div>"
) % (GH_LINK, BS_LINK, a(R, "Roundest Pokémon"), a(M, "Models"))

# ---------------------------------------------------------------- B: Riso print

RISO_CSS = """
.riso{background:#f7f2e7;color:#17130f;padding:3.4cqw 4.2cqw}
.riso .dotgrid{position:absolute;inset:0;background-image:radial-gradient(rgba(23,19,15,.13) 1px,transparent 1.4px);background-size:1.5cqw 1.5cqw;opacity:.5}
.riso .grain{position:absolute;inset:0;opacity:.16;mix-blend-mode:multiply;background-image:radial-gradient(rgba(23,19,15,.5) .5px,transparent .6px);background-size:.35cqw .35cqw}
.riso-top{position:relative;display:flex;justify-content:space-between;align-items:center;z-index:3}
.riso-top .badge{font-size:.78cqw;letter-spacing:.1em;border:.14cqw solid #17130f;padding:.5cqw .9cqw}
.riso-word{font-size:2.5cqw;letter-spacing:-.01em;text-transform:uppercase}
.riso-top nav{display:flex;gap:2.2cqw;font-size:.9cqw}
.riso h1{position:relative;width:66cqw;margin-top:5.4cqw;font-family:"Anton",Impact,sans-serif;font-size:10.4cqw;line-height:.84;text-transform:uppercase;letter-spacing:-.005em;color:#1b2a8f;z-index:2;white-space:pre}
.riso h1:before,.riso h1:after{content:attr(data-t);position:absolute;left:0;top:0;width:100%;white-space:pre;background-clip:text;-webkit-background-clip:text;color:transparent;-webkit-text-fill-color:transparent}
.riso h1:before{background:radial-gradient(circle,#ffd23f 33%,transparent 35%) 0 0/.55cqw .55cqw;-webkit-background-clip:text;background-clip:text;transform:translate(.58cqw,.44cqw);z-index:-2}
.riso h1:after{background:radial-gradient(circle,#ff5c8a 33%,transparent 35%) 0 0/.55cqw .55cqw;-webkit-background-clip:text;background-clip:text;transform:translate(.3cqw,.24cqw);z-index:-1}
.riso .kicker{position:absolute;top:20cqw;right:4.2cqw;width:22cqw;font-size:1.05cqw;line-height:1.45;z-index:3}
.riso .kicker b{font-weight:700}
.riso .sticker{position:absolute;top:6.4cqw;right:8cqw;width:9.6cqw;height:9.6cqw;border-radius:50%;background:#ff5c8a;color:#fff;display:grid;place-content:center;text-align:center;font-family:"Anton",sans-serif;font-size:1.5cqw;line-height:.95;transform:rotate(9deg);z-index:4;box-shadow:.5cqw .5cqw 0 #1b2a8f}
.riso-cards{position:absolute;left:4.2cqw;right:4.2cqw;bottom:6.6cqw;display:grid;grid-template-columns:1fr 1fr;gap:3cqw;z-index:2}
.riso .card{position:relative;height:22cqw;background:#fffdf7;border:.16cqw solid #17130f;padding:1.8cqw;display:flex;flex-direction:column;overflow:hidden}
.riso .card.pink{transform:rotate(-1.3deg);box-shadow:.7cqw .7cqw 0 #ff5c8a}
.riso .card.blue{transform:rotate(1.1deg);box-shadow:.7cqw .7cqw 0 #1b2a8f}
.riso .card .mono{font-size:.74cqw;letter-spacing:.08em}
.riso .card h3{font-family:"Anton",sans-serif;font-size:2.8cqw;text-transform:uppercase;margin-top:.4cqw;position:relative;z-index:2}
.riso .card p{font-size:.96cqw;margin-top:.5cqw;position:relative;z-index:2}
.riso .card .go{margin-top:auto;font-size:1.7cqw;align-self:flex-end;position:relative;z-index:2}
.riso .halftone{position:absolute;right:-2cqw;top:-1cqw;width:15cqw;height:15cqw;border-radius:50%;background:radial-gradient(circle,#17130f 36%,transparent 38%) 0 0/.5cqw .5cqw;opacity:.85}
.riso .card.blue .halftone{border-radius:0;background:radial-gradient(circle,#1b2a8f 36%,transparent 38%) 0 0/.5cqw .5cqw}
.riso-foot{position:absolute;left:4.2cqw;right:4.2cqw;bottom:1.5cqw;display:flex;justify-content:space-between;font-size:.74cqw;letter-spacing:.04em;z-index:3;border-top:.14cqw solid #17130f;padding-top:1cqw}
/* mobile */
.mobile .riso{padding:6cqw 6cqw}
.mobile .riso-word{font-size:6cqw}
.mobile .riso-top{flex-wrap:wrap;gap:3cqw}
.mobile .riso-top .riso-word{flex:1 0 100%}
.mobile .riso-top nav{font-size:2.5cqw;gap:5cqw}
.mobile .riso-top .badge{font-size:2cqw;border-width:.4cqw}
.mobile .riso h1{width:90cqw;margin-top:9cqw;font-size:13cqw;line-height:1}
.mobile .riso h1:before{background-size:1cqw 1cqw;transform:translate(1.1cqw,.85cqw)}
.mobile .riso h1:after{background-size:1cqw 1cqw;transform:translate(.55cqw,.45cqw)}
.mobile .riso .kicker{position:static;width:64cqw;margin-top:7cqw;font-size:3.3cqw}
.mobile .riso .sticker{top:66cqw;right:5cqw;width:18cqw;height:18cqw;font-size:3cqw;box-shadow:1cqw 1cqw 0 #1b2a8f}
.mobile .riso-cards{position:static;margin-top:9cqw;display:grid;grid-template-columns:1fr;gap:6cqw}
.mobile .riso .card{height:40cqw;padding:4cqw;border-width:.4cqw}
.mobile .riso .card.pink{box-shadow:1.4cqw 1.4cqw 0 #ff5c8a}
.mobile .riso .card.blue{box-shadow:1.4cqw 1.4cqw 0 #1b2a8f}
.mobile .riso .card .mono{font-size:2.1cqw}
.mobile .riso .card h3{font-size:7cqw}
.mobile .riso .card p{font-size:3.1cqw}
.mobile .riso .card .go{font-size:4.4cqw}
.mobile .riso .halftone{width:34cqw;height:34cqw;right:-4cqw;background-size:1.2cqw 1.2cqw}
.riso-foot{position:absolute}
.mobile .riso-foot{left:6cqw;right:6cqw;bottom:4cqw;font-size:2cqw;border-top-width:.4cqw;flex-direction:column;gap:1.4cqw}
"""

RISO = (
    '<div class="site riso">'
    '<span class="dotgrid" aria-hidden="true"></span><span class="grain" aria-hidden="true"></span>'
    '<header class="riso-top"><span class="riso-word grotesk">mussejusse</span>'
    '<span class="badge mono">RISO / EDITION 01</span>'
    '<nav>%s %s</nav></header>'
    '<h1 data-t="ALWAYS\nBUILDING\nNEVER FINISHED">ALWAYS\nBUILDING\nNEVER FINISHED</h1>'
    '<span class="sticker" aria-hidden="true">NEW<br>WORK</span>'
    '<p class="kicker grotesk">A screenprint of a personal site. Two inks, one <b>Roundest Pokémon</b>, one <b>Models</b> catalogue. Printed by hand, mostly.</p>'
    '<section class="riso-cards">'
    '<article class="card pink"><span class="mono">LOT 01 / NEXT.JS / COMPARISON</span>'
    '<span class="halftone" aria-hidden="true"></span>'
    "<h3>%s</h3><p>Which one is rounder?</p><span class=\"go\">↗</span></article>"
    '<article class="card blue"><span class="mono">LOT 02 / ASTRO / REFERENCE</span>'
    '<span class="halftone" aria-hidden="true"></span>'
    "<h3>%s</h3><p>The model catalogue, pared back.</p><span class=\"go\">↗</span></article>"
    "</section>"
    '<footer class="riso-foot mono"><span>Made by Musse. Hosted on Vercel.</span><span>Source on GitHub</span></footer>'
    "</div>"
) % (GH_LINK, BS_LINK, a(R, "Roundest Pokémon"), a(M, "Models"))

# ---------------------------------------------------------------- C: Blueprint

BP_CSS = """
.bp{background:#0c3055;color:#dbeafb;padding:3.2cqw 4cqw}
.bp .sheet{position:absolute;inset:1.4cqw;border:.12cqw solid rgba(219,234,251,.5)}
.bp .grid{position:absolute;inset:1.4cqw;
  background-image:linear-gradient(rgba(219,234,251,.09) 1px,transparent 1px),linear-gradient(90deg,rgba(219,234,251,.09) 1px,transparent 1px),
  linear-gradient(rgba(219,234,251,.16) 1px,transparent 1px),linear-gradient(90deg,rgba(219,234,251,.16) 1px,transparent 1px);
  background-size:2.5cqw 2.5cqw,2.5cqw 2.5cqw,12.5cqw 12.5cqw,12.5cqw 12.5cqw}
.bp .reg{position:absolute;font-size:1.6cqw;color:rgba(219,234,251,.6);z-index:4}
.bp .reg.tl{top:1.8cqw;left:2.2cqw}.bp .reg.tr{top:1.8cqw;right:2.2cqw}
.bp .reg.bl{bottom:1.8cqw;left:2.2cqw}.bp .reg.br{bottom:1.8cqw;right:2.2cqw}
.bp-top{position:absolute;top:3.2cqw;left:4.4cqw;right:4.4cqw;display:flex;justify-content:space-between;font-size:.82cqw;letter-spacing:.14em;z-index:3}
.bp-top nav{display:flex;gap:2.4cqw}
.bp-hero{position:absolute;top:11cqw;left:4.4cqw}
.bp-hero .eyebrow{font-size:.78cqw;color:#8fb6dd}
.bp-hero h1{margin-top:1.4cqw;font-family:"Space Grotesk",sans-serif;font-weight:700;font-size:9.6cqw;line-height:.9;letter-spacing:.01em;text-transform:uppercase;-webkit-text-stroke:.14cqw #dbeafb;color:transparent}
.bp-dim{display:flex;align-items:center;gap:1cqw;margin-top:1.6cqw;width:46cqw;color:#9cc2e6;font-size:.76cqw}
.bp-dim .line{position:relative;flex:1;height:.12cqw;background:currentColor}
.bp-dim .line:before,.bp-dim .line:after{content:"";position:absolute;top:-.55cqw;width:.12cqw;height:1.2cqw;background:currentColor}
.bp-dim .line:before{left:0}.bp-dim .line:after{right:0}
.bp-detail{position:absolute;width:37cqw;z-index:3}
.bp-detail.r{left:53.4cqw;top:9cqw}
.bp-detail.m{left:53.4cqw;top:39.5cqw}
.bp-frame{position:relative;height:23cqw;border:.14cqw solid rgba(219,234,251,.7)}
.bp-frame .tag{position:absolute;top:-.9cqw;left:1.4cqw;background:#0c3055;padding:0 .7cqw;font-size:.72cqw;letter-spacing:.14em;color:#9cc2e6}
.bp-frame svg{position:absolute;inset:0;width:100%;height:100%}
.bp-detail h3{font-family:"Space Grotesk",sans-serif;font-weight:700;font-size:2.1cqw;text-transform:uppercase;margin-top:1.4cqw;letter-spacing:.02em}
.bp-detail p{font-size:.92cqw;color:#a9c9e8;margin-top:.4cqw;max-width:30cqw}
.bp-detail .go{position:absolute;right:0;top:24.6cqw;font-size:1.8cqw}
.bp-titleblock{position:absolute;left:4.4cqw;bottom:3.2cqw;width:42cqw;border:.14cqw solid rgba(219,234,251,.75);display:grid;grid-template-columns:1.1fr 1fr 1fr;z-index:3;background:rgba(6,27,48,.55)}
.bp-titleblock div{border-right:.12cqw solid rgba(219,234,251,.4);border-bottom:.12cqw solid rgba(219,234,251,.4);padding:.9cqw 1.1cqw}
.bp-titleblock div:nth-child(3n){border-right:0}
.bp-titleblock div:nth-last-child(-n+3){border-bottom:0}
.bp-titleblock span{display:block;font-size:.62cqw;letter-spacing:.16em;color:#7fa9d2}
.bp-titleblock b{display:block;font-weight:700;font-size:1.15cqw;margin-top:.25cqw}
.bp-titleblock .accent b{color:#ffd166}
.bp-notes{position:absolute;left:4.4cqw;bottom:14cqw;width:42cqw;z-index:3;font-family:"Space Mono",monospace}
.bp-notes h4{font-size:.66cqw;letter-spacing:.18em;color:#7fa9d2;margin:0 0 .9cqw;font-weight:400}
.bp-notes ul{display:grid;gap:.5cqw}
.bp-notes li{font-size:.8cqw;color:#a9c9e8;padding-left:1.6cqw;position:relative}
.bp-notes li:before{content:attr(data-n);position:absolute;left:0;color:#ffd166}
.bp-sweep{position:absolute;left:1.4cqw;right:1.4cqw;top:1.4cqw;height:2.4cqw;background:linear-gradient(180deg,transparent,rgba(180,220,255,.5),transparent);animation:scanbeam 7s linear infinite;mix-blend-mode:screen;opacity:.5;z-index:2}
/* mobile */
.mobile .bp{padding:6cqw}
.mobile .bp .sheet{inset:3cqw}
.mobile .bp .grid{inset:3cqw;background-size:6cqw 6cqw,6cqw 6cqw,30cqw 30cqw,30cqw 30cqw}
.mobile .bp .reg{font-size:4cqw}
.mobile .bp-top{top:7cqw;left:7cqw;right:7cqw;font-size:2.1cqw}
.mobile .bp-top nav{gap:5cqw}
.mobile .bp-hero{position:static;padding:12cqw 6cqw 0}
.mobile .bp-hero .eyebrow{font-size:2.1cqw}
.mobile .bp-hero h1{font-size:20cqw;margin-top:3cqw;-webkit-text-stroke-width:.36cqw}
.mobile .bp-dim{width:74cqw;margin-top:3.4cqw;font-size:2cqw}
.mobile .bp-detail{position:static;width:auto;padding:5cqw 6cqw 0}
.mobile .bp-frame{height:37cqw;border-width:.4cqw}
.mobile .bp-frame .tag{font-size:1.9cqw;background:#0c3055}
.mobile .bp-detail h3{font-size:5cqw;margin-top:2.4cqw}
.mobile .bp-detail p{font-size:2.7cqw;max-width:none;margin-top:1.2cqw}
.mobile .bp-detail .go{display:none}
.mobile .bp-titleblock{position:static;margin:6cqw 6cqw 0;width:auto;border-width:.4cqw;grid-template-columns:1fr 1fr}
.mobile .bp-titleblock div{padding:2.2cqw 2.2cqw;border-right-width:.35cqw;border-bottom-width:.35cqw}
.mobile .bp-titleblock span{font-size:1.6cqw}
.mobile .bp-titleblock b{font-size:3cqw}
.mobile .bp-notes{display:none}
"""

BP_ROUNDEST_SVG = """
<svg viewBox="0 0 200 120" role="img" aria-label="Technical drawing of a circle with its diameter dimensioned">
  <g fill="none" stroke="#dbeafb" stroke-width="1">
    <circle cx="78" cy="60" r="40"/>
    <circle cx="78" cy="60" r="28" stroke-dasharray="3 3" opacity=".6"/>
    <path d="M78 20 V100 M38 60 H118"/>
  </g>
  <g fill="none" stroke="#ffd166" stroke-width="1.1">
    <path d="M78 60 L110 32" marker-end="url(#ar)"/>
  </g>
  <defs><marker id="ar" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto"><path d="M0 0 L6 3 L0 6" fill="#ffd166"/></marker></defs>
  <g fill="#9cc2e6" font-family="monospace" font-size="6" letter-spacing=".5">
    <text x="120" y="46">R 50.00</text><text x="82" y="16">90°</text><text x="150" y="64">&#8960; 100.00</text>
    <text x="8" y="112">DETAIL A / ROUNDNESS</text>
  </g>
  <g stroke="#ffd166" stroke-width="1"><path d="M126 60 H150"/><path d="M78 60 H50" opacity=".5"/></g>
</svg>
"""

BP_MODELS_SVG = """
<svg viewBox="0 0 200 120" role="img" aria-label="Technical drawing of stacked layers with dimensions">
  <g fill="none" stroke="#dbeafb" stroke-width="1">
    <rect x="40" y="18" width="120" height="16"/>
    <rect x="40" y="42" width="120" height="16"/>
    <rect x="40" y="66" width="120" height="16"/>
    <rect x="40" y="90" width="120" height="16" stroke-dasharray="3 3" opacity=".6"/>
  </g>
  <g stroke="#ffd166" stroke-width="1.1"><path d="M32 18 V106"/><path d="M180 42 V82"/></g>
  <g fill="#9cc2e6" font-family="monospace" font-size="6" letter-spacing=".5">
    <text x="52" y="29">PROVIDERS</text><text x="52" y="53">MODELS</text><text x="52" y="77">CAPABILITIES</text><text x="52" y="101">PRICING</text>
    <text x="150" y="64">N = 200+</text><text x="8" y="112">DETAIL B / LAYERS</text>
  </g>
  <g fill="none" stroke="#dbeafb" stroke-width=".6" opacity=".5"><path d="M160 26 H180 M160 50 H180 M160 74 H180"/></g>
</svg>
"""

BP = (
    '<div class="site bp">'
    '<span class="grid" aria-hidden="true"></span>'
    '<span class="reg mono tl">+</span><span class="reg mono tr">+</span><span class="reg mono bl">+</span><span class="reg mono br">+</span>'
    '<span class="sheet" aria-hidden="true"></span>'
    '<span class="sweep" aria-hidden="true"></span>'
    '<header class="bp-top mono"><span>MUSSEJUSSE.COM / EXPERIMENTS</span><nav>%s %s</nav></header>'
    '<div class="bp-hero"><span class="eyebrow mono">Drawing no. 01 / revision C</span>'
    "<h1>Musse<br>Jusse</h1>"
    '<div class="bp-dim mono"><span>|<</span><span class="line"></span><span>1440 &times; &infin;</span><span class="line"></span><span>|&gt;</span></div></div>'
    '<section class="bp-detail r"><div class="bp-frame"><span class="tag mono">DETAIL A</span>'
    + BP_ROUNDEST_SVG
    + "</div>"
    '<h3>%s</h3><p>Next.js, server actions, a KV store, and one very specific question.</p><span class="go">↗</span></section>'
    '<section class="bp-detail m"><div class="bp-frame"><span class="tag mono">DETAIL B</span>'
    + BP_MODELS_SVG
    + "</div>"
    '<h3>%s</h3><p>Astro, ultra light, the whole model catalogue in four layers.</p><span class="go">↗</span></section>'
    '<div class="bp-notes"><h4>NOTES</h4><ul>'
    '<li data-n="1">Built to be read. Every line earns its place.</li>'
    '<li data-n="2">Two experiments, drawn from life.</li>'
    '</ul></div>'
    '<div class="bp-titleblock mono">'
    '<div class="accent"><span>PROJECT</span><b>mussejusse.com</b></div><div><span>DRAWN</span><b>M. Jusse</b></div><div><span>SHEET</span><b>01 / 01</b></div>'
    '<div><span>SCALE</span><b>1 : 1</b></div><div><span>DATE</span><b>2026</b></div><div class="accent"><span>STATUS</span><b>Build</b></div>'
    "</div></div>"
) % (GH_LINK, BS_LINK, a(R, "Roundest Pokémon"), a(M, "Models"))

# ---------------------------------------------------------------- D: Tide

TIDE_CSS = """
.tide{background:linear-gradient(180deg,#1ec9cb 0%,#12a3b5 14%,#0a6f8c 34%,#074055 56%,#031c2b 78%,#01080e 100%);color:#eafdfb;padding:3.2cqw 4.4cqw}
.tide .rays{position:absolute;top:-10cqw;left:0;right:0;height:70cqw;opacity:.5;filter:blur(1.4cqw);pointer-events:none;
  background:repeating-linear-gradient(74deg,rgba(190,252,244,.5) 0 1.4cqw,transparent 1.4cqw 7cqw);
  -webkit-mask-image:linear-gradient(180deg,#000,transparent);mask-image:linear-gradient(180deg,#000,transparent);animation:sway 11s ease-in-out infinite}
.tide .caustics{position:absolute;left:-20%;top:-4cqw;width:140%;height:52cqw;opacity:.35;mix-blend-mode:soft-light;pointer-events:none;
  background-image:radial-gradient(circle,rgba(255,255,255,.9) 0 1.2%,transparent 1.4%),radial-gradient(circle,rgba(255,255,255,.7) 0 1%,transparent 1.3%);
  background-size:14cqw 11cqw,19cqw 15cqw;animation:sway 16s ease-in-out infinite reverse}
.tide .bubbles{position:absolute;inset:0;overflow:hidden;pointer-events:none}
.tide .bubbles i{position:absolute;bottom:6cqw;width:.7cqw;height:.7cqw;border-radius:50%;background:rgba(255,255,255,.5);animation:rise 12s linear infinite}
.tide .bubbles i:nth-child(1){left:12%;animation-delay:0s}.tide .bubbles i:nth-child(2){left:34%;animation-delay:4s}
.tide .bubbles i:nth-child(3){left:58%;animation-delay:7s}.tide .bubbles i:nth-child(4){left:78%;animation-delay:2s}.tide .bubbles i:nth-child(5){left:90%;animation-delay:9s}
.tide-top{position:absolute;top:3.2cqw;left:4.4cqw;right:4.4cqw;display:flex;justify-content:space-between;align-items:baseline;z-index:3}
.tide-word{font-size:2.4cqw}
.tide-top nav{display:flex;gap:2.4cqw;font-size:.9cqw;color:#c9fbf5}
.tide-hero{position:absolute;top:11cqw;left:4.4cqw;width:48cqw;z-index:3}
.tide-hero .eyebrow{font-size:.78cqw;color:#bff7ef}
.tide-hero h1{font-size:6.4cqw;line-height:1;letter-spacing:-.02em;margin-top:1.6cqw}
.tide-hero h1 em{font-style:italic;color:#bff7ef}
.tide-hero p{font-size:1.3cqw;line-height:1.55;max-width:32cqw;margin-top:2.2cqw;color:#cdeef0}
.tide-ruler{position:absolute;right:3.2cqw;top:9cqw;bottom:9cqw;width:12cqw;z-index:3}
.tide-ruler:before{content:"";position:absolute;left:0;top:0;bottom:0;width:.12cqw;background:rgba(234,253,251,.5)}
.tide-ruler .tick{position:absolute;left:0;font-size:.66cqw;color:#bff7ef;letter-spacing:.1em;white-space:nowrap;padding-left:1.2cqw}
.tide-ruler .tick:before{content:"";position:absolute;left:0;top:.55cqw;width:1cqw;height:.12cqw;background:rgba(234,253,251,.6)}
.tide-ruler .tick.a{top:0}.tide-ruler .tick.b{top:33%}.tide-ruler .tick.c{top:66%}.tide-ruler .tick.d{top:100%}
.tide-ruler .marker{position:absolute;left:-.7cqw;width:1.5cqw;height:1.5cqw;border-radius:50%;background:#7bf2c4;box-shadow:0 0 2cqw #7bf2c4;top:24%;animation:bob 6s ease-in-out infinite}
.specimen{position:absolute;width:37cqw;padding:2cqw;border-radius:1.6cqw;z-index:3;
  background:linear-gradient(135deg,rgba(255,255,255,.16),rgba(255,255,255,.05));border:.12cqw solid rgba(255,255,255,.3);
  backdrop-filter:blur(1.6cqw);box-shadow:0 2cqw 5cqw rgba(0,0,0,.3),inset 0 .2cqw 1cqw rgba(255,255,255,.28)}
.specimen.r{left:4.4cqw;top:35cqw}
.specimen.m{right:6.6cqw;top:50cqw}
.specimen .mono{font-size:.74cqw;letter-spacing:.12em;color:#c9fbf5}
.specimen h3{font-family:"Space Grotesk",sans-serif;font-weight:600;font-size:2.5cqw;letter-spacing:-.01em;margin-top:.6cqw;max-width:70%}
.specimen p{font-size:.98cqw;color:#d6f4f4;margin-top:.5cqw;max-width:66%}
.specimen .go{position:absolute;right:2cqw;top:1.8cqw;font-size:1.8cqw}
.specimen .orb{position:absolute;right:3cqw;bottom:-1cqw;width:8cqw;height:8cqw;border-radius:50%;background:radial-gradient(circle at 36% 32%,#fff,#9fe8ff 45%,rgba(120,242,196,.4));filter:blur(.1cqw)}
.specimen.m .grid-mark{position:absolute;right:3cqw;bottom:1.6cqw;width:8cqw;height:5cqw;background-image:linear-gradient(rgba(255,255,255,.5) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.5) 1px,transparent 1px);background-size:1.4cqw 1.4cqw;opacity:.7}
.tide-foot{position:absolute;left:4.4cqw;right:4.4cqw;bottom:2cqw;display:flex;justify-content:space-between;font-size:.74cqw;color:#9fdfe6;z-index:3}
/* mobile */
.mobile .tide{padding:6cqw}
.mobile .tide-word{font-size:5.2cqw}
.mobile .tide-top nav{font-size:2.5cqw;gap:5cqw}
.mobile .tide .rays{height:120cqw;background-size:auto;background:repeating-linear-gradient(70deg,rgba(190,252,244,.45) 0 3cqw,transparent 3cqw 13cqw)}
.mobile .tide .caustics{height:110cqw;background-size:34cqw 26cqw,44cqw 34cqw}
.mobile .tide-hero{position:static;padding:16cqw 6cqw 0;width:auto}
.mobile .tide-hero .eyebrow{font-size:2.2cqw}
.mobile .tide-hero h1{font-size:13.5cqw;margin-top:3.4cqw}
.mobile .tide-hero p{font-size:3.5cqw;max-width:none;margin-top:5cqw}
.mobile .tide-ruler{left:3cqw;right:auto;top:64cqw;bottom:10cqw;width:12cqw;z-index:2}
.mobile .tide-ruler .tick{font-size:0;padding:0}
.mobile .tide-ruler .tick:before{width:2.2cqw;height:.3cqw}
.mobile .tide-ruler .marker{left:-.9cqw;width:2.4cqw;height:2.4cqw}
.mobile .specimen{position:static;width:auto;margin:0 6cqw;padding:5cqw;border-radius:3cqw;border-width:.35cqw;backdrop-filter:blur(3cqw)}
.mobile .specimen.r{margin-top:12cqw}
.mobile .specimen.m{margin-top:6cqw}
.mobile .specimen .mono{font-size:2cqw}
.mobile .specimen h3{font-size:6.4cqw}
.mobile .specimen p{font-size:3cqw}
.mobile .specimen .go{font-size:4.4cqw;right:5cqw}
.mobile .specimen .orb{width:22cqw;height:22cqw;right:6cqw;bottom:-4cqw}
.mobile .specimen.m .grid-mark{width:22cqw;height:14cqw;background-size:3.5cqw 3.5cqw}
.mobile .tide-foot{left:6cqw;right:6cqw;bottom:5cqw;font-size:1.9cqw}
"""

TIDE = (
    '<div class="site tide">'
    '<span class="rays" aria-hidden="true"></span><span class="caustics" aria-hidden="true"></span>'
    '<span class="bubbles" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></span>'
    '<header class="tide-top"><span class="tide-word serif">MusseJusse</span><nav>%s %s</nav></header>'
    '<div class="tide-hero"><span class="eyebrow mono">Depth 0000 M / Surface</span>'
    "<h1>I keep building<br>where it gets <em>dark.</em></h1>"
    "<p>Below the surface are two experiments: a very round question and a catalogue of every model.</p></div>"
    '<div class="tide-ruler" aria-hidden="true"><span class="marker"></span>'
    '<span class="tick a">0 M · SURFACE</span><span class="tick b">200 M · TWILIGHT</span><span class="tick c">1000 M · MIDNIGHT</span><span class="tick d">4000 M · ABYSS</span></div>'
    '<article class="specimen r"><span class="mono">Specimen 01 / Next.js</span><span class="go">↗</span>'
    "<h3>%s</h3><p>Which Pokémon is roundest? Come help settle it.</p><span class=\"orb\" aria-hidden=\"true\"></span></article>"
    '<article class="specimen m"><span class="mono">Specimen 02 / Astro</span><span class="go">↗</span>'
    "<h3>%s</h3><p>Every model, provider and capability in one current.</p><span class=\"grid-mark\" aria-hidden=\"true\"></span></article>"
    '<footer class="tide-foot mono"><span>MusseJusse / made on the surface</span><span>Hosted on Vercel</span></footer>'
    "</div>"
) % (GH_LINK, BS_LINK, a(R, "Roundest Pokémon"), a(M, "Models"))

# ---------------------------------------------------------------- E: Terminal

GLYPHS = {
    "M": ["█   █", "██ ██", "█ █ █", "█   █", "█   █"],
    "U": ["█   █", "█   █", "█   █", "█   █", " ███ "],
    "S": [" ████", "█    ", " ███ ", "    █", "████ "],
    "E": ["█████", "█    ", "███  ", "█    ", "█████"],
    "J": ["█████", "    █", "    █", "█   █", " ███ "],
}


def ascii_word(word):
    rows = ["" for _ in range(5)]
    for ci, ch in enumerate(word):
        g = GLYPHS[ch]
        for r in range(5):
            rows[r] += g[r] + (" " if ci < len(word) - 1 else "")
    return "\n".join(rows)


ASCII_ART = ascii_word("MUSSEJUSSE")


def bars(n):
    out = []
    for i in range(n):
        h = 20 + (i * 37 % 70)
        out.append('<i style="height:%d%%;animation-delay:%.2fs"></i>' % (h, (i % 7) * 0.13))
    return "".join(out)


TERM_CSS = """
.term{background:#070604;color:#ffb454;padding:2.6cqw 3cqw;font-family:"Space Mono",monospace}
.term .scan{position:absolute;inset:0;background:repeating-linear-gradient(180deg,rgba(0,0,0,.42) 0 1px,transparent 1px 3px);opacity:.55;pointer-events:none;z-index:5}
.term .vig{position:absolute;inset:0;background:radial-gradient(120% 100% at 50% 40%,transparent 55%,rgba(0,0,0,.75));pointer-events:none;z-index:5}
.term .beam{position:absolute;left:0;right:0;top:0;height:16cqw;background:linear-gradient(180deg,transparent,rgba(255,180,84,.14),transparent);animation:scanbeam 6.5s linear infinite;pointer-events:none;z-index:4}
.term .glow{position:absolute;inset:0;background:radial-gradient(70% 50% at 50% 0%,rgba(255,150,40,.14),transparent 70%);pointer-events:none;z-index:1}
.term-inner{position:relative;z-index:3;height:100%;display:flex;flex-direction:column}
.term .status{display:flex;gap:2.4cqw;font-size:.86cqw;color:#c8843a;border-bottom:.12cqw solid rgba(255,180,84,.3);padding-bottom:1cqw}
.term .status b{color:#ffb454;font-weight:400}
.term .status .ok{color:#7bff9e}
.term .ascii{font-size:2.4cqw;line-height:.9;letter-spacing:0;color:#ffbe63;text-shadow:0 0 1.2cqw rgba(255,170,60,.6),0 0 4cqw rgba(255,140,30,.25);white-space:pre;margin:3.4cqw 0 0;animation:flicker 7s linear infinite}
.term .tagline{font-size:1.5cqw;color:#ffd39a;margin-top:2.4cqw}
.term .tagline .caret{display:inline-block;width:.9cqw;height:1.7cqw;background:#ffb454;vertical-align:-.3cqw;margin-left:.4cqw;animation:blink 1.05s steps(1) infinite;box-shadow:0 0 1cqw #ffb454}
.term .grid-head{display:grid;grid-template-columns:6cqw 1.6fr 1fr 1fr 8cqw;gap:1.4cqw;font-size:.72cqw;color:#a86a2c;letter-spacing:.12em;margin-top:4cqw;border-bottom:.12cqw solid rgba(255,180,84,.25);padding-bottom:.8cqw}
.term .proc{display:grid;grid-template-columns:6cqw 1.6fr 1fr 1fr 8cqw;gap:1.4cqw;align-items:center;font-size:1.05cqw;padding:1.2cqw 0;border-bottom:.12cqw solid rgba(255,180,84,.16);color:#f0b877}
.term .proc:hover{background:rgba(255,180,84,.08)}
.term .proc .pid{color:#a86a2c}
.term .proc .name{color:#ffcf94}
.term .proc .state{font-size:.82cqw}
.term .proc .state.run{color:#7bff9e}.term .proc .state.run:before{content:"● ";animation:blink 1.6s steps(1) infinite}
.term .proc .state.ready{color:#ffd166}.term .proc .state.ready:before{content:"○ "}
.term .bar{height:.9cqw;background:rgba(255,180,84,.18);position:relative;overflow:hidden}
.term .bar i{position:absolute;inset:0;transform-origin:left;background:linear-gradient(90deg,#ff9a2e,#ffd166);animation:meter 3.2s ease-in-out infinite}
.term .wave{margin-top:3.4cqw;border:.12cqw solid rgba(255,180,84,.3);padding:1.4cqw;display:flex;align-items:center;gap:2cqw}
.term .wave .lbl{font-size:.72cqw;color:#a86a2c;letter-spacing:.14em;white-space:nowrap}
.term .wave .bars{display:flex;align-items:flex-end;gap:.34cqw;height:5cqw;flex:1}
.term .wave .bars i{flex:1;background:#ffb454;transform-origin:bottom;animation:meter 1.4s ease-in-out infinite;box-shadow:0 0 1cqw rgba(255,170,60,.5)}
.term-foot{margin-top:1.4cqw;display:flex;justify-content:space-between;font-size:.8cqw;color:#c8843a;border-top:.12cqw solid rgba(255,180,84,.3);padding-top:1.2cqw}
.term-foot .prompt{color:#ffcf94}
.term .logs{margin-top:auto;display:flex;flex-direction:column;gap:.7cqw;font-size:.82cqw;color:#a86a2c}
.term .logs b{color:#7bff9e;font-weight:400}
.term .logs i{color:#c8843a;font-style:normal}
.term .promptline{font-size:1.1cqw;color:#ffcf94;margin-top:1.8cqw}
.term .promptline .pc{display:inline-block;width:.9cqw;height:1.5cqw;background:#ffb454;vertical-align:-.22cqw;margin-left:.3cqw;animation:blink 1.05s steps(1) infinite;box-shadow:0 0 1cqw #ffb454}
/* mobile */
.mobile .term{padding:5cqw 5cqw}
.mobile .term .status{font-size:2cqw;gap:5cqw;flex-wrap:wrap;padding-bottom:2.4cqw}
.mobile .term .ascii{font-size:2.02cqw;margin-top:8cqw}
.mobile .term .tagline{font-size:3.9cqw;margin-top:6cqw}
.mobile .term .tagline .caret{width:2.2cqw;height:4.2cqw;vertical-align:-.8cqw}
.mobile .term .grid-head{display:none}
.mobile .term .proc{grid-template-columns:1fr;gap:.6cqw;font-size:3.4cqw;padding:3.4cqw 0;border-bottom-width:.3cqw;border-color:rgba(255,180,84,.25)}
.mobile .term .proc .pid{font-size:2.4cqw}
.mobile .term .proc .state{font-size:2.6cqw}
.mobile .term .bar{height:2.4cqw;margin-top:1.4cqw}
.mobile .term .wave{padding:3cqw;margin-top:6cqw;gap:3cqw;border-width:.3cqw}
.mobile .term .wave .lbl{font-size:2cqw}
.mobile .term .wave .bars{height:12cqw;gap:.8cqw}
.mobile .term-foot{font-size:2.1cqw;padding-top:3cqw;flex-direction:column;gap:1.4cqw}
.mobile .term .logs{font-size:2.1cqw;gap:1.6cqw}
.mobile .term .promptline{font-size:3.2cqw;margin-top:3cqw}
.mobile .term .promptline .pc{width:2.2cqw;height:3.8cqw;vertical-align:-.6cqw}
"""


def proc(pid, name, url, stack, state, cls, pct):
    return (
        '<a class="proc" href="' + url + '" target="_blank" rel="noopener noreferrer">'
        '<span class="pid">' + pid + '</span><span class="name">' + name + '</span><span class="stack">' + stack + "</span>"
        '<span class="state ' + cls + '">' + state + '</span><span class="bar"><i style="width:' + str(pct) + '%"></i></span></a>'
    )


TERM = (
    '<div class="site term">'
    '<span class="glow" aria-hidden="true"></span><span class="beam" aria-hidden="true"></span>'
    '<span class="scan" aria-hidden="true"></span><span class="vig" aria-hidden="true"></span>'
    '<div class="term-inner">'
    '<header class="status"><span><b>mussejusse@web</b>:~$</span><span>TTY1</span><span>UPTIME <b>2Y 114D</b></span><span>LOAD <b>0.42</b></span><span class="ok">● ONLINE</span></header>'
    '<pre class="ascii">' + ASCII_ART + "</pre>"
    '<p class="tagline">&gt; always building, never finished<span class="caret" aria-hidden="true"></span></p>'
    '<div class="grid-head"><span>PID</span><span>PROCESS</span><span>STACK</span><span>STATE</span><span>CPU</span></div>'
    + proc("0001", "roundest_pokemon", R, "NEXT.JS", "RUNNING", "run", 72)
    + proc("0002", "models", M, "ASTRO", "READY", "ready", 38)
    + '<div class="wave"><span class="lbl">SIGNAL / LIVE</span><div class="bars">' + bars(34) + "</div></div>"
    '<div class="logs"><span><b>[ok]</b> roundest_pokemon listening on :3000</span><span><b>[ok]</b> models compiled in 0.81s</span><span><i>[info]</i> 2 experiments, 0 failures, 0 finished</span></div>'
    '<p class="promptline"><span class="prompt">$</span> ls experiments/ <span class="pc" aria-hidden="true"></span></p>'
    '<footer class="term-foot"><span><span class="prompt">$</span> __GH__ __BS__</span><span>hosted on vercel / source on github</span></footer>'
    "</div></div>"
).replace("__GH__", GH_LINK).replace("__BS__", BS_LINK)

# ---------------------------------------------------------------- horology helpers


def _polar(cx, cy, r, ang):
    a = math.radians(ang)
    return (cx + r * math.sin(a), cy - r * math.cos(a))


def _spiral(cx, cy, r0, r1, turns, steps=150):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        r = r0 + (r1 - r0) * t
        pts.append(_polar(cx, cy, r, turns * 360 * t))
    return "M" + "L".join("%.1f %.1f" % p for p in pts)


def _gear(cx, cy, r, teeth, dur, rev=False):
    circ = 2 * math.pi * r
    d = circ / teeth
    return (
        '<g class="spin" style="--ox:%.1fpx;--oy:%.1fpx;--d:%ss;animation-direction:%s">'
        '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#262c36"/>'
        '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#5b6472" stroke-width="%.1f" stroke-dasharray="%.1f %.1f"/>'
        '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#161a20" stroke="#5b6472" stroke-width="2"/>'
        '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#c9a24a" stroke="#8a6d2a" stroke-width="2"/>'
        "</g>"
    ) % (
        cx, cy, dur, "reverse" if rev else "normal",
        cx, cy, r,
        cx, cy, r, max(4.0, r * 0.24), d * 0.58, d * 0.42,
        cx, cy, r * 0.6,
        cx, cy, max(5.0, r * 0.15),
    )


def _hand(cx, cy, r, ang, w, color, tail=0.16):
    x, y = _polar(cx, cy, r, ang)
    dx, dy = x - cx, y - cy
    L = math.hypot(dx, dy)
    px, py = -dy / L * w / 2, dx / L * w / 2
    d = "M%.1f %.1f L%.1f %.1f L%.1f %.1f Z" % (cx + px, cy + py, x, y, cx - px, cy - py)
    bx, by = _polar(cx, cy, -r * tail, ang)
    return (
        '<path d="%s" fill="%s"/>'
        '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>'
    ) % (d, color, bx, by, max(4.0, w * 0.55), color)


def _movement():
    p = ['<svg viewBox="0 0 1000 1000" class="mv-svg" role="img" aria-label="Exhibition caseback with gear train and balance wheel">']
    p.append("<defs>")
    p.append('<radialGradient id="mplate" cx="40%" cy="34%"><stop offset="0" stop-color="#262c36"/><stop offset="55%" stop-color="#191d24"/><stop offset="100%" stop-color="#0e1115"/></radialGradient>')
    p.append('<pattern id="geneva" width="28" height="28" patternUnits="userSpaceOnUse" patternTransform="rotate(38)"><rect width="14" height="28" fill="#232833"/><rect x="14" width="14" height="28" fill="#2d3542"/></pattern>')
    p.append('<pattern id="perlage" width="30" height="30" patternUnits="userSpaceOnUse"><circle cx="9" cy="9" r="8" fill="none" stroke="#2b323d" stroke-width="1.4"/><circle cx="24" cy="24" r="8" fill="none" stroke="#2b323d" stroke-width="1.4"/></pattern>')
    p.append("</defs>")
    p.append('<circle cx="500" cy="500" r="500" fill="url(#mplate)"/>')
    p.append('<circle cx="500" cy="500" r="470" fill="url(#perlage)"/>')
    p.append('<circle cx="500" cy="500" r="372" fill="url(#geneva)"/>')
    p.append('<circle cx="500" cy="500" r="372" fill="none" stroke="#49515f" stroke-width="2.5" opacity=".8"/>')
    p.append('<circle cx="500" cy="500" r="252" fill="url(#perlage)"/>')
    p.append('<circle cx="500" cy="500" r="252" fill="none" stroke="#49515f" stroke-width="2" opacity=".7"/>')
    p.append(_gear(600, 380, 104, 32, 18, False))
    p.append(_gear(724, 556, 76, 24, 13, True))
    p.append(_gear(540, 662, 60, 20, 10, False))
    p.append(_gear(455, 455, 64, 22, 12, True))
    p.append('<g class="balance" style="--ox:360px;--oy:630px">')
    p.append('<circle cx="360" cy="630" r="132" fill="none" stroke="#727b88" stroke-width="15"/>')
    p.append('<circle cx="360" cy="630" r="132" fill="none" stroke="#0e1115" stroke-width="3" opacity=".6"/>')
    for a in (0, 120, 240):
        x, y = _polar(360, 630, 132, a)
        p.append('<line x1="360" y1="630" x2="%.1f" y2="%.1f" stroke="#727b88" stroke-width="9"/>' % (x, y))
    p.append('<circle cx="360" cy="630" r="24" fill="#c9a24a" stroke="#8a6d2a" stroke-width="2.5"/>')
    p.append('<path class="hair" d="%s" fill="none" stroke="#4a68e0" stroke-width="3"/>' % _spiral(360, 630, 28, 124, 7))
    p.append('<circle cx="360" cy="630" r="6" fill="#e05555"/>')
    p.append("</g>")
    for jx, jy in [(600, 380), (724, 556), (540, 662), (455, 455)]:
        p.append('<circle cx="%d" cy="%d" r="10" fill="#e05555" stroke="#c9a24a" stroke-width="3"/>' % (jx, jy))
    for a in (24, 150, 210, 336):
        x, y = _polar(500, 500, 330, a)
        p.append('<g transform="rotate(%d %.1f %.1f)"><circle cx="%.1f" cy="%.1f" r="12" fill="#4a68e0" stroke="#2b3f96" stroke-width="2"/><rect x="%.1f" y="%.1f" width="24" height="3.2" fill="#2b3f96"/></g>' % (a, x, y, x, y, x - 12, y - 1.6))
    p.append('<path id="mveng" d="M212 500 A288 288 0 0 1 788 500" fill="none"/>')
    p.append('<text fill="#98a2b0" font-family="Space Mono, monospace" font-size="25" letter-spacing="7"><textPath href="#mveng" startOffset="50%" text-anchor="middle">MUSSEJUSSE &#183; CALIBRE MJ-01 &#183; SWISS-ISH</textPath></text>')
    p.append('<text x="500" y="905" text-anchor="middle" fill="#727b88" font-family="Space Mono, monospace" font-size="24" letter-spacing="6">No. 0001 / 17 JEWELS</text>')
    p.append("</svg>")
    return "".join(p)


MOVEMENT = _movement()


def _sector_dial():
    p = ['<svg viewBox="0 0 1000 1000" class="sec-svg" role="img" aria-label="Vintage sector dial with small seconds and date">']
    p.append('<defs><radialGradient id="patina" cx="40%" cy="32%"><stop offset="0" stop-color="#f4eee0"/><stop offset="55%" stop-color="#e8e0cd"/><stop offset="100%" stop-color="#d5cbb3"/></radialGradient>')
    p.append('<filter id="lumeglow" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="7" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>')
    p.append('<circle cx="500" cy="500" r="500" fill="url(#patina)"/>')
    p.append('<circle cx="500" cy="500" r="498" fill="none" stroke="#c7bca1" stroke-width="4"/>')
    p.append('<circle cx="500" cy="500" r="455" fill="none" stroke="#1c1915" stroke-width="2.5"/>')
    p.append('<circle cx="500" cy="500" r="410" fill="none" stroke="#1c1915" stroke-width="2.5"/>')
    for i in range(60):
        a = i * 6
        long = i % 5 == 0
        x1, y1 = _polar(500, 500, 410, a)
        x2, y2 = _polar(500, 500, 441 if long else 428, a)
        p.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#1c1915" stroke-width="%.1f"/>' % (x1, y1, x2, y2, 3.2 if long else 1.3))
    for i in range(12):
        if i % 3 == 0:
            continue
        a = i * 30
        x1, y1 = _polar(500, 500, 330, a)
        x2, y2 = _polar(500, 500, 372, a)
        p.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#1c1915" stroke-width="6"/>' % (x1, y1, x2, y2))
    for n, a in [(12, 0), (6, 180), (9, 270)]:
        x, y = _polar(500, 500, 352, a)
        p.append('<text x="%.1f" y="%.1f" text-anchor="middle" dominant-baseline="central" font-family="DM Serif Display, serif" font-size="76" fill="#1c1915">%d</text>' % (x, y + 3, n))
    for a in (0, 120, 240):
        x1, y1 = _polar(500, 500, 252, a)
        x2, y2 = _polar(500, 500, 322, a)
        p.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#1c1915" stroke-width="2.5"/>' % (x1, y1, x2, y2))
    p.append('<circle cx="500" cy="500" r="252" fill="none" stroke="#1c1915" stroke-width="2.5"/>')
    p.append('<text x="500" y="322" text-anchor="middle" font-family="DM Serif Display, serif" font-size="58" fill="#1c1915">MusseJusse</text>')
    p.append('<text x="500" y="360" text-anchor="middle" font-family="Space Mono, monospace" font-size="20" letter-spacing="6" fill="#5a5140">SUR LE WEB</text>')
    p.append('<text x="500" y="575" text-anchor="middle" font-family="Space Mono, monospace" font-size="20" letter-spacing="6" fill="#5a5140">AUTOMATIC</text>')
    p.append('<text x="500" y="946" text-anchor="middle" font-family="Space Mono, monospace" font-size="18" letter-spacing="7" fill="#5a5140">WEB MADE</text>')
    p.append('<polygon points="486,58 514,58 500,100" fill="#bfe9c2" filter="url(#lumeglow)"/>')
    p.append('<circle cx="500" cy="720" r="118" fill="none" stroke="#1c1915" stroke-width="2.5"/>')
    p.append('<circle cx="500" cy="720" r="104" fill="none" stroke="#1c1915" stroke-width="1"/>')
    for i in range(12):
        a = i * 30
        x1, y1 = _polar(500, 720, 104, a)
        x2, y2 = _polar(500, 720, 116, a)
        p.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#1c1915" stroke-width="2"/>' % (x1, y1, x2, y2))
    p.append(_hand(500, 720, 90, 225, 5, "#2b3a8f", 0.2))
    p.append('<circle cx="500" cy="720" r="6" fill="#1c1915"/>')
    p.append('<rect x="790" y="452" width="124" height="96" rx="10" fill="#f4eee0" stroke="#1c1915" stroke-width="3"/>')
    p.append('<text x="852" y="524" text-anchor="middle" font-family="DM Serif Display, serif" font-size="72" fill="#1c1915">26</text>')
    p.append('<text x="852" y="590" text-anchor="middle" font-family="Space Mono, monospace" font-size="17" letter-spacing="4" fill="#5a5140">DATE</text>')
    p.append(_hand(500, 500, 392, 60, 16, "#2b3a8f", 0.14))
    p.append(_hand(500, 500, 268, 305, 20, "#2b3a8f", 0.16))
    p.append('<circle cx="500" cy="500" r="16" fill="#1c1915"/><circle cx="500" cy="500" r="7" fill="#c9a24a"/>')
    p.append("</svg>")
    return "".join(p)


SECTOR = _sector_dial()


def _tachy_dial():
    p = ['<svg viewBox="0 0 1000 1000" class="tach-svg" role="img" aria-label="Panda chronograph dial with tachymeter bezel">']
    p.append('<circle cx="500" cy="500" r="500" fill="#141414"/>')
    p.append('<circle cx="500" cy="500" r="472" fill="none" stroke="#3a3a3a" stroke-width="2"/>')
    p.append('<circle cx="500" cy="500" r="440" fill="none" stroke="#3a3a3a" stroke-width="2"/>')
    vals = [400, 350, 300, 250, 200, 175, 150, 125, 100, 80, 60]
    for i, v in enumerate(vals):
        a = -105 + i * (210 / (len(vals) - 1))
        x1, y1 = _polar(500, 500, 440, a)
        x2, y2 = _polar(500, 500, 456, a)
        p.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#e8e8e8" stroke-width="2"/>' % (x1, y1, x2, y2))
        xt, yt = _polar(500, 500, 412, a)
        p.append('<text x="%.1f" y="%.1f" text-anchor="middle" dominant-baseline="central" font-family="Space Mono, monospace" font-size="26" fill="#e8e8e8">%d</text>' % (xt, yt, v))
    p.append('<circle cx="500" cy="500" r="400" fill="#f4f1ea"/>')
    p.append('<circle cx="500" cy="500" r="400" fill="none" stroke="#141414" stroke-width="2"/>')
    for i in range(60):
        a = i * 6
        long = i % 5 == 0
        x1, y1 = _polar(500, 500, 352, a)
        x2, y2 = _polar(500, 500, 392 if long else 375, a)
        p.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#141414" stroke-width="%.1f"/>' % (x1, y1, x2, y2, 4 if long else 1.4))
    for sx, sy in [(320, 500), (680, 500)]:
        r = 120
        p.append('<circle cx="%d" cy="%d" r="%d" fill="#141414"/>' % (sx, sy, r))
        p.append('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="#555" stroke-width="2"/>' % (sx, sy, r - 10))
        for i in range(12):
            a = i * 30
            x1, y1 = _polar(sx, sy, r - 16, a)
            x2, y2 = _polar(sx, sy, r - 6, a)
            p.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#e8e8e8" stroke-width="1.8"/>' % (x1, y1, x2, y2))
        hx, hy = _polar(sx, sy, r - 26, 45)
        p.append('<line x1="%d" y1="%d" x2="%.1f" y2="%.1f" stroke="#e05555" stroke-width="3"/>' % (sx, sy, hx, hy))
        p.append('<circle cx="%d" cy="%d" r="6" fill="#e8e8e8"/>' % (sx, sy))
    p.append('<circle cx="500" cy="718" r="64" fill="#141414"/>')
    p.append('<circle cx="500" cy="718" r="56" fill="none" stroke="#555" stroke-width="1.6"/>')
    for i in range(12):
        a = i * 30
        x1, y1 = _polar(500, 718, 48, a)
        x2, y2 = _polar(500, 718, 56, a)
        p.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#e8e8e8" stroke-width="1.6"/>' % (x1, y1, x2, y2))
    hx, hy = _polar(500, 718, 44, 140)
    p.append('<line x1="500" y1="718" x2="%.1f" y2="%.1f" stroke="#e8e8e8" stroke-width="2.4"/>' % (hx, hy))
    p.append('<text x="500" y="286" text-anchor="middle" font-family="Space Grotesk, sans-serif" font-weight="700" font-size="46" letter-spacing="10" fill="#141414">MUSSEJUSSE</text>')
    p.append('<text x="500" y="322" text-anchor="middle" font-family="Space Mono, monospace" font-size="19" letter-spacing="6" fill="#141414">AUTOMATIC CHRONOGRAPH</text>')
    p.append('<text x="500" y="906" text-anchor="middle" font-family="Space Mono, monospace" font-size="18" letter-spacing="7" fill="#141414">WEB MADE</text>')
    p.append('<rect x="846" y="620" width="104" height="78" rx="8" fill="#f4f1ea" stroke="#141414" stroke-width="2.5"/>')
    p.append('<text x="898" y="680" text-anchor="middle" font-family="Space Grotesk, sans-serif" font-weight="600" font-size="52" fill="#141414">26</text>')
    p.append(_hand(500, 500, 318, 60, 17, "#141414", 0.14))
    p.append(_hand(500, 500, 216, 305, 21, "#141414", 0.16))
    p.append(_hand(500, 500, 346, 0, 7, "#d13b2e", 0.24))
    p.append('<circle cx="500" cy="500" r="15" fill="#141414"/><circle cx="500" cy="500" r="6" fill="#d13b2e"/>')
    p.append("</svg>")
    return "".join(p)


TACH = _tachy_dial()

# ---------------------------------------------------------------- F / G / H styles

WATCH_CSS = """
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes tick{0%,100%{transform:rotate(-22deg)}50%{transform:rotate(22deg)}}
.spin{transform-box:view-box;transform-origin:var(--ox) var(--oy);animation:spin var(--d,8s) linear infinite}
.balance{transform-box:view-box;transform-origin:var(--ox) var(--oy);animation:tick 1.1s ease-in-out infinite}
.hair{filter:drop-shadow(0 0 3px rgba(74,104,224,.65))}
/* F: exhibition caseback */
.mv{background:radial-gradient(120% 100% at 72% 40%,#1a1e25,#0c0e12 72%);color:#d7dce2;padding:3.4cqw 4cqw;overflow:hidden}
.mv:before{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.04) 1px,transparent 1.5px);background-size:2.4cqw 2.4cqw;opacity:.7}
.mv-caseback{position:absolute;right:1.5cqw;top:50%;transform:translateY(-50%);width:63cqw;height:63cqw;border-radius:50%;overflow:hidden;box-shadow:0 0 0 .5cqw #08090c,0 0 0 .72cqw #39414d,0 2.4cqw 6cqw rgba(0,0,0,.65)}
.mv-caseback:after{content:"";position:absolute;inset:0;border-radius:50%;box-shadow:inset 0 0 7cqw rgba(0,0,0,.7),inset 1.2cqw 1.4cqw 3cqw rgba(255,255,255,.1);z-index:2}
.mv-svg{width:100%;height:100%;display:block}
.mv-left{position:relative;z-index:3;width:33cqw}
.mv-brand{font-family:"Space Grotesk",sans-serif;font-weight:600;font-size:2.5cqw;letter-spacing:.32em;color:#cfd5de;text-shadow:0 1px 0 rgba(0,0,0,.85),0 -1px 0 rgba(255,255,255,.16)}
.mv-sub{font-family:"Space Mono",monospace;font-size:.76cqw;letter-spacing:.22em;color:#7f8896;margin-top:.8cqw}
.mv h1{font-size:4.5cqw;line-height:1.03;letter-spacing:-.02em;margin-top:2.8cqw;font-weight:600}
.mv h1 em{font-style:normal;color:#c9a24a}
.mv p{font-size:1cqw;color:#96a0ae;margin-top:1.5cqw;max-width:30cqw;line-height:1.55}
.mv-specs{display:grid;grid-template-columns:repeat(4,1fr);gap:1.4cqw;margin-top:2.6cqw;border-top:1px solid #2a303a;border-bottom:1px solid #2a303a;padding:1.3cqw 0}
.mv-specs span{display:block;font-family:"Space Mono",monospace;font-size:.62cqw;letter-spacing:.16em;color:#7f8896}
.mv-specs b{display:block;font-family:"Space Mono",monospace;font-weight:400;font-size:1cqw;color:#d7dce2;margin-top:.35cqw}
.mv-comp{margin-top:2.6cqw;display:grid;gap:1.2cqw}
.mv-comp a{display:grid;grid-template-columns:auto 1fr auto;gap:.9cqw;align-items:baseline;border:1px solid #2a303a;padding:1.1cqw 1.3cqw;background:linear-gradient(180deg,rgba(255,255,255,.035),rgba(255,255,255,0))}
.mv-comp a:hover{border-color:#c9a24a}
.mv-comp .n{font-family:"Space Mono",monospace;font-size:.7cqw;color:#c9a24a;letter-spacing:.08em}
.mv-comp .t{display:block;font-size:1.1cqw}
.mv-comp .d{display:block;font-family:"Space Mono",monospace;font-size:.66cqw;color:#7f8896;letter-spacing:.06em;margin-top:.3cqw}
.mv-comp .go{font-size:1.2cqw;color:#c9a24a}
.mv-foot{position:absolute;left:4cqw;right:4cqw;bottom:1.8cqw;display:flex;justify-content:space-between;font-family:"Space Mono",monospace;font-size:.7cqw;color:#6b7480;z-index:3}
.mv-crown{position:absolute;right:.5cqw;top:50%;width:1.7cqw;height:5.6cqw;transform:translateY(-50%);border-radius:.3cqw;background:repeating-linear-gradient(90deg,#3a4048 0 2px,#20242c 2px 4px);box-shadow:0 0 1.2cqw #000;z-index:4}
.mv-crown:before{content:"";position:absolute;left:-.5cqw;top:50%;transform:translateY(-50%);width:.7cqw;height:2.6cqw;background:#20242c;border-radius:.2cqw}
/* G: sector dial */
.sec{background:#efe8d8;color:#1c1915;padding:3.2cqw 4cqw;overflow:hidden}
.sec:before{content:"";position:absolute;inset:0;background:repeating-conic-gradient(from 0deg at 50% 36%,rgba(0,0,0,.018) 0deg 1deg,transparent 1deg 2deg);opacity:.6}
.sec-dial{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:50cqw;height:50cqw;border-radius:50%;overflow:hidden;box-shadow:0 0 0 .38cqw #b2a68c,0 1.6cqw 3.4cqw rgba(70,58,36,.28)}
.sec-svg{width:100%;height:100%;display:block}
.sec-top{position:absolute;top:3.2cqw;left:4cqw;right:4cqw;display:flex;justify-content:space-between;font-family:"Space Mono",monospace;font-size:.76cqw;letter-spacing:.16em;z-index:3}
.sec-top nav{display:flex;gap:2.4cqw}
.sec-bio{position:absolute;left:4cqw;bottom:6.4cqw;width:17cqw;z-index:3}
.sec-bio .eyebrow{font-family:"Space Mono",monospace;font-size:.68cqw;letter-spacing:.2em;color:#96896c}
.sec-bio p{font-size:1.02cqw;line-height:1.5;margin-top:.9cqw;color:#4a4234}
.sec-reg{position:absolute;right:4cqw;bottom:6.4cqw;width:19cqw;display:grid;gap:1.1cqw;z-index:3}
.sec-reg a{border-top:1px solid #1c1915;padding-top:.85cqw;display:block}
.sec-reg a:hover{color:#9a5a1e}
.sec-reg .mono{font-family:"Space Mono",monospace;font-size:.62cqw;letter-spacing:.14em;color:#96896c}
.sec-reg h3{font-family:"DM Serif Display",serif;font-size:1.55cqw;margin-top:.25cqw}
.sec-reg p{font-size:.76cqw;color:#6a6151;margin-top:.2cqw}
.sec-foot{position:absolute;left:4cqw;right:4cqw;bottom:1.5cqw;display:flex;justify-content:space-between;font-family:"Space Mono",monospace;font-size:.66cqw;color:#96896c;z-index:3}
/* H: chronograph */
.tach{background:#f4f1ea;color:#141414;padding:3.2cqw 4cqw;overflow:hidden}
.tach-dial{position:absolute;left:1.5cqw;top:50%;transform:translateY(-50%);width:57cqw;height:57cqw}
.tach-svg{width:100%;height:100%;display:block}
.tach-sub{position:absolute;top:50%;transform:translate(-50%,-50%);width:22%;text-align:center;color:#e8e8e8;text-decoration:none}
.tach-sub .mono{font-family:"Space Mono",monospace;font-size:.6cqw;letter-spacing:.08em;color:#e05555}
.tach-sub h3{font-size:1.12cqw;margin-top:.35cqw;line-height:1.12}
.tach-sub .go{display:block;font-size:.95cqw;margin-top:.3cqw;color:#e8e8e8}
.tach-copy{position:absolute;right:4cqw;top:50%;transform:translateY(-50%);width:34cqw;z-index:3}
.tach-copy .eyebrow{font-family:"Space Mono",monospace;font-size:.72cqw;letter-spacing:.2em;color:#8a8378}
.tach-copy h1{font-size:4.9cqw;line-height:1;letter-spacing:-.03em;margin-top:1.4cqw;font-weight:700;text-transform:uppercase}
.tach-copy h1 em{font-style:normal;color:#d13b2e}
.tach-copy p{font-size:1.02cqw;color:#57514a;margin-top:1.4cqw;max-width:30cqw;line-height:1.55}
.tach-meta{display:grid;grid-template-columns:1fr 1fr;gap:1.2cqw 2cqw;margin-top:2.2cqw;border-top:1px solid #d8d2c6;padding-top:1.4cqw}
.tach-meta span{font-family:"Space Mono",monospace;font-size:.62cqw;letter-spacing:.16em;color:#8a8378}
.tach-meta b{display:block;font-family:"Space Mono",monospace;font-weight:400;font-size:.95cqw;color:#141414;margin-top:.3cqw}
.tach-foot{position:absolute;right:4cqw;bottom:1.8cqw;font-family:"Space Mono",monospace;font-size:.68cqw;color:#8a8378;z-index:3}
.tach-foot a{color:#141414}
/* mobile */
.mobile .mv{padding:6cqw}
.mobile .mv:before{background-size:6cqw 6cqw}
.mobile .mv-crown{right:5cqw;top:40cqw;height:11cqw;width:3cqw}
.mobile .mv-crown:before{width:1.4cqw;height:5cqw;left:-1cqw}
.mobile .mv-caseback{position:static;transform:none;width:86cqw;height:86cqw;margin:0 auto}
.mobile .mv-left{width:auto;padding-top:9cqw}
.mobile .mv-brand{font-size:4.6cqw}
.mobile .mv-sub{font-size:1.9cqw}
.mobile .mv h1{font-size:10.5cqw;margin-top:5cqw}
.mobile .mv p{font-size:3.1cqw;max-width:none;margin-top:4cqw}
.mobile .mv-specs{grid-template-columns:1fr 1fr;gap:3cqw 4cqw;padding:3cqw 0;margin-top:6cqw}
.mobile .mv-specs span{font-size:1.7cqw}
.mobile .mv-specs b{font-size:2.9cqw}
.mobile .mv-comp{margin-top:6cqw;gap:3cqw}
.mobile .mv-comp a{padding:3cqw;gap:2cqw}
.mobile .mv-comp .n{font-size:1.9cqw}
.mobile .mv-comp .t{font-size:3.5cqw}
.mobile .mv-comp .d{font-size:1.9cqw}
.mobile .mv-comp .go{font-size:3.4cqw}
.mobile .mv-foot{position:static;margin-top:8cqw;font-size:1.9cqw;flex-direction:column;gap:1.4cqw}
.mobile .sec{padding:6cqw}
.mobile .sec-top{position:static;display:flex;justify-content:space-between;font-size:2.1cqw;margin-bottom:2cqw}
.mobile .sec-dial{position:static;transform:none;width:88cqw;height:88cqw;margin:2cqw auto 0}
.mobile .sec-bio{position:static;width:auto;margin-top:9cqw}
.mobile .sec-bio .eyebrow{font-size:1.9cqw}
.mobile .sec-bio p{font-size:3.3cqw;margin-top:2cqw}
.mobile .sec-reg{position:static;width:auto;margin-top:9cqw;gap:4cqw}
.mobile .sec-reg .mono{font-size:1.8cqw}
.mobile .sec-reg h3{font-size:5.2cqw}
.mobile .sec-reg p{font-size:2.8cqw}
.mobile .sec-foot{position:static;margin-top:9cqw;font-size:1.8cqw;flex-direction:column;gap:1.4cqw}
.mobile .tach{padding:6cqw}
.mobile .tach-dial{position:static;transform:none;width:90cqw;height:90cqw;margin:0 auto}
.mobile .tach-sub{width:24%}
.mobile .tach-sub .mono{font-size:1.8cqw}
.mobile .tach-sub h3{font-size:3.3cqw}
.mobile .tach-sub .go{font-size:3cqw}
.mobile .tach-copy{position:static;transform:none;width:auto;margin-top:9cqw}
.mobile .tach-copy .eyebrow{font-size:2cqw}
.mobile .tach-copy h1{font-size:11cqw;margin-top:3cqw}
.mobile .tach-copy p{font-size:3.2cqw;max-width:none;margin-top:4cqw}
.mobile .tach-meta{margin-top:6cqw;gap:3cqw 4cqw;padding-top:3cqw}
.mobile .tach-meta span{font-size:1.7cqw}
.mobile .tach-meta b{font-size:2.9cqw}
.mobile .tach-foot{position:static;margin-top:8cqw;font-size:1.9cqw}
"""

MOVEMENT_DIR = (
    '<div class="site mv">'
    '<div class="mv-caseback" aria-hidden="true">' + MOVEMENT + "</div>"
    '<span class="mv-crown" aria-hidden="true"></span>'
    '<div class="mv-left">'
    '<div class="mv-brand">MUSSEJUSSE</div>'
    '<div class="mv-sub">CALIBRE MJ-01 / No. 0001</div>'
    "<h1>Always building.<br><em>Never finished.</em></h1>"
    "<p>I'm Musse. By day I build for the web, by night I take movements apart and occasionally get them back together. This is the running log.</p>"
    '<div class="mv-specs">'
    "<span>JEWELS<b>17</b></span><span>FREQUENCY<b>4 Hz</b></span>"
    "<span>RESERVE<b>38 H</b></span><span>WATER<b>100 M</b></span>"
    "</div>"
    '<div class="mv-comp">'
    '<a href="' + R + '" target="_blank" rel="noopener noreferrer"><span class="n">01</span>'
    '<span><span class="t">Roundest Pok&eacute;mon</span><span class="d">MOONPHASE COMPLICATION</span></span><span class="go">&#8599;</span></a>'
    '<a href="' + M + '" target="_blank" rel="noopener noreferrer"><span class="n">02</span>'
    '<span><span class="t">Models</span><span class="d">ANNUAL CALENDAR COMPLICATION</span></span><span class="go">&#8599;</span></a>'
    "</div></div>"
    '<footer class="mv-foot"><span>SAPPHIRE CASE BACK / SERVICED 2026</span><span>' + GH_LINK + " &middot; " + BS_LINK + "</span></footer>"
    "</div>"
)

SECTOR_DIR = (
    '<div class="site sec">'
    '<header class="sec-top"><span>MUSSEJUSSE / GEN&Egrave;VE</span><nav>' + GH_LINK + " " + BS_LINK + "</nav></header>"
    '<div class="sec-dial" aria-hidden="true">' + SECTOR + "</div>"
    '<div class="sec-bio"><span class="eyebrow">REF. MJ-02 / SECTOR</span>'
    "<p>I collect old watches and build small sites. Both reward patience and a steady hand.</p></div>"
    '<section class="sec-reg">'
    '<a href="' + R + '" target="_blank" rel="noopener noreferrer"><span class="mono">01 / SMALL SECONDS</span>'
    "<h3>Roundest Pok&eacute;mon</h3><p>Which one is rounder?</p></a>"
    '<a href="' + M + '" target="_blank" rel="noopener noreferrer"><span class="mono">02 / DATE</span>'
    "<h3>Models</h3><p>The model catalogue, pared back.</p></a>"
    "</section>"
    '<footer class="sec-foot"><span>SWISS-ISH MOVEMENT / WEB MADE</span><span>A work in progress</span></footer>'
    "</div>"
)

TACH_DIR = (
    '<div class="site tach">'
    '<div class="tach-dial">' + TACH
    + '<a class="tach-sub" style="left:32%" href="' + R + '" target="_blank" rel="noopener noreferrer">'
    '<span class="mono">COMPLICATION 01</span><h3>Roundest<br>Pok&eacute;mon</h3><span class="go">&#8599;</span></a>'
    + '<a class="tach-sub" style="left:68%" href="' + M + '" target="_blank" rel="noopener noreferrer">'
    '<span class="mono">COMPLICATION 02</span><h3>Models</h3><span class="go">&#8599;</span></a>'
    + "</div>"
    '<div class="tach-copy"><span class="eyebrow">REF. MJ-03 / CHRONOGRAPH</span>'
    "<h1>Built to be<br>worn. <em>Wound<br>daily.</em></h1>"
    "<p>Two complications, no compromises. A roundness question and a model catalogue, timed to the second.</p>"
    '<div class="tach-meta">'
    "<span>PUSHERS<b>2</b></span><span>TACHYMETER<b>60-400</b></span>"
    "<span>CASE<b>STEEL</b></span><span>CRYSTAL<b>SAPPHIRE</b></span>"
    "</div></div>"
    '<footer class="tach-foot"><a href="' + GH + '" target="_blank" rel="noopener noreferrer">GitHub</a> &middot; <a href="' + BS + '" target="_blank" rel="noopener noreferrer">Bluesky</a></footer>'
    "</div>"
)

# ---------------------------------------------------------------- review chrome

CHROME_CSS = """
:root{--ink:#f4f3ef;--dim:#8d8d88;--line:#242427;--bg:#050506}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 "Space Grotesk",system-ui,sans-serif;-webkit-font-smoothing:antialiased}
.wrap{max-width:1760px;margin:0 auto;padding:0 clamp(16px,3vw,52px) 120px}
.rtop{position:sticky;top:0;z-index:100;background:rgba(5,5,6,.78);backdrop-filter:blur(16px);border-bottom:1px solid var(--line)}
.rtop .row{max-width:1760px;margin:0 auto;padding:14px clamp(16px,3vw,52px);display:flex;justify-content:space-between;align-items:center;gap:20px}
.rtop h1{font-size:14px;font-weight:500;letter-spacing:.01em}
.rtop .row>span{font-family:"Space Mono",monospace;font-size:11px;color:var(--dim);letter-spacing:.06em}
.rnav{display:flex;gap:6px}
.rnav a{font-family:"Space Mono",monospace;font-size:11px;letter-spacing:.08em;padding:6px 11px;border:1px solid var(--line);color:var(--ink);text-decoration:none;transition:background 160ms ease-out,color 160ms ease-out}
.rnav a:hover{background:var(--ink);color:#000}
.intro{padding:64px 0 8px;max-width:74ch}
.intro .k{font-family:"Space Mono",monospace;font-size:11px;letter-spacing:.22em;color:var(--dim)}
.intro h2{font-size:clamp(30px,4.4vw,58px);line-height:1.02;letter-spacing:-.03em;font-weight:500;margin:14px 0 0}
.intro h2 em{font-family:"DM Serif Display",Georgia,serif;font-style:italic;font-weight:400}
.intro p{color:var(--dim);margin-top:18px;font-size:15.5px}
.direction{padding-top:76px;scroll-margin-top:70px}
.revdivider{margin-top:96px;padding-top:22px;border-top:1px solid var(--line);font-family:"Space Mono",monospace;font-size:11px;letter-spacing:.26em;color:var(--dim)}
.dhead{display:grid;grid-template-columns:auto 1fr;gap:8px 28px;align-items:baseline;border-top:1px solid var(--line);padding-top:20px}
.dhead .letter{font-family:"Space Mono",monospace;font-size:12px;color:var(--dim);letter-spacing:.1em;grid-row:1 / span 2}
.dhead h2{font-size:clamp(24px,3vw,38px);font-weight:500;letter-spacing:-.025em}
.dhead p{color:var(--dim);font-size:14px;max-width:70ch}
.views{display:grid;grid-template-columns:minmax(0,1440fr) minmax(0,390fr);gap:30px;align-items:start;margin-top:26px}
.view{min-width:0}
.vlabel{display:flex;justify-content:space-between;gap:12px;font-family:"Space Mono",monospace;font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;color:var(--dim);margin-bottom:9px}
.vlabel b{color:var(--ink);font-weight:400}
.rfoot{margin-top:96px;border-top:1px solid var(--line);padding-top:22px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:14px;color:var(--dim);font-size:13px}.rfoot a{color:var(--ink)}
@media(max-width:1180px){
  .views{grid-template-columns:minmax(0,1fr)}
  .view.mobile{width:min(100%,390px)}
  .dhead{grid-template-columns:auto 1fr}
}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
"""

# ================================================================ round two
# B (Riso) is kept. Everything below replaces the other seven directions.

SPEC_CSS = """
.spc{background:#f3f1ea;color:#141414;padding:3cqw 4cqw;overflow:hidden;--wght:430;--ls:-.02em}
.spc .base{position:absolute;inset:0;background-image:repeating-linear-gradient(180deg,transparent 0 4.4cqw,rgba(20,20,20,.05) 4.4cqw 4.47cqw)}
.spc-top{position:relative;z-index:4;display:flex;justify-content:space-between;align-items:baseline;font-family:"Space Mono",monospace;font-size:.76cqw;letter-spacing:.14em}
.spc-top nav{display:flex;gap:2.4cqw}
.spc .lead{position:absolute;left:4cqw;top:8.8cqw;z-index:4;font-family:"Space Mono",monospace;font-size:.72cqw;letter-spacing:.2em;color:#2b2bff}
.spc-word{position:absolute;left:3.6cqw;top:12cqw;z-index:2;font-family:"Inter",sans-serif;font-weight:400;font-variation-settings:'wght' var(--wght);font-size:18.6cqw;line-height:.82;letter-spacing:var(--ls);text-transform:uppercase}
.spc-word span{display:block}
.spc-read{position:absolute;right:4cqw;top:13cqw;z-index:4;font-family:"Space Mono",monospace;font-size:.74cqw;line-height:2;text-align:right;color:#5c5c56}
.spc-read b{color:#2b2bff;font-weight:400}
.spc-glyphs{position:absolute;left:4cqw;top:45cqw;width:52cqw;z-index:4;font-family:"Inter",sans-serif;font-variation-settings:'wght' var(--wght);font-size:.92cqw;line-height:1.6;letter-spacing:.02em;color:#3a3a36}
.spc-work{position:absolute;left:4cqw;right:4cqw;bottom:5.2cqw;display:grid;grid-template-columns:1fr 1fr;gap:3cqw;border-top:1.3px solid #141414;padding-top:1.5cqw;z-index:4}
.spc-work a{display:grid;grid-template-columns:auto 1fr;gap:1.4cqw;align-items:center}
.spc-work .g{font-family:"Inter",sans-serif;font-variation-settings:'wght' var(--wght);font-size:5.6cqw;line-height:.85}
.spc-work h3{font-size:1.5cqw;letter-spacing:-.01em}
.spc-work .mono{font-family:"Space Mono",monospace;font-size:.7cqw;color:#6b6b64;margin-top:.5cqw;letter-spacing:.06em}
.spc-foot{position:absolute;left:4cqw;right:4cqw;bottom:1.5cqw;display:flex;justify-content:space-between;font-family:"Space Mono",monospace;font-size:.7cqw;color:#8a8a82;z-index:4}
.mobile .spc{padding:6cqw}
.mobile .spc .base{display:none}
.mobile .spc-top{font-size:2.1cqw}
.mobile .spc-top nav{gap:5cqw}
.mobile .spc .lead{position:static;font-size:1.9cqw;margin-top:2cqw}
.mobile .spc-word{position:static;font-size:23cqw;margin-top:6cqw}
.mobile .spc-read{position:static;text-align:left;font-size:2cqw;margin-top:7cqw}
.mobile .spc-glyphs{position:static;width:auto;font-size:2.6cqw;margin-top:6cqw}
.mobile .spc-work{position:static;grid-template-columns:1fr;gap:6cqw;margin-top:9cqw;padding-top:4cqw;border-top-width:2px}
.mobile .spc-work .g{font-size:13cqw}
.mobile .spc-work h3{font-size:4.6cqw}
.mobile .spc-work .mono{font-size:1.9cqw}
.mobile .spc-foot{position:static;margin-top:9cqw;font-size:1.9cqw}
"""

VIT_CSS = """
.vit{background:#0c0b0a;color:#efe7d8;overflow:hidden;perspective:1700px;padding:3cqw 4cqw}
.vit-scene{position:absolute;inset:-8% -6%;transform-style:preserve-3d;transform:rotateX(var(--rx,3deg)) rotateY(var(--ry,-7deg))}
.vit-wall{position:absolute;inset:0;transform:translateZ(-48cqw);background:linear-gradient(180deg,#322a23,#161210 80%);box-shadow:inset 0 0 24cqw rgba(0,0,0,.7)}
.vit-floor{position:absolute;left:-40%;right:-40%;bottom:-8%;height:80%;transform:rotateX(75deg);transform-origin:bottom center;background:linear-gradient(#241f19,#0a0908 72%)}
.vit-pool{position:absolute;left:15%;top:14%;width:24cqw;height:32cqw;transform:translateZ(-47.4cqw);background:radial-gradient(closest-side,rgba(255,214,160,.4),transparent);filter:blur(1.2cqw)}
.vit-pool.two{left:49%}
.vit-work{position:absolute;width:22cqw;transform:translateZ(-44cqw)}
.vit-work.one{left:16%}
.vit-work.two{left:51%}
.vit-frame{border:.7cqw solid #4a3a2c;background:#080706;padding:.7cqw;box-shadow:0 2.6cqw 5cqw rgba(0,0,0,.7);position:relative}
.vit-canvas{aspect-ratio:4/5;position:relative;overflow:hidden}
.vit-canvas.blue{background:radial-gradient(circle at 50% 44%,#0d1c3e,#050a18)}
.vit-canvas.blue:before{content:"";position:absolute;left:50%;top:44%;width:12cqw;height:12cqw;transform:translate(-50%,-50%);border-radius:50%;background:radial-gradient(circle at 38% 32%,#fff,#9db4e8 46%,#3a4f8a);box-shadow:0 0 3cqw rgba(200,220,255,.65)}
.vit-canvas.blue:after{content:"";position:absolute;inset:0;background:repeating-radial-gradient(circle at 50% 44%,transparent 0 1.3cqw,rgba(160,190,255,.22) 1.3cqw 1.42cqw)}
.vit-canvas.ochre{background:linear-gradient(160deg,#3b2d18,#1b1308)}
.vit-canvas.ochre:before{content:"";position:absolute;inset:12% 14%;background-image:linear-gradient(rgba(255,209,130,.55) 1px,transparent 1px),linear-gradient(90deg,rgba(255,209,130,.55) 1px,transparent 1px);background-size:2.3cqw 2.3cqw}
.vit-plaque{margin-top:1.1cqw;background:#e9e0cf;color:#15110d;padding:.9cqw 1cqw;font-family:"Space Mono",monospace}
.vit-plaque h3{font-size:1.05cqw;letter-spacing:.01em}
.vit-plaque p{font-size:.66cqw;color:#5a5145;margin-top:.35cqw;line-height:1.45}
.vit-plaque a{color:#0b3fa8}
.vit-light{position:absolute;inset:0;z-index:2;pointer-events:none;background:radial-gradient(46cqw 38cqw at var(--mx,62%) var(--my,24%),rgba(255,216,164,.2),transparent 62%)}
.vit-top{position:absolute;top:3cqw;left:4cqw;right:4cqw;z-index:5;display:flex;justify-content:space-between;font-family:"Space Mono",monospace;font-size:.74cqw;letter-spacing:.14em;color:#cbbfa8}
.vit-top nav{display:flex;gap:2.4cqw}
.vit-guide{position:absolute;left:4cqw;bottom:4cqw;z-index:5;width:27cqw;background:rgba(10,9,8,.72);border:1px solid rgba(220,205,180,.24);padding:1.6cqw;backdrop-filter:blur(6px)}
.vit-guide .mono{font-family:"Space Mono",monospace;font-size:.64cqw;letter-spacing:.2em;color:#9c8f78}
.vit-guide h1{font-family:"DM Serif Display",serif;font-size:2.7cqw;line-height:1.02;margin-top:.8cqw}
.vit-guide p{font-size:.82cqw;color:#cbbfa8;margin-top:.9cqw;line-height:1.5}
.vit-guide .list{margin-top:1.3cqw;border-top:1px solid rgba(220,205,180,.2);padding-top:1cqw;display:grid;gap:.7cqw}
.vit-guide .list span{font-size:.74cqw;display:flex;justify-content:space-between;color:#cbbfa8;font-family:"Space Mono",monospace}
.mobile .vit{padding:0;perspective:none}
.mobile .vit-scene{position:static;inset:0;transform:none}
.mobile .vit-wall,.mobile .vit-floor,.mobile .vit-pool,.mobile .vit-light{display:none}
.mobile .vit-top{position:static;padding:6cqw 6cqw 0;font-size:2cqw;color:#cbbfa8}
.mobile .vit-work{position:static;width:auto;transform:none;margin:9cqw 6cqw 0}
.mobile .vit-frame{border-width:1.4cqw;padding:1.4cqw}
.mobile .vit-canvas.blue:before{width:36cqw;height:36cqw}
.mobile .vit-canvas.ochre:before{background-size:6cqw 6cqw}
.mobile .vit-plaque{margin-top:2.4cqw;padding:2.6cqw}
.mobile .vit-plaque h3{font-size:3.8cqw}
.mobile .vit-plaque p{font-size:2.3cqw}
.mobile .vit-guide{position:static;width:auto;margin:9cqw 6cqw 0;padding:5cqw}
.mobile .vit-guide .mono{font-size:1.7cqw}
.mobile .vit-guide h1{font-size:7.4cqw}
.mobile .vit-guide p{font-size:2.9cqw}
.mobile .vit-guide .list span{font-size:2.1cqw}
"""

FOIL_CSS = """
.foil{background:radial-gradient(130% 100% at 50% -8%,#23264a,#0a0b14 68%);color:#f4f1ea;padding:3cqw 4cqw;overflow:hidden}
.foil-top{position:relative;z-index:4;display:flex;justify-content:space-between;font-family:"Space Mono",monospace;font-size:.74cqw;letter-spacing:.16em;color:#a9a6c9}
.foil-top nav{display:flex;gap:2.4cqw}
.foil-title{position:absolute;left:0;right:0;bottom:4cqw;text-align:center;font-family:"Anton",sans-serif;font-size:3.4cqw;letter-spacing:.02em;text-transform:uppercase;color:rgba(244,241,234,.5);z-index:3}
.foil-deck{position:absolute;left:0;right:0;top:11.5cqw;display:flex;justify-content:center;gap:4.4cqw;perspective:1500px}
.foil .card{width:33cqw;aspect-ratio:.716;position:relative;border-radius:1.8cqw;padding:1.3cqw;transform-style:preserve-3d;transform:rotateX(var(--rx,0deg)) rotateY(var(--ry,0deg)) rotate(var(--rot,0deg));box-shadow:0 3cqw 6cqw rgba(0,0,0,.55);will-change:transform}
.foil .card.pink{--rot:-1.8deg;background:linear-gradient(150deg,#f7cddb,#e88aa8 52%,#c35a83)}
.foil .card.blue{--rot:1.6deg;background:linear-gradient(150deg,#c3d4f4,#7fa3e0 52%,#4a6fbd)}
.foil .inner{position:absolute;inset:1.1cqw;border-radius:1.2cqw;background:#0e0f17;overflow:hidden;padding:1.2cqw;display:flex;flex-direction:column}
.foil .hbar{display:flex;justify-content:space-between;align-items:baseline}
.foil .hbar h3{font-family:"Space Grotesk",sans-serif;font-weight:700;font-size:1.55cqw;letter-spacing:.01em;text-transform:uppercase}
.foil .hp{font-family:"Space Mono",monospace;font-size:1.05cqw;color:#ffd166}
.foil .art{flex:1;margin:1cqw 0;border-radius:.8cqw;position:relative;overflow:hidden}
.foil .art.orb{background:radial-gradient(circle at 40% 32%,#4b5bd6,#161c3f 72%)}
.foil .art.orb:before{content:"";position:absolute;left:50%;top:54%;width:11cqw;height:11cqw;transform:translate(-50%,-50%);border-radius:50%;background:radial-gradient(circle at 38% 32%,#fff,#cdd6ff 46%,#7f8fe0);box-shadow:0 0 2cqw rgba(200,215,255,.7)}
.foil .art.orb:after{content:"";position:absolute;left:50%;top:50%;width:1.4cqw;height:1.4cqw;margin:-.7cqw;border-radius:50%;background:#0b0d18;box-shadow:2.4cqw 0 0 #0b0d18}
.foil .art.grid{background:linear-gradient(160deg,#2a3550,#101625)}
.foil .art.grid:before{content:"";position:absolute;inset:16%;background-image:linear-gradient(rgba(150,180,240,.65) 1px,transparent 1px),linear-gradient(90deg,rgba(150,180,240,.65) 1px,transparent 1px);background-size:1.6cqw 1.6cqw}
.foil .art.grid:after{content:"";position:absolute;left:22%;top:30%;width:26%;height:40%;background:rgba(150,180,240,.85);box-shadow:3.4cqw 0 0 rgba(150,180,240,.5),6.8cqw 0 0 rgba(150,180,240,.3)}
.foil .type{font-family:"Space Mono",monospace;font-size:.7cqw;letter-spacing:.1em;color:#a9a6c9}
.foil .moves{margin-top:.8cqw;display:grid;gap:.55cqw}
.foil .move{font-size:.8cqw;color:#ded9f0;display:grid;grid-template-columns:auto 1fr;gap:.7cqw;line-height:1.35}
.foil .move b{font-family:"Space Mono",monospace;font-size:.68cqw;color:#ffd166}
.foil .foot{margin-top:auto;display:flex;justify-content:space-between;font-family:"Space Mono",monospace;font-size:.64cqw;color:#8b88ad;padding-top:.7cqw}
.foil .holo{position:absolute;inset:0;border-radius:inherit;pointer-events:none;mix-blend-mode:color-dodge;opacity:.42;background:conic-gradient(from 210deg at var(--mx,50%) var(--my,50%),#ff9ad5,#ffe38a,#8affd0,#8ab6ff,#c98aff,#ff9ad5)}
.foil .glare{position:absolute;inset:0;border-radius:inherit;pointer-events:none;mix-blend-mode:screen;background:radial-gradient(28cqw 22cqw at var(--mx,50%) var(--my,40%),rgba(255,255,255,.4),transparent 60%)}
.mobile .foil{padding:6cqw}
.mobile .foil-top{font-size:2cqw}
.mobile .foil-deck{position:static;flex-direction:column;align-items:center;gap:8cqw;margin-top:9cqw}
.mobile .foil .card{width:78cqw;border-radius:4cqw;padding:2.6cqw;transform:none}
.mobile .foil .inner{inset:2.4cqw;border-radius:2.8cqw;padding:3cqw}
.mobile .foil .hbar h3{font-size:4cqw}
.mobile .foil .hp{font-size:2.6cqw}
.mobile .foil .art.orb:before{width:28cqw;height:28cqw}
.mobile .foil .art.orb:after{width:3.4cqw;height:3.4cqw;margin:-1.7cqw;box-shadow:6cqw 0 0 #0b0d18}
.mobile .foil .art.grid:before{background-size:4cqw 4cqw}
.mobile .foil .art.grid:after{box-shadow:8cqw 0 0 rgba(150,180,240,.5),16cqw 0 0 rgba(150,180,240,.3)}
.mobile .foil .type{font-size:1.9cqw}
.mobile .foil .move{font-size:2.7cqw;gap:2cqw}
.mobile .foil .move b{font-size:1.9cqw}
.mobile .foil .foot{font-size:1.8cqw}
.mobile .foil-title{position:static;text-align:left;font-size:9cqw;margin-top:9cqw}
"""

LINE_CSS = """
.line{background:#f6f4ef;color:#0f0f0f;padding:3cqw 4cqw;overflow:hidden}
.line-top{position:relative;z-index:4;display:flex;justify-content:space-between;align-items:center;font-family:"Space Mono",monospace;font-size:.74cqw;letter-spacing:.12em}
.line-top .brand{display:flex;align-items:center;gap:1cqw;font-family:"Space Grotesk",sans-serif;font-weight:700;font-size:1.5cqw;letter-spacing:-.01em}
.line-top .brand .roundel{width:2.2cqw;height:2.2cqw;border-radius:50%;background:#e2231a;color:#fff;display:grid;place-content:center;font-family:"Space Mono",monospace;font-size:.9cqw}
.line-top nav{display:flex;gap:2.4cqw;align-items:center}
.line-map{position:absolute;left:4cqw;right:4cqw;top:31cqw;height:18cqw;z-index:2}
.line-track{position:absolute;left:0;right:0;top:50%;height:.55cqw;background:#e2231a;border-radius:.3cqw}
.line-track:after{content:"";position:absolute;left:0;right:0;top:-2.2cqw;height:.2cqw;background:repeating-linear-gradient(90deg,#0f0f0f 0 .18cqw,transparent .18cqw 1.4cqw);opacity:.22}
.line-station{position:absolute;top:50%;transform:translate(-50%,-50%);width:2cqw;height:2cqw;border-radius:50%;background:#f6f4ef;border:.42cqw solid #e2231a;z-index:3;display:block}
.line-station.major{width:2.8cqw;height:2.8cqw;border-width:.72cqw}
.line-station.interchange{background:#0f0f0f;border-color:#0f0f0f;box-shadow:inset 0 0 0 .5cqw #f6f4ef}
.line-station.s1{left:3%}.line-station.s2{left:16%}.line-station.s3{left:27%}.line-station.s4{left:39%}
.line-station.s5{left:50%}.line-station.s6{left:63%}.line-station.s7{left:74%}.line-station.s8{left:88%}
.line-title{position:absolute;left:4cqw;top:10.5cqw;z-index:3;font-family:"Space Grotesk",sans-serif;font-weight:700;font-size:5.6cqw;line-height:1;letter-spacing:-.03em;text-transform:uppercase;color:#0f0f0f}
.line-station .name{position:absolute;left:50%;top:-2.5cqw;transform:translateX(-50%);white-space:nowrap;font-family:"Space Grotesk",sans-serif;font-weight:600;font-size:.92cqw;text-transform:uppercase;letter-spacing:.01em}
.line-station.down .name{top:auto;bottom:-2.5cqw}
.line-station .callout{position:absolute;left:50%;top:3.4cqw;transform:translate(-50%,.5cqw);opacity:0;pointer-events:none;width:15cqw;background:#fff;border:1px solid #0f0f0f;padding:1cqw;transition:opacity .18s ease-out,transform .18s ease-out;text-align:left;white-space:normal}
.line-station.down .callout{top:auto;bottom:3.4cqw}
.line-station:hover .callout,.line-station:focus-visible .callout{opacity:1;transform:translate(-50%,0);pointer-events:auto}
.line-station .callout .mono{font-family:"Space Mono",monospace;font-size:.6cqw;letter-spacing:.12em;color:#e2231a;display:block}
.line-station .callout h3{font-family:"Space Grotesk",sans-serif;font-weight:700;font-size:1.05cqw;margin-top:.3cqw}
.line-station .callout p{font-size:.68cqw;color:#5a5a52;margin-top:.3cqw;line-height:1.4}
.line-train{position:absolute;top:50%;left:3%;transform:translate(-50%,-50%);width:3.4cqw;height:1.7cqw;border-radius:.5cqw;background:#0f0f0f;box-shadow:0 0 0 .22cqw #e2231a;z-index:4;animation:ride 16s ease-in-out infinite}
.line-train:before{content:"";position:absolute;inset:.34cqw .5cqw;background:repeating-linear-gradient(90deg,#f6f4ef 0 .34cqw,transparent .34cqw .8cqw);border-radius:.2cqw}
.line-legend{position:absolute;left:4cqw;bottom:6cqw;width:24cqw;z-index:5;border:1px solid #0f0f0f;background:#fff;padding:1.4cqw}
.line-legend .mono{font-family:"Space Mono",monospace;font-size:.62cqw;letter-spacing:.16em;color:#8a8a80}
.line-legend h4{font-family:"Space Grotesk",sans-serif;font-weight:700;font-size:1.6cqw;margin-top:.4cqw}
.line-legend p{font-size:.74cqw;color:#5a5a52;margin-top:.5cqw;line-height:1.45}
.line-legend .key{margin-top:1cqw;display:grid;gap:.5cqw;font-family:"Space Mono",monospace;font-size:.66cqw;color:#4a4a44}
.line-legend .key span{display:flex;align-items:center;gap:.7cqw}
.line-legend .key i{width:1cqw;height:1cqw;border-radius:50%;border:.3cqw solid #e2231a;background:#f6f4ef}
.line-legend .key i.ic{border-color:#0f0f0f;background:#0f0f0f}
.line-foot{position:absolute;right:4cqw;bottom:6cqw;text-align:right;z-index:5;font-family:"Space Mono",monospace;font-size:.68cqw;color:#6b6b60}
.line-foot a{display:block;color:#0f0f0f;margin-top:.4cqw}
@keyframes ride{0%{left:3%}7%{left:16%}9%{left:16%}20%{left:27%}23%{left:27%}34%{left:39%}37%{left:39%}49%{left:50%}52%{left:50%}64%{left:63%}67%{left:63%}79%{left:74%}82%{left:74%}93%{left:88%}97%{left:88%}100%{left:3%}}
.mobile .line{padding:6cqw}
.mobile .line-top{font-size:2cqw}
.mobile .line-title{position:static;font-size:11cqw;margin-top:8cqw}
.mobile .line-top .brand{font-size:4.6cqw}
.mobile .line-top .brand .roundel{width:6cqw;height:6cqw;font-size:2.4cqw}
.mobile .line-map{position:relative;left:auto;right:auto;top:auto;height:auto;margin:12cqw 0 0}
.mobile .line-track{position:absolute;left:1.4cqw;top:0;bottom:0;width:.7cqw;height:auto;border-radius:.4cqw}
.mobile .line-track:after{display:none}
.mobile .line-station{position:relative;left:auto;top:auto;transform:none;margin:0 0 14cqw 0;width:2.6cqw;height:2.6cqw;border-width:.5cqw}
.mobile .line-station.major{width:3.4cqw;height:3.4cqw}
.mobile .line-station .name{left:6cqw;top:50%;transform:translateY(-50%);bottom:auto;font-size:3.6cqw}
.mobile .line-station.down .name{top:50%}
.mobile .line-station .callout{left:6cqw;top:4.4cqw;bottom:auto;transform:translate(0,.4cqw);width:66cqw}
.mobile .line-station.down .callout{top:4.4cqw;bottom:auto}
.mobile .line-station .callout .mono{font-size:1.9cqw}
.mobile .line-station .callout h3{font-size:3.6cqw}
.mobile .line-station .callout p{font-size:2.4cqw}
.mobile .line-train{left:1.4cqw;top:0;transform:translate(-50%,0);width:5cqw;height:2.6cqw;animation-name:ridev}
.mobile .line-train:before{inset:.5cqw .7cqw}
.mobile .line-legend{position:static;width:auto;margin-top:4cqw;padding:4cqw}
.mobile .line-legend .mono{font-size:1.9cqw}
.mobile .line-legend h4{font-size:5.4cqw}
.mobile .line-legend p{font-size:2.8cqw}
.mobile .line-legend .key{font-size:2.1cqw}
.mobile .line-foot{position:static;text-align:left;margin-top:6cqw;font-size:2cqw}
@keyframes ridev{0%{top:0}7%{top:14%}9%{top:14%}20%{top:28%}23%{top:28%}34%{top:42%}37%{top:42%}49%{top:56%}52%{top:56%}64%{top:70%}67%{top:70%}79%{top:84%}82%{top:84%}93%{top:96%}97%{top:96%}100%{top:0}}
"""

PATCH_CSS = """
.patch{background:#1a1c1f;color:#e9e7e0;padding:3cqw 4cqw;overflow:hidden}
.patch .metal{position:absolute;inset:0;background:repeating-linear-gradient(90deg,rgba(255,255,255,.022) 0 2px,transparent 2px 4px);opacity:.7}
.patch-top{position:relative;z-index:6;display:flex;justify-content:space-between;font-family:"Space Mono",monospace;font-size:.72cqw;letter-spacing:.14em;color:#9a978f}
.patch-top nav{display:flex;gap:2.4cqw}
.patch-rack{position:absolute;left:3.4cqw;right:3.4cqw;top:8.6cqw;bottom:7.6cqw;display:grid;grid-template-columns:repeat(4,1fr);gap:1.4cqw;z-index:3}
.patch .module{position:relative;background:linear-gradient(180deg,#2c2f33,#1d2023);border:1px solid #0c0d0e;border-radius:.9cqw;padding:1.4cqw;display:flex;flex-direction:column;box-shadow:inset 0 1px 0 rgba(255,255,255,.06)}
.patch .module .strip{display:flex;justify-content:space-between;font-family:"Space Mono",monospace;font-size:.58cqw;letter-spacing:.14em;color:#b9b6ad;border-bottom:1px solid rgba(255,255,255,.12);padding-bottom:.8cqw;margin-bottom:1cqw}
.patch .screw{position:absolute;width:.7cqw;height:.7cqw;border-radius:50%;background:radial-gradient(#6a6f75,#33373b);box-shadow:inset 0 0 0 .12cqw #14161a}
.patch .screw.tl{top:.6cqw;left:.6cqw}.patch .screw.tr{top:.6cqw;right:.6cqw}.patch .screw.bl{bottom:.6cqw;left:.6cqw}.patch .screw.br{bottom:.6cqw;right:.6cqw}
.patch .knob{width:6cqw;height:6cqw;border-radius:50%;background:conic-gradient(from 0deg,#3a3f45,#22262a);box-shadow:0 0 0 .3cqw #101215,inset 0 0 1cqw rgba(0,0,0,.6);position:relative;margin:.8cqw auto;cursor:grab;touch-action:none}
.patch .knob:before{content:"";position:absolute;left:50%;top:10%;width:.42cqw;height:2.4cqw;transform:translateX(-50%) rotate(var(--k,0deg));transform-origin:50% 200%;background:#e9e7e0;border-radius:.2cqw}
.patch .knob:active{cursor:grabbing}
.patch .readout{font-family:"Space Mono",monospace;font-size:.62cqw;color:#7bff9e;text-align:center;letter-spacing:.1em}
.patch .jacks{display:flex;gap:1cqw;margin-top:auto;justify-content:center}
.patch .jack{width:2.2cqw;height:2.2cqw;border-radius:50%;background:radial-gradient(#4a4f55,#1a1d20);box-shadow:inset 0 0 0 .3cqw #0f1113,inset 0 0 .6cqw #000}
.patch .name{font-family:"Space Grotesk",sans-serif;font-weight:600;font-size:1.15cqw;margin-top:.6cqw;text-align:center}
.patch .name a{color:#e9e7e0}
.patch .desc{font-size:.66cqw;color:#8f8c84;text-align:center;margin-top:.4cqw;line-height:1.4}
.patch .ring{width:5cqw;height:5cqw;border-radius:50%;margin:1cqw auto;border:.5cqw solid #2b2f33;position:relative;box-shadow:0 0 1.6cqw rgba(123,255,158,.35)}
.patch .ring:before{content:"";position:absolute;inset:.7cqw;border-radius:50%;background:radial-gradient(circle,#7bff9e,#2f7d52);box-shadow:0 0 1.6cqw #4bd487;animation:pulse 2.6s ease-in-out infinite}
.patch .matrix{display:grid;grid-template-columns:repeat(4,1fr);gap:.5cqw;margin:1.4cqw auto 0;width:80%}
.patch .matrix i{aspect-ratio:1;border-radius:.15cqw;background:#333f47}
.patch .matrix i.on{background:#7bff9e;box-shadow:0 0 1cqw #4bd487}
.patch .scope{margin:.6cqw auto 0;width:90%;height:6cqw;border:1px solid rgba(123,255,158,.3);background:#0c1410;position:relative;overflow:hidden}
.patch .scope svg{position:absolute;left:0;top:0;height:100%;width:200%;animation:scope 3.4s linear infinite}
.patch .scope path{fill:none;stroke:#7bff9e;stroke-width:1.4}
.patch-cables{position:absolute;inset:0;z-index:5;pointer-events:none;overflow:hidden}
.patch-cables path{fill:none;stroke-linecap:round;stroke-width:1.6}
.patch-cables .c1{stroke:#ffd23f}.patch-cables .c2{stroke:#4aa3ff}.patch-cables .c3{stroke:#ff5c8a}
.patch-cables .flow{stroke-dasharray:5 16;animation:flow 1.6s linear infinite;stroke-width:2.4;opacity:.9}
.patch-foot{position:absolute;left:4cqw;right:4cqw;bottom:2.4cqw;display:flex;justify-content:space-between;font-family:"Space Mono",monospace;font-size:.68cqw;color:#7f7c74;z-index:6}
@keyframes pulse{0%,100%{opacity:.5;transform:scale(.9)}50%{opacity:1;transform:scale(1)}}
@keyframes blip{0%,100%{opacity:.22}50%{opacity:1}}
@keyframes flow{to{stroke-dashoffset:-21}}
@keyframes scope{to{transform:translateX(-50%)}}
.mobile .patch{padding:6cqw}
.mobile .patch-top{font-size:2cqw}
.mobile .patch-rack{position:static;margin-top:8cqw;grid-template-columns:1fr 1fr;gap:3cqw}
.mobile .patch .module{padding:3cqw;border-radius:2cqw}
.mobile .patch .module .strip{font-size:1.7cqw;padding-bottom:2cqw;margin-bottom:2.4cqw}
.mobile .patch .screw{width:1.8cqw;height:1.8cqw}
.mobile .patch .knob{width:15cqw;height:15cqw}
.mobile .patch .knob:before{height:6cqw;width:1cqw}
.mobile .patch .readout{font-size:1.9cqw}
.mobile .patch .jacks{gap:2.4cqw}
.mobile .patch .jack{width:5cqw;height:5cqw}
.mobile .patch .name{font-size:3.1cqw}
.mobile .patch .desc{font-size:1.9cqw}
.mobile .patch .ring{width:13cqw;height:13cqw}
.mobile .patch .matrix{gap:1.2cqw}
.mobile .patch .scope{height:14cqw;width:100%}
.mobile .patch-cables{display:none}
.mobile .patch-foot{position:static;margin-top:8cqw;font-size:1.9cqw}
"""

FLASH_CSS = """
.flash{background:#efe6d2;color:#111;padding:3cqw 4cqw;overflow:hidden}
.flash .paper{position:absolute;inset:0;background:radial-gradient(120% 90% at 18% 0%,rgba(160,120,60,.14),transparent 52%),radial-gradient(90% 80% at 100% 100%,rgba(140,100,50,.18),transparent 56%)}
.flash-top{position:relative;z-index:3;display:flex;justify-content:space-between;align-items:flex-end;border-bottom:.34cqw solid #111;padding-bottom:1cqw}
.flash-top .title{font-family:"Anton",sans-serif;font-size:4.6cqw;line-height:.88;letter-spacing:.02em;text-transform:uppercase}
.flash-top .sub{font-family:"Space Mono",monospace;font-size:.72cqw;letter-spacing:.2em;color:#a11f1f;text-align:right}
.flash-top nav{display:flex;gap:2.4cqw;font-family:"Space Mono",monospace;font-size:.72cqw}
.flash-grid{position:absolute;left:4cqw;right:4cqw;top:17cqw;bottom:5.4cqw;display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:1fr 1fr;gap:2.2cqw;z-index:3}
.flash .sheet{position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;border:.14cqw solid rgba(17,17,17,.26);background:rgba(255,255,255,.22);transition:background .18s ease-out}
.flash .sheet:hover{background:rgba(255,255,255,.5)}
.flash .sheet svg{width:56%;height:auto;overflow:visible;transition:transform .18s cubic-bezier(.23,1,.32,1)}
.flash .sheet:hover svg{transform:scale(1.07) rotate(-1.5deg)}
.flash .sheet svg .boil{animation:boil .6s steps(2) infinite}
.flash .sheet svg path,.flash .sheet svg circle,.flash .sheet svg line,.flash .sheet svg rect,.flash .sheet svg polygon{fill:none;stroke:#111;stroke-width:7;stroke-linecap:round;stroke-linejoin:round}
.flash .sheet .label{position:absolute;left:.9cqw;bottom:.9cqw;font-family:"Space Mono",monospace;font-size:.6cqw;letter-spacing:.08em;color:#5a4a2a;line-height:1.5}
.flash .sheet .stamp{position:absolute;right:.9cqw;top:.9cqw;font-family:"Anton",sans-serif;font-size:1.15cqw;letter-spacing:.05em;color:#c1272d;border:.18cqw solid #c1272d;padding:.2cqw .6cqw;border-radius:.2cqw;transform:rotate(9deg) scale(.8);opacity:0;transition:opacity .16s ease-out,transform .16s cubic-bezier(.23,1,.32,1)}
.flash .sheet:hover .stamp,.flash .sheet:focus-within .stamp{opacity:1;transform:rotate(-6deg) scale(1)}
.flash-foot{position:absolute;left:4cqw;right:4cqw;bottom:1.5cqw;display:flex;justify-content:space-between;font-family:"Space Mono",monospace;font-size:.68cqw;color:#7a6a48;z-index:3}
@keyframes boil{0%{transform:translate(0,0)}50%{transform:translate(.18cqw,-.12cqw)}100%{transform:translate(0,0)}}
.mobile .flash{padding:6cqw}
.mobile .flash-top .title{font-size:11cqw}
.mobile .flash-top .sub{font-size:2cqw}
.mobile .flash-top nav{font-size:2cqw}
.mobile .flash-grid{position:static;margin-top:9cqw;grid-template-columns:1fr;grid-template-rows:none;gap:5cqw}
.mobile .flash .sheet{aspect-ratio:1.4;padding:4cqw}
.mobile .flash .sheet svg{width:44%}
.mobile .flash .sheet .label{font-size:1.9cqw;left:3cqw;bottom:3cqw}
.mobile .flash .sheet .stamp{font-size:3.4cqw;right:3cqw;top:3cqw;border-width:.4cqw}
.mobile .flash-foot{position:static;margin-top:8cqw;font-size:1.9cqw}
"""

COMMIT_CSS = """
.commit{background:#fbfaf7;color:#2b2b2b;padding:3cqw 4cqw;overflow:hidden;font-family:"Space Mono",monospace}
.commit-top{position:relative;z-index:3;display:flex;justify-content:space-between;font-size:.72cqw;letter-spacing:.12em;color:#8a8a80}
.commit-top nav{display:flex;gap:2.4cqw}
.commit-head{position:relative;z-index:3;margin-top:3cqw;border:1px solid #e2ded3;background:#fff;padding:1.6cqw 2cqw}
.commit-head .row{display:grid;grid-template-columns:7cqw 1fr;gap:1.4cqw;font-size:.76cqw;line-height:1.75}
.commit-head .row span:first-child{color:#9a9a90}
.commit-head .msg{font-family:"Space Grotesk",sans-serif;font-size:1.5cqw;color:#141414;margin-top:1cqw}
.commit-body{position:absolute;left:4cqw;right:4cqw;top:25.5cqw;bottom:6.4cqw;z-index:3;display:grid;grid-template-columns:1fr 24cqw;gap:2.4cqw}
.commit-diff{border:1px solid #e2ded3;background:#fff;overflow:hidden;font-size:.92cqw;line-height:1.95}
.commit-diff .file{display:flex;justify-content:space-between;border-bottom:1px solid #e2ded3;padding:.8cqw 1cqw;font-size:.74cqw;color:#5a5a52}
.commit-diff .hunk{background:#f4f2ec;color:#6b6b60;padding:.3cqw 1cqw;font-size:.74cqw}
.commit-diff .ln{display:grid;grid-template-columns:3.2cqw 1.8cqw 1fr;align-items:baseline;padding:0 .8cqw}
.commit-diff .ln .no{color:#c2bfb4;text-align:right;padding-right:1cqw;font-size:.7cqw}
.commit-diff .ln .sign{color:#8a8a80}
.commit-diff .ln.add{background:#eaf7ed}
.commit-diff .ln.add .code{color:#14632b}
.commit-diff .ln.del{background:#fdecec}
.commit-diff .ln.del .code{color:#9b2222}
.commit-diff .code{white-space:pre;overflow:hidden;text-overflow:ellipsis}
.commit-diff .ln:hover{outline:1px solid #b9d4f5;background:#f0f6ff}
.commit-side .panel{border:1px solid #e2ded3;background:#fff;padding:1.2cqw;margin-bottom:1.4cqw}
.commit-side h4{font-size:.68cqw;letter-spacing:.16em;color:#8a8a80;font-weight:400}
.commit-side .big{font-family:"Space Grotesk",sans-serif;font-size:2.2cqw;font-weight:700;margin-top:.4cqw}
.commit-side .big em{font-style:normal;color:#4bd487}
.commit-side .bar{height:.9cqw;background:#f0eee6;margin-top:.9cqw;display:flex;overflow:hidden}
.commit-side .bar i{background:#4bd487;width:100%}
.commit-side a.link{display:flex;justify-content:space-between;font-size:.76cqw;padding:.75cqw 0;border-top:1px solid #eeece4;color:#141414}
.commit-side a.link:first-of-type{border-top:0}
.commit-comment{position:absolute;z-index:4;left:49cqw;top:31cqw;width:17cqw;background:#fff;border:1px solid #dcd8cc;border-radius:.8cqw;padding:1cqw;font-family:"Space Grotesk",sans-serif;font-size:.8cqw;box-shadow:0 1cqw 2cqw rgba(0,0,0,.08)}
.commit-comment .who{font-family:"Space Mono",monospace;font-size:.64cqw;color:#8a8a80;margin-bottom:.4cqw}
.commit-foot{position:absolute;left:4cqw;right:4cqw;bottom:2.2cqw;display:flex;justify-content:space-between;font-size:.68cqw;color:#9a9a90;z-index:3}
.mobile .commit{padding:6cqw}
.mobile .commit-top{font-size:2cqw}
.mobile .commit-head{margin-top:6cqw;padding:4cqw}
.mobile .commit-head .row{grid-template-columns:18cqw 1fr;font-size:2cqw;line-height:2}
.mobile .commit-head .msg{font-size:4.6cqw;margin-top:2.4cqw}
.mobile .commit-body{position:static;grid-template-columns:1fr;gap:6cqw;margin-top:7cqw}
.mobile .commit-diff{font-size:2.35cqw;line-height:2.1}
.mobile .commit-diff .file{font-size:1.9cqw;padding:2cqw 2.4cqw}
.mobile .commit-diff .hunk{font-size:1.9cqw}
.mobile .commit-diff .ln{grid-template-columns:7cqw 4cqw 1fr;padding:0 2.4cqw}
.mobile .commit-diff .ln .no{font-size:1.8cqw}
.mobile .commit-side .panel{padding:4cqw;margin-bottom:4cqw}
.mobile .commit-side h4{font-size:1.8cqw}
.mobile .commit-side .big{font-size:6cqw}
.mobile .commit-side a.link{font-size:2.4cqw;padding:2.4cqw 0}
.mobile .commit-comment{position:static;width:auto;margin-top:4cqw;font-size:2.6cqw;padding:3cqw}
.mobile .commit-comment .who{font-size:1.9cqw}
.mobile .commit-foot{position:static;margin-top:7cqw;font-size:1.9cqw}
"""

NEW_CSS = "".join([SPEC_CSS, VIT_CSS, FOIL_CSS, LINE_CSS, PATCH_CSS, FLASH_CSS, COMMIT_CSS])

INTERACT = """
<script>
(function(){
  try{
    var m=/[?&]dir=([A-H])/.exec(location.search);
    if(m){
      Array.prototype.forEach.call(document.querySelectorAll('.direction'),function(s){ if(s.id!==m[1]){ s.parentNode.removeChild(s); } });
      Array.prototype.forEach.call(document.querySelectorAll('.intro,.rtop,.rfoot,.revdivider'),function(s){ s.parentNode.removeChild(s); });
    }
  }catch(e){}
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function lerp(a,b,t){return a+(b-a)*t;}
  function clamp(v,a,b){return Math.max(a,Math.min(b,v));}
  function loop(fn){ (function step(){ fn(); requestAnimationFrame(step); })(); }

  document.querySelectorAll('[data-specimen]').forEach(function(el){
    var o1=el.querySelector('[data-wght]'), o2=el.querySelector('[data-track]');
    if(reduce){ return; }
    var tx=.42, ty=.18, x=tx, y=ty;
    el.addEventListener('pointermove',function(e){var r=el.getBoundingClientRect(); tx=(e.clientX-r.left)/r.width; ty=(e.clientY-r.top)/r.height;});
    el.addEventListener('pointerleave',function(){tx=.42;ty=.18;});
    loop(function(){
      x=lerp(x,clamp(tx,0,1),.12); y=lerp(y,clamp(ty,0,1),.12);
      var wght=Math.round(150+x*630);
      var ls=(0.02-y*0.085);
      el.style.setProperty('--wght',wght);
      el.style.setProperty('--ls',ls.toFixed(3)+'em');
      if(o1){o1.textContent=wght;}
      if(o2){o2.textContent=ls.toFixed(3)+'em';}
    });
  });

  document.querySelectorAll('[data-tilt]').forEach(function(el){
    if(reduce){ return; }
    var max=parseFloat(el.getAttribute('data-tilt'))||8;
    var trx=0,trY=0,rx=0,ry=0;
    el.addEventListener('pointermove',function(e){var r=el.getBoundingClientRect(); trY=((e.clientX-r.left)/r.width-.5)*2*max; trx=-((e.clientY-r.top)/r.height-.5)*2*max;});
    el.addEventListener('pointerleave',function(){trx=0;trY=0;});
    loop(function(){
      rx=lerp(rx,trx,.1); ry=lerp(ry,trY,.1);
      el.style.setProperty('--rx',rx.toFixed(2)+'deg');
      el.style.setProperty('--ry',ry.toFixed(2)+'deg');
    });
  });

  document.querySelectorAll('[data-pointer]').forEach(function(el){
    if(reduce){ return; }
    var tx=.5,ty=.3,x=.5,y=.3;
    el.addEventListener('pointermove',function(e){var r=el.getBoundingClientRect(); tx=(e.clientX-r.left)/r.width; ty=(e.clientY-r.top)/r.height;});
    el.addEventListener('pointerleave',function(){tx=.5;ty=.3;});
    loop(function(){
      x=lerp(x,clamp(tx,0,1),.12); y=lerp(y,clamp(ty,0,1),.12);
      el.style.setProperty('--mx',(x*100).toFixed(1)+'%');
      el.style.setProperty('--my',(y*100).toFixed(1)+'%');
    });
  });

  document.querySelectorAll('[data-knob]').forEach(function(el){
    var val=parseFloat(el.getAttribute('data-knob'))||0, sy=0, sv=0, drag=false;
    var out=el.parentNode.querySelector('[data-val]');
    function apply(){ el.style.setProperty('--k',val+'deg'); if(out){ out.textContent=Math.round((val+135)/270*100); } }
    el.addEventListener('pointerdown',function(e){ drag=true; sy=e.clientY; sv=val; if(el.setPointerCapture){el.setPointerCapture(e.pointerId);} e.preventDefault(); });
    el.addEventListener('pointermove',function(e){ if(!drag){return;} val=clamp(sv+(sy-e.clientY)*1.4,-135,135); apply(); });
    el.addEventListener('pointerup',function(){ drag=false; });
    el.addEventListener('pointercancel',function(){ drag=false; });
    el.addEventListener('keydown',function(e){ if(e.key==='ArrowUp'||e.key==='ArrowRight'){val=clamp(val+8,-135,135);apply();e.preventDefault();} if(e.key==='ArrowDown'||e.key==='ArrowLeft'){val=clamp(val-8,-135,135);apply();e.preventDefault();} });
  });
})();
</script>
"""

GHM = a(GH, "GitHub", "mono")
BSM = a(BS, "Bluesky", "mono")

SPC = (
    '<div class="site spc" data-specimen><span class="base" aria-hidden="true"></span>'
    '<header class="spc-top"><span>MUSSE FOUNDRY</span><span>SPECIMEN 01 / VARIABLE GROTESK</span><nav>'
    + GHM + " " + BSM + "</nav></header>"
    '<span class="lead">INTERACTIVE. MOVE YOUR CURSOR OVER THE TYPE.</span>'
    '<div class="spc-word" aria-label="MusseJusse"><span>Musse</span><span>Jusse</span></div>'
    '<div class="spc-read">WEIGHT <b data-wght>430</b><br>TRACKING <b data-track>-0.020em</b><br>AXES 300-700</div>'
    '<div class="spc-glyphs">ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789 &amp;@#%</div>'
    '<section class="spc-work">'
    '<a href="' + R + '"><span class="g">Aa</span><div><h3>Roundest Pok&eacute;mon</h3>'
    '<p class="mono">SET IN 5.6 / NEXT.JS / COMPARISON &#8599;</p></div></a>'
    '<a href="' + M + '"><span class="g">Aa</span><div><h3>Models</h3>'
    '<p class="mono">SET IN 5.6 / ASTRO / REFERENCE &#8599;</p></div></a>'
    "</section>"
    '<footer class="spc-foot"><span>MUSSE FOUNDRY / 2026</span><span>LICENSED FOR THE WEB</span></footer>'
    "</div>"
)

VIT = (
    '<div class="site vit" data-pointer>'
    '<header class="vit-top"><span>MUSSEJUSSE / GALLERY</span><nav>' + GHM + " " + BSM + "</nav></header>"
    '<div class="vit-scene" data-tilt="5"><span class="vit-wall" aria-hidden="true"></span>'
    '<span class="vit-floor" aria-hidden="true"></span><span class="vit-pool" aria-hidden="true"></span>'
    '<span class="vit-pool two" aria-hidden="true"></span>'
    '<article class="vit-work one"><div class="vit-frame"><div class="vit-canvas blue"></div></div>'
    '<div class="vit-plaque"><h3>Roundest Pok&eacute;mon</h3>'
    '<p>Interactive comparison, 2026. Next.js.<br><a href="' + R + '">roundest.mussejusse.com &#8599;</a></p></div></article>'
    '<article class="vit-work two"><div class="vit-frame"><div class="vit-canvas ochre"></div></div>'
    '<div class="vit-plaque"><h3>Models</h3>'
    '<p>Reference catalogue, 2026. Astro.<br><a href="' + M + '">models.mussejusse.com &#8599;</a></p></div></article>'
    "</div>"
    '<span class="vit-light" aria-hidden="true"></span>'
    '<aside class="vit-guide"><span class="mono">EXHIBITION / OPEN INDEFINITELY</span>'
    "<h1>Two works,<br>one builder.</h1>"
    "<p>A small room for things I make and never quite finish. Look around; the light follows you.</p>"
    '<div class="list"><span><em>01</em><em>Roundest Pok&eacute;mon</em></span><span><em>02</em><em>Models</em></span></div></aside>'
    "</div>"
)


def foil_card(kind, name, hp, typeline, moves, url, cta):
    art = "orb" if kind == "pink" else "grid"
    mv = "".join('<div class="move"><b>%s</b><span>%s</span></div>' % m for m in moves)
    return (
        '<article class="card ' + kind + '" data-tilt="11" data-pointer><div class="inner">'
        '<div class="hbar"><h3>' + name + '</h3><span class="hp">' + hp + "</span></div>"
        '<div class="art ' + art + '"></div>'
        '<div class="type">' + typeline + "</div>"
        '<div class="moves">' + mv + "</div>"
        '<div class="foot"><span>ILLUS. M. JUSSE</span><a href="' + url + '">' + cta + " &#8599;</a></div>"
        "</div><span class=\"holo\" aria-hidden=\"true\"></span><span class=\"glare\" aria-hidden=\"true\"></span></article>"
    )


FOIL = (
    '<div class="site foil">'
    '<header class="foil-top"><span>SERIES MJ / FIRST EDITION</span><nav>' + GHM + " " + BSM + "</nav></header>"
    '<div class="foil-deck">'
    + foil_card("pink", "Roundest Pok&eacute;mon", "HP 90", "DEVELOPER / COMPARISON",
                [("01", "Server Actions. Renders the roundness question instantly."),
                 ("02", "KV Cache. Never answers the same way twice.")], R, "PLAY")
    + foil_card("blue", "Models", "HP 110", "DEVELOPER / REFERENCE",
                [("01", "Astro Islands. Ships almost no JavaScript."),
                 ("02", "Content Collections. Every model, typed.")], M, "PLAY")
    + "</div>"
    '<div class="foil-title">Gotta build &rsquo;em all.</div>'
    "</div>"
)


callout_url = {}
LINE_CALLOUTS = {
    "s1": ("HELLO", False, "major interchange", None),
    "s2": ("FIRST COMMIT", True, "", '<span class="mono">STATION</span><h3>Curiosity</h3><p>Where every build starts.</p>'),
    "s3": ("ROUNDEST POK&Eacute;MON", False, "major", None),
    "s4": ("SERVER ACTIONS", True, "", '<span class="mono">STATION</span><h3>Fetch</h3><p>Ask the server, keep it instant.</p>'),
    "s5": ("MODELS", False, "major", None),
    "s6": ("ASTRO", True, "", '<span class="mono">STATION</span><h3>Islands</h3><p>Ship less JavaScript.</p>'),
    "s7": ("CACHE COMPONENTS", False, "", '<span class="mono">STATION</span><h3>Cache</h3><p>Never ask twice.</p>'),
    "s8": ("ALWAYS BUILDING", True, "major", None),
}

LINE = (
    '<div class="site line">'
    '<header class="line-top"><span class="brand"><span class="roundel">MJ</span>MUSSEJUSSE TRANSIT</span>'
    "<nav>" + GHM + " " + BSM + "</nav></header>"
    '<h1 class="line-title">Two experiments,<br>one long line.</h1>'
    '<div class="line-map"><span class="line-track" aria-hidden="true"></span>'
    '<span class="line-station s1 major interchange"><span class="name">HELLO</span>'
    '<span class="callout"><span class="mono">TERMINUS / START</span><h3>You are here</h3>'
    "<p>Twelve years of making things on the web, in one line.</p></span></span>"
    '<span class="line-station s2 down"><span class="name">FIRST COMMIT</span>'
    '<span class="callout"><span class="mono">STATION</span><h3>Curiosity</h3><p>Where every build starts.</p></span></span>'
    '<a class="line-station s3 major" href="' + R + '"><span class="name">ROUNDEST POK&Eacute;MON</span>'
    '<span class="callout"><span class="mono">INTERCHANGE / NEXT.JS</span><h3>Roundest Pok&eacute;mon</h3>'
    "<p>Two Pokémon, one very round question. Ride the line to find out.</p></span></a>"
    '<span class="line-station s4 down"><span class="name">SERVER ACTIONS</span>'
    '<span class="callout"><span class="mono">STATION</span><h3>Fetch</h3><p>Ask the server, keep it instant.</p></span></span>'
    '<a class="line-station s5 major" href="' + M + '"><span class="name">MODELS</span>'
    '<span class="callout"><span class="mono">INTERCHANGE / ASTRO</span><h3>Models</h3>'
    "<p>A catalogue of every model, provider and capability.</p></span></a>"
    '<span class="line-station s6 down"><span class="name">ASTRO</span>'
    '<span class="callout"><span class="mono">STATION</span><h3>Islands</h3><p>Ship less JavaScript.</p></span></span>'
    '<span class="line-station s7"><span class="name">CACHE COMPONENTS</span>'
    '<span class="callout"><span class="mono">STATION</span><h3>Cache</h3><p>Never ask twice.</p></span></span>'
    '<span class="line-station s8 down major"><span class="name">ALWAYS BUILDING</span>'
    '<span class="callout"><span class="mono">TERMINUS</span><h3>Never finished</h3>'
    "<p>No final stop. The line keeps running.</p></span></span>"
    '<span class="line-train" aria-hidden="true"></span></div>'
    '<aside class="line-legend"><span class="mono">LINE 2 / SERVICE</span><h4>The Build Line</h4>'
    "<p>One train, two experiments, no timetable. It runs through everything I make.</p>"
    '<div class="key"><span><i></i>Major station / project</span><span><i class="ic"></i>Interchange / where it starts</span></div></aside>'
    '<div class="line-foot">ALL STATIONS ACCESSIBLE<br>SOURCE ON GITHUB</div>'
    "</div>"
)

PATCH = (
    '<div class="site patch"><span class="metal" aria-hidden="true"></span>'
    '<header class="patch-top"><span>MUSSEJUSSE / MODULAR SYSTEM</span><nav>' + GHM + " " + BSM + "</nav></header>"
    '<div class="patch-rack">'
    '<section class="module"><span class="screw tl"></span><span class="screw tr"></span><span class="screw bl"></span><span class="screw br"></span>'
    '<div class="strip"><span>01</span><span>SOURCE</span></div>'
    '<div class="knob" data-knob="20" tabindex="0" role="slider" aria-label="Curiosity amount"></div>'
    '<div class="readout">CURIOSITY <b data-val>57</b></div>'
    '<div class="jacks"><span class="jack"></span><span class="jack"></span></div></section>'
    '<section class="module"><span class="screw tl"></span><span class="screw tr"></span><span class="screw bl"></span><span class="screw br"></span>'
    '<div class="strip"><span>02</span><span>OSC</span></div>'
    '<div class="ring" aria-hidden="true"></div>'
    '<div class="name"><a href="' + R + '">Roundest Pok&eacute;mon &#8599;</a></div>'
    '<div class="desc">One round output. Absolutely no square edges.</div>'
    '<div class="jacks"><span class="jack"></span></div></section>'
    '<section class="module"><span class="screw tl"></span><span class="screw tr"></span><span class="screw bl"></span><span class="screw br"></span>'
    '<div class="strip"><span>03</span><span>SEQ</span></div>'
    '<div class="matrix" aria-hidden="true">'
    + "".join('<i class="on" style="animation:blip %ss steps(1) infinite"></i>' % (1.2 + (i % 5) * 0.28) if i % 3 == 0 else "<i></i>" for i in range(16))
    + "</div>"
    '<div class="name"><a href="' + M + '">Models &#8599;</a></div>'
    '<div class="desc">A 16-step register of everything.</div>'
    '<div class="jacks"><span class="jack"></span></div></section>'
    '<section class="module"><span class="screw tl"></span><span class="screw tr"></span><span class="screw bl"></span><span class="screw br"></span>'
    '<div class="strip"><span>04</span><span>OUT</span></div>'
    '<div class="scope" aria-hidden="true"><svg viewBox="0 0 400 60" preserveAspectRatio="none">'
    '<path d="M0 30 L10 30 L14 12 L20 48 L26 24 L32 36 L38 30 L60 30 L64 10 L70 50 L76 22 L82 38 L88 30 L110 30 L114 12 L120 48 L126 24 L132 36 L138 30 L160 30 L164 10 L170 50 L176 22 L182 38 L188 30 L200 30"/>'
    '<path transform="translate(200,0)" d="M0 30 L10 30 L14 12 L20 48 L26 24 L32 36 L38 30 L60 30 L64 10 L70 50 L76 22 L82 38 L88 30 L110 30 L114 12 L120 48 L126 24 L132 36 L138 30 L160 30 L164 10 L170 50 L176 22 L182 38 L188 30 L200 30"/></svg></div>'
    '<div class="name">Signal out</div><div class="desc">Everything routes to the web.</div>'
    '<div class="jacks"><span class="jack"></span><span class="jack"></span></div></section>'
    "</div>"
    '<svg class="patch-cables" viewBox="0 0 400 300" preserveAspectRatio="none" aria-hidden="true">'
    '<path class="c1" d="M58 250 C82 300,116 300,140 250"/>'
    '<path class="c2" d="M160 250 C184 304,216 304,240 250"/>'
    '<path class="c3" d="M38 250 C120 314,270 314,342 250"/>'
    '<path class="flow c1" d="M58 250 C82 300,116 300,140 250"/>'
    '<path class="flow c2" d="M160 250 C184 304,216 304,240 250"/>'
    "</svg>"
    '<footer class="patch-foot"><span>CV / GATE / TRIG / SIGNAL</span><span>PATCHED BY MUSSE</span></footer>'
    "</div>"
)


def flash_sheet(label, stamp, art, url=None):
    body = '<svg viewBox="0 0 120 120" aria-hidden="true">' + art + "</svg>"
    tag = "a" if url else "div"
    href = ' href="' + url + '"' if url else ""
    return (
        "<" + tag + href + ' class="sheet"><span class="label">' + label + "</span>"
        '<span class="stamp">' + stamp + "</span>" + body + "</" + tag + ">"
    )


FLASH_ART = {
    "roundest": '<g class="boil"><circle cx="60" cy="60" r="34"/><circle cx="60" cy="60" r="5"/><line x1="60" y1="8" x2="60" y2="20"/><line x1="60" y1="100" x2="60" y2="112"/><line x1="8" y1="60" x2="20" y2="60"/><line x1="100" y1="60" x2="112" y2="60"/></g>',
    "models": '<g class="boil"><rect x="24" y="28" width="72" height="14" rx="4"/><rect x="24" y="52" width="72" height="14" rx="4"/><rect x="24" y="76" width="72" height="14" rx="4"/></g>',
    "dagger": '<g class="boil"><path d="M60 10 L68 52 L60 60 L52 52 Z"/><line x1="60" y1="60" x2="60" y2="104"/><line x1="46" y1="56" x2="74" y2="56"/></g>',
    "snake": '<g class="boil"><path d="M66 12 L38 62 L58 62 L46 108 L82 50 L60 50 Z"/></g>',
    "eye": '<g class="boil"><path d="M12 60 C32 34,68 34,88 60 C68 86,32 86,12 60 Z"/><circle cx="50" cy="60" r="10"/><line x1="50" y1="20" x2="50" y2="32"/><line x1="18" y1="30" x2="26" y2="40"/><line x1="82" y1="30" x2="74" y2="40"/></g>',
    "banner": '<g class="boil"><path d="M18 40 L102 40 L94 60 L102 80 L18 80 L26 60 Z"/><text x="60" y="66" text-anchor="middle" font-family="Anton, sans-serif" font-size="20" fill="#111" stroke="none">BUILD</text></g>',
}

FLASH = (
    '<div class="site flash"><span class="paper" aria-hidden="true"></span>'
    '<header class="flash-top"><span class="title">Flash</span>'
    '<span class="sub">MUSSEJUSSE ORIGINALS /<br>WALK-INS WELCOME</span>'
    "<nav>" + GHM + " " + BSM + "</nav></header>"
    '<div class="flash-grid">'
    + flash_sheet("FLASH 01 / APPROX 4 IN<br>NEXT.JS / COMPARISON", "OPEN", FLASH_ART["roundest"], R)
    + flash_sheet("FLASH 02 / APPROX 5 IN<br>ASTRO / REFERENCE", "OPEN", FLASH_ART["models"], M)
    + flash_sheet("FLASH 03 / DAGGER", "BOOKED", FLASH_ART["dagger"])
    + flash_sheet("FLASH 04 / LIGHTNING BOLT", "BOOKED", FLASH_ART["snake"])
    + flash_sheet("FLASH 05 / EYE", "FLASH ONLY", FLASH_ART["eye"])
    + flash_sheet("FLASH 06 / BANNER", "BOOKED", FLASH_ART["banner"])
    + "</div>"
    '<footer class="flash-foot"><span>ALL FLASH DRAWN ONCE, NEVER REPEATED</span><span>DEPOSIT SECURES YOUR DATE</span></footer>'
    "</div>"
)

COMMIT_LINES = [
    ("add", "+", 'name: "MusseJusse"'),
    ("add", "+", 'role: "builds for the web"'),
    ("add", "+", 'status: "always building, never finished"'),
    ("add", "+", "experiments:"),
    ("add", "+", '  - name: "Roundest Pok&eacute;mon"'),
    ("add", "+", '    stack: "Next.js"'),
    ("add", "+", '    url:  "https://roundest.mussejusse.com"'),
    ("add", "+", '  - name: "Models"'),
    ("add", "+", '    stack: "Astro"'),
    ("add", "+", '    url:  "https://models.mussejusse.com"'),
    ("add", "+", "links: [github, bluesky]"),
]
_commit_rows = "".join(
    '<div class="ln %s"><span class="no">%d</span><span class="sign">%s</span><span class="code">%s</span></div>'
    % (kind, i + 1, sign, code)
    for i, (kind, sign, code) in enumerate(COMMIT_LINES)
)

COMMIT = (
    '<div class="site commit">'
    '<header class="commit-top"><span>mussejusse / git</span><nav>' + GHM + " " + BSM + "</nav></header>"
    '<div class="commit-head"><div class="row">'
    "<span>commit</span><span>9f3a1c2 (main)</span>"
    "<span>author</span><span>Musse Jusse &lt;musse@mussejusse.com&gt;</span>"
    "<span>date</span><span>Fri Sep 11 2026</span></div>"
    '<div class="msg">feat: launch a personal site about building</div></div>'
    '<div class="commit-body"><div class="commit-diff">'
    '<div class="file"><span>b/mussejusse</span><span>+11 -0</span></div>'
    '<div class="hunk">@@ -0,0 +1,11 @@</div>'
    + _commit_rows
    + "</div>"
    '<aside class="commit-side">'
    '<div class="panel"><h4>FILES CHANGED</h4><div class="big">1 <em>+11</em></div><div class="bar"><i></i></div></div>'
    '<div class="panel"><h4>DEPLOY PREVIEWS</h4>'
    '<a class="link" href="' + R + '">roundest.mussejusse.com<span>&#8599;</span></a>'
    '<a class="link" href="' + M + '">models.mussejusse.com<span>&#8599;</span></a></div>'
    '<div class="panel"><h4>STATUS</h4><div class="big">Building</div></div>'
    "</aside></div>"
    '<div class="commit-comment"><div class="who">reviewer / bsky</div>Nice. Ship it, but the status line should never change.</div>'
    '<footer class="commit-foot"><span>1 file changed / review requested</span><span>Approved by 1 reviewer</span></footer>'
    "</div>"
)

DIRECTIONS = [
    ("A", "Specimen", "A living type specimen. The wordmark is a variable font you morph with the cursor: weight and tracking follow your hand.", SPC),
    ("B", "Riso", "Kept from round one. A two-ink screenprint: halftone wordmark, misregistration, and two hand-printed project lots.", RISO),
    ("C", "Vitrine", "A small 3D gallery. Two hung works with wall labels, and a spotlight that follows the pointer as the room tilts.", VIT),
    ("D", "Foil", "The two experiments as holographic trading cards, with HP, moves, and a foil sheen that shifts when you tilt them.", FOIL),
    ("E", "Line 2", "The site as a transit diagram. A train runs the line, and the two projects are interchange stations you can open.", LINE),
    ("F", "Patch", "A modular synthesizer. Draggable knobs, patched cables, a pulsing oscillator and a live scope. Projects as modules.", PATCH),
    ("G", "Flash", "A tattoo flash sheet. Bold hand-drawn designs, two of them bookable, with a red stamp on hover.", FLASH),
    ("H", "Commit", "The site as a code review. A real diff that adds MusseJusse, with deploy previews and a review comment.", COMMIT),
]


def section(letter, title, desc, markup):
    views = "".join(
        '<div class="view %s"><div class="vlabel"><b>%s</b><span>%s</span></div>'
        '<div class="canvas">%s</div></div>' % (kind, kind.capitalize(), size, markup)
        for kind, size in [("desktop", "1440 &times; 1000"), ("mobile", "390 &times; 844")]
    )
    prefix = ""
    if letter == "A":
        prefix = '<div class="revdivider"><span>ROUND TWO / SEVEN NEW DIRECTIONS. B (RISO) IS KEPT FROM ROUND ONE.</span></div>'
    return (
        prefix
        + '<section class="direction" id="%s">'
        '<header class="dhead"><span class="letter">%s</span><h2>%s / %s</h2><p>%s</p></header>'
        '<div class="views">%s</div></section>'
    ) % (letter, letter, letter, title, desc, views)


def build():
    sections = "".join(section(*d) for d in DIRECTIONS)
    nav = "".join('<a href="#%s">%s</a>' % (d[0], d[0]) for d in DIRECTIONS)
    html = (
        '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        "<title>MusseJusse / Redesign directions</title>"
        "<style>" + FONT_CSS + STAGE_CSS + CHROME_CSS + RISO_CSS + NEW_CSS + "</style>"
        "</head><body>"
        '<div class="rtop"><div class="row"><h1>MusseJusse / redesign directions</h1>'
        "<span>eight directions &middot; desktop + mobile</span>"
        '<nav class="rnav" aria-label="Directions">' + nav + "</nav></div></div>"
        '<div class="wrap">'
        '<header class="intro"><span class="k">FULL UI REDESIGN / ROUND TWO</span>'
        "<h2>Eight directions. I kept the one you liked (B, Riso) and rebuilt the rest from scratch, bigger swing this time: a living type specimen, a 3D gallery, holographic cards, a transit map, a modular synth, a tattoo flash sheet, and the site as a code diff.</h2>"
        "<p>Every direction is a working page with desktop and mobile views, not a picture. The interactive ones (A, C, D, F) respond to your cursor; move over them. Pick one, or mix the parts you like, and I will build it for real.</p></header>"
        + sections
        + '<footer class="rfoot"><span>Eight directions, rendered live. A, C, D and F respond to the pointer.</span>'
        "<span>" + a(GH, "GitHub", "") + " &middot; " + a(BS, "Bluesky", "") + "</span></footer>"
        "</div>" + INTERACT + "</body></html>"
    )
    return html


if __name__ == "__main__":
    html = build()
    out = ROOT / "redesign-directions.html"
    out.write_text(html)
    assert "\u2014" not in html, "em dash found"
    assert "http://" not in html.replace("http://www.w3.org", ""), "insecure url"
    size = len(html.encode())
    assert size < 512 * 1024, "over 512KB: %d" % size
    print("%s: %s bytes" % (out, format(size, ",")))
