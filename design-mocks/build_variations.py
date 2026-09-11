"""Build a focused review doc with three variations of H (code review) and three of E (transit).

Reuses the embedded fonts, stage, chrome and interaction script from build_redesign_mocks.
"""

from pathlib import Path

from build_redesign_mocks import (
    FONT_CSS, STAGE_CSS, CHROME_CSS, INTERACT, a, GH, BS, R, M, GHM, BSM,
)

ROOT = Path(__file__).resolve().parent

# ================================================================ A / Review

REVIEW_CSS = """
.rv{background:#0e0f13;color:#e6e6e6;padding:2.8cqw 3cqw;font-family:"Space Mono",monospace;overflow:hidden}
.rv-top{position:relative;z-index:3;display:flex;justify-content:space-between;align-items:center;font-size:.72cqw;color:#9aa0ab;border-bottom:1px solid #23262e;padding-bottom:1.1cqw}
.rv-top .repo{display:flex;align-items:center;gap:1cqw;color:#e6e6e6}
.rv-top .chip{color:#3fb950;border:1px solid #2ea04366;background:#3fb9501a;padding:.15cqw .7cqw;border-radius:1cqw;font-size:.66cqw}
.rv-tabs{position:relative;z-index:3;display:flex;gap:2.2cqw;margin-top:1cqw;font-size:.74cqw;color:#9aa0ab;border-bottom:1px solid #23262e;padding-bottom:1cqw}
.rv-tabs .on{color:#e6e6e6;border-bottom:2px solid #f78166;margin-bottom:-1.02cqw;padding-bottom:1cqw}
.rv-body{position:absolute;left:3cqw;right:3cqw;top:12.6cqw;bottom:3cqw;z-index:3;display:grid;grid-template-columns:15cqw 1fr 21cqw;gap:1.4cqw}
.rv-tree{border:1px solid #23262e;border-radius:.6cqw;background:#12141a;padding:1cqw;font-size:.7cqw;color:#9aa0ab}
.rv-tree .h{color:#e6e6e6;font-size:.72cqw}
.rv-tree .f{display:flex;justify-content:space-between;color:#e6e6e6;padding:.5cqw .6cqw;background:#1b1e26;border-radius:.35cqw;margin-top:.7cqw}
.rv-diff{border:1px solid #23262e;border-radius:.6cqw;background:#0b0d11;overflow:hidden}
.rv-diff .fh{display:flex;justify-content:space-between;padding:.8cqw 1cqw;border-bottom:1px solid #23262e;color:#9aa0ab;font-size:.7cqw}
.rv-diff .ln{display:grid;grid-template-columns:2.4cqw 2.4cqw 1.6cqw 1fr;font-size:.82cqw;line-height:1.95;align-items:baseline;padding:0 .8cqw}
.rv-diff .ln .old,.rv-diff .ln .new{color:#6b717c;text-align:right;padding-right:.9cqw}
.rv-diff .ln .sg{color:#6b717c}
.rv-diff .code{white-space:pre;overflow:hidden;text-overflow:ellipsis;color:#c8cdd6}
.rv-diff .ln.add{background:rgba(63,185,80,.13)}
.rv-diff .ln.add .code{color:#7ee787}
.rv-diff .ln.del{background:rgba(248,81,73,.12)}
.rv-diff .ln.del .code{color:#ffa198}
.rv-diff .ln:hover{outline:1px solid #1f6feb;background:#0d1b2e}
.rv-side{display:flex;flex-direction:column;gap:1.4cqw;min-height:0}
.rv-thread{border:1px solid #23262e;border-radius:.6cqw;background:#12141a;padding:1.1cqw;font-family:"Space Grotesk",sans-serif}
.rv-thread .who{font-family:"Space Mono",monospace;font-size:.64cqw;color:#9aa0ab;margin-bottom:.5cqw;display:flex;justify-content:space-between}
.rv-thread .msg{font-size:.82cqw;line-height:1.5;color:#d6d9df}
.rv-thread .resolved{font-family:"Space Mono",monospace;font-size:.6cqw;color:#3fb950;border:1px solid #2ea04366;padding:.2cqw .6cqw;border-radius:1cqw;display:inline-block;margin-top:.7cqw}
.rv-merge{border:1px solid #23262e;border-radius:.6cqw;background:#12141a;padding:1.1cqw;font-family:"Space Grotesk",sans-serif}
.rv-merge h4{font-size:.9cqw;color:#e6e6e6;font-weight:600}
.rv-merge p{font-size:.72cqw;color:#9aa0ab;margin-top:.5cqw;line-height:1.5}
.rv-merge .btns{display:grid;gap:.7cqw;margin-top:1cqw}
.rv-merge .btn{text-align:center;padding:.7cqw;border-radius:.5cqw;font-size:.76cqw;font-weight:600}
.rv-merge .btn.go{background:#238636;color:#fff}
.rv-merge .btn.no{background:#21262d;color:#f85149;border:1px solid #f8514955}
.rv-foot{position:absolute;left:3cqw;right:3cqw;bottom:1.4cqw;display:flex;justify-content:space-between;font-size:.66cqw;color:#6b717c;z-index:3}
.mobile .rv{padding:5cqw}
.mobile .rv-top{font-size:2cqw;flex-wrap:wrap;gap:2cqw}
.mobile .rv-tabs{font-size:2cqw;gap:5cqw}
.mobile .rv-body{position:static;grid-template-columns:1fr;gap:4cqw;margin-top:5cqw}
.mobile .rv-tree{font-size:1.9cqw}
.mobile .rv-tree .h,.mobile .rv-tree .f{font-size:1.9cqw}
.mobile .rv-diff .ln{grid-template-columns:5cqw 5cqw 4cqw 1fr;font-size:2.3cqw;line-height:2.15;padding:0 2cqw}
.mobile .rv-diff .fh{font-size:1.9cqw;padding:2cqw 2.4cqw}
.mobile .rv-thread .msg{font-size:2.6cqw}
.mobile .rv-thread .who{font-size:1.8cqw}
.mobile .rv-thread .resolved{font-size:1.7cqw}
.mobile .rv-merge h4{font-size:3cqw}
.mobile .rv-merge p{font-size:2.3cqw}
.mobile .rv-merge .btn{font-size:2.5cqw;padding:2.4cqw}
.mobile .rv-foot{position:static;margin-top:6cqw;font-size:1.8cqw;flex-direction:column;gap:1.2cqw}
"""

