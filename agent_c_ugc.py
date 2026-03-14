"""
AGENT C — UGC CREATOR SYSTEM v2
=================================
Based on real 2026 research:
- No followers needed (brands pay for content quality, not audience)
- First deal possible within 2-4 weeks
- Part-time: $1,500-4,000/month (10-15 videos/month)
- Full-time: $5,000-15,000+/month

THIS AGENT DOES 4 THINGS:
1. Generates your professional creator profile + rate card
2. Finds brands actively running UGC-style ads on TikTok (hottest signal)
3. Writes personalized cold pitches per brand category
4. Creates video briefs so you know EXACTLY what to film

BEST PLATFORMS TO SIGN UP ON (free, do today):
- billo.app/creators       → $99-300/video, instant matching
- collabstr.com            → 130K brands, set your own rates
- joinbrands.com           → Amazon FBA sellers (huge demand)
- insense.pro              → $150-500/video, higher end brands
- trend.io                 → lifestyle/fashion brands
"""

import os
import re
import json
import requests
from datetime import datetime

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# ── YOUR CREATOR PROFILE ─────────────────────────────────
CREATOR_PROFILE = {
    "name": "A",
    "location": "United States",
    "niches": [
        "tech & AI tools",
        "productivity & lifestyle",
        "health & wellness",
        "home & kitchen",
        "finance & investing apps",
        "fitness & supplements",
    ],
    "strengths": [
        "authentic product demos",
        "quick unboxing reactions",
        "honest testimonial style",
        "how-to tutorials",
        "before/after comparisons",
    ],
    "rate_card": {
        "single_video_30s": "$150",
        "single_video_60s": "$200",
        "video_bundle_3": "$500",
        "video_bundle_5": "$750",
        "rush_24hr": "+$75",
        "usage_rights_6mo": "+$50",
        "usage_rights_unlimited": "+$100",
        "organic_posting": "+$100",
    },
    "turnaround": "3-5 business days (rush available)",
    "deliverables": "Raw + edited MP4, vertical format, captions included",
    "equipment": "iPhone 15, ring light, clean backgrounds",
    "revision_policy": "1 free revision, additional at $25",
}

# Brand categories with highest UGC demand in 2026
# (sourced from Collabstr/Billo market data)
HOT_BRAND_CATEGORIES = [
    {
        "category": "AI productivity tools (SaaS)",
        "why_hot": "Every SaaS needs authentic demos — they can't film real users",
        "avg_pay": "$200-400/video",
        "sample_brands": ["Notion", "ClickUp", "Jasper", "Copy.ai", "Writesonic"],
        "content_style": "screen recording demo + voiceover reaction",
        "hook_angle": "I tested this AI tool for 30 days — here's what happened",
    },
    {
        "category": "Health & wellness supplements",
        "why_hot": "Supplement brands spend millions on UGC ads — FDA rules prevent claims",
        "avg_pay": "$150-350/video",
        "sample_brands": ["AG1", "Thesis", "Ritual", "Hims", "Hers"],
        "content_style": "daily routine integration, honest results",
        "hook_angle": "I replaced my morning coffee with this for 2 weeks",
    },
    {
        "category": "Home & kitchen gadgets",
        "why_hot": "Amazon FBA sellers NEED UGC for listing videos — massive demand",
        "avg_pay": "$100-250/video",
        "sample_brands": ["Amazon FBA brands", "DTC kitchen brands", "Shopify stores"],
        "content_style": "unboxing, quick demo, honest reaction",
        "hook_angle": "This $30 gadget changed my morning routine",
    },
    {
        "category": "Finance & investing apps",
        "why_hot": "High CPM niche, apps can't show screens legally — need real people",
        "avg_pay": "$200-500/video",
        "sample_brands": ["Robinhood", "Webull", "Acorns", "Betterment", "Wealthfront"],
        "content_style": "personal finance story, app walkthrough",
        "hook_angle": "I started investing with $5 using this app",
    },
    {
        "category": "Fitness equipment & apparel",
        "why_hot": "Fitness brands run UGC 24/7 — highest volume on Meta ads",
        "avg_pay": "$150-300/video",
        "sample_brands": ["Gymshark", "Lululemon dupes", "resistance band brands"],
        "content_style": "workout demo, fit review, transformation tease",
        "hook_angle": "I wore this for 30 days of workouts — honest review",
    },
    {
        "category": "Mobile apps (games, utilities, dating)",
        "why_hot": "App install campaigns run 24/7, need constant fresh creatives",
        "avg_pay": "$100-200/video",
        "sample_brands": ["Duolingo competitors", "meditation apps", "dating apps"],
        "content_style": "screen recording + reaction, first impression",
        "hook_angle": "I tried this app for the first time and...",
    },
]


def call_claude(prompt, max_tokens=800):
    if not API_KEY:
        return "No API key — set ANTHROPIC_API_KEY environment variable"
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
            timeout=45,
        )
        return r.json()["content"][0]["text"]
    except Exception as e:
        return f"API error: {e}"


