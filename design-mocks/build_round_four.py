"""Build one self-contained HTML file with five redesign directions for mussejusse.com.

Each direction is a full homepage for desktop (1440 x 1000) and mobile (390 x 844),
rendered live side by side. Fonts are embedded, no external assets.
"""

from pathlib import Path
import math
import random
import re

ROOT = Path(__file__).resolve().parent
FONTS = (ROOT / "round-four-assets" / "fonts.css").read_text()

ARROW = (
    '<svg viewBox="0 0 24 24" aria-hidden="true" class="ar">'
    '<path d="M6 18 L18 6 M9 6h9v9"/></svg>'
)

SHELL_CSS = """
:root{--ink:#f1f0ec;--dim:#8a8a90;--line:#242428;--bg:#0a0a0b}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 Archivo,system-ui,sans-serif;-webkit-font-smoothing:antialiased}
h1,h2,h3,p{margin:0;font-weight:400}
a{color:inherit}
.wrap{max-width:1800px;margin:0 auto;padding:0 clamp(16px,3vw,54px) 110px}
.top{position:sticky;top:0;z-index:300;background:rgba(10,10,11,.84);backdrop-filter:blur(18px);border-bottom:1px solid var(--line)}
.top .row{max-width:1800px;margin:0 auto;padding:13px clamp(16px,3vw,54px);display:flex;justify-content:space-between;align-items:center;gap:18px}
.top strong{font-weight:600;font-size:14.5px;letter-spacing:-.01em}
.top .meta{font:400 11px/1 'Space Mono',monospace;letter-spacing:.12em;color:var(--dim);text-transform:uppercase}
.nav{display:flex;gap:6px}
.nav a{font:700 11px/1 'Space Mono',monospace;letter-spacing:.08em;padding:7px 12px;border:1px solid var(--line);text-decoration:none;transition:background 160ms ease-out,color 160ms ease-out}
.nav a:hover{background:var(--ink);color:#0a0a0b}
.intro{padding:64px 0 4px;max-width:82ch}
.intro .k{font:400 11px/1 'Space Mono',monospace;letter-spacing:.24em;color:var(--dim);text-transform:uppercase}
.intro h2{font-size:clamp(28px,3.6vw,52px);line-height:1.04;letter-spacing:-.03em;font-weight:600;margin:16px 0 0}
.intro p{color:var(--dim);margin-top:16px;max-width:70ch}
.direction{padding-top:84px;scroll-margin-top:64px}
.dhead{display:grid;grid-template-columns:auto 1fr;gap:6px 26px;align-items:baseline;border-top:1px solid var(--line);padding-top:20px}
.dhead .letter{font:400 12px/1 'Space Mono',monospace;color:var(--dim);letter-spacing:.12em;grid-row:1/span 2;padding-top:6px}
.dhead h3{font-size:clamp(22px,2.6vw,34px);font-weight:600;letter-spacing:-.025em}
.dhead p{color:var(--dim);font-size:14px;max-width:80ch}
.views{display:grid;grid-template-columns:minmax(0,1440fr) minmax(0,390fr);gap:28px;align-items:start;margin-top:26px}
.view{min-width:0}
.vlabel{display:flex;justify-content:space-between;gap:12px;font:400 10.5px/1 'Space Mono',monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--dim);margin-bottom:9px}
.vlabel b{color:var(--ink);font-weight:700}
.canvas{container-type:inline-size;width:100%;overflow:hidden;position:relative;background:#000;box-shadow:inset 0 0 0 1px #26262a}
.site{width:100%;position:relative;overflow:hidden;font-size:1.25cqw;line-height:1.45;-webkit-font-smoothing:antialiased}
.desktop .site{height:69.4444cqw}
.mobile .site{height:216.4103cqw}
.site a{color:inherit;text-decoration:none}
.site a:focus-visible{outline:2px solid currentColor;outline-offset:3px}
.site h1,.site h2,.site h3,.site h4,.site p,.site figure,.site figcaption,.site dl,.site dd,.site dt,.site ol,.site ul,.site li{margin:0;padding:0;font-weight:400}
.site ul,.site ol{list-style:none}
.site svg{display:block}
.site button{font:inherit;color:inherit;background:none;border:0;padding:0;cursor:pointer}
.site svg text{font-family:inherit}
.ar{fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.foot{margin-top:96px;border-top:1px solid var(--line);padding-top:20px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px;color:var(--dim);font-size:13px}
.foot a{text-decoration:underline;text-underline-offset:4px}
@media(max-width:1180px){.views{grid-template-columns:1fr}.view.mobile{width:min(100%,390px)}.dhead{grid-template-columns:auto 1fr}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}.site *{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}
.site button:focus-visible{outline:2px solid currentColor;outline-offset:3px}
.gdefs{position:absolute;width:0;height:0;overflow:hidden}
"""


def site_pair(body: str) -> str:
    d = body.replace("{u}", "d")
    m = body.replace("{u}", "m")
    d = re.sub(r"<!--m-->.*?<!--/m-->", "", d, flags=re.S)
    m = re.sub(r"<!--d-->.*?<!--/d-->", "", m, flags=re.S)
    return (
        f'<div class="view desktop"><div class="vlabel"><b>Desktop</b><span>1440 &times; 1000</span></div>'
        f'<div class="canvas"><div class="site-slot">{d}</div></div></div>'
        f'<div class="view mobile"><div class="vlabel"><b>Mobile</b><span>390 &times; 844</span></div>'
        f'<div class="canvas"><div class="site-slot">{m}</div></div></div>'
    )


# ---------------------------------------------------------------------------
# helpers for generated svg
# ---------------------------------------------------------------------------


def sine_path(x1, y, x2, amp, period, step=7):
    pts = []
    x = x1
    while x <= x2:
        pts.append((x, y + amp * math.sin((x - x1) / period * 2 * math.pi)))
        x += step
    return "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in pts)


def perf_edge(x1, y1, x2, y2, nx, ny, r):
    """One scalloped edge of a stamp. nx,ny is the inward unit normal."""
    dist = math.hypot(x2 - x1, y2 - y1)
    n = max(1, round(dist / (2 * r)))
    inner = 0.62 * r
    d = ""
    for i in range(n):
        t0, t1 = i / n, (i + 1) / n
        ax, ay = x1 + (x2 - x1) * t0, y1 + (y2 - y1) * t0
        bx, by = x1 + (x2 - x1) * t1, y1 + (y2 - y1) * t1
        mx, my = (ax + bx) / 2 + nx * inner, (ay + by) / 2 + ny * inner
        d += f"L{ax:.1f},{ay:.1f}Q{mx:.1f},{my:.1f} {bx:.1f},{by:.1f}"
    return d


def stamp_path(w, h, r=6):
    d = f"M0,0"
    d += perf_edge(0, 0, w, 0, 0, 1, r)
    d += perf_edge(w, 0, w, h, -1, 0, r)
    d += perf_edge(w, h, 0, h, 0, -1, r)
    d += perf_edge(0, h, 0, 0, 1, 0, r)
    return d + "Z"


def circle_text_path(cx, cy, r):
    return (
        f"M{cx - r},{cy} a{r},{r} 0 1,1 {2 * r},0 a{r},{r} 0 1,1 {-2 * r},0"
    )


# ---------------------------------------------------------------------------
# A / Par Avion
# ---------------------------------------------------------------------------

PA_CSS = """
.pa{background:#eee5d0;color:#241f18;font-family:'Fraunces',Georgia,serif;line-height:1.3}
.pa:before{content:'';position:absolute;inset:0;pointer-events:none;z-index:30;opacity:.5;mix-blend-mode:multiply;
 background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='220' height='220'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/%3E%3CfeColorMatrix values='0 0 0 0 .62 0 0 0 0 .55 0 0 0 0 .42 0 0 0 .05 0'/%3E%3C/filter%3E%3Crect width='220' height='220' filter='url(%23n)'/%3E%3C/svg%3E")}
.pa-band{position:absolute;left:0;right:0;height:1.05cqw;z-index:9;background:repeating-linear-gradient(45deg,#c8402f 0 1.5cqw,#f2ead9 1.5cqw 3cqw,#2f4f9e 3cqw 4.5cqw,#f2ead9 4.5cqw 6cqw)}
.pa-band.t{top:0}.pa-band.b{bottom:0}
.pa-kicker{position:absolute;left:4.2cqw;top:3.1cqw;font-family:'Space Mono',monospace;font-size:.62cqw;letter-spacing:.34em;color:#8a7c62;text-transform:uppercase;z-index:8}
.pa-name{position:absolute;left:4.2cqw;top:5.2cqw;z-index:8;width:36cqw}
.pa-name h1{font-size:6.6cqw;line-height:.92;font-weight:600;letter-spacing:-.015em}
.pa-name h1 em{font-style:italic;font-weight:300;color:#c8402f}
.pa-name p{margin-top:1.4cqw;font-size:1.12cqw;line-height:1.5;color:#5c5240;max-width:26cqw}
.pa-name .rule{width:7cqw;height:.22cqw;background:#241f18;margin-top:1.6cqw}
.pa-post{position:absolute;right:3.4cqw;top:2.6cqw;z-index:7;width:17cqw;height:17cqw;transform:rotate(-9deg)}
.pa-post svg{width:100%;height:100%;overflow:visible}
.pa-post text{font-family:'Space Mono',monospace;fill:#4a4234}
.pa-wave{position:absolute;right:21.6cqw;top:9.2cqw;width:12cqw;height:5cqw;z-index:6;opacity:.75}
.pa-wave svg{width:100%;height:100%}
.pa-env{position:absolute;display:block;width:39cqw;height:25cqw;z-index:4;outline:none}
.pa-env.e1{left:33cqw;top:24.5cqw;transform:rotate(-1.4deg)}
.pa-env.e2{left:52cqw;top:45cqw;width:36cqw;height:20cqw;transform:rotate(1.7deg)}
.pa-env .body{position:absolute;display:block;inset:0;z-index:2;background:#f8f3e4;box-shadow:0 1.2cqw 2.6cqw rgba(64,48,20,.22),0 .15cqw 0 rgba(64,48,20,.18);
 transition:transform 320ms cubic-bezier(.23,1,.32,1),box-shadow 320ms cubic-bezier(.23,1,.32,1)}
.pa-env .chev{position:absolute;left:0;right:0;height:.62cqw;background:repeating-linear-gradient(45deg,#c8402f 0 .8cqw,#f8f3e4 .8cqw 1.6cqw,#2f4f9e 1.6cqw 2.4cqw,#f8f3e4 2.4cqw 3.2cqw)}
.pa-env .chev.t{top:0}.pa-env .chev.b{bottom:0}
.pa-env .flap{position:absolute;left:0;right:0;top:0;height:38%;background:#f1ead8;clip-path:polygon(0 0,100% 0,50% 100%);border-bottom:1px solid rgba(90,74,44,.25)}
.pa-env .stamp{position:absolute;right:1.6cqw;top:1.7cqw;width:8.2cqw;transform:rotate(2.5deg);transition:transform 260ms cubic-bezier(.23,1,.32,1),filter 260ms ease-out;filter:drop-shadow(0 .18cqw .1cqw rgba(60,44,16,.28))}
.pa-env .stamp svg{width:100%;height:auto}
.pa-env .addr{position:absolute;left:3.4cqw;top:26%;width:22cqw;font-family:'Space Mono',monospace;color:#2b251c;text-transform:uppercase}
.pa-env .addr .to{font-size:.56cqw;letter-spacing:.3em;color:#9b8c6e}
.pa-env .addr h2{font-size:1.62cqw;line-height:1.12;letter-spacing:.02em;font-weight:700;margin-top:.55cqw}
.pa-env .addr .url{margin-top:.85cqw;font-size:.6cqw;letter-spacing:.12em;color:#7c6c4e}
.pa-env .postmark{position:absolute;right:11.6cqw;top:8.6cqw;width:7.6cqw;height:7.6cqw;transform:rotate(-12deg);opacity:.85}
.pa-env .postmark svg{width:100%;height:100%;overflow:visible}
.pa-env .postmark text{font-family:'Space Mono',monospace;fill:#6b5c40}
.pa-env .sender{position:absolute;left:3.4cqw;bottom:1.4cqw;font-family:'Space Mono',monospace;font-size:.52cqw;letter-spacing:.18em;color:#a2946f;text-transform:uppercase}
.pa-env .prio{position:absolute;left:3.4cqw;top:6cqw;transform:rotate(-4deg);background:#c8402f;color:#f8f3e4;font-family:'Space Mono',monospace;font-size:.56cqw;letter-spacing:.24em;padding:.45cqw .8cqw;text-transform:uppercase}
.pa-env .letter{position:absolute;display:block;left:6%;right:6%;bottom:6%;min-height:70%;background:#fbf8ee;border:1px solid rgba(90,74,44,.35);padding:2.2cqw 2.4cqw;z-index:3;
 box-shadow:0 -.4cqw 1.2cqw rgba(64,48,20,.2);transition:transform 340ms cubic-bezier(.23,1,.32,1),opacity 240ms ease-out;opacity:0;transform:translateY(9%) scale(.985);transform-origin:50% 100%}
.pa-env .letter .no{font-family:'Space Mono',monospace;font-size:.55cqw;letter-spacing:.3em;color:#9b8c6e;text-transform:uppercase}
.pa-env .letter h3{font-size:2.05cqw;line-height:1;font-weight:600;margin-top:.7cqw}
.pa-env .letter p{margin-top:.7cqw;font-size:.98cqw;line-height:1.45;color:#5c5240;max-width:24cqw;font-family:'Archivo',sans-serif}
.pa-env .letter .go{margin-top:1.1cqw;display:flex;width:max-content;align-items:center;gap:.6cqw;font-family:'Space Mono',monospace;font-size:.58cqw;letter-spacing:.24em;color:#c8402f;text-transform:uppercase}
.pa-env .letter .go .ar{width:.9cqw;height:.9cqw}
.pa-env:hover .body,.pa-env:focus-visible .body{transform:translateY(-.9cqw);box-shadow:0 2.2cqw 4cqw rgba(64,48,20,.3),0 .15cqw 0 rgba(64,48,20,.18)}
.pa-env:hover .stamp,.pa-env:focus-visible .stamp{transform:rotate(-1.5deg) translate(-.35cqw,-.5cqw)}
.pa-env:hover .letter,.pa-env:focus-visible .letter{opacity:1;transform:translateY(0) scale(1)}
.pa-back{position:absolute;left:4.2cqw;bottom:4.4cqw;z-index:8;display:flex;gap:1.6cqw}
.pa-back .lab{display:block;border:.14cqw solid #241f18;padding:.9cqw 1.2cqw;background:#f8f3e4;transition:background 200ms ease-out,color 200ms ease-out,transform 200ms cubic-bezier(.23,1,.32,1)}
.pa-back .lab .lb{display:block;font-family:'Space Mono',monospace;font-size:.52cqw;letter-spacing:.28em;color:#8a7c62;text-transform:uppercase}
.pa-back .lab .nm{display:block;font-size:1.16cqw;font-weight:600;margin-top:.35cqw}
.pa-back .lab:hover{background:#241f18;color:#f2ead9;transform:translateY(-.3cqw)}
.pa-back .lab:hover .lb{color:#c9a86e}
.pa-customs{position:absolute;left:4.2cqw;bottom:11.6cqw;z-index:8;border:.14cqw solid #241f18;background:#fdfaf0;padding:.8cqw 1.1cqw;transform:rotate(-.8deg)}
.pa-customs .hd{font-family:'Space Mono',monospace;font-size:.5cqw;letter-spacing:.26em;color:#8a7c62;text-transform:uppercase}
.pa-customs .ln{margin-top:.45cqw;font-family:'Space Mono',monospace;font-size:.56cqw;letter-spacing:.06em;color:#3b342a}
.pa-edge{position:absolute;right:4.2cqw;bottom:4.4cqw;z-index:8;text-align:right;font-family:'Space Mono',monospace;font-size:.56cqw;letter-spacing:.22em;color:#8a7c62;text-transform:uppercase;line-height:2.1}
.pa-edge b{color:#c8402f;font-weight:400}
.pa-edge .en{display:block;margin-top:1cqw;font-family:'Fraunces',serif;font-style:italic;font-size:1.1cqw;letter-spacing:0;text-transform:none;color:#5c5240}
.pa-soc-row{display:none}
.mobile .pa-kicker{left:6cqw;top:3cqw;font-size:1.5cqw;letter-spacing:.2em}
.mobile .pa-name{position:relative;inset:auto;width:auto;margin:0 6cqw;padding-top:10cqw}
.mobile .pa-name h1{font-size:10.5cqw}
.mobile .pa-name p{margin-top:2.4cqw;font-size:2.4cqw;max-width:80cqw}
.mobile .pa-name .rule{height:.5cqw;width:14cqw;margin-top:2.6cqw}
.mobile .pa-post{display:none}
.mobile .pa-wave{display:none}
.mobile .pa-env{position:relative;inset:auto;width:auto;height:auto;transform:none;display:block;margin:7cqw 6cqw 0}
.mobile .pa-env.e2{margin-top:6cqw}
.mobile .pa-env .body{position:relative;inset:auto;height:36cqw}
.mobile .pa-env .addr{left:5cqw;top:26%;width:62cqw}
.mobile .pa-env .addr .to{font-size:1.5cqw}
.mobile .pa-env .addr h2{font-size:4cqw;margin-top:1.1cqw}
.mobile .pa-env .addr .url{margin-top:1.6cqw;font-size:1.6cqw}
.mobile .pa-env .stamp{right:3.4cqw;top:3cqw;width:15cqw}
.mobile .pa-env .postmark{right:19cqw;top:16cqw;width:13cqw;height:13cqw}
.mobile .pa-env .prio{left:5cqw;top:9cqw;font-size:1.4cqw;padding:.9cqw 1.5cqw}
.mobile .pa-env .sender{left:5cqw;bottom:2cqw;font-size:1.3cqw}
.mobile .pa-env .chev{height:1.5cqw}
.mobile .pa-env .flap{height:30%}
.mobile .pa-env .letter{position:relative;left:auto;right:auto;top:auto;bottom:auto;min-height:0;height:auto;margin:0 2.4cqw;padding:3cqw 3.4cqw;opacity:1;transform:none;box-shadow:0 1.2cqw 2.4cqw rgba(64,48,20,.16)}
.mobile .pa-env .letter h3{font-size:4.2cqw;margin-top:1.4cqw}
.mobile .pa-env .letter p{font-size:2.4cqw;max-width:76cqw;margin-top:1.6cqw}
.mobile .pa-env .letter .no{font-size:1.4cqw}
.mobile .pa-env .letter .go{font-size:1.5cqw;margin-top:2.2cqw;gap:1.2cqw}
.mobile .pa-env .letter .go .ar{width:2.2cqw;height:2.2cqw}
.mobile .pa-customs,.mobile .pa-edge{display:none}
.mobile .pa-back{position:relative;inset:auto;margin:6cqw 6cqw 0;display:grid;grid-template-columns:1fr 1fr 1fr;gap:2.4cqw}
.mobile .pa-back .lab{padding:2cqw 2.2cqw;border-width:.35cqw;text-align:center}
.mobile .pa-back .lab .lb{font-size:1.3cqw}
.mobile .pa-back .lab .nm{font-size:2.8cqw;margin-top:.9cqw}
.pa-customs-m{display:none}
.pa-foot-m{display:none}
.mobile .pa-foot-m{display:none}
.mobile .pa-customs-m{display:none}
"""