RV_LINES = [
    ("ctx", "1", "1", " ", 'name: "MusseJusse"'),
    ("del", "2", "2", "-", 'role: "student"'),
    ("add", "3", "2", "+", 'role: "builds for the web"'),
    ("ctx", "3", "3", " ", "experiments:"),
    ("add", "4", "4", "+", '  - name: "Roundest Pok&eacute;mon"'),
    ("add", "5", "5", "+", '    stack: "Next.js"'),
    ("add", "6", "6", "+", '  - name: "Models"'),
    ("add", "7", "7", "+", '    stack: "Astro"'),
    ("del", "4", "8", "-", "hobbies: []"),
    ("add", "9", "9", "+", 'hobbies: ["watches", "the web"]'),
    ("ctx", "5", "10", " ", 'status: "always building, never finished"'),
]
_rv_rows = "".join(
    '<div class="ln %s"><span class="old">%s</span><span class="new">%s</span><span class="sg">%s</span><span class="code">%s</span></div>'
    % (k, o, n, s, c)
    for (k, o, n, s, c) in RV_LINES
)

REVIEW = (
    '<div class="site rv">'
    '<header class="rv-top"><span class="repo">mussejusse / mussejusse.com &middot; <span class="chip">Open</span>'
    " &middot; PR #1</span><span>GitHub &middot; Bluesky</span></header>"
    '<nav class="rv-tabs"><span>Conversation</span><span>Commits</span><span>Checks</span><span class="on">Files changed</span></nav>'
    '<div class="rv-body">'
    '<aside class="rv-tree"><span class="h">Files (1)</span><div class="f"><span>mussejusse</span><span>+8 -2</span></div></aside>'
    '<div class="rv-diff"><div class="fh"><span>b/mussejusse</span><span>+8 -2</span></div>' + _rv_rows + "</div>"
    '<div class="rv-side">'
    '<div class="rv-thread"><div class="who"><span>reviewer / bsky</span><span>2m ago</span></div>'
    '<div class="msg">Nice. One nit: the status line should never change. Everything else looks right.</div>'
    '<span class="resolved">&#10003; Resolved</span></div>'
    '<div class="rv-merge"><h4>All checks passed</h4>'
    '<p>This branch has no conflicts with the base branch. 2 deploy previews are ready.</p>'
    '<div class="btns"><span class="btn go">Squash and merge</span><span class="btn no">Request changes</span></div></div>'
    "</div></div>"
    '<footer class="rv-foot"><span>1 approving review / 0 changes requested</span><span>merged 3 days later</span></footer>'
    "</div>"
)

# ================================================================ B / History

HISTORY_CSS = """
.hist{background:#0a0c14;color:#d7dbe6;padding:3cqw 4cqw;overflow:hidden}
.hist-top{position:relative;z-index:4;display:flex;justify-content:space-between;font-family:"Space Mono",monospace;font-size:.72cqw;color:#8b93a1;letter-spacing:.1em}
.hist-top nav{display:flex;gap:2.4cqw}
.hist-graph{position:absolute;left:3.4cqw;right:3.4cqw;top:10cqw;bottom:4cqw;z-index:2;display:grid;grid-template-columns:12cqw 1fr;gap:1.6cqw}
.hist-svgwrap{position:relative}
.hist-svg{position:absolute;inset:0;width:100%;height:100%}
.hist-rows{position:relative;display:grid;align-content:start}
.hist .row{position:relative;display:grid;grid-template-columns:8cqw 1fr auto;gap:1.4cqw;align-items:center;padding:.9cqw 1cqw;border-bottom:1px solid #151a26;font-family:"Space Mono",monospace;font-size:.78cqw}
.hist .row .hash{color:#5d6c8a}
.hist .row .sub{color:#8b93a1}
.hist .row .msg{color:#d7dbe6}
.hist .row .sub2{font-size:.68cqw;color:#6b7688;font-family:"Space Grotesk",sans-serif}
.hist .row .tags{display:flex;gap:.6cqw}
.hist .row .tag{font-size:.62cqw;border:1px solid;padding:.15cqw .6cqw;border-radius:1cqw}
.hist .row .tag.rel{color:#ffd166;border-color:#ffd16666}
.hist .row .tag.head{color:#3fb950;border-color:#3fb95066}
.hist .row:hover{background:#111522}
.hist .row:hover .detail{opacity:1;transform:none}
.hist .detail{position:absolute;right:0;top:100%;z-index:5;width:34cqw;background:#121724;border:1px solid #232c40;border-radius:.6cqw;padding:1cqw;opacity:0;transform:translateY(.4cqw);transition:opacity .16s ease-out,transform .16s ease-out;font-family:"Space Grotesk",sans-serif;pointer-events:none}
.hist .detail b{font-family:"Space Mono",monospace;font-size:.66cqw;color:#3fb950}
.hist .detail p{font-size:.78cqw;color:#aab3c2;margin-top:.4cqw;line-height:1.5}
.hist-foot{position:absolute;left:4cqw;right:4cqw;bottom:1.4cqw;display:flex;justify-content:space-between;font-family:"Space Mono",monospace;font-size:.66cqw;color:#6b7688;z-index:4}
.hist svg text{font-family:"Space Mono",monospace}
.mobile .hist{padding:6cqw}
.mobile .hist-top{font-size:2cqw}
.mobile .hist-graph{position:static;grid-template-columns:1fr;gap:3cqw;margin-top:6cqw}
.mobile .hist-svgwrap{display:none}
.mobile .hist .row{grid-template-columns:1fr auto;gap:1.5cqw;font-size:2.1cqw;padding:3cqw 0}
.mobile .hist .row .hash{display:none}
.mobile .hist .row .msg{font-size:2.6cqw}
.mobile .hist .row .sub2{font-size:1.9cqw;grid-column:1}
.mobile .hist .detail{position:static;opacity:1;transform:none;width:auto;margin-top:2cqw;font-size:2.2cqw;pointer-events:auto}
.mobile .hist .detail b{font-size:1.8cqw}
.mobile .hist .detail p{font-size:2.3cqw}
.mobile .hist-foot{position:static;margin-top:7cqw;font-size:1.9cqw}
"""

HIST_ROWS = [
    ("abc4012", "chore: never finish", "Musse", "2 hours ago", ["HEAD", "main"], "The status line stays exactly as written. This commit is rewritten daily."),
    ("def3891", "Merge branch 'feature/models'", "Musse", "1 day ago", [], "Models joins main. Astro, content collections, 200+ entries."),
    ("7782aa0", "feat: add Models", "Musse", "1 day ago", ["models-v1.0"], "A catalogue of every model, provider and capability."),
    ("c1a9f44", "Merge branch 'feature/roundest'", "Musse", "3 days ago", [], "Roundest Pokémon joins main. Server actions, KV cache."),
    ("90ab123", "feat: add Roundest Pok&eacute;mon", "Musse", "3 days ago", ["roundest-v1.0"], "Two Pokémon, one roundness question, answered instantly."),
    ("5f2c001", "feat: scaffold the site", "Musse", "6 days ago", [], "Astro, one page, almost nothing else."),
    ("0000000", "init: curiosity", "Musse", "12 years ago", ["origin"], "Where every build starts."),
]


