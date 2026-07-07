#!/usr/bin/env python3
"""
Skills Health Check — Dashboard Builder
===================================
Takes the JSON from audit_skills.py and writes a single self-contained,
on-brand HTML dashboard: a force-directed skill network map (overlap +
reference edges, cluster colours), per-skill EquiAI/hygiene scorecards,
and a priority fix queue. No external dependencies, no internet. The
force layout is a small inline canvas simulation so it opens anywhere.

Usage:
    python3 build_dashboard.py skills_data.json [--out skill-map.html] [--title "..."]
"""
import json, argparse, html, datetime

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
  .meta{font-size:12px;opacity:.75;margin-top:14px}
  .kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:0;border:2px solid var(--charcoal);margin-bottom:22px;background:var(--paper)}
  .kpi{padding:16px 18px;border-right:2px solid var(--charcoal)}
  .kpi:last-child{border-right:none}
  .kpi .n{font-family:'Noto Serif Display',Georgia,serif;font-size:30px;line-height:1}
  .kpi .l{font-size:11px;text-transform:uppercase;letter-spacing:.08em;opacity:.7;margin-top:6px}
  .section{border:2px solid var(--charcoal);background:var(--paper);margin-bottom:22px}
  .section > h2{margin:0;padding:14px 18px;background:var(--charcoal);color:var(--linen);font-size:16px}
  .section .body{padding:18px}
  .legend{display:flex;flex-wrap:wrap;gap:14px;align-items:center;font-size:12px;margin-bottom:12px}
  .legend .sw{display:inline-block;width:12px;height:12px;border:1px solid var(--charcoal);margin-right:6px;vertical-align:middle;border-radius:50%}
  .legend .edge{display:inline-block;width:22px;height:0;border-top:3px solid;margin-right:6px;vertical-align:middle}
  #mapwrap{position:relative;border:2px solid var(--charcoal);background:#fff;overflow:hidden}
  #map{display:block;width:100%;height:560px;touch-action:none}
  #tip{position:absolute;pointer-events:none;background:var(--charcoal);color:var(--linen);
    padding:8px 10px;font-size:12px;border-radius:4px;max-width:240px;opacity:0;transition:opacity .1s;z-index:5}
  .controls{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px;align-items:center}
  .controls label{font-size:12px;display:flex;gap:5px;align-items:center;cursor:pointer}
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:0;border-top:2px solid var(--charcoal);border-left:2px solid var(--charcoal)}
  .card{border-right:2px solid var(--charcoal);border-bottom:2px solid var(--charcoal);padding:14px 16px;background:var(--paper)}
  .card h3{margin:0 0 2px;font-size:15px}
  .card .clu{font-size:11px;letter-spacing:.05em;text-transform:uppercase;opacity:.65}
  .pill{display:inline-block;font-size:11px;font-weight:600;padding:2px 9px;border:1.5px solid var(--charcoal);border-radius:20px;margin-left:6px}
  .gA{background:#D7E6DC} .gB{background:#E4ECDF} .gC{background:#F1E6CE} .gD{background:#F0D9C9} .gF{background:#EBC9C0}
  .bars{margin:10px 0 8px}
  .bar{display:flex;align-items:center;gap:8px;font-size:12px;margin:3px 0}
  .bar .lab{width:64px;opacity:.7}
  .track{flex:1;height:9px;background:#E8DFD3;border:1px solid var(--charcoal);position:relative}
  .fill{height:100%;background:var(--forest)}
  .fill.eq{background:var(--clay)}
  .pillars{display:flex;flex-wrap:wrap;gap:5px;margin-top:8px}
  .pdot{font-size:10px;padding:2px 7px;border:1px solid var(--charcoal);border-radius:12px}
  .pon{background:var(--forest);color:var(--linen)} .poff{background:#fff;color:#9a9a93;border-color:#cfc8bd;text-decoration:line-through}
  .notes{font-size:12px;margin-top:8px;color:#5d5a50}
  .notes li{margin:2px 0}
  table{width:100%;border-collapse:collapse;font-size:13px}
  th,td{text-align:left;padding:9px 10px;border-bottom:1px solid #d9d0c4;vertical-align:top}
  th{background:var(--linen);font-size:11px;text-transform:uppercase;letter-spacing:.06em}
  .P0{color:var(--bad);font-weight:700}.P1{color:var(--warn);font-weight:700}.P2{color:var(--forest);font-weight:700}
  .cov{display:grid;grid-template-columns:1fr auto;gap:6px 14px;align-items:center;font-size:13px}
  .covbar{height:10px;background:#E8DFD3;border:1px solid var(--charcoal)}
  .covbar > i{display:block;height:100%;background:var(--clay)}
  .muted{opacity:.65;font-size:12px}
  .foot{font-size:12px;opacity:.7;margin-top:18px;text-align:center}
  details summary{cursor:pointer;font-size:12px;color:var(--forest);margin-top:6px}
</style>
</head>
<body>
<div class="wrap">

  <div class="top">
    <div class="eyebrow">AI Her Way · Skills Health Check</div>
    <h1>__TITLE__</h1>
    <p>Every skill you have, audited for hygiene and scored against the EquiAI framework, with a live map of how they all connect. Clean skills, clear boundaries, safety built in.</p>
    <div class="meta">Generated __WHEN__ · __NCUST__ custom skills (__NGEN__ generic excluded from scores) · source: <code>__SRC__</code></div>
  </div>

  <div class="kpis">
    <div class="kpi"><div class="n">__AVG__</div><div class="l">Avg overall score</div></div>
    <div class="kpi"><div class="n">__AVGHY__</div><div class="l">Avg hygiene</div></div>
    <div class="kpi"><div class="n">__AVGEQ__</div><div class="l">Avg EquiAI</div></div>
    <div class="kpi"><div class="n">__OVL__</div><div class="l">Overlap links</div></div>
    <div class="kpi"><div class="n">__P0__</div><div class="l">P0 must-fix</div></div>
  </div>

  <div class="section">
    <h2>The skill network</h2>
    <div class="body">
      <div class="legend" id="clusterLegend"></div>
      <div class="legend">
        <span><span class="edge" style="border-color:var(--bad)"></span>Trigger overlap (they compete for the same prompt)</span>
        <span><span class="edge" style="border-top-style:dashed;border-color:var(--forest)"></span>Reference / hand-off (one skill calls another)</span>
        <span class="muted">Node size = how many skills it overlaps with. Drag nodes. Hover for detail.</span>
      </div>
      <div class="controls">
        <label><input type="checkbox" id="tOverlap" checked> Overlap links</label>
        <label><input type="checkbox" id="tRef" checked> Reference links</label>
        <label><input type="checkbox" id="tLabels" checked> Labels</label>
        <button id="reheat" style="font-size:12px;padding:4px 10px;border:1.5px solid var(--charcoal);background:var(--linen);cursor:pointer">Re-settle layout</button>
      </div>
      <div id="mapwrap"><canvas id="map"></canvas><div id="tip"></div></div>
    </div>
  </div>

  <div class="section">
    <h2>EquiAI coverage: where the gaps are across all your skills</h2>
    <div class="body">
      <p class="muted" style="margin-top:0">How many of your __NCUST__ custom skills actively write each safety pillar into the file. Low bars are your fastest path to the global standard.</p>
      <div class="cov" id="coverage"></div>
    </div>
  </div>

  <div class="section">
    <h2>Priority fix queue</h2>
    <div class="body">
      <p class="muted" style="margin-top:0">Suggested, not applied. In the skill, each of these becomes a draft rewrite you approve before anything is written to a file.</p>
      <table><thead><tr><th>Priority</th><th>Skill</th><th>Issue</th><th>Suggested fix</th></tr></thead>
      <tbody id="fixes"></tbody></table>
    </div>
  </div>

  <div class="section">
    <h2>Every skill, scored</h2>
    <div class="body"><div class="grid" id="cards"></div></div>
  </div>

  <div class="foot">Skills Health Check · AI Her Way · audit + map are advisory. You own the files and approve every change.</div>
</div>

<script>
const DATA = __DATA__;
const CLUSTER_COLORS = {
  "Content & copy":"#876553","Launch & campaign":"#22392C","Member health":"#9A4B3B",
  "Daily & triage":"#3F6B4E","Brand & authority":"#5B6E74","Build & ops":"#B07B3E",
  "Format helpers":"#9aa0a6","Uncategorised":"#777"
};
function cc(c){return CLUSTER_COLORS[c]||"#777";}
const esc = s => (s==null?"":String(s)).replace(/[&<>"]/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[m]));

/* ---------- cluster legend ---------- */
(function(){
  const seen=[...new Set(DATA.skills.map(s=>s.cluster))].sort();
  document.getElementById('clusterLegend').innerHTML =
    seen.map(c=>`<span><span class="sw" style="background:${cc(c)}"></span>${esc(c)}</span>`).join('');
})();

/* ---------- coverage bars ---------- */
(function(){
  const cov=DATA.summary.equiai_pillar_coverage, n=DATA.summary.custom_skills;
  const rows=Object.entries(cov).sort((a,b)=>a[1]-b[1]);
  document.getElementById('coverage').innerHTML = rows.map(([k,v])=>{
    const pct=Math.round(100*v/n);
    return `<div>${esc(k)}</div><div style="display:flex;gap:8px;align-items:center;min-width:200px">
      <div class="covbar" style="flex:1"><i style="width:${pct}%"></i></div>
      <span class="muted" style="width:54px;text-align:right">${v}/${n}</span></div>`;
  }).join('');
})();

/* ---------- fix queue ---------- */
(function(){
  document.getElementById('fixes').innerHTML = DATA.fixes.map(f=>
    `<tr><td class="${f.priority}">${f.priority}</td><td><strong>${esc(f.skill)}</strong></td>
     <td>${esc(f.issue)}</td><td>${esc(f.fix)}</td></tr>`).join('');
})();

/* ---------- scorecards ---------- */
(function(){
  const order=DATA.skills.slice().sort((a,b)=>a.overall-b.overall);
  document.getElementById('cards').innerHTML = order.map(s=>{
    const pillars=Object.entries(s.equiai_detail).map(([k,p])=>
      `<span class="pdot ${p.hit?'pon':'poff'}" title="${esc(p.blurb)}">${esc(p.label)}</span>`).join('');
    const notes=(s.hygiene_notes&&s.hygiene_notes.length)
      ? `<details><summary>${s.hygiene_notes.length} hygiene note(s)</summary><ul class="notes">${s.hygiene_notes.map(n=>`<li>${esc(n)}</li>`).join('')}</ul></details>`
      : `<div class="notes">Clean on hygiene checks.</div>`;
    const gen = s.is_generic?`<span class="muted"> · generic</span>`:'';
    return `<div class="card">
      <div style="display:flex;justify-content:space-between;align-items:flex-start">
        <div><h3>${esc(s.name)}</h3><div class="clu">${esc(s.cluster)}${gen}</div></div>
        <span class="pill g${s.grade}">${s.grade} · ${s.overall}</span>
      </div>
      <div class="bars">
        <div class="bar"><span class="lab">Hygiene</span><div class="track"><div class="fill" style="width:${s.hygiene_score}%"></div></div><b>${s.hygiene_score}</b></div>
        <div class="bar"><span class="lab">EquiAI</span><div class="track"><div class="fill eq" style="width:${s.equiai_score}%"></div></div><b>${s.equiai_score}</b></div>
      </div>
      <div class="pillars">${pillars}</div>
      ${notes}
    </div>`;
  }).join('');
})();

/* ---------- force-directed network (inline, no deps) ---------- */
(function(){
  const cv=document.getElementById('map'), tip=document.getElementById('tip');
  const ctx=cv.getContext('2d');
  let W=0,H=0,DPR=Math.min(2,window.devicePixelRatio||1);
  function resize(){const r=cv.getBoundingClientRect();W=r.width;H=r.height;
    cv.width=W*DPR;cv.height=H*DPR;ctx.setTransform(DPR,0,0,DPR,0,0);}
  const nodes=DATA.skills.map((s,i)=>({
    id:s.name,cluster:s.cluster,deg:s.overlap_degree||0,grade:s.grade,overall:s.overall,
    eq:s.equiai_score,hy:s.hygiene_score,
    x:0,y:0,vx:0,vy:0,
    r:7+Math.min(13,(s.overlap_degree||0)*2.2)
  }));
  const idx={};nodes.forEach((n,i)=>idx[n.id]=i);
  const overlapE=DATA.overlap.filter(e=>idx[e.source]!=null&&idx[e.target]!=null)
    .map(e=>({a:idx[e.source],b:idx[e.target],w:e.weight,type:'ovl',info:e}));
  const refE=[];
  DATA.skills.forEach(s=>(s.references||[]).forEach(r=>{
    if(idx[r]!=null&&r!==s.name) refE.push({a:idx[s.name],b:idx[r],w:.5,type:'ref'});
  }));
  // seed positions in a circle by cluster
  const clusters=[...new Set(nodes.map(n=>n.cluster))];
  resize();
  nodes.forEach((n,i)=>{const ci=clusters.indexOf(n.cluster);
    const ca=(ci/clusters.length)*Math.PI*2, ra=(i/nodes.length)*Math.PI*2;
    n.x=W/2+Math.cos(ca)*150+Math.cos(ra)*60; n.y=H/2+Math.sin(ca)*120+Math.sin(ra)*60;});
  let alpha=1;
  const showOvl=()=>document.getElementById('tOverlap').checked;
  const showRef=()=>document.getElementById('tRef').checked;
  const showLab=()=>document.getElementById('tLabels').checked;

  function step(){
    // repulsion
    for(let i=0;i<nodes.length;i++){for(let j=i+1;j<nodes.length;j++){
      const a=nodes[i],b=nodes[j];let dx=a.x-b.x,dy=a.y-b.y;let d2=dx*dx+dy*dy||.01;
      let f=2600/d2;let d=Math.sqrt(d2);dx/=d;dy/=d;
      a.vx+=dx*f;a.vy+=dy*f;b.vx-=dx*f;b.vy-=dy*f;}}
    // springs
    const springs=[];if(showOvl())springs.push(...overlapE);if(showRef())springs.push(...refE);
    springs.forEach(e=>{const a=nodes[e.a],b=nodes[e.b];let dx=b.x-a.x,dy=b.y-a.y;
      let d=Math.sqrt(dx*dx+dy*dy)||.01;const target=e.type==='ref'?150:90;
      let f=(d-target)*0.02*(e.w+0.3);dx/=d;dy/=d;
      a.vx+=dx*f;a.vy+=dy*f;b.vx-=dx*f;b.vy-=dy*f;});
    // same-cluster mild attraction + centering
    nodes.forEach(n=>{n.vx+=(W/2-n.x)*0.0016;n.vy+=(H/2-n.y)*0.0016;
      n.x+=n.vx*alpha;n.y+=n.vy*alpha;n.vx*=0.86;n.vy*=0.86;
      n.x=Math.max(n.r+4,Math.min(W-n.r-4,n.x));n.y=Math.max(n.r+4,Math.min(H-n.r-4,n.y));});
    alpha*=0.992;if(alpha<0.02)alpha=0.02;
  }
  function draw(){
    ctx.clearRect(0,0,W,H);
    if(showOvl())overlapE.forEach(e=>{const a=nodes[e.a],b=nodes[e.b];
      ctx.strokeStyle='rgba(154,75,59,'+Math.min(.85,.3+e.w).toFixed(2)+')';
      ctx.lineWidth=1+e.w*4;ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();});
    if(showRef()){ctx.setLineDash([4,4]);refE.forEach(e=>{const a=nodes[e.a],b=nodes[e.b];
      ctx.strokeStyle='rgba(34,57,44,.35)';ctx.lineWidth=1.2;
      ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();});ctx.setLineDash([]);}
    nodes.forEach(n=>{
      ctx.beginPath();ctx.arc(n.x,n.y,n.r,0,Math.PI*2);
      ctx.fillStyle=cc(n.cluster);ctx.fill();
      ctx.lineWidth=n.grade==='F'||n.grade==='D'?2.5:1.2;
      ctx.strokeStyle=(n.grade==='F'||n.grade==='D')?'#9A4B3B':'#252620';ctx.stroke();
      if(showLab()){ctx.fillStyle='#252620';ctx.font='11px DM Sans, sans-serif';
        ctx.textAlign='center';ctx.fillText(n.id,n.x,n.y+n.r+12);}
    });
  }
  function loop(){step();draw();requestAnimationFrame(loop);}
  loop();

  // interaction
  let drag=null;
  function pos(ev){const r=cv.getBoundingClientRect();
    const t=ev.touches?ev.touches[0]:ev;return{x:t.clientX-r.left,y:t.clientY-r.top};}
  function hit(p){let best=null,bd=1e9;nodes.forEach(n=>{const d=Math.hypot(n.x-p.x,n.y-p.y);
    if(d<n.r+4&&d<bd){bd=d;best=n;}});return best;}
  cv.addEventListener('mousedown',e=>{const n=hit(pos(e));if(n){drag=n;alpha=Math.max(alpha,.4);}});
  window.addEventListener('mousemove',e=>{const p=pos(e);
    if(drag){drag.x=p.x;drag.y=p.y;drag.vx=drag.vy=0;}
    const n=drag||hit(p);
    if(n){const s=DATA.skills.find(x=>x.name===n.id);
      tip.style.opacity=1;tip.style.left=Math.min(W-10,p.x+14)+'px';tip.style.top=(p.y+14)+'px';
      const ov=(s.overlap_degree||0);
      tip.innerHTML=`<b>${esc(n.id)}</b><br>${esc(n.cluster)} · grade ${s.grade} (${s.overall})<br>`+
        `Hygiene ${s.hygiene_score} · EquiAI ${s.equiai_score}<br>Overlaps ${ov} skill(s)`;
    } else tip.style.opacity=0;});
  window.addEventListener('mouseup',()=>drag=null);
  cv.addEventListener('touchstart',e=>{const n=hit(pos(e));if(n){drag=n;alpha=.4;}},{passive:true});
  cv.addEventListener('touchmove',e=>{if(drag){const p=pos(e);drag.x=p.x;drag.y=p.y;drag.vx=drag.vy=0;}},{passive:true});
  cv.addEventListener('touchend',()=>drag=null);
  document.getElementById('reheat').onclick=()=>{alpha=1;};
  window.addEventListener('resize',()=>{resize();alpha=Math.max(alpha,.4);});
})();
</script>
</body>
</html>"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("data")
    ap.add_argument("--out", default="skill-map.html")
    ap.add_argument("--title", default="Your Skills Health Check")
    args = ap.parse_args()
    d = json.load(open(args.data, encoding="utf-8"))
    s = d["summary"]
    out = (TEMPLATE
        .replace("__TITLE__", html.escape(args.title))
        .replace("__WHEN__", html.escape(s["generated"]))
        .replace("__SRC__", html.escape(s["source_dir"]))
        .replace("__NCUST__", str(s["custom_skills"]))
        .replace("__NGEN__", str(s["generic_skills"]))
        .replace("__AVG__", str(s["avg_overall"]))
        .replace("__AVGHY__", str(s["avg_hygiene"]))
        .replace("__AVGEQ__", str(s["avg_equiai"]))
        .replace("__OVL__", str(s["overlap_edges"]))
        .replace("__P0__", str(s["p0_count"]))
        .replace("__DATA__", json.dumps(d, ensure_ascii=False)))
    open(args.out, "w", encoding="utf-8").write(out)
    print(f"Wrote dashboard -> {args.out} ({len(out)//1024} KB)")

if __name__ == "__main__":
    main()
