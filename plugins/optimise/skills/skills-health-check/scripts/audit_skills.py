#!/usr/bin/env python3
"""
Skills Health Check — Audit Engine
==============================
Scans a folder of Claude skill files, audits each against the AI Her Way
global standard (hygiene + the EquiAI safety framework), maps how they
connect (trigger overlap, skill-to-skill references, domain clusters),
and writes a single JSON file the dashboard renders.

Usage:
    python3 audit_skills.py <skills_dir> [--out skills_data.json]

A "skill" is either:
  - a directory containing SKILL.md, or
  - a standalone *.md file with YAML frontmatter (name + description).

No external dependencies. Python 3.8+.
"""

import os, re, sys, json, glob, argparse
from datetime import datetime

# ----------------------------------------------------------------------
# EquiAI framework — the eight pillars we score every skill against.
# Each pillar has cue phrases. A skill "evidences" a pillar if its body
# or description contains the cues. This is a heuristic surface scan: it
# rewards skills that WRITE THE SAFETY IN, which is the whole point.
# ----------------------------------------------------------------------
EQUIAI_PILLARS = {
    "consent_least_privilege": {
        "label": "Consent & least privilege",
        "blurb": "Starts read-only, asks before it touches more. Access is consent.",
        "cues": ["least privilege", "read-only", "read first", "write with permission",
                 "permission", "access", "scope", "connect the minimum", "start restrictive"],
    },
    "human_in_the_loop": {
        "label": "Human in the loop",
        "blurb": "Drafts and waits on anything that matters (the Amber tier).",
        "cues": ["human in the loop", "draft", "approval", "approve", "review first",
                 "amber", "wait for", "do not send", "don't send", "stop for", "sign off",
                 "do not auto", "don't auto", "gate"],
    },
    "red_line": {
        "label": "A line it won't cross",
        "blurb": "A short, hard 'never' list. Money, contracts, sending as you.",
        "cues": ["never", "red tier", "red line", "do not", "must not", "off-limits",
                 "non-negotiable", "hard rule", "forbidden", "banned"],
    },
    "transparency": {
        "label": "Transparency / disclosure",
        "blurb": "Discloses AI assistance when it acts as you.",
        "cues": ["disclose", "disclosure", "transparency", "transparent", "ai assisted",
                 "ai-assisted", "label as", "make clear"],
    },
    "honesty": {
        "label": "Honesty / no fabrication",
        "blurb": "Never invents facts, quotes or numbers. Flags what it doesn't know.",
        "cues": ["never fabricate", "do not fabricate", "don't fabricate", "no invented",
                 "do not invent", "don't make up", "if you don't know", "flag it",
                 "no hallucinat", "verify", "fact-check", "fact check", "source"],
    },
    "evidence_led": {
        "label": "Research-led / evidence-based",
        "blurb": "Grounded in a named framework, research or proven method, not vibes.",
        "cues": ["framework", "research", "evidence", "proven", "based on", "methodology",
                 "5 levels", "five levels", "playbook", "best practice", "data", "benchmark",
                 "citation", "reference file", "source of truth"],
    },
    "portability": {
        "label": "Portability / no lock-in",
        "blurb": "Plain files the student owns. Works without any one vendor.",
        "cues": ["portable", "no lock-in", "export", "own your", "you own", "plain language",
                 "markdown", "your os", "file you own", "version", "changelog"],
    },
    "traceability": {
        "label": "Traceability / logs",
        "blurb": "Reads its rules before acting, writes down what it did after.",
        "cues": ["log", "logs", "decision-log", "activity-log", "audit trail", "traceab",
                 "writes down", "record", "memory", "reads first", "history"],
    },
}