def _hist_row(i, row):
    h, msg, who, when, tags, detail = row
    taghtml = "".join(
        '<span class="tag %s">%s</span>' % ("head" if t in ("HEAD", "main", "origin") else "rel", t)
        for t in tags
    )
    return (
        '<div class="row" style="z-index:%d"><span class="hash">%s</span>'
        '<span><span class="msg">%s</span> <span class="sub2">%s &middot; %s</span></span>'
        '<span class="tags">%s</span>'
        '<div class="detail"><b>%s</b><p>%s</p></div></div>'
    ) % (60 - i, h, msg, who, when, taghtml, h, detail)


_hist_rows = "".join(_hist_row(i, r) for i, r in enumerate(HIST_ROWS))

HISTORY = (
    '<div class="site hist">'
    '<header class="hist-top"><span>mussejusse / git log --graph</span><nav>' + GHM + " " + BSM + "</nav></header>"
    '<div class="hist-graph">'
    '<div class="hist-svgwrap"><svg class="hist-svg" viewBox="0 0 120 700" preserveAspectRatio="none" aria-hidden="true">'
    '<path d="M30 50 L30 650" stroke="#2f81f7" stroke-width="3" fill="none"/>'
    '<path d="M30 250 C30 290,70 290,70 320 L70 430 C70 460,30 460,30 500" stroke="#ffd166" stroke-width="3" fill="none"/>'
    '<path d="M30 90 C30 130,70 130,70 160 L70 210 C70 240,30 240,30 270" stroke="#56d364" stroke-width="3" fill="none"/>'
    '<g>'
    '<circle cx="30" cy="50" r="7" fill="#3fb950"/>'
    '<circle cx="30" cy="160" r="6" fill="#ffd166"/><circle cx="30" cy="270" r="6" fill="#2f81f7"/>'
    '<circle cx="30" cy="360" r="6" fill="#56d364"/><circle cx="30" cy="470" r="6" fill="#2f81f7"/>'
    '<circle cx="30" cy="560" r="6" fill="#56d364"/><circle cx="30" cy="640" r="6" fill="#8b93a1"/>'
    '</g></svg></div>'
    '<div class="hist-rows">' + _hist_rows + "</div></div>"
    '<footer class="hist-foot"><span>7 commits / 3 branches / 2 releases</span><span>HEAD -&gt; main</span></footer>'
    "</div>"
)

# ================================================================ C / Pipeline

PIPELINE_CSS = """
.pipe{background:#0a0d12;color:#e6e9ee;padding:3cqw 4cqw;overflow:hidden}
.pipe-top{position:relative;z-index:4;display:flex;justify-content:space-between;align-items:center;font-family:"Space Mono",monospace;font-size:.72cqw;color:#8b93a1}
.pipe-top nav{display:flex;gap:2.4cqw}
.pipe-stages{position:absolute;left:4cqw;right:4cqw;top:15cqw;z-index:3;display:grid;grid-template-columns:repeat(6,1fr);gap:1.6cqw}
.pipe .stage{position:relative;border:1px solid #1b212b;border-radius:.8cqw;background:#10141a;padding:1.3cqw}
.pipe .stage .ic{width:2.4cqw;height:2.4cqw;border-radius:50%;display:grid;place-content:center;font-size:1.1cqw;border:1px solid #2a323d;color:#8b93a1}
.pipe .stage.done .ic{color:#3fb950;border-color:#2ea04366;background:#3fb95014}
.pipe .stage.run .ic{color:#58a6ff;border-color:#1f6feb66;background:#1f6feb14;animation:spinpulse 1.6s ease-in-out infinite}
.pipe .stage h4{font-family:"Space Grotesk",sans-serif;font-weight:600;font-size:1cqw;margin-top:.8cqw}
.pipe .stage .dur{font-family:"Space Mono",monospace;font-size:.62cqw;color:#8b93a1;margin-top:.3cqw}
.pipe .stage:not(:first-child):before{content:"";position:absolute;left:-1.6cqw;top:2.6cqw;width:1.6cqw;height:.14cqw;background:#1b212b}
.pipe-logs{position:absolute;left:4cqw;right:4cqw;top:31cqw;height:15cqw;border:1px solid #1b212b;border-radius:.8cqw;background:#070a0e;padding:1.3cqw;overflow:hidden;font-family:"Space Mono",monospace;font-size:.76cqw;line-height:1.85;color:#8b93a1;z-index:3}
.pipe-logs .ok{color:#3fb950}
.pipe-logs .info{color:#58a6ff}
.pipe-logs .dim{color:#5d6875}
.pipe-logs .cur{display:inline-block;width:.6cqw;height:1.1cqw;background:#e6e9ee;vertical-align:-.15cqw;animation:blink 1.05s steps(1) infinite}
.pipe-deploys{position:absolute;left:4cqw;right:4cqw;bottom:6cqw;z-index:3;display:grid;grid-template-columns:1fr 1fr;gap:2cqw}
.pipe .env{border:1px solid #1b212b;border-radius:.8cqw;background:#10141a;padding:1.2cqw 1.4cqw;display:flex;justify-content:space-between;align-items:center}
.pipe .env .mono{font-family:"Space Mono",monospace;font-size:.62cqw;color:#8b93a1;letter-spacing:.1em}
.pipe .env h4{font-family:"Space Grotesk",sans-serif;font-weight:600;font-size:1.3cqw;margin-top:.3cqw}
.pipe .env .u{font-family:"Space Mono",monospace;font-size:.66cqw;color:#58a6ff}
.pipe .env .badge{font-family:"Space Mono",monospace;font-size:.64cqw;color:#3fb950;border:1px solid #2ea04366;background:#3fb95014;padding:.2cqw .7cqw;border-radius:1cqw}
.pipe-foot{position:absolute;left:4cqw;right:4cqw;bottom:2cqw;display:flex;justify-content:space-between;font-family:"Space Mono",monospace;font-size:.66cqw;color:#6b7688;z-index:4}
@keyframes spinpulse{0%,100%{transform:scale(.92);opacity:.6}50%{transform:scale(1.05);opacity:1}}
@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}
.mobile .pipe{padding:6cqw}
.mobile .pipe-top{font-size:2cqw}
.mobile .pipe-stages{position:static;grid-template-columns:1fr 1fr;gap:3cqw;margin-top:7cqw}
.mobile .pipe .stage{padding:3cqw}
.mobile .pipe .stage .ic{width:7cqw;height:7cqw;font-size:3.2cqw}
.mobile .pipe .stage h4{font-size:2.9cqw;margin-top:1.6cqw}
.mobile .pipe .stage .dur{font-size:1.8cqw}
.mobile .pipe .stage:not(:first-child):before{display:none}
.mobile .pipe-logs{position:static;margin-top:5cqw;height:auto;font-size:2.1cqw;line-height:2;padding:3cqw}
.mobile .pipe-logs .cur{width:1.6cqw;height:3cqw}
.mobile .pipe-deploys{position:static;margin-top:5cqw;grid-template-columns:1fr;gap:3cqw}
.mobile .pipe .env{padding:3cqw}
.mobile .pipe .env .mono{font-size:1.7cqw}
.mobile .pipe .env h4{font-size:3.4cqw}
.mobile .pipe .env .u{font-size:1.9cqw}
.mobile .pipe .env .badge{font-size:1.7cqw}
.mobile .pipe-foot{position:static;margin-top:6cqw;font-size:1.8cqw;flex-direction:column;gap:1.2cqw}
"""


