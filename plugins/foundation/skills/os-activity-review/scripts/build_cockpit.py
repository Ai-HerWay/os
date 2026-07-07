#!/usr/bin/env python3
"""
OS Activity Review - Cockpit Builder
====================================
Renders your OS's own local logs (logs/activity-log.md and
logs/decision-log.md) into a single self-contained, on-brand HTML cockpit:
what the OS did this period, drafts versus sent, approvals and declines,
escalations, estimated time saved, stalls, anomalies, and quiet skills.

Honest by design: this is a snapshot generated from your local files, on
your machine, on demand. It is not a hosted dashboard and nothing is sent
anywhere. No dependencies beyond the Python standard library.

Usage:
    python3 build_cockpit.py [--logs-dir logs] [--out logs/cockpit.html]
                             [--days 7] [--stall-days 7] [--title "..."]

Log rows the parser understands (markdown tables, header-mapped, so column
order can vary; older simpler tables are read too):

| Date | Department | Skill | Action | Tier | Status | Time saved | Notes |

Status vocabulary: done, draft (awaiting approval), approved, sent,
declined, escalated, parked. Time saved: "20m", "1.5h", "45 min".
"""
import argparse
import datetime
import html
import re
from pathlib import Path

TODAY = datetime.date.today()

# ---------------------------------------------------------------- parsing

def parse_tables(text):
    """Yield dict rows from every markdown table in text, header-mapped."""
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("|") and i + 1 < len(lines) and \
                re.match(r"^\s*\|[\s\-|:]+\|\s*$", lines[i + 1]):
            headers = [h.strip().lower() for h in line.strip().strip("|").split("|")]
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if any(cells):
                    yield dict(zip(headers, cells + [""] * (len(headers) - len(cells))))
                i += 1
        else:
            i += 1


def parse_date(s):
    s = s.strip().strip("[]")
    if not s or "__" in s:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d %b %Y", "%d %B %Y"):
        try:
            return datetime.datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def parse_minutes(s):
    if not s:
        return None
    m = re.search(r"(\d+(?:\.\d+)?)\s*(h|hr|hour)", s, re.I)
    if m:
        return float(m.group(1)) * 60
    m = re.search(r"(\d+(?:\.\d+)?)\s*(m|min)", s, re.I)
    if m:
        return float(m.group(1))
    return None


# Order matters: "draft awaiting approval" must match draft, not approved.
STATUS_MAP = [
    ("escalat", "escalated"), ("declin", "declined"), ("await", "draft"),
    ("draft", "draft"), ("park", "parked"), ("hold", "parked"),
    ("sent", "sent"), ("approv", "approved"), ("done", "done"),
]


def norm_status(s):
    low = (s or "").lower()
    for key, val in STATUS_MAP:
        if key in low:
            return val
    return "done" if s else ""


def load_activity(path, since):
    rows = []
    if not path.is_file():
        return rows
    for r in parse_tables(path.read_text(encoding="utf-8")):
        date = parse_date(r.get("date", ""))
        if date is None:
            continue
        skill = r.get("skill", "")
        if not skill:
            continue
        rows.append({
            "date": date,
            "in_period": date >= since,
            "department": r.get("department", "") or "General",
            "skill": skill,
            "action": r.get("action", "") or r.get("what it did", ""),
            "tier": r.get("tier", ""),
            "status": norm_status(r.get("status", "") or r.get("result", "")),
            "minutes": parse_minutes(r.get("time saved", "")),
            "notes": r.get("notes", "") or r.get("result", ""),
        })
    return rows


def load_decisions(path, since):
    rows = []
    if not path.is_file():
        return rows
    for r in parse_tables(path.read_text(encoding="utf-8")):
        date = parse_date(r.get("date", ""))
        if date is None or date < since:
            continue
        rows.append({
            "date": date,
            "skill": r.get("skill", ""),
            "decision": r.get("decision", ""),
            "why": r.get("why", ""),
            "flagged": (r.get("flagged to you?", "") or r.get("flagged", "")).lower().startswith("y"),
        })
    return rows

# ------------------------------------------------------------- aggregating

def fmt_minutes(total):
    if total >= 60:
        return f"{total / 60:.1f} hours"
    return f"{int(round(total))} minutes"


def aggregate(activity, decisions, stall_days):
    period_rows = [r for r in activity if r["in_period"]]
    counts = {s: 0 for s in
              ["done", "draft", "approved", "sent", "declined", "escalated", "parked"]}
    saved, unrecorded = 0.0, 0
    departments, skill_counts = {}, {}
    for r in period_rows:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
        if r["minutes"] is None:
            unrecorded += 1
        else:
            saved += r["minutes"]
        departments.setdefault(r["department"], []).append(r)
        skill_counts[r["skill"]] = skill_counts.get(r["skill"], 0) + 1

    stalled = [r for r in activity
               if r["status"] == "draft" and (TODAY - r["date"]).days > stall_days]

    declined_by_skill = {}
    for r in period_rows:
        if r["status"] == "declined":
            declined_by_skill[r["skill"]] = declined_by_skill.get(r["skill"], 0) + 1
    anomalies = [f"{s}: drafts declined {n} times this period"
                 for s, n in sorted(declined_by_skill.items()) if n >= 3]

    all_skills = {r["skill"] for r in activity}
    quiet = sorted(all_skills - {r["skill"] for r in period_rows})

    governance = [r for r in period_rows if r["status"] == "escalated"]

    return {
        "rows": period_rows, "counts": counts, "saved": saved,
        "unrecorded": unrecorded, "departments": departments,
        "skill_counts": skill_counts, "stalled": stalled,
        "anomalies": anomalies, "quiet": quiet,
        "governance": governance, "decisions": decisions,
    }

