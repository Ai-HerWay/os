#!/usr/bin/env python3
"""
Tool Stack Audit, Dashboard Builder
===================================
Takes the audit JSON an AI produced (the schema in SKILL.md) and writes a
single self-contained, on-brand HTML dashboard: the whole stack on a page,
the money picture, the four lenses (cut, streamline, maximise, add), the
AI-leverage map, the pay-twice-for-AI check, the security pass, and the
30-day plan. No external dependencies, no internet needed to view.

Usage:
    python3 build_dashboard.py tool_stack.json [--out Tool_Stack_Audit.html] [--title "..."]
"""
import json, argparse, html

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
  :root{
    --charcoal:#252620; --linen:#F1EAE1; --forest:#22392C; --sage:#C0CACE; --clay:#876553;
    --paper:#FBF8F4; --line:#252620; --good:#3F6B4E; --warn:#B07B3E; --bad:#9A4B3B;
  }
  *{box-sizing:border-box}
  html,body{margin:0;background:var(--linen);color:var(--charcoal);
    font-family:'DM Sans','Nexa',-apple-system,Segoe UI,Helvetica,Arial,sans-serif;
    -webkit-font-smoothing:antialiased;font-size:15px;line-height:1.5}
  h1,h2,h3,.serif{font-family:'Noto Serif Display',Georgia,'Times New Roman',serif;font-weight:600}
  a{color:var(--forest)}
  .wrap{max-width:1180px;margin:0 auto;padding:28px 22px 80px}
  .top{background:var(--forest);color:var(--linen);border:2px solid var(--charcoal);
    padding:26px 28px;margin-bottom:22px}
  .top .eyebrow{letter-spacing:.18em;text-transform:uppercase;font-size:11px;opacity:.8;margin-bottom:8px}
  .top h1{margin:0 0 6px;font-size:30px;color:var(--linen)}
  .top p{margin:6px 0 0;max-width:760px;opacity:.92}
  .top .facts{display:flex;flex-wrap:wrap;gap:8px 18px;margin-top:14px;font-size:13px}
  .top .facts b{font-weight:600}
  .goals{margin:12px 0 0;padding:0;list-style:none;display:flex;flex-wrap:wrap;gap:8px}
  .goals li{background:rgba(241,234,225,.12);border:1px solid rgba(241,234,225,.35);
    padding:4px 11px;border-radius:20px;font-size:12px}
  .meta{font-size:12px;opacity:.75;margin-top:14px}
  .kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:0;border:2px solid var(--charcoal);margin-bottom:22px;background:var(--paper)}
  .kpi{padding:16px 18px;border-right:2px solid var(--charcoal)}
  .kpi:last-child{border-right:none}
  .kpi .n{font-family:'Noto Serif Display',Georgia,serif;font-size:30px;line-height:1}
  .kpi .l{font-size:11px;text-transform:uppercase;letter-spacing:.08em;opacity:.7;margin-top:6px}
  .section{border:2px solid var(--charcoal);background:var(--paper);margin-bottom:22px}
  .section > h2{margin:0;padding:14px 18px;background:var(--charcoal);color:var(--linen);font-size:16px}
  .section .body{padding:18px}
  .muted{opacity:.65;font-size:12px}
  .empty{opacity:.6;font-size:13px;font-style:italic}
  table{width:100%;border-collapse:collapse;font-size:13px}
  th,td{text-align:left;padding:9px 10px;border-bottom:1px solid #d9d0c4;vertical-align:top}
  th{background:var(--linen);font-size:11px;text-transform:uppercase;letter-spacing:.06em}
  td .src{font-size:11px;opacity:.6;margin-top:3px}
  /* verdict + status badges */
  .badge{display:inline-block;font-size:11px;font-weight:600;padding:2px 9px;border:1.5px solid var(--charcoal);border-radius:20px;white-space:nowrap}
  .v-keep{background:#D7E6DC;color:var(--good);border-color:var(--good)}
  .v-maximise{background:#F1E2D2;color:var(--clay);border-color:var(--clay)}
  .v-streamline{background:#DCE3E6;color:#3C5560;border-color:#3C5560}
  .v-cut{background:#EBC9C0;color:var(--bad);border-color:var(--bad)}
  .s-ok{background:#D7E6DC;color:var(--good);border-color:var(--good)}
  .s-action{background:#F1E2D2;color:var(--warn);border-color:var(--warn)}
  .s-unknown{background:#E8E2D8;color:#6c675c;border-color:#9a948a}
  .c-high{background:#D7E6DC;color:var(--good);border-color:var(--good)}
  .c-medium{background:#F1E2D2;color:var(--warn);border-color:var(--warn)}
  .c-low{background:#E8E2D8;color:#6c675c;border-color:#9a948a}
  /* money bars */
  .moneyline{font-size:14px;margin:0 0 16px}
  .moneyline b{font-family:'Noto Serif Display',Georgia,serif}
  .bars{margin:6px 0 0}
  .bar{display:flex;align-items:center;gap:10px;font-size:13px;margin:7px 0}
  .bar .lab{width:170px;flex-shrink:0}
  .track{flex:1;height:16px;background:#E8DFD3;border:1px solid var(--charcoal);position:relative}
  .fill{height:100%;background:var(--forest)}
  .bar .amt{width:90px;text-align:right;flex-shrink:0;font-variant-numeric:tabular-nums}
  /* lens blocks */
  .lenses{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:0;border-top:2px solid var(--charcoal);border-left:2px solid var(--charcoal)}
  .lens{border-right:2px solid var(--charcoal);border-bottom:2px solid var(--charcoal);padding:14px 16px;background:var(--paper)}
  .lens h3{margin:0 0 4px;font-size:15px;display:flex;align-items:center;gap:8px}
  .lens .tag{font-size:10px;text-transform:uppercase;letter-spacing:.08em;padding:2px 8px;border-radius:12px}
  .lens ul{margin:8px 0 0;padding-left:0;list-style:none}
  .lens li{border-top:1px solid #e2d9cc;padding:9px 0}
  .lens li:first-child{border-top:none}
  .lens .name{font-weight:600}
  .lens .why{font-size:12px;color:#5d5a50;margin-top:3px}
  .lens .save{font-size:12px;color:var(--good);font-weight:600;margin-top:3px}
  .lens .feat{display:inline-block;font-size:11px;background:var(--linen);border:1px solid #cfc6b8;
    border-radius:12px;padding:1px 8px;margin:4px 4px 0 0}
  .plain-list{margin:0;padding-left:18px}
  .plain-list li{margin:6px 0}
  .foot{font-size:12px;opacity:.7;margin-top:18px;text-align:center}
</style>
</head>
<body>
<div class="wrap">

  <div class="top">
    <div class="eyebrow">AI Her Way · Tool Stack Audit</div>
    <h1>__TITLE__</h1>
    <p>Your whole software stack on a page: what each tool is for, what it really costs, where two tools do one job, what your AI workspace already covers, and the smallest, sharpest stack that does the job.</p>
    <div class="facts">
      <span><b>Owner:</b> <span id="ownerLabel"></span></span>
      <span><b>Main AI workspace:</b> <span id="aiWorkspace"></span></span>
    </div>
    <ul class="goals" id="goals"></ul>
    <div class="meta">Generated <span id="genDate"></span> · advice based on research at a point in time. Re-run each quarter.</div>
  </div>

  <div class="kpis" id="kpis"></div>

  <div class="section">
    <h2>Your stack on a page</h2>
    <div class="body">
      <table>
        <thead><tr>
          <th>Tool</th><th>Category</th><th>Job</th><th>Tier</th>
          <th>Monthly</th><th>Usage</th><th>Verdict</th><th>Reason</th>
        </tr></thead>
        <tbody id="stack"></tbody>
      </table>
    </div>
  </div>

  <div class="section">
    <h2>The money</h2>
    <div class="body">
      <p class="moneyline" id="moneyLine"></p>
      <div class="muted" style="margin-bottom:4px">Monthly spend by category</div>
      <div class="bars" id="moneyBars"></div>
    </div>
  </div>

  <div class="section">
    <h2>What to do</h2>
    <div class="body"><div class="lenses" id="lenses"></div></div>
  </div>

  <div class="section">
    <h2>What your AI could already do</h2>
    <div class="body">
      <table>
        <thead><tr><th>You currently pay for</th><th>Your AI could do it</th><th>Using</th><th>Confidence</th></tr></thead>
        <tbody id="aiLeverage"></tbody>
      </table>
    </div>
  </div>

  <div class="section">
    <h2>Paying twice for AI</h2>
    <div class="body" id="payTwice"></div>
  </div>

  <div class="section">
    <h2>Security pass</h2>
    <div class="body" id="security"></div>
  </div>

  <div class="section">
    <h2>Your next 30 days</h2>
    <div class="body">
      <table>
        <thead><tr><th>Action</th><th>By when</th><th>Impact</th></tr></thead>
        <tbody id="plan"></tbody>
      </table>
    </div>
  </div>

  <div class="foot">Tool Stack Audit · AI Her Way · advice based on research at a point in time. You own the files and make every change.</div>
</div>

<script>
const DATA = __DATA__;
const S = DATA.summary || {};
const CUR = S.currency || "AUD";

const esc = s => (s==null?"":String(s)).replace(/[&<>"]/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[m]));
const arr = x => Array.isArray(x) ? x : [];
function money(n){
  const v = (typeof n === "number" && isFinite(n)) ? n : 0;
  const rounded = Math.round(v*100)/100;
  const txt = Number.isInteger(rounded) ? String(rounded) : rounded.toFixed(2);
  return "$" + txt;
}
function perMo(n){ return money(n) + "/mo"; }
function perYr(n){ return money(n) + "/yr"; }
function num(n){ return (typeof n === "number" && isFinite(n)) ? n : 0; }

/* ---------- header ---------- */
document.getElementById('ownerLabel').textContent = S.owner_label || "Not set";
document.getElementById('aiWorkspace').textContent = S.ai_workspace || "Not set";
document.getElementById('genDate').textContent = S.generated || "";
(function(){
  const goals = arr(S.goals).filter(Boolean);
  const el = document.getElementById('goals');
  if(!goals.length){ el.style.display='none'; return; }
  el.innerHTML = goals.map(g=>`<li>${esc(g)}</li>`).join('');
})();

/* ---------- KPI row ---------- */
(function(){
  const kpis = [
    {n: perMo(S.monthly_total), l:"Monthly total"},
    {n: perYr(S.annual_total), l:"Annual total"},
    {n: perMo(S.projected_monthly_saving), l:"Projected saving"},
    {n: String(num(S.tool_count)), l:"Tools in stack"},
    {n: String(num(S.cut_count)), l:"To cut"}
  ];
  document.getElementById('kpis').innerHTML = kpis.map(k=>
    `<div class="kpi"><div class="n">${esc(k.n)}</div><div class="l">${esc(k.l)}</div></div>`).join('');
})();

/* ---------- stack table ---------- */
(function(){
  const tools = arr(DATA.tools);
  const tb = document.getElementById('stack');
  if(!tools.length){
    tb.innerHTML = `<tr><td colspan="8" class="empty">No tools captured.</td></tr>`;
    return;
  }
  tb.innerHTML = tools.map(t=>{
    const v = (t.verdict||"").toLowerCase();
    const vClass = ["keep","maximise","streamline","cut"].includes(v) ? "v-"+v : "v-keep";
    const vLabel = t.verdict ? esc(t.verdict) : "keep";
    const sources = arr(t.sources).filter(Boolean);
    let srcNote = "";
    if(sources.length === 1){ srcNote = `<div class="src">source: ${esc(sources[0])}</div>`; }
    else if(sources.length > 1){ srcNote = `<div class="src">${sources.length} sources</div>`; }
    return `<tr>
      <td><strong>${esc(t.name)}</strong></td>
      <td>${esc(t.category)}</td>
      <td>${esc(t.job)}</td>
      <td>${esc(t.tier)}</td>
      <td>${esc(perMo(t.monthly_cost))}</td>
      <td>${esc(t.usage)}</td>
      <td><span class="badge ${vClass}">${vLabel}</span></td>
      <td>${esc(t.reason)}${srcNote}</td>
    </tr>`;
  }).join('');
})();

/* ---------- the money ---------- */
(function(){
  const tools = arr(DATA.tools);
  const line = document.getElementById('moneyLine');
  line.innerHTML = `You spend <b>${esc(perMo(S.monthly_total))}</b> (<b>${esc(perYr(S.annual_total))}</b>). `
    + `Roughly <b>${esc(perMo(S.monthly_waste))}</b> a month is waste. `
    + `Following the cut and streamline moves projects a saving of <b>${esc(perMo(S.projected_monthly_saving))}</b> (<b>${esc(perYr(num(S.projected_monthly_saving)*12))}</b>).`;

  const bars = document.getElementById('moneyBars');
  if(!tools.length){ bars.innerHTML = `<div class="empty">No spend to chart.</div>`; return; }
  const byCat = {};
  tools.forEach(t=>{
    const cat = t.category || "Uncategorised";
    byCat[cat] = (byCat[cat]||0) + num(t.monthly_cost);
  });
  const rows = Object.entries(byCat).sort((a,b)=>b[1]-a[1]);
  const max = Math.max(1, ...rows.map(r=>r[1]));
  bars.innerHTML = rows.map(([cat,val])=>{
    const pct = Math.round(100*val/max);
    return `<div class="bar">
      <span class="lab">${esc(cat)}</span>
      <div class="track"><div class="fill" style="width:${pct}%"></div></div>
      <span class="amt">${esc(perMo(val))}</span>
    </div>`;
  }).join('');
})();

/* ---------- what to do (four lenses) ---------- */
(function(){
  const r = DATA.recommendations || {};
  const cut = arr(r.cut), streamline = arr(r.streamline), maximise = arr(r.maximise), add = arr(r.add);

  function block(title, tagColour, items, render){
    const inner = items.length
      ? `<ul>${items.map(render).join('')}</ul>`
      : `<p class="empty" style="margin:8px 0 0">Nothing flagged.</p>`;
    return `<div class="lens">
      <h3><span class="tag" style="background:${tagColour};color:#fff">${esc(title)}</span></h3>
      ${inner}
    </div>`;
  }

  const cutHtml = block("Cut", "var(--bad)", cut, c=>`<li>
    <div class="name">${esc(c.tool)}</div>
    <div class="why">${esc(c.why)}</div>
    <div class="save">Saves ${esc(perMo(c.monthly_saving))}</div>
  </li>`);

  const streamHtml = block("Streamline", "#3C5560", streamline, s=>{
    const tools = arr(s.tools).filter(Boolean).join(" + ") || "(tools)";
    return `<li>
      <div class="name">${esc(tools)}</div>
      <div class="why">Keep <strong>${esc(s.keep)}</strong>. ${esc(s.why)}</div>
      <div class="save">Saves ${esc(perMo(s.monthly_saving))}</div>
    </li>`;
  });

  const maxHtml = block("Maximise", "var(--clay)", maximise, m=>{
    const feats = arr(m.missing).filter(Boolean).map(f=>`<span class="feat">${esc(f)}</span>`).join('');
    return `<li>
      <div class="name">${esc(m.tool)}</div>
      <div class="why">${esc(m.why)}</div>
      ${feats ? `<div>${feats}</div>` : ''}
    </li>`;
  });

  const addHtml = block("Add", "var(--forest)", add, a=>`<li>
    <div class="name">${esc(a.tool_or_feature)}</div>
    <div class="why">Fills: ${esc(a.fills_gap)}</div>
    ${a.note ? `<div class="why">${esc(a.note)}</div>` : ''}
  </li>`);

  document.getElementById('lenses').innerHTML = cutHtml + streamHtml + maxHtml + addHtml;
})();

/* ---------- AI leverage ---------- */
(function(){
  const rows = arr(DATA.ai_leverage);
  const tb = document.getElementById('aiLeverage');
  if(!rows.length){ tb.innerHTML = `<tr><td colspan="4" class="empty">No AI-leverage items.</td></tr>`; return; }
  tb.innerHTML = rows.map(a=>{
    const c = (a.confidence||"").toLowerCase();
    const cClass = ["high","medium","low"].includes(c) ? "c-"+c : "c-low";
    const cLabel = a.confidence ? esc(a.confidence) : "low";
    return `<tr>
      <td>${esc(a.currently_paying_for)}</td>
      <td>${esc(a.your_ai_could_do_it)}</td>
      <td>${esc(a.tool)}</td>
      <td><span class="badge ${cClass}">${cLabel}</span></td>
    </tr>`;
  }).join('');
})();

/* ---------- pay twice for AI ---------- */
(function(){
  const rows = arr(DATA.pay_twice_for_ai);
  const el = document.getElementById('payTwice');
  if(!rows.length){ el.innerHTML = `<p class="empty" style="margin:0">No double-paying for AI found. Good.</p>`; return; }
  el.innerHTML = `<ul class="plain-list">${rows.map(p=>`<li>${esc(p.note)}</li>`).join('')}</ul>`;
})();

/* ---------- security pass ---------- */
(function(){
  const rows = arr(DATA.security);
  const el = document.getElementById('security');
  if(!rows.length){ el.innerHTML = `<p class="empty" style="margin:0">No security checks recorded.</p>`; return; }
  el.innerHTML = `<table><thead><tr><th>Status</th><th>Check</th><th>Note</th></tr></thead><tbody>${
    rows.map(s=>{
      const st = (s.status||"").toLowerCase();
      const stClass = ["ok","action","unknown"].includes(st) ? "s-"+st : "s-unknown";
      const stLabel = s.status ? esc(s.status) : "unknown";
      return `<tr>
        <td><span class="badge ${stClass}">${stLabel}</span></td>
        <td>${esc(s.check)}</td>
        <td>${esc(s.note)}</td>
      </tr>`;
    }).join('')
  }</tbody></table>`;
})();

/* ---------- 30-day plan ---------- */
(function(){
  const rows = arr(DATA.plan);
  const tb = document.getElementById('plan');
  if(!rows.length){ tb.innerHTML = `<tr><td colspan="3" class="empty">No plan items yet.</td></tr>`; return; }
  tb.innerHTML = rows.map(p=>`<tr>
    <td><strong>${esc(p.action)}</strong></td>
    <td>${esc(p.by_when)}</td>
    <td>${esc(p.impact)}</td>
  </tr>`).join('');
})();
</script>
</body>
</html>"""


def main():
    ap = argparse.ArgumentParser(description="Render a Tool Stack Audit HTML dashboard from audit JSON.")
    ap.add_argument("data")
    ap.add_argument("--out", default="Tool_Stack_Audit.html")
    ap.add_argument("--title", default="My Tool Stack Audit")
    args = ap.parse_args()

    with open(args.data, encoding="utf-8") as f:
        d = json.load(f)

    out = (TEMPLATE
        .replace("__TITLE__", html.escape(args.title))
        .replace("__DATA__", json.dumps(d, ensure_ascii=False)))

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"Wrote dashboard -> {args.out} ({len(out)//1024} KB)")


if __name__ == "__main__":
    main()