def _stage(icon, name, dur, cls, pct):
    return (
        '<section class="stage %s"><span class="ic">%s</span><h4>%s</h4><span class="dur">%s</span></section>'
        % (cls, icon, name, dur)
    )


PIPELINE = (
    '<div class="site pipe">'
    '<header class="pipe-top"><span>pipelines / mussejusse &middot; #42 &middot; <span style="color:#3fb950">&#10003; passed</span></span>'
    "<nav>" + GHM + " " + BSM + "</nav></header>"
    '<div class="pipe-stages">'
    + _stage("&#10003;", "Checkout", "4s", "done", 100)
    + _stage("&#10003;", "Install", "31s", "done", 100)
    + _stage("&#10003;", "Typecheck", "12s", "done", 100)
    + _stage("&#10003;", "Build", "48s", "done", 100)
    + _stage("&#10227;", "Test", "running", "run", 60)
    + _stage("&#8226;", "Deploy", "queued", "", 0)
    + "</div>"
    '<div class="pipe-logs">'
    '<div class="dim">$ astro build</div>'
    '<div class="info">&#9656; building client (vite)</div>'
    '<div class="ok">&#10003; 1 page(s) built in 0.81s</div>'
    '<div class="ok">&#10003; Complete!</div>'
    '<div class="info">&#9656; uploading artefacts</div>'
    '<div class="dim">$ vitest run <span class="cur"></span></div>'
    "</div>"
    '<div class="pipe-deploys">'
    '<div class="env"><span><span class="mono">PRODUCTION / EXP 01</span><h4>Roundest Pok&eacute;mon</h4><span class="u">roundest.mussejusse.com</span></span><span class="badge">Live</span></div>'
    '<div class="env"><span><span class="mono">PRODUCTION / EXP 02</span><h4>Models</h4><span class="u">models.mussejusse.com</span></span><span class="badge">Live</span></div>'
    "</div>"
    '<footer class="pipe-foot"><span>run 42 / main / 9f3a1c2</span><span>2 environments / always building</span></footer>'
    "</div>"
)

# ================================================================ D / Night

NIGHT_CSS = """
.night{background:#07080c;color:#dbe6f0;padding:3cqw 4cqw;overflow:hidden}
.night:before{content:"";position:absolute;inset:0;background:radial-gradient(60% 50% at 50% 30%,#12203a,transparent 70%)}
.night-top{position:relative;z-index:4;display:flex;justify-content:space-between;align-items:center;font-family:"Space Mono",monospace;font-size:.72cqw;color:#7f8ea6}
.night-top nav{display:flex;gap:2.4cqw}
.night-title{position:absolute;left:4cqw;top:9.5cqw;z-index:3;font-family:"Space Grotesk",sans-serif;font-weight:700;font-size:5.4cqw;line-height:1;letter-spacing:-.03em;text-transform:uppercase;color:#eaf2ff;text-shadow:0 0 3cqw rgba(120,180,255,.5)}
.night-map{position:absolute;left:4cqw;right:4cqw;top:27cqw;height:16cqw;z-index:3}
.night-rail{position:absolute;left:0;right:0;top:50%;height:.5cqw;border-radius:.3cqw;background:#4aa3ff;box-shadow:0 0 1.4cqw #4aa3ff,0 0 4cqw rgba(74,163,255,.6)}
.night-st{position:absolute;top:50%;transform:translate(-50%,-50%);width:1.8cqw;height:1.8cqw;border-radius:50%;background:#07080c;border:.4cqw solid #4aa3ff;z-index:3;box-shadow:0 0 1.2cqw rgba(74,163,255,.8)}
.night-st.major{width:2.4cqw;height:2.4cqw;border-color:#ffd166;box-shadow:0 0 1.6cqw rgba(255,209,102,.9)}
.night-st .nm{position:absolute;left:50%;top:-2.4cqw;transform:translateX(-50%);white-space:nowrap;font-family:"Space Grotesk",sans-serif;font-weight:600;font-size:.9cqw;text-transform:uppercase;color:#cfe0f5}
.night-st.down .nm{top:auto;bottom:-2.4cqw}
.night-st .cl{position:absolute;left:50%;top:3.2cqw;transform:translate(-50%,.4cqw);opacity:0;width:14cqw;background:#0c1220;border:1px solid #21304a;border-radius:.5cqw;padding:.9cqw;transition:opacity .16s ease-out,transform .16s ease-out;font-family:"Space Grotesk",sans-serif;pointer-events:none;text-align:left;white-space:normal;z-index:6}
.night-st.down .cl{top:auto;bottom:3.2cqw}
.night-st:hover .cl,.night-st:focus-visible .cl{opacity:1;transform:translate(-50%,0);pointer-events:auto}
.night-st .cl b{font-family:"Space Mono",monospace;font-size:.6cqw;color:#ffd166}
.night-st .cl h4{font-size:1cqw;color:#eaf2ff;margin-top:.3cqw}
.night-st .cl p{font-size:.7cqw;color:#93a6c0;margin-top:.3cqw;line-height:1.4}
.night-st.s1{left:4%}.night-st.s2{left:17%}.night-st.s3{left:30%}.night-st.s4{left:43%}
.night-st.s5{left:57%}.night-st.s6{left:70%}.night-st.s7{left:83%}.night-st.s8{left:96%}
.night-train{position:absolute;top:50%;left:4%;transform:translate(-50%,-50%);width:3.4cqw;height:1.6cqw;border-radius:.5cqw;background:#eaf2ff;box-shadow:0 0 1.4cqw #9fd0ff,0 0 4cqw #4aa3ff;z-index:4;animation:ride 16s ease-in-out infinite}
.night-train:before{content:"";position:absolute;right:100%;top:50%;transform:translateY(-50%);width:10cqw;height:.2cqw;background:linear-gradient(90deg,transparent,#9fd0ff);opacity:.7}
.night-board{position:absolute;left:4cqw;right:4cqw;bottom:8cqw;z-index:3;border:1px solid #2a2136;border-radius:.6cqw;background:#0a0805;padding:1.2cqw 1.4cqw}
.night-board .cap{display:flex;justify-content:space-between;font-family:"Space Mono",monospace;font-size:.62cqw;color:#c58b2e;letter-spacing:.22em;border-bottom:1px solid #2a2136;padding-bottom:.8cqw}
.night-board .dep{display:grid;grid-template-columns:2.4cqw 1fr 8cqw 6cqw;gap:1.2cqw;font-family:"Space Mono",monospace;font-size:.8cqw;color:#ffb454;padding:.55cqw 0;text-shadow:0 0 1cqw rgba(255,180,84,.6)}
.night-board .dep .t{color:#ffd166}
.night-board .dep.dim{color:#7a5a24;text-shadow:none}
.night-board .dep.blink{animation:depblink 2.4s steps(1) infinite}
.night-foot{position:absolute;left:4cqw;right:4cqw;bottom:2cqw;display:flex;justify-content:space-between;font-family:"Space Mono",monospace;font-size:.66cqw;color:#5d6880;z-index:3}
@keyframes depblink{0%,70%{opacity:1}71%,100%{opacity:.35}}
.mobile .night{padding:6cqw}
.mobile .night-top{font-size:2cqw}
.mobile .night-title{position:static;font-size:11cqw;margin-top:8cqw}
.mobile .night-map{position:relative;left:auto;right:auto;top:auto;height:auto;margin:10cqw 0 0}
.mobile .night-rail{left:1.4cqw;top:0;bottom:0;width:.6cqw;height:auto}
.mobile .night-st{position:relative;left:auto;top:auto;transform:none;margin:0 0 13cqw 0;width:2.4cqw;height:2.4cqw}
.mobile .night-st.major{width:3.2cqw;height:3.2cqw}
.mobile .night-st .nm{left:6cqw;top:50%;transform:translateY(-50%);bottom:auto;font-size:3.4cqw}
.mobile .night-st.down .nm{top:50%}
.mobile .night-st .cl{left:6cqw;top:4cqw;width:64cqw;transform:translate(0,.4cqw)}
.mobile .night-st.down .cl{top:4cqw;bottom:auto}
.mobile .night-st .cl b{font-size:1.8cqw}.mobile .night-st .cl h4{font-size:3.4cqw}.mobile .night-st .cl p{font-size:2.4cqw}
.mobile .night-train{left:1.4cqw;top:0;transform:translate(-50%,0);width:5cqw;height:2.4cqw;animation-name:ridev}
.mobile .night-train:before{display:none}
.mobile .night-board{position:static;margin-top:6cqw;padding:3cqw}
.mobile .night-board .cap{font-size:1.8cqw;padding-bottom:2cqw}
.mobile .night-board .dep{grid-template-columns:6cqw 1fr 16cqw 12cqw;font-size:2.4cqw;gap:2cqw;padding:1.6cqw 0}
.mobile .night-foot{position:static;margin-top:6cqw;font-size:1.8cqw}
@keyframes ride{0%{left:4%}7%{left:17%}9%{left:17%}20%{left:30%}23%{left:30%}34%{left:43%}37%{left:43%}49%{left:57%}52%{left:57%}64%{left:70%}67%{left:70%}79%{left:83%}82%{left:83%}93%{left:96%}97%{left:96%}100%{left:4%}}
@keyframes ridev{0%{top:0}7%{top:13%}9%{top:13%}20%{top:26%}23%{top:26%}34%{top:39%}37%{top:39%}49%{top:52%}52%{top:52%}64%{top:65%}67%{top:65%}79%{top:78%}82%{top:78%}93%{top:91%}97%{top:91%}100%{top:0}}
"""