def pa_stamp(art, top, denom, alt=False):
    w, h = 132, 158
    d = stamp_path(w, h, 5.5)
    return f"""<svg viewBox="0 0 {w} {h}" aria-hidden="true">
<path d="{d}" fill="#fdfaf0" stroke="rgba(60,44,16,.35)" stroke-width=".8"/>
<rect x="9" y="9" width="{w - 18}" height="{h - 18}" fill="none" stroke="{'#57683f' if alt else '#2f4f9e'}" stroke-width="1.4"/>
<text x="{w/2}" y="22" text-anchor="middle" font-family="Space Mono" font-size="7.2" letter-spacing="1.6" fill="#4a4234">{top}</text>
{art}
<text x="{w/2}" y="{h-12}" text-anchor="middle" font-family="Space Mono" font-size="10" fill="#241f18">{denom}</text>
</svg>"""


def pa_body(u):
    roundest_art = """<g>
<circle cx="66" cy="86" r="34" fill="none" stroke="#2f4f9e" stroke-width="1.3"/>
<circle cx="66" cy="86" r="27" fill="#2f4f9e" opacity=".14"/>
<circle cx="66" cy="86" r="19" fill="none" stroke="#c8402f" stroke-width="1.1" stroke-dasharray="2 2"/>
<circle cx="58" cy="78" r="4.4" fill="#2f4f9e" opacity=".5"/>
<text x="66" y="140" text-anchor="middle" font-family="Space Mono" font-size="6" letter-spacing="1.2" fill="#8a7c62">1ST CLASS EXPERIMENT</text>
</g>"""
    models_art = """<g>
<g stroke="#57683f" stroke-width="1" opacity=".55">
<line x1="30" y1="66" x2="48" y2="54"/><line x1="48" y1="54" x2="66" y2="64"/><line x1="66" y1="64" x2="88" y2="44"/>
<line x1="48" y1="54" x2="60" y2="34"/><line x1="60" y1="34" x2="66" y2="64"/><line x1="88" y1="44" x2="102" y2="58"/>
<line x1="66" y1="64" x2="84" y2="82"/><line x1="84" y1="82" x2="102" y2="58"/></g>
<g fill="#57683f"><circle cx="30" cy="66" r="3"/><circle cx="48" cy="54" r="4"/><circle cx="66" cy="64" r="2.6"/><circle cx="88" cy="44" r="4.4"/><circle cx="60" cy="34" r="2.4"/><circle cx="102" cy="58" r="3.4"/><circle cx="84" cy="82" r="2.6"/></g>
<rect x="26" y="94" width="80" height="16" fill="none" stroke="#4a4234" stroke-width=".8" stroke-dasharray="3 2"/>
<text x="66" y="105" text-anchor="middle" font-family="Space Mono" font-size="5.6" letter-spacing="1.2" fill="#8a7c62">CATALOGUE No. 2</text>
</g>"""
    def pm_small(uid):
        return f"""<svg viewBox="0 0 96 96">
<circle cx="48" cy="48" r="38" fill="none" stroke="#6b5c40" stroke-width="1.2"/>
<circle cx="48" cy="48" r="29" fill="none" stroke="#6b5c40" stroke-width=".8"/>
<path id="pms{uid}" d="{circle_text_path(48, 48, 33.5)}" fill="none"/>
<text font-size="6.4" letter-spacing="1.1"><textPath href="#pms{uid}" startOffset="4%">MUSSEJUSSE POST</textPath></text>
<text x="48" y="46" text-anchor="middle" font-size="11" font-family="Space Mono" fill="#3b342a">V4</text>
<text x="48" y="58" text-anchor="middle" font-size="5.6" font-family="Space Mono" fill="#6b5c40">2026</text>
<path d="{sine_path(12, 76, 84, 2.4, 9, 4)}" fill="none" stroke="#6b5c40" stroke-width="1"/>
<path d="{sine_path(12, 82, 84, 2.4, 9, 4)}" fill="none" stroke="#6b5c40" stroke-width="1"/>
</svg>"""

    big_post = f"""<svg viewBox="0 0 240 240">
<g transform="rotate(0 120 120)">
<circle cx="120" cy="120" r="96" fill="none" stroke="#5c5240" stroke-width="2"/>
<circle cx="120" cy="120" r="80" fill="none" stroke="#5c5240" stroke-width="1"/>
<path id="pmb{u}" d="{circle_text_path(120, 120, 88)}" fill="none"/>
<text font-size="12.4" letter-spacing="1.8" fill="#4a4234" font-family="Space Mono">
<textPath href="#pmb{u}" startOffset="4%">MUSSEJUSSE &#183; EST. 2024 &#183; ALWAYS BUILDING &#183;</textPath></text>
<text x="120" y="112" text-anchor="middle" font-size="30" font-family="Space Mono" fill="#3b342a">V4</text>
<text x="120" y="136" text-anchor="middle" font-size="12" font-family="Space Mono" fill="#6b5c40">2026</text>
<path d="{sine_path(30, 186, 210, 5, 16, 6)}" fill="none" stroke="#5c5240" stroke-width="1.6"/>
<path d="{sine_path(30, 198, 210, 5, 16, 6)}" fill="none" stroke="#5c5240" stroke-width="1.6"/>
</g>
</svg>"""
    big_wave = f"""<svg viewBox="0 0 200 72" preserveAspectRatio="none">
<path d="{sine_path(0, 14, 200, 6, 18, 5)}" fill="none" stroke="#5c5240" stroke-width="1.4"/>
<path d="{sine_path(0, 32, 200, 6, 18, 5)}" fill="none" stroke="#5c5240" stroke-width="1.4"/>
<path d="{sine_path(0, 50, 200, 6, 18, 5)}" fill="none" stroke="#5c5240" stroke-width="1.4"/>
</svg>"""

    def env(cls, stamp, href, label, h2, url, no, blurb, stack, sender, prio, uid):
        pms_id = u + "-" + uid
        return f"""
<a class="pa-env {cls}" href="{href}" aria-label="{label}">
  <span class="body">
    <span class="chev t"></span>
    <span class="flap"></span>
    <span class="prio">{prio}</span>
    <span class="stamp">{stamp}</span>
    <span class="postmark">{pm_small(pms_id)}</span>
    <span class="addr">
      <span class="to">Deliver to</span>
      <h2>{h2}</h2>
      <span class="url">{url}</span>
    </span>
    <span class="sender">{sender}</span>
    <span class="chev b"></span>
  </span>
  <span class="letter">
    <span class="no">{no}</span>
    <h3>{label}</h3>
    <p>{blurb}</p>
    <span class="go">{stack} {ARROW}</span>
  </span>
</a>"""

    return f"""
<div class="site pa {u}">
  <span class="pa-band t" aria-hidden="true"></span>
  <span class="pa-band b" aria-hidden="true"></span>
  <div class="pa-kicker">Edition 4 &middot; Airmail &middot; Printed in the browser</div>
  <div class="pa-name">
    <h1>Musse<br><em>Jusse</em></h1>
    <div class="rule"></div>
    <p>Building and experimenting with cutting-edge technology, then posting the results before they are dry.</p>
  </div>
  <div class="pa-post" aria-hidden="true">{big_post}</div>
  <div class="pa-wave" aria-hidden="true">{big_wave}</div>
  {env("e1", pa_stamp(roundest_art, "ROUNDEST POKEMON", "&#8734;"), "https://roundest.mussejusse.com",
       "Roundest Pok&eacute;mon", "ROUNDEST<br>POK&Eacute;MON", "c/o roundest.mussejusse.com",
       "MJ-001 &middot; Next.js 16", "A comparison built around one question: which one is rounder? Server actions answer it, a cache remembers the answer.",
       "Next.js 16 &middot; cache &middot; actions", "MUSSEJUSSE &middot; THE INTERNET", "Priority", "e1")}
  {env("e2", pa_stamp(models_art, "MODELS", "&#8734;", alt=True), "https://models.mussejusse.com",
       "Models", "MODELS", "c/o models.mussejusse.com",
       "MJ-002 &middot; Astro", "A catalogue of models, providers and what each one can do. Static pages, almost no client code, quick everywhere.",
       "Astro &middot; models.dev", "MUSSEJUSSE &middot; THE INTERNET", "Par avion", "e2")}
  <div class="pa-customs">
    <div class="hd">Customs declaration</div>
    <div class="ln">CONTENTS: 1 (ONE) PERSONAL WEBSITE</div>
    <div class="ln">ITEMS: 2 EXPERIMENTS &#183; VALUE: NOTHING TO DECLARE</div>
  </div>
  <div class="pa-back">
    <a class="lab" href="https://bsky.app/profile/mussejusse.com"><span class="lb">Return to</span><span class="nm">Bluesky</span></a>
    <a class="lab" href="https://github.com/MusseJusse"><span class="lb">Return to</span><span class="nm">GitHub</span></a>
    <a class="lab" href="https://vercel.com"><span class="lb">Return to</span><span class="nm">Vercel</span></a>
  </div>
  <div class="pa-customs-m">
    <div class="hd">Customs declaration</div>
    <div class="ln">CONTENTS: 1 (ONE) PERSONAL WEBSITE</div>
    <div class="ln">ITEMS: 2 EXPERIMENTS &#183; VALUE: NOTHING DECLARED</div>
  </div>
  <div class="pa-edge">
    <span>Postage paid &middot; <b>&#8734;</b></span>
    <span>If undeliverable, return to sender</span>
    <span class="en">Some things start with a loose end.</span>
  </div>
  <div class="pa-foot-m">Postage paid &#8734; &middot; return to sender</div>
</div>"""


# ---------------------------------------------------------------------------
# B / Darkroom
# ---------------------------------------------------------------------------

