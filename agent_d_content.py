"""
AGENT D — CONTENT FACTORY + AFFILIATE ENGINE v2
=================================================
Based on real 2026 data:
- Faceless channels earn $2,800-15,000/month (proven, not hype)
- Affiliate marketing earns MORE than AdSense for most channels
- YouTube ALLOWS AI narration + AI-assisted editing (must disclose)
- YouTube BANS mass-produced low-value content (no original thought)

THIS AGENT PRODUCES CONTENT THAT SURVIVES YOUTUBE'S AI DETECTION:
- Every script includes original research + specific data points
- Hooks are written to maximize watch time (key algorithm signal)
- Each video has a clear affiliate monetization angle built in
- Scripts are written to sound like a real person, not a bot

NICHE SELECTED: "AI tools + passive income + financial freedom"
WHY: Highest CPM on YouTube ($15-25 per 1000 views vs $2-4 for gaming)
     Every video has natural affiliate opportunities (20-40% commission)
     Evergreen content — videos earn for years, not days

AFFILIATE PROGRAMS TO JOIN TODAY (all free, most instant):
- ClickUp:    clickup.com/affiliates          → $200/signup
- Hostinger:  hostinger.com/affiliates        → 60% per sale  
- Jasper AI:  jasper.ai/affiliate-program     → 30% recurring
- NordVPN:    nordvpn.com/affiliate           → $100+/sale
- Fiverr:     affiliates.fiverr.com           → $15-150/sale
- Coursera:   about.coursera.org/affiliates   → 45% per course
"""

import os
import re
import json
import requests
from datetime import datetime

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# ── CHANNEL CONFIG ───────────────────────────────────────
CHANNEL = {
    "name": "AI Income Lab",  # suggested channel name
    "niche": "AI tools, passive income, financial freedom",
    "target_audience": "25-45 year olds wanting to quit 9-5 using AI",
    "tone": "direct, no-hype, real talk — like a friend who figured it out",
    "upload_schedule": "1 Short daily, 2 long-form per week",
    "monetization_priority": ["affiliate links", "sponsorships", "digital products", "AdSense"],
}

# Top affiliate programs mapped to content topics
AFFILIATE_MAP = {
    "AI writing tools": {
        "program": "Jasper AI",
        "commission": "30% recurring",
        "signup": "jasper.ai/affiliate-program",
        "placeholder": "[JASPER_AFFILIATE_LINK]",
    },
    "productivity software": {
        "program": "ClickUp",
        "commission": "$200 per signup",
        "signup": "clickup.com/affiliates",
        "placeholder": "[CLICKUP_AFFILIATE_LINK]",
    },
    "web hosting / online business": {
        "program": "Hostinger",
        "commission": "60% per sale",
        "signup": "hostinger.com/affiliates",
        "placeholder": "[HOSTINGER_AFFILIATE_LINK]",
    },
    "VPN / online privacy": {
        "program": "NordVPN",
        "commission": "$100+ per sale",
        "signup": "nordvpn.com/affiliate",
        "placeholder": "[NORDVPN_AFFILIATE_LINK]",
    },
    "online courses / skills": {
        "program": "Coursera",
        "commission": "45% per course",
        "signup": "about.coursera.org/affiliates",
        "placeholder": "[COURSERA_AFFILIATE_LINK]",
    },
    "freelance marketplace": {
        "program": "Fiverr",
        "commission": "$15-150 per sale",
        "signup": "affiliates.fiverr.com",
        "placeholder": "[FIVERR_AFFILIATE_LINK]",
    },
}

# Video topics — mix of Shorts and long-form
VIDEO_TOPICS = [
    # HIGH-VALUE LONG FORM (8-12 min, $15-25 CPM)
    {
        "title": "I Used 5 AI Tools for 30 Days to Make Money — Honest Results",
        "type": "long_form",
        "affiliate": "AI writing tools",
        "why_it_works": "Review format = highest affiliate click rate, personal story = watch time",
        "estimated_rpm": "$18-22",
    },
    {
        "title": "The $0 Passive Income System I Built With Free AI Tools",
        "type": "long_form",
        "affiliate": "productivity software",
        "why_it_works": "Zero cost hook is irresistible, system reveal = high completion rate",
        "estimated_rpm": "$20-25",
    },
    {
        "title": "How I Automated My Freelance Work With AI (Step by Step)",
        "type": "long_form",
        "affiliate": "freelance marketplace",
        "why_it_works": "Tutorial format = highest watch time, directly actionable",
        "estimated_rpm": "$15-20",
    },
    # YOUTUBE SHORTS (traffic drivers → long form → affiliate clicks)
    {
        "title": "This AI Tool Saved Me 10 Hours Last Week",
        "type": "short",
        "affiliate": "productivity software",
        "why_it_works": "Specific number hook, relatable pain point",
        "estimated_rpm": "$0.05-0.13",
    },
    {
        "title": "3 AI Side Hustles You Can Start Tonight",
        "type": "short",
        "affiliate": "AI writing tools",
        "why_it_works": "List format + urgency = highest share rate",
        "estimated_rpm": "$0.05-0.13",
    },
    {
        "title": "Nobody Talks About This Passive Income Method",
        "type": "short",
        "affiliate": "online courses / skills",
        "why_it_works": "Curiosity gap forces completion, strong CTA for long video",
        "estimated_rpm": "$0.05-0.13",
    },
]