# Domain clustering — assign each skill a primary cluster for the map.
CLUSTERS = {
    "Content & copy": ["email", "copy", "copywriter", "hook", "viral", "feel seen",
                        "social", "caption", "newsletter", "content", "persuasive", "youtube"],
    "Launch & campaign": ["launch", "campaign", "funnel", "masterclass", "cart",
                          "dm-flow", "dm flow", "scorecard", "promo", "offer"],
    "Member health": ["retention", "churn", "product-pulse", "product pulse", "friction",
                      "bug", "member health", "support", "complaint"],
    "Daily & triage": ["inbox", "daily brief", "daily-brief", "triage", "client",
                       "morning", "meeting prep", "board of advisors"],
    "Brand & authority": ["brand", "manifesto", "authority", "voice", "design guideline",
                          "positioning", "bio"],
    "Build & ops": ["sop", "role card", "role-card", "agent", "mcp", "skill-creator",
                    "skill creator", "process", "ops", "vetting", "spec"],
    "Format helpers": ["pdf", "docx", "pptx", "xlsx", "spreadsheet", "presentation",
                       "word document", "theme", "canvas", "web-artifact"],
}

# Generic Anthropic file-format skills — flagged so the audit can exclude
# them from "your skills" scoring if asked. Not a quality judgement.
GENERIC = {"pdf", "docx", "pptx", "xlsx", "mcp-builder", "skill-creator",
           "theme-factory", "canvas-design", "web-artifacts-builder", "schedule",
           "consolidate-memory", "setup-cowork"}

STOPWORDS = set("""a an the and or but for to of in on with your you it is be this that
these those use using used when what which who whom how why where any all also into from
as at by skill skills claude nici always never do not don t can could should would more
most other another need needs want wants help create make write writing draft drafts get
their them they she he her his we our us if then than so such per via etc ie eg about up
down out over under again further once here there each few both same own only just
""".split())

# House-style / brand boilerplate that appears in almost every AI Her Way skill
# (the em-dash ban, AU English, the brand name). Shared because they are RULES,
# not because two skills do the same job — so they must not count as overlap.
BOILERPLATE = set("""australian english spelling dashes em dash house voice herway her way
ai hub nici always use never spelling realise organise colour favourite content member
members women founder founders trigger triggers phrases also high-converting authentic
""".split())
STOPWORDS |= BOILERPLATE


def parse_frontmatter(text):
    """Return (meta_dict, body). Handles --- delimited YAML-ish frontmatter."""
    meta, body = {}, text
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.DOTALL)
    if m:
        raw, body = m.group(1), m.group(2)
        # naive key: value parse (good enough for name/description)
        key, buf = None, []
        for line in raw.split("\n"):
            km = re.match(r"^([A-Za-z0-9_\-]+):\s*(.*)$", line)
            if km and not line.startswith(" "):
                if key:
                    meta[key] = "\n".join(buf).strip().strip('"').strip("'")
                key, buf = km.group(1).strip(), [km.group(2)]
            else:
                buf.append(line)
        if key:
            meta[key] = "\n".join(buf).strip().strip('"').strip("'")
    return meta, body


def quoted_phrases(s):
    """Trigger phrases authors put in quotes inside the description."""
    return [p.strip().lower() for p in re.findall(r"['\"]([^'\"]{3,60})['\"]", s)]


def keyword_set(text):
    """Content keywords for overlap (Jaccard) comparison."""
    words = re.findall(r"[a-zA-Z][a-zA-Z\-']{2,}", text.lower())
    return {w for w in words if w not in STOPWORDS and len(w) > 2}


def detect_cluster(name, desc, body):
    blob = f"{name} {desc} {body[:1500]}".lower()
    best, best_hits = "Build & ops", 0
    for cluster, cues in CLUSTERS.items():
        hits = sum(blob.count(c) for c in cues)
        if hits > best_hits:
            best, best_hits = cluster, hits
    return best


def find_references(name, body, all_names):
    """Directed edges: this skill names another skill (a hand-off)."""
    refs = set()
    low = body.lower()
    for other in all_names:
        if other == name:
            continue
        # match the skill slug as a token
        if re.search(r"(?<![a-z0-9])" + re.escape(other.lower()) + r"(?![a-z0-9])", low):
            refs.add(other)
    return sorted(refs)