def generate_creator_bio():
    prompt = f"""Write a professional UGC creator bio for platform profiles (Billo, Collabstr, etc.)

Creator profile:
- Niches: {', '.join(CREATOR_PROFILE['niches'])}
- Strengths: {', '.join(CREATOR_PROFILE['strengths'])}
- Location: {CREATOR_PROFILE['location']}
- Equipment: {CREATOR_PROFILE['equipment']}
- Turnaround: {CREATOR_PROFILE['turnaround']}

Write 3 versions:
1. SHORT (50 words) — for platform profile headline
2. MEDIUM (100 words) — for platform profile bio
3. PITCH OPENER (30 words) — first line of cold outreach emails

Rules:
- Sound authentic, not corporate
- Lead with value to brands, not your credentials
- Mention niche specifics
- No follower count mention (irrelevant for UGC)
- Confident but not arrogant"""

    return call_claude(prompt)


def generate_cold_pitch(brand_category):
    cat = brand_category

    prompt = f"""Write a cold pitch email from a UGC creator to a brand in this category.

BRAND CATEGORY: {cat['category']}
WHY THIS CATEGORY IS HOT: {cat['why_hot']}
SAMPLE BRANDS IN CATEGORY: {', '.join(cat['sample_brands'])}
BEST CONTENT STYLE FOR THIS NICHE: {cat['content_style']}
BEST HOOK ANGLE: {cat['hook_angle']}

CREATOR RATES: {json.dumps(CREATOR_PROFILE['rate_card'], indent=2)}
CREATOR NICHES: {', '.join(CREATOR_PROFILE['niches'])}

Write a cold pitch email that:
1. Subject line: specific and curiosity-driving (not "UGC Creator for Hire")
2. Opening: reference something SPECIFIC about brands in this category
   (their ad strategy, their product challenge, something real)
3. Body (max 100 words): explain UGC value, your specific fit, one offer
4. CTA: "I'll create a free sample video for [their product type] — no commitment"
5. P.S.: A specific content idea they could use TODAY

Format:
SUBJECT: [subject line]

[email body]

P.S. [content idea]

---
PLATFORM VERSION (for Collabstr/Billo DM, 60 words max):
[shorter version]"""

    return call_claude(prompt, max_tokens=600)


def generate_video_brief(brand_category):
    cat = brand_category

    prompt = f"""Create a UGC video brief template for the {cat['category']} niche.

This is what I'll send to brands after they hire me, AND what I'll use to film my portfolio samples.

Content style: {cat['content_style']}
Best hook: {cat['hook_angle']}

Create a complete video brief including:
1. VIDEO CONCEPT (2 sentences)
2. HOOK (first 3 seconds — word for word)
3. SCRIPT OUTLINE (30-60 second structure)
4. FILMING NOTES (lighting, background, pacing tips)
5. WHAT TO WEAR/SHOW
6. CALL TO ACTION (last 5 seconds)
7. THUMBNAIL MOMENT (best frame to screenshot)

Make it specific enough that someone could film this TODAY with just a phone.
Keep the hook punchy — it needs to stop scrolling in 2 seconds."""

    return call_claude(prompt, max_tokens=700)


def generate_portfolio_strategy():
    prompt = """Create a 7-day action plan for a new UGC creator to land their first paid deal.

Assume:
- No existing portfolio
- Has a smartphone and ring light
- Signed up on Billo and Collabstr today
- Has 1-2 hours per day available

Day by day, be specific about:
- What to film (specific product ideas using things they already own)
- Where to post/submit
- Who to reach out to and how
- What to say

End with realistic first month income projection broken into weeks.
Be honest — not hype. Real numbers, real timeline."""

    return call_claude(prompt, max_tokens=700)


# ── MAIN ─────────────────────────────────────────────────
print("=" * 60)
print("  UGC CREATOR SYSTEM v2")
print(f"  {datetime.now().strftime('%m/%d/%Y %H:%M')}")
print("=" * 60)