def _nst(cls, name, down, major, callout):
    k = "night-st " + cls + (" down" if down else "") + (" major" if major else "")
    return '<span class="%s"><span class="nm">%s</span><span class="cl">%s</span></span>' % (k, name, callout)


NIGHT = (
    '<div class="site night">'
    '<header class="night-top"><span>MUSSEJUSSE / LAST TRAIN</span><nav>' + GHM + " " + BSM + "</nav></header>"
    '<h1 class="night-title">The night<br>line runs.</h1>'
    '<div class="night-map"><span class="night-rail" aria-hidden="true"></span>'
    + _nst("s1", "HELLO", False, True, '<b>DEPARTS 00:00</b><h4>You are here</h4><p>Every build starts at the first stop.</p>')
    + _nst("s2", "FIRST COMMIT", True, False, '<b>DEPARTS 00:06</b><h4>Curiosity</h4><p>The urge to make something.</p>')
    + _nst("s3", "ROUNDEST POK&Eacute;MON", False, True, '<b>NEXT / PLATFORM 1</b><h4>Roundest Pok&eacute;mon</h4><p>Next.js, server actions, one round question.</p>')
    + _nst("s4", "SERVER ACTIONS", True, False, '<b>DEPARTS 02:41</b><h4>Fetch</h4><p>Ask the server, keep it instant.</p>')
    + _nst("s5", "MODELS", False, True, '<b>NEXT / PLATFORM 2</b><h4>Models</h4><p>Astro, the whole catalogue.</p>')
    + _nst("s6", "ASTRO", True, False, '<b>DEPARTS 04:18</b><h4>Islands</h4><p>Ship almost no JavaScript.</p>')
    + _nst("s7", "CACHE", False, False, '<b>DEPARTS 05:02</b><h4>Cache</h4><p>Never ask twice.</p>')
    + _nst("s8", "ALWAYS BUILDING", True, True, '<b>TERMINUS</b><h4>Never finished</h4><p>The line keeps running.</p>')
    + '<span class="night-train" aria-hidden="true"></span></div>'
    '<div class="night-board"><div class="cap"><span>DEPARTURES / LIVE</span><span>HH:MM:SS</span></div>'
    '<div class="dep blink"><span class="t">01</span><span>ROUNDEST POK&Eacute;MON</span><span>PLATFORM 1</span><span class="t">1 min</span></div>'
    '<div class="dep"><span class="t">02</span><span>MODELS</span><span>PLATFORM 2</span><span class="t">4 min</span></div>'
    '<div class="dep dim"><span>03</span><span>ALWAYS BUILDING</span><span>TERMINUS</span><span>-- min</span></div>'
    "</div>"
    '<footer class="night-foot"><span>LINE 2 / NIGHT SERVICE / RUNS ALWAYS</span><span>SOURCE ON GITHUB</span></footer>'
    "</div>"
)

# ================================================================ E / Planner

