#!/usr/bin/env python3
"""
Hub Gap-Finder & Sync, Dashboard Builder
=========================================
Takes the report JSON an AI produced (the schema in SKILL.md) and writes a
single self-contained, on-brand HTML dashboard: where the student's library
stands against the AI for Impact Hub catalogue. Updates to sync, gaps worth
adding (by department), what they are up to date on, their own custom skills
to keep, and a recommended order. No external dependencies, no internet
needed to view.

Usage:
    python3 build_dashboard.py hub_gap_report.json [--out Hub_Gap_Report.html] [--title "..."]
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
  .meta{font-size:12px;opacity:.78;margin-top:14px}
  .cat-line{font-size:12px;opacity:.85;margin-top:8px}
  .caution{margin-top:8px;font-size:12px;background:rgba(241,234,225,.14);
    border:1px solid rgba(241,234,225,.4);border-radius:6px;padding:7px 11px;display:inline-block}
  .kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:0;border:2px solid var(--charcoal);margin-bottom:22px;background:var(--paper)}
  .kpi{padding:16px 18px;border-right:2px solid var(--charcoal)}
  .kpi:last-child{border-right:none}
  .kpi .n{font-family:'Noto Serif Display',Georgia,serif;font-size:30px;line-height:1}
  .kpi .l{font-size:11px;text-transform:uppercase;letter-spacing:.08em;opacity:.7;margin-top:6px}
  .section{border:2px solid var(--charcoal);background:var(--paper);margin-bottom:22px}
  .section > h2{margin:0;padding:14px 18px;background:var(--charcoal);color:var(--linen);font-size:16px}
  .section .body{padding:18px}
  .intro{font-size:13px;color:#5d5a50;margin:0 0 14px}
  .muted{opacity:.65;font-size:12px}
  .empty{opacity:.6;font-size:13px;font-style:italic}
  /* priority + status badges */
  .badge{display:inline-block;font-size:11px;font-weight:600;padding:2px 9px;border:1.5px solid var(--charcoal);border-radius:20px;white-space:nowrap}
  .p-high{background:#F1E2D2;color:var(--clay);border-color:var(--clay)}
  .p-medium{background:#DCE3E6;color:#3C5560;border-color:#3C5560}
  .p-low{background:#E8E2D8;color:#6c675c;border-color:#9a948a}
  /* update cards */
  .cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:0;
    border-top:2px solid var(--charcoal);border-left:2px solid var(--charcoal)}
  .card{border-right:2px solid var(--charcoal);border-bottom:2px solid var(--charcoal);
    padding:14px 16px;background:var(--paper)}
  .card .head{display:flex;justify-content:space-between;align-items:flex-start;gap:10px}
  .card .name{font-weight:600;font-size:15px}
  .verline{font-size:12px;margin:6px 0 0;font-variant-numeric:tabular-nums}
  .verline .v-old{color:#9a948a}
  .verline .v-new{color:var(--good);font-weight:600}
  .card .whatsnew{font-size:13px;color:#5d5a50;margin-top:6px}
  .card .sync{font-size:12px;margin-top:8px;border-top:1px solid #e2d9cc;padding-top:8px}
  .card .sync b{font-weight:600}
  /* gaps grouped by department */
  .dept{border-top:2px solid var(--charcoal);padding:14px 0 4px}
  .dept:first-child{border-top:none;padding-top:2px}
  .dept > h3{margin:0 0 4px;font-size:16px}
  .gap{border-top:1px solid #e2d9cc;padding:11px 0}
  .gap:first-of-type{border-top:none}
  .gap .head{display:flex;justify-content:space-between;align-items:flex-start;gap:10px}
  .gap .name{font-weight:600}
  .gap .desc{font-size:13px;margin-top:4px}
  .gap .why{font-size:12px;color:var(--forest);margin-top:4px}
  .gap .fit{font-size:12px;color:#5d5a50;margin-top:4px}
  .tags{margin-top:6px}
  .tag{display:inline-block;font-size:11px;background:var(--linen);border:1px solid #cfc6b8;
    border-radius:12px;padding:1px 8px;margin:0 4px 4px 0}
  /* compact lists */
  .compact{margin:0;padding:0;list-style:none;columns:2;column-gap:26px}
  .compact li{break-inside:avoid;padding:6px 0;border-top:1px solid #e2d9cc}
  .compact li:first-child{border-top:none}
  .compact .n{font-weight:600}
  .compact .note{font-size:12px;color:#5d5a50}
  @media(max-width:640px){.compact{columns:1}}
  .also{font-size:13px;margin-top:14px;background:var(--linen);border:1px solid #cfc6b8;
    border-radius:6px;padding:9px 12px}
  .also b{font-weight:600}
  /* recommended order */
  .steps{margin:0;padding:0;list-style:none;counter-reset:step}
  .steps li{position:relative;padding:10px 0 10px 44px;border-top:1px solid #e2d9cc}
  .steps li:first-child{border-top:none}
  .steps li:before{counter-increment:step;content:counter(step);
    position:absolute;left:0;top:9px;width:28px;height:28px;line-height:28px;text-align:center;
    background:var(--forest);color:var(--linen);border:2px solid var(--charcoal);
    font-family:'Noto Serif Display',Georgia,serif;font-size:14px}
  .steps .act{font-weight:600}
  .steps .why{font-size:12px;color:#5d5a50;margin-top:2px}
  .foot{font-size:12px;opacity:.7;margin-top:18px;text-align:center}
</style>
</head>
<body>
<div class="wrap">

  <div class="top">
    <div class="eyebrow">AI Her Way · Hub Gap-Finder &amp; Sync</div>
    <h1>__TITLE__</h1>
    <p>Where your skill library stands against the AI for Impact Hub: the newer versions worth syncing, the gaps worth adding for your goals, what you are already up to date on, and the custom skills that are yours to keep.</p>
    <div class="facts">
      <span><b>Owner:</b> <span id="ownerLabel"></span></span>
    </div>
    <ul class="goals" id="goals"></ul>
    <div class="cat-line" id="catLine"></div>
    <div id="catCaution"></div>
    <div class="meta">Generated <span id="genDate"></span> · compares against the Hub at a point in time. Re-run when you want to check again.</div>
  </div>

  <div class="kpis" id="kpis"></div>

  <div class="section">
    <h2>Updates to sync</h2>
    <div class="body">
      <p class="intro">Syncing brings a newer Hub version into a skill you already have. It keeps your customisations (your context, your voice, your edits) and every change waits for your approval before anything is written.</p>
      <div id="updates"></div>
    </div>
  </div>

  <div class="section">
    <h2>Gaps worth adding</h2>
    <div class="body">
      <p class="intro">Hub skills you do not have yet that fit your goals and departments. Grouped by department, highest-priority departments first.</p>
      <div id="gaps"></div>
      <div id="alsoAvailable"></div>
    </div>
  </div>

  <div class="section">
    <h2>You are up to date on</h2>
    <div class="body" id="matched"></div>
  </div>

  <div class="section">
    <h2>Your own skills (keep these)</h2>
    <div class="body">
      <p class="intro">Custom work with no Hub equivalent. This is yours: keep it, build on it. It is not a gap.</p>
      <div id="own"></div>
    </div>
  </div>

  <div class="section">
    <h2>Recommended order</h2>
    <div class="body" id="order"></div>
  </div>

  <div class="foot">Hub Gap-Finder &amp; Sync · AI Her Way · compares against the Hub at a point in time. You own the files and approve every change.</div>
</div>

<script>
const DATA = __DATA__;
const S = DATA.summary || {};

const esc = s => (s==null?"":String(s)).replace(/[&<>"]/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[m]));
const arr = x => Array.isArray(x) ? x : [];
const num = n => (typeof n === "number" && isFinite(n)) ? n : 0;
function prioBadge(p){
  const v = (p||"").toLowerCase();
  const cls = ["high","medium","low"].includes(v) ? "p-"+v : "p-medium";
  const lab = p ? esc(p) : "medium";
  return `<span class="badge ${cls}">${lab}</span>`;
}
function prioRank(p){
  const v = (p||"").toLowerCase();
  return v === "high" ? 0 : v === "medium" ? 1 : 2;
}

/* ---------- header ---------- */
document.getElementById('ownerLabel').textContent = S.owner_label || "Not set";
document.getElementById('genDate').textContent = S.generated || "";
(function(){
  const goals = arr(S.goals).filter(Boolean);
  const el = document.getElementById('goals');
  if(!goals.length){ el.style.display='none'; return; }
  el.innerHTML = goals.map(g=>`<li>${esc(g)}</li>`).join('');
})();
(function(){
  const src = (S.catalogue_source || "").trim();
  const ver = S.catalogue_version ? "v"+esc(S.catalogue_version) : "";
  const date = S.catalogue_date ? " ("+esc(S.catalogue_date)+")" : "";
  const srcLc = src.toLowerCase();
  const isSnapshot = srcLc.indexOf("snapshot") !== -1;
  let srcText = "";
  if(isSnapshot) srcText = "from a bundled snapshot";
  else if(srcLc === "live") srcText = "fetched live";
  else if(src) srcText = esc(src);
  const parts = [];
  if(ver || date) parts.push("Hub catalogue " + ver + date);
  else parts.push("Hub catalogue");
  let line = "Compared against " + parts.join("");
  if(srcText) line += ", " + srcText;
  document.getElementById('catLine').textContent = line;
  if(isSnapshot){
    document.getElementById('catCaution').innerHTML =
      `<div class="caution">Note: this used a bundled snapshot, so it may be behind the live Hub. Re-run online to compare against the latest.</div>`;
  }
})();

/* ---------- KPI row ---------- */
(function(){
  const kpis = [
    {n: num(S.installed_count),  l:"Installed skills"},
    {n: num(S.matched_current),  l:"Up to date"},
    {n: num(S.update_count),     l:"Updates to sync"},
    {n: num(S.gap_count),        l:"Gaps worth adding"},
    {n: num(S.own_count),        l:"Your own skills"}
  ];
  document.getElementById('kpis').innerHTML = kpis.map(k=>
    `<div class="kpi"><div class="n">${esc(String(k.n))}</div><div class="l">${esc(k.l)}</div></div>`).join('');
})();

/* ---------- updates to sync ---------- */
(function(){
  const rows = arr(DATA.updates);
  const el = document.getElementById('updates');
  if(!rows.length){ el.innerHTML = `<p class="empty" style="margin:0">Nothing to sync. Everything you have is current.</p>`; return; }
  const sorted = rows.slice().sort((a,b)=>prioRank(a.priority)-prioRank(b.priority));
  el.innerHTML = `<div class="cards">` + sorted.map(u=>{
    const yourV = u.your_version ? esc(u.your_version) : "your version";
    const hubV = u.hub_version ? esc(u.hub_version) : "Hub version";
    return `<div class="card">
      <div class="head">
        <div class="name">${esc(u.title)}</div>
        ${prioBadge(u.priority)}
      </div>
      <div class="verline"><span class="v-old">${yourV}</span> &rarr; <span class="v-new">${hubV}</span></div>
      ${u.whats_new ? `<div class="whatsnew">${esc(u.whats_new)}</div>` : ''}
      ${u.sync_note ? `<div class="sync"><b>Sync:</b> ${esc(u.sync_note)}</div>` : ''}
    </div>`;
  }).join('') + `</div>`;
})();

/* ---------- gaps worth adding, grouped by department ---------- */
(function(){
  const rows = arr(DATA.gaps);
  const el = document.getElementById('gaps');
  if(!rows.length){ el.innerHTML = `<p class="empty" style="margin:0">No gaps flagged for your goals and departments. Nice work.</p>`; return; }
  const groups = {};
  const orderSeen = [];
  rows.forEach(g=>{
    const dept = (g.department || "").trim() || "Other";
    if(!(dept in groups)){ groups[dept] = []; orderSeen.push(dept); }
    groups[dept].push(g);
  });
  // best (lowest) priority rank per group; ties keep first-seen order
  const deptList = orderSeen.slice().sort((a,b)=>{
    const ra = Math.min.apply(null, groups[a].map(x=>prioRank(x.priority)));
    const rb = Math.min.apply(null, groups[b].map(x=>prioRank(x.priority)));
    if(ra !== rb) return ra - rb;
    return orderSeen.indexOf(a) - orderSeen.indexOf(b);
  });
  el.innerHTML = deptList.map(dept=>{
    const items = groups[dept].slice().sort((a,b)=>prioRank(a.priority)-prioRank(b.priority));
    const inner = items.map(g=>{
      const tags = arr(g.tags).filter(Boolean).map(t=>`<span class="tag">${esc(t)}</span>`).join('');
      return `<div class="gap">
        <div class="head">
          <div class="name">${esc(g.title)}</div>
          ${prioBadge(g.priority)}
        </div>
        ${g.description ? `<div class="desc">${esc(g.description)}</div>` : ''}
        ${g.why_relevant ? `<div class="why">Why it helps: ${esc(g.why_relevant)}</div>` : ''}
        ${g.audience_fit ? `<div class="fit">Fit: ${esc(g.audience_fit)}</div>` : ''}
        ${tags ? `<div class="tags">${tags}</div>` : ''}
      </div>`;
    }).join('');
    return `<div class="dept"><h3>${esc(dept)}</h3>${inner}</div>`;
  }).join('');
})();

/* ---------- also available in the Hub (not gaps) ---------- */
(function(){
  const present = arr(S.departments_present).filter(Boolean);
  const available = arr(S.departments_available).filter(Boolean);
  const presentLc = present.map(d=>String(d).toLowerCase());
  const extra = available.filter(d=>presentLc.indexOf(String(d).toLowerCase()) === -1);
  const el = document.getElementById('alsoAvailable');
  if(!extra.length){ return; }
  el.innerHTML = `<div class="also"><b>Also available in the Hub:</b> ${
    extra.map(esc).join(', ')
  }. These are departments you have not chosen to run, so they are not counted as gaps. They are here if you want them.</div>`;
})();

/* ---------- you are up to date on ---------- */
(function(){
  const rows = arr(DATA.matched_current);
  const el = document.getElementById('matched');
  if(!rows.length){ el.innerHTML = `<p class="empty" style="margin:0">Nothing matched at the current Hub version yet.</p>`; return; }
  el.innerHTML = `<ul class="compact">` + rows.map(m=>`<li>
    <span class="n">${esc(m.title || m.installed)}</span>
    ${m.note ? `<span class="note"> , ${esc(m.note)}</span>` : ''}
  </li>`).join('') + `</ul>`;
})();

/* ---------- your own skills (keep these) ---------- */
(function(){
  const rows = arr(DATA.your_own);
  const el = document.getElementById('own');
  if(!rows.length){ el.innerHTML = `<p class="empty" style="margin:0">No custom skills found. Anything you build that the Hub does not have will live here.</p>`; return; }
  el.innerHTML = `<ul class="compact">` + rows.map(o=>`<li>
    <span class="n">${esc(o.name)}</span>
    ${o.note ? `<span class="note"> , ${esc(o.note)}</span>` : ''}
  </li>`).join('') + `</ul>`;
})();

/* ---------- recommended order ---------- */
(function(){
  const rows = arr(DATA.recommended_order);
  const el = document.getElementById('order');
  if(!rows.length){ el.innerHTML = `<p class="empty" style="margin:0">No ordered steps yet.</p>`; return; }
  const sorted = rows.slice().sort((a,b)=>num(a.step)-num(b.step));
  el.innerHTML = `<ol class="steps">` + sorted.map(s=>`<li>
    <div class="act">${esc(s.action)}</div>
    ${s.why ? `<div class="why">${esc(s.why)}</div>` : ''}
  </li>`).join('') + `</ol>`;
})();
</script>
</body>
</html>"""


def main():
    ap = argparse.ArgumentParser(description="Render a Hub Gap-Finder & Sync HTML dashboard from report JSON.")
    ap.add_argument("data")
    ap.add_argument("--out", default="Hub_Gap_Report.html")
    ap.add_argument("--title", default="My Hub Gap Report")
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