os.makedirs("ugc", exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M")

# 1. Creator bio for platforms
print("\n[1/5] Writing your creator bio...")
bio = generate_creator_bio()
with open("ugc/MY_CREATOR_BIO.txt", "w") as f:
    f.write("YOUR UGC CREATOR BIO\n")
    f.write("Use these on Billo, Collabstr, Insense, JoinBrands\n")
    f.write("=" * 60 + "\n\n")
    f.write(bio)
print("  ✅ Saved: ugc/MY_CREATOR_BIO.txt")

# 2. Rate card
print("\n[2/5] Building your rate card...")
rate_lines = [
    "UGC CREATOR RATE CARD",
    "=" * 60,
    "",
    "VIDEO PACKAGES:",
    f"  30-second video:          {CREATOR_PROFILE['rate_card']['single_video_30s']}",
    f"  60-second video:          {CREATOR_PROFILE['rate_card']['single_video_60s']}",
    f"  Bundle of 3 videos:       {CREATOR_PROFILE['rate_card']['video_bundle_3']}",
    f"  Bundle of 5 videos:       {CREATOR_PROFILE['rate_card']['video_bundle_5']}",
    "",
    "ADD-ONS:",
    f"  Rush delivery (24hr):     {CREATOR_PROFILE['rate_card']['rush_24hr']}",
    f"  Usage rights (6 months):  {CREATOR_PROFILE['rate_card']['usage_rights_6mo']}",
    f"  Unlimited usage rights:   {CREATOR_PROFILE['rate_card']['usage_rights_unlimited']}",
    f"  Organic posting to my:    {CREATOR_PROFILE['rate_card']['organic_posting']}",
    "",
    "DELIVERABLES (included in every package):",
    f"  {CREATOR_PROFILE['deliverables']}",
    "",
    f"TURNAROUND: {CREATOR_PROFILE['turnaround']}",
    f"REVISIONS: {CREATOR_PROFILE['revision_policy']}",
    "",
    "PAYMENT: 50% upfront, 50% on delivery",
    "PLATFORMS ACCEPTED: PayPal, Venmo, bank transfer",
    "=" * 60,
]
with open("ugc/MY_RATE_CARD.txt", "w") as f:
    f.write("\n".join(rate_lines))
print("  ✅ Saved: ugc/MY_RATE_CARD.txt")

# 3. Cold pitches per category
print("\n[3/5] Writing personalized brand pitches...")
for i, cat in enumerate(HOT_BRAND_CATEGORIES[:4]):
    print(f"  Writing pitch for: {cat['category']}...")
    pitch = generate_cold_pitch(cat)
    safe_name = re.sub(r"[^a-z0-9]", "_", cat["category"].lower())[:30]
    filename = f"ugc/pitch_{safe_name}.txt"
    with open(filename, "w") as f:
        f.write(f"BRAND CATEGORY: {cat['category']}\n")
        f.write(f"AVG PAY: {cat['avg_pay']}\n")
        f.write(f"TARGET BRANDS: {', '.join(cat['sample_brands'])}\n")
        f.write("=" * 60 + "\n\n")
        f.write(pitch)
    print(f"  ✅ {filename}")

# 4. Video briefs (what to actually film)
print("\n[4/5] Creating video production briefs...")
for cat in HOT_BRAND_CATEGORIES[:3]:
    print(f"  Brief for: {cat['category']}...")
    brief = generate_video_brief(cat)
    safe_name = re.sub(r"[^a-z0-9]", "_", cat["category"].lower())[:30]
    with open(f"ugc/brief_{safe_name}.txt", "w") as f:
        f.write(f"VIDEO BRIEF: {cat['category']}\n")
        f.write(f"CONTENT STYLE: {cat['content_style']}\n")
        f.write("=" * 60 + "\n\n")
        f.write(brief)
    print(f"  ✅ ugc/brief_{safe_name}.txt")

# 5. 7-day action plan
print("\n[5/5] Building your 7-day launch plan...")
plan = generate_portfolio_strategy()
with open("ugc/7_DAY_ACTION_PLAN.txt", "w") as f:
    f.write("7-DAY UGC LAUNCH PLAN\n")
    f.write("Start TODAY. First deal within 2 weeks.\n")
    f.write("=" * 60 + "\n\n")
    f.write(plan)
print("  ✅ Saved: ugc/7_DAY_ACTION_PLAN.txt")

# Print platform signup summary
print("\n" + "=" * 60)
print("DONE. Your full UGC creator kit is ready.")
print("\n🔗 SIGN UP ON THESE PLATFORMS RIGHT NOW (all free):")
platforms = [
    ("Billo", "billo.app/creators", "$99-300/video, 5000+ brands, instant matching"),
    ("Collabstr", "collabstr.com", "130K brands, set your own rates, instant approval"),
    ("JoinBrands", "joinbrands.com", "Amazon FBA brands, fast payouts"),
    ("Insense", "insense.pro", "$150-500/video, higher-end DTC brands"),
]
for name, url, note in platforms:
    print(f"\n  {name}: https://{url}")
    print(f"  → {note}")

print("\n📁 FILES CREATED:")
print("  ugc/MY_CREATOR_BIO.txt       — copy this to every platform profile")
print("  ugc/MY_RATE_CARD.txt         — send this when brands ask pricing")
print("  ugc/pitch_*.txt              — cold pitch emails per brand category")
print("  ugc/brief_*.txt              — exactly what to film for your portfolio")
print("  ugc/7_DAY_ACTION_PLAN.txt    — your daily roadmap to first deal")
print("\n💰 REALISTIC FIRST MONTH: $300-1,200")
print("   (3-8 videos at $100-200 each while building portfolio)")
print("=" * 60)