DR_CSS = """
.dr{background:
 radial-gradient(46cqw 40cqw at 6% -4%,rgba(196,58,40,.34),rgba(196,58,40,0) 62%),
 radial-gradient(30cqw 24cqw at 58% -8%,rgba(150,42,28,.2),rgba(150,42,28,0) 70%),
 linear-gradient(#0e0b0c,#0a0809 60%,#080707);
 color:#e3dbcf;font-family:'Archivo',sans-serif;line-height:1.4;--wall:#0e0b0c;--accent:#c43a28;--glow:.34}
.dr:after{content:'';position:absolute;inset:0;pointer-events:none;z-index:28;opacity:.4;mix-blend-mode:overlay;
 background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='2'/%3E%3C/filter%3E%3Crect width='180' height='180' filter='url(%23n)' opacity='.55'/%3E%3C/svg%3E")}
.dr.lit{background:
 radial-gradient(46cqw 40cqw at 6% -4%,rgba(255,240,208,.13),rgba(255,240,208,0) 62%),
 radial-gradient(30cqw 24cqw at 58% -8%,rgba(210,220,255,.06),rgba(210,220,255,0) 70%),
 linear-gradient(#131316,#0d0d10 60%,#0a0a0c);--accent:#e8e2d6}
.dr-strip{position:absolute;left:0;right:0;top:0;height:4.6cqw;z-index:12;display:flex;align-items:center;gap:2.2cqw;padding:0 4.2cqw;border-bottom:1px solid rgba(255,255,255,.09);font-family:'Space Mono',monospace;font-size:.6cqw;letter-spacing:.24em;text-transform:uppercase;color:#9c8f83;background:rgba(8,6,7,.5)}
.dr-led{width:.7cqw;height:.7cqw;border-radius:50%;background:#ff4a33;box-shadow:0 0 1.2cqw rgba(255,74,51,.9);animation:dr-pulse 2.4s ease-in-out infinite}
@keyframes dr-pulse{0%,100%{opacity:1}50%{opacity:.25}}
.dr-strip .sp{margin-left:auto}
.dr-switch{display:flex;align-items:center;gap:.8cqw;border:.14cqw solid rgba(255,255,255,.22);padding:.55cqw 1cqw;background:rgba(255,255,255,.04);transition:background 220ms ease-out,border-color 220ms ease-out}
.dr-switch:hover{background:rgba(255,255,255,.1)}
.dr-switch .track{position:relative;width:2.6cqw;height:1.2cqw;border:1px solid rgba(255,255,255,.4);border-radius:1.2cqw;background:rgba(0,0,0,.4)}
.dr-switch .knob{position:absolute;top:.1cqw;left:.12cqw;width:.86cqw;height:.86cqw;border-radius:50%;background:#d8cdbf;transition:transform 220ms cubic-bezier(.23,1,.32,1),background 220ms ease-out}
.dr.lit .dr-switch .knob{transform:translateX(1.34cqw);background:#fff6df}
.dr-switch .st{color:#c9bcaf}
.dr.lit .dr-switch .st{color:#fff6df}
.dr-title{position:absolute;left:4.2cqw;top:8.6cqw;z-index:8;width:29cqw}
.dr-title .kick{font-family:'Space Mono',monospace;font-size:.58cqw;letter-spacing:.32em;text-transform:uppercase;color:#a89a8d}
.dr-title h1{font-size:4.4cqw;line-height:1;font-weight:800;letter-spacing:-.015em;text-transform:uppercase;margin-top:1cqw;color:#efe7da}
.dr-title .circle{position:absolute;left:-2.4cqw;top:.7cqw;width:27cqw;height:10.8cqw;pointer-events:none}
.dr-title .circle path{fill:none;stroke:#d9cfbf;stroke-width:2.4;opacity:.75}
.dr-title p{margin-top:1.6cqw;font-family:'Instrument Serif',Georgia,serif;font-style:italic;font-size:1.5cqw;line-height:1.4;color:#c9bcaf;max-width:24cqw}
.dr-meta{margin-top:2cqw;display:flex;gap:1.6cqw;font-family:'Space Mono',monospace;font-size:.56cqw;letter-spacing:.2em;text-transform:uppercase;color:#8c7f74}
.dr-meta b{color:#e8dfd1;font-weight:400}
.dr-timer{position:absolute;left:4.6cqw;top:31cqw;z-index:8;display:flex;align-items:center;gap:1.2cqw}
.dr-timer .g{width:5.4cqw;height:5.4cqw}
.dr-timer .g svg{width:100%;height:100%;overflow:visible}
.dr-timer .t .big{font-family:'Space Mono',monospace;font-size:.86cqw;letter-spacing:.12em;color:#e8dfd1}
.dr-timer .t .sm{margin-top:.4cqw;font-family:'Space Mono',monospace;font-size:.54cqw;letter-spacing:.22em;text-transform:uppercase;color:#8c7f74}
.dr-wire{position:absolute;left:0;right:0;top:9cqw;height:9cqw;z-index:3;pointer-events:none}
.dr-wire svg{width:100%;height:100%}
.dr-print{position:absolute;z-index:5;display:block;transition:transform 320ms cubic-bezier(.23,1,.32,1)}
.dr-print.p1{left:38.5cqw;top:12.4cqw;width:32cqw;transform:rotate(-1.7deg)}
.dr-print.p2{left:72cqw;top:14cqw;width:24cqw;transform:rotate(1.3deg)}
.dr-print:hover,.dr-print:focus-visible{transform:rotate(0deg) translateY(-.6cqw)}
.dr-print .clip{position:absolute;left:50%;top:-1.5cqw;width:1.5cqw;height:2.6cqw;transform:translateX(-50%);z-index:2}
.dr-print .frame{display:block;background:#efe9dc;padding:1.5cqw 1.5cqw 0;box-shadow:0 1.6cqw 3.4cqw rgba(0,0,0,.6),0 .2cqw .4cqw rgba(0,0,0,.5)}
.dr-print .img{position:relative;display:block;background:#0b0909;overflow:hidden;aspect-ratio:4/3}
.dr-print.p2 .img{aspect-ratio:5/4}
.dr-print .img svg{position:absolute;inset:0;width:100%;height:100%}
.dr-print .img .dev{opacity:.3;filter:blur(7px) saturate(.5);transform:scale(1.03);transition:opacity 620ms cubic-bezier(.23,1,.32,1),filter 620ms cubic-bezier(.23,1,.32,1),transform 700ms cubic-bezier(.23,1,.32,1)}
.dr-print .img .latent{opacity:.5;transition:opacity 500ms ease-out}
.dr-print.dev-on .dev,.dr.lit .dr-print .dev{opacity:1;filter:none;transform:scale(1)}
.dr-print.dev-on .latent,.dr.lit .dr-print .latent{opacity:.08}
.dr-print .cap{display:block;padding:1.2cqw .2cqw 1.4cqw;font-family:'Instrument Serif',Georgia,serif;font-style:italic;font-size:1.02cqw;line-height:1.42;color:#4c443a}
.dr-print .cap b{font-style:normal;font-family:'Space Mono',monospace;font-size:.55cqw;letter-spacing:.22em;text-transform:uppercase;color:#8a7c6d;display:block;margin-bottom:.5cqw}
.dr-trays{position:absolute;left:4.2cqw;right:4.2cqw;bottom:4.4cqw;z-index:10;display:flex;gap:2.6cqw}
.dr-tray{position:relative;flex:1;height:13.4cqw;border-radius:.7cqw;background:linear-gradient(#2a2523,#181413);border:1px solid rgba(255,255,255,.09);box-shadow:inset 0 .6cqw 1.4cqw rgba(0,0,0,.7),0 1.2cqw 2.4cqw rgba(0,0,0,.5);display:block;padding:1.5cqw 1.8cqw;transition:transform 300ms cubic-bezier(.23,1,.32,1),border-color 300ms ease-out}
.dr-tray:hover,.dr-tray:focus-visible{transform:translateY(-.5cqw);border-color:rgba(255,180,140,.28)}
.dr-tray .liquid{position:absolute;inset:.75cqw;border-radius:.45cqw;background:linear-gradient(118deg,#241d18 0%,#3a2b1f 40%,#201915 70%,#2d241d);overflow:hidden}
.dr-tray .liquid:after{content:'';position:absolute;inset:0;background:linear-gradient(115deg,rgba(255,214,170,0) 30%,rgba(255,214,170,.16) 46%,rgba(255,214,170,0) 60%);transform:translateX(-70%);transition:transform 900ms cubic-bezier(.23,1,.32,1)}
.dr-tray:hover .liquid:after,.dr-tray:focus-visible .liquid:after{transform:translateX(70%)}
.dr-tray .tape{position:absolute;display:block;left:1.8cqw;top:2.2cqw;background:#efe9dc;color:#242020;padding:.5cqw .8cqw;font-family:'Space Mono',monospace;font-size:.55cqw;letter-spacing:.2em;text-transform:uppercase;transform:rotate(-1deg)}
.dr-tray .tname{position:absolute;left:1.8cqw;bottom:2.2cqw;right:1.8cqw;display:flex;align-items:flex-end;justify-content:space-between;gap:1cqw}
.dr-tray .tname h3{font-size:1.7cqw;font-weight:700;letter-spacing:-.01em;color:#f0e8db}
.dr-tray .tname .stack{font-family:'Space Mono',monospace;font-size:.52cqw;letter-spacing:.18em;text-transform:uppercase;color:#a1907c;text-align:right;line-height:1.9}
.dr-soc{position:absolute;right:4.2cqw;top:45.6cqw;z-index:8;text-align:right}
.dr-soc .hd{font-family:'Space Mono',monospace;font-size:.56cqw;letter-spacing:.3em;text-transform:uppercase;color:#8c7f74;margin-bottom:1.4cqw}
.dr-soc .row{display:flex;gap:1.4cqw;justify-content:flex-end}
.dr-soc a{position:relative;display:block;background:#0f0d0e;border:1px solid rgba(255,255,255,.14);padding:1.5cqw 1.1cqw .9cqw;font-family:'Space Mono',monospace;font-size:.56cqw;letter-spacing:.2em;text-transform:uppercase;color:#bfb2a4;transition:transform 240ms cubic-bezier(.23,1,.32,1),color 200ms ease-out,border-color 200ms ease-out}
.dr-soc a:before{content:'';position:absolute;left:50%;top:-.8cqw;width:.9cqw;height:1.4cqw;transform:translateX(-50%);border:.14cqw solid #6d6258;border-bottom:0;border-radius:.2cqw .2cqw 0 0}
.dr-soc a:hover{transform:translateY(-.4cqw);color:#f0e8db;border-color:rgba(255,180,140,.4)}
.dr-note{position:absolute;right:4.2cqw;top:40.6cqw;z-index:8;font-family:'Space Mono',monospace;font-size:.54cqw;letter-spacing:.2em;text-transform:uppercase;color:#6f645b;text-align:right;line-height:2}
.mobile .dr-strip{height:8.4cqw;gap:3cqw;padding:0 4.4cqw;font-size:1.35cqw}
.mobile .dr-led{width:1.6cqw;height:1.6cqw}
.mobile .dr-switch{padding:1.2cqw 2cqw;border-width:.3cqw;gap:1.4cqw}
.mobile .dr-switch .track{width:5.4cqw;height:2.6cqw;border-radius:2.6cqw}
.mobile .dr-switch .knob{width:1.9cqw;height:1.9cqw;top:.25cqw;left:.3cqw}
.mobile .dr.lit .dr-switch .knob{transform:translateX(2.8cqw)}
.mobile .dr-strip .hide-m{display:none}
.mobile .dr-title{position:relative;width:auto;margin:7cqw 5cqw 0}
.mobile .dr-title h1{font-size:8cqw;margin-top:2cqw}
.mobile .dr-title .circle{left:-2cqw;top:-1.4cqw;width:46cqw;height:21cqw}
.mobile .dr-title p{font-size:2.9cqw;margin-top:2.6cqw;max-width:82cqw}
.mobile .dr-meta{margin-top:2.6cqw;font-size:1.4cqw;gap:3cqw}
.mobile .dr-timer{display:none}
.mobile .dr-wire{display:none}
.mobile .dr-print{position:relative;inset:auto;width:auto;margin:9cqw 5cqw 0;transform:none}
.mobile .dr-print.p2{margin-top:4cqw}
.mobile .dr-print:hover,.mobile .dr-print:focus-visible{transform:none}
.mobile .dr-print .frame{padding:2.2cqw 2.2cqw 0;box-shadow:0 2.4cqw 5cqw rgba(0,0,0,.6)}
.mobile .dr-print .img{aspect-ratio:16/8}
.mobile .dr-print.p2 .img{aspect-ratio:16/8}
.mobile .dr-print .clip{top:-2.4cqw;width:2.6cqw;height:4.4cqw}
.mobile .dr-print .cap{font-size:2.6cqw;padding:2.4cqw .2cqw 2.6cqw}
.mobile .dr-print .cap b{font-size:1.4cqw;margin-bottom:1cqw}
.mobile .dr-soc{position:relative;inset:auto;margin:6cqw 5cqw 0;text-align:left}
.mobile .dr-soc .hd{font-size:1.4cqw;margin-bottom:2cqw}
.mobile .dr-soc .row{justify-content:flex-start;gap:4cqw}
.mobile .dr-soc a{font-size:1.6cqw;padding:0;border:0;background:none;border-bottom:.25cqw solid rgba(255,255,255,.3);padding-bottom:.8cqw;text-decoration:none}
.mobile .dr-soc a:before{display:none}
.mobile .dr-note{display:none}
.mobile .dr-trays{position:relative;inset:auto;margin:5cqw 5cqw 0;display:block}
.mobile .dr-tray{height:auto;display:flex;align-items:center;gap:2.4cqw;margin-top:2.6cqw;border-radius:1.6cqw;padding:2.6cqw 3cqw;border-width:.25cqw}
.mobile .dr-tray .liquid{display:none}
.mobile .dr-tray .tape{position:static;transform:none;font-size:1.3cqw;padding:.7cqw 1.6cqw}
.mobile .dr-tray .tname{position:static;margin:0;flex:1;align-items:center}
.mobile .dr-tray .tname h3{font-size:3.2cqw}
.mobile .dr-tray .tname .stack{font-size:1.25cqw}
.mobile .dr-foot{display:none}
.dr-foot{display:none}
.mobile .dr-foot{display:block}
"""


def dr_roundest():
    latent = """<g opacity=".85">
<rect width="400" height="300" fill="#0d0b0c"/>
<circle cx="200" cy="152" r="86" fill="none" stroke="#cbbfae" stroke-width="1.4"/>
<circle cx="200" cy="152" r="62" fill="none" stroke="#8d8174" stroke-width=".9" stroke-dasharray="3 4"/>
<line x1="60" y1="152" x2="340" y2="152" stroke="#6e655c" stroke-width=".7"/>
<line x1="200" y1="30" x2="200" y2="274" stroke="#6e655c" stroke-width=".7"/>
<text x="200" y="282" text-anchor="middle" font-family="Space Mono" font-size="9" letter-spacing="3" fill="#8d8174">FRAME 01 / ROUNDEST</text>
</g>"""
    dev = """<g>
<rect width="400" height="300" fill="#120d0b"/>
<circle cx="286" cy="212" r="52" fill="#241a14"/>
<circle cx="200" cy="152" r="86" fill="#0a0706"/>
<circle cx="200" cy="152" r="86" fill="url(#drg1)"/>
<ellipse cx="168" cy="116" rx="30" ry="22" fill="#fff2d8" opacity=".5"/>
<circle cx="200" cy="152" r="86" fill="url(#drg2)"/>
<circle cx="200" cy="152" r="86" fill="none" stroke="#f7ead0" stroke-opacity=".25" stroke-width="1"/>
<path d="M200 240 a88 88 0 0 0 84 -62" fill="none" stroke="#fff" stroke-opacity=".2" stroke-width="2"/>
<text x="200" y="282" text-anchor="middle" font-family="Space Mono" font-size="9" letter-spacing="3" fill="#bda58a">FRAME 01 / ROUNDEST</text>
</g>"""
    return latent, dev


def dr_models():
    latent = """<g opacity=".85">
<rect width="400" height="300" fill="#0d0b0c"/>
<g fill="none" stroke="#cbbfae" stroke-width="1">
<rect x="52" y="48" width="62" height="44"/><rect x="126" y="48" width="62" height="44"/><rect x="200" y="48" width="62" height="44"/><rect x="274" y="48" width="62" height="44"/>
<rect x="52" y="104" width="62" height="44"/><rect x="126" y="104" width="62" height="44"/><rect x="200" y="104" width="62" height="44"/><rect x="274" y="104" width="62" height="44"/>
<rect x="52" y="160" width="62" height="44"/><rect x="126" y="160" width="62" height="44"/><rect x="200" y="160" width="62" height="44"/><rect x="274" y="160" width="62" height="44"/>
</g>
<text x="200" y="248" text-anchor="middle" font-family="Space Mono" font-size="9" letter-spacing="3" fill="#8d8174">FRAME 02 / MODELS</text>
</g>"""
    dev = """<g>
<rect width="400" height="300" fill="#101418"/>
<g>
<rect x="52" y="48" width="62" height="44" rx="4" fill="#1d2836"/>
<rect x="126" y="48" width="62" height="44" rx="4" fill="#243447"/>
<rect x="200" y="48" width="62" height="44" rx="4" fill="#1a2330"/>
<rect x="274" y="48" width="62" height="44" rx="4" fill="url(#drg3)"/>
<rect x="52" y="104" width="62" height="44" rx="4" fill="#22303f"/>
<rect x="126" y="104" width="62" height="44" rx="4" fill="#1a2330"/>
<rect x="200" y="104" width="62" height="44" rx="4" fill="#e0a458"/>
<rect x="274" y="104" width="62" height="44" rx="4" fill="#1d2836"/>
<rect x="52" y="160" width="62" height="44" rx="4" fill="#1a2330"/>
<rect x="126" y="160" width="62" height="44" rx="4" fill="#26374a"/>
<rect x="200" y="160" width="62" height="44" rx="4" fill="#1d2836"/>
<rect x="274" y="160" width="62" height="44" rx="4" fill="#c98d4a"/>
</g>
<g fill="#8fa5bd" font-family="Space Mono" font-size="7">
<text x="60" y="74">GPT</text><text x="134" y="74">CLAUDE</text><text x="208" y="74">LLAMA</text><text x="282" y="74">GEMINI</text>
<text x="60" y="130">MISTRAL</text><text x="208" y="130" fill="#241a10">DEEPSEEK</text><text x="282" y="130">GROK</text>
</g>
<text x="200" y="248" text-anchor="middle" font-family="Space Mono" font-size="9" letter-spacing="3" fill="#9fb2c6">FRAME 02 / MODELS</text>
</g>"""
    return latent, dev


def dr_body(u):
    r_lat, r_dev = dr_roundest()
    m_lat, m_dev = dr_models()

    def clip_svg():
        return """<svg viewBox="0 0 24 42" aria-hidden="true">
<rect x="6" y="0" width="12" height="9" rx="2" fill="#5b5348"/>
<rect x="4" y="7" width="16" height="12" rx="3" fill="#8a8074"/>
<rect x="6" y="9" width="12" height="8" rx="2" fill="#b3a898"/>
<rect x="7" y="18" width="10" height="22" rx="2" fill="#6d655a"/>
<rect x="9" y="20" width="6" height="18" fill="#d8cdbf" opacity=".7"/>
</svg>"""

    timer = """<div class="g"><svg viewBox="0 0 100 100">
<circle cx="50" cy="50" r="44" fill="rgba(255,255,255,.03)" stroke="rgba(255,255,255,.18)" stroke-width="1.4"/>
<circle cx="50" cy="50" r="36" fill="none" stroke="rgba(255,255,255,.1)" stroke-width="1"/>
<g stroke="rgba(255,255,255,.3)" stroke-width="1.4">
<line x1="50" y1="6" x2="50" y2="14"/><line x1="94" y1="50" x2="86" y2="50"/><line x1="50" y1="94" x2="50" y2="86"/><line x1="6" y1="50" x2="14" y2="50"/>
</g>
<path d="M50 50 L50 24 A26 26 0 0 1 71 39 Z" fill="#e0a458" opacity=".22"/>
<line x1="50" y1="50" x2="66" y2="28" stroke="#e0a458" stroke-width="2.4" stroke-linecap="round"/>
<circle cx="50" cy="50" r="3" fill="#e0a458"/>
<text x="50" y="72" text-anchor="middle" font-family="Space Mono" font-size="13" fill="#e8dfd1">20</text>
</svg></div>"""

    return f"""
<div class="site dr {u}">
  <div class="dr-strip">
    <span class="dr-led" aria-hidden="true"></span>
    <span>Safelight</span>
    <span class="hide-m">Mussejusse.com &middot; darkroom</span>
    <span class="sp"></span>
    <span class="hide-m">Film 04 &middot; developed 2026</span>
    <button class="dr-switch" type="button" data-dr-switch aria-pressed="false">
      <span class="track" aria-hidden="true"><span class="knob"></span></span>
      <span class="st"><span data-dr-on>Inspection light</span></span>
    </button>
  </div>
  <div class="dr-title">
    <div class="kick">Roll 04 &middot; experiments, developed one at a time</div>
    <h1>Musse<br>Jusse</h1>
    <svg class="circle" viewBox="0 0 520 150" aria-hidden="true">
      <path d="M262 12 C 120 10 16 36 14 74 C 12 112 150 140 300 138 C 452 136 508 112 506 72 C 504 34 400 14 246 12"/>
      <path d="M258 18 C 140 20 28 42 26 76 C 24 106 160 132 306 130 C 448 128 498 104 496 70"/>
    </svg>
    <p>I build small things for the web. Some of them still develop.</p>
    <div class="dr-meta"><span>Est. <b>2024</b></span><span>Frames <b>2 of 2</b></span><span>Fixer <b>fresh</b></span></div>
  </div>
  <div class="dr-timer">{timer}
    <div class="t"><div class="big">T - 04 : 12</div><div class="sm">20.0 &deg;C &middot; agitation every 30s</div></div>
  </div>
  <div class="dr-wire" aria-hidden="true"><svg viewBox="0 0 1440 120" preserveAspectRatio="none">
    <path d="M-20 26 C 240 74 520 30 760 56 C 1000 82 1240 44 1460 60" fill="none" stroke="#4a423c" stroke-width="2"/>
    <path d="M-20 32 C 240 80 520 36 760 62 C 1000 88 1240 50 1460 66" fill="none" stroke="#2c2724" stroke-width="1"/>
  </svg></div>
  <a class="dr-print p1" data-dr-print="p1" href="https://roundest.mussejusse.com" aria-label="Roundest Pok&eacute;mon">
    <span class="clip" aria-hidden="true">{clip_svg()}</span>
    <span class="frame">
      <span class="img">
        <svg class="latent" viewBox="0 0 400 300" aria-hidden="true">{r_lat}</svg>
        <svg class="dev" viewBox="0 0 400 300" aria-hidden="true">{r_dev}</svg>
      </span>
      <span class="cap"><b>Frame 01 &middot; Next.js 16</b>Roundest Pok&eacute;mon. A question of what is roundest, answered by server actions and remembered by a cache.</span>
    </span>
  </a>
  <a class="dr-print p2" data-dr-print="p2" href="https://models.mussejusse.com" aria-label="Models">
    <span class="clip" aria-hidden="true">{clip_svg()}</span>
    <span class="frame">
      <span class="img">
        <svg class="latent" viewBox="0 0 400 300" aria-hidden="true">{m_lat}</svg>
        <svg class="dev" viewBox="0 0 400 300" aria-hidden="true">{m_dev}</svg>
      </span>
      <span class="cap"><b>Frame 02 &middot; Astro</b>Models. Every model, provider and capability, laid out like a contact sheet. Quick everywhere.</span>
    </span>
  </a>
  <div class="dr-note">Do not open the door<br>the prints are still in the fixer</div>
  <div class="dr-soc">
    <div class="hd">On the drying line</div>
    <div class="row">
      <a href="https://bsky.app/profile/mussejusse.com">Bluesky</a>
      <a href="https://github.com/MusseJusse">GitHub</a>
      <a href="https://vercel.com">Vercel</a>
    </div>
  </div>
  <div class="dr-trays">
    <a class="dr-tray" data-dr-tray="p1" href="https://roundest.mussejusse.com">
      <span class="liquid" aria-hidden="true"></span>
      <span class="tape">Developer &middot; 1</span>
      <span class="tname">
        <h3>Roundest Pok&eacute;mon</h3>
        <span class="stack">Next.js 16<br>Cache &middot; actions &middot; KV</span>
      </span>
    </a>
    <a class="dr-tray" data-dr-tray="p2" href="https://models.mussejusse.com">
      <span class="liquid" aria-hidden="true"></span>
      <span class="tape">Developer &middot; 2</span>
      <span class="tname">
        <h3>Models</h3>
        <span class="stack">Astro<br>Models.dev &middot; static</span>
      </span>
    </a>
  </div>
  <div class="dr-foot">Mussejusse &middot; safelight on &middot; 2026</div>
</div>"""