def call_claude(prompt, max_tokens=1200):
    if not API_KEY:
        return "No API key — set ANTHROPIC_API_KEY"
    try:
        r = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": max_tokens,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=60,
        )
        return r.json()["content"][0]["text"]
    except Exception as e:
        return f"API error: {e}"


def generate_script(video):
    affiliate_info = AFFILIATE_MAP.get(video["affiliate"], {})
    aff_program = affiliate_info.get("program", "relevant tool")
    aff_placeholder = affiliate_info.get("placeholder", "[AFFILIATE_LINK]")
    aff_commission = affiliate_info.get("commission", "commission")

    if video["type"] == "short":
        format_guide = """YouTube Short script (55-70 seconds when read aloud, ~140-160 words):

STRUCTURE:
- HOOK (0-3s): Bold statement or question. Must stop scrolling instantly.
- PROBLEM (3-10s): Why this matters right now, one sentence.
- VALUE DELIVERY (10-45s): 3 fast specific points. Each one sentence max.
- AFFILIATE CTA (45-55s): Natural mention of one tool, with link reference.
- FOLLOW CTA (55-65s): "Follow for more like this."

RULES:
- Every sentence earns its place — cut anything that doesn't add value
- Use specific numbers: "saves 3 hours" not "saves time"
- Sound like texting a friend, not presenting to a boardroom
- The affiliate mention must feel earned and natural, not forced"""

    else:
        format_guide = """Long-form YouTube script (9-11 minutes when read aloud, ~1,300-1,600 words):

STRUCTURE:
- HOOK (0-30s, ~70 words): Bold claim + preview of 3 specific things they'll learn
- INTRO (30s-2min, ~200 words): Personal story establishing credibility on this topic
- SECTION 1 (2-4min, ~300 words): First major point with specific examples + data
- SECTION 2 (4-6min, ~300 words): Second major point — go deeper than intro videos
- SECTION 3 (6-8min, ~300 words): Third point — this is where the real value lives
- AFFILIATE INTEGRATION (8-9min, ~150 words): Natural tool recommendation with story
- RECAP + CTA (9-11min, ~100 words): Summarize, affiliate link reminder, subscribe

RULES:
- Open loops: tease what's coming to keep people watching
- Pattern interrupt every 2 minutes: change topic angle or add a story
- Affiliate integration must include: what you use it for + one honest limitation
- All stats and claims must sound specific and researched (use exact numbers)
- Disclosure: "Some links in the description are affiliate links" (required by YouTube)"""

    prompt = f"""Write a complete YouTube {video['type']} script.

CHANNEL: {CHANNEL['name']} — {CHANNEL['niche']}
AUDIENCE: {CHANNEL['target_audience']}
TONE: {CHANNEL['tone']}

VIDEO TITLE: {video['title']}
AFFILIATE TO FEATURE: {aff_program} ({aff_commission})
USE THIS PLACEHOLDER FOR THE LINK: {aff_placeholder}

FORMAT TO FOLLOW:
{format_guide}

IMPORTANT — Why this video works (use this insight to shape the script):
{video['why_it_works']}

Write the complete script now. Start with the hook — no preamble.
The script must:
1. Sound like a real person who has actually done this
2. Include at least 2 specific data points or real examples
3. Naturally integrate the affiliate product where it fits the content
4. Be optimized for watch time (open loops, curiosity, payoffs)"""

    return call_claude(prompt, max_tokens=2000)


def generate_description(video, script_preview):
    affiliate_info = AFFILIATE_MAP.get(video["affiliate"], {})
    aff_program = affiliate_info.get("program", "")
    aff_signup = affiliate_info.get("signup", "")
    aff_placeholder = affiliate_info.get("placeholder", "[AFFILIATE_LINK]")

    prompt = f"""Write a complete YouTube video description for this video.

Title: {video['title']}
Type: {video['type']}
Script preview: {script_preview[:400]}
Affiliate featured: {aff_program} ({aff_signup})

Include:
1. FIRST 2 LINES (shown before "show more"): must hook clicks, include main keyword
2. VIDEO SUMMARY (100 words): what they'll learn, conversational
3. TIMESTAMPS (realistic for the structure, even if approximate)
4. TOOLS MENTIONED: list with {aff_placeholder} for the affiliate
5. AFFILIATE DISCLOSURE: "Some links are affiliate links — I earn a commission at no cost to you"
6. CONNECT: social links placeholder
7. TAGS: 25 SEO-optimized tags as comma-separated list

Start with the two hook lines immediately."""

    return call_claude(prompt, max_tokens=600)