# --------------------------------------------------------------- rendering

CSS = """
:root{--charcoal:#252620;--linen:#F1EAE1;--forest:#22392C;--sage:#C0CACE;
  --clay:#876553;--paper:#FBF8F4;--good:#3F6B4E;--warn:#B07B3E;--bad:#9A4B3B}
*{box-sizing:border-box}
html,body{margin:0;background:var(--linen);color:var(--charcoal);
  font-family:'DM Sans','Nexa',-apple-system,'Segoe UI',Helvetica,Arial,sans-serif;
  font-size:15px;line-height:1.5;-webkit-font-smoothing:antialiased}
h1,h2,h3{font-family:'Noto Serif Display',Georgia,'Times New Roman',serif;font-weight:600}
.wrap{max-width:1080px;margin:0 auto;padding:28px 22px 80px}
.top{background:var(--forest);color:var(--linen);border:2px solid var(--charcoal);
  padding:26px 28px;margin-bottom:22px}
.top .eyebrow{letter-spacing:.18em;text-transform:uppercase;font-size:11px;opacity:.8;margin-bottom:8px}
.top h1{margin:0 0 6px;font-size:30px;color:var(--linen)}
.top .honest{margin:10px 0 0;font-size:13px;opacity:.85}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:0;
  border:2px solid var(--charcoal);margin-bottom:22px;background:var(--paper)}
.kpi{padding:16px 18px;border-right:2px solid var(--charcoal)}
.kpi:last-child{border-right:none}
.kpi .n{font-family:'Noto Serif Display',Georgia,serif;font-size:30px;line-height:1}
.kpi .l{font-size:11px;text-transform:uppercase;letter-spacing:.08em;opacity:.7;margin-top:6px}
.section{border:2px solid var(--charcoal);background:var(--paper);margin-bottom:22px}
.section>h2{margin:0;padding:14px 18px;background:var(--charcoal);color:var(--linen);font-size:16px}
.section.gov>h2{background:var(--bad)}
.section .body{padding:18px}
table{width:100%;border-collapse:collapse;font-size:13px}
th{text-align:left;text-transform:uppercase;letter-spacing:.06em;font-size:11px;
  border-bottom:2px solid var(--charcoal);padding:6px 8px}
td{border-bottom:1px solid var(--sage);padding:6px 8px;vertical-align:top}
.badge{display:inline-block;padding:1px 8px;border:1px solid var(--charcoal);
  border-radius:10px;font-size:11px;text-transform:uppercase;letter-spacing:.04em}
.b-draft{background:var(--sage)} .b-sent,.b-approved,.b-done{background:#DCE7DD}
.b-declined{background:#EAD4CD} .b-escalated{background:var(--bad);color:var(--linen)}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}
.card{border:2px solid var(--charcoal);padding:14px 16px;background:#fff}
.card h3{margin:0 0 8px;font-size:16px}
.small{font-size:12px;opacity:.75}
.footer{font-size:12px;opacity:.7;margin-top:8px}
"""


def esc(s):
    return html.escape(str(s))


def badge(status):
    return f'<span class="badge b-{esc(status)}">{esc(status or "logged")}</span>'