PLANNER_CSS = """
.plan{background:#eef2f7;color:#0b1736;padding:3cqw 4cqw;overflow:hidden;font-family:"Space Grotesk",sans-serif}
.plan-top{position:relative;z-index:4;display:flex;justify-content:space-between;align-items:center;font-family:"Space Mono",monospace;font-size:.72cqw;color:#5b6b86}
.plan-top .brand{display:flex;align-items:center;gap:1cqw;font-family:"Space Grotesk",sans-serif;font-weight:700;font-size:1.5cqw;color:#0b1736}
.plan-top .brand i{width:2.2cqw;height:2.2cqw;border-radius:.5cqw;background:#0b57d0;color:#fff;display:grid;place-content:center;font-family:"Space Mono";font-size:.9cqw;font-style:normal}
.plan-top nav{display:flex;gap:2.4cqw}
.plan-search{position:absolute;left:4cqw;top:10cqw;width:38cqw;z-index:3;display:grid;grid-template-columns:1fr auto;gap:.8cqw}
.plan-field{background:#fff;border:1px solid #d5ddea;border-radius:.7cqw;padding:1cqw 1.2cqw;display:flex;justify-content:space-between;align-items:center}
.plan-field span{font-family:"Space Mono",monospace;font-size:.62cqw;color:#7c8aa5;letter-spacing:.1em;display:block}
.plan-field b{font-size:1.1cqw;font-weight:600}
.plan-field.to{margin-top:.8cqw}
.plan-go{background:#0b57d0;color:#fff;border-radius:.7cqw;padding:0 1.6cqw;display:grid;place-content:center;font-weight:600;font-size:.9cqw}
.plan-route{position:absolute;left:4cqw;top:24cqw;width:52cqw;z-index:3;background:#fff;border:1px solid #d5ddea;border-radius:1cqw;padding:1.6cqw 1.8cqw}
.plan-route .sum{display:flex;justify-content:space-between;align-items:baseline;border-bottom:1px solid #e7ecf4;padding-bottom:1.1cqw}
.plan-route .sum h2{font-size:2.4cqw;font-weight:700;letter-spacing:-.02em}
.plan-route .sum span{font-family:"Space Mono",monospace;font-size:.7cqw;color:#5b6b86}
.plan-leg{display:grid;grid-template-columns:4.4cqw 1fr auto;gap:1.2cqw;padding:1.1cqw 0;border-bottom:1px solid #eef2f8;align-items:center}
.plan-leg .ic{width:3.4cqw;height:3.4cqw;border-radius:.6cqw;display:grid;place-content:center;font-size:1.2cqw;color:#fff}
.plan-leg .ic.walk{background:#8a97ab}.plan-leg .ic.ride{background:#0b57d0}.plan-leg .ic.xfer{background:#ffb300;color:#3a2a00}.plan-leg .ic.arrive{background:#0f9d58}
.plan-leg h3{font-size:1.1cqw;font-weight:600}
.plan-leg p{font-family:"Space Mono",monospace;font-size:.66cqw;color:#5b6b86;margin-top:.3cqw}
.plan-leg .t{font-family:"Space Mono",monospace;font-size:.74cqw;color:#0b1736}
.plan-leg a{color:#0b57d0}
.plan-map{position:absolute;right:4cqw;top:10cqw;bottom:8cqw;width:34cqw;z-index:3;border:1px solid #d5ddea;border-radius:1cqw;background:linear-gradient(160deg,#e8eef7,#dbe4f0);overflow:hidden}
.plan-map .lbl{position:absolute;left:1.4cqw;top:1.2cqw;font-family:"Space Mono",monospace;font-size:.62cqw;color:#5b6b86;letter-spacing:.12em}
.plan-map svg{position:absolute;inset:0;width:100%;height:100%}
.plan-foot{position:absolute;left:4cqw;right:4cqw;bottom:2.2cqw;display:flex;justify-content:space-between;font-family:"Space Mono",monospace;font-size:.66cqw;color:#7c8aa5;z-index:4}
.mobile .plan{padding:6cqw}
.mobile .plan-top{font-size:2cqw}
.mobile .plan-top .brand{font-size:4.4cqw}
.mobile .plan-search{position:static;width:auto;margin-top:8cqw}
.mobile .plan-field b{font-size:3.4cqw}
.mobile .plan-field span{font-size:1.8cqw}
.mobile .plan-go{font-size:2.6cqw}
.mobile .plan-route{position:static;width:auto;margin-top:6cqw;padding:4cqw}
.mobile .plan-route .sum h2{font-size:6cqw}
.mobile .plan-route .sum span{font-size:1.9cqw}
.mobile .plan-leg{grid-template-columns:11cqw 1fr auto;gap:3cqw;padding:3cqw 0}
.mobile .plan-leg .ic{width:9cqw;height:9cqw;font-size:3.4cqw;border-radius:1.6cqw}
.mobile .plan-leg h3{font-size:3.4cqw}
.mobile .plan-leg p{font-size:1.9cqw;margin-top:.6cqw}
.mobile .plan-leg .t{font-size:2.1cqw}
.mobile .plan-map{position:static;width:auto;height:70cqw;margin-top:6cqw}
.mobile .plan-foot{position:static;margin-top:6cqw;font-size:1.8cqw;flex-direction:column;gap:1.2cqw}
"""


def _leg(ic, icls, title, sub, dur, href=None):
    t = ('<a href="%s">%s</a>' % (href, dur)) if href else dur
    return (
        '<div class="plan-leg"><span class="ic %s">%s</span>'
        "<span><h3>%s</h3><p>%s</p></span><span class=\"t\">%s</span></div>"
        % (icls, ic, title, sub, t)
    )


PLANNER = (
    '<div class="site plan">'
    '<header class="plan-top"><span class="brand"><i>MJ</i>MusseJusse Planner</span><nav>' + GHM + " " + BSM + "</nav></header>"
    '<div class="plan-search">'
    '<div><div class="plan-field"><span>FROM</span><b>You</b></div>'
    '<div class="plan-field to"><span>TO</span><b>Always Building</b></div></div>'
    '<div class="plan-go">Plan</div></div>'
    '<div class="plan-route"><div class="sum"><h2>1 change &middot; 12 years</h2><span>LEAVE NOW</span></div>'
    + _leg("&#8226;", "walk", "Start at Hello", "Departs every morning", "00:00")
    + _leg("&#9654;", "ride", "Ride Line 2", "Toward Always Building", "4 stops")
    + _leg("&#8644;", "xfer", "Change at Roundest Pok&eacute;mon", "Next.js, server actions", "platform 1", R)
    + _leg("&#9654;", "ride", "Ride Line 2", "Toward the terminus", "2 stops")
    + _leg("&#8644;", "xfer", "Change at Models", "Astro, content collections", "platform 2", M)
    + _leg("&#10003;", "arrive", "Arrive: Always Building", "Never finished", "07:12")
    + "</div>"
    '<div class="plan-map"><span class="lbl">ROUTE / LIVE</span><svg viewBox="0 0 340 560" preserveAspectRatio="xMidYMid meet" aria-hidden="true">'
    '<path d="M60 60 L60 500" stroke="#0b57d0" stroke-width="8" fill="none" stroke-linecap="round"/>'
    '<path d="M60 230 L200 230" stroke="#ffb300" stroke-width="6" fill="none" stroke-dasharray="12 10"/>'
    '<path d="M60 360 L210 360" stroke="#ffb300" stroke-width="6" fill="none" stroke-dasharray="12 10"/>'
    '<g font-family="Space Mono, monospace" font-size="15" fill="#0b1736">'
    '<circle cx="60" cy="60" r="12" fill="#fff" stroke="#0b57d0" stroke-width="7"/>'
    '<text x="82" y="66">HELLO</text>'
    '<circle cx="60" cy="230" r="16" fill="#0b1736"/>'
    '<text x="86" y="236">ROUNDEST</text>'
    '<circle cx="60" cy="360" r="16" fill="#0b1736"/>'
    '<text x="86" y="366">MODELS</text>'
    '<circle cx="60" cy="500" r="14" fill="#fff" stroke="#0f9d58" stroke-width="7"/>'
    '<text x="82" y="506">ALWAYS BUILDING</text>'
    '</g></svg></div>'
    '<footer class="plan-foot"><span>FARES / FREE FOREVER</span><span>NO TIMETABLE / RUNS ALWAYS</span></footer>'
    "</div>"
)