# ---------------------------------------------------------------------------
# C / Soundings
# ---------------------------------------------------------------------------

def gdefs():
    return (
        '<svg class="gdefs" aria-hidden="true" focusable="false"><defs>'
        + rd_glass_defs()
        + '<radialGradient id="drg1" cx="38%" cy="30%" r="78%">'
        '<stop offset="0%" stop-color="#f3d9a4"/><stop offset="45%" stop-color="#c98d4a"/>'
        '<stop offset="100%" stop-color="#3a2415"/></radialGradient>'
        '<radialGradient id="drg2" cx="50%" cy="50%" r="60%">'
        '<stop offset="0%" stop-color="#e8c88e" stop-opacity=".5"/>'
        '<stop offset="100%" stop-color="#e8c88e" stop-opacity="0"/></radialGradient>'
        '<linearGradient id="drg3" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0%" stop-color="#2b3a4e"/><stop offset="100%" stop-color="#141b24"/></linearGradient>'
        '<radialGradient id="rog1" cx="38%" cy="32%" r="72%">'
        '<stop offset="0%" stop-color="#ffe9bb"/><stop offset="45%" stop-color="#d9a253"/>'
        '<stop offset="100%" stop-color="#5a3418"/></radialGradient>'
        '<pattern id="snDots" width="9" height="9" patternUnits="userSpaceOnUse">'
        '<circle cx="2.2" cy="2.2" r="1" fill="#a8916a"/></pattern>'
        '</defs></svg>'
    )


SN_PAPER = "#f2ecdb"
SN_INK = "#1d333e"
SN_MAGENTA = "#ac3a6f"


def catmull(pts, closed=True):
    n = len(pts)
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n]
        p1 = pts[i]
        p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return d + ("Z" if closed else "")


def pip(poly, x, y):
    inside = False
    j = len(poly) - 1
    for i in range(len(poly)):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside


def coast_y(poly, x):
    ys = []
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        if (x1 <= x < x2) or (x2 <= x < x1):
            t = (x - x1) / (x2 - x1)
            ys.append(y1 + (y2 - y1) * t)
    return max(ys) if ys else 0


def sn_land(pts):
    return (
        f'<path d="{catmull(pts)}" fill="#e7dcc0" stroke="{SN_INK}" stroke-width="2.2"/>'
        f'<path d="{catmull([(x, y + 7) for x, y in pts])}" fill="none" stroke="#c9b98f" stroke-width="5" opacity=".55"/>'
    )


def sn_contour(d, label=None, lx=None, ly=None):
    out = f'<path d="{d}" fill="none" stroke="#7d97a0" stroke-width="1.3"/>'
    if label:
        out += (
            f'<rect x="{lx - 13}" y="{ly - 9}" width="26" height="16" fill="{SN_PAPER}"/>'
            f'<text x="{lx}" y="{ly + 3}" text-anchor="middle" font-family="Libre Franklin" '
            f'font-size="11" font-weight="600" fill="#5d7783" letter-spacing=".5">{label}</text>'
        )
    return out


def dry_bank(cx, cy, rx, ry, rot, label, size=10):
    rnd = random.Random(3)
    pts = []
    n = 12
    for i in range(n):
        a = i / n * 2 * math.pi
        r = 1 + rnd.uniform(-.14, .14)
        pts.append((math.cos(a) * rx * r, math.sin(a) * ry * r))
    d = catmull(pts)
    return (
        f'<g transform="translate({cx} {cy}) rotate({rot})">'
        f'<path d="{d}" fill="url(#snDots)" stroke="#b9a273" stroke-width="1.1" stroke-dasharray="5 3"/>'
        f'<path d="{d}" fill="none" stroke="#dccdaa" stroke-width="3" opacity=".55"/>'
        f'<text y="4" text-anchor="middle" font-family="Space Mono, monospace" font-size="{size}" '
        f'letter-spacing="1.6" fill="#8a7443" text-decoration="underline">{label}</text>'
        "</g>"
    )


def sn_rose(cx, cy, r):
    parts = [f'<g transform="translate({cx} {cy})">']
    parts.append(f'<circle r="{r}" fill="none" stroke="{SN_INK}" stroke-width="1.4"/>')
    parts.append(f'<circle r="{r * .78:.0f}" fill="none" stroke="{SN_INK}" stroke-width=".8"/>')
    for a in range(0, 360, 5):
        ln = r * .07 if a % 45 else r * .13
        x1 = math.sin(math.radians(a)) * r
        y1 = -math.cos(math.radians(a)) * r
        x2 = math.sin(math.radians(a)) * (r - ln)
        y2 = -math.cos(math.radians(a)) * (r - ln)
        parts.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{SN_INK}" stroke-width=".8"/>')
    rp = r * .74
    for a in range(0, 360, 45):
        ca, sa = math.sin(math.radians(a)), -math.cos(math.radians(a))
        ca2, sa2 = math.sin(math.radians(a + 90)), -math.cos(math.radians(a + 90))
        tip = (ca * rp, sa * rp)
        side1 = (ca2 * rp * .17, sa2 * rp * .17)
        side2 = (-ca2 * rp * .17, -sa2 * rp * .17)
        parts.append(
            f'<path d="M0,0 L{side1[0]:.1f},{side1[1]:.1f} L{tip[0]:.1f},{tip[1]:.1f} Z" fill="{SN_INK}"/>'
        )
        parts.append(
            f'<path d="M0,0 L{tip[0]:.1f},{tip[1]:.1f} L{side2[0]:.1f},{side2[1]:.1f} Z" fill="{SN_PAPER}" stroke="{SN_INK}" stroke-width=".7"/>'
        )
    for a in range(22, 360, 45):
        ca, sa = math.sin(math.radians(a)), -math.cos(math.radians(a))
        ca2, sa2 = math.sin(math.radians(a + 90)), -math.cos(math.radians(a + 90))
        tip = (ca * rp * .48, sa * rp * .48)
        parts.append(
            f'<path d="M0,0 L{ca2 * rp * .1:.1f},{sa2 * rp * .1:.1f} L{tip[0]:.1f},{tip[1]:.1f} L{-ca2 * rp * .1:.1f},{-sa2 * rp * .1:.1f} Z" fill="{SN_INK}"/>'
        )
    parts.append(f'<circle r="{r * .1:.0f}" fill="{SN_PAPER}" stroke="{SN_INK}" stroke-width=".9"/>')
    parts.append(
        f'<text y="{-rp * .62:.0f}" text-anchor="middle" font-family="Libre Franklin" font-size="{r * .12:.0f}" font-weight="700" fill="{SN_INK}">N</text>'
    )
    parts.append(
        f'<text y="{r * .52:.0f}" text-anchor="middle" font-family="Libre Franklin" font-size="{max(7, r * .085):.0f}" letter-spacing="1" fill="#6d8993">VAR 4&deg;15&#8242;W (2026)</text>'
    )
    parts.append("</g>")
    return "".join(parts)


def sn_soundings(poly, cfg, rnd):
    out = []
    placed = []
    tries = 0
    x0, x1 = cfg["sx"]
    y0, y1 = cfg["sy"]
    while len(placed) < cfg["n"] and tries < cfg["n"] * 90:
        tries += 1
        x = rnd.uniform(x0, x1)
        y = rnd.uniform(y0, y1)
        skip = False
        for r in cfg["excl"]:
            if r[0] <= x <= r[2] and r[1] <= y <= r[3]:
                skip = True
                break
        if skip or pip(poly, x, y):
            continue
        if cfg.get("island") and pip(cfg["island"], x, y):
            continue
        dx, dy = x - cfg["dry"][0], y - cfg["dry"][1]
        if (dx * dx) / (cfg["dry"][2] ** 2) + (dy * dy) / (cfg["dry"][3] ** 2) < 1:
            continue
        for px, py in placed:
            if (px - x) ** 2 + (py - y) ** 2 < cfg["gap"] ** 2:
                skip = True
                break
        if skip:
            continue
        c = coast_y(poly, x)
        depth = (y - c) / cfg["rate"] + rnd.uniform(-2.6, 2.6)
        if y - c < cfg["shore"]:
            continue
        depth = max(1, min(cfg["deep"], round(depth)))
        placed.append((x, y))
        size = 12.5 if depth < 10 else (11.5 if depth < 40 else 10.5)
        out.append(
            f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="middle" font-family="Libre Franklin" '
            f'font-size="{size}" fill="#2b4a56" letter-spacing=".3">{depth}</text>'
        )
    return "".join(out)


SN_D = dict(
    w=1440,
    h=1000,
    land=[
        (-30, -30), (1470, -30), (1470, 150), (1390, 138), (1310, 178), (1234, 158),
        (1160, 238), (1080, 292), (1010, 326), (952, 258), (886, 212), (822, 246),
        (752, 182), (686, 152), (618, 196), (556, 248), (518, 316), (470, 396),
        (428, 364), (382, 296), (330, 238), (256, 198), (178, 228), (100, 186),
        (28, 216), (-30, 196),
    ],
    island=[(700, 556), (734, 536), (764, 552), (772, 588), (742, 612), (706, 600)],
    dry=(560, 500, 104, 46, -14, "DRYING 2 FT"),
    title=(250, 128, 46, 11),
    river="M118,-10 C138,74 188,132 250,196",
    riverw=3,
    lh=[(464, 386), (1006, 318)],
    sx=(40, 1400),
    sy=(330, 950),
    n=105,
    gap=56,
    shore=16,
    rate=9.4,
    deep=87,
    excl=[(24, 656, 448, 972), (1000, 548, 1416, 830), (1120, 74, 1345, 330), (592, 512, 944, 664)],
    rose=(1228, 200, 116),
    contours=[
        ("M-20,432 C 200,412 356,446 470,494 C 602,552 706,486 838,392 C 950,312 1052,344 1180,412 C 1282,462 1382,442 1460,402", "10", 250, 448),
        ("M-20,556 C 240,536 420,576 562,616 C 704,656 862,574 982,494 C 1102,414 1242,456 1460,516", "20", 660, 630),
        ("M-20,724 C 300,714 520,744 700,784 C 900,826 1100,724 1260,662 C 1360,622 1420,642 1460,672", "50", 330, 730),
    ],
)

SN_M = dict(
    w=390,
    h=844,
    land=[
        (-20, -20), (410, -20), (410, 96), (344, 88), (306, 128), (262, 108),
        (222, 168), (182, 148), (150, 190), (112, 162), (80, 202), (42, 184), (-20, 214),
    ],
    island=[(292, 318), (306, 310), (320, 322), (312, 340), (294, 336)],
    dry=(142, 238, 42, 19, -12, "DRYING 2 FT"),
    river="M40,-10 C56,44 82,92 112,146",
    riverw=2,
    lh=[(112, 160), (262, 106)],
    sx=(18, 372),
    sy=(210, 640),
    n=34,
    gap=40,
    shore=10,
    rate=11.5,
    deep=64,
    excl=[(16, 246, 376, 420), (16, 470, 376, 640)],
    contours=[
        ("M-20,236 C 70,228 130,254 190,270 C 262,290 320,258 410,238", "10", 92, 250),
        ("M-20,330 C 80,322 150,352 220,372 C 300,394 340,352 410,340", "20", 246, 378),
        ("M-20,438 C 90,432 160,462 240,486 C 310,506 350,470 410,462", "50", 96, 448),
    ],
)


def sn_base(cfg, mobile=False):
    w, h = cfg["w"], cfg["h"]
    rnd = random.Random(41 if not mobile else 17)
    parts = [f'<svg class="sn-base" viewBox="0 0 {w} {h}" preserveAspectRatio="none" aria-hidden="true">']
    parts.append(f'<rect width="{w}" height="{h}" fill="{SN_PAPER}"/>')
    parts.append('<g stroke="#dcd2b8" stroke-width=".7">')
    for x in range(96, w, 96):
        parts.append(f'<path d="M{x},24 V{h-24}"/>')
    for y in range(96, h, 96):
        parts.append(f'<path d="M24,{y} H{w-24}"/>')
    parts.append("</g>")
    parts.append(f'<rect x="20" y="20" width="{w-40}" height="{h-40}" fill="none" stroke="{SN_INK}" stroke-width="2"/>')
    parts.append(f'<rect x="27" y="27" width="{w-54}" height="{h-54}" fill="none" stroke="{SN_INK}" stroke-width=".7"/>')
    parts.append(sn_land(cfg["land"]))
    parts.append(sn_land(cfg["island"]))
    dx, dy, drx, dry_, rot, dlab = cfg["dry"]
    parts.append(dry_bank(dx, dy, drx, dry_, rot, dlab, 10 if not mobile else 8))
    if cfg.get("river"):
        parts.append(
            f'<path d="{cfg["river"]}" fill="none" stroke="#9db7bf" stroke-width="{cfg["riverw"]}" stroke-linecap="round"/>'
        )
    if cfg.get("title"):
        tx, ty, tsize, ssize = cfg["title"]
        parts.append(
            f'<text x="{tx}" y="{ty}" text-anchor="middle" font-family="Instrument Serif, Georgia, serif" '
            f'font-size="{tsize}" letter-spacing="{tsize * .14:.1f}" fill="#274451" opacity=".92">MUSSEJUSSE</text>'
        )
        parts.append(
            f'<text x="{tx}" y="{ty + ssize * 2.4:.0f}" text-anchor="middle" font-family="Space Mono, monospace" '
            f'font-size="{ssize}" letter-spacing="{ssize * .35:.1f}" fill="#6d8993">PERSONAL WATERS &#183; EST. 2024</text>'
        )
    for d, lab, lx, ly in cfg["contours"]:
        parts.append(sn_contour(d, lab, lx, ly))
    parts.append(sn_soundings(cfg["land"], cfg, rnd))
    if cfg.get("rose"):
        parts.append(sn_rose(*cfg["rose"]))
    for x, y in cfg["lh"]:
        if mobile:
            parts.append(
                f'<g transform="translate({x} {y})">'
                f'<path d="M0,4 L-3,4 L-2,-7 L2,-7 L3,4 Z" fill="#f6f1e2" stroke="{SN_INK}" stroke-width="1"/>'
                f'<circle cy="-9" r="1.8" fill="{SN_MAGENTA}"/></g>'
            )
        else:
            parts.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{SN_MAGENTA}"/>')
    parts.append("</svg>")
    return "".join(parts)


def sn_water(cfg, mobile=False):
    w = cfg["w"]
    edge = []
    x = -20.0
    while x <= w + 20:
        edge.append((x, 5.5 * math.sin(x / 46) + 2.4 * math.sin(x / 17 + 1.2)))
        x += 14
    d = "M" + " L".join(f"{px:.0f},{py:.1f}" for px, py in edge)
    top = 720 if not mobile else 560
    rng = 330 if not mobile else 390
    return (
        f'<svg class="sn-sea" viewBox="0 0 {cfg["w"]} {cfg["h"]}" preserveAspectRatio="none" aria-hidden="true">'
        f'<g class="sn-water" data-base="{top}" data-range="{rng}" style="transform:translateY({top - rng * .52:.0f}px)">'
        f'<path d="{d} L{cfg["w"] + 20},{cfg["h"] + 40} L-20,{cfg["h"] + 40} Z" fill="#8fb4bb" opacity=".3"/>'
        f'<path d="{d}" fill="none" stroke="#e8f2f0" stroke-width="2.6" opacity=".85"/>'
        f'<path d="{d}" fill="none" stroke="#5f8b93" stroke-width="1" opacity=".5" transform="translate(0 7)"/>'
        "</g></svg>"
    )