def body_is_broken(body):
    """Detect a skill whose body is not instructions (e.g. leftover code)."""
    stripped = body.strip()
    if len(stripped) < 200:
        return True, "Body is almost empty (under 200 chars), nothing for Claude to follow."
    # A skill that opens with a code fence is instructions-as-code: broken.
    if re.match(r"^```", stripped) and re.search(r"\b(import |os\.|shutil|def |pip install)", stripped[:600]):
        return True, "Body opens with a code block, not instructions, it is leftover setup code."
    # Count headings OUTSIDE fenced code (headings inside an embedded string don't count).
    no_fence = re.sub(r"```.*?```", "", stripped, flags=re.DOTALL)
    real_headings = len(re.findall(r"(?m)^#{1,4}\s", no_fence))
    code_signals = ["import ", "def ", "print(", "os.path", "if __name__",
                    "pip install", "#!/usr/bin", "</html>", "function(", "os.makedirs", "shutil"]
    code_hits = sum(stripped.count(s) for s in code_signals)
    # If real prose is thin once code is stripped, it is not a real skill body.
    if code_hits >= 3 and (real_headings <= 1 or len(no_fence.strip()) < 300):
        return True, "Body looks like leftover code/setup, not skill instructions."
    return False, ""


def score_skill(s):
    """Hygiene 0-100 + EquiAI 0-100, with a transparent breakdown."""
    hy, hy_notes = 100, []
    desc_words = s["description_words"]
    if not s["has_description"]:
        hy -= 45; hy_notes.append("No description in frontmatter (-45)")
    elif desc_words < 12:
        hy -= 30; hy_notes.append(f"Description very thin ({desc_words} words) (-30)")
    elif desc_words < 25:
        hy -= 12; hy_notes.append(f"Description on the short side ({desc_words} words) (-12)")
    if s["broken_body"]:
        hy -= 40; hy_notes.append("Body is broken / not instructions (-40)")
    if not s["has_non_negotiable_block"]:
        hy -= 12; hy_notes.append("No NON-NEGOTIABLE RULES block at the top (-12)")
    if not s["has_not_for_line"] and not s["is_generic"]:
        hy -= 8; hy_notes.append("No 'do NOT use for / use X instead' boundary line (-8)")
    if s["has_emoji_headings"]:
        hy -= 6; hy_notes.append("Decorative emoji in structural headings (-6)")
    if s["has_em_dash"]:
        hy -= 6; hy_notes.append("Contains em dashes (house style: banned) (-6)")
    if s["stale_dates"]:
        hy -= 6; hy_notes.append(f"Hardcoded dates that will go stale: {', '.join(s['stale_dates'][:3])} (-6)")
    if s["dead_refs"]:
        hy -= 8; hy_notes.append(f"Points to skills that were not found: {', '.join(s['dead_refs'])} (-8)")
    hy = max(0, hy)

    pillars_hit = s["equiai_pillars_hit"]
    eq = round(100 * len(pillars_hit) / len(EQUIAI_PILLARS))
    return hy, hy_notes, eq


def grade(score):
    if score >= 90: return "A"
    if score >= 80: return "B"
    if score >= 65: return "C"
    if score >= 50: return "D"
    return "F"