# ================================================================ F / Network

NETWORK_CSS = """
.net{background:#f7f6f1;color:#141414;padding:3cqw 4cqw;overflow:hidden}
.net-top{position:relative;z-index:4;display:flex;justify-content:space-between;align-items:center;font-family:"Space Mono",monospace;font-size:.72cqw;letter-spacing:.1em;color:#6b6b60}
.net-top nav{display:flex;gap:2.4cqw}
.net-title{position:absolute;left:4cqw;top:9.5cqw;z-index:3;font-family:"Space Grotesk",sans-serif;font-weight:700;font-size:4.6cqw;line-height:1;letter-spacing:-.03em;text-transform:uppercase}
.net-map{position:absolute;left:4cqw;top:22cqw;width:62cqw;height:40cqw;z-index:2}
.net-map svg{width:100%;height:100%;overflow:visible}
.net-map .v{transition:opacity .18s ease-out}
.net-map .ln{fill:none;stroke-linecap:round;stroke-linejoin:round}
.net-map .l1{stroke:#e2231a;stroke-width:1.6cqw}
.net-map .l2{stroke:#0b57d0;stroke-width:1.6cqw}
.net-map .l3{stroke:#0f9d58;stroke-width:1.6cqw}
.net-map .st{fill:#f7f6f1;stroke:#141414;stroke-width:.5cqw}
.net-map .st.major{fill:#141414;stroke:#f7f6f1;stroke-width:.6cqw}
.net-map .conn{stroke:#141414;stroke-width:1.1cqw;fill:none}
.net-map text{font-family:"Space Grotesk",sans-serif;font-weight:600;font-size:2.3cqw;fill:#141414}
.net-map text.sm{font-family:"Space Mono",monospace;font-weight:400;font-size:1.7cqw;fill:#6b6b60}
.net-map text.rd{fill:#e2231a}.net-map text.bl{fill:#0b57d0}.net-map text.gr{fill:#0f9d58}
.net-legend{position:absolute;right:4cqw;top:22cqw;width:26cqw;z-index:4;border:1px solid #141414;background:#f7f6f1;padding:1.4cqw}
.net-legend .cap{font-family:"Space Mono",monospace;font-size:.62cqw;letter-spacing:.18em;color:#6b6b60;border-bottom:1px solid #d8d5cb;padding-bottom:.8cqw}
.net-legend .lg{display:flex;align-items:center;gap:1cqw;padding:.9cqw 0;border-bottom:1px solid #ece9e0;cursor:pointer}
.net-legend .lg:last-child{border-bottom:0}
.net-legend .lg i{width:2.4cqw;height:.7cqw;border-radius:.4cqw;flex:0 0 auto}
.net-legend .lg.l1 i{background:#e2231a}.net-legend .lg.l2 i{background:#0b57d0}.net-legend .lg.l3 i{background:#0f9d58}
.net-legend .lg span{font-family:"Space Grotesk",sans-serif;font-weight:600;font-size:.95cqw}
.net-legend .lg em{font-family:"Space Mono",monospace;font-size:.62cqw;color:#6b6b60;margin-left:auto;font-style:normal}
.net:has(.lg.l1:hover) .v:not(.l1){opacity:.1}
.net:has(.lg.l2:hover) .v:not(.l2){opacity:.1}
.net:has(.lg.l3:hover) .v:not(.l3){opacity:.1}
.net:has(.lg.l1:hover) .legend-note.l1,.net:has(.lg.l2:hover) .legend-note.l2,.net:has(.lg.l3:hover) .legend-note.l3{opacity:1}
.net-note{position:absolute;right:4cqw;bottom:6cqw;width:26cqw;z-index:4;border:1px solid #141414;background:#141414;color:#f7f6f1;padding:1.2cqw}
.net-note .mono{font-family:"Space Mono",monospace;font-size:.62cqw;letter-spacing:.16em;color:#b9b6ad}
.net-note h4{font-family:"Space Grotesk",sans-serif;font-weight:700;font-size:1.4cqw;margin-top:.4cqw}
.net-note p{font-size:.76cqw;color:#cfcdc5;margin-top:.4cqw;line-height:1.45}
.net-foot{position:absolute;left:4cqw;right:4cqw;bottom:2.2cqw;display:flex;justify-content:space-between;font-family:"Space Mono",monospace;font-size:.66cqw;color:#6b6b60;z-index:4}
.mobile .net{padding:6cqw}
.mobile .net-top{font-size:2cqw}
.mobile .net-title{position:static;font-size:10cqw;margin-top:6cqw}
.mobile .net-map{position:relative;left:auto;top:auto;width:auto;height:auto;margin-top:6cqw}
.mobile .net-map svg{height:auto}
.mobile .net-map text{font-size:5.4cqw}.mobile .net-map text.sm{font-size:3.9cqw}
.mobile .net-map .l1,.mobile .net-map .l2,.mobile .net-map .l3{stroke-width:4cqw}
.mobile .net-map .conn{stroke-width:3cqw}
.mobile .net-legend{position:static;width:auto;margin-top:6cqw;padding:4cqw}
.mobile .net-legend .cap{font-size:1.8cqw;padding-bottom:2cqw}
.mobile .net-legend .lg{padding:2.4cqw 0}
.mobile .net-legend .lg i{width:7cqw;height:2cqw}
.mobile .net-legend .lg span{font-size:3cqw}
.mobile .net-legend .lg em{font-size:1.8cqw}
.mobile .net-note{position:static;width:auto;margin-top:6cqw;padding:4cqw}
.mobile .net-note .mono{font-size:1.8cqw}
.mobile .net-note h4{font-size:4cqw}
.mobile .net-note p{font-size:2.5cqw}
.mobile .net-foot{position:static;margin-top:6cqw;font-size:1.8cqw;flex-direction:column;gap:1.2cqw}
"""