SN_CSS = """
.sn{background:#f2ecdb;color:#1d333e;font-family:'Libre Franklin',sans-serif;line-height:1.4}
.sn-base,.sn-sea{position:absolute;inset:0;width:100%;height:100%}
.sn-sea{pointer-events:none;z-index:3}
.sn-sea .sn-water{transition:transform 260ms cubic-bezier(.23,1,.32,1)}
.sn-copy{position:absolute;left:41cqw;top:37.4cqw;z-index:6;width:24cqw}
.sn-copy h1{text-shadow:0 0 .6cqw #f2ecdb,0 0 .3cqw #f2ecdb;font-family:'Instrument Serif',Georgia,serif;font-size:2.6cqw;line-height:1.08;font-weight:400}
.sn-copy h1 em{font-style:italic;color:#ac3a6f}
.sn-copy .meta{text-shadow:0 0 .5cqw #f2ecdb,0 0 .25cqw #f2ecdb;margin-top:1.1cqw;font-family:'Space Mono',monospace;font-size:.56cqw;letter-spacing:.24em;text-transform:uppercase;color:#6d8993}
.sn-copy .meta b{font-weight:400;color:#1d333e}
.sn-lh{position:absolute;z-index:7;display:block;outline:none}
.sn-lh .tower{position:relative;display:block}
.sn-lh.lh1{left:30.6cqw;top:21.3cqw;width:3.6cqw;height:6.3cqw}
.sn-lh.lh2{left:68.1cqw;top:15.9cqw;width:3.6cqw;height:6.3cqw}
.sn-lh svg{width:100%;height:100%;overflow:visible}
.sn-lh .lamp{animation:sn-flash 10s linear infinite}
.sn-lh.lh2 .lamp{animation:sn-occ 6s linear infinite}
@keyframes sn-flash{0%,4%{opacity:1}6%,8%{opacity:.1}10%,14%{opacity:1}16%,100%{opacity:.12}}
@keyframes sn-occ{0%,74%{opacity:1}80%,100%{opacity:.12}}
.sn-lh .beam{opacity:0;transition:opacity 320ms ease-out}
.sn-lh:hover .beam,.sn-lh:focus-visible .beam{opacity:.85}
.sn-lh .lab{position:absolute;text-shadow:0 0 .5cqw #f2ecdb,0 0 .25cqw #f2ecdb,0 0 .1cqw #f2ecdb;white-space:nowrap;font-family:'Space Mono',monospace;font-size:.58cqw;letter-spacing:.16em;text-transform:uppercase;color:#ac3a6f;border-bottom:.1cqw solid rgba(172,58,111,.5);padding-bottom:.35cqw;transition:color 200ms ease-out}
.sn-lh .lab b{font-weight:400;color:#1d333e}
.sn-lh.lh1 .lab{right:calc(100% + 1.6cqw);top:46%}
.sn-lh.lh2 .lab{right:calc(100% + 1.6cqw);top:56%;text-align:right}
.sn-lh .lead{position:absolute;height:.1cqw;background:rgba(172,58,111,.5);top:52%}
.sn-lh.lh1 .lead{right:100%;width:1.6cqw}
.sn-lh.lh2 .lead{right:100%;width:1.6cqw}
.sn-card{position:absolute;width:21cqw;background:#faf6ea;border:.12cqw solid #1d333e;box-shadow:.7cqw .9cqw 0 rgba(29,51,62,.14);padding:1.4cqw 1.5cqw;opacity:0;transform:translateY(.7cqw);pointer-events:none;transition:opacity 220ms cubic-bezier(.23,1,.32,1),transform 220ms cubic-bezier(.23,1,.32,1);z-index:9}
.sn-lh:hover .sn-card,.sn-lh:focus-visible .sn-card{opacity:1;transform:translateY(0)}
.sn-lh.lh1 .sn-card{right:2cqw;top:calc(100% + .8cqw)}
.sn-lh.lh2 .sn-card{right:2cqw;top:calc(100% + .8cqw)}
.sn-card .no{font-family:'Space Mono',monospace;font-size:.53cqw;letter-spacing:.26em;text-transform:uppercase;color:#ac3a6f}
.sn-card h2{font-family:'Instrument Serif',Georgia,serif;font-size:1.9cqw;line-height:1;margin-top:.7cqw}
.sn-card p{margin-top:.75cqw;font-size:.92cqw;line-height:1.45;color:#3d5763}
.sn-card .go{margin-top:1cqw;display:flex;align-items:center;gap:.6cqw;font-family:'Space Mono',monospace;font-size:.54cqw;letter-spacing:.22em;text-transform:uppercase;color:#ac3a6f}
.sn-card .go .ar{width:.85cqw;height:.85cqw}
.sn-buoys{position:absolute;left:4.4cqw;bottom:16.4cqw;z-index:7;display:flex;gap:2.2cqw}
.sn-buoy{display:block;text-align:center;transition:transform 240ms cubic-bezier(.23,1,.32,1)}
.sn-buoy svg{width:2.2cqw;height:2.8cqw;margin:0 auto}
.sn-buoy .bl{display:block;margin-top:.5cqw;font-family:'Space Mono',monospace;font-size:.5cqw;letter-spacing:.24em;text-transform:uppercase;color:#6d8993;transition:color 200ms ease-out}
.sn-buoy:hover{transform:translateY(-.4cqw)}
.sn-buoy:hover .bl{color:#ac3a6f}
.sn-cart{position:absolute;left:4.2cqw;top:46.6cqw;z-index:8;width:23.5cqw;background:#faf6ea;border:.12cqw solid #1d333e;box-shadow:.6cqw .8cqw 0 rgba(29,51,62,.12)}
.sn-cart .hd{display:flex;justify-content:space-between;align-items:center;border-bottom:.1cqw solid #1d333e;padding:.9cqw 1.2cqw;font-family:'Space Mono',monospace;font-size:.52cqw;letter-spacing:.22em;text-transform:uppercase}
.sn-cart .hd b{font-weight:400;color:#ac3a6f}
.sn-cart .big{padding:1.2cqw 1.2cqw .6cqw}
.sn-cart .big .nm{font-family:'Instrument Serif',Georgia,serif;font-size:2.5cqw;line-height:1}
.sn-cart .big .sub{margin-top:.45cqw;font-size:.78cqw;letter-spacing:.16em;text-transform:uppercase;color:#6d8993}
.sn-cart .grid{display:grid;grid-template-columns:1fr 1fr;border-top:.1cqw solid #1d333e}
.sn-cart .grid div{padding:.75cqw 1.2cqw;border-right:.08cqw solid rgba(29,51,62,.35);border-bottom:.08cqw solid rgba(29,51,62,.35)}
.sn-cart .grid div:nth-child(2n){border-right:0}
.sn-cart .grid div:nth-last-child(-n+2){border-bottom:0}
.sn-cart .k{display:block;font-family:'Space Mono',monospace;font-size:.48cqw;letter-spacing:.2em;text-transform:uppercase;color:#6d8993}
.sn-cart .v{display:block;margin-top:.3cqw;font-size:.8cqw;font-weight:600}
.sn-notice{position:absolute;right:4.2cqw;top:39.6cqw;z-index:8;width:25cqw;background:#faf6ea;border:.12cqw solid #1d333e;box-shadow:-.6cqw .8cqw 0 rgba(29,51,62,.12)}
.sn-notice .hd{border-bottom:.1cqw solid #1d333e;padding:.9cqw 1.2cqw;display:flex;justify-content:space-between;font-family:'Space Mono',monospace;font-size:.52cqw;letter-spacing:.22em;text-transform:uppercase}
.sn-notice .hd b{font-weight:400;color:#ac3a6f}
.sn-nrow{display:block;padding:1.05cqw 1.2cqw;border-bottom:.08cqw solid rgba(29,51,62,.3);transition:background 200ms ease-out}
.sn-nrow:last-child{border-bottom:0}
.sn-nrow:hover{background:#f1e9d2}
.sn-nrow .l1{display:flex;justify-content:space-between;font-family:'Space Mono',monospace;font-size:.5cqw;letter-spacing:.2em;text-transform:uppercase;color:#6d8993}
.sn-nrow .l1 b{font-weight:400;color:#ac3a6f}
.sn-nrow h3{font-family:'Instrument Serif',Georgia,serif;font-size:1.55cqw;line-height:1;margin-top:.55cqw}
.sn-nrow .l2{margin-top:.5cqw;font-size:.72cqw;letter-spacing:.1em;text-transform:uppercase;color:#3d5763}
.sn-nrow .ct{margin-top:.5cqw;font-family:'Space Mono',monospace;font-size:.5cqw;letter-spacing:.14em;color:#ac3a6f;display:flex;align-items:center;gap:.45cqw}
.sn-nrow .ct .ar{width:.7cqw;height:.7cqw}
.sn-note{padding:1cqw 1.2cqw;font-size:.72cqw;line-height:1.5;color:#6d8993;border-top:.08cqw solid rgba(29,51,62,.3)}
.sn-tide{position:absolute;left:0;right:0;bottom:0;height:8.6cqw;z-index:10;background:#f7f2e3;border-top:.14cqw solid #1d333e;box-shadow:0 -.25cqw 0 rgba(29,51,62,.35)}
.sn-tide .cap{position:absolute;left:2.2cqw;top:1.1cqw;font-family:'Space Mono',monospace;font-size:.5cqw;letter-spacing:.26em;text-transform:uppercase;color:#6d8993}
.sn-tide .cap b{font-weight:400;color:#ac3a6f}
.sn-tide svg.curve{position:absolute;left:1.2cqw;right:13cqw;top:.8cqw;height:5.2cqw;width:calc(100% - 14.2cqw)}
.sn-tide .guide{position:absolute;top:1.4cqw;bottom:1.1cqw;width:.1cqw;background:#ac3a6f;opacity:.55}
.sn-tide .knob{position:absolute;top:1.4cqw;width:1.5cqw;height:1.5cqw;margin-left:-.75cqw;border-radius:50%;background:#f7f2e3;border:.16cqw solid #1d333e;box-shadow:0 .18cqw .35cqw rgba(29,51,62,.35);cursor:grab;touch-action:none;transition:transform 160ms ease-out}
.sn-tide .knob:hover{transform:scale(1.12)}
.sn-tide .knob:active{cursor:grabbing;transform:scale(1.2)}
.sn-tide .knob:before{content:'';position:absolute;inset:.35cqw;border-radius:50%;background:#ac3a6f}
.sn-tide .read{position:absolute;right:2.2cqw;top:1.5cqw;width:12cqw;text-align:right;font-family:'Space Mono',monospace}
.sn-tide .read .t{font-size:.95cqw;letter-spacing:.08em;color:#1d333e}
.sn-tide .read .s{margin-top:.45cqw;font-size:.5cqw;letter-spacing:.22em;text-transform:uppercase;color:#ac3a6f}
.sn-tide .read .h{margin-top:.4cqw;font-size:.5cqw;letter-spacing:.22em;text-transform:uppercase;color:#6d8993}
.sn-tide .ticks{position:absolute;left:1.2cqw;right:13cqw;bottom:1cqw;display:flex;justify-content:space-between;font-family:'Space Mono',monospace;font-size:.46cqw;letter-spacing:.14em;color:#8fa2ab;width:calc(100% - 14.2cqw)}
.sn-plate{position:absolute;left:4.2cqw;bottom:11.6cqw;z-index:7;text-shadow:0 0 .5cqw #f2ecdb,0 0 .25cqw #f2ecdb;font-family:'Space Mono',monospace;font-size:.5cqw;letter-spacing:.2em;text-transform:uppercase;color:#8a7443}
.sn-plate b{font-weight:400;color:#ac3a6f}
.mobile .sn-copy{position:relative;inset:auto;width:auto;margin:0 5cqw;padding-top:0}
.mobile .sn-copy h1{font-size:6.2cqw}
.mobile .sn-copy .meta{margin-top:3cqw;font-size:1.5cqw}
.mobile .sn-cart{position:relative;inset:auto;width:auto;margin:11cqw 5cqw 0}
.mobile .sn-cart .hd{font-size:1.4cqw;padding:2.4cqw 3cqw}
.mobile .sn-cart .big{padding:3cqw 3cqw 1.6cqw}
.mobile .sn-cart .big .nm{font-size:7cqw}
.mobile .sn-cart .big .sub{font-size:2cqw}
.mobile .sn-cart .grid div{padding:2cqw 3cqw}
.mobile .sn-cart .k{font-size:1.3cqw}
.mobile .sn-cart .v{font-size:2.1cqw;margin-top:.9cqw}
.mobile .sn-notice{position:relative;inset:auto;width:auto;margin:7cqw 5cqw 0}
.mobile .sn-notice .hd{font-size:1.4cqw;padding:2.4cqw 3cqw}
.mobile .sn-nrow{padding:3cqw}
.mobile .sn-nrow .l1{font-size:1.35cqw}
.mobile .sn-nrow h3{font-size:4.4cqw;margin-top:1.6cqw}
.mobile .sn-nrow .l2{font-size:1.9cqw;margin-top:1.4cqw}
.mobile .sn-nrow .ct{font-size:1.35cqw;margin-top:1.4cqw;gap:1.2cqw}
.mobile .sn-nrow .ct .ar{width:2cqw;height:2cqw}
.mobile .sn-note{font-size:1.9cqw;padding:2.6cqw 3cqw}
.mobile .sn-buoys{position:relative;inset:auto;margin:8cqw 5cqw 0;gap:6cqw}
.mobile .sn-buoy svg{width:6cqw;height:7.6cqw}
.mobile .sn-buoy .bl{font-size:1.4cqw;margin-top:1.6cqw}
.mobile .sn-plate{position:relative;inset:auto;margin:7cqw 5cqw 0;text-align:center;font-size:1.4cqw}
.mobile .sn-tide{position:relative;margin-top:8cqw}
.mobile .sn-hide{display:none}
.sn-cart,.sn-notice,.sn-copy,.sn-tide,.sn-buoys,.sn-plate{position:absolute}
.mobile .sn-cart,.mobile .sn-notice,.mobile .sn-copy,.mobile .sn-buoys,.mobile .sn-plate{position:relative}
.mobile .sn-lh{display:none}
.mobile .sn-mhead{display:none}
.mobile .sn-copy{padding-top:8cqw}
.sn-mhead{display:none}
"""


def sn_tide_curve(cfg, mobile=False):
    w = 1320 if not mobile else 330
    h = 110 if not mobile else 96

    def level(t):
        return 0.5 + 0.30 * math.sin(2 * math.pi * t) + 0.11 * math.sin(4 * math.pi * t + 0.9)

    d = ""
    for i in range(0, 241):
        t = i / 240
        x = t * w
        y = h - 12 - level(t) * (h - 26)
        d += ("M" if i == 0 else " L") + f"{x:.1f},{y:.1f}"
    return (
        f'<svg class="curve" viewBox="0 0 {w} {h}" preserveAspectRatio="none" aria-hidden="true">'
        f'<path d="{d} L{w},{h} L0,{h} Z" fill="#8fb4bb" opacity=".2"/>'
        f'<path d="{d}" fill="none" stroke="#1d333e" stroke-width="1.8"/>'
        f'<line x1="0" y1="{h - 12 - .5 * (h - 26):.1f}" x2="{w}" y2="{h - 12 - .5 * (h - 26):.1f}" stroke="#ac3a6f" stroke-width=".9" stroke-dasharray="5 4" opacity=".7"/>'
        "</svg>"
    )


def sn_tower(i):
    green = i == 1
    lamp = "#59d6a0" if green else "#ffe6b0"
    return f"""<svg viewBox="-40 -128 80 142" preserveAspectRatio="xMidYMax meet" aria-hidden="true">
<path d="M0,10 L-10,10 L-6,-70 L6,-70 L10,10 Z" fill="#f6f1e2" stroke="#1d333e" stroke-width="1.6"/>
<path d="M-8.2,-34 L8.2,-34 L8.8,-16 L-8.8,-16 Z" fill="{'#2f6f52' if green else '#ac3a6f'}" opacity=".85"/>
<rect x="-12" y="-80" width="24" height="9" fill="#1d333e"/>
<rect x="-8" y="-106" width="16" height="26" fill="#f6f1e2" stroke="#1d333e" stroke-width="1.4"/>
<line x1="-2.7" y1="-104" x2="-2.7" y2="-82" stroke="#1d333e" stroke-width="1"/>
<line x1="2.7" y1="-104" x2="2.7" y2="-82" stroke="#1d333e" stroke-width="1"/>
<path d="M-9,-106 Q0,-120 9,-106 Z" fill="#1d333e"/>
<circle class="lamp" cx="0" cy="-95" r="4.6" fill="{lamp}"/>
<circle cx="0" cy="-95" r="11" fill="{lamp}" opacity=".22"/>
<g class="beam" fill="{lamp}" opacity="0">
<path d="M0,-95 L-165,-124 L-165,-66 Z" opacity=".3"/>
<path d="M0,-95 L165,-124 L165,-66 Z" opacity=".3"/>
</g>
</svg>"""


def sn_body(u):
    buoy = (
        '<svg viewBox="0 0 44 56" aria-hidden="true">'
        '<path d="M10,50 L34,50 L30,16 L14,16 Z" fill="#f6f1e2" stroke="#1d333e" stroke-width="1.6"/>'
        '<rect x="12" y="30" width="20" height="7" fill="#ac3a6f" opacity=".8"/>'
        '<rect x="19" y="6" width="6" height="10" fill="#1d333e"/>'
        '<circle cx="22" cy="4" r="3.4" fill="#ac3a6f"/>'
        '<line x1="8" y1="50" x2="36" y2="50" stroke="#1d333e" stroke-width="2.4"/>'
        "</svg>"
    )
    ticks = "".join(f"<span>{h:02d}:00</span>" for h in range(0, 25, 4))

    return f"""
<div class="site sn {u}">
  <!--d-->{sn_base(SN_D, False)}{sn_water(SN_D, False)}<!--/d-->
  <!--m-->{sn_base(SN_M, True)}{sn_water(SN_M, True)}<!--/m-->
  <div class="sn-copy">
    <h1>Two marks on the chart, both still <em>sounding.</em></h1>
    <div class="meta">Personal chart No. 4 &middot; <b>MusseJusse</b> &middot; corrected to 2026</div>
  </div>
  <a class="sn-lh lh1" href="https://roundest.mussejusse.com" aria-label="Roundest Pok&eacute;mon lighthouse">
    <span class="lead" aria-hidden="true"></span>
    <span class="lab"><b>Roundest Pok&eacute;mon</b> &middot; Fl(2)W 10s &middot; 61m &middot; 24M</span>
    <span class="tower">{sn_tower(0)}</span>
    <span class="sn-card">
      <span class="no">Lighthouse No. 1 &middot; Next.js 16</span>
      <h2>Roundest Pok&eacute;mon</h2>
      <p>Which one is rounder? The comparison runs on server actions and keeps its answer in a cache, so the light does not have to think twice.</p>
      <span class="go">Open the chart {ARROW}</span>
    </span>
  </a>
  <a class="sn-lh lh2" href="https://models.mussejusse.com" aria-label="Models lighthouse">
    <span class="lead" aria-hidden="true"></span>
    <span class="lab"><b>Models</b> &middot; Oc G 6s &middot; 43m &middot; 18M</span>
    <span class="tower">{sn_tower(1)}</span>
    <span class="sn-card">
      <span class="no">Lighthouse No. 2 &middot; Astro</span>
      <h2>Models</h2>
      <p>A catalogue of models and providers, drawn from models.dev. Static pages, so every bearing is quick to take.</p>
      <span class="go">Open the chart {ARROW}</span>
    </span>
  </a>
  <div class="sn-cart">
    <div class="hd"><span>Personal chart No. 4</span><b>MusseJusse</b></div>
    <div class="big">
      <div class="nm">The internet, sounded</div>
      <div class="sub">North Atlantic of the browser</div>
    </div>
    <div class="grid">
      <div><span class="k">Scale</span><span class="v">1 : &#8734;</span></div>
      <div><span class="k">Edition</span><span class="v">4, 2026</span></div>
      <div><span class="k">Soundings in</span><span class="v">Fathoms</span></div>
      <div><span class="k">Sources</span><span class="v">Astro &middot; models.dev</span></div>
    </div>
  </div>
  <div class="sn-notice">
    <div class="hd"><span>Notice to mariners No. 4/26</span><b>2 entries</b></div>
    <a class="sn-nrow" href="https://roundest.mussejusse.com">
      <span class="l1"><span>Chart 2143 &middot; Next.js 16</span><b>MJ-001</b></span>
      <h3>Roundest Pok&eacute;mon</h3>
      <span class="l2">Cache components &middot; server actions &middot; KV store</span>
      <span class="ct">Sail to roundest.mussejusse.com {ARROW}</span>
    </a>
    <a class="sn-nrow" href="https://models.mussejusse.com">
      <span class="l1"><span>Chart 2144 &middot; Astro</span><b>MJ-002</b></span>
      <h3>Models</h3>
      <span class="l2">A models.dev implementation, kept light</span>
      <span class="ct">Sail to models.mussejusse.com {ARROW}</span>
    </a>
    <div class="sn-note">Corrections outstanding: none. The web moves; the chart lags a little, as charts do.</div>
  </div>
  <div class="sn-buoys">
    <a class="sn-buoy" href="https://bsky.app/profile/mussejusse.com">{buoy}<span class="bl">Bluesky</span></a>
    <a class="sn-buoy" href="https://github.com/MusseJusse">{buoy}<span class="bl">GitHub</span></a>
    <a class="sn-buoy" href="https://vercel.com">{buoy}<span class="bl">Vercel</span></a>
  </div>
  <div class="sn-plate">Sounded between <b>2024</b> and now &middot; every depth taken by hand</div>
  <div class="sn-tide">
    <span class="cap">Tide &middot; <b>drag to sound the water</b></span>
    <!--d-->{sn_tide_curve(SN_D, False)}<!--/d-->
    <!--m-->{sn_tide_curve(SN_M, True)}<!--/m-->
    <span class="guide" data-sn-guide style="left:4%;"></span>
    <button class="knob" type="button" role="slider" data-sn-knob aria-label="Tide time" aria-valuemin="0" aria-valuemax="24" aria-valuenow="12" aria-valuetext="12:00, mid tide" style="left:4%;"></button>
    <div class="read">
      <div class="t" data-sn-time>12:00</div>
      <div class="s" data-sn-state>Tide &middot; falling</div>
      <div class="h" data-sn-height>3.6 ft</div>
    </div>
    <div class="ticks">{ticks}</div>
  </div>
</div>"""