def audit_one(path, name_hint, all_names_lower):
    text = open(path, encoding="utf-8", errors="ignore").read()
    meta, body = parse_frontmatter(text)
    name = (meta.get("name") or name_hint).strip()
    desc = (meta.get("description") or "").strip()

    broken, broken_reason = body_is_broken(body)
    low_body = body.lower()
    headings = re.findall(r"(?m)^(#{1,4})\s*(.+)$", body)

    # EquiAI pillar detection
    scan = f"{desc}\n{body}".lower()
    pillars_hit = []
    pillar_detail = {}
    for key, p in EQUIAI_PILLARS.items():
        hits = [c for c in p["cues"] if c in scan]
        pillar_detail[key] = {"label": p["label"], "blurb": p["blurb"],
                              "hit": bool(hits), "matched": hits[:4]}
        if hits:
            pillars_hit.append(key)

    rec = {
        "name": name,
        "description": desc,
        "description_words": len(desc.split()),
        "has_description": bool(desc),
        "body_chars": len(body.strip()),
        "broken_body": broken,
        "broken_reason": broken_reason,
        "is_generic": name.lower() in GENERIC,
        "triggers": quoted_phrases(desc),
        "keywords": sorted(keyword_set(desc)),
        "has_non_negotiable_block": bool(re.search(
            r"(?im)^#{1,4}\s.*(non-negotiable|never break|hard rules|rules you must|guardrails)", body)),
        "has_not_for_line": bool(re.search(
            r"(?i)(do not use|don't use|not for|use .* instead|use the .* skill for)", scan)),
        "has_emoji_headings": bool(re.search(
            r"(?m)^#{1,4}\s*[^\w\s#]", body)) and bool(re.search(
            r"(?m)^#{1,4}\s*[\U0001F000-\U0001FAFF☀-➿]", body)),
        "has_em_dash": "—" in body or "—" in desc,
        "stale_dates": sorted(set(re.findall(
            r"(?i)(?:as of|since|in)\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+20\d{2}", body))),
        "heading_count": len(headings),
        "equiai_pillars_hit": pillars_hit,
        "equiai_detail": pillar_detail,
    }
    return rec, body


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("skills_dir")
    ap.add_argument("--out", default="skills_data.json")
    ap.add_argument("--overlap-threshold", type=float, default=0.12)
    args = ap.parse_args()

    # discover skills
    found = []  # (name_hint, path)
    for d in sorted(glob.glob(os.path.join(args.skills_dir, "*"))):
        if os.path.isdir(d):
            sk = os.path.join(d, "SKILL.md")
            if os.path.exists(sk):
                found.append((os.path.basename(d), sk))
    for f in sorted(glob.glob(os.path.join(args.skills_dir, "*.md"))):
        if os.path.basename(f).upper() != "SKILL.MD":
            found.append((os.path.splitext(os.path.basename(f))[0], f))

    if not found:
        print(f"No skills found in {args.skills_dir}", file=sys.stderr)
        sys.exit(1)

    all_names = [n for n, _ in found]
    all_names_lower = [n.lower() for n in all_names]

    skills, bodies = [], {}
    for hint, path in found:
        rec, body = audit_one(path, hint, all_names_lower)
        rec["cluster"] = detect_cluster(rec["name"], rec["description"], body)
        skills.append(rec)
        bodies[rec["name"]] = body

    name_set = {s["name"] for s in skills}
    # references + dead refs
    for s in skills:
        refs = find_references(s["name"], s["description"] + "\n" + bodies[s["name"]], all_names)
        s["references"] = refs
        # dead refs: a skill-looking slug it points to that isn't present
        mentioned = set(re.findall(r"`([a-z][a-z0-9\-]{4,})`", bodies[s["name"]].lower()))
        looks_like_skill = {m for m in mentioned if "-" in m and not m.endswith((".md", ".py", ".json", ".html"))}
        s["dead_refs"] = sorted([m for m in looks_like_skill
                                 if m not in name_set and m not in {x.lower() for x in name_set}
                                 and m.count("-") >= 1])[:4]

    # overlap edges (Jaccard on description keywords + shared trigger phrases)
    overlap = []
    for i in range(len(skills)):
        for j in range(i + 1, len(skills)):
            a, b = skills[i], skills[j]
            ka, kb = set(a["keywords"]), set(b["keywords"])
            if not ka or not kb:
                continue
            jac = len(ka & kb) / len(ka | kb)
            shared_tr = set(a["triggers"]) & set(b["triggers"])
            score = jac + 0.15 * len(shared_tr)
            if score >= args.overlap_threshold:
                overlap.append({
                    "source": a["name"], "target": b["name"],
                    "weight": round(score, 3),
                    "shared_keywords": sorted(ka & kb)[:8],
                    "shared_triggers": sorted(shared_tr)[:5],
                })

    # scoring
    for s in skills:
        hy, hy_notes, eq = score_skill(s)
        s["hygiene_score"] = hy
        s["hygiene_notes"] = hy_notes
        s["equiai_score"] = eq
        s["overall"] = round(0.5 * hy + 0.5 * eq)
        s["grade"] = grade(s["overall"])
        # overlap degree
        s["overlap_degree"] = sum(1 for e in overlap
                                  if e["source"] == s["name"] or e["target"] == s["name"])

    # priority fix queue
    fixes = []
    for s in skills:
        if s["broken_body"]:
            fixes.append({"skill": s["name"], "priority": "P0",
                          "issue": s["broken_reason"],
                          "fix": "Rebuild the body with real step-by-step instructions, or merge into a working skill."})
        if not s["has_description"] or s["description_words"] < 12:
            fixes.append({"skill": s["name"], "priority": "P0",
                          "issue": f"Description is missing or too thin ({s['description_words']} words), it will rarely trigger or trigger wrongly.",
                          "fix": "Rewrite to the 3-sentence standard: Use this when X (with 4-6 quoted trigger phrases). It does Y. Do NOT use for Z, use [other-skill]."})
        if s["overlap_degree"] >= 4 and not s["has_not_for_line"]:
            fixes.append({"skill": s["name"], "priority": "P1",
                          "issue": f"Competes with {s['overlap_degree']} other skills for the same prompts and has no boundary line.",
                          "fix": "Add a 'Use THIS not THAT when...' line naming what it is NOT for and which skill to use instead."})
        if not s["has_non_negotiable_block"] and not s["is_generic"]:
            fixes.append({"skill": s["name"], "priority": "P2",
                          "issue": "Critical rules (em-dash ban, draft-don't-send, AU English) are not pulled to the top.",
                          "fix": "Add a `## NON-NEGOTIABLE RULES` block at the very top, rules as bold/CAPS dot points."})
        if len(s["equiai_pillars_hit"]) < 4 and not s["is_generic"]:
            missing = [EQUIAI_PILLARS[k]["label"] for k in EQUIAI_PILLARS
                       if k not in s["equiai_pillars_hit"]]
            fixes.append({"skill": s["name"], "priority": "P2",
                          "issue": f"EquiAI coverage is thin ({len(s['equiai_pillars_hit'])}/8 pillars). Missing: {', '.join(missing[:4])}.",
                          "fix": "Add a Responsible Use / guardrails section: disclosure, human-in-loop tier, a 'never' line, and 'never fabricate'."})
        if s["dead_refs"]:
            fixes.append({"skill": s["name"], "priority": "P2",
                          "issue": f"Points to skills that do not exist: {', '.join(s['dead_refs'])}.",
                          "fix": "Create those skills or remove the dead pointers so Claude stops hunting for missing files."})
    prio_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    fixes.sort(key=lambda f: prio_order.get(f["priority"], 9))

    # summary
    custom = [s for s in skills if not s["is_generic"]]
    summary = {
        "generated": datetime.now().strftime("%d %B %Y, %H:%M"),
        "source_dir": os.path.abspath(args.skills_dir),
        "total_skills": len(skills),
        "custom_skills": len(custom),
        "generic_skills": len(skills) - len(custom),
        "avg_hygiene": round(sum(s["hygiene_score"] for s in custom) / max(1, len(custom))),
        "avg_equiai": round(sum(s["equiai_score"] for s in custom) / max(1, len(custom))),
        "avg_overall": round(sum(s["overall"] for s in custom) / max(1, len(custom))),
        "overlap_edges": len(overlap),
        "reference_edges": sum(len(s["references"]) for s in skills),
        "p0_count": sum(1 for f in fixes if f["priority"] == "P0"),
        "p1_count": sum(1 for f in fixes if f["priority"] == "P1"),
        "clusters": sorted({s["cluster"] for s in skills}),
        "equiai_pillar_coverage": {
            EQUIAI_PILLARS[k]["label"]: sum(1 for s in custom if k in s["equiai_pillars_hit"])
            for k in EQUIAI_PILLARS
        },
    }

    data = {"summary": summary, "skills": skills, "overlap": overlap, "fixes": fixes,
            "equiai_pillars": {k: {"label": v["label"], "blurb": v["blurb"]}
                               for k, v in EQUIAI_PILLARS.items()}}
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
    print(f"Audited {len(skills)} skills ({len(custom)} custom). "
          f"Avg overall {summary['avg_overall']}. "
          f"{summary['overlap_edges']} overlap edges, {len(fixes)} fixes queued. -> {args.out}")


if __name__ == "__main__":
    main()
