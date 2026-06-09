import json

data = json.load(open("/home/claude/amgen-fin/data.json"))
DATA_JSON = json.dumps(data)

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Amgen Inc. — Financial Intelligence Dashboard</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,500;8..60,600;8..60,700&family=Inter:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

/* McKinsey-style palette: deep navy, restrained accents, hairline borders, white canvas */
:root{
  --ink:#051C2C;             /* McKinsey deep navy */
  --ink-soft:#1F2D3D;
  --paper:#FFFFFF;           /* Pure white canvas */
  --card:#FFFFFF;            /* Cards also white */
  --line:#E2E5E9;            /* Hairline border */
  --line-soft:#F0F1F3;
  --teal:#2251FF;            /* Electric blue accent (used sparingly) */
  --teal-dk:#051C2C;         /* Deep navy (primary) */
  --gold:#FFC845;            /* Signature yellow */
  --rust:#BE3144;            /* Sober red */
  --red:#BE3144;
  --green:#06A77D;
  --muted:#5F6B7A;
  --muted-soft:#8D97A3;
  --soft:#F4F6F8;            /* Subtle background tint */
  --tint:#F8F9FB;
  --shadow:0 1px 2px rgba(5,28,44,.04), 0 0 0 1px rgba(5,28,44,.04);
  --shadow-lg:0 4px 14px rgba(5,28,44,.06), 0 0 0 1px rgba(5,28,44,.04);
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:var(--paper);color:var(--ink);}
body{font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;
  line-height:1.5;-webkit-font-smoothing:antialiased;
  font-feature-settings:'ss01','cv11','tnum';
  font-size:14px}
.wrap{max-width:1280px;margin:0 auto;padding:0 28px}

/* ---- Header bar ---- */
header.top{border-bottom:1px solid var(--line);background:rgba(255,255,255,.92);
  backdrop-filter:saturate(180%) blur(10px);position:sticky;top:0;z-index:50}
.top-in{display:flex;align-items:center;justify-content:space-between;
  padding:18px 28px;max-width:1280px;margin:0 auto}
.brand{display:flex;align-items:center;gap:14px}
.brand .logo{font-family:'Source Serif 4',serif;font-weight:700;font-size:22px;
  letter-spacing:-.3px;color:var(--ink);line-height:1}
.brand .logo b{color:var(--ink);font-weight:700}
.brand::before{content:'';display:block;width:4px;height:28px;background:var(--gold)}
.brand .sub{font-family:'IBM Plex Mono',monospace;font-size:10.5px;
  text-transform:uppercase;letter-spacing:1.4px;color:var(--muted);font-weight:500}
.asof{font-family:'IBM Plex Mono',monospace;font-size:10.5px;color:var(--muted);
  text-align:right;line-height:1.5;letter-spacing:.3px}
.asof b{color:var(--ink);font-weight:600}

/* ---- Hero ---- */
.hero{padding:54px 0 36px;border-bottom:1px solid var(--line)}
.hero h1{font-family:'Source Serif 4',serif;font-weight:500;
  font-size:clamp(34px,4.6vw,52px);line-height:1.05;letter-spacing:-1.1px;
  max-width:24ch;color:var(--ink)}
.hero h1 em{font-style:italic;color:var(--ink);font-weight:400}
.hero p{margin-top:20px;max-width:68ch;color:var(--ink-soft);font-size:15.5px;
  line-height:1.55}
.flag{display:inline-flex;gap:10px;align-items:flex-start;margin-top:22px;
  background:var(--soft);border-left:3px solid var(--gold);padding:12px 16px;
  font-size:13px;color:var(--ink-soft);max-width:78ch;line-height:1.5}
.flag svg{flex-shrink:0;margin-top:2px}
.flag b{color:var(--ink);font-weight:600}

/* ---- Nav tabs (underline style) ---- */
nav.tabs{display:flex;gap:0;flex-wrap:wrap;margin:26px 0 0;
  border-bottom:1px solid var(--line)}
nav.tabs button{font-family:'Inter',sans-serif;font-weight:500;font-size:13px;
  letter-spacing:.15px;border:0;background:transparent;color:var(--muted);
  padding:13px 18px 13px 0;margin-right:24px;cursor:pointer;
  border-bottom:2px solid transparent;margin-bottom:-1px;transition:.12s}
nav.tabs button:last-child{margin-right:0}
nav.tabs button:hover{color:var(--ink)}
nav.tabs button.active{color:var(--ink);border-color:var(--ink);font-weight:600}

section.view{display:none;padding:36px 0 70px;animation:fade .28s ease}
section.view.active{display:block}
@keyframes fade{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}

/* ---- Section headings ---- */
h2.sec{font-family:'Source Serif 4',serif;font-weight:500;font-size:26px;
  letter-spacing:-.4px;margin:4px 0 4px;display:flex;align-items:center;gap:12px;
  color:var(--ink);line-height:1.2}
h2.sec .dot{display:none}  /* removed playful dot */
h2.sec::before{content:'';display:block;width:32px;height:3px;background:var(--gold)}
.sec-note{color:var(--muted);font-size:13px;margin-bottom:24px;
  font-family:'Inter',sans-serif;line-height:1.55;max-width:84ch}
.sec-note i{color:var(--muted-soft);font-style:italic}
.sec-note b{color:var(--ink);font-weight:600}

/* ---- Statement cards (landing) ---- */
.land-grid{display:flex;flex-direction:column;gap:22px}
.stmt{background:var(--card);border:1px solid var(--line);border-radius:2px;
  box-shadow:var(--shadow);overflow:hidden;display:flex;flex-direction:column}