# ---------------------------------------------------------------------------
# D / Radiant
# ---------------------------------------------------------------------------

RD_GLASS = {
    "cobalt": ("#3f68cf", "#152e63"),
    "deep": ("#2a4a9e", "#101f4a"),
    "ruby": ("#c8402f", "#6d1420"),
    "garnet": ("#96303c", "#45101a"),
    "amber": ("#eec05a", "#9c5c14"),
    "gold": ("#f4d98b", "#a8791c"),
    "emerald": ("#3d9a6c", "#14503a"),
    "teal": ("#2f8f96", "#123f47"),
}


def rd_glass_defs():
    out = []
    for name, (a, b) in RD_GLASS.items():
        out.append(
            f'<linearGradient id="rdg-{name}" x1="0" y1="0" x2=".85" y2="1">'
            f'<stop offset="0%" stop-color="{a}"/><stop offset="100%" stop-color="{b}"/></linearGradient>'
        )
    out.append(
        '<radialGradient id="rdg-bloom" cx="50%" cy="50%" r="50%">'
        '<stop offset="0%" stop-color="#ffe6b0" stop-opacity=".95"/>'
        '<stop offset="60%" stop-color="#ffc46a" stop-opacity=".35"/>'
        '<stop offset="100%" stop-color="#ffc46a" stop-opacity="0"/></radialGradient>'
    )
    return "".join(out)


def rd_leaf(size=1.0, fill="cobalt", boss="gold"):
    return (
        f'<path d="M0,-218 C 34,-186 37,-112 0,-78 C -37,-112 -34,-186 0,-218 Z" '
        f'fill="url(#rdg-{fill})" stroke="#101114" stroke-width="4.6"/>'
        f'<path d="M0,-206 C 26,-180 28,-116 0,-90 C -28,-116 -26,-180 0,-206 Z" '
        f'fill="none" stroke="#ffffff" stroke-opacity=".22" stroke-width="2"/>'
        f'<circle cy="-148" r="13" fill="url(#rdg-{boss})" stroke="#101114" stroke-width="3.4"/>'
    )


def rd_rose():
    petals = ["cobalt", "amber", "ruby", "emerald", "deep", "gold", "teal", "ruby", "cobalt", "gold", "emerald", "amber"]
    bosses = ["gold", "cobalt", "amber", "ruby", "gold", "emerald", "amber", "cobalt", "ruby", "emerald", "gold", "teal"]
    parts = [f'<svg class="rd-rose" viewBox="-320 -320 640 640" aria-hidden="true">']
    parts.append('<circle r="302" fill="#22262e" stroke="#0b0c0f" stroke-width="8"/>')
    parts.append('<circle r="258" fill="none" stroke="#0b0c0f" stroke-width="10"/>')
    parts.append('<circle r="246" fill="none" stroke="#3a4049" stroke-width="3"/>')
    for k in range(24):
        a = k * 15
        parts.append(f'<circle cx="0" cy="-272" r="13" fill="#0b0c0f" transform="rotate({a})"/>')
        parts.append(f'<circle cx="0" cy="-272" r="9" fill="#181b21" transform="rotate({a})"/>')
    for k in range(12):
        a = k * 30
        parts.append(f'<g transform="rotate({a})">{rd_leaf(1.0, petals[k], bosses[k])}</g>')
    for k in range(12):
        a = k * 30 + 15
        fill = "amber" if k % 2 == 0 else "gold"
        parts.append(
            f'<g transform="rotate({a}) translate(0,-206)">'
            f'<path d="M0,-52 C 17,-24 18,20 0,44 C -18,20 -17,-24 0,-52 Z" fill="url(#rdg-{fill})" stroke="#101114" stroke-width="3.6"/>'
            f'<circle cy="56" r="9" fill="url(#rdg-deep)" stroke="#101114" stroke-width="3"/>'
            "</g>"
        )
    parts.append('<circle r="106" fill="#22262e" stroke="#0b0c0f" stroke-width="7"/>')
    parts.append('<circle r="92" fill="#0d0e11" stroke="#3a4049" stroke-width="2.4"/>')
    parts.append('<circle r="80" fill="url(#rdg-deep)" stroke="#101114" stroke-width="4.4"/>')
    for k in range(8):
        a = k * 45
        parts.append(
            f'<g transform="rotate({a})">'
            f'<path d="M0,-76 C 17,-54 18,-26 0,-12 C -18,-26 -17,-54 0,-76 Z" fill="url(#rdg-gold)" stroke="#101114" stroke-width="3.2"/>'
            "</g>"
        )
    parts.append('<circle r="25" fill="url(#rdg-amber)" stroke="#101114" stroke-width="3.6"/>')
    parts.append('<circle r="25" fill="url(#rdg-bloom)" opacity=".55"/>')
    parts.append('<circle r="302" fill="url(#rdg-bloom)" opacity=".22"/>')
    parts.append("</svg>")
    return "".join(parts)


def rd_lancet(variant):
    a, b, c = (
        ("cobalt", "amber", "ruby") if variant == 0 else ("emerald", "gold", "teal")
    )
    motif = (
        """<g transform="translate(125 300)">
        <circle r="34" fill="url(#rdg-amber)" stroke="#101114" stroke-width="4"/>
        <circle r="34" fill="#fff" opacity=".12"/>
        <circle cx="-9" cy="-10" r="9" fill="#fff6dd" opacity=".65"/>
        <circle r="34" fill="none" stroke="#fff" stroke-opacity=".25" stroke-width="2"/>
        </g>"""
        if variant == 0
        else """<g transform="translate(125 300)">
        <rect x="-34" y="-34" width="68" height="68" fill="url(#rdg-teal)" stroke="#101114" stroke-width="4"/>
        <g stroke="#0d2f36" stroke-width="2.2" opacity=".8">
        <line x1="-34" y1="-11" x2="34" y2="-11"/><line x1="-34" y1="11" x2="34" y2="11"/>
        <line x1="-11" y1="-34" x2="-11" y2="34"/><line x1="11" y1="-34" x2="11" y2="34"/></g>
        <circle cx="11" cy="-11" r="5" fill="#f4d98b"/>
        </g>"""
    )
    name_lines = ["ROUNDEST", "POK&Eacute;MON"] if variant == 0 else ["MODELS"]
    verse_lines = (
        ["which of these is roundest,", "ask the cache"] if variant == 0 else ["every model, laid out", "like a window"]
    )
    if len(name_lines) == 2:
        name_svg = (
            f'<text x="125" y="362" text-anchor="middle" font-family="Cormorant Garamond, Georgia, serif" font-size="28" '
            f'letter-spacing="2" fill="#f6efdc" stroke="#101114" stroke-width="3.2" paint-order="stroke" font-weight="600">{name_lines[0]}</text>'
            f'<text x="125" y="392" text-anchor="middle" font-family="Cormorant Garamond, Georgia, serif" font-size="28" '
            f'letter-spacing="2" fill="#f6efdc" stroke="#101114" stroke-width="3.2" paint-order="stroke" font-weight="600">{name_lines[1]}</text>'
        )
    else:
        name_svg = (
            f'<text x="125" y="380" text-anchor="middle" font-family="Cormorant Garamond, Georgia, serif" font-size="30" '
            f'letter-spacing="3" fill="#f6efdc" stroke="#101114" stroke-width="3.2" paint-order="stroke" font-weight="600">{name_lines[0]}</text>'
        )
    verse_svg = "".join(
        f'<text x="125" y="{418 + i * 17}" text-anchor="middle" font-family="Cormorant Garamond, Georgia, serif" '
        f'font-style="italic" font-size="15" fill="#e8dfc4" stroke="#101114" stroke-width="2.6" paint-order="stroke">{line}</text>'
        for i, line in enumerate(verse_lines)
    )
    return f"""<svg viewBox="0 0 250 470" aria-hidden="true">
<path d="M6,464 L6,152 Q6,36 125,6 Q244,36 244,152 L244,464 Z" fill="#22262e" stroke="#0b0c0f" stroke-width="8"/>
<path d="M18,456 L18,152 Q18,48 125,20 Q232,48 232,152 L232,456 Z" fill="#0d0e11" stroke="#3a4049" stroke-width="2.4"/>
<path d="M26,448 L26,152 Q26,58 125,30 Q224,58 224,152 L224,448 Z" fill="url(#rdg-{a})"/>
<g stroke="#101114" stroke-width="4">
<line x1="26" y1="140" x2="224" y2="140"/><line x1="26" y1="210" x2="224" y2="210"/>
<line x1="26" y1="370" x2="224" y2="370"/>
<line x1="65" y1="140" x2="65" y2="448"/><line x1="125" y1="40" x2="125" y2="448"/><line x1="185" y1="140" x2="185" y2="448"/>
</g>
<path d="M26,140 L224,140 L224,210 L26,210 Z" fill="url(#rdg-{c})" opacity=".5"/>
<path d="M26,370 L224,370 L224,448 L26,448 Z" fill="url(#rdg-{b})" opacity=".35"/>
<g stroke="#101114" stroke-width="3">
<circle cx="125" cy="122" r="26" fill="url(#rdg-{b})"/>
<circle cx="64" cy="112" r="18" fill="url(#rdg-{c})"/>
<circle cx="186" cy="112" r="18" fill="url(#rdg-{b})"/>
</g>
{motif}
{name_svg}
{verse_svg}
</svg>"""


RD_CSS = """
.rd{background:
 radial-gradient(60cqw 55cqw at 50% 34%,rgba(255,214,150,.16),rgba(255,214,150,0) 62%),
 linear-gradient(#191c22,#12141a 55%,#0d0f13);
 color:#d8cdb6;font-family:'Archivo',sans-serif;line-height:1.4;--sun:.5;--noon:1}
.rd:before{content:'';position:absolute;inset:0;pointer-events:none;z-index:1;opacity:.5;mix-blend-mode:overlay;
 background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.7' numOctaves='3'/%3E%3C/filter%3E%3Crect width='160' height='160' filter='url(%23n)' opacity='.6'/%3E%3C/svg%3E")}
.rd:after{content:'';position:absolute;inset:0;pointer-events:none;z-index:2;opacity:.5;
 background:
 repeating-linear-gradient(0deg,rgba(0,0,0,.34) 0 1px,rgba(0,0,0,0) 1px 46px),
 repeating-linear-gradient(90deg,rgba(255,255,255,.028) 0 1px,rgba(255,255,255,0) 1px 120px)}
.rd-lintel{position:absolute;left:0;right:0;top:2.6cqw;text-align:center;z-index:6}
.rd-lintel .nm{font-family:'Cormorant Garamond',Georgia,serif;font-weight:300;font-size:3cqw;letter-spacing:.22em;color:#cbbc9e;text-shadow:.08cqw .08cqw 0 rgba(0,0,0,.8),-.06cqw -.06cqw 0 rgba(255,255,255,.07)}
.rd-lintel .sub{margin-top:.6cqw;font-family:'Space Mono',monospace;font-size:.54cqw;letter-spacing:.34em;text-transform:uppercase;color:#847a6a}
.rd-bloom{position:absolute;left:50%;top:22cqw;width:40cqw;height:40cqw;transform:translate(-50%,-50%);z-index:0;
 background:radial-gradient(circle,rgba(255,224,160,.5),rgba(255,190,110,.16) 42%,rgba(255,190,110,0) 68%);
 opacity:calc(.35 + var(--noon) * .65);transition:opacity 300ms ease-out,transform 400ms cubic-bezier(.23,1,.32,1)}
.rd-rose{position:absolute;left:50%;top:24cqw;width:34cqw;height:34cqw;transform:translate(-50%,-50%);z-index:3;
 filter:saturate(calc(.85 + var(--noon) * .25));transition:filter 400ms ease-out}
.rd-shield{position:absolute;left:0;right:0;top:0;bottom:0;pointer-events:none;z-index:4}
.rd-shield i{position:absolute;left:50%;top:24cqw;width:34cqw;height:34cqw;transform:translate(-50%,-50%) skewX(calc((var(--sun) - .5) * -30deg));opacity:calc((1 - var(--noon)) * .3);
 background:linear-gradient(160deg,rgba(255,150,90,.5),rgba(255,150,90,0) 60%);mix-blend-mode:screen;transition:opacity 300ms ease-out,transform 400ms cubic-bezier(.23,1,.32,1)}
.rd-lancets{position:absolute;left:0;right:0;top:42.4cqw;z-index:5;display:flex;justify-content:center;gap:7cqw}
.rd-lan{position:relative;display:block;width:12.6cqw;transition:filter 320ms ease-out,opacity 320ms ease-out}
.rd-lan svg{width:100%;height:auto;filter:drop-shadow(0 .8cqw 1.6cqw rgba(0,0,0,.55))}
.rd-lancets:hover .rd-lan{opacity:.52}
.rd-lancets .rd-lan:hover,.rd-lancets .rd-lan:focus-visible{opacity:1;filter:brightness(1.22) saturate(1.08)}
.rd-lan .go{position:absolute;left:50%;bottom:-2.4cqw;transform:translateX(-50%);display:flex;align-items:center;gap:.55cqw;font-family:'Space Mono',monospace;font-size:.52cqw;letter-spacing:.26em;text-transform:uppercase;color:#c8b98f;opacity:0;transition:opacity 240ms ease-out}
.rd-lan .go .ar{width:.8cqw;height:.8cqw}
.rd-lan:hover .go,.rd-lan:focus-visible .go{opacity:1}
.rd-floor{position:absolute;left:0;right:0;bottom:0;height:13cqw;z-index:4;background:linear-gradient(rgba(10,11,14,0),rgba(9,10,13,.92) 40%);pointer-events:none}
.rd-pool{position:absolute;bottom:-4cqw;width:24cqw;height:10cqw;border-radius:50%;filter:blur(30px);mix-blend-mode:screen;opacity:.5;
 transition:transform 420ms cubic-bezier(.23,1,.32,1),opacity 360ms ease-out}
.rd-pool.p1{left:22cqw;background:#3a63c8}
.rd-pool.p2{left:40cqw;width:19cqw;background:#e9b64c}
.rd-pool.p3{left:54cqw;background:#3d9a6c}
.rd-pool.p4{right:12cqw;width:17cqw;background:#c8402f}
.rd-sill{position:absolute;right:4.4cqw;bottom:1.6cqw;z-index:7;display:flex;gap:2.2cqw}
.rd-quarry{display:block;width:7.6cqw;height:2.9cqw;background:#1b1e24;border:.1cqw solid #3a4049;transform:skewX(-12deg);position:relative;transition:background 220ms ease-out,transform 260ms cubic-bezier(.23,1,.32,1)}
.rd-quarry span{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;transform:skewX(12deg);font-family:'Space Mono',monospace;font-size:.5cqw;letter-spacing:.22em;text-transform:uppercase;color:#a99a7d}
.rd-quarry:after{content:'';position:absolute;inset:.35cqw;background:linear-gradient(120deg,rgba(90,140,255,.4),rgba(90,140,255,0) 55%);opacity:0;transition:opacity 220ms ease-out}
.rd-quarry:hover{transform:skewX(-12deg) translateY(-.3cqw)}
.rd-quarry:hover:after{opacity:1}
.rd-plaque{position:absolute;left:4.4cqw;bottom:1.6cqw;z-index:7;background:linear-gradient(#8a6f3a,#5f4a24);border:.1cqw solid #2c2210;box-shadow:inset 0 .12cqw 0 rgba(255,235,170,.4),0 .5cqw 1cqw rgba(0,0,0,.5);padding:.7cqw 1.5cqw;text-align:left}
.rd-plaque .a{font-family:'Cormorant Garamond',Georgia,serif;font-size:.86cqw;letter-spacing:.2em;color:#2a2110;text-transform:uppercase}
.rd-plaque .b{margin-top:.25cqw;font-family:'Space Mono',monospace;font-size:.46cqw;letter-spacing:.26em;text-transform:uppercase;color:#3d3016}
.rd-sun{position:absolute;right:4.4cqw;top:5cqw;z-index:9;width:24cqw}
.rd-sun .hd{display:flex;justify-content:space-between;font-family:'Space Mono',monospace;font-size:.52cqw;letter-spacing:.24em;text-transform:uppercase;color:#847a6a}
.rd-sun .rail{position:relative;margin-top:1.4cqw;height:2.6cqw;cursor:grab;touch-action:none}
.rd-sun .rail:active{cursor:grabbing}
.rd-sun .rail:before{content:'';position:absolute;left:0;right:0;top:1.1cqw;height:.12cqw;background:linear-gradient(90deg,rgba(200,185,143,.25),#c8b98f 50%,rgba(200,185,143,.25))}
.rd-sun .tick{position:absolute;top:.5cqw;width:.1cqw;height:.8cqw;background:#6c6353}
.rd-sun .knob{position:absolute;top:-.1cqw;left:50%;width:2.8cqw;height:2.8cqw;margin-left:-1.4cqw;border-radius:50%;
 background:radial-gradient(circle at 38% 34%,#ffedc4,#e9b64c 58%,#a8791c);box-shadow:0 0 2.2cqw rgba(255,205,120,.55),0 .2cqw .4cqw rgba(0,0,0,.5);
 transition:box-shadow 200ms ease-out}
.rd-sun .rail:hover .knob{box-shadow:0 0 3cqw rgba(255,205,120,.8),0 .2cqw .4cqw rgba(0,0,0,.5)}
.rd-motes{position:absolute;inset:0;z-index:5;pointer-events:none}
.rd-motes i{position:absolute;width:.3cqw;height:.3cqw;border-radius:50%;background:#ffe9bb;opacity:.28;animation:rd-drift 12s linear infinite}
@keyframes rd-drift{0%{transform:translate(0,0)}100%{transform:translate(2.6cqw,6cqw)}}
.rd-note{position:absolute;left:4.4cqw;top:5cqw;z-index:8;font-family:'Space Mono',monospace;font-size:.54cqw;letter-spacing:.22em;text-transform:uppercase;color:#847a6a;line-height:2.1}
.rd-note b{font-weight:400;color:#c8b98f}
.rd-foot-m{display:none}
.mobile .rd-lintel{position:relative;inset:auto;padding:9cqw 5cqw 0}
.mobile .rd-lintel .nm{font-size:9.5cqw}
.mobile .rd-lintel .sub{margin-top:2cqw;font-size:1.4cqw}
.mobile .rd-rose{position:relative;left:auto;top:auto;margin:5cqw auto 0;width:52cqw;height:52cqw;transform:none}
.mobile .rd-bloom{position:absolute;left:50%;top:30cqw;width:80cqw;height:80cqw}
.mobile .rd-shield i{left:50%;top:30cqw;width:80cqw;height:80cqw}
.mobile .rd-lancets{position:relative;inset:auto;display:grid;grid-template-columns:1fr 1fr;gap:4cqw;padding:0 5cqw;margin-top:5cqw}
.mobile .rd-lan{width:auto;margin:0}
.mobile .rd-lan .go{position:static;transform:none;justify-content:center;margin-top:1.6cqw;font-size:1.4cqw;gap:1cqw;opacity:1}
.mobile .rd-lan .go .ar{width:2cqw;height:2cqw}
.mobile .rd-lancets:hover .rd-lan{opacity:1}
.mobile .rd-sun{position:relative;inset:auto;width:auto;margin:6cqw 5cqw 0}
.mobile .rd-sun .hd{font-size:1.4cqw}
.mobile .rd-sun .rail{margin-top:2.4cqw;height:6cqw}
.mobile .rd-sun .rail:before{top:2.6cqw;height:.3cqw}
.mobile .rd-sun .tick{top:1.5cqw;height:2.2cqw;width:.25cqw}
.mobile .rd-sun .knob{width:5.4cqw;height:5.4cqw;margin-left:-2.7cqw;top:.3cqw}
.mobile .rd-sill{position:relative;inset:auto;margin:6cqw 5cqw 0;display:grid;grid-template-columns:1fr 1fr 1fr;gap:2.4cqw}
.mobile .rd-quarry{width:auto;height:8.6cqw;border-width:.25cqw}
.mobile .rd-quarry span{font-size:1.4cqw}
.mobile .rd-quarry:after{inset:.8cqw}
.mobile .rd-plaque{display:none}
.mobile .rd-floor{height:20cqw}
.mobile .rd-pool{filter:blur(24px)}
.mobile .rd-pool.p1{left:-8cqw;width:44cqw}
.mobile .rd-pool.p2{left:34cqw;width:36cqw}
.mobile .rd-pool.p3{left:66cqw;width:40cqw}
.mobile .rd-pool.p4{display:none}
.mobile .rd-note{display:none}
.mobile .rd-motes{display:none}
.mobile .rd-foot-m{display:none}
.rd-motes i:nth-child(1){left:34%;top:34%}.rd-motes i:nth-child(2){left:41%;top:32%;animation-delay:-2s}
.rd-motes i:nth-child(3){left:47%;top:35%;animation-delay:-4s}.rd-motes i:nth-child(4){left:55%;top:33%;animation-delay:-6s}
.rd-motes i:nth-child(5){left:62%;top:35%;animation-delay:-8s}.rd-motes i:nth-child(6){left:38%;top:41%;animation-delay:-3s}
.rd-motes i:nth-child(7){left:52%;top:42%;animation-delay:-7s}.rd-motes i:nth-child(8){left:60%;top:40%;animation-delay:-1s}
.rd-motes i:nth-child(9){left:44%;top:46%;animation-delay:-5s}.rd-motes i:nth-child(10){left:57%;top:47%;animation-delay:-9s}
"""


