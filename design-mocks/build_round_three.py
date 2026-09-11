from pathlib import Path
import random
import re

ROOT = Path(__file__).resolve().parent
FONTS = (ROOT / "round-three-assets" / "fonts.css").read_text()

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
.intro{padding:64px 0 4px;max-width:80ch}
.intro .k{font:400 11px/1 'Space Mono',monospace;letter-spacing:.24em;color:var(--dim);text-transform:uppercase}
.intro h2{font-size:clamp(28px,3.6vw,52px);line-height:1.04;letter-spacing:-.03em;font-weight:600;margin:16px 0 0}
.intro p{color:var(--dim);margin-top:16px;max-width:66ch}
.direction{padding-top:84px;scroll-margin-top:64px}
.dhead{display:grid;grid-template-columns:auto 1fr;gap:6px 26px;align-items:baseline;border-top:1px solid var(--line);padding-top:20px}
.dhead .letter{font:400 12px/1 'Space Mono',monospace;color:var(--dim);letter-spacing:.12em;grid-row:1/span 2;padding-top:6px}
.dhead h3{font-size:clamp(22px,2.6vw,34px);font-weight:600;letter-spacing:-.025em}
.dhead p{color:var(--dim);font-size:14px;max-width:78ch}
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
.site img{display:block;max-width:100%}
.foot{margin-top:96px;border-top:1px solid var(--line);padding-top:20px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px;color:var(--dim);font-size:13px}
.foot a{text-decoration:underline;text-underline-offset:4px}
@media(max-width:1180px){.views{grid-template-columns:1fr}.view.mobile{width:min(100%,390px)}.dhead{grid-template-columns:auto 1fr}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}.site *{animation:none!important;transition:none!important}.site .mr-gate{transform:none!important}}
.site button:focus-visible{outline:2px solid currentColor;outline-offset:3px}
.gdefs{position:absolute;width:0;height:0;overflow:hidden}
"""

# ---------------------------------------------------------------------------
# A / Observatory
# ---------------------------------------------------------------------------

OBS_CSS = """
.obs{background:
 radial-gradient(130cqw 90cqw at 72% 18%,#17204a 0%,rgba(12,17,38,0) 58%),
 radial-gradient(80cqw 70cqw at 6% 100%,#131a3d 0%,rgba(12,17,38,0) 62%),
 linear-gradient(#0a0e20,#05070f);
 color:#efe3c8;font-family:'Cormorant Garamond',Georgia,serif;line-height:1.35}
.obs-stars{position:absolute;inset:0;width:100%;height:100%;opacity:.9}
.obs-stars circle{fill:#e9e7e1}
@keyframes obs-tw{0%,100%{opacity:.2}50%{opacity:1}}
.obs-stars circle{animation:obs-tw 6s ease-in-out infinite alternate}
.obs-stars circle:nth-child(3n){animation-duration:8.4s}
.obs-stars circle:nth-child(3n+1){animation-duration:4.6s}
.obs-mw{position:absolute;left:-10cqw;top:-12cqw;width:120cqw;height:56cqw;transform:rotate(-13deg);
 background:radial-gradient(closest-side,rgba(140,158,214,.14),rgba(140,158,214,.05) 55%,rgba(140,158,214,0));pointer-events:none}
.obs-brand{position:absolute;left:4.6cqw;top:4cqw;z-index:6}
.obs-brand .nm{font-size:3.4cqw;line-height:.96;font-weight:600;letter-spacing:.005em}
.obs-brand .eyebrow{display:block;margin-top:1cqw;font-family:'Space Mono',monospace;font-size:.64cqw;letter-spacing:.34em;color:#d3ac6b;text-transform:uppercase}
.obs-meta{position:absolute;right:4.6cqw;top:4.2cqw;text-align:right;font-family:'Space Mono',monospace;font-size:.64cqw;line-height:2.1;letter-spacing:.18em;color:#8b96be;text-transform:uppercase;z-index:6}
.obs-chart{position:absolute;left:36cqw;top:3.4cqw;width:62cqw;height:62cqw;z-index:2}
.obs-chart svg{width:100%;height:100%;overflow:visible}
.obs-chart text{font-family:'Space Mono',monospace;fill:#8b96be}
.obs-copy{position:absolute;left:4.6cqw;top:23.5cqw;width:31cqw;z-index:6}
.obs-copy h1{font-size:5.6cqw;line-height:.98;font-weight:600;letter-spacing:-.01em}
.obs-copy p{margin-top:1.8cqw;font-size:1.28cqw;line-height:1.5;color:#cdc3a9;max-width:26cqw}
.obs-copy .hint{margin-top:2.6cqw;font-family:'Space Mono',monospace;font-size:.6cqw;letter-spacing:.28em;color:#5f6a94;text-transform:uppercase}
.obs-cond{position:absolute;left:4.6cqw;bottom:3cqw;font-family:'Space Mono',monospace;font-size:.62cqw;letter-spacing:.2em;color:#8b96be;text-transform:uppercase;z-index:6;display:flex;gap:2.6cqw}
.obs-cond i{font-style:normal;color:#efe3c8}
.obs-soc{position:absolute;right:4.6cqw;bottom:3cqw;display:flex;gap:2.2cqw;font-family:'Space Mono',monospace;font-size:.62cqw;letter-spacing:.2em;text-transform:uppercase;z-index:6}
.obs-soc a{color:#8b96be;display:flex;align-items:center;gap:.7cqw;transition:color 200ms ease-out}
.obs-soc a:hover{color:#efe3c8}
.obs-soc svg{width:.9cqw;height:.9cqw;stroke:currentColor;stroke-width:2;fill:none}
.obs-soc svg path{stroke-linecap:round;stroke-linejoin:round}
.obs-hot{position:absolute;z-index:7;display:block;width:11cqw;height:8cqw;margin:-4cqw 0 0 -5.5cqw}
.obs-hot.h1{left:58.15cqw;top:43.7cqw}
.obs-hot.h2{left:79.1cqw;top:25.3cqw}
.mobile .obs-hot{display:none}
.obs-hot .spot{position:absolute;inset:0;border-radius:50%}
.obs-hot .tag{position:absolute;font-family:'Space Mono',monospace;font-size:.64cqw;letter-spacing:.24em;color:#efe3c8;text-transform:uppercase;white-space:nowrap;transition:color 220ms ease-out;top:calc(50% - .35cqw)}
.obs-hot .tag b{color:#d3ac6b;font-weight:400}
.obs-hot .tag:before{content:'';position:absolute;top:50%;height:1px;width:4.2cqw;background:linear-gradient(90deg,rgba(211,172,107,.85),rgba(211,172,107,.15))}
.obs-hot.h1 .tag{left:calc(50% + 6.2cqw)}
.obs-hot.h1 .tag:before{right:calc(100% + 1.4cqw);background:linear-gradient(270deg,rgba(211,172,107,.85),rgba(211,172,107,.15))}
.obs-hot.h2 .tag{right:calc(50% + 6.2cqw);text-align:right}
.obs-hot.h2 .tag:before{left:calc(100% + 1.4cqw)}
.obs-card{position:absolute;width:23cqw;padding:1.5cqw 1.6cqw;background:rgba(10,14,31,.92);border:1px solid rgba(211,172,107,.4);
 box-shadow:0 2.4cqw 5cqw rgba(2,4,12,.7);opacity:0;transform:translateY(.8cqw);pointer-events:none;
 transition:opacity 240ms cubic-bezier(.23,1,.32,1),transform 240ms cubic-bezier(.23,1,.32,1)}
.obs-hot:focus-visible{outline:none}
.obs-hot:focus-visible .tag,.obs-hot:hover .tag{color:#d3ac6b}
.obs-hot:focus-visible .obs-card,.obs-hot:hover .obs-card{opacity:1;transform:translateY(0)}
.obs-card .no{font-family:'Space Mono',monospace;font-size:.56cqw;letter-spacing:.3em;color:#8b96be;text-transform:uppercase}
.obs-card h2{margin-top:.7cqw;font-size:2cqw;line-height:1.05;font-weight:600}
.obs-card p{margin-top:.7cqw;font-size:1.02cqw;line-height:1.45;color:#cdc3a9}
.obs-card .go{margin-top:1.1cqw;font-family:'Space Mono',monospace;font-size:.58cqw;letter-spacing:.24em;color:#d3ac6b;text-transform:uppercase;display:flex;align-items:center;gap:.6cqw}
.obs-card .go svg{width:.85cqw;height:.85cqw;stroke:#d3ac6b;stroke-width:2;fill:none}
.obs-shoot{position:absolute;left:52cqw;top:9cqw;width:14cqw;height:1px;z-index:3;pointer-events:none;
 background:linear-gradient(90deg,rgba(233,231,225,0),rgba(233,231,225,.95));transform:rotate(24deg);opacity:0}
@keyframes obs-shoot{0%{opacity:0;transform:rotate(24deg) translateX(0)}6%{opacity:1}22%{opacity:0;transform:rotate(24deg) translateX(-26cqw)}100%{opacity:0;transform:rotate(24deg) translateX(-26cqw)}}
.obs-shoot{animation:obs-shoot 9s ease-in 2.2s infinite}
.obs-rows{display:none}
.obs-mchart{display:none}
.mobile .obs-brand{left:6cqw;top:4.4cqw}
.mobile .obs-brand .nm{font-size:6.6cqw}
.mobile .obs-brand .eyebrow{font-size:1.9cqw;letter-spacing:.3em;margin-top:1.6cqw}
.mobile .obs-meta{right:6cqw;top:5cqw;font-size:1.6cqw;line-height:2}
.mobile .obs-mchart{display:block;position:absolute;left:-3cqw;top:10cqw;width:106cqw;height:106cqw;z-index:2}
.mobile .obs-mchart svg{width:100%;height:100%;overflow:visible}
.mobile .obs-mchart text{font-family:'Space Mono',monospace;fill:#8b96be}
.mobile .obs-chart{display:none}
.mobile .obs-copy{left:6cqw;top:109cqw;width:88cqw}
.mobile .obs-copy h1{font-size:11.4cqw;line-height:.98}
.mobile .obs-copy p{margin-top:3cqw;font-size:3.15cqw;line-height:1.45;max-width:none;color:#cdc3a9}
.mobile .obs-copy .hint{display:none}
.mobile .obs-rows{display:block;position:absolute;left:6cqw;right:6cqw;top:146cqw;z-index:6}
.obs-row{display:flex;align-items:center;gap:3.4cqw;padding:3.4cqw 0;border-top:1px solid rgba(139,150,190,.28)}
.obs-row:last-child{border-bottom:1px solid rgba(139,150,190,.28)}
.obs-row .ic{flex:0 0 12cqw;height:12cqw;display:flex;align-items:center;justify-content:center}
.obs-row .ic svg{width:12cqw;height:12cqw;overflow:visible}
.obs-row h2{font-size:4.9cqw;line-height:1.02;font-weight:600}
.obs-row .no{font-family:'Space Mono',monospace;font-size:1.55cqw;letter-spacing:.26em;color:#d3ac6b;text-transform:uppercase}
.obs-row p{margin-top:1cqw;font-size:2.75cqw;line-height:1.4;color:#cdc3a9}
.obs-row .go{margin-left:auto;font-family:'Space Mono',monospace;font-size:1.5cqw;letter-spacing:.2em;color:#d3ac6b;white-space:nowrap}
.mobile .obs-cond{left:6cqw;right:6cqw;bottom:13cqw;font-size:1.5cqw;gap:3.4cqw;flex-wrap:wrap;line-height:2}
.mobile .obs-soc{left:6cqw;right:6cqw;bottom:5cqw;font-size:1.5cqw;gap:4cqw}
.mobile .obs-soc svg{width:2.2cqw;height:2.2cqw}
.mobile .obs-shoot{left:56cqw;top:18cqw;width:26cqw;animation-delay:1.4s}
"""


def obs_chart_svg(cls: str, seed: int) -> str:
    rnd = random.Random(seed)
    ticks = []
    for deg in range(0, 360, 5):
        long = deg % 15 == 0
        r1, r2 = (346, 364) if long else (355, 364)
        import math

        a = math.radians(deg - 90)
        x1, y1 = 400 + r1 * math.cos(a), 400 + r1 * math.sin(a)
        x2, y2 = 400 + r2 * math.cos(a), 400 + r2 * math.sin(a)
        w = 1.6 if long else 0.8
        op = 0.55 if long else 0.28
        ticks.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#8b96be" stroke-width="{w}" opacity="{op}"/>'
        )
    hours = []
    for h in range(24):
        deg = h * 15
        import math

        a = math.radians(deg - 90)
        x, y = 400 + 324 * math.cos(a), 400 + 324 * math.sin(a)
        if h % 2 == 0:
            hours.append(
                f'<text x="{x:.1f}" y="{y+3:.1f}" text-anchor="middle" font-size="12" letter-spacing="1">{h:02d}h</text>'
            )
    spokes = []
    for deg in range(0, 360, 45):
        import math

        a = math.radians(deg - 90)
        x1, y1 = 400 + 74 * math.cos(a), 400 + 74 * math.sin(a)
        x2, y2 = 400 + 344 * math.cos(a), 400 + 344 * math.sin(a)
        spokes.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#8b96be" stroke-width=".7" opacity=".14"/>'
        )
    disc = []
    for _ in range(46):
        import math

        a = rnd.uniform(0, math.tau)
        r = rnd.uniform(30, 330) ** 0.94
        x, y = 400 + r * math.cos(a), 400 + r * math.sin(a)
        rr = rnd.choice([0.7, 0.9, 1.1, 1.4])
        op = round(rnd.uniform(0.15, 0.5), 2)
        disc.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rr}" fill="#e9e7e1" opacity="{op}"/>')
    const = [(500, 250), (536, 268), (556, 232), (592, 246), (612, 288), (578, 312), (540, 318), (516, 292)]
    links = " ".join(
        f'<line x1="{const[i][0]}" y1="{const[i][1]}" x2="{const[i+1][0]}" y2="{const[i+1][1]}"/>'
        for i in range(len(const) - 1)
    )
    cstars = []
    for i, (x, y) in enumerate(const):
        r = [4.6, 2.6, 3.4, 2.4, 5.2, 2.8, 3.1, 2.5][i]
        op = [0.95, 0.6, 0.8, 0.55, 1, 0.62, 0.72, 0.58][i]
        cstars.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#e9e7e1" opacity="{op}"/>')
    return f"""<svg class="{cls}" viewBox="0 0 800 800" aria-hidden="true">
<defs>
<radialGradient id="obsDust"><stop offset="0" stop-color="#4b5680" stop-opacity=".5"/><stop offset="1" stop-color="#4b5680" stop-opacity="0"/></radialGradient>
</defs>
<circle cx="400" cy="400" r="372" fill="url(#obsDust)" opacity=".5"/>
<circle cx="400" cy="400" r="368" fill="none" stroke="#d3ac6b" stroke-width="1.4" opacity=".5"/>
<circle cx="400" cy="400" r="358" fill="none" stroke="#d3ac6b" stroke-width=".7" opacity=".28"/>
<circle cx="400" cy="400" r="344" fill="none" stroke="#8b96be" stroke-width=".7" opacity=".22"/>
<circle cx="400" cy="400" r="252" fill="none" stroke="#8b96be" stroke-width=".7" opacity=".16"/>
<circle cx="400" cy="400" r="158" fill="none" stroke="#8b96be" stroke-width=".7" opacity=".14"/>
{''.join(spokes)}
{''.join(ticks)}
{''.join(hours)}
{''.join(disc)}
<circle cx="418" cy="386" r="236" fill="none" stroke="#efe3c8" stroke-width=".8" stroke-dasharray="3 9" opacity=".2"/>
<g stroke="#d3ac6b" stroke-width=".9" opacity=".4">{links}</g>
{''.join(cstars)}
<circle cx="592" cy="246" r="26" fill="url(#obsDust)" opacity=".8"/>
<circle cx="286" cy="520" r="62" fill="url(#obsDust)" opacity=".9"/>
<circle cx="286" cy="520" r="30" fill="#d8b273"/>
<circle cx="286" cy="520" r="30" fill="#05070f" opacity=".38" clip-path="url(#obsClip)"/>
<ellipse cx="286" cy="520" rx="54" ry="14" fill="none" stroke="#d3ac6b" stroke-width="1.6" opacity=".8" transform="rotate(-16 286 520)"/>
<circle cx="286" cy="520" r="3" fill="#efe3c8"/>
<line x1="248" y1="520" x2="230" y2="520" stroke="#d3ac6b" stroke-width=".8" opacity=".6"/>
<line x1="324" y1="520" x2="342" y2="520" stroke="#d3ac6b" stroke-width=".8" opacity=".6"/>
<line x1="286" y1="480" x2="286" y2="464" stroke="#d3ac6b" stroke-width=".8" opacity=".6"/>
<line x1="286" y1="560" x2="286" y2="576" stroke="#d3ac6b" stroke-width=".8" opacity=".6"/>
</svg>"""


def obs_body() -> str:
    rnd = random.Random(7)
    stars = []
    for i in range(150):
        x = round(rnd.uniform(0, 1440), 1)
        y = round(rnd.uniform(0, 1000), 1)
        r = rnd.choice([0.5, 0.7, 0.9, 1.1, 1.5, 2.1])
        o = round(rnd.uniform(0.18, 0.92), 2)
        d = f' style="animation-delay:-{round(rnd.uniform(0,7),1)}s"' if i % 3 == 0 else ""
        stars.append(f'<circle cx="{x}" cy="{y}" r="{r}" opacity="{o}"{d}/>')
    star_svg = (
        '<svg class="obs-stars" viewBox="0 0 1440 1000" preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
        + "".join(stars)
        + "</svg>"
    )
    mini_planet = """<svg viewBox="0 0 120 120" aria-hidden="true"><circle cx="60" cy="60" r="30" fill="#d8b273"/><circle cx="60" cy="60" r="30" fill="#05070f" opacity=".35" clip-path="url(#obsClip)"/><ellipse cx="60" cy="60" rx="52" ry="13" fill="none" stroke="#d3ac6b" stroke-width="2" opacity=".8" transform="rotate(-16 60 60)"/></svg>"""
    mini_const = """<svg viewBox="0 0 120 120" aria-hidden="true"><g stroke="#d3ac6b" stroke-width="1.4" opacity=".5"><line x1="24" y1="80" x2="46" y2="62"/><line x1="46" y1="62" x2="66" y2="74"/><line x1="66" y1="74" x2="92" y2="40"/><line x1="46" y1="62" x2="58" y2="32"/><line x1="58" y1="32" x2="66" y2="74"/></g><g fill="#e9e7e1"><circle cx="24" cy="80" r="3.4"/><circle cx="46" cy="62" r="4.8"/><circle cx="66" cy="74" r="3"/><circle cx="92" cy="40" r="5.4"/><circle cx="58" cy="32" r="2.8"/></g></svg>"""
    arrow = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 19 L19 5 M9 5h10v10"/></svg>'
    return f"""
<div class="site obs">
{star_svg}
<span class="obs-mw" aria-hidden="true"></span>
<span class="obs-shoot" aria-hidden="true"></span>
<div class="obs-brand">
  <span class="nm">Musse&nbsp;Jusse</span>
  <span class="eyebrow">Night draft &middot; observatory</span>
</div>
<div class="obs-meta">Est. 2024<br>V3.0<br>Lat 56&deg;N</div>
<div class="obs-chart">{obs_chart_svg("", 11)}</div>
<div class="obs-mchart">{obs_chart_svg("", 11)}</div>
<div class="obs-copy">
  <h1>Two objects<br>worth watching.</h1>
  <p>I build small things on the web and chart them here. The chart changes when something new gets found.</p>
  <div class="hint">Hover an object</div>
</div>
<a class="obs-hot h1" href="https://roundest.mussejusse.com" aria-label="Roundest Pokémon, project MJ-001">
  <span class="spot"></span>
  <span class="tag"><b>MJ-001</b> / Roundest Pok&eacute;mon</span>
  <span class="obs-card" style="left:5.6cqw;top:calc(50% + 2.4cqw)">
    <span class="no">MJ-001 &middot; Next.js</span>
    <h2>Roundest Pok&eacute;mon</h2>
    <p>A comparison built around one question: which one is rounder? Server actions answer, a cache remembers.</p>
    <span class="go">Open chart {arrow}</span>
  </span>
</a>
<a class="obs-hot h2" href="https://models.mussejusse.com" aria-label="Models, project MJ-002">
  <span class="spot"></span>
  <span class="tag"><b>MJ-002</b> / Models</span>
  <span class="obs-card" style="right:5.6cqw;top:calc(50% + 2.4cqw)">
    <span class="no">MJ-002 &middot; Astro</span>
    <h2>Models</h2>
    <p>A catalogue of models, providers and what each can do. Static pages, almost no client code.</p>
    <span class="go">Open chart {arrow}</span>
  </span>
</a>
<div class="obs-rows">
  <a class="obs-row" href="https://roundest.mussejusse.com">
    <span class="ic">{mini_planet}</span>
    <span><span class="no">MJ-001 / Next.js</span><h2>Roundest Pok&eacute;mon</h2>
    <p>A comparison built around one question: which one is rounder?</p></span>
    <span class="go">Open</span>
  </a>
  <a class="obs-row" href="https://models.mussejusse.com">
    <span class="ic">{mini_const}</span>
    <span><span class="no">MJ-002 / Astro</span><h2>Models</h2>
    <p>A catalogue of models, providers and what each can do.</p></span>
    <span class="go">Open</span>
  </a>
</div>
<div class="obs-cond"><span>Seeing <i>steady</i></span><span>Transparency <i>clear</i></span><span>First light <i>2024</i></span></div>
<div class="obs-soc">
  <a href="https://bsky.app/profile/mussejusse.com">{arrow} Bluesky</a>
  <a href="https://github.com/MusseJusse">{arrow} GitHub</a>
</div>
</div>"""


# ---------------------------------------------------------------------------
# B / Field guide
# ---------------------------------------------------------------------------

FG_CSS = """
.fg{background:#efe9da;color:#33402f;font-family:'Spectral',Georgia,serif;line-height:1.5}
.fg-paper{position:absolute;inset:0;background:
 repeating-linear-gradient(0deg,rgba(51,64,47,.03) 0 1px,transparent 1px 4px),
 radial-gradient(120cqw 90cqw at 50% -20%,rgba(255,255,255,.5),rgba(255,255,255,0) 60%),
 radial-gradient(80cqw 60cqw at 90% 110%,rgba(124,58,50,.07),rgba(124,58,50,0) 60%);pointer-events:none}
.fg-run{position:absolute;left:4cqw;right:4cqw;top:3cqw;display:flex;justify-content:space-between;gap:3cqw;
 font-family:'Space Mono',monospace;font-size:.62cqw;letter-spacing:.24em;text-transform:uppercase;color:#6d7c5f;z-index:4}
.fg-run:after{content:'';position:absolute;left:0;right:0;top:2.1cqw;height:2px;background:#33402f}
.fg-run:before{content:'';position:absolute;left:0;right:0;top:2.55cqw;height:1px;background:#33402f;opacity:.55}
.fg-plates{position:absolute;left:4cqw;right:4cqw;top:7.4cqw;display:grid;grid-template-columns:1fr 1fr;gap:3.4cqw;z-index:3}
.fg-plate{display:grid;grid-template-rows:auto 1fr;transition:opacity 240ms ease-out}
.fg-art{position:relative;border:1px solid #33402f;padding:.55cqw;background:#efe9da}
.fg-art:before{content:'';position:absolute;inset:.45cqw;border:1px solid #33402f;opacity:.5;pointer-events:none}
.fg-art .wash{position:absolute;inset:.9cqw;background:#e7d6a8}
.fg-plate.p2 .fg-art .wash{background:#cdd9d6}
.fg-art svg{position:relative;width:100%;height:auto;z-index:2}
.fg-plate .pno{position:absolute;top:1.5cqw;left:1.9cqw;font-family:'Space Mono',monospace;font-size:.56cqw;letter-spacing:.28em;color:#33402f;text-transform:uppercase;z-index:3}
.fg-plate .pnm{position:absolute;top:1.3cqw;right:1.9cqw;font-family:'Space Mono',monospace;font-size:.56cqw;letter-spacing:.28em;color:#33402f;text-transform:uppercase;z-index:3}
.fg-ann-l{font-family:'Spectral',Georgia,serif;font-style:italic;font-size:15px;fill:#7c3a32}
.fg-ann-a{stroke:#33402f;stroke-width:1.1;fill:none}
.fg-ann-g{opacity:.42;transition:opacity 240ms ease-out}
.fg-plate:hover .fg-ann-g{opacity:1}
.fg-plates:hover .fg-plate:not(:hover){opacity:.42}
.fg-meta{padding-top:1.4cqw}
.fg-cap{margin-top:1cqw;font-style:italic;font-size:.78cqw;color:#6d7c5f}
.fg-meta h2{font-family:'Gloock',Georgia,serif;font-size:2.7cqw;line-height:1.04;letter-spacing:-.01em;color:#33402f;margin-top:.7cqw}
.fg-meta .latin{font-style:italic;font-size:1cqw;color:#6d7c5f;margin-top:.4cqw}
.fg-meta .desc{margin-top:1.1cqw;font-size:.88cqw;line-height:1.5;color:#3d4a37;max-width:40cqw}
.fg-dl{margin-top:1.3cqw;font-size:.82cqw;line-height:1.75}
.fg-dl div{display:flex;align-items:baseline;gap:.6cqw;color:#3d4a37}
.fg-dl dt{flex:0 0 auto;font-family:'Space Mono',monospace;font-size:.56cqw;letter-spacing:.2em;text-transform:uppercase;color:#6d7c5f}
.fg-dl dd{flex:1 1 auto;border-bottom:1px dotted rgba(51,64,47,.35)}
.fg-link{display:inline-flex;align-items:center;gap:.6cqw;margin-top:1.3cqw;font-family:'Space Mono',monospace;font-size:.6cqw;letter-spacing:.16em;text-transform:uppercase;color:#7c3a32}
.fg-link svg{width:.85cqw;height:.85cqw;stroke:#7c3a32;stroke-width:2;fill:none}
.fg-link:hover{text-decoration:underline;text-underline-offset:.4em}
.fg-notes{position:absolute;left:4cqw;right:4cqw;top:52.6cqw;border-top:1px solid #33402f;padding-top:1.4cqw;display:grid;grid-template-columns:1fr 1fr 1.2fr;gap:3.4cqw;z-index:4}
.fg-note b{display:block;font-family:'Space Mono',monospace;font-size:.56cqw;letter-spacing:.22em;font-weight:400;color:#6d7c5f;text-transform:uppercase;margin-bottom:.6cqw}
.fg-note p{font-size:.84cqw;line-height:1.55;color:#3d4a37}
.fg-range b{display:block;font-family:'Space Mono',monospace;font-size:.56cqw;letter-spacing:.22em;font-weight:400;color:#6d7c5f;text-transform:uppercase;margin-bottom:.6cqw}
.fg-range .bar{display:block;height:1.5cqw;border:1px solid #33402f;background:repeating-linear-gradient(135deg,rgba(51,64,47,.55) 0 1px,transparent 1px 4px)}
.fg-range .lbl{display:block;margin-top:.6cqw;font-style:italic;font-size:.78cqw;color:#6d7c5f}
.fg-list{position:absolute;left:4cqw;right:4cqw;bottom:3.4cqw;border-top:2px solid #33402f;padding-top:1.2cqw;display:flex;justify-content:space-between;align-items:flex-end;gap:3cqw;z-index:4}
.fg-list h3{font-family:'Gloock',Georgia,serif;font-size:1.35cqw;font-weight:400}
.fg-list .items{display:flex;gap:2.2cqw;font-size:.82cqw;color:#3d4a37}
.fg-list .items b{display:block;font-family:'Space Mono',monospace;font-size:.56cqw;letter-spacing:.18em;font-weight:400;color:#6d7c5f;text-transform:uppercase}
.fg-soc{display:flex;gap:2cqw;font-family:'Space Mono',monospace;font-size:.58cqw;letter-spacing:.16em;text-transform:uppercase}
.fg-soc a{color:#6d7c5f;border-bottom:1px solid rgba(51,64,47,.4);padding-bottom:.25cqw}
.fg-soc a:hover{color:#7c3a32;border-color:#7c3a32}
.mobile .fg-run{left:6cqw;right:6cqw;top:4cqw;font-size:1.5cqw;letter-spacing:.2em}
.mobile .fg-run:after{top:4.6cqw;height:3px}
.mobile .fg-run:before{top:5.5cqw}
.mobile .fg-plates{left:6cqw;right:6cqw;top:9.6cqw;grid-template-columns:1fr;gap:3.4cqw}
.mobile .fg-art{padding:1.4cqw}
.mobile .fg-art:before{inset:1.1cqw}
.mobile .fg-art .wash{inset:2cqw}
.mobile .fg-art svg{width:85%;margin:0 auto}
.mobile .fg-plate .pno,.mobile .fg-plate .pnm{font-size:1.4cqw;top:3.4cqw}
.mobile .fg-plate .pno{left:4cqw}
.mobile .fg-plate .pnm{right:4cqw}
.mobile .fg-ann-g{opacity:.75}
.mobile .fg-meta{padding-top:1.4cqw}
.mobile .fg-cap{margin-top:1.5cqw;font-size:2.1cqw}
.mobile .fg-notes{display:none}
.mobile .fg-meta h2{font-size:6.6cqw;margin-top:.4cqw}
.mobile .fg-meta .latin{font-size:2.3cqw;margin-top:.8cqw}
.mobile .fg-meta .desc{margin-top:1.5cqw;font-size:2.3cqw;line-height:1.38;max-width:none}
.mobile .fg-dl{margin-top:1.6cqw;font-size:2.2cqw;line-height:1.5}
.mobile .fg-dl div{display:block;padding:.3cqw 0;border-bottom:1px dotted rgba(51,64,47,.3)}
.mobile .fg-dl dt{display:inline;font-size:1.42cqw;letter-spacing:.18em;margin-right:1.6cqw}
.mobile .fg-dl dd{display:inline;border-bottom:0}
.mobile .fg-link{margin-top:1.4cqw;font-size:1.55cqw}
.mobile .fg-link svg{width:2.1cqw;height:2.1cqw}
.mobile .fg-list{left:6cqw;right:6cqw;bottom:4cqw;display:block;padding-top:1.8cqw}
.mobile .fg-list h3{font-size:3.4cqw}
.mobile .fg-list .items{margin-top:1.2cqw;display:grid;grid-template-columns:1fr 1fr;column-gap:4cqw;font-size:2.05cqw}
.mobile .fg-list .items span{display:flex;gap:2cqw;padding:.35cqw 0;border-bottom:1px dotted rgba(51,64,47,.3)}
.mobile .fg-list .items b{flex:0 0 13cqw;font-size:1.38cqw;padding-top:.4cqw}
.mobile .fg-soc{margin-top:1.2cqw;gap:4.4cqw;font-size:1.55cqw}
"""

FG_PLATE1_SVG = """<svg viewBox="0 0 720 400" aria-hidden="true">
<circle cx="300" cy="208" r="122" fill="url(#hatchSage)" opacity=".65"/>
<circle cx="284" cy="200" r="122" fill="#e7d6a8"/>
<circle cx="300" cy="208" r="122" fill="none" stroke="#33402f" stroke-width="1.6"/>
<g fill="none" stroke="#33402f" opacity=".22"><ellipse cx="300" cy="208" rx="122" ry="40"/><ellipse cx="300" cy="208" rx="122" ry="82"/><ellipse cx="300" cy="208" rx="40" ry="122"/><ellipse cx="300" cy="208" rx="82" ry="122"/></g>
<ellipse cx="300" cy="208" rx="196" ry="66" fill="none" stroke="#33402f" stroke-width="1.2" stroke-dasharray="2 7" opacity=".65" transform="rotate(-17 300 208)"/>
<circle cx="472" cy="152" r="8" fill="#efe9da" stroke="#33402f" stroke-width="1.4"/>
<g class="fg-ann-g">
<line class="fg-ann-a" x1="452" y1="88" x2="372" y2="130" marker-end="url(#ahSage)"/>
<text class="fg-ann-l" x="460" y="84">spherical silhouette</text>
<line class="fg-ann-a" x1="118" y1="112" x2="230" y2="168" marker-end="url(#ahSage)"/>
<text class="fg-ann-l" x="110" y="108" text-anchor="end">holds one answer</text>
<line class="fg-ann-a" x1="470" y1="340" x2="428" y2="272" marker-end="url(#ahSage)"/>
<text class="fg-ann-l" x="478" y="344">cached at the edge</text>
</g>
</svg>"""

FG_PLATE2_SVG = """<svg viewBox="0 0 720 400" aria-hidden="true">
<rect x="176" y="86" width="368" height="228" fill="none" stroke="#33402f" stroke-width="1.1" stroke-dasharray="5 7" opacity=".6"/>
<g stroke="#33402f" stroke-width="1.4">
<g transform="rotate(-13 330 210)"><rect x="243" y="100" width="174" height="220" fill="#cdd9d6"/></g>
<g transform="rotate(-4 330 210)"><rect x="243" y="100" width="174" height="220" fill="#cdd9d6"/></g>
<g transform="rotate(5 330 210)"><rect x="243" y="100" width="174" height="220" fill="#cdd9d6"/></g>
<g transform="rotate(13 330 210)"><rect x="243" y="100" width="174" height="220" fill="#cdd9d6"/><line x1="266" y1="140" x2="396" y2="140" opacity=".5"/><line x1="266" y1="158" x2="360" y2="158" opacity=".4"/><line x1="266" y1="176" x2="382" y2="176" opacity=".4"/><line x1="266" y1="194" x2="340" y2="194" opacity=".3"/></g>
</g>
<g fill="url(#hatchSage)" opacity=".5"><rect x="266" y="230" width="130" height="70" transform="rotate(13 330 210)"/></g>
<text x="330" y="366" text-anchor="middle" font-family="'Space Mono',monospace" font-size="13" letter-spacing="3" fill="#33402f">200+ ENTRIES</text>
<line x1="330" y1="352" x2="330" y2="330" stroke="#33402f" stroke-width="1" opacity=".6"/>
<g class="fg-ann-g">
<line class="fg-ann-a" x1="152" y1="120" x2="238" y2="152" marker-end="url(#ahSage)"/>
<text class="fg-ann-l" x="144" y="116" text-anchor="end">flattened, static pages</text>
<line class="fg-ann-a" x1="510" y1="118" x2="430" y2="150" marker-end="url(#ahSage)"/>
<text class="fg-ann-l" x="518" y="114">no client framework</text>
<line class="fg-ann-a" x1="516" y1="330" x2="444" y2="286" marker-end="url(#ahSage)"/>
<text class="fg-ann-l" x="524" y="334">each one a page</text>
</g>
</svg>"""


def fg_body() -> str:
    arrow = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 19 L19 5 M9 5h10v10"/></svg>'
    return f"""
<div class="site fg">
<span class="fg-paper" aria-hidden="true"></span>
<header class="fg-run"><span>MusseJusse / a field guide to the web</span><span>Vol. 3 &middot; Plates I&ndash;II</span></header>
<div class="fg-plates">
<article class="fg-plate p1">
  <div class="fg-art"><span class="wash" aria-hidden="true"></span><span class="pno">No. 001</span><span class="pnm">Plate I</span>{FG_PLATE1_SVG}</div>
  <div class="fg-cap">Fig. 1 &middot; adult specimen, drawn from the live site</div>
  <div class="fg-meta">
    <h2>Roundest Pok&eacute;mon</h2>
    <div class="latin">Rotundus pokemonius</div>
    <p class="desc">A small comparison that asks one question and answers it without ceremony. Two creatures enter, one is rounder, and the page remembers the verdict.</p>
    <dl class="fg-dl">
      <div><dt>Habitat</dt><dd>edge habitat, nests in a KV store</dd></div>
      <div><dt>Song</dt><dd>a single question, repeated</dd></div>
      <div><dt>Range</dt><dd>everywhere a browser reaches</dd></div>
    </dl>
    <a class="fg-link" href="https://roundest.mussejusse.com">{arrow} roundest.mussejusse.com</a>
  </div>
</article>
<article class="fg-plate p2">
  <div class="fg-art"><span class="wash" aria-hidden="true"></span><span class="pno">No. 002</span><span class="pnm">Plate II</span>{FG_PLATE2_SVG}</div>
  <div class="fg-cap">Fig. 2 &middot; collected pages, pinned in order</div>
  <div class="fg-meta">
    <h2>Models</h2>
    <div class="latin">Catalogus modelorum</div>
    <p class="desc">A field catalogue of models, providers and capabilities, collected, sorted and pinned like specimens. The whole catalogue arrives prewritten.</p>
    <dl class="fg-dl">
      <div><dt>Habitat</dt><dd>static plains, builds at dawn</dd></div>
      <div><dt>Song</dt><dd>silent; pages arrive prewritten</dd></div>
      <div><dt>Range</dt><dd>everywhere a browser reaches, often offline</dd></div>
    </dl>
    <a class="fg-link" href="https://models.mussejusse.com">{arrow} models.mussejusse.com</a>
  </div>
</article>
</div>
<section class="fg-notes">
  <div class="fg-note"><b>Collected</b><p>Both species were found within walking distance of a browser tab and have been observed in the wild since 2025.</p></div>
  <div class="fg-note"><b>Method</b><p>No build step is needed to observe either one. Approach quietly and refresh if a specimen is mid-change.</p></div>
  <div class="fg-range"><b>Range</b><span class="bar" aria-hidden="true"></span><span class="lbl">worldwide, wherever there is a browser</span></div>
</section>
<footer class="fg-list">
  <h3>Life list</h3>
  <div class="items">
    <span><b>2024</b>the first site</span>
    <span><b>2025</b>Roundest Pok&eacute;mon</span>
    <span><b>2026</b>Models</span>
    <span><b>2026</b>V3.0, this page</span>
  </div>
  <div class="fg-soc"><a href="https://bsky.app/profile/mussejusse.com">Bluesky</a><a href="https://github.com/MusseJusse">GitHub</a><a href="https://vercel.com">Vercel</a></div>
</footer>
</div>"""




# ---------------------------------------------------------------------------
# C / Lab notebook
# ---------------------------------------------------------------------------

LAB_CSS = """
.lab{background:radial-gradient(140cqw 90cqw at 50% -10%,#3a382f 0%,#26251f 55%,#1d1c17 100%);color:#1a1c21;font-family:Archivo,system-ui,sans-serif}
.lab-spread{position:absolute;left:5cqw;top:4.6cqw;width:90cqw;height:59.6cqw;display:grid;grid-template-columns:1fr 1fr;box-shadow:0 1.4cqw 3.4cqw rgba(0,0,0,.5)}
.lab-single{display:none}
.lab-page{position:relative;background:#f6f5ef;padding:2.4cqw 2.8cqw 2.2cqw 3.8cqw;overflow:hidden;
 background-image:repeating-linear-gradient(0deg,rgba(28,63,158,.07) 0 1px,transparent 1px 2.7cqw),repeating-linear-gradient(90deg,rgba(28,63,158,.07) 0 1px,transparent 1px 2.7cqw)}
.lab-page:before{content:'';position:absolute;left:2.5cqw;top:0;bottom:0;width:1px;background:rgba(223,167,158,.95)}
.lab-page.gutter-l:after{content:'';position:absolute;right:0;top:0;bottom:0;width:2.6cqw;background:linear-gradient(90deg,transparent,rgba(0,0,0,.16))}
.lab-page.gutter-r:after{content:'';position:absolute;left:0;top:0;bottom:0;width:2.6cqw;background:linear-gradient(270deg,transparent,rgba(0,0,0,.16))}
.lab-head{display:flex;justify-content:space-between;align-items:baseline;gap:1cqw;font-family:'Space Mono',monospace;font-size:.58cqw;letter-spacing:.2em;text-transform:uppercase;border-bottom:2px solid #1a1c21;padding-bottom:.65cqw}
.lab-head b{font-weight:700}
.lab-page h2{margin-top:1.2cqw;font-size:2.25cqw;font-weight:700;letter-spacing:-.02em;line-height:1.05}
.lab-reagents{margin-top:.45cqw;font-family:'Space Mono',monospace;font-size:.56cqw;letter-spacing:.15em;color:#1c3f9e}
.lab-aim{display:inline;margin-top:1cqw;font-size:.98cqw;font-weight:600;line-height:1.65;background:linear-gradient(transparent 56%,rgba(243,215,116,.72) 56%,rgba(243,215,116,.72) 92%,transparent 92%)}
.lab-body{display:grid;grid-template-columns:1fr 1.06fr;gap:1.6cqw;margin-top:.9cqw}
.lab-ph{font-family:'Space Mono',monospace;font-size:.54cqw;letter-spacing:.22em;text-transform:uppercase;color:#8b8e94}
.lab-steps{margin-top:.6cqw}
.lab-steps li{display:grid;grid-template-columns:.95cqw 1fr;gap:.55cqw;font-size:.8cqw;line-height:1.42;padding:.28cqw 0}
.lab-steps li b{font-family:'Space Mono',monospace;font-size:.62cqw;color:#1c3f9e;font-weight:700}
.lab-fig{margin-top:.7cqw;border:1px solid rgba(26,28,33,.28);background:rgba(255,255,255,.5)}
.lab-fig svg{width:100%;height:auto}
.lab-figcap{display:block;padding:.4cqw .6cqw;font-family:'Space Mono',monospace;font-size:.5cqw;letter-spacing:.16em;text-transform:uppercase;color:#8b8e94;border-top:1px solid rgba(26,28,33,.16)}
.lab-obs{margin-top:1cqw;font-size:.82cqw;line-height:1.45;color:#2a2d33}
.lab-obs b{font-family:'Space Mono',monospace;font-size:.54cqw;letter-spacing:.22em;text-transform:uppercase;color:#8b8e94;font-weight:400;display:block;margin-bottom:.35cqw}
.lab-nextsteps{position:absolute;left:3.8cqw;bottom:8.6cqw;width:30cqw;font-size:.8cqw;line-height:1.4;color:#6f7278}
.lab-nextsteps b{font-family:'Space Mono',monospace;font-size:.54cqw;letter-spacing:.22em;text-transform:uppercase;color:#8b8e94;font-weight:400;display:block;margin-bottom:.3cqw}
.lab-stamp{position:absolute;bottom:4.2cqw;transform:rotate(-7deg);border:1.5px solid rgba(194,59,43,.75);border-radius:.2cqw;padding:.45cqw .8cqw;font-family:'Space Mono',monospace;font-size:.56cqw;letter-spacing:.18em;text-transform:uppercase;color:#c23b2b;box-shadow:inset 0 0 0 1px rgba(194,59,43,.3)}
.lab-page.gutter-l .lab-stamp{left:3.8cqw}
.lab-page.gutter-r .lab-stamp{right:2.8cqw}
.lab-pgno{position:absolute;bottom:1.6cqw;font-family:'Space Mono',monospace;font-size:.5cqw;letter-spacing:.22em;color:#8b8e94}
.lab-page.gutter-l .lab-pgno{left:3.8cqw}
.lab-page.gutter-r .lab-pgno{right:2.8cqw}
.lab-rings{position:absolute;inset:0;pointer-events:none;z-index:5}
.lab-rings svg{position:absolute;inset:0;width:100%;height:100%}
.lab-rings-l{display:none}
.lab-next{position:absolute;left:50%;top:60.4cqw;transform:translateX(-50%) rotate(-1.3deg);width:46cqw;background:#efeddf;border:1px solid #d8d3c0;padding:1cqw 1.6cqw 1.1cqw;box-shadow:0 .9cqw 2.2cqw rgba(0,0,0,.45);z-index:6}
.lab-next:before{content:'';position:absolute;left:50%;top:-1cqw;transform:translateX(-50%) rotate(1.8deg);width:9cqw;height:2cqw;background:rgba(255,255,255,.42);border:1px solid rgba(0,0,0,.06)}
.lab-next .row{display:flex;justify-content:space-between;align-items:baseline;gap:1cqw;font-family:'Space Mono',monospace;font-size:.54cqw;letter-spacing:.2em;text-transform:uppercase}
.lab-next .row b{font-weight:700}
.lab-next .row em{font-style:normal;color:#c23b2b}
.lab-next p{margin-top:.5cqw;font-size:.78cqw;line-height:1.4}
.lab-bar{margin-top:.8cqw;height:.75cqw;border:1px solid #1a1c21;position:relative;overflow:hidden}
.lab-bar i{position:absolute;inset:0;transform-origin:0 50%;transform:scaleX(.72);background:repeating-linear-gradient(90deg,#1c3f9e 0 3px,transparent 3px 5px)}
.lab-bar span{position:absolute;inset:0;background:linear-gradient(90deg,transparent,rgba(28,63,158,.28),transparent);animation:lab-scan 5s linear infinite}
@keyframes lab-scan{0%{transform:translateX(-100%)}100%{transform:translateX(100%)}}
.lab-foot{position:absolute;left:5cqw;right:5cqw;bottom:1cqw;display:flex;justify-content:space-between;gap:2cqw;font-family:'Space Mono',monospace;font-size:.56cqw;letter-spacing:.18em;text-transform:uppercase;color:#9d9787;z-index:7}
.lab-foot a{color:#9d9787;border-bottom:1px solid rgba(157,151,135,.4);padding-bottom:.2cqw}
.lab-foot a:hover{color:#f6f5ef;border-color:#f6f5ef}
.lab-page .lab-clip{position:absolute;top:-1.2cqw;right:1.6cqw;width:4cqw;height:5.6cqw;transform:rotate(14deg);z-index:4}
.lab-page .lab-clip svg{width:100%;height:100%}
.mobile .lab-spread{display:none}
.mobile .lab-single{display:block;position:absolute;left:9cqw;right:4.5cqw;top:5cqw;bottom:13cqw;background:#f6f5ef;padding:2.8cqw 3.6cqw 2.4cqw 4cqw;overflow:hidden;
 background-image:repeating-linear-gradient(0deg,rgba(28,63,158,.07) 0 1px,transparent 1px 6.8cqw),repeating-linear-gradient(90deg,rgba(28,63,158,.07) 0 1px,transparent 1px 6.8cqw);box-shadow:0 1.6cqw 4cqw rgba(0,0,0,.5)}
.mobile .lab-single:before{content:'';position:absolute;top:0;bottom:0;left:3.6cqw;width:1px;background:rgba(223,167,158,.95)}
.mobile .lab-rings-l{display:block;position:absolute;left:3cqw;top:5cqw;bottom:13cqw;width:6cqw;z-index:6}
.mobile .lab-rings-l svg{width:100%;height:100%}
.mobile .lab-rings{display:none}
.mobile .lab-head{font-size:1.42cqw;padding-bottom:1.4cqw}
.mobile .lab-single h2{margin-top:1.6cqw;font-size:5.8cqw}
.mobile .lab-reagents{margin-top:1cqw;font-size:1.42cqw}
.mobile .lab-aim{margin-top:1.6cqw;font-size:2.4cqw;line-height:1.6}
.mobile .lab-body{grid-template-columns:1fr;gap:0;margin-top:2cqw}
.mobile .lab-ph{font-size:1.38cqw}
.mobile .lab-steps{margin-top:1.4cqw}
.mobile .lab-steps li{grid-template-columns:2.4cqw 1fr;gap:1.4cqw;font-size:2cqw;line-height:1.38;padding:.4cqw 0}
.mobile .lab-steps li b{font-size:1.7cqw}
.mobile .lab-fig{margin-top:1.6cqw;display:flex;flex-direction:column;align-items:center}
.mobile .lab-fig svg{height:24cqw;width:auto}
.mobile .lab-figcap{display:none}
.mobile .lab-obs{margin-top:1.6cqw;font-size:2.15cqw;line-height:1.4}
.mobile .lab-obs b{display:inline;font-size:1.32cqw;margin:0 .9cqw 0 0}
.mobile .lab-rule{height:2px;background:#1a1c21;margin:3cqw 0 0}
.mobile .lab-entry2{margin-top:2.6cqw}
.mobile .lab-nextsteps{position:static;width:auto;margin-top:1.8cqw;font-size:2.05cqw}
.mobile .lab-nextsteps b{font-size:1.32cqw;margin-bottom:.7cqw}
.mobile .lab-stamp{display:none}
.mobile .lab-pgno{display:none}
.mobile .lab-next{position:static;transform:none;width:auto;margin:2.6cqw 0 0;padding:2cqw 2.4cqw 2.2cqw}
.mobile .lab-next:before{top:-1.8cqw;width:18cqw;height:4cqw}
.mobile .lab-next .row{font-size:1.4cqw}
.mobile .lab-next p{margin-top:1.2cqw;font-size:2.05cqw}
.mobile .lab-bar{margin-top:2cqw;height:2cqw}
.mobile .lab-foot{left:4.5cqw;right:4.5cqw;bottom:3cqw;font-size:1.4cqw;flex-direction:column;gap:1.6cqw}
.mobile .lab-page .lab-clip{display:none}
"""

LAB_FIG1 = """<svg viewBox="0 0 300 210" aria-hidden="true">
<g stroke="#1c3f9e" stroke-width="1.6" fill="none">
<circle cx="172" cy="100" r="62" fill="rgba(28,63,158,.07)"/>
<circle cx="52" cy="100" r="24" stroke-dasharray="3 5"/>
<line x1="160" y1="100" x2="184" y2="100"/>
<line x1="172" y1="88" x2="172" y2="112"/>
<line x1="110" y1="100" x2="172" y2="100" stroke-dasharray="2 4" opacity=".7"/>
<line x1="172" y1="36" x2="172" y2="18"/>
<line x1="240" y1="100" x2="258" y2="100"/>
</g>
<line x1="86" y1="180" x2="172" y2="180" stroke="#1c3f9e" stroke-width="1.2" marker-start="url(#ahCobalt)" marker-end="url(#ahCobalt)"/>
<line x1="86" y1="174" x2="86" y2="186" stroke="#1c3f9e" stroke-width="1.2"/>
<line x1="172" y1="174" x2="172" y2="186" stroke="#1c3f9e" stroke-width="1.2"/>
<line x1="198" y1="112" x2="226" y2="130" stroke="#1c3f9e" stroke-width="1.2" marker-end="url(#ahCobalt)"/>
<text x="170" y="62" text-anchor="middle" font-family="'Space Mono',monospace" font-size="11" fill="#1c3f9e">A</text>
<text x="52" y="104" text-anchor="middle" font-family="'Space Mono',monospace" font-size="10" fill="#1c3f9e">B</text>
<text x="129" y="174" text-anchor="middle" font-family="'Space Mono',monospace" font-size="9" fill="#1c3f9e">d</text>
<text x="232" y="142" font-family="'Space Mono',monospace" font-size="9" fill="#1c3f9e">A &gt; B</text>
<text x="172" y="14" text-anchor="middle" font-family="'Space Mono',monospace" font-size="9" fill="#8b8e94">SOLID</text>
<text x="52" y="140" text-anchor="middle" font-family="'Space Mono',monospace" font-size="9" fill="#8b8e94">REF</text>
</svg>"""

LAB_FIG2 = """<svg viewBox="0 0 300 210" aria-hidden="true">
<g stroke="#1c3f9e" stroke-width="1.5" fill="#f6f5ef">
<rect x="80" y="34" width="118" height="140"/>
<rect x="88" y="42" width="118" height="140"/>
<rect x="96" y="50" width="118" height="140"/>
</g>
<rect x="96" y="50" width="118" height="140" fill="none" stroke="#1c3f9e" stroke-width="1.5" stroke-dasharray="4 5"/>
<g stroke="#1c3f9e" stroke-width="1.2" opacity=".65">
<line x1="112" y1="78" x2="196" y2="78"/>
<line x1="112" y1="94" x2="178" y2="94"/>
<line x1="112" y1="110" x2="190" y2="110"/>
<line x1="112" y1="126" x2="164" y2="126"/>
</g>
<path d="M232 50 h8 v140 h-8" fill="none" stroke="#1c3f9e" stroke-width="1.4"/>
<text x="248" y="116" font-family="'Space Mono',monospace" font-size="11" fill="#1c3f9e">N=200+</text>
</svg>"""

LAB_CLIP = """<svg viewBox="0 0 44 60" aria-hidden="true"><path d="M14 54 V14 a8 8 0 0 1 16 0 v34 a5 5 0 0 1 -10 0 V22" fill="none" stroke="#1a1c21" stroke-width="2.6" stroke-linecap="round" opacity=".85"/></svg>"""


def lab_rings(count: int, vertical: bool = False) -> str:
    if vertical:
        return (
            '<svg viewBox="0 0 60 1900" preserveAspectRatio="none" aria-hidden="true">'
            + "".join(
                f'<rect x="0" y="{i*118+20}" width="60" height="14" rx="7" fill="none" stroke="#23231f" stroke-width="2.4"/>'
                for i in range(count)
            )
            + "</svg>"
        )
    return (
        '<svg viewBox="0 0 900 596" aria-hidden="true">'
        + "".join(
            f'<rect x="438" y="{i*42+18}" width="24" height="14" rx="7" fill="none" stroke="#23231f" stroke-width="2.2"/>'
            for i in range(count)
        )
        + "</svg>"
    )


def lab_entry(n: str, date: str, title: str, reagents: str, aim: str, steps: list, fig: str, figcap: str, obs: str, nxt: str) -> str:
    s = "".join(f"<li><b>{i+1:02d}</b><span>{t}</span></li>" for i, t in enumerate(steps))
    return f"""
<header class="lab-head"><span><b>Experiment {n}</b></span><span>Logged {date}</span></header>
<h2>{title}</h2>
<div class="lab-reagents">{reagents}</div>
<div class="lab-aim">{aim}</div>
<div class="lab-body">
  <div><div class="lab-ph">Procedure</div><ol class="lab-steps">{s}</ol></div>
  <div><div class="lab-fig">{fig}<span class="lab-figcap">{figcap}</span></div></div>
</div>
<div class="lab-obs"><b>Observation</b>{obs}</div>
<div class="lab-nextsteps"><b>Next</b>{nxt}</div>
"""


def lab_body() -> str:
    e1 = lab_entry(
        "01", "2025", "Roundest Pok&eacute;mon", "NEXT.JS 16 / SERVER ACTIONS / KV STORE",
        "Which one is rounder?",
        ["Serve the comparison from the edge.", "Ask the cache once, then remember the answer.", "Draw both creatures to scale and let the rounder one win."],
        LAB_FIG1, "Fig. 1 / sphere, to scale",
        "Results arrive immediately and repeat exactly. Nobody has disputed the method.",
        "Measure once more, then leave it alone.",
    )
    e2 = lab_entry(
        "02", "2026", "Models", "ASTRO / CONTENT COLLECTIONS / STATIC OUTPUT",
        "What is inside every model?",
        ["Collect models, providers and their capabilities.", "Flatten each entry into a page at build time.", "Ship the pages and keep the client quiet."],
        LAB_FIG2, "Fig. 2 / entries, flattened",
        "The catalogue grows by pull request. Nothing is computed twice.",
        "Add a provider whose status is always changing.",
    )
    return f"""
<div class="site lab">
<div class="lab-spread">
  <section class="lab-page gutter-l">{e1}
    <span class="lab-stamp">Recorded 2025</span><span class="lab-pgno">Page 014</span>
  </section>
  <section class="lab-page gutter-r">{e2}
    <span class="lab-stamp">Recorded 2026</span><span class="lab-pgno">Page 015</span>
  </section>
</div>
<div class="lab-rings">{lab_rings(13)}</div>
<div class="lab-next">
  <div class="row"><b>Experiment 03 / this page</b><em>In progress</em></div>
  <p>A live record of version 3.0, observed while you read. The layout is still reacting.</p>
  <div class="lab-bar"><i></i><span></span></div>
</div>
<section class="lab-single">{e1}<div class="lab-rule"></div><div class="lab-entry2">{e2}</div>
  <div class="lab-next">
    <div class="row"><b>Experiment 03 / this page</b><em>In progress</em></div>
    <p>A live record of version 3.0, observed while you read.</p>
    <div class="lab-bar"><i></i><span></span></div>
  </div>
</section>
<div class="lab-rings-l">{lab_rings(16, True)}</div>
<div class="lab-foot">
  <span>Initials MJ &middot; Book 3 &middot; Page 014, continued</span>
  <span><a href="https://github.com/MusseJusse">Source on GitHub</a> &middot; <a href="https://vercel.com">Hosted on Vercel</a></span>
</div>
</div>"""


# ---------------------------------------------------------------------------
# D / Radio
# ---------------------------------------------------------------------------

import math

RAD_CSS = """
.rad{background:radial-gradient(120cqw 80cqw at 50% 8%,#3b342a 0%,#211d17 55%,#15130f 100%);color:#1a1714;font-family:Oswald,system-ui,sans-serif}
.rad-cab{position:absolute;left:8cqw;right:8cqw;top:4.4cqw;height:60.6cqw;border-radius:1.4cqw;background:
 linear-gradient(90deg,#5a3d28,#7a5638 6%,#5f412b 12%,#6d4c31 50%,#5f412b 88%,#7a5638 94%,#5a3d28),
 linear-gradient(#6d4c31,#3f2a1b);box-shadow:0 2cqw 5cqw rgba(0,0,0,.55),inset 0 1px 0 rgba(255,235,200,.25)}
.rad-cab:before{content:'';position:absolute;left:-1.4cqw;right:-1.4cqw;bottom:-1.1cqw;height:2.2cqw;border-radius:0 0 1.2cqw 1.2cqw;background:linear-gradient(#2e1f14,#1c130c)}
.rad-face{position:absolute;left:3cqw;right:3cqw;top:2.6cqw;bottom:2.6cqw;border-radius:.7cqw;background:#e9e1cd;
 background-image:repeating-linear-gradient(0deg,rgba(26,23,20,.028) 0 1px,transparent 1px 3px);box-shadow:inset 0 0 0 1.5px #b08d57,inset 0 0 1.6cqw rgba(90,61,40,.22),0 .4cqw 1cqw rgba(0,0,0,.35);padding:2.2cqw 2.6cqw;overflow:hidden}
.rad-row1{display:flex;align-items:flex-start;justify-content:space-between;gap:2cqw}
.rad-brand .nm{font-size:2.9cqw;font-weight:500;letter-spacing:.05em;line-height:1;text-transform:uppercase}
.rad-brand .sub{margin-top:.5cqw;font-family:'Space Mono',monospace;font-size:.58cqw;letter-spacing:.3em;text-transform:uppercase;color:#7a6a52}
.rad-row1 .right{display:flex;align-items:center;gap:2cqw}
.rad-badge{font-family:'Space Mono',monospace;font-size:.58cqw;letter-spacing:.22em;border:1.5px solid #1a1714;border-radius:.3cqw;padding:.4cqw .8cqw;text-transform:uppercase}
.rad-lamp{display:flex;align-items:center;gap:.8cqw;font-family:'Space Mono',monospace;font-size:.6cqw;letter-spacing:.24em;text-transform:uppercase}
.rad-lamp i{width:1cqw;height:1cqw;border-radius:50%;background:#e8a33d;box-shadow:0 0 .9cqw rgba(232,163,61,.9),inset 0 0 0 1px rgba(90,61,40,.5);opacity:calc(.2 + .8*var(--tune,1));transition:opacity 200ms ease-out}
.rad-main{display:grid;grid-template-columns:26cqw 1fr;gap:3cqw;margin-top:2cqw}
.rad-grille{position:relative;height:17.6cqw;border:1.5px solid #1a1714;border-radius:.4cqw;overflow:hidden;
 background:
 repeating-linear-gradient(90deg,rgba(255,240,210,.05) 0 1px,transparent 1px 3px),
 repeating-linear-gradient(0deg,#453b2e 0 .2cqw,#221d16 .2cqw .34cqw,#191612 .34cqw .62cqw);
 box-shadow:inset 0 .4cqw 1.4cqw rgba(0,0,0,.7),inset 0 -.4cqw 1cqw rgba(0,0,0,.5)}
.rad-grille .plate{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);background:#b08d57;border-radius:.3cqw;padding:.35cqw 1.2cqw;font-family:'Space Mono',monospace;font-size:.62cqw;letter-spacing:.3em;color:#241a10}
.rad-tuner{display:flex;align-items:center;gap:2.6cqw}
.rad-scope{position:relative;flex:1;height:17.6cqw;border:1.5px solid #1a1714;border-radius:.4cqw;background:radial-gradient(80% 120% at 50% 0%,#20402a,#0d1c12 70%);overflow:hidden;box-shadow:inset 0 0 1.4cqw rgba(0,0,0,.7)}
.rad-scope svg{position:absolute;inset:0;width:100%;height:100%}
.rad-scope .clean{opacity:var(--tune,1);transition:opacity 120ms linear}
.rad-scope .noise{opacity:calc(1 - var(--tune,1));transition:opacity 120ms linear}
.rad-scope .scan{position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(120,200,140,.05) 0 1px,transparent 1px 3px);pointer-events:none}
.rad-eye-wrap{display:flex;flex-direction:column;align-items:center;gap:.8cqw}
.rad-eye{position:relative;width:5.4cqw;height:5.4cqw;border-radius:50%;background:radial-gradient(circle at 50% 32%,#24391d,#0b120a 72%);display:flex;align-items:center;justify-content:center;overflow:hidden;
 box-shadow:inset 0 0 0 2px #b08d57,inset 0 0 0 3px rgba(26,23,20,.7),inset 0 0 1.2cqw rgba(0,0,0,.9),0 .25cqw .6cqw rgba(0,0,0,.35)}
.rad-eye i{width:72%;height:30%;border-radius:50%;background:radial-gradient(closest-side,#c3e89a,#4d7a35 70%,#274218);box-shadow:0 0 1.1cqw rgba(150,220,120,.55);transition:transform 140ms ease-out;transform:scaleX(calc(.12 + .88 * var(--tune,1)))}
.rad-eye b{position:absolute;left:0;top:0;bottom:0;width:52%;background:linear-gradient(90deg,rgba(0,0,0,.9),rgba(0,0,0,0));opacity:calc(.92 - .92*var(--tune,1))}
.rad-eye-t{font-family:'Space Mono',monospace;font-size:.5cqw;letter-spacing:.22em;color:#7a6a52}
.rad-dial{position:relative;height:9cqw;margin-top:2cqw;border-top:1.5px solid #1a1714;border-bottom:1.5px solid #1a1714;background:linear-gradient(#f3ecdb,#e4dbc4);overflow:hidden;cursor:ew-resize;touch-action:none}
.rad-dial:focus-visible{outline:2px solid #1a1714;outline-offset:2px}
.rad-dial .ticks{position:absolute;left:0;right:0;top:0;bottom:0}
.rad-dial .ticks svg{width:100%;height:100%}
.rad-num{position:absolute;top:30%;transform:translateX(-50%);font-family:'Space Mono',monospace;font-size:.62cqw;color:#1a1714;pointer-events:none}
.rad-hint{display:none}
.rad-station{position:absolute;top:.5cqw;transform:translateX(-50%);font-family:'Space Mono',monospace;font-size:.5cqw;letter-spacing:.14em;color:#7c2f22;white-space:nowrap;cursor:pointer;background:none;border:0;padding:0}
.rad-station:hover{text-decoration:underline;text-underline-offset:.25em}
.rad-needle{position:absolute;top:-.4cqw;bottom:-.4cqw;width:.28cqw;background:#c0392b;box-shadow:0 0 .5cqw rgba(192,57,43,.5);transform:translateX(-50%);pointer-events:none}
.rad-needle:before{content:'';position:absolute;left:50%;top:-.5cqw;transform:translateX(-50%);border-left:.55cqw solid transparent;border-right:.55cqw solid transparent;border-top:.8cqw solid #c0392b}
.rad-glass{position:absolute;inset:0;background:linear-gradient(105deg,rgba(255,255,255,.5) 0%,rgba(255,255,255,0) 22%,rgba(255,255,255,0) 76%,rgba(255,255,255,.28) 100%);pointer-events:none}
.rad-readout{display:flex;align-items:baseline;gap:1.6cqw;margin-top:1.2cqw;font-family:'Space Mono',monospace}
.rad-readout .freq{font-size:2.6cqw;letter-spacing:.04em;font-weight:700}
.rad-readout .unit{font-size:.7cqw;letter-spacing:.26em;color:#7a6a52}
.rad-readout .st{font-size:.68cqw;letter-spacing:.24em;text-transform:uppercase;color:#1a1714;min-width:16cqw}
.rad-readout .state{margin-left:auto;font-size:.6cqw;letter-spacing:.2em;text-transform:uppercase;color:#7c2f22;opacity:0;transition:opacity 160ms ease-out}
.rad[data-static="1"] .rad-readout .state{opacity:1}
.rad-programs{display:grid;grid-template-columns:1fr 1fr;gap:1.6cqw;margin-top:1.6cqw;margin-right:8.6cqw}
.rad-card{display:block;border:1.5px solid rgba(26,23,20,.5);border-radius:.4cqw;padding:1.1cqw 1.3cqw;background:rgba(255,255,255,.35);transition:border-color 160ms ease-out,background 160ms ease-out,opacity 160ms ease-out;opacity:.55}
.rad-card.active{opacity:1;border-color:#1a1714;background:#f6f0e2}
.rad-card .no{font-family:'Space Mono',monospace;font-size:.54cqw;letter-spacing:.22em;color:#7c2f22;text-transform:uppercase}
.rad-card h3{font-size:1.5cqw;font-weight:500;letter-spacing:.02em;text-transform:uppercase;margin-top:.4cqw}
.rad-card p{margin-top:.4cqw;font-family:'Space Mono',monospace;font-size:.56cqw;line-height:1.5;color:#5a5142;letter-spacing:.02em}
.rad-card .go{display:inline-block;margin-top:.7cqw;font-family:'Space Mono',monospace;font-size:.54cqw;letter-spacing:.2em;text-transform:uppercase;color:#7c2f22;border-bottom:1px solid rgba(124,47,34,.5);padding-bottom:.15cqw}
.rad-knobs{position:absolute;right:2.4cqw;bottom:2.2cqw;display:flex;gap:1.2cqw}
.rad-knob{width:3.4cqw;height:3.4cqw;border-radius:50%;background:radial-gradient(circle at 35% 30%,#e6cfa4,#b08d57 55%,#6f5730);box-shadow:0 .4cqw .8cqw rgba(0,0,0,.4),inset 0 0 0 2px rgba(40,28,16,.35)}
.rad-knob:after{content:'';position:absolute;left:50%;top:14%;width:.22cqw;height:1.5cqw;background:#292016;transform:translateX(-50%) rotate(var(--a,-30deg));transform-origin:50% 150%}
.rad-serial{display:none;position:absolute;left:2.6cqw;bottom:1.9cqw;font-family:'Space Mono',monospace;font-size:.52cqw;letter-spacing:.22em;text-transform:uppercase;color:#7a6a52}
.rad-foot{position:absolute;left:50%;bottom:.6cqw;transform:translateX(-50%);font-family:'Space Mono',monospace;font-size:.56cqw;letter-spacing:.2em;text-transform:uppercase;color:#8d8677;display:flex;gap:3cqw;white-space:nowrap}
.rad-foot a{color:#8d8677;border-bottom:1px solid rgba(141,134,119,.4);padding-bottom:.15cqw}
.rad-foot a:hover{color:#e9e1cd;border-color:#e9e1cd}
.mobile .rad-cab{left:4cqw;right:4cqw;top:6cqw;height:190cqw;border-radius:3cqw}
.mobile .rad-cab:before{left:-2cqw;right:-2cqw;bottom:-1.6cqw;height:3.4cqw}
.mobile .rad-face{left:2.6cqw;right:2.6cqw;top:3cqw;bottom:3cqw;padding:4cqw 4.4cqw;border-radius:1.6cqw}
.mobile .rad-brand .nm{font-size:9.4cqw}
.mobile .rad-brand .sub{margin-top:1.6cqw;font-size:1.7cqw;letter-spacing:.26em}
.mobile .rad-row1 .right{flex-direction:column;align-items:flex-end;gap:1.6cqw}
.mobile .rad-badge{font-size:1.6cqw;padding:1cqw 1.6cqw;border-width:2px}
.mobile .rad-lamp{font-size:1.7cqw;gap:1.6cqw}
.mobile .rad-lamp i{width:2.8cqw;height:2.8cqw}
.mobile .rad-main{grid-template-columns:1fr;gap:3.4cqw;margin-top:4cqw}
.mobile .rad-grille{height:20cqw;background:repeating-linear-gradient(0deg,#3b332a 0 1.2cqw,#191612 1.2cqw 2.6cqw)}
.mobile .rad-grille .plate{font-size:1.8cqw;padding:1cqw 2.6cqw}
.mobile .rad-tuner{gap:3.4cqw}
.mobile .rad-scope{height:24cqw}
.mobile .rad-eye{width:13cqw;height:13cqw}
.mobile .rad-eye-t{font-size:1.4cqw}
.mobile .rad-dial{height:20cqw;margin-top:3cqw;border-width:2px}
.mobile .rad-station{top:1cqw;font-size:1.35cqw}
.mobile .rad-num{top:30%;font-size:1.35cqw}
.mobile .rad-hint{display:block;flex:1 1 100%;font-size:1.5cqw;letter-spacing:.16em;text-transform:uppercase;color:#7a6a52;margin-top:.4cqw}
.mobile .rad-readout{margin-top:2cqw;gap:2.4cqw;flex-wrap:wrap}
.mobile .rad-readout .freq{font-size:7cqw}
.mobile .rad-readout .unit{font-size:2cqw}
.mobile .rad-readout .st{font-size:1.9cqw;min-width:0;flex:1 1 100%}
.mobile .rad-readout .state{margin-left:0;font-size:1.7cqw}
.mobile .rad-programs{grid-template-columns:1fr;gap:2.2cqw;margin-top:2.4cqw;margin-right:0}
.mobile .rad-card{padding:2.2cqw 2.8cqw;border-width:2px}
.mobile .rad-card .no{font-size:1.5cqw}
.mobile .rad-card h3{font-size:3.8cqw;margin-top:.8cqw}
.mobile .rad-card p{font-size:1.5cqw;margin-top:.8cqw}
.mobile .rad-card .go{font-size:1.45cqw;margin-top:1.2cqw}
.mobile .rad-knobs{display:none}
.mobile .rad-knob{width:9cqw;height:9cqw}
.mobile .rad-knob:after{width:.5cqw;height:3.6cqw}
.mobile .rad-serial{display:block;left:4.4cqw;bottom:4cqw;font-size:1.35cqw}
.mobile .rad-foot{flex-direction:column;gap:1.6cqw;bottom:1.4cqw;font-size:1.5cqw;text-align:center;align-items:center}
"""


def rad_ticks() -> str:
    ticks = []
    for f in range(88, 109):
        pct = 2 + (f - 88) / 20 * 96
        long = f % 2 == 0
        h = 26 if long else 13
        ticks.append(
            f'<line x1="{pct:.2f}%" y1="100%" x2="{pct:.2f}%" y2="{100-h}" stroke="#1a1714" stroke-width="{1.6 if long else .8}"/>'
        )
    return f'<svg viewBox="0 0 1000 100" preserveAspectRatio="none" aria-hidden="true">{"".join(ticks)}</svg>'


def rad_wave() -> str:
    clean = " ".join(
        f"{x},{30 + 16 * math.sin(x / 11):.1f}" for x in range(0, 241, 5)
    )
    rnd = random.Random(4)
    y = 30
    pts = []
    for x in range(0, 241, 5):
        y = max(4, min(56, y + rnd.uniform(-9, 9)))
        pts.append(f"{x},{y:.1f}")
    return f"""<svg viewBox="0 0 240 60" preserveAspectRatio="none" aria-hidden="true">
<polyline class="noise" points="{' '.join(pts)}" fill="none" stroke="#6fae77" stroke-width="1.4" opacity="0"/>
<polyline class="clean" points="{clean}" fill="none" stroke="#9fe08a" stroke-width="1.8"/>
</svg>"""


def rad_body() -> str:
    return f"""
<div class="site rad" data-radio style="--tune:1">
<div class="rad-cab">
  <div class="rad-face">
    <div class="rad-row1">
      <div class="rad-brand"><div class="nm">MusseJusse</div><div class="sub">Superhet &middot; Edge FM</div></div>
      <div class="right">
        <span class="rad-badge">V3.0</span>
        <span class="rad-lamp"><i></i>On air</span>
      </div>
    </div>
    <div class="rad-main">
      <div class="rad-grille"><span class="plate">MJ</span></div>
      <div class="rad-tuner">
        <div class="rad-eye-wrap"><span class="rad-eye"><i></i><b></b></span><span class="rad-eye-t">TUNING</span></div>
        <div class="rad-scope">{rad_wave()}<span class="scan"></span></div>
      </div>
    </div>
    <div class="rad-dial" data-dial tabindex="0" role="slider" aria-label="Tuning dial, 88 to 108 MHz" aria-valuemin="88" aria-valuemax="108" aria-valuenow="91.7">
      <span class="ticks" aria-hidden="true">{rad_ticks()}</span>
      {''.join(f'<span class="rad-num" style="left:{2 + (f-88)/20*96:.2f}%">{f}</span>' for f in range(88,109,2))}
      <button class="rad-station" data-station="91.7" style="left:19.76%">ROUNDEST</button>
      <button class="rad-station" data-station="104.3" style="left:80.24%">MODELS</button>
      <span class="rad-needle" data-needle style="left:22.99%"></span>
      <span class="rad-glass" aria-hidden="true"></span>
    </div>
    <div class="rad-readout">
      <span class="freq" data-freq>91.7</span><span class="unit">MHz</span>
      <span class="st" data-st></span>
      <span class="state">Static &middot; drag to tune</span>
      <span class="rad-hint">Drag the dial to tune</span>
    </div>
    <div class="rad-programs">
      <a class="rad-card c1" href="https://roundest.mussejusse.com">
        <span class="no">Station 91.7 &middot; Next.js</span>
        <h3>Roundest Pok&eacute;mon</h3>
        <p>Which one is rounder? Answered from the edge and cached for the next listener.</p>
        <span class="go">Open station</span>
      </a>
      <a class="rad-card c2" href="https://models.mussejusse.com">
        <span class="no">Station 104.3 &middot; Astro</span>
        <h3>Models</h3>
        <p>Every model, provider and capability, prewritten as pages and shipped as files.</p>
        <span class="go">Open station</span>
      </a>
    </div>
    <span class="rad-serial">Made on the edge &middot; Serial 3.0</span>
    <div class="rad-knobs"><span class="rad-knob" style="--a:-40deg"></span><span class="rad-knob" style="--a:24deg"></span></div>
  </div>
</div>
<div class="rad-foot">
  <span><a href="https://bsky.app/profile/mussejusse.com">Bluesky</a></span>
  <span><a href="https://github.com/MusseJusse">Source on GitHub</a></span>
  <span><a href="https://vercel.com">Hosted on Vercel</a></span>
</div>
</div>"""


RAD_SCRIPT = """<script>
(function(){
  var roots=[].slice.call(document.querySelectorAll('[data-radio]'));
  roots.forEach(function(root){
    var dial=root.querySelector('[data-dial]'), needle=root.querySelector('[data-needle]'),
        freqEl=root.querySelector('[data-freq]'), stEl=root.querySelector('[data-st]'),
        cards=[root.querySelector('.c1'),root.querySelector('.c2')];
    var stations=[{f:91.7,name:'Roundest Pok\u00e9mon',card:cards[0]},{f:104.3,name:'Models',card:cards[1]}];
    var fmin=88,fmax=108,cur=91.7,target=91.7,vel=0,raf=null,dragging=false,lastT=0,lastF=0;
    var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    function clamp(f){return Math.max(fmin,Math.min(fmax,f));}
    function pos(f){return 2+(f-fmin)/(fmax-fmin)*96;}
    function render(){
      needle.style.left=pos(cur)+'%';
      freqEl.textContent=cur.toFixed(1);
      var near=stations[0],d=Math.abs(cur-stations[0].f);
      stations.forEach(function(s){var dd=Math.abs(cur-s.f);if(dd<d){d=dd;near=s;}});
      var t=Math.max(0,Math.min(1,1-d/1.8));
      root.style.setProperty('--tune',t.toFixed(3));
      dial.setAttribute('aria-valuenow',cur.toFixed(1));
      stEl.textContent=t>.6?near.name:'';
      root.dataset.static=t>.6?'0':'1';
      stations.forEach(function(s){s.card.classList.toggle('active',t>.6&&s===near);});
    }
    function step(){
      if(reduce){cur=target;vel=0;render();raf=null;return;}
      var d=target-cur;
      vel+=d*0.09;vel*=0.8;cur+=vel;
      if(Math.abs(target-cur)<0.015&&Math.abs(vel)<0.06){cur=target;vel=0;render();raf=null;return;}
      render();raf=requestAnimationFrame(step);
    }
    function go(f){
      target=clamp(f);
      if(raf)cancelAnimationFrame(raf);
      if(reduce){cur=target;vel=0;render();return;}
      raf=requestAnimationFrame(step);
    }
    function fromEvent(e){
      var r=dial.getBoundingClientRect();
      var p=(e.clientX-r.left)/r.width;
      p=(p-0.02)/0.96;p=Math.max(0,Math.min(1,p));
      return fmin+p*(fmax-fmin);
    }
    dial.addEventListener('pointerdown',function(e){
      dragging=true;vel=0;lastF=fromEvent(e);lastT=performance.now();
      if(dial.setPointerCapture)dial.setPointerCapture(e.pointerId);
      cur=target=lastF;render();e.preventDefault();
    });
    dial.addEventListener('pointermove',function(e){
      if(!dragging)return;
      var now=performance.now(),f=fromEvent(e),dt=now-lastT;
      if(dt>0){vel=(f-lastF)/dt;lastF=f;lastT=now;}
      cur=target=f;render();
    });
    function release(){
      if(!dragging)return;
      dragging=false;
      var near=stations[0],d=99;
      stations.forEach(function(s){var dd=Math.abs(cur-s.f);if(dd<d){d=dd;near=s;}});
      if(d<1.4){go(near.f);return;}
      go(cur+vel*220);
    }
    dial.addEventListener('pointerup',release);
    dial.addEventListener('pointercancel',release);
    dial.addEventListener('keydown',function(e){
      var k=e.key;
      if(k==='ArrowRight'||k==='ArrowUp'){go(target+.2);e.preventDefault();}
      else if(k==='ArrowLeft'||k==='ArrowDown'){go(target-.2);e.preventDefault();}
      else if(k==='Home'){go(fmin);e.preventDefault();}
      else if(k==='End'){go(fmax);e.preventDefault();}
    });
    [].slice.call(root.querySelectorAll('[data-station]')).forEach(function(b){
      b.addEventListener('click',function(e){e.stopPropagation();go(parseFloat(b.dataset.station));});
    });
    render();
  });
})();
</script>"""


# ---------------------------------------------------------------------------
# E / Roundness engine
# ---------------------------------------------------------------------------

MR_CSS = """
.mr{background:
 radial-gradient(120cqw 80cqw at 50% -10%,#f4ecd9 0%,#ece3d0 45%,#e2d7bf 100%);color:#23242a;font-family:Archivo,system-ui,sans-serif}
.mr:before{content:'';position:absolute;inset:1.6cqw;border:1.5px solid #23242a;opacity:.8;pointer-events:none}
.mr:after{content:'';position:absolute;inset:2.2cqw;border:1px solid #23242a;opacity:.35;pointer-events:none}
.mr-top{position:absolute;left:4.5cqw;right:4.5cqw;top:4cqw;display:flex;justify-content:space-between;align-items:flex-start;gap:3cqw;z-index:5}
.mr-title .eyebrow{font-family:'Space Mono',monospace;font-size:.56cqw;letter-spacing:.3em;text-transform:uppercase;color:#8a8f98}
.mr-title h1{margin-top:.8cqw;font-size:3.9cqw;line-height:.95;font-weight:900;letter-spacing:-.035em;text-transform:uppercase;font-stretch:105%}
.mr-title p{margin-top:1cqw;font-size:.95cqw;line-height:1.45;color:#4a4d56;max-width:36cqw}
.mr-ctl{text-align:right;flex:0 0 auto}
.mr-btn{display:inline-flex;align-items:center;gap:.9cqw;border:2px solid #23242a;background:#f0b429;padding:1cqw 1.6cqw;font-family:'Space Mono',monospace;font-size:.66cqw;letter-spacing:.22em;text-transform:uppercase;cursor:pointer;box-shadow:.5cqw .5cqw 0 #23242a;transition:transform 120ms ease-out,box-shadow 120ms ease-out}
.mr-btn:hover{transform:translate(-.1cqw,-.1cqw);box-shadow:.65cqw .65cqw 0 #23242a}
.mr-btn:active{transform:translate(.4cqw,.4cqw);box-shadow:.1cqw .1cqw 0 #23242a}
.mr-btn i{width:.9cqw;height:.9cqw;border-radius:50%;background:#dc4a2f;border:1.5px solid #23242a}
.mr-status{margin-top:1cqw;font-family:'Space Mono',monospace;font-size:.56cqw;letter-spacing:.24em;text-transform:uppercase;color:#6d717b}
.mr[data-run="1"] .mr-status b{color:#dc4a2f}
.mr[data-run="done"] .mr-status b{color:#2f7d4f}
.mr-machine{position:absolute;left:3.6cqw;right:3.6cqw;top:15.4cqw;z-index:3}
.mr-machine svg{width:100%;height:auto;overflow:visible}
.mr-track{fill:none;stroke:#23242a;stroke-width:3}
.mr-rail{fill:none;stroke:#8a8f98;stroke-width:1;opacity:.5}
.mr-anchor{fill:none;stroke:none}
.mr-ball{fill:#dc4a2f;stroke:#23242a;stroke-width:1.6}
.mr-gate{transition:transform 260ms cubic-bezier(.23,1,.32,1)}
.mr[data-run="1"] .mr-gate,.mr[data-run="done"] .mr-gate{transform:translateX(-74px)}
.mr-badge circle{fill:#ece3d0;stroke:#23242a;stroke-width:1.6}
.mr-badge text{font-family:'Space Mono',monospace;font-size:11px;fill:#23242a;text-anchor:middle}
.mr-gear{transform-box:fill-box;transform-origin:50% 50%;animation:mr-spin 24s linear infinite}
@keyframes mr-spin{to{transform:rotate(360deg)}}
.mr-cards{position:absolute;left:4.5cqw;right:28cqw;top:57.8cqw;display:grid;grid-template-columns:repeat(3,1fr);gap:1.4cqw;z-index:6}
.mr-card{position:relative;display:block;border:1.6px solid #23242a;background:#f2ead8;padding:1.1cqw 1.2cqw 1.2cqw;box-shadow:.45cqw .45cqw 0 rgba(35,36,42,.9);transition:background 200ms ease-out,transform 200ms ease-out}
.mr-card .n{position:absolute;top:-1.1cqw;left:1.2cqw;width:2.2cqw;height:2.2cqw;border-radius:50%;background:#ece3d0;border:1.6px solid #23242a;display:flex;align-items:center;justify-content:center;font-family:'Space Mono',monospace;font-size:.62cqw;transition:background 200ms ease-out,color 200ms ease-out}
.mr-card h3{margin-top:.8cqw;font-size:1.35cqw;font-weight:800;letter-spacing:-.01em;text-transform:uppercase}
.mr-card .tags{margin-top:.35cqw;font-family:'Space Mono',monospace;font-size:.5cqw;letter-spacing:.14em;text-transform:uppercase;color:#8a8f98}
.mr-card p{margin-top:.5cqw;font-size:.7cqw;line-height:1.4;color:#4a4d56}
.mr-card .go{display:inline-block;margin-top:.7cqw;font-family:'Space Mono',monospace;font-size:.54cqw;letter-spacing:.2em;text-transform:uppercase;color:#23242a;border-bottom:1.5px solid #23242a;padding-bottom:.15cqw}
.mr-card .pass{position:absolute;top:.8cqw;right:.9cqw;font-family:'Space Mono',monospace;font-size:.5cqw;letter-spacing:.2em;color:#2f7d4f;border:1.5px solid rgba(47,125,79,.7);padding:.2cqw .5cqw;transform:rotate(6deg);opacity:0;transition:opacity 220ms ease-out}
.mr-card.hit{background:#fdf6e4;transform:translate(-.15cqw,-.15cqw)}
.mr-card.hit .n{background:#f0b429}
.mr-card.hit .pass{opacity:1}
.mr-stamp{position:absolute;right:20cqw;top:42cqw;font-family:'Space Mono',monospace;font-size:1.5cqw;letter-spacing:.24em;text-transform:uppercase;color:#dc4a2f;border:3px solid rgba(220,74,47,.8);padding:.5cqw 1.2cqw;transform:rotate(-9deg) scale(.85);opacity:0;transition:opacity 260ms ease-out,transform 320ms cubic-bezier(.23,1,.32,1);z-index:7}
.mr[data-run="done"] .mr-stamp{opacity:1;transform:rotate(-9deg) scale(1)}
.mr-key{position:absolute;left:4.5cqw;right:28cqw;bottom:12.8cqw;z-index:6;display:flex;align-items:baseline;gap:1.6cqw}
.mr-key h4{font-family:'Space Mono',monospace;font-size:.54cqw;letter-spacing:.24em;text-transform:uppercase;color:#8a8f98;font-weight:400}
.mr-key ul{display:flex;gap:1.6cqw;font-family:'Space Mono',monospace;font-size:.5cqw;letter-spacing:.06em;color:#4a4d56}
.mr-key b{color:#23242a;font-weight:400}
.mr-block{position:absolute;right:4.5cqw;bottom:3cqw;border:1.6px solid #23242a;background:#f2ead8;padding:.9cqw 1.1cqw;width:25cqw;z-index:6;font-family:'Space Mono',monospace;font-size:.54cqw;letter-spacing:.08em;line-height:1.7}
.mr-block .r{display:flex;justify-content:space-between;gap:1cqw}
.mr-block .r b{font-weight:400;color:#8a8f98}
.mr-block .hd{font-size:.62cqw;letter-spacing:.2em;text-transform:uppercase;padding-bottom:.5cqw;margin-bottom:.5cqw;border-bottom:1.2px solid #23242a}
.mr-links{position:absolute;left:4.5cqw;bottom:1.2cqw;display:flex;gap:2.4cqw;font-family:'Space Mono',monospace;font-size:.54cqw;letter-spacing:.18em;text-transform:uppercase;color:#6d717b;z-index:6}
.mr-links a{border-bottom:1px solid rgba(109,113,123,.5);padding-bottom:.15cqw}
.mr-links a:hover{color:#23242a;border-color:#23242a}
.mobile .mr:before{inset:2.4cqw}
.mobile .mr:after{inset:3.2cqw;display:none}
.mobile .mr-top{left:7cqw;right:7cqw;top:6cqw;display:block}
.mobile .mr-title .eyebrow{font-size:1.5cqw}
.mobile .mr-title h1{margin-top:1.6cqw;font-size:9.2cqw;letter-spacing:-.03em}
.mobile .mr-title p{margin-top:1.8cqw;font-size:2.3cqw;max-width:none;line-height:1.4}
.mobile .mr-ctl{margin-top:2.6cqw;text-align:left;display:block}
.mobile .mr-btn{font-size:1.7cqw;padding:2.4cqw 3.4cqw;gap:2cqw;border-width:2.5px;box-shadow:1.2cqw 1.2cqw 0 #23242a}
.mobile .mr-btn i{width:2.2cqw;height:2.2cqw}
.mobile .mr-status{margin-top:1.4cqw;font-size:1.45cqw}
.mobile .mr-machine{left:7cqw;right:7cqw;top:55cqw}
.mobile .mr-cards{left:7cqw;right:7cqw;top:154.5cqw;grid-template-columns:1fr;gap:3cqw}
.mobile .mr-card{padding:1.8cqw 2.4cqw 2cqw;box-shadow:.7cqw .7cqw 0 rgba(35,36,42,.9)}
.mobile .mr-card .n{top:-2.4cqw;left:3cqw;width:5cqw;height:5cqw;font-size:1.5cqw;border-width:2px}
.mobile .mr-card h3{margin-top:1cqw;font-size:3.4cqw}
.mobile .mr-card .tags{display:none}
.mobile .mr-card p{margin-top:1.2cqw;font-size:2cqw;line-height:1.35}
.mobile .mr-card .go{margin-top:1.4cqw;font-size:1.4cqw}
.mobile .mr-card .pass{font-size:1.3cqw;padding:.5cqw 1cqw;top:2cqw;right:2.4cqw}
.mobile .mr-stamp{right:40cqw;bottom:auto;top:136cqw;font-size:3.2cqw;border-width:3px}
.mobile .mr-key{display:none}


.mobile .mr-block{display:none}

.mobile .mr-links{left:7cqw;right:7cqw;bottom:2.4cqw;justify-content:space-between;gap:0;font-size:1.4cqw}
"""


def mr_badge(x: int, y: int, n: int) -> str:
    return f'<g class="mr-badge"><circle cx="{x}" cy="{y}" r="9"/><text x="{x}" y="{y+4}">{n}</text></g>'


MR_TRACK_D = "M150 72 C340 96 520 108 640 122 C700 128 730 150 730 166 C730 184 700 196 640 202 C480 216 340 230 220 240 C176 244 168 268 196 282 C232 300 300 306 420 312 C560 320 680 326 760 332 C800 336 830 340 852 346"
MR_TRACK_M = "M250 70 C320 84 360 96 372 112 C394 128 394 148 360 156 C300 168 200 178 148 188 C112 196 108 220 148 230 C220 246 300 252 356 260 C392 266 396 288 356 298 C300 310 220 316 168 328 C128 338 132 362 180 372 C250 386 320 390 372 398 C416 404 444 418 452 436 C458 452 446 466 426 474"

MR_DESK = f"""<div class="mr-machine">
<svg viewBox="0 0 1000 440" aria-hidden="true">
<g stroke="#23242a" stroke-width="2.4" fill="none">
<path d="M60 12 L200 12 L172 58 L88 58 Z" fill="#e2d7bf"/>
<path d="M92 30 L168 30 M98 44 L162 44" stroke-width="1.2" opacity=".5"/>
<line x1="730" y1="166" x2="730" y2="408"/>
<line x1="420" y1="312" x2="420" y2="408"/>
<line x1="760" y1="332" x2="760" y2="408"/>
<line x1="420" y1="312" x2="730" y2="166" stroke-width="1" opacity=".28"/>
<line x1="760" y1="332" x2="730" y2="166" stroke-width="1" opacity=".28"/>
<line x1="140" y1="408" x2="880" y2="408" stroke-width="5"/>
<path d="M150 408 L166 424 M230 408 L246 424 M310 408 L326 424 M390 408 L406 424 M470 408 L486 424 M550 408 L566 424 M630 408 L646 424 M710 408 L726 424 M790 408 L806 424 M860 408 L876 424" stroke-width="1.4" opacity=".45"/>
</g>
<path class="mr-rail" d="{MR_TRACK_D}" transform="translate(0,13)"/>
<path class="mr-track" d="{MR_TRACK_D}"/>
<g class="mr-gate"><line x1="112" y1="66" x2="182" y2="66" stroke="#23242a" stroke-width="5"/><circle cx="112" cy="66" r="4" fill="#23242a"/></g>
<g class="mr-gear" stroke="#23242a" stroke-width="1.4" fill="none"><circle cx="788" cy="152" r="34" stroke-dasharray="3 4"/><circle cx="834" cy="172" r="22" stroke-dasharray="2.5 3.5"/></g>
<g stroke="#23242a" fill="#e2d7bf" stroke-width="1.8">
<circle cx="788" cy="152" r="26"/>
<circle cx="834" cy="172" r="17"/>
<path d="M178 308 L214 308 L196 286 Z" fill="#f0b429"/>
<line x1="162" y1="286" x2="230" y2="294" stroke-width="4"/>
<path d="M790 334 a 26 26 0 0 1 52 0 z"/>
<line x1="816" y1="334" x2="816" y2="322"/>
<circle cx="816" cy="338" r="4" fill="#23242a"/>
<path d="M820 330 L940 330 L932 372 L828 372 Z" fill="#e2d7bf"/>
</g>
<text x="880" y="392" text-anchor="middle" font-family="'Space Mono',monospace" font-size="12" letter-spacing="3" fill="#23242a">SHIPPED</text>
<text x="130" y="8" text-anchor="middle" font-family="'Space Mono',monospace" font-size="11" letter-spacing="2" fill="#8a8f98">IDEAS IN</text>
<g class="mr-badge"><circle cx="128" cy="30" r="9"/><text x="128" y="34">1</text></g>
<g class="mr-badge"><circle cx="190" cy="72" r="9"/><text x="190" y="76">2</text></g>
<g class="mr-badge"><circle cx="420" cy="104" r="9"/><text x="420" y="108">3</text></g>
<g class="mr-badge"><circle cx="160" cy="318" r="9"/><text x="160" y="322">4</text></g>
<g class="mr-badge"><circle cx="836" cy="122" r="9"/><text x="836" y="126">5</text></g>
<g class="mr-badge"><circle cx="866" cy="306" r="9"/><text x="866" y="310">6</text></g>
<g class="mr-badge"><circle cx="800" cy="388" r="9"/><text x="800" y="392">7</text></g>
<circle class="mr-anchor" data-mr-anchor="0" cx="520" cy="106" r="1"/>
<circle class="mr-anchor" data-mr-anchor="1" cx="788" cy="152" r="1"/>
<circle class="mr-anchor" data-mr-anchor="2" cx="852" cy="346" r="1"/>
<circle class="mr-ball" cx="150" cy="72" r="8.5"/>
</svg>
</div>
<div class="mr-cards">
<a class="mr-card" data-mr-card="0" href="https://roundest.mussejusse.com"><span class="n">01</span><span class="pass">Passed</span><h3>Roundest Pok&eacute;mon</h3><div class="tags">Next.js / server actions / KV</div><p>Two creatures, one question, sorted by roundness.</p><span class="go">Open experiment</span></a>
<a class="mr-card" data-mr-card="1" href="https://models.mussejusse.com"><span class="n">02</span><span class="pass">Passed</span><h3>Models</h3><div class="tags">Astro / static output</div><p>Every model and provider, flattened into prewritten pages.</p><span class="go">Open experiment</span></a>
<a class="mr-card" data-mr-card="2" href="https://github.com/MusseJusse"><span class="n">03</span><span class="pass">Passed</span><h3>Elsewhere</h3><div class="tags">GitHub / Bluesky / Vercel</div><p>The exits. Where the machinery lives between runs.</p><span class="go">Leave the sheet</span></a>
</div>"""

MR_MOB = f"""<div class="mr-machine">
<svg viewBox="0 0 500 560" aria-hidden="true">
<g stroke="#23242a" stroke-width="2.6" fill="none">
<path d="M180 14 L320 14 L296 58 L204 58 Z" fill="#e2d7bf"/>
<line x1="205" y1="32" x2="295" y2="32" stroke-width="1.2" opacity=".5"/>
<line x1="394" y1="140" x2="394" y2="520"/>
<line x1="150" y1="230" x2="150" y2="520"/>
<line x1="392" y1="290" x2="392" y2="520"/>
<line x1="150" y1="230" x2="394" y2="140" stroke-width="1" opacity=".3"/>
<line x1="394" y1="140" x2="392" y2="290" stroke-width="1" opacity=".3"/>
<line x1="70" y1="520" x2="440" y2="520" stroke-width="5"/>
<path d="M90 520 L104 534 M160 520 L174 534 M230 520 L244 534 M300 520 L314 534 M370 520 L384 534 M420 520 L434 534" stroke-width="1.4" opacity=".45"/>
</g>
<path class="mr-rail" d="{MR_TRACK_M}" transform="translate(0,13)"/>
<path class="mr-track" d="{MR_TRACK_M}"/>
<g class="mr-gate"><line x1="222" y1="64" x2="282" y2="64" stroke="#23242a" stroke-width="5"/><circle cx="222" cy="64" r="4" fill="#23242a"/></g>
<g class="mr-gear" stroke="#23242a" stroke-width="1.4" fill="none"><circle cx="430" cy="160" r="26" stroke-dasharray="3 4"/></g>
<g stroke="#23242a" fill="#e2d7bf" stroke-width="2">
<circle cx="430" cy="160" r="20"/>
<path d="M132 250 L166 250 L149 272 Z" fill="#f0b429"/>
<line x1="120" y1="246" x2="180" y2="256" stroke-width="4"/>
<path d="M420 452 a 24 24 0 0 1 48 0 z"/><line x1="444" y1="452" x2="444" y2="440"/>
<path d="M382 486 L470 486 L462 522 L390 522 Z" fill="#e2d7bf"/>
</g>
<text x="250" y="8" text-anchor="middle" font-family="'Space Mono',monospace" font-size="12" letter-spacing="2" fill="#8a8f98">IDEAS IN</text>
<text x="425" y="540" text-anchor="middle" font-family="'Space Mono',monospace" font-size="12" letter-spacing="3" fill="#23242a">SHIPPED</text>
<g class="mr-badge"><circle cx="250" cy="26" r="10"/><text x="250" y="30">1</text></g>
<g class="mr-badge"><circle cx="300" cy="70" r="10"/><text x="300" y="74">2</text></g>
<g class="mr-badge"><circle cx="394" cy="112" r="10"/><text x="394" y="116">3</text></g>
<g class="mr-badge"><circle cx="120" cy="252" r="10"/><text x="120" y="256">4</text></g>
<g class="mr-badge"><circle cx="466" cy="140" r="10"/><text x="466" y="144">5</text></g>
<g class="mr-badge"><circle cx="408" cy="436" r="10"/><text x="408" y="440">6</text></g>
<g class="mr-badge"><circle cx="366" cy="502" r="10"/><text x="366" y="506">7</text></g>
<circle class="mr-anchor" data-mr-anchor="0" cx="300" cy="86" r="1"/>
<circle class="mr-anchor" data-mr-anchor="1" cx="430" cy="160" r="1"/>
<circle class="mr-anchor" data-mr-anchor="2" cx="440" cy="470" r="1"/>
<circle class="mr-ball" cx="250" cy="70" r="8.5"/>
</svg>
</div>
<div class="mr-cards">
<a class="mr-card" data-mr-card="0" href="https://roundest.mussejusse.com"><span class="n">01</span><span class="pass">Passed</span><h3>Roundest Pok&eacute;mon</h3><div class="tags">Next.js / server actions / KV</div><p>Two creatures, one question, sorted by roundness.</p><span class="go">Open experiment</span></a>
<a class="mr-card" data-mr-card="1" href="https://models.mussejusse.com"><span class="n">02</span><span class="pass">Passed</span><h3>Models</h3><div class="tags">Astro / static output</div><p>Every model and provider, flattened into prewritten pages.</p><span class="go">Open experiment</span></a>
<a class="mr-card" data-mr-card="2" href="https://github.com/MusseJusse"><span class="n">03</span><span class="pass">Passed</span><h3>Elsewhere</h3><div class="tags">GitHub / Bluesky / Vercel</div><p>The exits. Where the machinery lives between runs.</p><span class="go">Leave the sheet</span></a>
</div>"""

def mr_body() -> str:
    return f"""
<div class="site mr" data-run="0">
<div class="mr-top">
  <div class="mr-title">
    <div class="eyebrow">Sheet 1 of 1 &middot; drawn to scale</div>
    <h1>The roundness<br>engine</h1>
    <p>Drop the ball. It passes every experiment on the way down.</p>
  </div>
  <div class="mr-ctl">
    <button class="mr-btn" data-mr-drop><i></i><span data-mr-label>Drop the ball</span></button>
    <div class="mr-status">Status: <b data-mr-status>Waiting at the gate</b></div>
  </div>
</div>
<!--d-->{MR_DESK}<!--/d-->
<!--m-->{MR_MOB}<!--/m-->
<div class="mr-stamp">Shipped &middot; est. 2024</div>
<div class="mr-key">
  <h4>Parts key</h4>
  <ul><li><b>1</b> Hopper</li><li><b>2</b> Gate</li><li><b>3</b> Ramps</li><li><b>4</b> Lever</li><li><b>5</b> Gears</li><li><b>6</b> Bell</li><li><b>7</b> Tray</li></ul>
</div>
<div class="mr-block">
  <div class="hd">Fig. 1 / Roundness engine</div>
  <div class="r"><b>Drawn by</b><span>MJ</span></div>
  <div class="r"><b>Checked by</b><span>Nobody</span></div>
  <div class="r"><b>Scale</b><span>1 : 1 with reality</span></div>
  <div class="r"><b>Sheet</b><span>1 of 1</span></div>
</div>
<div class="mr-links">
  <a href="https://bsky.app/profile/mussejusse.com">Bluesky</a>
  <a href="https://github.com/MusseJusse">Source on GitHub</a>
  <a href="https://vercel.com">Hosted on Vercel</a>
</div>
</div>"""


MR_SCRIPT = """<script>
(function(){
  var roots=[].slice.call(document.querySelectorAll('.mr'));
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  roots.forEach(function(root){
    var path=root.querySelector('.mr-track'), ball=root.querySelector('.mr-ball'),
        btn=root.querySelector('[data-mr-drop]'), label=root.querySelector('[data-mr-label]'),
        status=root.querySelector('[data-mr-status]'), L=path.getTotalLength();
    var base=L/3.4;
    var anchors=[].slice.call(root.querySelectorAll('[data-mr-anchor]')).map(function(a){
      var cx=parseFloat(a.getAttribute('cx')),cy=parseFloat(a.getAttribute('cy'));
      var best=0,bd=1e9;
      for(var i=0;i<=L;i+=4){
        var p=path.getPointAtLength(i),d=(p.x-cx)*(p.x-cx)+(p.y-cy)*(p.y-cy);
        if(d<bd){bd=d;best=i;}
      }
      return best;
    });
    var cards=anchors.map(function(_,i){return root.querySelector('[data-mr-card="'+i+'"]');});
    var s=0,v=0,running=false,last=0,hit=[false,false,false],tPrev=0;
    function setBall(x,y){ball.setAttribute('cx',x.toFixed(1));ball.setAttribute('cy',y.toFixed(1));}
    function place(f){var p=path.getPointAtLength(f);setBall(p.x,p.y);}
    function reset(){
      running=false;s=0;v=0;hit=[false,false,false];
      root.dataset.run='0';cards.forEach(function(c){c.classList.remove('hit');});
      place(0);label.textContent='Drop the ball';status.textContent='Waiting at the gate';
    }
    function finish(){
      running=false;root.dataset.run='done';label.textContent='Run it again';
      status.textContent='Shipped, 2024 to 2026';
      cards.forEach(function(c){c.classList.add('hit');});
      place(L);
    }
    function frame(now){
      var dt=Math.min(.032,(now-last)/1000);last=now;
      if(!dt)dt=.016;
      var a=path.getPointAtLength(Math.min(L,s+2)),b=path.getPointAtLength(Math.max(0,s-2));
      var slope=Math.max(-1,Math.min(1,(a.y-b.y)/4));
      var tv=base*(1+slope*.8);
      v+=(tv-v)*Math.min(1,4*dt);
      v=Math.max(base*.4,Math.min(base*1.9,v));
      s+=v*dt;
      if(s>=L){place(L);finish();return;}
      place(s);
      for(var i=0;i<anchors.length;i++){
        if(!hit[i]&&s>=anchors[i]-4){
          hit[i]=true;
          if(cards[i])cards[i].classList.add('hit');
          status.textContent=(i===0?'Rolling':i===1?'Rolling, 200+ entries':'Almost shipped');
        }
      }
      if(running)requestAnimationFrame(frame);
    }
    function drop(){
      if(running)return;
      hit=[false,false,false];cards.forEach(function(c){c.classList.remove('hit');});
      root.dataset.run='1';label.textContent='Rolling';status.textContent='Rolling';
      if(reduce){
        running=false;
        cards.forEach(function(c,i){setTimeout(function(){c.classList.add('hit');},140*i);});
        setTimeout(function(){place(L);finish();},140*cards.length+180);
        return;
      }
      s=0;v=0;running=true;
      setTimeout(function(){if(running){last=performance.now();requestAnimationFrame(frame);}},200);
    }
    btn.addEventListener('click',function(){
      if(root.dataset.run==='done'){reset();return;}
      drop();
    });
    place(0);
  });
})();
</script>"""


GDEFS = """<svg class="gdefs" width="0" height="0" aria-hidden="true" focusable="false"><defs>
<clipPath id="obsClip" clipPathUnits="objectBoundingBox"><circle cx=".5" cy=".5" r=".5"/></clipPath>
<marker id="ahCobalt" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1 L9 5 L0 9 z" fill="#1c3f9e"/></marker>
<marker id="ahSage" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1 L9 5 L0 9 z" fill="#33402f"/></marker>
<marker id="ahPrint" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1 L9 5 L0 9 z" fill="#1a1714"/></marker>
<pattern id="hatchSage" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(42)"><line x1="0" y1="0" x2="0" y2="7" stroke="#33402f" stroke-width="1" opacity=".5"/></pattern>
<pattern id="hatchCobalt" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(42)"><line x1="0" y1="0" x2="0" y2="7" stroke="#1c3f9e" stroke-width="1" opacity=".45"/></pattern>
<pattern id="hatchGraphite" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(42)"><line x1="0" y1="0" x2="0" y2="7" stroke="#23242a" stroke-width="1" opacity=".4"/></pattern>
</defs></svg>"""


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


DIRECTIONS = [
    ("A", "Observatory", "A working night chart. Two objects, plotted and labelled. Hover either one to open its card; the field twinkles the whole time.", OBS_CSS, obs_body()),
    ("B", "Field guide", "Two specimens on one plate page. Hover a plate and its field marks appear annotated at the margins, the way a bird guide would mark them.", FG_CSS, fg_body()),
    ("C", "Lab notebook", "The two projects as logged experiments, with a spread, graphs, a stamp and a third entry still in progress. Hover the figures.", LAB_CSS, lab_body()),
    ("D", "Radio", "A table radio tuned to two stations. Drag the dial; the needle has momentum, the scope clears, the magic eye opens, and each station lights its card.", RAD_CSS, rad_body()),
    ("E", "Roundness engine", "A drawing of a machine that ships things. Press the button, watch the ball take the whole track, and the experiments stamp themselves as it passes.", MR_CSS, mr_body()),
]


def build() -> None:
    sections = []
    site_css = []
    nav = []
    for letter, name, desc, css, body in DIRECTIONS:
        nav.append(f'<a href="#{letter}">{letter}</a>')
        site_css.append(css)
        sections.append(
            f'<section class="direction" id="{letter}"><div class="dhead"><span class="letter">{letter}</span>'
            f"<h3>{name}</h3><p>{desc}</p></div><div class=\"views\">{site_pair(body)}</div></section>"
        )
    html = (
        "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
        "<title>MusseJusse / five new directions</title>"
        f"<style>{FONTS}{SHELL_CSS}{''.join(site_css)}</style></head><body>{GDEFS}"
        "<header class=\"top\"><div class=\"row\"><strong>MusseJusse / five new directions</strong>"
        f"<span class=\"meta\">Round three</span><nav class=\"nav\" aria-label=\"Directions\">{''.join(nav)}</nav></div></header>"
        "<main class=\"wrap\"><div class=\"intro\"><span class=\"k\">Five full pages, desktop and mobile</span>"
        "<h2>Same homepage, five different worlds.</h2>"
        "<p>Every direction is a working page, not a picture. Hover, drag and press the parts that move. "
        "Desktop sits next to mobile on each row. Pick one whole, or point at the pieces you want merged.</p></div>"
        + "".join(sections)
        + "</main><footer class=\"wrap foot\"><span>MusseJusse, 2026. Mockups only, nothing here ships as drawn.</span>"
        "<span><a href=\"https://roundest.mussejusse.com\">Roundest Pok&eacute;mon</a> &middot; "
        "<a href=\"https://models.mussejusse.com\">Models</a></span></footer>" + RAD_SCRIPT + MR_SCRIPT + "</body></html>"
    )
    out = ROOT / "round-three-directions.html"
    out.write_text(html)
    kb = out.stat().st_size / 1024
    assert out.stat().st_size < 512 * 1024, f"too big: {kb:.0f} KB"
    print(f"{out} written, {kb:.1f} KB")


if __name__ == "__main__":
    build()