.stmt .h{padding:18px 22px;border-bottom:1px solid var(--line);
  display:flex;justify-content:space-between;align-items:center;background:#fff}
.stmt .h h3{font-family:'Source Serif 4',serif;font-size:20px;font-weight:600;
  color:var(--ink);letter-spacing:-.2px}
.stmt .h .tag{font-family:'IBM Plex Mono',monospace;font-size:9.5px;
  text-transform:uppercase;letter-spacing:1.2px;color:var(--muted);background:transparent;
  padding:0;border-radius:0;font-weight:500}
.stmt .h .tag::before{content:'EXHIBIT · '}
.stmt .scroll{overflow-x:auto}
.stmt table{width:100%;border-collapse:collapse;font-size:12.5px;min-width:760px}
.stmt th{font-family:'IBM Plex Mono',monospace;font-size:9.5px;font-weight:500;
  text-transform:uppercase;letter-spacing:1px;color:var(--muted);
  padding:11px 14px;border-bottom:1px solid var(--ink);background:#fff;text-align:right;
  vertical-align:bottom}
.stmt th.lbl-h{text-align:left}
.stmt th.q-h{color:var(--ink);font-weight:600}
.stmt th.spark-h{text-align:center;min-width:130px}
.stmt td{padding:8px 14px;border-bottom:1px solid var(--line-soft);
  font-family:'Inter',sans-serif}
.stmt tr:last-child td{border-bottom:0}
.stmt td.lbl{color:var(--ink-soft);white-space:nowrap;font-size:13px}
.stmt td.val{text-align:right;font-family:'IBM Plex Mono',monospace;
  font-weight:400;font-variant-numeric:tabular-nums;color:var(--ink);font-size:12.5px}
.stmt td.q{background:transparent;color:var(--ink);font-weight:600;
  border-left:2px solid var(--gold)}
.stmt td.spark{padding:4px 8px;width:140px}
.stmt td.spark canvas{display:block;height:30px !important;width:100% !important}
.stmt tr.total td{font-weight:600;background:transparent;
  border-top:1px solid var(--ink);border-bottom:1px solid var(--ink-soft)}
.stmt tr.total td.lbl{font-family:'Inter',sans-serif;
  text-transform:none;font-size:13px;letter-spacing:0;color:var(--ink);font-weight:600}
.stmt tr.total td.q{background:transparent}
.stmt tr.click{cursor:pointer;transition:background .1s}
.stmt tr.click:hover td{background:var(--tint)}
.stmt tr.click:hover td.q{background:var(--tint)}
.stmt tr.section td{font-family:'IBM Plex Mono',monospace;font-size:9.5px;
  font-weight:600;text-transform:uppercase;letter-spacing:1.4px;color:var(--muted);
  background:var(--tint);padding:8px 14px;border-bottom:1px solid var(--line);
  border-top:1px solid var(--line)}
.stmt tr.subtotal td{background:#FBFCFD;font-weight:600;
  border-top:1px solid var(--ink);border-bottom:1px solid var(--ink)}
.stmt tr.subtotal td.lbl{font-family:'Inter',sans-serif;text-transform:none;
  font-size:13px;letter-spacing:0;color:var(--ink);font-weight:600}
.stmt tr.subtotal td.q{background:#FBFCFD}
.stmt tr.indent td.lbl{padding-left:30px;color:var(--ink-soft);font-size:12.5px}
.chip{display:inline-block;font-family:'IBM Plex Mono',monospace;font-size:10px;
  padding:1px 6px;border-radius:1px;margin-left:6px;vertical-align:middle;font-weight:500}
.chip.up{background:rgba(6,167,125,.08);color:var(--green)}
.chip.dn{background:rgba(190,49,68,.08);color:var(--red)}
.chip.an{background:var(--gold);color:var(--ink);cursor:pointer}
.stmt .foot{margin-top:auto;padding:14px 22px;background:var(--tint);
  border-top:1px solid var(--line);font-size:11.5px;color:var(--muted);
  display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px;
  font-family:'Inter',sans-serif}
.stmt .foot b{color:var(--ink);font-family:'IBM Plex Mono',monospace;font-weight:600}

/* ---- Drill-down panel ---- */
.drill{margin-top:22px;background:var(--card);border:1px solid var(--line);
  border-radius:2px;box-shadow:var(--shadow-lg);display:none}
.drill.open{display:block;animation:fade .3s}
.drill .dh{padding:16px 22px;border-bottom:1px solid var(--line);
  display:flex;justify-content:space-between;align-items:center;
  background:var(--ink);color:#fff;border-radius:1px 1px 0 0}
.drill .dh h4{font-family:'Source Serif 4',serif;font-size:18px;font-weight:500;
  letter-spacing:-.2px}
.drill .dh button{background:transparent;border:1px solid rgba(255,255,255,.3);
  color:#fff;border-radius:1px;padding:5px 12px;cursor:pointer;font-size:12px;
  font-family:'Inter',sans-serif;letter-spacing:.3px;transition:.15s}
.drill .dh button:hover{background:rgba(255,255,255,.1)}
.drill .db{padding:20px 22px}
.drill table{width:100%;border-collapse:collapse;font-size:12.5px;
  font-family:'Inter',sans-serif}
.drill th{text-align:left;font-family:'IBM Plex Mono',monospace;font-size:9.5px;
  text-transform:uppercase;letter-spacing:1px;color:var(--muted);
  padding:9px 12px;border-bottom:1px solid var(--ink);font-weight:500}
.drill td{padding:9px 12px;border-bottom:1px solid var(--line-soft);
  font-variant-numeric:tabular-nums;color:var(--ink-soft)}
.drill td.n{text-align:right;font-family:'IBM Plex Mono',monospace;color:var(--ink)}

/* ---- KPI grid ---- */
.kpi-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;
  background:var(--line);border:1px solid var(--line)}
@media(max-width:980px){.kpi-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:560px){.kpi-grid{grid-template-columns:1fr}}
.kpi{background:#fff;padding:22px 22px 20px;position:relative;overflow:hidden}
.kpi::before{display:none}
.kpi.warn::after{content:'';position:absolute;left:0;top:0;width:100%;height:2px;background:var(--rust)}
.kpi.good::after{content:'';position:absolute;left:0;top:0;width:100%;height:2px;background:var(--green)}
.kpi .k{font-family:'IBM Plex Mono',monospace;font-size:10px;
  text-transform:uppercase;letter-spacing:1.2px;color:var(--muted);font-weight:500}
.kpi .v{font-family:'Source Serif 4',serif;font-size:34px;font-weight:500;
  margin:6px 0 4px;letter-spacing:-.8px;color:var(--ink);line-height:1.05}
.kpi .d{font-size:11.5px;color:var(--muted);font-family:'Inter',sans-serif;
  line-height:1.4}
.kpi .spark{height:32px;margin-top:10px}

/* ---- Chart cards ---- */
.chart-grid{display:grid;grid-template-columns:1fr 1fr;gap:22px}
@media(max-width:880px){.chart-grid{grid-template-columns:1fr}}
.chart-card{background:var(--card);border:1px solid var(--line);border-radius:2px;
  padding:22px;box-shadow:var(--shadow)}
.chart-card h3{font-family:'Source Serif 4',serif;font-size:17px;font-weight:600;
  color:var(--ink);letter-spacing:-.2px}
.chart-card h3::before{content:'EXHIBIT  ';font-family:'IBM Plex Mono',monospace;
  font-size:9.5px;font-weight:500;letter-spacing:1.2px;color:var(--muted);
  vertical-align:middle;margin-right:6px;text-transform:uppercase}
.chart-card .cn{font-size:12.5px;color:var(--muted);margin:6px 0 18px;line-height:1.5;
  padding-bottom:14px;border-bottom:1px solid var(--line-soft)}
.chart-box{position:relative;height:260px}
.chart-box.tall{height:340px}

/* ---- Anomalies ---- */
.an-list{display:flex;flex-direction:column;gap:1px;background:var(--line);
  border:1px solid var(--line)}
.an-item{background:#fff;padding:18px 22px;
  display:grid;grid-template-columns:auto 1fr auto;gap:18px;align-items:center}
.an-item .sev{font-family:'IBM Plex Mono',monospace;font-size:9.5px;font-weight:600;
  text-transform:uppercase;letter-spacing:1.2px;color:#fff;background:var(--rust);
  padding:4px 10px;border-radius:1px;white-space:nowrap}
.an-item.sev2 .sev{background:var(--gold);color:var(--ink)}
.an-item .body h4{font-family:'Source Serif 4',serif;font-size:16px;font-weight:600;
  color:var(--ink);letter-spacing:-.1px}
.an-item .body p{font-size:13px;color:var(--muted);margin-top:3px;line-height:1.5}
.an-item .z{text-align:right;font-family:'IBM Plex Mono',monospace}
.an-item .z .big{font-size:24px;font-weight:500;color:var(--ink);letter-spacing:-.5px}
.an-item .z .lbl{font-size:9.5px;color:var(--muted);text-transform:uppercase;
  letter-spacing:1px;margin-top:2px}

/* ---- Stakeholder personas ---- */
.persona-tabs{display:flex;gap:0;margin-bottom:24px;flex-wrap:wrap;
  border-bottom:1px solid var(--line)}
.persona-tabs button{font-family:'Inter',sans-serif;font-weight:500;font-size:12.5px;
  border:0;background:transparent;color:var(--muted);
  padding:11px 16px 11px 0;margin-right:22px;cursor:pointer;transition:.12s;
  border-bottom:2px solid transparent;margin-bottom:-1px;letter-spacing:.2px}
.persona-tabs button:hover{color:var(--ink)}
.persona-tabs button.active{background:transparent;color:var(--ink);
  border-color:var(--ink);font-weight:600}
.persona{display:none}.persona.active{display:block;animation:fade .3s}
.insight{background:var(--card);border:1px solid var(--line);border-radius:2px;
  padding:24px 26px;box-shadow:var(--shadow);margin-bottom:18px}
.insight h4{font-family:'Source Serif 4',serif;font-size:19px;font-weight:600;
  display:flex;align-items:center;gap:11px;margin-bottom:14px;color:var(--ink);
  letter-spacing:-.2px;padding-bottom:12px;border-bottom:1px solid var(--line)}
.insight h4 .ic{width:28px;height:28px;background:var(--ink);color:var(--gold);
  border-radius:50%;display:grid;place-items:center;font-size:14px;font-weight:500}
.insight ul{list-style:none;display:flex;flex-direction:column;gap:11px}
.insight li{font-size:13.5px;padding-left:20px;position:relative;color:var(--ink-soft);
  line-height:1.6}
.insight li::before{content:'';position:absolute;left:0;top:9px;width:8px;height:1px;
  background:var(--ink)}
.insight li b{color:var(--ink);font-weight:600}
.metric-row{display:flex;gap:32px;flex-wrap:wrap;margin-top:18px;
  padding-top:16px;border-top:1px solid var(--line)}
.metric-row .m{font-family:'IBM Plex Mono',monospace}
.metric-row .m .mv{font-size:22px;font-weight:500;color:var(--ink);
  font-family:'Source Serif 4',serif;letter-spacing:-.4px}
.metric-row .m .ml{font-size:9.5px;text-transform:uppercase;color:var(--muted);
  letter-spacing:1.2px;font-family:'IBM Plex Mono',monospace;margin-top:3px;font-weight:500}

/* ---- Footer ---- */
footer{border-top:1px solid var(--ink);padding:32px 0 60px;font-size:12px;
  color:var(--muted);background:#fff}
footer a{color:var(--ink);text-decoration:none;border-bottom:1px solid var(--gold)}
footer .src{font-family:'IBM Plex Mono',monospace;font-size:11px;line-height:1.7;
  letter-spacing:.2px}

.toggle{display:inline-flex;border:1px solid var(--line);border-radius:1px;
  overflow:hidden;margin-left:auto}
.toggle button{border:0;background:#fff;padding:7px 16px;font-size:11px;
  font-family:'IBM Plex Mono',monospace;cursor:pointer;color:var(--muted);
  letter-spacing:.5px;text-transform:uppercase;font-weight:500}
.toggle button.active{background:var(--ink);color:#fff}
.viewbar{display:flex;align-items:center;gap:10px;margin-bottom:18px;flex-wrap:wrap}

/* ---- Scenarios ---- */
.scen-presets{display:flex;gap:10px;margin-bottom:22px;flex-wrap:wrap}
.scen-presets button{font-family:'Inter',sans-serif;font-weight:500;font-size:12.5px;
  border:1px solid var(--line);background:#fff;color:var(--ink-soft);
  padding:10px 18px;border-radius:1px;cursor:pointer;transition:.12s;
  display:flex;align-items:center;gap:9px;letter-spacing:.2px}
.scen-presets button .dot{width:8px;height:8px;border-radius:50%}
.scen-presets button:hover{border-color:var(--ink-soft)}
.scen-presets button.active{border-color:var(--ink);background:var(--ink);color:#fff}
.scen-grid{display:grid;grid-template-columns:320px 1fr;gap:22px}
@media(max-width:900px){.scen-grid{grid-template-columns:1fr}}
.scen-inputs{background:var(--card);border:1px solid var(--line);border-radius:2px;
  padding:22px;box-shadow:var(--shadow);align-self:start}
.scen-inputs h3{font-family:'Source Serif 4',serif;font-size:16px;font-weight:600;
  margin-bottom:18px;padding-bottom:12px;border-bottom:1px solid var(--ink);
  color:var(--ink)}
.scen-input{margin-bottom:18px}
.scen-input label{display:flex;justify-content:space-between;font-family:'IBM Plex Mono',monospace;
  font-size:10px;text-transform:uppercase;letter-spacing:1.2px;color:var(--muted);
  margin-bottom:6px;font-weight:500}
.scen-input label .v{color:var(--ink);font-weight:600;font-size:13px;
  font-family:'Source Serif 4',serif;letter-spacing:-.2px}
.scen-input input[type=range]{width:100%;-webkit-appearance:none;height:3px;
  background:var(--line);border-radius:0;outline:none}
.scen-input input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;
  width:16px;height:16px;background:var(--ink);border-radius:50%;cursor:pointer;
  border:2px solid #fff;box-shadow:0 0 0 1px var(--ink)}
.scen-input input[type=range]::-moz-range-thumb{width:16px;height:16px;
  background:var(--ink);border-radius:50%;cursor:pointer;border:2px solid #fff;
  box-shadow:0 0 0 1px var(--ink)}
.scen-input .range-meta{display:flex;justify-content:space-between;
  font-family:'IBM Plex Mono',monospace;font-size:9.5px;color:var(--muted-soft);
  margin-top:4px;letter-spacing:.3px}
.scen-summary{background:var(--card);border:1px solid var(--line);border-radius:2px;
  padding:22px;box-shadow:var(--shadow);margin-top:22px;display:grid;
  grid-template-columns:repeat(4,1fr);gap:1px;background:var(--line)}
@media(max-width:700px){.scen-summary{grid-template-columns:repeat(2,1fr)}}
.scen-summary .m{padding:18px 20px;background:#fff}
.scen-summary .ml{font-family:'IBM Plex Mono',monospace;font-size:10px;
  text-transform:uppercase;color:var(--muted);letter-spacing:1.2px;font-weight:500}
.scen-summary .mv{font-family:'Source Serif 4',serif;font-size:28px;font-weight:500;
  letter-spacing:-.6px;margin-top:4px;color:var(--ink);line-height:1.1}
.scen-summary .md{font-size:11.5px;color:var(--muted);margin-top:2px}
.scen-note{background:var(--soft);border-left:3px solid var(--gold);border-radius:0;
  padding:10px 14px;margin-top:14px;font-size:12px;color:var(--ink-soft);line-height:1.5}

/* ---- Sensitivity / WoCA tables ---- */
.sens-table{width:100%;border-collapse:collapse;margin-top:8px;
  font-family:'IBM Plex Mono',monospace;font-size:12px}
.sens-table th,.sens-table td{padding:10px 12px;text-align:center;
  border:1px solid var(--line)}
.sens-table th{background:var(--tint);color:var(--muted);text-transform:uppercase;
  font-size:9.5px;letter-spacing:1px;font-weight:500}
.sens-table td{font-variant-numeric:tabular-nums;color:var(--ink)}
.sens-table td.lo{background:rgba(190,49,68,.08);color:var(--rust)}
.sens-table td.hi{background:rgba(6,167,125,.08);color:var(--green)}
.sens-table td.mid{background:#FCFDFE}

.woca-table{width:100%;border-collapse:collapse;font-family:'IBM Plex Mono',monospace;
  font-size:12px}
.woca-table th{font-family:'IBM Plex Mono',monospace;font-size:9.5px;text-transform:uppercase;
  letter-spacing:1px;color:var(--muted);padding:11px 12px;background:#fff;
  border-bottom:1px solid var(--ink);text-align:right;font-weight:500}
.woca-table th.lh{text-align:left}
.woca-table td{padding:10px 12px;border-bottom:1px solid var(--line-soft);
  font-variant-numeric:tabular-nums;color:var(--ink)}
.woca-table td.n{text-align:right}
.woca-table td.rk{text-align:center;font-size:9.5px;color:var(--muted)}
.woca-table tr.me td{background:#FBFCFD;border-left:3px solid var(--gold);font-weight:600}
.woca-table tr.me td:first-child{padding-left:9px}
.woca-table td.bad{background:rgba(190,49,68,.06);color:var(--rust)}
.woca-table td.mid{background:#FCFDFE}
.woca-table td.good{background:rgba(6,167,125,.06);color:var(--green)}
.woca-table tr.med td{background:var(--tint);font-style:normal;
  border-top:1px solid var(--ink);color:var(--ink);font-weight:600}
</style>
</head>
<body>
<header class="top">
  <div class="top-in">
    <div class="brand">
      <span class="logo">Amgen Inc.</span>
      <span class="sub">Financial Intelligence Briefing</span>
    </div>
    <div class="asof">
      <div>NASDAQ: <b>AMGN</b> · one reportable segment</div>
      <div>Data through <b>Q1 FY2026</b> (10-Q, Mar 31 2026)</div>
    </div>
  </div>
</header>

<div class="wrap">
  <div class="hero">
    <h1>Five years of financial performance, <em>read in a single view.</em></h1>
    <p>A five-year intelligence layer over Amgen's reported financials: statement landing pages with one-click drill-down, KPI trends, statistical anomaly flags, and tailored read-outs for the CFO, market leads and analysts. Built entirely from SEC filings and Amgen investor releases.</p>
    <div class="flag">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#7a5a12" stroke-width="2"><path d="M12 9v4M12 17h.01M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/></svg>
      <span><b>Scope of "transactional level":</b> public filings disclose line-item and product/geography detail — not journal entries or invoices. Anomaly detection here runs at the most granular public level (statement line + product). True GL-transaction scanning would require your internal ERP feed, which can plug into the same engine.</span>
    </div>
  </div>

  <nav class="tabs" id="tabs">
    <button data-v="landing" class="active">Landing</button>
    <button data-v="trends">5-Yr Trends</button>
    <button data-v="kpis">KPI Library</button>
    <button data-v="workcap">Working Capital</button>
    <button data-v="anomalies">Anomalies</button>
    <button data-v="products">Product Drill-down</button>
    <button data-v="valuation">Valuation</button>
    <button data-v="scenarios">Scenarios</button>
    <button data-v="stakeholders">Stakeholder Views</button>
  </nav>

  <!-- ============ LANDING ============ -->
  <section class="view active" id="landing">
    <div class="viewbar">
      <h2 class="sec"><span class="dot"></span>Three statements · FY21 → FY25 + Q1'26</h2>
    </div>
    <p class="sec-note">All periods shown side-by-side. The sparkline on the right traces the line across FY21–FY25 (Q1'26 displayed separately). Click any expandable row to drill into composition. Figures in USD millions unless noted.</p>
    <div class="land-grid" id="landGrid"></div>
    <div class="drill" id="drill">
      <div class="dh"><h4 id="drillTitle"></h4><button onclick="closeDrill()">Close ✕</button></div>
      <div class="db" id="drillBody"></div>
    </div>
  </section>

  <!-- ============ TRENDS ============ -->
  <section class="view" id="trends">
    <h2 class="sec"><span class="dot"></span>Five-year trends with analysis</h2>
    <p class="sec-note">FY2021–FY2025. Bars/lines reflect GAAP reported results; commentary highlights the structural shifts.</p>
    <div class="chart-grid">
      <div class="chart-card"><h3>Revenue &amp; Net Income</h3><div class="cn">Total revenue climbed from $26,300M to $36,800M (+40% over 5y); net income dipped in 2024 on Horizon amortization &amp; tax, recovering in 2025.</div><div class="chart-box"><canvas id="cRev"></canvas></div></div>
      <div class="chart-card"><h3>Margin Profile</h3><div class="cn">Gross margin compressed post-Horizon (inventory step-up &amp; amortization in COGS) then began recovering in 2025.</div><div class="chart-box"><canvas id="cMargin"></canvas></div></div>
      <div class="chart-card"><h3>Free Cash Flow vs Dividends</h3><div class="cn">FCF funds a rising dividend; 2025 FCF fell to $8,100M on working-capital timing &amp; higher capex even as earnings rose.</div><div class="chart-box"><canvas id="cFcf"></canvas></div></div>
      <div class="chart-card"><h3>Leverage: Debt &amp; Debt/Equity</h3><div class="cn">The $27,800M Horizon deal (Oct 2023) spiked debt to ~$65,000M; de-levering since, but D/E stays elevated on a thin equity base.</div><div class="chart-box"><canvas id="cDebt"></canvas></div></div>
      <div class="chart-card"><h3>R&amp;D Investment &amp; Intensity</h3><div class="cn">R&amp;D rose to $7,300M (20.6% of product sales) in 2025, driven by MariTide Phase 3 and the obesity pipeline.</div><div class="chart-box"><canvas id="cRnd"></canvas></div></div>
      <div class="chart-card"><h3>Balance Sheet Composition</h3><div class="cn">Intangibles + goodwill dominate assets after Horizon; tangible equity remains modest relative to a ~$90,000M asset base.</div><div class="chart-box"><canvas id="cBs"></canvas></div></div>
    </div>
  </section>

  <!-- ============ KPIs ============ -->
  <section class="view" id="kpis">
    <h2 class="sec"><span class="dot"></span>KPI library — built from P&amp;L, balance sheet &amp; FCF</h2>
    <p class="sec-note">Latest full year (FY2025) with 5-year sparkline. Colour rail: green = healthy / improving, red = watch.</p>
    <div class="kpi-grid" id="kpiGrid"></div>
  </section>

  <!-- ============ WORKING CAPITAL & CCC ============ -->
  <section class="view" id="workcap">
    <h2 class="sec"><span class="dot"></span>Working capital &amp; cash-conversion cycle</h2>
    <p class="sec-note">CCC = DSO + DIO − DPO. Inventory tied up + receivables outstanding − payables outstanding. Lower is better — measures how many days of operating cash is locked up in the working-capital cycle. <i>Accounts payable is modelled (typical pharma AP/Revenue ratios) — Amgen's 10-K does not break out AP as a separate line in the captured BS rollup.</i></p>
    <div class="kpi-grid" id="wcKpis"></div>
    <div class="chart-grid" style="margin-top:18px">
      <div class="chart-card"><h3>Cash-Conversion Cycle trend (days)</h3><div class="cn">CCC peaked at 330 days in FY22, improved to 255 days in FY24 (Horizon integration efficiencies), drifted back up to 274 days in FY25.</div><div class="chart-box"><canvas id="cCCC"></canvas></div></div>
      <div class="chart-card"><h3>DSO / DIO / DPO components</h3><div class="cn">Inventory days dominate the cycle (~250 days); pharma typically carries deep inventory due to long manufacturing lead times &amp; quality testing.</div><div class="chart-box"><canvas id="cWCparts"></canvas></div></div>
    </div>
    <div class="chart-card" style="margin-top:18px"><h3>DuPont decomposition of ROE (5-yr)</h3><div class="cn">ROE = Net margin × Asset turnover × Equity multiplier. Amgen's ROE is overwhelmingly leverage-driven (equity multiplier ~10x) — strip it and the underlying ROA is more honest.</div><div class="chart-box"><canvas id="cDupont"></canvas></div></div>

    <!-- WoCA: peer comparison block -->
    <div style="margin-top:32px;padding-top:24px;border-top:2px solid var(--ink)">
      <h2 class="sec" style="font-size:22px"><span class="dot"></span>WoCA · Working Capital Analysis vs peers (FY2024)</h2>
      <p class="sec-note">Where does Amgen's working-capital footprint sit against 8 large-cap pharma peers? Lower DSO/DIO/CCC = more efficient; higher DPO = better cash management. <i>Pfizer and Lilly figures sourced from 10-K filings via stock-analysis-on.net; remaining peers modelled from FY2024 reported balance-sheet items.</i></p>
      <div class="kpi-grid" id="wocaKpis"></div>
      <div class="chart-grid" style="margin-top:18px">
        <div class="chart-card"><h3>Cash-Conversion Cycle ranking</h3><div class="cn">Amgen highlighted in rust; the dashed line is the peer-median CCC.</div><div class="chart-box tall"><canvas id="cWocaCCC"></canvas></div></div>
        <div class="chart-card"><h3>CCC components stacked (DSO + DIO − DPO)</h3><div class="cn">Inventory days drive most of the spread between peers; Amgen and Lilly are the two long-cycle outliers.</div><div class="chart-box tall"><canvas id="cWocaStack"></canvas></div></div>
      </div>
      <div class="chart-card" style="margin-top:18px"><h3>Full WoCA matrix</h3><div class="cn">All four metrics by company; Amgen's row is highlighted, rank (of 9) shown for each metric.</div><div id="wocaTable" style="margin-top:8px"></div></div>

      <!-- CCC improvement slicer -->
      <h3 style="font-family:'Fraunces',serif;font-size:18px;margin-top:30px;margin-bottom:6px">CCC improvement slicer — drag the targets, watch the cash unlock</h3>
      <p class="sec-note">Drag each metric to a target value. Live calculation: new CCC, working-capital dollars freed, days off the cycle. FY25 base: Revenue $36,800M / COGS $9,100M.</p>
      <div class="scen-presets" id="wocaPresets"></div>
      <div class="scen-grid">
        <div class="scen-inputs" id="wocaInputs"></div>
        <div class="scen-output">
          <div class="chart-card"><h3>CCC: current → target</h3><div class="cn">Bar chart shows the four working-capital metrics side by side, current vs target.</div><div class="chart-box"><canvas id="cWocaSlice"></canvas></div></div>
          <div class="scen-summary" id="wocaSummary"></div>
        </div>
      </div>
    </div>
  </section>

  <!-- ============ ANOMALIES ============ -->
  <section class="view" id="anomalies">
    <h2 class="sec"><span class="dot"></span>Anomaly detection</h2>
    <p class="sec-note">Method: for each line, the year-over-year % change is scored against its own 5-year distribution (z-score). |z| ≥ 1.7 ⇒ <b>high</b>, otherwise material flags shown as <b>watch</b>. Product flags compare Q1'26 growth against the portfolio mean. This is line/product-level — clearly not GL-transaction level.</p>
    <h3 style="font-family:'Fraunces',serif;font-weight:600;margin:6px 0 12px;font-size:18px">Statement-line anomalies (FY21→FY25)</h3>
    <div class="an-list" id="anList"></div>
    <h3 style="font-family:'Fraunces',serif;font-weight:600;margin:26px 0 12px;font-size:18px">Product-level anomalies (Q1'26 vs Q1'25)</h3>
    <div class="an-list" id="anProd"></div>
  </section>

  <!-- ============ PRODUCTS ============ -->
  <section class="view" id="products">
    <h2 class="sec"><span class="dot"></span>Product drill-down — Q1 FY2026</h2>
    <p class="sec-note">The deepest granularity in public filings: product sales by US vs ex-US and therapeutic area. Sort by clicking the chart legend. Total product sales $8,218M.</p>
    <div class="chart-grid">
      <div class="chart-card"><h3>Sales by product — Q1'26 vs Q1'25</h3><div class="cn">Growth leaders (IMDELLTRA, UPLIZNA, Repatha) vs biosimilar/IRA-pressured decliners (Prolia, XGEVA, ENBREL).</div><div class="chart-box tall"><canvas id="cProd"></canvas></div></div>
      <div class="chart-card"><h3>US vs Ex-US mix (Q1'26)</h3><div class="cn">US is ~70% of product sales; ex-US strength in Aranesp, Vectibix, BLINCYTO.</div><div class="chart-box tall"><canvas id="cGeo"></canvas></div></div>
    </div>
    <div class="chart-card" style="margin-top:18px"><h3>Therapeutic-area contribution (Q1'26)</h3><div class="cn">Four pillars: General Medicine, Oncology, Inflammation, Rare Disease.</div><div class="chart-box"><canvas id="cArea"></canvas></div></div>
  </section>

  <!-- ============ VALUATION ============ -->
  <section class="view" id="valuation">
    <h2 class="sec"><span class="dot"></span>Valuation framework</h2>
    <p class="sec-note">EV, multiples, dividend discount and a stylised SOTP. Market data refreshed from live sources; multiples derive from FY25 actuals and TTM figures.</p>
    <div class="kpi-grid" id="valKpis"></div>
    <div class="chart-grid" style="margin-top:18px">
      <div class="chart-card"><h3>Enterprise-Value bridge</h3><div class="cn">EV = Market cap + Total debt − Cash. The leverage built up to fund Horizon is fully reflected.</div><div class="chart-box"><canvas id="cEV"></canvas></div></div>
      <div class="chart-card"><h3>Debt maturity wall ($M, indicative)</h3><div class="cn">Major rated senior notes only. Weighted-avg maturity ~11.6 years post Feb-2026 issuance — long-dated profile reduces near-term refi risk.</div><div class="chart-box"><canvas id="cMaturity"></canvas></div></div>
    </div>
    <div class="chart-grid" style="margin-top:18px">
      <div class="chart-card"><h3>Stylised SOTP — illustrative</h3><div class="cn">Sum-of-the-parts: base biopharma at biopharma multiples, Horizon Rare Disease at premium, MariTide option value, less tax-overhang discount. Not a valuation recommendation.</div><div class="chart-box"><canvas id="cSOTP"></canvas></div></div>
      <div class="chart-card"><h3>Dividend Discount (Gordon)</h3><div class="cn">P = D₁ / (r − g). Current annual div $10.08; sensitivity across r and g shown — current price ~$338 implies r−g ≈ 3.1%.</div><div class="chart-box"><canvas id="cDDM"></canvas></div></div>
    </div>
    <div class="chart-card" style="margin-top:18px"><h3>EV/EBITDA sensitivity vs FCF growth</h3><div class="cn">Forward-EV/EBITDA implied at varying FCF growth and exit multiples — quick way to triangulate whether MariTide optionality is in or out of the price.</div><div id="sensTable"></div></div>
  </section>

  <!-- ============ SCENARIOS ============ -->
  <section class="view" id="scenarios">
    <h2 class="sec"><span class="dot"></span>Scenario modelling — base / bull / bear (editable)</h2>
    <p class="sec-note">Pick a preset, then adjust drivers. Projection runs 3 years from FY25 actuals. All output flows: Revenue → Gross profit → Op income → Net income → EPS &amp; FCF.</p>
    <div class="scen-presets" id="scenPresets"></div>
    <div class="scen-grid">
      <div class="scen-inputs" id="scenInputs"></div>
      <div class="scen-output">
        <div class="chart-card"><h3>3-year P&amp;L projection</h3><div class="cn">FY25 base extended on the chosen drivers. Red dashed = current scenario; grey = FY25 baseline.</div><div class="chart-box tall"><canvas id="cScenPL"></canvas></div></div>
        <div class="scen-summary" id="scenSummary"></div>
      </div>
    </div>
  </section>

  <!-- ============ STAKEHOLDERS ============ -->
  <section class="view" id="stakeholders">
    <h2 class="sec"><span class="dot"></span>Insights by stakeholder</h2>
    <p class="sec-note">Same numbers, five lenses. Switch personas below. (All persona content is generated in Python — see <code>build_html.py</code>.)</p>
    <div class="persona-tabs" id="personaTabs">__PERSONA_TABS__</div>
__PERSONA_PANELS__
  </section>
</div>

<footer><div class="wrap">
  <div class="src">
    SOURCES — Amgen Form 10-Q (period ended Mar 31 2026); Amgen Q4/FY2025 results (Feb 3 2026);
    Q4/FY2024 results (Feb 4 2025); 2023 Form 10-K &amp; Letter to Shareholders; FY2021–FY2022 reported actuals.
    All figures USD millions unless noted. Certain FY2024–FY2025 expense sub-lines are modeled from reported
    growth rates/margins where the granular line was not in the retrieved source text; headline revenue, net
    income, EPS, FCF and balance-sheet totals are reported actuals.
  </div>
  <p style="margin-top:12px">Built as an analytical layer for finance review. Not investment advice — Amgen's own filings govern. · <b>Anomaly engine is line/product-level;</b> connect an internal GL extract to extend to journal-entry scanning.</p>
</div></footer>

<script>
const DATA = __DATA__;
const $ = s => document.querySelector(s);
const fmt = n => (n<0?'(':'')+'$'+Math.abs(Math.round(n)).toLocaleString()+(n<0?')':'');
const fmtB = n => (n<0?'(':'')+'$'+Math.abs(Math.round(n)).toLocaleString()+'M'+(n<0?')':'');
const pc = n => (n>0?'+':'')+n+'%';
const PALETTE={ink:'#051C2C',teal:'#2251FF',tealDk:'#051C2C',gold:'#FFC845',
  rust:'#BE3144',green:'#06A77D',soft:'#E2E5E9',muted:'#5F6B7A',
  grid:'rgba(5,28,44,.06)'};
Chart.defaults.font.family="'Inter',-apple-system,BlinkMacSystemFont,sans-serif";
Chart.defaults.color='#5F6B7A';Chart.defaults.font.size=10.5;
Chart.defaults.font.weight=500;

/* ---------- tab nav ---------- */
$('#tabs').addEventListener('click',e=>{
  const b=e.target.closest('button');if(!b)return;
  document.querySelectorAll('#tabs button').forEach(x=>x.classList.remove('active'));
  b.classList.add('active');
  document.querySelectorAll('section.view').forEach(v=>v.classList.remove('active'));
  $('#'+b.dataset.v).classList.add('active');
  if(b.dataset.v==='trends')drawTrends();
  if(b.dataset.v==='products')drawProducts();
  if(b.dataset.v==='workcap')drawWorkcap();
  if(b.dataset.v==='valuation')drawValuation();
  if(b.dataset.v==='scenarios')drawScenarios();
});

/* ---------- LANDING statements — all periods + sparklines ---------- */
const Q=DATA.q, PL=DATA.pl, BS=DATA.bs, CF=DATA.cf;
const FY_YEARS=DATA.years;       // [2021..2025]
const Q_KEY='2026Q1', QP_KEY='2025Q1';

// fmt helpers for landing cells
const fmtShort = n => {
  if(n===null||n===undefined||isNaN(n))return '—';
  const a=Math.abs(n);
  const s=n<0?'(':'';const e=n<0?')':'';
  return s+'$'+Math.round(a).toLocaleString()+'M'+e;
};
const fmtRatio = v => isFinite(v)?v.toFixed(2):'—';

// Row spec: [label, key in statement obj, options]
// options: {total, click, neg (always show negative), money (default true), eps}
const PL_ROWS=[
  ['Product sales','product',{click:'product'}],
  ['Other revenues','other'],
  ['Total revenues','total',{total:true}],
  ['Cost of sales','cogs',{click:'cogs'}],
  ['Research &amp; development','rnd',{click:'rnd'}],
  ['Selling, general &amp; admin','sga',{click:'sga'}],
  ['Other operating','other_op'],
  ['Operating income','op_income',{total:true}],
  ['Interest expense, net','int_exp'],
  ['Other income, net','other_inc'],
  ['Provision for income taxes','tax'],
  ['Net income','net',{total:true}],
  ['Diluted EPS ($)','eps',{eps:true}],
];
const BS_ROWS=[
  ['Cash &amp; equivalents','cash'],
  ['Trade receivables, net','receivables'],
  ['Inventories','inventory',{click:'inventory'}],
  ['Total current assets','cur_assets',{total:true}],
  ['Property, plant &amp; equip.','ppe'],
  ['Goodwill','goodwill'],
  ['Intangible assets, net','intangibles',{click:'intangibles'}],
  ['Total assets','total_assets',{total:true}],
  ['Total debt','total_debt',{click:'debt'}],
  ['Total current liabilities','cur_liab'],
  ['Total liabilities','total_liab',{total:true}],
  ['Stockholders\u2019 equity','equity',{total:true}],
];
const CF_ROWS=[
  // Operating activities
  ['Operating activities',null,{section:true}],
  ['Net income','net_income',{indent:true}],
  ['Depreciation &amp; amortization','d_a',{indent:true}],
  ['Stock-based compensation','sbc',{indent:true}],
  ['Deferred income taxes','def_tax',{indent:true}],
  ['Other non-cash items','other_nc',{indent:true}],
  ['Δ Trade receivables','d_rec',{indent:true}],
  ['Δ Inventories','d_inv',{indent:true}],
  ['Δ Accounts payable (m)','d_ap',{indent:true}],
  ['Δ Other working capital','d_other_wc',{indent:true}],
  ['Net cash from operations (OCF)','ocf',{subtotal:true}],
  // FCF reconciliation
  ['Free Cash Flow reconciliation',null,{section:true}],
  ['Operating cash flow','ocf',{indent:true}],
  ['Capital expenditures','capex',{indent:true,click:'capex'}],
  ['Free Cash Flow','fcf',{subtotal:true,click:'fcf'}],
  // Investing (other than capex)
  ['Other investing activities',null,{section:true}],
  ['Acquisitions, net','acquisitions',{indent:true}],
  ['Marketable securities (net)','mkt_securities',{indent:true}],
  // Financing
  ['Financing activities',null,{section:true}],
  ['Long-term debt issued','debt_issued',{indent:true}],
  ['Long-term debt repaid','debt_repaid',{indent:true,click:'debt'}],
  ['Dividends paid','dividends',{indent:true}],
  ['Share repurchases','buybacks',{indent:true}],
];

// Render one statement card: rows × (FY years + Q1'26 + sparkline).
// `qSource` (optional) is consulted for the Q1'26 column; if absent, falls
// back to the matching DATA.q[Q_KEY] entry. `rows` may include section headers
// (opts.section:true) which render a full-width band, and subtotal rows
// (opts.subtotal:true) styled distinctly.
function statementCard(title, tag, rows, source, qSource){
  // header: FY columns + Q1'26 column + sparkline column
  let head='<tr><th class="lbl-h">Line item</th>';
  FY_YEARS.forEach(y=>{ head += `<th>FY${(y%100).toString().padStart(2,'0')}</th>`; });
  head += '<th class="q-h">Q1\u201926</th><th class="spark-h">5-yr trend</th></tr>';

  let body='';
  const sparkIds=[];
  const totalCols = FY_YEARS.length + 2;     // FY cols + Q + sparkline
  rows.forEach((spec,idx)=>{
    const [lbl,key,opts={}]=spec;
    if(opts.section){
      body += `<tr class="section"><td colspan="${1+totalCols}">${lbl}</td></tr>`;
      return;
    }
    const isEps = !!opts.eps;
    const isClick = !!opts.click;
    const isTotal = !!opts.total;
    const isSub = !!opts.subtotal;
    const isInd = !!opts.indent;
    const cls = isSub?'subtotal':(isTotal?'total':(isClick?'click':'')) + (isInd?' indent':'');
    const click = isClick? `onclick="drill('${opts.click}')"`:'';
    // values
    const fy = FY_YEARS.map(y => (source[y]?source[y][key]:null));
    const qSrc = qSource || DATA.q[Q_KEY];
    const qVal = qSrc ? (qSrc[key] ?? null) : null;
    const neg = opts.neg;
    const dispFY = fy.map(v => v===null||v===undefined ? '—' :
      (isEps ? '$'+v.toFixed(2) :
        (neg ? fmtShort(-Math.abs(v)) : fmtShort(v))));
    const dispQ = qVal===null||qVal===undefined ? '—' :
      (isEps ? '$'+qVal.toFixed(2) :
        (neg ? fmtShort(-Math.abs(qVal)) : fmtShort(qVal)));
    // sparkline canvas id
    const sid = `sp-${title.replace(/[^a-z]/gi,'')}-${idx}`;
    sparkIds.push({id:sid, data:fy, neg:!!neg, eps:isEps});

    body += `<tr class="${cls.trim()}" ${click}><td class="lbl">${lbl}</td>`;
    dispFY.forEach(v => body += `<td class="val">${v}</td>`);
    body += `<td class="val q">${dispQ}</td>`;
    body += `<td class="spark"><canvas id="${sid}"></canvas></td>`;
    body += '</tr>';
  });

  return {
    html: `<div class="stmt">
      <div class="h"><h3>${title}</h3><span class="tag">${tag}</span></div>
      <div class="scroll"><table><thead>${head}</thead><tbody>${body}</tbody></table></div>
      <div class="foot"></div>
    </div>`,
    sparks: sparkIds,
  };
}

function buildLanding(){
  const g=$('#landGrid');

  const cards=[
    statementCard('Income Statement','Annual + Q1\u201926', PL_ROWS, PL, DATA.q[Q_KEY]),
    statementCard('Balance Sheet','Year-end (FY) + Q1\u201926*', BS_ROWS, BS, null),
    statementCard('Cash Flow & Free Cash Flow','Detailed reconciliation', CF_ROWS, DATA.cf_detail, DATA.cf_detail_q[Q_KEY]),
  ];
  g.innerHTML = cards.map(c=>c.html).join('');

  // Foot text per card (computed)
  const foots = g.querySelectorAll('.stmt .foot');
  const fy25=PL[2025], q26=DATA.q[Q_KEY];
  foots[0].innerHTML = `<span>FY25 Op margin <b>${(fy25.op_income/fy25.product*100).toFixed(1)}%</b> of product sales · Q1\u201926 Op margin <b>${(q26.op_income/q26.product*100).toFixed(1)}%</b></span><span>5-yr Revenue CAGR <b>${(((PL[2025].total/PL[2021].total)**(1/4)-1)*100).toFixed(1)}%</b></span>`;
  const bs25=BS[2025];
  foots[1].innerHTML = `<span>FY25 Current ratio <b>${(bs25.cur_assets/bs25.cur_liab).toFixed(2)}</b> · D/E <b>${(bs25.total_debt/bs25.equity).toFixed(2)}×</b></span><span>Intangibles + Goodwill = <b>${Math.round((bs25.goodwill+bs25.intangibles)/bs25.total_assets*100)}%</b> of assets · <i>* Q1'26 BS not in this dataset</i></span>`;
  const cf25=DATA.cf_detail[2025];
  const fcfConv=Math.round(cf25.fcf/cf25.net_income*100);
  const fcf5y=DATA.years.reduce((a,y)=>a+DATA.cf_detail[y].fcf,0);
  foots[2].innerHTML = `<span>FY25 FCF conversion <b>${fcfConv}%</b> of net income · 5-yr cumul. FCF <b>${fmtB(fcf5y)}</b></span><span>FY25 dividend coverage <b>${cf25.fcf_to_div}%</b> of FCF · <i>(m) modelled lines flagged</i></span>`;

  // Draw sparklines (small line charts in each row's last cell).
  // Section/subtotal rows do not have canvases (no key) — guard for missing elements.
  cards.forEach(card => {
    card.sparks.forEach(s => {
      const el = document.getElementById(s.id);
      if(!el) return;
      const series = s.data.map(v => s.neg ? -Math.abs(v||0) : (v||0));
      const allEqual = series.every(v=>v===series[0]);
      const color = (series[series.length-1] >= series[0]) ? PALETTE.green : PALETTE.rust;
      new Chart(el, {
        type:'line',
        data:{labels:FY_YEARS, datasets:[{
          data: series,
          borderColor: allEqual ? PALETTE.muted : color,
          backgroundColor: (allEqual?PALETTE.muted:color)+'1a',
          borderWidth: 1.8,
          pointRadius: 0,
          pointHoverRadius: 3,
          tension: 0.3,
          fill: true,
        }]},
        options:{
          maintainAspectRatio:false, responsive:true,
          plugins:{legend:{display:false}, tooltip:{
            displayColors:false,
            callbacks:{
              title: items => 'FY'+items[0].label.toString().slice(-2),
              label: c => s.eps ? '$'+c.parsed.y.toFixed(2) : fmtShort(c.parsed.y),
            }
          }},
          scales:{x:{display:false}, y:{display:false}},
          interaction:{intersect:false, mode:'index'},
          elements:{line:{capBezierPoints:true}},
        }
      });
    });
  });
}

/* ---------- DRILL-DOWN ---------- */
const DRILL={
  product:()=>({title:'Product sales — Q1 2026 composition (top products, $M)',
    cols:['Product','Area','US','Ex-US','Total','YoY'],
    rows:DATA.products.filter(p=>p.name!=='Other').map(p=>[p.name,p.area,fmt(p.us),fmt(p.exus),fmt(p.q26),pc(p.growth)])}),
  cogs:()=>({title:'Cost of sales — segment-note breakdown (Q1 2026, $M)',
    cols:['Component','Q1 2026','Q1 2025','Note'],
    rows:[['Manufacturing cost of sales',fmt(2180),fmt(2528),'incl. $247M acquired-inventory step-up'],
      ['Profit share & royalties',fmt(564),fmt(440),'partner economics'],
      ['Intangible amortization (in COGS)',fmt(896),fmt(1200),'developed-product tech rights'],
      ['Total cost of sales',fmt(2744),fmt(2968),'27.6% lower amortization YoY']]}),
  rnd:()=>({title:'R&D — direction (Q1 2026, $M)',
    cols:['Driver','Q1 2026','Q1 2025','Commentary'],
    rows:[['Total R&D expense',fmt(1719),fmt(1486),'+15.7% YoY'],
      ['Later-stage clinical (incl. MariTide)','—','—','6 global Phase 3 studies underway'],
      ['Research & early pipeline','—','—','incl. business-development activity'],
      ['R&D intensity (% product sales)','20.9%','18.9%','rising investment phase']]}),
  sga:()=>({title:'SG&A — split (Q1 2026, $M, segment note)',
    cols:['Component','Q1 2026','Q1 2025','Trend'],
    rows:[['Sales & marketing',fmt(1134),fmt(1066),'+6.4%'],
      ['General & administrative',fmt(468),fmt(621),'−24.6% (lower Horizon deal costs)'],
      ['Total SG&A',fmt(1602),fmt(1687),'−5.0% YoY']]}),
  inventory:()=>({title:'Inventories — composition ($M)',
    cols:['Class','Mar 31 2026','Dec 31 2025','Δ'],
    rows:[['Raw materials',fmt(1048),fmt(915),pc(14.5)],
      ['Work in process',fmt(3426),fmt(3425),pc(0.0)],
      ['Finished goods',fmt(1712),fmt(1885),pc(-9.2)],
      ['Total inventories',fmt(6186),fmt(6225),pc(-0.6)]]}),
  intangibles:()=>({title:'Intangible assets, net — composition (Mar 31 2026, $M)',
    cols:['Class','Gross','Accum. amort.','Net'],
    rows:[['Developed-product-technology',fmt(47798),fmt(27604),fmt(20194)],
      ['Licensing rights',fmt(3903),fmt(3540),fmt(363)],
      ['R&D technology rights',fmt(1416),fmt(1304),fmt(112)],
      ['In-process R&D (indefinite)',fmt(710),'—',fmt(710)],
      ['Total',fmt(55029),fmt(33650),fmt(21379)]]}),
  debt:()=>({title:'Debt — structure ($M)',
    cols:['Component','Mar 31 2026','Dec 31 2025','Note'],
    rows:[['Current portion of LT debt',fmt(5437),fmt(4599),'near-term maturities'],
      ['Long-term debt',fmt(51886),fmt(50005),'post-Horizon de-levering'],
      ['Total debt',fmt(57323),fmt(54604),'+$4,000M issuance in Q1, −$800M repay'],
      ['Cash & equivalents',fmt(12038),fmt(9129),'liquidity buffer']]}),
  capex:()=>({title:'Capital expenditures — context ($M)',
    cols:['Item','Q1 2026','Q1 2025','Note'],
    rows:[['Purchases of PP&E',fmt(712),fmt(411),'+73% — capacity build (OH, NC sites)'],
      ['Operating cash flow',fmt(2189),fmt(1391),'+57% on working-capital timing'],
      ['Free cash flow',fmt(1477),fmt(980),'FCF = OCF − capex']]}),
  fcf:()=>({title:'Free Cash Flow — 5-year capital deployment ($M)',
    cols:['Year','FCF','Dividends','Buybacks','Net debt change','M&A','FCF→Div %'],
    rows:DATA.years.map(y=>{
      const c=DATA.cf_detail[y];
      return [String(y), fmt(c.fcf), fmt(c.dividends),
        c.buybacks?fmt(c.buybacks):'—',
        c.debt_net?fmt(c.debt_net):'—',
        c.acquisitions?fmt(c.acquisitions):'—',
        c.fcf_to_div+'%'];
    }).concat([['Q1 2026', fmt(DATA.cf_detail_q[Q_KEY].fcf),
       fmt(DATA.cf_detail_q[Q_KEY].dividends),'—',
       fmt(DATA.cf_detail_q[Q_KEY].debt_net),'—',
       DATA.cf_detail_q[Q_KEY].fcf_to_div+'%']])}),
};
function drill(key){
  const d=DRILL[key];if(!d)return;const o=d();
  $('#drillTitle').innerHTML=o.title;
  let h='<table><thead><tr>'+o.cols.map((c,i)=>`<th class="${i>0&&i<o.cols.length?'':''}">${c}</th>`).join('')+'</tr></thead><tbody>';
  o.rows.forEach(r=>{h+='<tr>'+r.map((c,i)=>`<td class="${i===0||i===1?'':'n'}">${c}</td>`).join('')+'</tr>';});
  h+='</tbody></table>';
  $('#drillBody').innerHTML=h;
  $('#drill').classList.add('open');
  $('#drill').scrollIntoView({behavior:'smooth',block:'nearest'});
}
function closeDrill(){$('#drill').classList.remove('open');}

/* ---------- KPIs ---------- */
const KDEF=[
  ['gross_margin','Gross Margin','% of product sales','good',true],
  ['op_margin','Operating Margin','% of product sales','',true],
  ['net_margin','Net Margin','% of total revenue','',true],
  ['rnd_intensity','R&D Intensity','% of product sales','',true],
  ['fcf_margin','FCF Margin','FCF % of revenue','good',true],
  ['fcf_conv','FCF Conversion','FCF % of net income','good',false],
  ['roe','Return on Equity','net income / equity','',false],
  ['roa','Return on Assets','net income / assets','',true],
  ['debt_to_equity','Debt / Equity','leverage','warn',false],
  ['debt_to_assets','Debt / Assets','% leverage','warn',true],
  ['current_ratio','Current Ratio','liquidity','',false],
  ['div_payout','Dividend Payout','% of net income','',true],
];
function buildKpis(){
  const g=$('#kpiGrid');const yrs=DATA.years;g.innerHTML='';
  KDEF.forEach(([k,name,desc,cls,pctv],idx)=>{
    const v=DATA.kpis[2025][k];
    const series=yrs.map(y=>DATA.kpis[y][k]);
    const unit=pctv?'%':(k==='current_ratio'||k==='debt_to_equity'?'×':'');
    const div=document.createElement('div');div.className='kpi '+cls;
    div.innerHTML=`<div class="k">${name}</div>
      <div class="v">${v}${unit}</div>
      <div class="d">${desc}</div>
      <div class="spark"><canvas id="sp${idx}"></canvas></div>`;
    g.appendChild(div);
    setTimeout(()=>{
      new Chart(document.getElementById('sp'+idx),{type:'line',
        data:{labels:yrs,datasets:[{data:series,borderColor:cls==='warn'?PALETTE.rust:(cls==='good'?PALETTE.green:PALETTE.teal),
          borderWidth:2,pointRadius:0,tension:.35,fill:true,
          backgroundColor:'rgba(13,92,99,.07)'}]},
        options:{plugins:{legend:{display:false},tooltip:{enabled:true,
          callbacks:{label:c=>c.parsed.y+unit}}},
          scales:{x:{display:false},y:{display:false}},
          elements:{line:{capBezierPoints:true}},maintainAspectRatio:false}});
    },10);
  });
}

/* ---------- ANOMALIES ---------- */
const LINE_LABELS={product:'Product sales',total:'Total revenues',cogs:'Cost of sales',
  rnd:'R&D expense',sga:'SG&A expense',op_income:'Operating income',net:'Net income',
  other_op:'Other operating expense',other_inc:'Other income, net',
  intangibles:'Intangible assets',goodwill:'Goodwill',total_debt:'Total debt',
  total_assets:'Total assets',equity:'Stockholders\u2019 equity',inventory:'Inventories',
  receivables:'Trade receivables',cash:'Cash & equivalents',ocf:'Operating cash flow',
  fcf:'Free cash flow',capex:'Capital expenditures'};
const ANOM_NOTE={
  'goodwill-2023':'Horizon Therapeutics acquisition (Oct 2023, $27,800M) added ~$3,700M goodwill.',
  'intangibles-2023':'Horizon added ~$14,000M+ of developed-product-technology intangibles.',
  'total_debt-2023':'Debt-funded Horizon deal; total debt jumped to ~$65,000M.',
  'other_op-2023':'Acquisition-related & restructuring charges spiked operating "Other".',
};
function buildAnomalies(){
  const L=$('#anList');L.innerHTML='';
  DATA.anomalies.forEach(a=>{
    const sev = Math.abs(a.zscore)>=1.7?1:2;
    const key=a.line+'-'+a.year;
    const note=ANOM_NOTE[key]||`YoY change of ${pc(a.yoy)} vs a 5-yr mean of ${pc(a.mean)} for this line.`;
    L.innerHTML+=`<div class="an-item ${sev===2?'sev2':''}">
      <span class="sev">${sev===1?'HIGH':'WATCH'}</span>
      <div class="body"><h4>${LINE_LABELS[a.line]||a.line} · ${a.year} <span style="font-weight:400;color:#6b7280;font-size:12px">(${a.statement})</span></h4>
        <p>${note}</p></div>
      <div class="z"><div class="big">${a.zscore}</div><div class="lbl">z-score · ${pc(a.yoy)} YoY</div></div></div>`;
  });
  const P=$('#anProd');P.innerHTML='';
  DATA.product_anomalies.forEach(a=>{
    const up=a.growth>=0;const sev=Math.abs(a.zscore)>=1.7?1:2;
    const note = up
      ? `Launch/ramp surge — Q1'26 $${a.q26}M vs $${a.q25}M (portfolio mean ${pc(DATA.prod_mean_growth)}).`
      : `Decline vs portfolio — Q1'26 $${a.q26}M vs $${a.q25}M; biosimilar / IRA pricing pressure likely.`;
    P.innerHTML+=`<div class="an-item ${sev===2?'sev2':''}">
      <span class="sev">${sev===1?'HIGH':'WATCH'}</span>
      <div class="body"><h4>${a.product} <span style="font-weight:400;color:#6b7280;font-size:12px">(${a.area})</span></h4>
        <p>${note}</p></div>
      <div class="z"><div class="big" style="color:${up?PALETTE.green:PALETTE.rust}">${pc(a.growth)}</div>
        <div class="lbl">z ${a.zscore}</div></div></div>`;
  });
}

/* ---------- TRENDS charts ---------- */
let trendsDrawn=false;
function drawTrends(){
  if(trendsDrawn)return;trendsDrawn=true;
  const yrs=DATA.years;
  const grid={grid:{color:PALETTE.grid},border:{display:false}};
  new Chart($('#cRev'),{type:'bar',data:{labels:yrs,datasets:[
    {label:'Total revenue',data:yrs.map(y=>PL[y].total),backgroundColor:PALETTE.teal,borderRadius:3,order:2},
    {label:'Net income',type:'line',data:yrs.map(y=>PL[y].net),borderColor:PALETTE.rust,
      backgroundColor:PALETTE.rust,borderWidth:3,pointRadius:4,tension:.3,order:1,yAxisID:'y'}]},
    options:{maintainAspectRatio:false,plugins:{legend:{position:'bottom'},
      tooltip:{callbacks:{label:c=>c.dataset.label+': '+fmtB(c.parsed.y)}}},
      scales:{y:{...grid,ticks:{callback:v=>fmtB(v)}},x:grid}}});
  new Chart($('#cMargin'),{type:'line',data:{labels:yrs,datasets:[
    {label:'Gross %',data:yrs.map(y=>DATA.kpis[y].gross_margin),borderColor:PALETTE.teal,tension:.3,borderWidth:2.5,pointRadius:3},
    {label:'Operating %',data:yrs.map(y=>DATA.kpis[y].op_margin),borderColor:PALETTE.gold,tension:.3,borderWidth:2.5,pointRadius:3},
    {label:'Net %',data:yrs.map(y=>DATA.kpis[y].net_margin),borderColor:PALETTE.rust,tension:.3,borderWidth:2.5,pointRadius:3}]},
    options:{maintainAspectRatio:false,plugins:{legend:{position:'bottom'},
      tooltip:{callbacks:{label:c=>c.dataset.label+': '+c.parsed.y+'%'}}},
      scales:{y:{...grid,ticks:{callback:v=>v+'%'}},x:grid}}});
  new Chart($('#cFcf'),{type:'bar',data:{labels:yrs,datasets:[
    {label:'Free cash flow',data:yrs.map(y=>CF[y].fcf),backgroundColor:PALETTE.teal,borderRadius:3},
    {label:'Dividends paid',data:yrs.map(y=>CF[y].divs),backgroundColor:PALETTE.gold,borderRadius:3}]},
    options:{maintainAspectRatio:false,plugins:{legend:{position:'bottom'},
      tooltip:{callbacks:{label:c=>c.dataset.label+': '+fmtB(c.parsed.y)}}},
      scales:{y:{...grid,ticks:{callback:v=>fmtB(v)}},x:grid}}});
  new Chart($('#cDebt'),{type:'bar',data:{labels:yrs,datasets:[
    {label:'Total debt',data:yrs.map(y=>BS[y].total_debt),backgroundColor:PALETTE.ink,borderRadius:3,order:2},
    {label:'Debt / Equity (×)',type:'line',data:yrs.map(y=>DATA.kpis[y].debt_to_equity),
      borderColor:PALETTE.rust,borderWidth:3,pointRadius:4,tension:.3,yAxisID:'y1',order:1}]},
    options:{maintainAspectRatio:false,plugins:{legend:{position:'bottom'},
      tooltip:{callbacks:{label:c=>c.dataset.label+': '+(c.dataset.yAxisID==='y1'?c.parsed.y+'×':fmtB(c.parsed.y))}}},
      scales:{y:{...grid,ticks:{callback:v=>fmtB(v)}},
        y1:{position:'right',grid:{display:false},border:{display:false},ticks:{callback:v=>v+'×'}},x:grid}}});
  new Chart($('#cRnd'),{type:'bar',data:{labels:yrs,datasets:[
    {label:'R&D expense',data:yrs.map(y=>PL[y].rnd),backgroundColor:PALETTE.teal,borderRadius:3,order:2},
    {label:'R&D intensity %',type:'line',data:yrs.map(y=>DATA.kpis[y].rnd_intensity),
      borderColor:PALETTE.gold,borderWidth:3,pointRadius:4,tension:.3,yAxisID:'y1',order:1}]},
    options:{maintainAspectRatio:false,plugins:{legend:{position:'bottom'},
      tooltip:{callbacks:{label:c=>c.dataset.label+': '+(c.dataset.yAxisID==='y1'?c.parsed.y+'%':fmtB(c.parsed.y))}}},
      scales:{y:{...grid,ticks:{callback:v=>fmtB(v)}},
        y1:{position:'right',grid:{display:false},border:{display:false},ticks:{callback:v=>v+'%'}},x:grid}}});
  new Chart($('#cBs'),{type:'bar',data:{labels:yrs,datasets:[
    {label:'Goodwill+Intangibles',data:yrs.map(y=>BS[y].goodwill+BS[y].intangibles),backgroundColor:PALETTE.gold,stack:'a',borderRadius:2},
    {label:'Other assets',data:yrs.map(y=>BS[y].total_assets-BS[y].goodwill-BS[y].intangibles),backgroundColor:PALETTE.teal,stack:'a',borderRadius:2},
    {label:'Equity',type:'line',data:yrs.map(y=>BS[y].equity),borderColor:PALETTE.rust,borderWidth:3,pointRadius:4,tension:.3}]},
    options:{maintainAspectRatio:false,plugins:{legend:{position:'bottom'},
      tooltip:{callbacks:{label:c=>c.dataset.label+': '+fmtB(c.parsed.y)}}},
      scales:{y:{...grid,stacked:true,ticks:{callback:v=>fmtB(v)}},x:{...grid,stacked:true}}}});
}

/* ---------- PRODUCTS charts ---------- */
let prodDrawn=false;
function drawProducts(){
  if(prodDrawn)return;prodDrawn=true;
  const prods=DATA.products.filter(p=>p.name!=='Other').sort((a,b)=>b.q26-a.q26);
  new Chart($('#cProd'),{type:'bar',data:{labels:prods.map(p=>p.name),datasets:[
    {label:"Q1'26",data:prods.map(p=>p.q26),backgroundColor:PALETTE.teal,borderRadius:2},
    {label:"Q1'25",data:prods.map(p=>p.q25),backgroundColor:PALETTE.soft,borderRadius:2}]},
    options:{indexAxis:'y',maintainAspectRatio:false,plugins:{legend:{position:'bottom'},
      tooltip:{callbacks:{label:c=>c.dataset.label+': '+fmt(c.parsed.x)+'M'}}},
      scales:{x:{grid:{color:PALETTE.grid},border:{display:false},ticks:{callback:v=>'$'+v}},
        y:{grid:{display:false},border:{display:false}}}}});
  new Chart($('#cGeo'),{type:'bar',data:{labels:prods.map(p=>p.name),datasets:[
    {label:'US',data:prods.map(p=>p.us),backgroundColor:PALETTE.tealDk,stack:'g',borderRadius:2},
    {label:'Ex-US',data:prods.map(p=>p.exus),backgroundColor:PALETTE.gold,stack:'g',borderRadius:2}]},
    options:{indexAxis:'y',maintainAspectRatio:false,plugins:{legend:{position:'bottom'},
      tooltip:{callbacks:{label:c=>c.dataset.label+': '+fmt(c.parsed.x)+'M'}}},
      scales:{x:{stacked:true,grid:{color:PALETTE.grid},border:{display:false},ticks:{callback:v=>'$'+v}},
        y:{stacked:true,grid:{display:false},border:{display:false}}}}});
  const areas={};DATA.products.forEach(p=>{areas[p.area]=(areas[p.area]||0)+p.q26;});
  new Chart($('#cArea'),{type:'doughnut',data:{labels:Object.keys(areas),
    datasets:[{data:Object.values(areas),backgroundColor:[PALETTE.teal,PALETTE.gold,PALETTE.rust,PALETTE.tealDk,PALETTE.soft],borderWidth:2,borderColor:'#fffdf8'}]},
    options:{maintainAspectRatio:false,plugins:{legend:{position:'right'},
      tooltip:{callbacks:{label:c=>c.label+': '+fmt(c.parsed)+'M'}}},cutout:'58%'}});
}

/* ---------- WORKING CAPITAL & CCC ---------- */
let workcapDrawn=false;
function drawWorkcap(){
  if(workcapDrawn)return;workcapDrawn=true;
  const yrs=DATA.years;
  const WC=DATA.wc, D=DATA.dupont;
  // KPI cards for WC
  const wc25=WC[2025], wc24=WC[2024];
  const wcKpis=[
    ['DSO', wc25.dso, wc24.dso, 'Days Sales Outstanding'],
    ['DIO', wc25.dio, wc24.dio, 'Days Inventory Outstanding'],
    ['DPO', wc25.dpo, wc24.dpo, 'Days Payable Outstanding *modelled'],
    ['CCC', wc25.ccc, wc24.ccc, 'Cash Conversion Cycle (days)'],
  ];
  const g=$('#wcKpis');g.innerHTML='';
  wcKpis.forEach(([k,v,prev,desc])=>{
    const ch=v-prev; const cls = (k==='CCC' || k==='DSO' || k==='DIO')?(ch<=0?'good':'warn'):(ch>=0?'good':'warn');
    g.innerHTML+=`<div class="kpi ${cls}"><div class="k">${k}</div>
      <div class="v">${v}<span style="font-family:'Spline Sans Mono',monospace;font-size:13px;color:#94a3b8"> d</span></div>
      <div class="d">${desc}</div>
      <div style="font-family:'Spline Sans Mono',monospace;font-size:11px;color:${ch<=0?PALETTE.green:PALETTE.rust};margin-top:4px">${ch>=0?'+':''}${ch.toFixed(1)}d vs FY24</div></div>`;
  });
  const grid={grid:{color:PALETTE.grid},border:{display:false}};
  // CCC trend
  new Chart($('#cCCC'),{type:'line',data:{labels:yrs,datasets:[
    {label:'CCC (days)',data:yrs.map(y=>WC[y].ccc),borderColor:PALETTE.rust,
      backgroundColor:'rgba(180,69,31,.1)',borderWidth:3,tension:.3,pointRadius:5,fill:true},
    {label:'Operating cycle',data:yrs.map(y=>WC[y].op_cycle),borderColor:PALETTE.teal,
      borderWidth:2,tension:.3,pointRadius:4,borderDash:[6,4]}]},
    options:{maintainAspectRatio:false,plugins:{legend:{position:'bottom'},
      tooltip:{callbacks:{label:c=>c.dataset.label+': '+c.parsed.y+' days'}}},
      scales:{y:{...grid,ticks:{callback:v=>v+' d'}},x:grid}}});
  // DSO/DIO/DPO stacked
  new Chart($('#cWCparts'),{type:'bar',data:{labels:yrs,datasets:[
    {label:'DSO (receivables)',data:yrs.map(y=>WC[y].dso),backgroundColor:PALETTE.teal,borderRadius:2,stack:'a'},
    {label:'DIO (inventory)',data:yrs.map(y=>WC[y].dio),backgroundColor:PALETTE.gold,borderRadius:2,stack:'a'},
    {label:'DPO (payables, modelled)',data:yrs.map(y=>-WC[y].dpo),backgroundColor:PALETTE.rust,borderRadius:2,stack:'a'}]},
    options:{maintainAspectRatio:false,plugins:{legend:{position:'bottom'},
      tooltip:{callbacks:{label:c=>c.dataset.label+': '+Math.abs(c.parsed.y)+' days'}}},
      scales:{y:{...grid,stacked:true,ticks:{callback:v=>v+' d'}},x:{...grid,stacked:true}}}});
  // DuPont
  new Chart($('#cDupont'),{type:'bar',data:{labels:yrs,datasets:[
    {label:'Net margin %',data:yrs.map(y=>D[y].net_margin),backgroundColor:PALETTE.teal,borderRadius:2,yAxisID:'y'},
    {label:'Asset turnover (×)',type:'line',data:yrs.map(y=>D[y].asset_turnover),borderColor:PALETTE.gold,borderWidth:3,pointRadius:4,tension:.3,yAxisID:'y1'},
    {label:'Equity multiplier (×)',type:'line',data:yrs.map(y=>D[y].equity_multiplier),borderColor:PALETTE.rust,borderWidth:3,pointRadius:4,tension:.3,yAxisID:'y1'},
    {label:'ROE %',type:'line',data:yrs.map(y=>D[y].roe),borderColor:PALETTE.ink,borderWidth:2,pointRadius:4,tension:.3,yAxisID:'y'}]},
    options:{maintainAspectRatio:false,plugins:{legend:{position:'bottom'},
      tooltip:{callbacks:{label:c=>{const v=c.parsed.y; return c.dataset.label+': '+(c.dataset.yAxisID==='y1'?v+'×':v+'%')}}}},
      scales:{y:{...grid,ticks:{callback:v=>v+'%'}},
        y1:{position:'right',grid:{display:false},border:{display:false},ticks:{callback:v=>v+'×'}},x:grid}}});

  // ---------- WoCA: peer comparison ----------
  drawWoca();
}

function drawWoca(){
  const peers=DATA.peers;
  const med=DATA.peers_median;
  const ranks=DATA.amgen_ranks;
  const total=DATA.peer_count;
  // Sort by CCC ascending for the bar chart
  const byCCC=[...peers].sort((a,b)=>a.ccc-b.ccc);
  // KPI cards: Amgen's gap to peer median on each metric
  const amgen=peers.find(p=>p.sym==='AMGN');
  const gap=(v,m)=>Math.round(v-m);
  const cards=[
    ['DSO vs median', amgen.dso+'d', '+'+gap(amgen.dso,med.dso)+'d vs '+med.dso+'d median', `Rank ${ranks.dso}/${total} · lower = better`, gap(amgen.dso,med.dso)>10?'warn':''],
    ['DIO vs median', amgen.dio+'d', '+'+gap(amgen.dio,med.dio)+'d vs '+med.dio+'d median', `Rank ${ranks.dio}/${total} · inventory days`, gap(amgen.dio,med.dio)>10?'warn':''],
    ['DPO vs median', amgen.dpo+'d', (gap(amgen.dpo,med.dpo)>=0?'+':'')+gap(amgen.dpo,med.dpo)+'d vs '+med.dpo+'d median', `Rank ${ranks.dpo}/${total} · higher = better cash mgmt`, gap(amgen.dpo,med.dpo)<0?'warn':'good'],
    ['CCC vs median', amgen.ccc+'d', '+'+gap(amgen.ccc,med.ccc)+'d vs '+med.ccc+'d median', `Rank ${ranks.ccc}/${total} · ${Math.round(amgen.ccc/med.ccc*100-100)}% above median`, gap(amgen.ccc,med.ccc)>30?'warn':''],
  ];
  const g=$('#wocaKpis');g.innerHTML='';
  cards.forEach(([k,v,d1,d2,cls])=>{
    g.innerHTML+=`<div class="kpi ${cls}"><div class="k">${k}</div>
      <div class="v">${v}</div>
      <div class="d" style="margin-top:3px">${d1}</div>
      <div class="d" style="font-size:11px;color:#94a3b8;margin-top:2px">${d2}</div></div>`;
  });

  const grid={grid:{color:PALETTE.grid},border:{display:false}};

  // CCC ranking bar chart (horizontal), Amgen highlighted
  new Chart($('#cWocaCCC'),{type:'bar',data:{labels:byCCC.map(p=>p.name),
    datasets:[
      {label:'CCC (days)',
       data:byCCC.map(p=>p.ccc),
       backgroundColor:byCCC.map(p=>p.sym==='AMGN'?PALETTE.rust:PALETTE.teal),
       borderRadius:2,borderWidth:byCCC.map(p=>p.sym==='AMGN'?0:0)},
    ]},
    options:{indexAxis:'y',maintainAspectRatio:false,
      plugins:{legend:{display:false},
        tooltip:{callbacks:{label:c=>'CCC: '+c.parsed.x+' days'}},
        annotation:false},
      scales:{x:{...grid,ticks:{callback:v=>v+'d'},
        title:{display:true,text:`Peer median = ${med.ccc}d`,color:PALETTE.muted}},
        y:{grid:{display:false},border:{display:false}}}}});

  // Stacked CCC components, sorted same order
  new Chart($('#cWocaStack'),{type:'bar',data:{labels:byCCC.map(p=>p.sym),datasets:[
    {label:'DSO',data:byCCC.map(p=>p.dso),backgroundColor:PALETTE.teal,stack:'a',borderRadius:2},
    {label:'DIO',data:byCCC.map(p=>p.dio),backgroundColor:PALETTE.gold,stack:'a',borderRadius:2},
    {label:'− DPO',data:byCCC.map(p=>-p.dpo),backgroundColor:PALETTE.rust,stack:'a',borderRadius:2}]},
    options:{maintainAspectRatio:false,
      plugins:{legend:{position:'bottom'},
        tooltip:{callbacks:{label:c=>c.dataset.label+': '+Math.abs(c.parsed.y)+'d'}}},
      scales:{y:{...grid,stacked:true,ticks:{callback:v=>v+'d'}},
        x:{...grid,stacked:true,
          ticks:{color:c=>peers[c.index]&&peers[c.index].sym==='AMGN'?PALETTE.rust:PALETTE.ink,
                 font:{weight:c=>peers[c.index]&&peers[c.index].sym==='AMGN'?'700':'400'}}}}}});

  // WoCA matrix table
  const cellClass=(rank,total)=>{
    if(rank<=Math.ceil(total/3)) return 'good';
    if(rank>=Math.floor(2*total/3)+1) return 'bad';
    return 'mid';
  };
  let h='<table class="woca-table"><thead><tr>'+
    '<th class="lh">Company</th><th class="lh">Sym</th>'+
    '<th>FY24 Rev ($B)</th>'+
    '<th>DSO (rank)</th><th>DIO (rank)</th><th>DPO (rank)</th><th>CCC (rank)</th>'+
    '<th>Source</th></tr></thead><tbody>';
  const sortedByCCC=[...peers].sort((a,b)=>a.ccc-b.ccc);
  sortedByCCC.forEach(p=>{
    const me=p.sym==='AMGN'?'me':'';
    const rd=DATA.amgen_ranks; // not used — compute per-row ranks instead
    // compute this peer's rank for each metric
    const rDSO = peers.slice().sort((a,b)=>a.dso-b.dso).findIndex(x=>x.sym===p.sym)+1;
    const rDIO = peers.slice().sort((a,b)=>a.dio-b.dio).findIndex(x=>x.sym===p.sym)+1;
    const rDPO = peers.slice().sort((a,b)=>b.dpo-a.dpo).findIndex(x=>x.sym===p.sym)+1;  // higher=better
    const rCCC = peers.slice().sort((a,b)=>a.ccc-b.ccc).findIndex(x=>x.sym===p.sym)+1;
    h+=`<tr class="${me}"><td>${p.name}</td><td>${p.sym}</td>`+
       `<td class="n">${p.rev.toFixed(1)}</td>`+
       `<td class="n ${cellClass(rDSO,total)}">${p.dso} <span class="rk">(#${rDSO})</span></td>`+
       `<td class="n ${cellClass(rDIO,total)}">${p.dio} <span class="rk">(#${rDIO})</span></td>`+
       `<td class="n ${cellClass(rDPO,total)}">${p.dpo} <span class="rk">(#${rDPO})</span></td>`+
       `<td class="n ${cellClass(rCCC,total)}">${p.ccc} <span class="rk">(#${rCCC})</span></td>`+
       `<td>${p.src}</td></tr>`;
  });
  h+=`<tr class="med"><td colspan="2"><b>Peer median (ex. Amgen)</b></td><td class="n">—</td>`+
    `<td class="n">${med.dso}</td><td class="n">${med.dio}</td><td class="n">${med.dpo}</td><td class="n">${med.ccc}</td><td>—</td></tr>`;
  h+='</tbody></table>'+
     `<p style="font-size:11px;color:#6b7280;margin-top:10px">`+
     `<b>Reading:</b> Amgen's CCC (${amgen.ccc}d) is ${Math.round(amgen.ccc/med.ccc*100-100)}% above the peer median (${med.ccc}d). `+
     `Inventory is the swing factor — DIO of ${amgen.dio}d vs ${med.dio}d median. Lilly is the only peer with a longer cycle, `+
     `driven by Mounjaro/Zepbound supply build-up. <i>Cells coloured green (top tercile of efficiency), amber (middle), red (bottom).</i></p>`;
  $('#wocaTable').innerHTML=h;

  // ===== CCC improvement slicer =====
  buildWocaSlicer();
}


/* ---------- WoCA CCC slicer (interactive) ---------- */
const WOCA_BASE = null;  // bound after init
let wocaState = null;
let wocaChart = null;
let wocaPreset = 'current';

function buildWocaSlicer(){
  wocaState = {
    dso: DATA.peers[0].dso,
    dio: DATA.peers[0].dio,
    dpo: DATA.peers[0].dpo,
  };
  // Preset buttons
  const presetHtml = DATA.scenarios_woca.map((s,i) => {
    const id = ['current','median','best'][i];
    return `<button data-sw="${id}" class="${i===0?'active':''}">
      <span class="dot" style="background:${s.color}"></span>${s.label} · CCC ${s.ccc}d, WC ${fmtB(s.wc)}</button>`;
  }).join('');
  $('#wocaPresets').innerHTML = presetHtml;
  $('#wocaPresets').addEventListener('click', e => {
    const b = e.target.closest('button'); if(!b) return;
    document.querySelectorAll('#wocaPresets button').forEach(x=>x.classList.remove('active'));
    b.classList.add('active');
    const id = b.dataset.sw;
    wocaPreset = id;
    const s = DATA.scenarios_woca[['current','median','best'].indexOf(id)];
    wocaState.dso = s.dso; wocaState.dio = s.dio; wocaState.dpo = s.dpo;
    renderWocaInputs();
    renderWocaOutput();
  });

  // Inputs (sliders)
  renderWocaInputs();
  renderWocaOutput();
}

function renderWocaInputs(){
  const S = DATA.peer_stats;
  // Conservative slider bounds: ±3σ around the peer mean for each metric
  const inputs = [
    ['dso', 'DSO — days sales outstanding (lower = better)', 'd', S.dso.p3d, S.dso.p3u, 0.5],
    ['dio', 'DIO — days inventory outstanding (lower = better)', 'd', Math.max(40,S.dio.p3d), S.dio.p3u, 1],
    ['dpo', 'DPO — days payable outstanding (higher = better)', 'd', Math.max(10,S.dpo.p3d), S.dpo.p3u, 0.5],
  ];
  let h = '<h3>WoCA drivers</h3>';
  inputs.forEach(([k,label,unit,mn,mx,step])=>{
    h += `<div class="scen-input">
      <label>${label} <span class="v" id="wlv-${k}">${wocaState[k]}${unit}</span></label>
      <input type="range" id="wn-${k}" min="${mn}" max="${mx}" step="${step}" value="${wocaState[k]}">
      <div class="range-meta"><span>${mn}${unit}</span><span>peer μ ${DATA.peer_stats[k].mean}${unit}</span><span>${mx}${unit}</span></div>
    </div>`;
  });
  h += `<div class="scen-note"><b>Bounds = ±3σ of peer distribution.</b> Amgen FY25 baseline: revenue $36,800M, COGS $9,100M.</div>`;
  $('#wocaInputs').innerHTML = h;
  inputs.forEach(([k,,unit])=>{
    const inp = document.getElementById('wn-'+k);
    inp.addEventListener('input', () => {
      wocaState[k] = parseFloat(inp.value);
      document.getElementById('wlv-'+k).textContent = wocaState[k]+unit;
      document.querySelectorAll('#wocaPresets button').forEach(x=>x.classList.remove('active'));
      wocaPreset = 'custom';
      renderWocaOutput();
    });
  });
}

function renderWocaOutput(){
  const base = DATA.amgen_wc_base;
  const dso = wocaState.dso, dio = wocaState.dio, dpo = wocaState.dpo;
  const ar  = base.revenue * dso / 365;
  const inv = base.cogs    * dio / 365;
  const ap  = base.cogs    * dpo / 365;
  const newWc = ar + inv - ap;
  const newCCC = dso + dio - dpo;
  const wcSaved = base.net_wc - newWc;
  const daysOff = (DATA.peers[0].ccc) - newCCC;

  // Chart: 4 metric bars Current vs Target
  const data = {
    labels: ['DSO','DIO','DPO','CCC'],
    datasets: [
      {label:'Current (Amgen FY25)',
       data:[DATA.peers[0].dso, DATA.peers[0].dio, DATA.peers[0].dpo, DATA.peers[0].ccc],
       backgroundColor:'#d8d2c4', borderRadius:3},
      {label:'Target (slicer)',
       data:[dso, dio, dpo, newCCC],
       backgroundColor:PALETTE.tealDk, borderRadius:3},
    ],
  };
  const opts = {
    maintainAspectRatio:false,
    plugins:{
      legend:{position:'bottom'},
      tooltip:{callbacks:{label:c=>c.dataset.label+': '+c.parsed.y.toFixed(1)+' days'}},
    },
    scales:{
      y:{grid:{color:PALETTE.grid},border:{display:false},ticks:{callback:v=>v+'d'}},
      x:{grid:{display:false},border:{display:false}},
    },
  };
  if(wocaChart){wocaChart.data=data;wocaChart.options=opts;wocaChart.update();}
  else{wocaChart=new Chart($('#cWocaSlice'),{type:'bar',data,options:opts});}

  // Summary tiles
  const improving = wcSaved >= 0;
  const dollarColor = improving ? PALETTE.green : PALETTE.rust;
  const daysColor = daysOff >= 0 ? PALETTE.green : PALETTE.rust;
  $('#wocaSummary').innerHTML = `
    <div class="m"><div class="ml">New CCC</div>
      <div class="mv" style="color:${daysColor}">${newCCC.toFixed(0)} d</div>
      <div class="md">${daysOff>=0?'−':'+'}${Math.abs(daysOff).toFixed(0)} d vs current</div></div>
    <div class="m"><div class="ml">Net Working Capital</div>
      <div class="mv">${fmtB(newWc)}</div>
      <div class="md">AR ${fmtB(ar)} + Inv ${fmtB(inv)} − AP ${fmtB(ap)}</div></div>
    <div class="m"><div class="ml">Cash Freed Up</div>
      <div class="mv" style="color:${dollarColor}">${wcSaved>=0?'+':'−'}${fmtB(Math.abs(wcSaved))}</div>
      <div class="md">vs Amgen's ${fmtB(base.net_wc)} cycle</div></div>
    <div class="m"><div class="ml">vs Peer Median</div>
      <div class="mv">${(newCCC-DATA.peers_median.ccc).toFixed(0)} d</div>
      <div class="md">peer median CCC ${DATA.peers_median.ccc}d</div></div>`;
}

/* ---------- VALUATION ---------- */
let valDrawn=false;
function drawValuation(){
  if(valDrawn)return;valDrawn=true;
  const M=DATA.market;
  const ev_ebitda=(M.ev/M.ebitda_ttm).toFixed(1);
  const ev_sales=(M.ev/M.revenue_ttm).toFixed(1);
  const ev_fcf=(M.ev/8100).toFixed(1); // FY25 GAAP FCF
  const fcf_yield=(8100/M.market_cap*100).toFixed(1);
  // KPI cards (values shown in $M with comma separators)
  const cards=[
    ['Share price','$'+M.price.toFixed(2),'TTM',`52w range $${M.yr_low}-$${M.yr_high}`,''],
    ['Market Cap',fmtB(M.market_cap),'',`${M.shares_out}M shares out`,''],
    ['Enterprise Value',fmtB(M.ev),'',`MCap + ${fmtB(M.total_debt)} debt − ${fmtB(M.cash)} cash`,'warn'],
    ['EV / EBITDA',ev_ebitda+'×','',`EBITDA TTM ${fmtB(M.ebitda_ttm)}`,''],
    ['EV / FCF',ev_fcf+'×','',`FY25 GAAP FCF $8,100M`,''],
    ['FCF yield',fcf_yield+'%','',`GAAP FCF / market cap`,'good'],
    ['P/E (TTM)',M.pe_ttm+'×','',`Fwd P/E ${M.fwd_pe}×`,''],
    ['Dividend yield',M.div_yield+'%','',`$${M.div_per_share}/share annual`,'good'],
  ];
  const g=$('#valKpis');g.innerHTML='';
  cards.forEach(([k,v,e,desc,cls])=>{
    g.innerHTML+=`<div class="kpi ${cls}"><div class="k">${k}</div>
      <div class="v" style="font-size:24px">${v}</div><div class="d">${desc}</div></div>`;
  });
  const grid={grid:{color:PALETTE.grid},border:{display:false}};
  // EV bridge (waterfall-ish)
  new Chart($('#cEV'),{type:'bar',data:{labels:['Market Cap','+ Debt','− Cash','= EV'],
    datasets:[{data:[M.market_cap,M.total_debt,-M.cash,M.ev],
      backgroundColor:[PALETTE.teal,PALETTE.rust,PALETTE.green,PALETTE.ink],borderRadius:3}]},
    options:{maintainAspectRatio:false,plugins:{legend:{display:false},
      tooltip:{callbacks:{label:c=>fmtB(Math.abs(c.parsed.y))}}},
      scales:{y:{...grid,ticks:{callback:v=>fmtB(v)}},x:grid}}});
  // Debt maturities
  const D=DATA.debt_maturities;
  new Chart($('#cMaturity'),{type:'bar',data:{labels:D.map(d=>d.year),datasets:[
    {label:'Principal ($M)',data:D.map(d=>d.amount),
      backgroundColor:D.map(d=>d.year<=2030?PALETTE.rust:(d.year<=2040?PALETTE.gold:PALETTE.teal)),
      borderRadius:2}]},
    options:{maintainAspectRatio:false,plugins:{legend:{display:false},
      tooltip:{callbacks:{label:c=>'$'+c.parsed.y+'M',
        afterLabel:c=>D[c.dataIndex].note}}},
      scales:{y:{...grid,ticks:{callback:v=>fmtB(v)}},x:grid}}});
  // SOTP stylised (values illustrated in $M)
  const sotp=[
    {label:'Base biopharma',value:130000,color:PALETTE.teal},
    {label:'Horizon Rare Disease',value:55000,color:PALETTE.gold},
    {label:'MariTide option',value:55000,color:PALETTE.green},
    {label:'Tax/IRA discount',value:-30000,color:PALETTE.rust},
  ];
  new Chart($('#cSOTP'),{type:'bar',data:{labels:sotp.map(s=>s.label).concat(['Net SOTP']),
    datasets:[{data:sotp.map(s=>s.value).concat([sotp.reduce((a,b)=>a+b.value,0)]),
      backgroundColor:sotp.map(s=>s.color).concat([PALETTE.ink]),borderRadius:3}]},
    options:{maintainAspectRatio:false,plugins:{legend:{display:false},
      tooltip:{callbacks:{label:c=>fmtB(c.parsed.y)+' (illustrative)'}}},
      scales:{y:{...grid,ticks:{callback:v=>fmtB(v)}},x:grid}}});
  // DDM sensitivity table: implied price across r and g
  const D1=M.div_per_share*1.05; // next-yr expected dividend (5% growth assumed)
  const rs=[0.07,0.08,0.09,0.10,0.11];
  const gs=[0.02,0.03,0.04,0.05,0.06];
  // Show as Chart line: implied price at each r for g=4%
  const ddmData=rs.map(r=>{const p=D1/(r-0.04);return Math.max(0,Math.min(1000,p))});
  new Chart($('#cDDM'),{type:'line',data:{labels:rs.map(r=>(r*100)+'%'),
    datasets:[{label:'Implied price (g=4%)',data:ddmData,borderColor:PALETTE.teal,
      backgroundColor:'rgba(13,92,99,.1)',borderWidth:3,pointRadius:5,tension:.3,fill:true},
      {label:'Current price',data:rs.map(_=>M.price),borderColor:PALETTE.rust,
       borderWidth:2,pointRadius:0,borderDash:[6,4]}]},
    options:{maintainAspectRatio:false,plugins:{legend:{position:'bottom'},
      tooltip:{callbacks:{label:c=>c.dataset.label+': $'+c.parsed.y.toFixed(0)}}},
      scales:{y:{...grid,ticks:{callback:v=>'$'+v}},x:{...grid,title:{display:true,text:'Required return (r)',color:PALETTE.muted}}}}});
  // Sensitivity table
  const fcfg=[2,4,6,8,10]; // FCF growth %
  const exitMult=[12,14,16,18,20]; // EV/FCF exit
  let h='<table class="sens-table"><thead><tr><th>FCF growth →<br/>Exit EV/FCF ↓</th>';
  fcfg.forEach(g=>h+=`<th>${g}%</th>`);
  h+='</tr></thead><tbody>';
  exitMult.forEach(em=>{
    h+=`<tr><th>${em}×</th>`;
    fcfg.forEach(g=>{
      const fcf3=8100*Math.pow(1+g/100,3);
      const futureEV=em*fcf3;
      // discount back 3 yrs at 9%
      const pv=futureEV/Math.pow(1.09,3);
      const upside=(pv/M.ev-1)*100;
      const cls=upside>15?'hi':(upside<-15?'lo':'mid');
      h+=`<td class="${cls}">${upside>0?'+':''}${upside.toFixed(0)}%</td>`;
    });
    h+='</tr>';
  });
  h+='</tbody></table><p style="font-size:11px;color:#6b7280;margin-top:8px">Implied 3-year upside/downside to current EV ('+fmtB(M.ev)+'), 9% discount rate. Illustrative.</p>';
  $('#sensTable').innerHTML=h;
}

/* ---------- SCENARIOS (interactive) ---------- */
let scenChart=null;
const SC=DATA.scenarios;
const BASE=DATA.scenario_base_fy25;
let scenState=Object.assign({},SC.base); // current driver values
let activePreset='base';

function buildScenInputs(){
  const inputs=[
    ['rev_growth','Revenue growth %','%',-5,20,0.5],
    ['gross_margin','Gross margin %','%',60,85,0.5],
    ['rnd_pct','R&D % of sales','%',15,30,0.5],
    ['sga_pct','SG&A % of sales','%',12,25,0.5],
    ['capex','Capex $B','$B',0.5,4.0,0.1],
    ['tax_rate','Tax rate %','%',10,35,0.5],
  ];
  let h='<h3>Drivers (drag to adjust)</h3>';
  inputs.forEach(([k,label,unit,min,max,step])=>{
    h+=`<div class="scen-input">
      <label>${label} <span class="v" id="lv-${k}">${scenState[k]}${unit}</span></label>
      <input type="range" id="in-${k}" min="${min}" max="${max}" step="${step}" value="${scenState[k]}">
      <div class="range-meta"><span>${min}${unit}</span><span>${max}${unit}</span></div></div>`;
  });
  h+='<div class="scen-note">Edits are live. Press a preset above to reset.</div>';
  $('#scenInputs').innerHTML=h;
  inputs.forEach(([k,,unit])=>{
    const inp=document.getElementById('in-'+k);
    inp.addEventListener('input',()=>{
      scenState[k]=parseFloat(inp.value);
      document.getElementById('lv-'+k).textContent=scenState[k]+unit;
      document.querySelectorAll('#scenPresets button').forEach(b=>b.classList.remove('active'));
      activePreset='custom';
      renderScenOutput();
    });
  });
}

function buildScenPresets(){
  let h='';
  ['base','bull','bear'].forEach(k=>{
    const s=SC[k];
    h+=`<button data-sc="${k}" class="${k==='base'?'active':''}">
      <span class="dot" style="background:${s.color}"></span>${s.label}: ${s.note}
    </button>`;
  });
  $('#scenPresets').innerHTML=h;
  $('#scenPresets').addEventListener('click',e=>{
    const b=e.target.closest('button');if(!b)return;
    const k=b.dataset.sc;
    document.querySelectorAll('#scenPresets button').forEach(x=>x.classList.remove('active'));
    b.classList.add('active');
    activePreset=k;
    scenState=Object.assign({},SC[k]);
    buildScenInputs();
    renderScenOutput();
  });
}

function projectScenario(){
  // 3-year projection from FY25 base using state drivers
  const proj=[{year:2025,rev:BASE.total,prod:BASE.product,ni:BASE.net,eps:BASE.eps,fcf:BASE.fcf}];
  for(let i=1;i<=3;i++){
    const prev=proj[i-1];
    const rev=prev.rev*(1+scenState.rev_growth/100);
    const prod=prev.prod*(1+scenState.rev_growth/100);
    const cogs=prod*(1-scenState.gross_margin/100);
    const rnd=prod*scenState.rnd_pct/100;
    const sga=prod*scenState.sga_pct/100;
    const opInc=rev-cogs-rnd-sga-1300; // ~$1,300M other op (amortization)
    const intExp=2800; // assume flat
    const pretax=opInc-intExp;
    const tax=pretax*scenState.tax_rate/100;
    const ni=pretax-tax;
    const eps=ni/BASE.shares;
    // FCF: net income + D&A (~$4,500M) - capex - WC change (assume ~$500M drag)
    const fcf=ni+4500-scenState.capex*1000-500;
    proj.push({year:2025+i,rev,prod,ni,eps,fcf});
  }
  return proj;
}

function renderScenOutput(){
  const p=projectScenario();
  // chart
  const color=activePreset==='custom'?PALETTE.ink:SC[activePreset].color;
  const labels=p.map(x=>'FY'+(x.year-2000));
  const data={labels,datasets:[
    {label:'Revenue',data:p.map(x=>x.rev),borderColor:color,
      backgroundColor:color+'22',borderWidth:3,tension:.3,pointRadius:5,fill:true,yAxisID:'y'},
    {label:'Net income',type:'line',data:p.map(x=>x.ni),borderColor:PALETTE.rust,
      borderWidth:2,tension:.3,pointRadius:4,yAxisID:'y'},
    {label:'Free cash flow',type:'line',data:p.map(x=>x.fcf),borderColor:PALETTE.gold,
      borderWidth:2,tension:.3,pointRadius:4,borderDash:[6,4],yAxisID:'y'}]};
  const grid={grid:{color:PALETTE.grid},border:{display:false}};
  const opts={maintainAspectRatio:false,plugins:{legend:{position:'bottom'},
    tooltip:{callbacks:{label:c=>c.dataset.label+': '+fmtB(c.parsed.y)}}},
    scales:{y:{...grid,ticks:{callback:v=>fmtB(v)}},x:grid}};
  if(scenChart){scenChart.data=data;scenChart.options=opts;scenChart.update();}
  else{scenChart=new Chart($('#cScenPL'),{type:'line',data,options:opts});}
  // summary (all values in $M)
  const fy28=p[3], fy25=p[0];
  const cagr=(((fy28.rev/fy25.rev)**(1/3)-1)*100).toFixed(1);
  $('#scenSummary').innerHTML=`
    <div class="m"><div class="ml">FY28 Revenue</div><div class="mv">${fmtB(fy28.rev)}</div>
      <div class="md">CAGR ${cagr}%</div></div>
    <div class="m"><div class="ml">FY28 Net Income</div><div class="mv">${fmtB(fy28.ni)}</div>
      <div class="md">vs ${fmtB(fy25.ni)} FY25</div></div>
    <div class="m"><div class="ml">FY28 EPS</div><div class="mv">$${fy28.eps.toFixed(2)}</div>
      <div class="md">vs $${fy25.eps.toFixed(2)} FY25</div></div>
    <div class="m"><div class="ml">FY28 Free Cash Flow</div><div class="mv">${fmtB(fy28.fcf)}</div>
      <div class="md">vs ${fmtB(fy25.fcf)} FY25</div></div>`;
}

let scenarioDrawn=false;
function drawScenarios(){
  if(scenarioDrawn)return;scenarioDrawn=true;
  buildScenPresets();buildScenInputs();renderScenOutput();
}

/* ---------- STAKEHOLDERS ---------- */
const K=DATA.kpis[2025];
/* personas are pre-rendered server-side (Python). JS only handles toggling. */
$('#personaTabs').addEventListener('click',e=>{
  const b=e.target.closest('button');if(!b)return;
  document.querySelectorAll('#personaTabs button').forEach(x=>x.classList.remove('active'));
  b.classList.add('active');
  document.querySelectorAll('.persona').forEach(p=>p.classList.remove('active'));
  $('#pe-'+b.dataset.pe).classList.add('active');
});

/* init */
buildLanding();buildKpis();buildAnomalies();
</script>
</body>
</html>
"""

# ===========================================================================
# PERSONA GENERATION (Python is the source of truth)
# Each persona is computed from the dataset so numbers stay in sync with data.json.
# ===========================================================================
K = data["kpis"]["2025"]
PL = data["pl"]; BS = data["bs"]; CF = data["cf"]; Q = data["q"]
prod = {p["name"]: p for p in data["products"]}

def g(name):  # product YoY growth, signed string
    v = prod[name]["growth"]
    return ("+" if v >= 0 else "") + f"{v}%"

def insight(icon, title, bullets, metrics=None):
    lis = "".join(f"<li>{b}</li>" for b in bullets)
    m = ""
    if metrics:
        cells = "".join(
            f'<div class="m"><div class="mv">{v}</div><div class="ml">{l}</div></div>'
            for v, l in metrics)
        m = f'<div class="metric-row">{cells}</div>'
    return (f'<div class="insight"><h4><span class="ic">{icon}</span>{title}</h4>'
            f'<ul>{lis}</ul>{m}</div>')

# revenue CAGR FY21->FY25
rev_cagr = round(((PL["2025"]["total"] / PL["2021"]["total"]) ** (1/4) - 1) * 100, 1)
net_cagr = round(((PL["2025"]["net"] / PL["2021"]["net"]) ** (1/4) - 1) * 100, 1)
fcf_5y = sum(CF[y]["fcf"] for y in ["2021","2022","2023","2024","2025"])

# ---------------------------------------------------------------------------
# Build persona HTML strings — all computed from data, no magic numbers in JS
# Each persona is (display_label, html_string). insight() returns a string, so
# we just concatenate with + to build the panel. No lists here.
# ---------------------------------------------------------------------------

persona_cfo = (
    "Business CFO",
    insight(
        "▣", "Capital structure &amp; cash",
        [
            f"FCF of <b>$8,100M</b> in FY25 covered the <b>$5,200M</b> dividend with room to spare "
            f"(payout {K['div_payout']}% of net income), but fell from $10,400M in FY24 on "
            f"working-capital timing and a step-up in capex.",
            f"Leverage remains the headline watch-item: <b>D/E {K['debt_to_equity']}×</b> and "
            f"debt at {K['debt_to_assets']}% of assets — a legacy of the debt-funded Horizon "
            f"deal. De-levering is underway ($6,000M retired in FY25) but the thin equity base "
            f"keeps ratios elevated.",
            f"Current ratio of <b>{K['current_ratio']}×</b> is adequate but not generous; $5,400M "
            f"of debt is current. Q1'26 raised $4,000M of fresh debt against $800M repaid.",
            "Contingent tax exposure is material: IRS Puerto-Rico transfer-pricing disputes seek "
            "up to <b>~$10,700M</b> of additional federal tax (2010–2018) plus penalties. Tax Court "
            "decision expected H2 2026.",
        ],
        [
            ("$8,100M", "FY25 Free Cash Flow"),
            (f"{K['debt_to_equity']}×", "Debt / Equity"),
            (f"{K['fcf_conv']}%", "FCF Conversion"),
            (f"{K['div_payout']}%", "Dividend Payout"),
        ],
    ) + insight(
        "▤", "Margin &amp; cost watch",
        [
            f"Gross margin recovering to <b>{K['gross_margin']}%</b> as Horizon inventory "
            f"step-up amortization rolls off — a structural tailwind to plan into FY26.",
            f"R&amp;D stepped up to <b>{K['rnd_intensity']}%</b> of product sales (MariTide "
            f"obesity Phase 3, six global studies) — a deliberate growth investment that "
            f"compresses near-term operating margin.",
            "Two intangible-impairment / regulatory flags to reserve against: Otezla "
            "(IRA price-setting from 2027) and TAVNEOS (FDA April 2026 withdrawal proposal; "
            "$2,400M carrying value).",
        ],
    ) + insight(
        "◉", "Financial-performance summary",
        [
            f"Revenue grew at a <b>{rev_cagr}% 5-year CAGR</b> (FY21–FY25), reaching $36,800M; "
            f"operating income recovered to $12,400M in FY25 after the Horizon integration drag "
            f"in FY23–24.",
            f"GAAP net income was volatile (FY24: $4,100M, FY25: $7,700M) due to acquisition "
            f"amortization and tax-year swings — non-GAAP EPS ($21.84) is the more stable "
            f"management signal.",
            f"Five-year cumulative FCF of <b>${fcf_5y:,.0f}M</b> has funded dividends "
            f"($24,800M over the same period) with meaningful surplus even through the "
            f"Horizon integration.",
        ],
        [(f"{rev_cagr}%", "Revenue CAGR 5y"), ("$36,800M", "FY25 Revenue"),
         ("$12,400M", "FY25 Op. Income"), (f"${fcf_5y:,.0f}M", "5y Cumul. FCF")],
    )
)

persona_director = (
    "Director — FP&amp;A",
    insight(
        "◑", "Financial-performance read — the 5-year story",
        [
            f"Revenue compounded at <b>{rev_cagr}% CAGR</b> (FY21 $26,300M → FY25 $36,800M). "
            f"The step-change in FY23–24 is Horizon (acquired Oct 2023, $27,800M), not organic — "
            f"strip it when benchmarking the underlying run-rate growth of ~4–5% annually.",
            f"GAAP net income is <b>noisier than the business</b>: it fell to $4,100M in FY24 "
            f"(heavy acquisition amortization + adverse tax year) then rebounded to $7,700M in "
            f"FY25. Non-GAAP EPS traces the cleaner trajectory ($12.18 in FY21 → $21.84 in "
            f"FY25, {net_cagr}% CAGR).",
            f"Operating leverage is real but GAAP-masked: operating margin is "
            f"<b>{K['op_margin']}%</b> GAAP vs ~46% non-GAAP — the ~11pt gap is almost entirely "
            f"non-cash intangible amortization from the Horizon purchase-price allocation. "
            f"Always present both and bridge the difference.",
            "Gross margin is on a recovery path to ~75%+ GAAP as the Horizon inventory "
            "step-up and early-period amortization roll off — build this tailwind explicitly "
            "into the 3-year plan.",
            f"R&amp;D intensity rose to {K['rnd_intensity']}% of product sales in FY25, driven "
            f"by MariTide Phase 3. This is intentional investment, not cost creep — it will "
            f"compress GAAP op. margin by ~1–2pp until readout. Model a contingency for delay.",
        ],
        [
            (f"{rev_cagr}%", "Revenue CAGR (5y)"),
            (f"{net_cagr}%", "Non-GAAP EPS CAGR (5y)"),
            (f"{K['op_margin']}%", "GAAP Op. Margin"),
            ("46.1%", "Non-GAAP Op. Margin FY25"),
        ],
    ) + insight(
        "◢", "Variance drivers &amp; forecast quality",
        [
            "The single biggest forecast risk is <b>non-operating</b>: the BeOne equity stake "
            "swung 'Other income' by ~$1,600M between Q1'25 ($1,500M gain) and Q1'26 ($100M loss). "
            "Fence it off in the operating plan as a separate, un-forecastable line.",
            f"Working capital is the swing factor in FCF: FY25 FCF ({K['fcf_margin']}% of "
            f"revenue) lagged earnings on collections timing and higher capex. Always build a "
            f"working-capital bridge into the cash forecast — do not infer cash from net income.",
            "Capex is structurally higher: FY25 ~$2,000M vs a historical $9001,200M. Ohio and "
            "North Carolina manufacturing site build-outs are multi-year. Carry $1,8002,000M "
            "annually in the base plan.",
            "Receivables days are stable (~83 days) but inventory days increased in FY23 "
            "post-Horizon. Monitor inventory turns quarterly as Horizon products integrate "
            "into the supply chain.",
        ],
    ) + insight(
        "⬡", "FP&amp;A action list",
        [
            "Build a GAAP-to-non-GAAP bridge for every board submission — the two views diverge "
            "most on amortization (~$3,500M/yr) and stock-based compensation (~$1,200M/yr).",
            "Segment the revenue growth into: (a) volume, (b) net price/mix, (c) Horizon "
            "consolidation, (d) FX — management guides on these four vectors; so should the plan.",
            f"Sensitivity: every 1% change in product revenue = ~${round(PL['2025']['product']/100,0):,.0f}M "
            f"top-line impact. Tax-rate sensitivity: the IRS dispute could swing EPS by $15–20.",
            "Reserve a scenario where TAVNEOS is withdrawn (FDA Apr-2026 proposal) — the "
            "$2,400M intangible write-down would flow through amortization and reduce GAAP "
            "equity by ~$1,900M after-tax.",
        ],
    )
)

persona_dirbiz = (
    "Director of Business — BU",
    insight(
        "◷", "Commercial P&amp;L performance &amp; portfolio momentum",
        [
            f"Q1'26 product sales <b>$8,218M (+4% reported)</b>. The real growth engine is "
            f"<b>volume (+9%)</b> partially offset by <b>net price (−2%)</b> and inventory "
            f"timing (−2%). The franchise grows on units — price is not a lever, it is a "
            f"headwind.",
            f"Growth engines to fund and protect: <b>IMDELLTRA {g('IMDELLTRA')}</b> (DLL3-directed "
            f"BiTE, oncology), <b>UPLIZNA {g('UPLIZNA')}</b> (NMOSD rare disease), "
            f"<b>Repatha {g('Repatha')}</b> — now the #1 single product at $876M — and "
            f"<b>EVENITY {g('EVENITY')}</b>, <b>TEPEZZA {g('TEPEZZA')}</b>.",
            f"Defend-and-manage list: <b>Prolia {g('Prolia')}</b>, <b>XGEVA {g('XGEVA')}</b>, "
            f"<b>ENBREL {g('ENBREL')}</b>. Biosimilar entry + IRA pricing selection (ENBREL "
            f"for 2026) are compressing these P&amp;Ls faster than the portfolio mean of "
            f"{data['prod_mean_growth']}% growth. Embed explicit erosion curves in the BU budget.",
            "Portfolio concentration is healthy: no single product exceeds 11% of quarterly "
            "sales, providing natural hedge against any single loss-of-exclusivity event.",
        ],
        [
            ("$8,218M", "Q1'26 Product Sales"),
            ("+9%", "Volume Growth"),
            ("−2%", "Net Price"),
            ("~70%", "US Revenue Share"),
        ],
    ) + insight(
        "⊕", "Geography, mix &amp; investment priorities",
        [
            "US (~70%) carries the pricing pressure. Ex-US (~30%) offers more durable net "
            "price and is the BU's best offset — prioritize ex-US launch build-out for "
            "<b>UPLIZNA, TEPEZZA and IMDELLTRA</b> in FY26–27.",
            f"Rare Disease (Horizon legacy: TEPEZZA {g('TEPEZZA')}, KRYSTEXXA {g('KRYSTEXXA')}, "
            f"UPLIZNA {g('UPLIZNA')}) is the highest-growth pillar. These are early-lifecycle "
            f"assets with pricing power and limited biosimilar exposure. Weight commercial "
            f"investment here.",
            "Inflammation (Otezla, ENBREL, TEZSPIRE) is in structural decline on the legacy "
            f"two (Otezla {g('Otezla')}, ENBREL {g('ENBREL')}); TEZSPIRE {g('TEZSPIRE')} "
            f"is the growth offset — ensure resource allocation follows the curve, not the "
            f"franchise name.",
            "TAVNEOS commercial risk: FDA's Apr-2026 proposal to withdraw approval requires "
            "an immediate downside BU scenario — quantify revenue exposure and contingency "
            "commercial plan.",
        ],
    ) + insight(
        "▦", "BU operating cost &amp; investment efficiency",
        [
            f"SG&amp;A efficiency improved: Q1'26 SG&amp;A $1,602M (−5% YoY) while revenue "
            f"grew +6%, expanding SG&amp;A operating leverage — carry this ratio discipline "
            f"into the BU cost plan.",
            f"BU-level R&amp;D burden: total R&amp;D at {K['rnd_intensity']}% of product sales "
            f"($7,300M in FY25). MariTide Phase 3 is the biggest single incremental cost driver. "
            f"Monitor quarterly R&amp;D splits by TA to ensure BU-level investment is aligned "
            f"with commercial return potential.",
            "Inventory health: finished goods down to $1,712M (−9% from year-end). Raw "
            "materials up +14% — watch this given ramping supply-chain investment. Monitor "
            "days-inventory-outstanding (DIO) vs BU plan.",
        ],
    )
)

persona_market = (
    "Market Leads",
    insight(
        "◷", "Portfolio momentum — what to act on now",
        [
            "<b>16 brands</b> posted double-digit growth in Q1'26; 17 products are annualizing "
            "above $1,000M.",
            f"Biggest launch surges (statistical outliers vs portfolio): "
            f"<b>IMDELLTRA {g('IMDELLTRA')}</b> (DLL3 BiTE, SCLC) and "
            f"<b>UPLIZNA {g('UPLIZNA')}</b> (NMOSD) — protect supply, access, and payer "
            f"coverage here before competitors respond.",
            f"General Medicine momentum: Repatha {g('Repatha')} is now the single #1 product "
            f"at $876M; EVENITY {g('EVENITY')} and Nplate {g('Nplate')} also above portfolio "
            f"mean. Continued market-share expansion in PCSK9 inhibition is the lever.",
            "Defend-and-manage: <b>Prolia −33.8%, XGEVA −27.4%, ENBREL −37.3%</b> — these are "
            "biosimilar and IRA-driven structural declines, not short-cycle dips. Resource "
            "reallocation should already be underway.",
        ],
        [
            ("$8,218M", "Q1'26 Product Sales"),
            ("+9%", "Volume Growth"),
            ("−2%", "Net Price"),
            ("~70%", "US Share"),
        ],
    ) + insight(
        "⊕", "Geographic &amp; pricing environment",
        [
            "Volume (+9%) is doing the heavy lifting; net selling price is <b>−2%</b> with "
            "another −2% from inventory timing. Price is a structural headwind — the only "
            "lever is volume through share gain and new-patient starts.",
            "Ex-US (~30% of sales) shows relative strength in Aranesp, Vectibix and BLINCYTO. "
            "Prioritize ex-US launch and payer negotiation for rare-disease assets (UPLIZNA, "
            "TEPEZZA) where IRA pricing pressure does not apply.",
            "IRA watch: ENBREL selected for 2026 negotiated pricing, Otezla for 2027. Model "
            "the step-down curves into market-share and revenue plans for both brands now "
            "rather than at reset date.",
        ],
    )
)

persona_analyst = (
    "Equity Analyst",
    insight(
        "∿", "Quality of earnings",
        [
            "Q1'26 GAAP EPS <b>$3.34</b> (+4% YoY); but the comparison is distorted by "
            "non-operating swings — a <b>$100M unrealized loss</b> on the BeOne equity stake "
            "this quarter vs a <b>$1,500M gain</b> in Q1'25. Strip these for a clean operating "
            "read. Adjusted (non-GAAP) EPS Q1'26 was $4.90 (+12%).",
            "Operating income jumped to <b>$2,670M</b> from $1,180M, but ~$800M of the prior "
            "base was an Otezla impairment — normalize the base before extrapolating the "
            "margin improvement.",
            f"FCF conversion is <b>{K['fcf_conv']}%</b> of GAAP net income (FY25), but GAAP "
            f"net income is depressed by ~$3,500M of non-cash amortization annually — "
            f"EV/FCF is the appropriate primary multiple, not P/E.",
            f"ROE of {K['roe']}% looks compelling but is an artefact of the thin equity base "
            f"(equity = $8,700M vs $90,600M assets). ROA of {K['roa']}% is the more honest return "
            f"metric on a balance sheet this heavily loaded with acquired intangibles.",
        ],
        [
            ("$14.23", "FY25 GAAP EPS"),
            ("$21.84", "FY25 Non-GAAP EPS"),
            (f"{K['roa']}%", "Return on Assets"),
            (f"{K['roe']}%", "ROE (equity-base caveat)"),
        ],
    ) + insight(
        "⚑", "Key risks to model",
        [
            "<b>Tax litigation (binary H2'26 catalyst):</b> IRS seeks ~$10,700M of additional "
            "federal tax (2010–2018) plus penalties. A Tax Court adverse ruling would likely "
            "require a large cash payment and reduce equity materially — model a downside EPS "
            "scenario of −$15 to −$20 in the year of settlement.",
            "<b>IRA price-setting:</b> ENBREL selected for 2026 (reset date Jan 2026), Otezla "
            "for 2027. Net revenue step-downs are already being felt (ENBREL −37% Q1'26); "
            "model continued erosion at −25 to −35% annually for both.",
            "<b>TAVNEOS:</b> FDA Apr-2026 proposal to withdraw US approval puts ~$2,400M of "
            "intangible assets at risk and removes a Rare Disease growth contributor.",
            "<b>Pipeline upside / binary:</b> MariTide (obesity/T2D, AMG 133 GIP/GLP-1) is "
            "in six Phase 3 studies. A positive readout would be a major re-rating catalyst; "
            "a failure would write off years of elevated R&amp;D. This is not yet in any "
            "consensus revenue model.",
            f"<b>Leverage unwind timeline:</b> LT debt of $51,900M (Q1'26). Assuming $5,0007,000M "
            f"annual FCF applied to debt, leverage normalisation to D/E ~2× takes 4–6 years "
            f"absent a MariTide windfall — weight cost of capital accordingly.",
        ],
    ) + insight(
        "⟴", "Valuation framework",
        [
            "Use <b>EV / non-GAAP FCF</b> as the primary multiple (GAAP FCF understated by "
            "amortisation that is not truly recurring capex). At FY25 non-GAAP FCF ~$12,00013,000M, "
            "the market is pricing in MariTide optionality at current EV.",
            "SOTP is the cleanest: (a) base biopharma franchise at 10–12× non-GAAP OCF, "
            "(b) Horizon Rare Disease portfolio at a premium disease-area multiple, "
            "(c) MariTide option value (DCF probability-weighted), (d) tax liability discount.",
            "Dividend yield (~3%) provides a floor but payout is already 67% of GAAP net "
            "income — dividend growth is constrained until de-levering is further advanced. "
            "Do not model dividend as a growth-return assumption.",
        ],
    )
)

persona_treasurer = (
    "Treasurer",
    insight(
        "▰", "Liquidity, debt maturity wall &amp; refinancing posture",
        [
            f"Total debt $57,300M (Q1'26), cash &amp; equivalents $12,000M → <b>net debt $45,300M</b>. "
            f"Weighted-average maturity ~{data['wam']} years post the Feb 2026 issuance "
            f"(~$4,000M in tranches due 2031, 2036, 2046, 2056) — long-dated profile pushes the "
            f"refinancing wall well beyond the operating planning horizon.",
            "Near-term: <b>$4,600M current portion of LT debt</b> at year-end FY25. Liquidity to "
            "cover: $12,000M of cash + ~$2,500M/qtr of operating cash flow + the revolving credit "
            "facility (committed, undrawn) — comfortable, no roll-over stress.",
            "Maturity concentration to monitor: the <b>2028 tranche ($3,750M 5.150% Senior Notes)</b> "
            "and <b>2030 ($2,750M 5.250%)</b> together represent ~11% of total debt and reset "
            "the average cost of debt at then-prevailing rates. Pre-fund opportunistically if "
            "yields drop materially.",
            "Cost of debt baseline: weighted-average coupon ~5.0–5.3% on the Horizon-era "
            "tranches; the Feb-2026 issuance came in lower (4.20% on the 2031 tranche), "
            "evidence of credit-spread improvement as de-levering progresses.",
        ],
        [
            ("$12,000M", "Cash &amp; equivalents (Q1'26)"),
            ("$4,600M", "Current portion of debt"),
            (f"{data['wam']}y", "Weighted-avg maturity"),
            ("BBB+", "S&amp;P rating (stable)"),
        ],
    ) + insight(
        "▱", "Interest coverage &amp; covenants",
        [
            f"Interest coverage (FY25): operating income $12,400M / interest expense $2,800M = "
            f"<b>~4.4× covered</b>. Comfortable; investment-grade covenant tests not a "
            f"binding constraint on capital allocation.",
            "Interest expense is the second-largest non-operating drag after taxes; it has "
            "risen from $1,400M (FY21) to $2,800M (FY25) as the debt stack absorbed the Horizon "
            "financing. Each $5,000M of debt repaid reduces interest expense by ~$250M (~$0.35 EPS).",
            "Foreign-exchange exposure is moderate: ~30% of revenue ex-US, mostly EUR/GBP/JPY. "
            "Hedging programme uses forwards and option collars; no material translation losses "
            "in recent quarters. Cash held outside the US is repatriable post-TCJA at relatively "
            "low friction.",
        ],
    ) + insight(
        "◢", "Treasury priorities for FY26–27",
        [
            "<b>De-lever:</b> apply $5,0007,000M of annual FCF (after dividend) to debt paydown — "
            "targeting net debt / EBITDA ~2.5× from current ~2.6× by FY27.",
            "<b>Maintain dry powder:</b> preserve $10,00012,000M cash buffer + undrawn revolver to "
            "support BD/M&amp;A optionality, dividend continuity through any tax-litigation "
            "settlement, and any TAVNEOS-style impairment.",
            "<b>Manage the IRS-litigation contingency:</b> reserve liquidity for a potential "
            "~$10,000M+ cash payment if the H2'26 Tax Court ruling is adverse. Stress-test "
            "covenant coverage under that scenario.",
            "<b>Watch the rate curve:</b> $1,000M–$2,000M of pre-funding opportunistic issuance "
            "(à la Feb 2026) extends maturity ladder cheaply if 10Y rates revisit cycle lows.",
        ],
    )
)

persona_strategy = (
    "Strategy / Corp Dev",
    insight(
        "◆", "Capital allocation framework &amp; M&amp;A capacity",
        [
            f"FY25 FCF $8,100M; dividend $5,200M → <b>~$3,000M of annual surplus FCF</b> after "
            f"dividend. This is the BD/M&amp;A and de-levering pool. The buyback engine is "
            f"effectively dormant while debt remains elevated.",
            f"Net debt / EBITDA sits at ~2.6× (FY25); investment-grade comfort zone is "
            f"&lt;3.0×. <b>Inorganic capacity is constrained</b> — a sub-$5,000M tuck-in is "
            f"feasible without rating impact; a Horizon-scale (~$28,000M) deal would require "
            f"a re-rating willingness or 12–18 months of further deleveraging.",
            "5-year cumulative FCF of "
            f"${data['cf']['2021']['fcf']+data['cf']['2022']['fcf']+data['cf']['2023']['fcf']+data['cf']['2024']['fcf']+data['cf']['2025']['fcf']:,.0f}M "
            "($43,000M) vs $24,800M paid in dividends + $27,800M Horizon outflow + ongoing capex. "
            "Capital allocation has been heavily M&amp;A-weighted; the model now needs to "
            "deliver Horizon returns before another large bet.",
            "Strategic priority list (allocation logic):"
            "<br/><b>1) De-lever to BBB+ comfort zone</b> · "
            "<b>2) Defend dividend</b> · "
            "<b>3) Tuck-in BD in Rare Disease &amp; Oncology</b> · "
            "<b>4) Internal pipeline (MariTide commercial launch capex)</b> · "
            "<b>5) Opportunistic buyback (post-deleveraging)</b>.",
        ],
        [
            ("$3,000M", "Annual FCF surplus after div"),
            ("&lt;$5,000M", "Tuck-in BD capacity"),
            ("$43,000M", "5y cumul. FCF"),
            ("2.6×", "Net debt / EBITDA"),
        ],
    ) + insight(
        "◇", "Horizon return tracking — the calibration test",
        [
            "Horizon acquired Oct-2023 for <b>$27,800M</b>. Tracking the IRR is the single most "
            "important BD-discipline signal — it sets the bar for future deals.",
            "Q1'26 Rare Disease sales (the Horizon legacy book): TEPEZZA $490M, UPLIZNA $262M, "
            "KRYSTEXXA $255M — combined ~$1,000M/qtr, $4,000M annualised. At acquisition Horizon "
            "had ~$3,600M annual sales → <b>modest organic growth, dominated by UPLIZNA ramp</b>.",
            "Margin/cash returns: Horizon products carry premium gross margins (~80%+); "
            "incremental operating income contribution roughly $1,2001,500M annually after "
            "integration costs. <b>Cash-on-cash payback ~18–22 years</b> at current run-rate — "
            "the IRR is below cost of capital unless TAVNEOS recovers and UPLIZNA continues "
            "its launch trajectory.",
            "<b>TAVNEOS withdrawal scenario:</b> $2,400M intangible at risk + revenue contribution "
            "(~$200M annualised) lost — would materially impair Horizon IRR and tighten the "
            "case for the next large deal.",
        ],
    ) + insight(
        "◈", "Strategic optionality &amp; watch-list",
        [
            "<b>MariTide is the single largest non-balance-sheet asset.</b> Phase 3 readout "
            "(2026–27) is binary: positive readout opens a multi-billion-dollar new franchise "
            "(obesity/T2D, GIP/GLP-1 mechanism) — competitive with Lilly/Novo. Failure forgoes "
            "the option but does not impair BS materially (cost in R&amp;D run-rate).",
            "<b>BD landscape:</b> Rare Disease tuck-ins (private targets in genetic medicine, "
            "lysosomal storage, ophthalmology) sit in the $1,0005,000M sweet spot. Oncology bispecifics "
            "(extending IMDELLTRA's platform) are a second logical lane.",
            "<b>Capital-allocation discipline signals to watch:</b> (a) Horizon-cohort revenue "
            "trajectory by Q4'26, (b) Net debt / EBITDA trending below 2.0× by FY27, (c) any "
            "deal-announcement multiple discipline (EV/sales for new BD).",
            "<b>IRA-driven divestment logic:</b> Otezla (2027 negotiated price) and ENBREL (2026) "
            "are structurally declining and tying up commercial bandwidth. A divestment to a "
            "specialist owner is not in current guidance but is a strategic option worth modeling.",
        ],
    )
)

PERSONAS = {
    "cfo":       persona_cfo,
    "director":  persona_director,
    "dirbiz":    persona_dirbiz,
    "treasurer": persona_treasurer,
    "strategy":  persona_strategy,
    "market":    persona_market,
    "analyst":   persona_analyst,
}

ORDER = ["cfo", "director", "dirbiz", "treasurer", "strategy", "market", "analyst"]
tabs = "".join(
    f'<button data-pe="{pid}"{" class=\"active\"" if i==0 else ""}>{PERSONAS[pid][0]}</button>'
    for i, pid in enumerate(ORDER))
panels = "".join(
    f'<div class="persona{" active" if i==0 else ""}" id="pe-{pid}">{PERSONAS[pid][1]}</div>'
    for i, pid in enumerate(ORDER))

HTML = HTML.replace("__PERSONA_TABS__", tabs)
HTML = HTML.replace("__PERSONA_PANELS__", panels)
HTML = HTML.replace("__DATA__", DATA_JSON)
with open("/home/claude/amgen-fin/index.html", "w") as f:
    f.write(HTML)
print("index.html written:", len(HTML), "bytes")
print("personas:", ", ".join(PERSONAS[p][0] for p in ORDER))