def rd_body(u):
    motes = "".join("<i></i>" for _ in range(10))
    return f"""
<div class="site rd {u}">
  <span class="rd-bloom" aria-hidden="true"></span>
  <span class="rd-shield" aria-hidden="true"><i></i></span>
  <div class="rd-lintel">
    <div class="nm">MUSSEJUSSE</div>
    <div class="sub">Window made 2024 &middot; reglazed daily</div>
  </div>
  <span class="rd-motes" aria-hidden="true">{motes}</span>
  <div class="rd-note">Glass cut by hand<br>light from the browser<br><b>Lat 56&deg;N</b></div>
  <div class="rd-sun">
    <div class="hd"><span>Matins</span><span>Noon</span><span>Vespers</span></div>
    <div class="rail" data-rd-rail role="slider" tabindex="0" aria-label="Sun position" aria-valuemin="0" aria-valuemax="100" aria-valuenow="62">
      <span class="tick" style="left:0"></span>
      <span class="tick" style="left:25%"></span>
      <span class="tick" style="left:50%"></span>
      <span class="tick" style="left:75%"></span>
      <span class="tick" style="left:calc(100% - .1cqw)"></span>
      <span class="knob" data-rd-knob style="left:50%"></span>
    </div>
  </div>
  {rd_rose()}
  <div class="rd-lancets">
    <a class="rd-lan" href="https://roundest.mussejusse.com" aria-label="Roundest Pok&eacute;mon">
      {rd_lancet(0)}
      <span class="go">Enter {ARROW}</span>
    </a>
    <a class="rd-lan" href="https://models.mussejusse.com" aria-label="Models">
      {rd_lancet(1)}
      <span class="go">Enter {ARROW}</span>
    </a>
  </div>
  <div class="rd-sill">
    <a class="rd-quarry" href="https://bsky.app/profile/mussejusse.com"><span>Bluesky</span></a>
    <a class="rd-quarry" href="https://github.com/MusseJusse"><span>GitHub</span></a>
    <a class="rd-quarry" href="https://vercel.com"><span>Vercel</span></a>
  </div>
  <div class="rd-plaque">
    <div class="a">Dedicated to the ongoing experiment</div>
    <div class="b">MMXXIV &middot; the maker reglazes it every day</div>
  </div>
  <div class="rd-floor" aria-hidden="true">
    <span class="rd-pool p1"></span><span class="rd-pool p2"></span>
    <span class="rd-pool p3"></span><span class="rd-pool p4"></span>
  </div>
  <div class="rd-foot-m">Mussejusse &middot; reglazed daily</div>
</div>"""


# ---------------------------------------------------------------------------
# E / Reel One
# ---------------------------------------------------------------------------

RO_CSS = """
.ro{background:#0a0908;color:#f2ece1;font-family:'Archivo',sans-serif;line-height:1.45}
.ro-grain{position:absolute;inset:0;z-index:26;pointer-events:none;opacity:.35;mix-blend-mode:overlay;
 background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='170' height='170'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/%3E%3C/filter%3E%3Crect width='170' height='170' filter='url(%23n)' opacity='.6'/%3E%3C/svg%3E")}
.ro-vig{position:absolute;inset:0;z-index:25;pointer-events:none;background:radial-gradient(120% 90% at 50% 42%,rgba(0,0,0,0) 42%,rgba(0,0,0,.55) 100%)}
.ro-bar{position:absolute;left:0;right:0;height:3.4cqw;background:#000;z-index:24}
.ro-bar.t{top:0;border-bottom:1px solid rgba(255,255,255,.08)}
.ro-bar.b{bottom:0;border-top:1px solid rgba(255,255,255,.08)}
.ro-leader{position:absolute;left:50%;top:22cqw;width:34cqw;height:34cqw;margin-left:-17cqw;z-index:20;opacity:0;visibility:hidden;transition:opacity 240ms ease-out}
.js .ro-leader{opacity:1;visibility:visible}
.js .ro-played .ro-leader{opacity:0;visibility:hidden}
.ro-leader svg{width:100%;height:100%}
.ro-leader text{font-family:'Gloock',Georgia,serif;fill:#f2ece1}
.ro-leader .sweep{animation:ro-sweep .82s linear infinite}
@keyframes ro-sweep{to{transform:rotate(360deg)}}
.js .ro-title h1 .in{transform:translateY(114%)}
.js .ro-played .ro-title h1 .in{transform:translateY(0)}
.js .ro-title .pre,.js .ro-title .sub{opacity:0}
.js .ro-feats,.js .ro-billing{opacity:0}
.js .ro-played .ro-feats,.js .ro-played .ro-billing{opacity:1;transition:opacity 500ms ease-out 120ms}
.js .ro-played .ro-title .pre,.js .ro-played .ro-title .sub{opacity:1;transition:opacity 500ms ease-out 200ms}
.ro-title{position:absolute;left:0;right:0;top:15.4cqw;z-index:6;text-align:center}
.ro-title .pre{display:flex;align-items:center;justify-content:center;gap:1.6cqw;font-size:.78cqw;font-weight:700;letter-spacing:.62em;text-transform:uppercase;color:#c9bfae}
.ro-title .pre i{display:block;width:9cqw;height:1px;background:linear-gradient(90deg,rgba(201,191,174,0),#c9bfae)}
.ro-title .pre i:last-child{background:linear-gradient(90deg,#c9bfae,rgba(201,191,174,0))}
.ro-title h1{margin-top:2.6cqw;font-family:'Gloock',Georgia,serif;font-weight:400;font-size:7.6cqw;line-height:.98;letter-spacing:.005em}
.ro-title h1 .ln{display:block;overflow:hidden}
.ro-title h1 .in{display:block;transition:transform 760ms cubic-bezier(.23,1,.32,1)}
.ro-title h1 .ln:nth-child(2) .in{transition-delay:80ms}
.ro-title .sub{margin-top:2.2cqw;font-size:.82cqw;letter-spacing:.42em;text-transform:uppercase;color:#b3a795}
.ro-title .sub b{color:#d23b2f;font-weight:400}
.ro-feats{position:absolute;left:9cqw;right:9cqw;top:42cqw;z-index:6;display:grid;grid-template-columns:1fr 1fr;gap:3cqw}
.ro-feat{display:grid;grid-template-columns:10.6cqw 1fr;gap:2.2cqw;border:1px solid rgba(255,255,255,.16);background:#100e0c;padding:2.2cqw;transition:opacity 260ms ease-out,transform 300ms cubic-bezier(.23,1,.32,1),border-color 260ms ease-out,background 260ms ease-out}
.ro-feats:hover .ro-feat{opacity:.5}
.ro-feats .ro-feat:hover,.ro-feats .ro-feat:focus-visible{opacity:1;transform:translateY(-.4cqw);border-color:rgba(255,255,255,.4);background:#16130f}
.ro-feat .art{position:relative;width:10.6cqw;height:10.6cqw;border:1px solid rgba(255,255,255,.14);background:#0b0a09;overflow:hidden}
.ro-feat .art svg{width:100%;height:100%}
.ro-feat .ring{transform-origin:60px 60px;transition:transform 900ms cubic-bezier(.23,1,.32,1)}
.ro-feat:hover .ring{transform:rotate(48deg)}
.ro-feat .scan{transform:translateY(-60px);transition:transform 900ms cubic-bezier(.23,1,.32,1)}
.ro-feat:hover .scan{transform:translateY(120px)}
.ro-feat .no{display:block;font-family:'Space Mono',monospace;font-size:.5cqw;letter-spacing:.3em;text-transform:uppercase;color:#8d8271}
.ro-feat h3{margin-top:.7cqw;font-family:'Gloock',Georgia,serif;font-weight:400;font-size:2.3cqw;line-height:1}
.ro-feat p{margin-top:.9cqw;font-size:.88cqw;line-height:1.5;color:#b3a795;max-width:26cqw}
.ro-feat .meta{display:block;margin-top:1cqw;font-family:'Space Mono',monospace;font-size:.48cqw;letter-spacing:.2em;text-transform:uppercase;color:#8d8271;line-height:1.9}
.ro-feat .go{margin-top:1.1cqw;display:flex;width:max-content;align-items:center;gap:.55cqw;font-family:'Space Mono',monospace;font-size:.5cqw;letter-spacing:.26em;text-transform:uppercase;color:#e8dfd0;border-bottom:1px solid rgba(232,223,208,.4);padding-bottom:.35cqw;transition:color 200ms ease-out,border-color 200ms ease-out}
.ro-feat:hover .go{color:#d23b2f;border-color:#d23b2f}
.ro-feat .go .ar{width:.75cqw;height:.75cqw}
.ro-billing{position:absolute;left:50%;bottom:5.4cqw;transform:translateX(-50%);z-index:6;width:46cqw;text-align:center;font-size:.64cqw;font-weight:600;letter-spacing:.24em;text-transform:uppercase;line-height:2.2;color:#a89d8b}
.ro-billing b{color:#f2ece1;font-weight:700}
.ro-billing a{border-bottom:1px solid rgba(168,157,139,.5);transition:color 180ms ease-out,border-color 180ms ease-out}
.ro-billing a:hover{color:#d23b2f;border-color:#d23b2f}
.ro-reel{position:absolute;right:4.2cqw;top:4.6cqw;z-index:8;display:flex;align-items:center;gap:.7cqw;font-family:'Space Mono',monospace;font-size:.5cqw;letter-spacing:.28em;text-transform:uppercase;color:#8d8271}
.ro-reel i{width:.55cqw;height:.55cqw;border-radius:50%;background:#d23b2f;animation:ro-blink 9s linear infinite}
@keyframes ro-blink{0%,88%{opacity:.25}90%,94%{opacity:1}96%,100%{opacity:.25}}
.ro-foot{position:absolute;left:4.2cqw;bottom:1.3cqw;z-index:8;font-family:'Space Mono',monospace;font-size:.5cqw;letter-spacing:.26em;text-transform:uppercase;color:#8d8271}
.ro-stub{position:absolute;right:4.2cqw;bottom:4.2cqw;z-index:9;width:16.4cqw;height:5.4cqw;background:#efe6d2;color:#191410;transform:rotate(-2deg);box-shadow:0 1cqw 2cqw rgba(0,0,0,.6);display:grid;grid-template-columns:1fr 4.6cqw;overflow:hidden}
.ro-stub .main{padding:.9cqw 1cqw}
.ro-stub .ad{font-family:'Gloock',Georgia,serif;font-size:1.5cqw;line-height:1;color:#d23b2f}
.ro-stub .no{margin-top:.5cqw;font-family:'Space Mono',monospace;font-size:.46cqw;letter-spacing:.2em;text-transform:uppercase;color:#5c5142}
.ro-stub .end{position:relative;border-left:1px dashed rgba(25,20,16,.5);display:flex;align-items:center;justify-content:center}
.ro-stub .end:before,.ro-stub .end:after{content:'';position:absolute;left:50%;width:1.6cqw;height:.8cqw;background:#0a0908;border-radius:.8cqw;transform:translateX(-50%)}
.ro-stub .end:before{top:-.4cqw}.ro-stub .end:after{bottom:-.4cqw}
.ro-stub .end span{font-family:'Space Mono',monospace;font-size:.5cqw;letter-spacing:.14em;text-transform:uppercase;color:#5c5142;writing-mode:vertical-rl;transform:rotate(180deg)}
.mobile .ro-bar{height:9cqw}
.mobile .ro-title{position:relative;inset:auto;padding:12cqw 5cqw 0}
.mobile .ro-title .pre{font-size:1.8cqw;gap:2.6cqw;letter-spacing:.4em}
.mobile .ro-title .pre i{width:12cqw}
.mobile .ro-title h1{font-size:13cqw;margin-top:4cqw}
.mobile .ro-title .sub{font-size:1.9cqw;margin-top:3.6cqw;letter-spacing:.3em}
.mobile .ro-feats{position:relative;inset:auto;display:block;padding:0}
.mobile .ro-feat{grid-template-columns:24cqw 1fr;gap:3.4cqw;margin:5cqw 5cqw 0;padding:3.4cqw;transition:none}
.mobile .ro-feats:hover .ro-feat{opacity:1}
.mobile .ro-feat .art{width:24cqw;height:24cqw}
.mobile .ro-feat .no{font-size:1.35cqw}
.mobile .ro-feat h3{font-size:5cqw;margin-top:1.4cqw}
.mobile .ro-feat p{font-size:2.4cqw;max-width:none;margin-top:1.8cqw}
.mobile .ro-feat .meta{font-size:1.3cqw;margin-top:1.8cqw}
.mobile .ro-feat .go{font-size:1.45cqw;gap:1.2cqw;margin-top:2.2cqw}
.mobile .ro-feat .go .ar{width:2cqw;height:2cqw}
.mobile .ro-billing{position:relative;inset:auto;transform:none;width:auto;margin:7cqw 5cqw 0;font-size:1.6cqw;line-height:2.3;letter-spacing:.14em}
.mobile .ro-reel{right:5cqw;top:3.4cqw;font-size:1.4cqw;gap:1.6cqw}
.mobile .ro-reel i{width:1.6cqw;height:1.6cqw}
.mobile .ro-foot{position:relative;inset:auto;margin:6cqw 5cqw 0;font-size:1.4cqw;text-align:center}
.mobile .ro-stub{position:relative;inset:auto;margin:5cqw auto 0;transform:rotate(-1.4deg);width:70cqw;height:18cqw;grid-template-columns:1fr 15cqw}
.mobile .ro-stub .main{padding:3cqw 4cqw}
.mobile .ro-stub .ad{font-size:5.4cqw}
.mobile .ro-stub .no{font-size:1.4cqw;margin-top:1.2cqw}
.mobile .ro-stub .end span{font-size:1.5cqw}
.mobile .ro-stub .end:before,.mobile .ro-stub .end:after{width:5cqw;height:2.5cqw;border-radius:2.5cqw}
.mobile .ro-stub .end:before{top:-1.2cqw}.mobile .ro-stub .end:after{bottom:-1.2cqw}
.mobile .ro-leader{top:30cqw;width:54cqw;height:54cqw;margin-left:-27cqw}
.mobile .ro-pad{height:4cqw}
.ro-pad{display:none}
"""