def render(agg, title, since, thin):
    c = agg["counts"]
    saved_line = fmt_minutes(agg["saved"]) if agg["saved"] else "not recorded"
    if agg["unrecorded"] and agg["saved"]:
        saved_line += f" (est.; {agg['unrecorded']} rows not recorded)"
    parts = [f"""<!DOCTYPE html><html lang="en-AU"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title><style>{CSS}</style></head><body><div class="wrap">
<div class="top"><div class="eyebrow">AI Her Way OS · Cockpit</div>
<h1>{esc(title)}</h1>
<p>Period: {since.strftime('%-d %B %Y')} to {TODAY.strftime('%-d %B %Y')}</p>
<p class="honest">Generated from your local logs on {TODAY.strftime('%-d %B %Y')}.
This is a snapshot, not a live feed. Nothing leaves your machine.
Refresh it any time by running os-activity-review.</p>
{f'<p class="honest"><strong>Data quality note:</strong> the logs for this period are thin, so these numbers are partial. The habit that fixes it: every skill logs one row per action in logs/activity-log.md.</p>' if thin else ''}
</div>"""]

    if agg["governance"]:
        rows = "".join(
            f"<tr><td>{esc(r['date'])}</td><td>{esc(r['skill'])}</td>"
            f"<td>{esc(r['action'])}</td><td>{esc(r['notes'])}</td></tr>"
            for r in agg["governance"])
        parts.append(f"""<div class="section gov"><h2>Governance findings (act on these first)</h2>
<div class="body"><table><tr><th>Date</th><th>Skill</th><th>Action</th><th>Notes</th></tr>
{rows}</table></div></div>""")

    parts.append(f"""<div class="kpis">
<div class="kpi"><div class="n">{len(agg['rows'])}</div><div class="l">Actions logged</div></div>
<div class="kpi"><div class="n">{c['draft']}</div><div class="l">Awaiting your yes</div></div>
<div class="kpi"><div class="n">{c['sent'] + c['approved']}</div><div class="l">Approved / sent</div></div>
<div class="kpi"><div class="n">{c['declined']}</div><div class="l">Declined</div></div>
<div class="kpi"><div class="n">{c['escalated']}</div><div class="l">Escalated</div></div>
<div class="kpi"><div class="n">{esc(saved_line)}</div><div class="l">Time saved (estimate)</div></div>
</div>""")

    cards = []
    for dept, rows in sorted(agg["departments"].items()):
        skills = {}
        for r in rows:
            skills.setdefault(r["skill"], []).append(r)
        lines = "".join(
            f"<tr><td>{esc(s)}</td><td>{len(rs)}</td>"
            f"<td>{' '.join(badge(x['status']) for x in rs[:6])}</td></tr>"
            for s, rs in sorted(skills.items()))
        cards.append(f"""<div class="card"><h3>{esc(dept)}</h3>
<table><tr><th>Skill</th><th>Runs</th><th>Status</th></tr>{lines}</table></div>""")
    parts.append(f"""<div class="section"><h2>By department</h2>
<div class="body"><div class="cards">{''.join(cards) or '<p>No activity logged this period.</p>'}</div></div></div>""")

    if agg["stalled"]:
        rows = "".join(
            f"<tr><td>{esc(r['skill'])}</td><td>{esc(r['action'])}</td>"
            f"<td>{(TODAY - r['date']).days} days</td><td>Approve or decline</td></tr>"
            for r in sorted(agg["stalled"], key=lambda r: r["date"]))
        parts.append(f"""<div class="section"><h2>Stalled (waiting on you)</h2>
<div class="body"><table><tr><th>Skill</th><th>Draft</th><th>Age</th><th>Next step</th></tr>
{rows}</table></div></div>""")

    anomalies = "".join(f"<li>{esc(a)}</li>" for a in agg["anomalies"]) or "<li>None this period.</li>"
    quiet = ", ".join(esc(q) for q in agg["quiet"]) or "none"
    parts.append(f"""<div class="section"><h2>Anomalies and quiet skills</h2>
<div class="body"><ul>{anomalies}</ul>
<p class="small">Quiet this period (previously used): {quiet}.
A quiet seasonal skill is expected; a quiet core skill is worth a look.</p></div></div>""")

    if agg["decisions"]:
        rows = "".join(
            f"<tr><td>{esc(r['date'])}</td><td>{esc(r['skill'])}</td>"
            f"<td>{esc(r['decision'])}</td><td>{esc(r['why'])}</td>"
            f"<td>{'yes' if r['flagged'] else 'no'}</td></tr>"
            for r in agg["decisions"])
        parts.append(f"""<div class="section"><h2>Judgement calls (from the decision log)</h2>
<div class="body"><table><tr><th>Date</th><th>Skill</th><th>Decision</th><th>Why</th><th>Flagged</th></tr>
{rows}</table></div></div>""")

    parts.append("""<p class="footer">Built by os-activity-review from logs/activity-log.md
and logs/decision-log.md. Time saved is an estimate from your own log entries and is
labelled as such. AI Her Way · EquiAI: the human approves what ships.</p>
</div></body></html>""")
    return "".join(parts)

# --------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--logs-dir", type=Path, default=Path("logs"))
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--stall-days", type=int, default=7)
    ap.add_argument("--title", default="Your OS this period")
    args = ap.parse_args()

    since = TODAY - datetime.timedelta(days=args.days)
    activity = load_activity(args.logs_dir / "activity-log.md", since)
    decisions = load_decisions(args.logs_dir / "decision-log.md", since)
    agg = aggregate(activity, decisions, args.stall_days)
    thin = len(agg["rows"]) < 3

    out = args.out or (args.logs_dir / "cockpit.html")
    if out.exists():
        backup = out.with_name("cockpit-previous.html")
        backup.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    out.write_text(render(agg, args.title, since, thin), encoding="utf-8")
    print(f"Cockpit written to {out} ({len(agg['rows'])} actions in period; "
          f"{agg['counts']['draft']} awaiting approval; "
          f"{len(agg['stalled'])} stalled)")


if __name__ == "__main__":
    main()