NETWORK = (
    '<div class="site net">'
    '<header class="net-top"><span>MUSSEJUSSE / SYSTEM MAP</span><nav>' + GHM + " " + BSM + "</nav></header>"
    '<h1 class="net-title">The whole<br>network.</h1>'
    '<div class="net-map"><svg viewBox="0 0 620 400" preserveAspectRatio="xMidYMid meet" aria-label="Schematic network map">'
    '<g class="v l3"><path class="ln" d="M40 110 L580 110"/></g>'
    '<g class="v l1"><path class="ln" d="M40 200 L580 200"/></g>'
    '<g class="v l2"><path class="ln" d="M40 290 L580 290"/></g>'
    '<g class="v l1 l2 l3"><path class="conn" d="M170 110 L170 290"/></g>'
    '<g class="v l3"><circle class="st" cx="300" cy="110" r="7"/><circle class="st" cx="450" cy="110" r="7"/></g>'
    '<g class="v l1"><circle class="st" cx="300" cy="200" r="7"/><circle class="st" cx="450" cy="200" r="7"/></g>'
    '<g class="v l2"><circle class="st" cx="300" cy="290" r="7"/><circle class="st" cx="450" cy="290" r="7"/></g>'
    '<g class="v l1 l2 l3"><circle class="st" cx="170" cy="110" r="7"/><circle class="st" cx="170" cy="290" r="7"/><circle class="st major" cx="170" cy="200" r="14"/></g>'
    '<text class="sm gr" x="44" y="99">BUILD LINE</text>'
    '<text class="sm rd" x="44" y="189">ROUNDEST LINE</text>'
    '<text class="sm bl" x="44" y="279">MODELS LINE</text>'
    '<text x="576" y="99" text-anchor="end">ALWAYS BUILDING</text>'
    '<text x="576" y="189" text-anchor="end">ROUNDEST POK&Eacute;MON</text>'
    '<text x="576" y="279" text-anchor="end">MODELS</text>'
    '<text class="sm" x="188" y="236">MUSSEJUSSE / INTERCHANGE</text>'
    "</svg></div>"
    '<aside class="net-legend"><div class="cap">THREE LINES / ONE BUILDER</div>'
    '<div class="lg l1"><i></i><span>Roundest Line</span><em>NEXT.JS</em></div>'
    '<div class="lg l2"><i></i><span>Models Line</span><em>ASTRO</em></div>'
    '<div class="lg l3"><i></i><span>Build Line</span><em>ALWAYS</em></div></aside>'
    '<div class="net-note"><span class="mono">INTERCHANGE / LIVE</span>'
    "<h4>All lines meet at MusseJusse.</h4><p>Hover a line in the legend to trace it through the network.</p></div>"
    '<footer class="net-foot"><span>SYSTEM MAP / 2026</span><span>ALL LINES RUN ALWAYS</span></footer>'
    "</div>"
)

DIRECTIONS = [
    ("A", "Review", "H, taken to the code host: a three-pane pull request with a real diff, a resolved review thread, and a merge box.", REVIEW_CSS, REVIEW),
    ("B", "History", "H, taken to git log --graph: a branching commit history where the two projects are tagged releases you can hover.", HISTORY_CSS, HISTORY),
    ("C", "Pipeline", "H, taken to the CI run: a stage pipeline with live logs and two deployed environments.", PIPELINE_CSS, PIPELINE),
    ("D", "Night", "E, taken to the last train: a glowing night line with a live departures board that counts down to each project.", NIGHT_CSS, NIGHT),
    ("E", "Planner", "E, taken to a journey planner: a from/to search and a step-by-step itinerary with the projects as interchanges.", PLANNER_CSS, PLANNER),
    ("F", "Network", "E, taken to a full system map: three lines meeting at one interchange, with a legend you can hover to trace.", NETWORK_CSS, NETWORK),
]


def section(letter, title, desc, css, markup):
    views = "".join(
        '<div class="view %s"><div class="vlabel"><b>%s</b><span>%s</span></div>'
        '<div class="canvas">%s</div></div>' % (kind, kind.capitalize(), size, markup)
        for kind, size in [("desktop", "1440 &times; 1000"), ("mobile", "390 &times; 844")]
    )
    prefix = ""
    if letter == "A":
        prefix = '<div class="revdivider"><span>H-BASED / THE CODE WORLD</span></div>'
    if letter == "D":
        prefix = '<div class="revdivider"><span>E-BASED / THE TRANSIT WORLD</span></div>'
    return (
        prefix
        + '<section class="direction" id="%s">'
        '<header class="dhead"><span class="letter">%s</span><h2>%s / %s</h2><p>%s</p></header>'
        '<div class="views">%s</div></section>'
    ) % (letter, letter, letter, title, desc, views)


def build():
    var_css = "".join(d[3] for d in DIRECTIONS)
    sections = "".join(section(*d) for d in DIRECTIONS)
    nav = "".join('<a href="#%s">%s</a>' % (d[0], d[0]) for d in DIRECTIONS)
    html = (
        '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        "<title>MusseJusse / H and E studies</title>"
        "<style>" + FONT_CSS + STAGE_CSS + CHROME_CSS + var_css + "</style>"
        "</head><body>"
        '<div class="rtop"><div class="row"><h1>MusseJusse / H and E studies</h1>'
        "<span>six directions &middot; desktop + mobile</span>"
        '<nav class="rnav" aria-label="Directions">' + nav + "</nav></div></div>"
        '<div class="wrap">'
        '<header class="intro"><span class="k">H + E / THREE EACH</span>'
        "<h2>Two ideas you liked, pushed three ways each. A, B and C grow the code review (H). D, E and F grow the transit map (E). Same content, different worlds.</h2>"
        "<p>Each is a working page with desktop and mobile views. Hover the diff lines, the commit rows, the stations and the legend; the interactive bits respond.</p></header>"
        + sections
        + '<footer class="rfoot"><span>Six directions, rendered live. Hover the diff, commits, stations and legend.</span>'
        "<span>" + a(GH, "GitHub", "") + " &middot; " + a(BS, "Bluesky", "") + "</span></footer>"
        "</div>" + INTERACT + "</body></html>"
    )
    return html


if __name__ == "__main__":
    html = build()
    out = ROOT / "h-and-e-studies.html"
    out.write_text(html)
    assert "\u2014" not in html, "em dash found"
    assert "http://" not in html.replace("http://www.w3.org", ""), "insecure url"
    assert 'target="_blank"' not in html, "target blank with script present"
    size = len(html.encode())
    assert size < 512 * 1024, "over 512KB: %d" % size
    print("%s: %s bytes" % (out, format(size, ",")))