def ro_leader():
    return """<svg viewBox="0 0 400 400" aria-hidden="true">
<circle cx="200" cy="200" r="188" fill="#0a0908" stroke="#f2ece1" stroke-width="1.4"/>
<g fill="#f2ece1" opacity=".14">
<path d="M200,200 L200,12 A188,188 0 0 1 388,200 Z"/>
<path d="M200,200 L200,388 A188,188 0 0 1 12,200 Z"/>
</g>
<g stroke="#f2ece1" stroke-width="1" opacity=".5">
<line x1="200" y1="0" x2="200" y2="400"/><line x1="0" y1="200" x2="400" y2="200"/>
</g>
<g stroke="#f2ece1" stroke-width="1" opacity=".75">
<line x1="200" y1="8" x2="200" y2="26"/><line x1="200" y1="374" x2="200" y2="392"/>
<line x1="8" y1="200" x2="26" y2="200"/><line x1="374" y1="200" x2="392" y2="200"/>
</g>
<g class="sweep" style="transform-origin:200px 200px">
<path d="M200,200 L200,26 A174,174 0 0 1 61,126 Z" fill="#f2ece1" opacity=".1"/>
<line x1="200" y1="200" x2="200" y2="26" stroke="#f2ece1" stroke-width="1.6" opacity=".8"/>
</g>
<circle cx="200" cy="200" r="118" fill="#0a0908" stroke="#f2ece1" stroke-width="1" opacity=".7"/>
<text x="200" y="252" text-anchor="middle" font-size="150" data-ro-number>3</text>
</svg>"""


def ro_feat_art(i):
    if i == 0:
        return """<svg viewBox="0 0 120 120" aria-hidden="true">
<circle cx="60" cy="60" r="30" fill="#1b1712"/>
<circle cx="60" cy="60" r="30" fill="url(#rog1)"/>
<ellipse class="ring" cx="60" cy="60" rx="48" ry="13" fill="none" stroke="#e9b64c" stroke-width="1.4" opacity=".8" transform="rotate(-18 60 60)"/>
<circle cx="60" cy="60" r="4.4" fill="#f6e3b2"/>
<text x="60" y="106" text-anchor="middle" font-family="Space Mono" font-size="8" letter-spacing="2.4" fill="#8d8271">ROUND</text>
</svg>"""
    return """<svg viewBox="0 0 120 120" aria-hidden="true">
<g fill="none" stroke="#5f6f86" stroke-width="1.2">
<rect x="14" y="18" width="20" height="20"/><rect x="40" y="18" width="20" height="20"/><rect x="66" y="18" width="20" height="20"/><rect x="92" y="18" width="20" height="20"/>
<rect x="14" y="44" width="20" height="20"/><rect x="40" y="44" width="20" height="20"/><rect x="66" y="44" width="20" height="20"/><rect x="92" y="44" width="20" height="20"/>
<rect x="14" y="70" width="20" height="20"/><rect x="40" y="70" width="20" height="20"/><rect x="66" y="70" width="20" height="20"/><rect x="92" y="70" width="20" height="20"/>
</g>
<rect x="40" y="44" width="20" height="20" fill="#e9b64c"/>
<rect x="66" y="70" width="20" height="20" fill="#3d9a6c"/>
<rect class="scan" x="10" y="60" width="104" height="2" fill="#f6e3b2" opacity=".85"/>
<text x="60" y="106" text-anchor="middle" font-family="Space Mono" font-size="8" letter-spacing="2.4" fill="#8d8271">CATALOGUE</text>
</svg>"""


def ro_body(u):
    return f"""
<div class="site ro {u}">
  <span class="ro-grain" aria-hidden="true"></span>
  <span class="ro-vig" aria-hidden="true"></span>
  <span class="ro-bar t" aria-hidden="true"></span>
  <span class="ro-bar b" aria-hidden="true"></span>
  <div class="ro-leader">{ro_leader()}</div>
  <div class="ro-reel"><i aria-hidden="true"></i>Reel 1 of 1</div>
  <div class="ro-title">
    <div class="pre"><i></i>Mussejusse presents<i></i></div>
    <h1>
      <span class="ln"><span class="in">A work</span></span>
      <span class="ln"><span class="in">in progress</span></span>
    </h1>
    <div class="sub">A double feature &middot; in two parts &middot; runtime <b>&#8734;</b></div>
  </div>
  <div class="ro-feats">
    <a class="ro-feat" href="https://roundest.mussejusse.com">
      <span class="art" aria-hidden="true">{ro_feat_art(0)}</span>
      <span>
        <span class="no">Feature one &middot; Next.js 16</span>
        <h3>Roundest Pok&eacute;mon</h3>
        <p>In which the question of roundness is settled by server actions and remembered by a cache.</p>
        <span class="meta">Technicolor &middot; cache components &middot; server actions &middot; KV store</span>
        <span class="go">Program notes {ARROW}</span>
      </span>
    </a>
    <a class="ro-feat" href="https://models.mussejusse.com">
      <span class="art" aria-hidden="true">{ro_feat_art(1)}</span>
      <span>
        <span class="no">Feature two &middot; Astro</span>
        <h3>Models</h3>
        <p>A complete catalogue of everything that answers, shot mostly on static paper.</p>
        <span class="meta">Scope &middot; Astro &middot; models.dev &middot; no client code</span>
        <span class="go">Program notes {ARROW}</span>
      </span>
    </a>
  </div>
  <div class="ro-billing">
    <b>Mussejusse</b> presents <b>a work in progress</b> starring <b>Roundest Pok&eacute;mon</b> and <b>Models</b>
    with <a href="https://bsky.app/profile/mussejusse.com">Bluesky</a> &middot; <a href="https://github.com/MusseJusse">GitHub</a> &middot; <a href="https://vercel.com">Vercel</a>
    photographed on the web &middot; edited after dark &middot; titles set in the browser &middot; released MMXXIV &middot; running time without end
  </div>
  <div class="ro-foot">Shot on the web &middot; no projector was harmed</div>
  <div class="ro-stub" aria-hidden="true">
    <div class="main">
      <div class="ad">Admit one</div>
      <div class="no">No. 0004 &middot; Row &#8734; &middot; Seat 03</div>
    </div>
    <div class="end"><span>Mussejusse</span></div>
  </div>
  <div class="ro-pad"></div>
</div>"""


# ---------------------------------------------------------------------------
# scripts
# ---------------------------------------------------------------------------

SCRIPT = """
(function(){
  function each(sel, fn){ Array.prototype.forEach.call(document.querySelectorAll(sel), fn); }

  // E / reel leader
  each('.site.ro', function(root){
    var num = root.querySelector('[data-ro-number]');
    if(!num) return;
    var n = 8;
    var iv = setInterval(function(){
      n -= 1;
      if(n < 2){
        clearInterval(iv);
        root.classList.add('ro-played');
        return;
      }
      num.textContent = n;
    }, 290);
  });

  // B / safelight switch
  each('[data-dr-switch]', function(btn){
    btn.addEventListener('click', function(){
      var site = btn.closest('.site');
      var lit = site.classList.toggle('lit');
      btn.setAttribute('aria-pressed', lit ? 'true' : 'false');
      var on = btn.querySelector('[data-dr-on]');
      if(on) on.textContent = lit ? 'Safelight' : 'Inspection light';
    });
  });

  // B / tray develops its print
  each('[data-dr-tray]', function(tray){
    var site = tray.closest('.site');
    var print = site.querySelector('[data-dr-print="' + tray.getAttribute('data-dr-tray') + '"]');
    if(!print) return;
    function on(){ print.classList.add('dev-on'); }
    function off(){ print.classList.remove('dev-on'); }
    tray.addEventListener('mouseenter', on);
    tray.addEventListener('focus', on);
    tray.addEventListener('mouseleave', off);
    tray.addEventListener('blur', off);
    print.addEventListener('mouseenter', on);
    print.addEventListener('mouseleave', off);
  });
  if('IntersectionObserver' in window){
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if(e.isIntersecting) e.target.classList.add('dev-on');
      });
    }, {threshold:.4});
    each('.site.m .dr-print', function(el){ io.observe(el); });
  }

  // C / tide scrubber
  each('.site.sn', function(site){
    var knob = site.querySelector('[data-sn-knob]');
    var guide = site.querySelector('[data-sn-guide]');
    var water = site.querySelector('.sn-water');
    var tide = site.querySelector('.sn-tide');
    var timeEl = site.querySelector('[data-sn-time]');
    var stateEl = site.querySelector('[data-sn-state]');
    var heightEl = site.querySelector('[data-sn-height]');
    if(!knob || !water || !tide) return;
    var base = parseFloat(water.getAttribute('data-base'));
    var range = parseFloat(water.getAttribute('data-range'));
    function level(t){ return .5 + .3 * Math.sin(2*Math.PI*t) + .11 * Math.sin(4*Math.PI*t + .9); }
    function set(t){
      t = Math.max(0, Math.min(1, t));
      var pct = 4 + t * 92;
      knob.style.left = pct + '%';
      if(guide) guide.style.left = pct + '%';
      water.style.transform = 'translateY(' + (base - range * level(t)).toFixed(1) + 'px)';
      var mins = Math.round(t * 1440);
      var hh = ('0' + Math.floor(mins / 60)).slice(-2);
      var mm = ('0' + (mins % 60)).slice(-2);
      if(timeEl) timeEl.textContent = hh + ':' + mm;
      var rising = level(Math.min(1, t + .008)) > level(t);
      if(stateEl) stateEl.textContent = 'Tide \\u00b7 ' + (rising ? 'rising' : 'falling');
      if(heightEl) heightEl.textContent = (level(t) * 6.2).toFixed(1) + ' ft';
      knob.setAttribute('aria-valuenow', (t * 24).toFixed(1));
      knob.setAttribute('aria-valuetext', hh + ':' + mm + ', tide ' + (rising ? 'rising' : 'falling') + ', ' + (level(t) * 6.2).toFixed(1) + ' feet');
    }
    var drag = false;
    function pos(e){
      var r = tide.getBoundingClientRect();
      return (e.clientX - r.left) / r.width;
    }
    knob.addEventListener('pointerdown', function(e){
      drag = true;
      site.classList.add('sn-drag');
      try { knob.setPointerCapture(e.pointerId); } catch(err){}
      set((pos(e) - .04) / .92);
    });
    knob.addEventListener('pointermove', function(e){ if(drag) set((pos(e) - .04) / .92); });
    knob.addEventListener('pointerup', function(){ drag = false; site.classList.remove('sn-drag'); });
    knob.addEventListener('pointercancel', function(){ drag = false; site.classList.remove('sn-drag'); });
    knob.addEventListener('keydown', function(e){
      var cur = parseFloat(knob.getAttribute('aria-valuenow')) / 24;
      if(e.key === 'ArrowLeft' || e.key === 'ArrowDown'){ set(cur - .02); e.preventDefault(); }
      if(e.key === 'ArrowRight' || e.key === 'ArrowUp'){ set(cur + .02); e.preventDefault(); }
      if(e.key === 'Home'){ set(0); e.preventDefault(); }
      if(e.key === 'End'){ set(1); e.preventDefault(); }
    });
    set(.5);
  });

  // D / sun rail
  each('[data-rd-rail]', function(rail){
    var site = rail.closest('.site');
    var knob = rail.querySelector('[data-rd-knob]');
    if(!site) return;
    function set(v){
      v = Math.max(0, Math.min(1, v));
      site.style.setProperty('--sun', v.toFixed(3));
      site.style.setProperty('--noon', (1 - Math.abs(v - .5) * 2).toFixed(3));
      if(knob) knob.style.left = (v * 100) + '%';
      rail.setAttribute('aria-valuenow', Math.round(v * 100));
    }
    var drag = false;
    function pos(e){
      var r = rail.getBoundingClientRect();
      return (e.clientX - r.left) / r.width;
    }
    rail.addEventListener('pointerdown', function(e){
      drag = true;
      try { rail.setPointerCapture(e.pointerId); } catch(err){}
      set(pos(e));
    });
    rail.addEventListener('pointermove', function(e){ if(drag) set(pos(e)); });
    rail.addEventListener('pointerup', function(){ drag = false; });
    rail.addEventListener('pointercancel', function(){ drag = false; });
    rail.addEventListener('keydown', function(e){
      var cur = parseFloat(rail.getAttribute('aria-valuenow')) / 100;
      if(e.key === 'ArrowLeft' || e.key === 'ArrowDown'){ set(cur - .04); e.preventDefault(); }
      if(e.key === 'ArrowRight' || e.key === 'ArrowUp'){ set(cur + .04); e.preventDefault(); }
    });
    set(.62);
  });
})();
"""

SCRIPT_CSS = """
.sn-drag .sn-sea .sn-water{transition:none}
"""

# ---------------------------------------------------------------------------
# document
# ---------------------------------------------------------------------------

DIRECTIONS = [
    ("A", "Par Avion", "The homepage as airmail. Two stamped envelopes on a desk, a postmark over the name, and letters that slide out when you hover an envelope.", PA_CSS, pa_body),
    ("B", "Darkroom", "The whole page under a safelight. Two prints hang on a wire and develop when you hover their tray; the switch turns on the inspection light.", DR_CSS, dr_body),
    ("C", "Soundings", "A working personal chart. Two lighthouses flash their real characteristics, soundings scatter across the sea, and the tide slider moves water over the whole page.", SN_CSS, sn_body),
    ("D", "Radiant", "A rose window and two lancets. Drag the sun across the rail to change the light; the floor catches colour and the glass answers.", RD_CSS, rd_body),
    ("E", "Reel One", "A double feature. A countdown leader once, then a title card, a billing block and a ticket stub for two projects.", RO_CSS, ro_body),
]


def build():
    sections = []
    site_css = []
    nav = []
    for letter, name, desc, css, body in DIRECTIONS:
        nav.append(f'<a href="#{letter}">{letter}</a>')
        site_css.append(css)
        markup = site_pair(body("{u}"))
        sections.append(
            f'<section class="direction" id="{letter}"><div class="dhead"><span class="letter">{letter}</span>'
            f'<h3>{name}</h3><p>{desc}</p></div><div class="views">{markup}</div></section>'
        )
    html = (
        '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        "<title>MusseJusse / five directions, round four</title>"
        "<script>document.documentElement.className+=' js';</script>"
        f"<style>{FONTS}{SHELL_CSS}{SCRIPT_CSS}{''.join(site_css)}</style></head><body>{gdefs()}"
        '<header class="top"><div class="row"><strong>MusseJusse / five directions, round four</strong>'
        f'<span class="meta">Round four</span><nav class="nav" aria-label="Directions">{"".join(nav)}</nav></div></header>'
        '<main class="wrap"><div class="intro"><span class="k">Five full pages, desktop and mobile</span>'
        "<h2>Same homepage, five new worlds.</h2>"
        "<p>Airmail, a darkroom, a chart, a window, a cinema. Every direction is a working page, not a picture: "
        "hover the envelopes and trays, drag the tide and the sun, let the leader run once. Desktop sits beside mobile on each row, "
        "and each page reads fine with JavaScript off. Pick one whole, or point at the pieces worth merging.</p></div>"
        + "".join(sections)
        + '</main><footer class="wrap foot"><span>MusseJusse, 2026. Mockups only, nothing here ships as drawn.</span>'
        '<span><a href="https://roundest.mussejusse.com">Roundest Pok&eacute;mon</a> &middot; '
        '<a href="https://models.mussejusse.com">Models</a></span></footer>'
        f"<script>{SCRIPT}</script></body></html>"
    )
    out = ROOT / "round-four-directions.html"
    out.write_text(html)
    kb = out.stat().st_size / 1024
    print(f"{out} written, {kb:.1f} KB")


if __name__ == "__main__":
    build()