def generate_thumbnail_concepts(video):
    prompt = f"""Generate 3 high-CTR YouTube thumbnail concepts for:
"{video['title']}"

For each concept provide:
- BACKGROUND: color/image description
- MAIN TEXT: max 5 words, all caps, bold
- SECONDARY TEXT: max 4 words (smaller)
- FACE/EXPRESSION: what emotion to show (if using face)
- VISUAL ELEMENT: one icon or image to include
- WHY IT WORKS: one sentence on the psychology

The best thumbnails for this niche use: contrast, curiosity, specific numbers, faces.
Format: numbered list, each concept clearly separated."""

    return call_claude(prompt, max_tokens=400)


def save_content_package(video, script, description, thumbnails):
    os.makedirs("content", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    safe_title = re.sub(r"[^a-z0-9]", "_", video["title"].lower())[:35]
    folder = f"content/{timestamp}_{video['type']}_{safe_title}"
    os.makedirs(folder, exist_ok=True)

    # Script file
    with open(f"{folder}/SCRIPT.txt", "w") as f:
        f.write(f"TITLE: {video['title']}\n")
        f.write(f"TYPE: {video['type'].upper()}\n")
        f.write(f"AFFILIATE: {AFFILIATE_MAP.get(video['affiliate'], {}).get('program', '')}\n")
        f.write(f"EST. RPM: {video['estimated_rpm']}\n")
        f.write(f"DATE: {datetime.now().strftime('%m/%d/%Y')}\n")
        f.write("=" * 60 + "\n\n")
        f.write("⚠️  DISCLOSURE: Add 'AI-assisted content' to description (YouTube policy)\n\n")
        f.write(script)

    # Description file
    with open(f"{folder}/DESCRIPTION.txt", "w") as f:
        f.write("VIDEO DESCRIPTION\n")
        f.write("Replace [AFFILIATE_LINK_*] with your real affiliate links\n")
        f.write("=" * 60 + "\n\n")
        f.write(description)

    # Thumbnails file
    with open(f"{folder}/THUMBNAILS.txt", "w") as f:
        f.write("THUMBNAIL CONCEPTS\n")
        f.write("Use Canva (free) to create. Pick concept 1 first, A/B test later.\n")
        f.write("=" * 60 + "\n\n")
        f.write(thumbnails)

    # Production checklist
    if video["type"] == "short":
        checklist = f"""SHORT VIDEO CHECKLIST
Title: {video['title']}
Target length: 55-70 seconds
{"="*50}

RECORD:
[ ] Read script 2x to memorize flow (don't read off screen)
[ ] Film vertical (9:16 ratio)  
[ ] Good lighting (face near window or ring light)
[ ] Clean simple background
[ ] Record 2-3 takes, pick the most natural

EDIT (CapCut — free):
[ ] Trim silences (pace should feel fast)
[ ] Add captions (auto-caption in CapCut, fix errors)
[ ] Add 1-2 text overlays on key stats
[ ] Background music at 10-15% volume (CapCut library)
[ ] Export: 1080x1920, MP4

UPLOAD:
[ ] Copy description from DESCRIPTION.txt
[ ] Add your affiliate link where placeholder says {AFFILIATE_MAP.get(video['affiliate'], {}).get('placeholder', '[LINK]')}
[ ] Schedule for 12-3pm EST (peak engagement)
[ ] Reply to first 5 comments within 1 hour (boosts algorithm)

EXPECTED RESULT:
First 48 hours: algorithm test (100-1000 views)  
If it hooks: can blow up to 10K-100K+ views
Affiliate clicks: typically 0.5-2% of viewers
"""
    else:
        checklist = f"""LONG-FORM VIDEO CHECKLIST  
Title: {video['title']}
Target length: 9-11 minutes
{"="*50}

RECORD:
[ ] Read full script at least 3x before recording
[ ] Record in 2-3 sections (easier than one take)
[ ] Consistent lighting throughout
[ ] Stable camera (tripod or propped up)
[ ] Good audio is MORE important than video quality

EDIT (CapCut or DaVinci Resolve free):
[ ] Cut dead air and ums/ahs
[ ] Add B-roll over boring sections (Pexels.com = free)
[ ] Captions (auto-caption, fix errors, style consistently)
[ ] Chapter markers (helps watch time + search)
[ ] End screen with subscribe button (last 20 seconds)

UPLOAD:
[ ] Use exact title from SCRIPT.txt (SEO optimized)
[ ] Copy full description from DESCRIPTION.txt
[ ] Add your real affiliate link where placeholder shows
[ ] Custom thumbnail from THUMBNAILS.txt concepts
[ ] Add to relevant playlist
[ ] Premiere or schedule (builds anticipation)

EXPECTED RESULT:
Month 1-2: 50-500 views per video (building)
Month 3+: algorithm picks up consistent content
RPM in this niche: {video['estimated_rpm']}
Affiliate income: can exceed AdSense from day 1
"""

    with open(f"{folder}/PRODUCTION_CHECKLIST.txt", "w") as f:
        f.write(checklist)

    return folder


# ── MAIN ─────────────────────────────────────────────────
print("=" * 60)
print("  CONTENT FACTORY + AFFILIATE ENGINE v2")
print(f"  Channel: {CHANNEL['name']}")
print(f"  {datetime.now().strftime('%m/%d/%Y %H:%M')}")
print("=" * 60)

os.makedirs("content", exist_ok=True)
produced = []

# Mix of shorts and long-form
to_produce = [
    v for v in VIDEO_TOPICS if v["type"] == "short"
][:2] + [
    v for v in VIDEO_TOPICS if v["type"] == "long_form"
][:1]

print(f"\nProducing {len(to_produce)} video packages...")

for i, video in enumerate(to_produce):
    print(f"\n[{i+1}/{len(to_produce)}] {video['type'].upper()}: {video['title'][:50]}...")

    print("  Writing script...")
    script = generate_script(video)

    print("  Writing description + tags...")
    description = generate_description(video, script[:500])

    print("  Creating thumbnail concepts...")
    thumbnails = generate_thumbnail_concepts(video)

    print("  Saving package...")
    folder = save_content_package(video, script, description, thumbnails)
    produced.append((video, folder))
    print(f"  ✅ {folder}/")

# Affiliate signup sheet
print("\n[Extra] Generating affiliate signup guide...")
affiliate_guide_lines = [
    "AFFILIATE PROGRAMS — SIGN UP TODAY",
    "All free to join. Most instant approval.",
    "=" * 60,
    "",
]
for topic, info in AFFILIATE_MAP.items():
    affiliate_guide_lines += [
        f"PROGRAM: {info['program']}",
        f"Commission: {info['commission']}",
        f"Sign up: https://{info['signup']}",
        f"Best for content about: {topic}",
        f"Placeholder to replace in scripts: {info['placeholder']}",
        "",
    ]

affiliate_guide_lines += [
    "=" * 60,
    "AFTER SIGNING UP:",
    "1. Get your unique affiliate link for each program",
    "2. Add to Linktree (free) at linktr.ee — one link for all",
    "3. Put Linktree link in your YouTube bio and video descriptions",
    "4. In each video description, replace the placeholder with your real link",
    "5. Track clicks in each program's dashboard",
    "",
    "INCOME PROJECTION (realistic):",
    "Month 1: $0-50 (building content library)",
    "Month 2: $50-300 (gaining traction, first affiliate clicks)",
    "Month 3: $300-800 (compounding, consistent uploads)",
    "Month 6: $1,000-3,000 (if posting 1 Short/day + 2 long/week)",
    "Month 12: $3,000-10,000 (channel authority + evergreen income)",
]

with open("content/AFFILIATE_SIGNUP_GUIDE.txt", "w") as f:
    f.write("\n".join(affiliate_guide_lines))

print("  ✅ content/AFFILIATE_SIGNUP_GUIDE.txt")

print("\n" + "=" * 60)
print(f"DONE. {len(produced)} content packages ready.")
print("\n📁 WHAT WAS CREATED:")
for video, folder in produced:
    aff = AFFILIATE_MAP.get(video["affiliate"], {}).get("program", "")
    print(f"\n  [{video['type'].upper()}] {video['title'][:50]}")
    print(f"  Affiliate: {aff} | Est. RPM: {video['estimated_rpm']}")
    print(f"  → {folder}/SCRIPT.txt")
    print(f"  → {folder}/DESCRIPTION.txt")
    print(f"  → {folder}/THUMBNAILS.txt")
    print(f"  → {folder}/PRODUCTION_CHECKLIST.txt")

print("\n🔗 NEXT STEP — DO THIS TODAY:")
print("  1. Open content/AFFILIATE_SIGNUP_GUIDE.txt")
print("  2. Sign up for ClickUp + Hostinger affiliates (both instant)")
print("  3. Film the first Short using SCRIPT.txt (10 minutes, phone is fine)")
print("  4. Post it — the algorithm needs data to push your content")
print("\n💡 KEY INSIGHT FROM RESEARCH:")
print("  Channels earning $3K-10K/month posted for 3-6 months")
print("  before seeing results. The ones who quit in month 2 missed it.")
print("=" * 60)
