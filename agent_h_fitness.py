"""
AGENT H — FITNESS CONTENT ENGINE v2
======================================
Alejandro. San Diego. 7 years training. Athletic / functional aesthetic.
Starting fresh on camera. Under 1K on Instagram. 20K on X.
All product categories. Outdoor + gym + beach content.
Building from zero to brand deals.

STRATEGY FOR STARTING FRESH ON CAMERA:
- Week 1-2: No face required. Hands, movements, equipment, environment.
- Week 3-4: Back to camera, side angles. Build comfort gradually.
- Month 2+: Face to camera once comfortable. By then content is proven.

This approach lets you build an audience and content library
before putting your face fully out there. Smart, not shy.

ZERO AI MENTIONS anywhere in output. Ever.
Reads like someone who lives this lifestyle and knows what they're doing.
"""

import os
import requests
import random
from datetime import datetime

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "").strip()

CREATOR = {
    "location": "San Diego",
    "years": 7,
    "aesthetic": "athletic and functional — strong, capable, built to move",
    "environments": ["gym", "beach", "outdoor San Diego", "home"],
    "camera_stage": "starting fresh — building up to face cam gradually",
    "ig_followers": "under 1K",
    "x_followers": "20K",
    "products": ["supplements", "apparel", "equipment", "nutrition", "recovery"],
    "tone": "real, direct, no motivational fluff — someone who actually trains",
    "platforms": {
        "growth": "TikTok + Instagram Reels",
        "existing": "X/Twitter (20K)",
        "longterm": "YouTube",
    }
}

# Content that works WITHOUT showing face first
NO_FACE_FORMATS = [
    "hands loading a barbell — no face needed, pure aesthetic",
    "feet walking into gym / onto beach / court",
    "back + shoulders shot during a lift",
    "POV workout — camera held during movement",
    "hands + equipment close up — pre-workout ritual",
    "silhouette against San Diego sunset or outdoor light",
    "workout from behind — shows physique without face",
    "split screen — before and after sets, no face",
    "time lapse of a full workout, wide shot",
    "hands gripping bar — chalk, calluses, the real thing",
]

# Content once comfortable on camera (month 2+)
FACE_CAM_FORMATS = [
    "talking through a training mistake after 7 years",
    "honest take on a supplement — does it actually work",
    "day in the life — SD outdoor + gym",
    "reaction to common fitness advice that's wrong",
    "physique check — athletic functional build",
]

# Rotating content pillars
PILLARS = {
    0: ("training", "a specific movement, lift, or training concept"),
    1: ("physique", "the athletic aesthetic — what it looks like and how it's built"),
    2: ("lifestyle", "San Diego gym culture, outdoor training, the environment"),
    3: ("nutrition", "what actually fuels the training — real food, real supplements"),
    4: ("mindset", "7 years in — what changed, what stayed, what was wrong"),
    5: ("gear", "what I actually use — apparel, equipment, supplements"),
    6: ("progress", "showing the work — no motivation speech, just results"),
}

AFFILIATE_MAP = {
    "supplements": {"name": "pre-workout or protein", "placeholder": "[SUPPLEMENT_LINK]", "angle": "what I actually take"},
    "apparel": {"name": "gym apparel", "placeholder": "[APPAREL_LINK]", "angle": "what I train in"},
    "equipment": {"name": "gym equipment", "placeholder": "[EQUIPMENT_LINK]", "angle": "what's actually in my bag"},
    "nutrition": {"name": "nutrition product", "placeholder": "[NUTRITION_LINK]", "angle": "how I hit my macros"},
    "recovery": {"name": "recovery tool", "placeholder": "[RECOVERY_LINK]", "angle": "what keeps me training consistently"},
}

HANDLE_IDEAS = [
    "@apexphysique.sd",
    "@alejandro.builds",
    "@sd.athlete",
    "@functionalsd",
    "@buildingalejandro",
    "@apexathletic",
]


def call_claude(prompt, max_tokens=600):
    if not API_KEY:
        return "No API key"
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


def get_todays_pillar():
    day = datetime.now().weekday()
    return PILLARS.get(day, PILLARS[0])


def write_ig_caption(pillar_name, pillar_focus, affiliate):
    prompt = f"""Write an Instagram caption for a fitness creator.

CREATOR CONTEXT:
- Location: San Diego — gym, beach, outdoor training
- Training: 7 years in. Athletic and functional aesthetic. Built to move.
- Stage: Just starting to post. Under 1K followers. Building from scratch.
- Tone: {CREATOR['tone']}

TODAY'S PILLAR: {pillar_name} — {pillar_focus}
AFFILIATE TO EMBED: {affiliate['name']} — {affiliate['angle']}
LINK PLACEHOLDER: {affiliate['placeholder']}

CAPTION RULES:
- 3-5 lines. Short. White space matters.
- First line stops scrolling — specific, not generic
- One affiliate mention only, woven into the story naturally
- Ends with something that invites a comment or save
- NO hashtags in caption (go in first comment)
- NO emojis unless genuinely needed
- Sound like someone who trains, not someone who posts about training

Write the caption only. Nothing else."""
    return call_claude(prompt, 250)


def write_ig_hashtags(pillar_name):
    prompt = f"""Instagram hashtags for a fitness / athletic aesthetic post about: {pillar_name}
San Diego based creator. Athletic functional physique.

Give exactly 25 hashtags:
- 5 broad (1M+ posts)
- 12 medium (50K-500K posts)
- 8 niche under 50K (best for engagement)

Return only hashtags, space separated, one line."""
    return call_claude(prompt, 150)


def write_tiktok(pillar_name, pillar_focus, camera_stage):
    no_face = random.choice(NO_FACE_FORMATS)
    prompt = f"""Write a TikTok concept for a fitness creator just starting out.

CREATOR: San Diego. 7 years training. Athletic functional build.
Starting fresh on camera — not comfortable with face cam yet.
PILLAR: {pillar_name} — {pillar_focus}

CAMERA APPROACH FOR TODAY: {no_face}
(Creator is building up to face cam — starting with no-face formats)

Write:
HOOK: (text overlay, first 2 seconds — stops scrolling)
FORMAT: (exactly what type of shot and why no face is needed)
SHOT LIST: (3-5 shots, each under 5 seconds)
MUSIC VIBE: (energy/feel — no specific song names)
CAPTION: (under 100 chars, no more than 3 hashtags)
WHY IT WORKS: (one sentence — algorithm reason)

Native TikTok feel. Not polished. Real."""
    return call_claude(prompt, 400)


def write_x_post(pillar_name):
    prompt = f"""Write a tweet for a fitness creator with 20K followers.

Pillar: {pillar_name}
Location: San Diego
Background: 7 years training, athletic functional build
Tone: {CREATOR['tone']}

Rules:
- Under 240 characters
- No hashtags
- Real thought — not content
- Makes someone with an interest in fitness stop and read
- Could be a take, an observation, something that happened at the gym, or a hard truth
- Not motivational poster language. Ever.

Write the tweet only."""
    return call_claude(prompt, 120)


def write_stories(pillar_name):
    prompt = f"""3 Instagram Story ideas for a San Diego fitness creator.

Pillar: {pillar_name}
Creator just starting out — under 1K followers, building.
Athletic functional physique. Trains outdoors + gym + beach.

Each story:
- One clear concept (2 sentences)
- Type: photo / video / poll / question sticker
- Takes under 3 minutes to create
- Designed to get replies or saves

Number them 1, 2, 3. Brief. Specific."""
    return call_claude(prompt, 300)


def write_youtube(pillar_name, pillar_focus):
    prompt = f"""YouTube video concept for a fitness creator building from scratch.

Creator: San Diego. 7 years training. Athletic functional aesthetic.
Pillar: {pillar_name} — {pillar_focus}
Goal: rank on search AND get clicks from suggested

Write:
TITLE: (SEO-optimized, under 58 chars, high click rate)
THUMBNAIL: (image concept + text overlay — no face required yet)
HOOK: (first 30 seconds — what makes them stay)
OUTLINE: (5-7 minutes, 4-5 chapters)
SEARCH KEYWORDS: (3 terms this would rank for)
AFFILIATE FIT: (which product category fits naturally)

Should work as a no-face video — voiceover + gym footage."""
    return call_claude(prompt, 500)


def write_brand_dm(pillar_name, affiliate):
    prompt = f"""Cold DM to a {affiliate['name']} brand from a fitness creator.

Creator stats: 7 years training, 20K on X, building Instagram from scratch
Location: San Diego. Athletic functional build. Outdoor + gym content.
Today's content angle: {pillar_name}

DM rules:
- Under 80 words
- References something specific about their brand: [BRAND NAME] placeholder
- Leads with content value, not follower count
- Specific offer: free UGC video or collab Reel
- Sounds like a real person who actually uses their product

Write the DM only."""
    return call_claude(prompt, 200)


def suggest_handle():
    prompt = f"""Suggest 5 Instagram/TikTok handle ideas for a fitness creator.

Profile: San Diego based. 7 years training. Athletic functional aesthetic.
Gym + beach + outdoor content. Building a real brand.

Rules:
- Short (under 20 chars)
- Memorable and brandable
- Could expand beyond just fitness later
- Not cheesy or overly generic
- No numbers if possible

Format: @handle — one line reason why it works
Number them 1-5."""
    return call_claude(prompt, 200)


# ── MAIN ─────────────────────────────────────────────────
print("=" * 60)
print("  FITNESS CONTENT ENGINE v2")
print(f"  {datetime.now().strftime('%A, %B %d %Y')}")
print(f"  Location: {CREATOR['location']}")
print("=" * 60)

os.makedirs("fitness", exist_ok=True)
today = datetime.now().strftime("%Y%m%d")
pillar_name, pillar_focus = get_todays_pillar()
affiliate_category = random.choice(CREATOR["products"])
affiliate = AFFILIATE_MAP[affiliate_category]

print(f"\nPillar: {pillar_name} — {pillar_focus}")
print(f"Affiliate: {affiliate['name']}")

lines = []
lines.append(f"FITNESS CONTENT — {datetime.now().strftime('%A %B %d, %Y')}")
lines.append(f"Pillar: {pillar_name.upper()} — {pillar_focus}")
lines.append(f"Affiliate today: {affiliate['name']} | {affiliate['placeholder']}")
lines.append("=" * 60)

print("\n[1/7] Instagram caption...")
ig = write_ig_caption(pillar_name, pillar_focus, affiliate)
tags = write_ig_hashtags(pillar_name)
lines += ["\n📸 INSTAGRAM CAPTION", "─" * 40, ig,
          "\nFIRST COMMENT — paste these hashtags:", tags]

print("[2/7] TikTok concept...")
tiktok = write_tiktok(pillar_name, pillar_focus, CREATOR["camera_stage"])
lines += ["\n\n🎵 TIKTOK CONCEPT", "─" * 40, tiktok]

print("[3/7] X post...")
x = write_x_post(pillar_name)
lines += ["\n\n𝕏 X / TWITTER", "─" * 40, x]

print("[4/7] Stories...")
stories = write_stories(pillar_name)
lines += ["\n\n📱 INSTAGRAM STORIES", "─" * 40, stories]

print("[5/7] YouTube concept...")
yt = write_youtube(pillar_name, pillar_focus)
lines += ["\n\n▶️  YOUTUBE CONCEPT", "─" * 40, yt]

print("[6/7] Brand DM...")
dm = write_brand_dm(pillar_name, affiliate)
lines += ["\n\n💼 BRAND DEAL DM", "─" * 40,
          "Send to 3-5 brands today on Instagram or email:", dm,
          f"\nReplace [BRAND NAME] and {affiliate['placeholder']} before sending"]

print("[7/7] Handle suggestions...")
handles = suggest_handle()
lines += ["\n\n🏷️  BRAND HANDLE IDEAS", "─" * 40,
          "Pick one and lock it in across all platforms:", handles]

lines += [
    "\n\n📅 TODAY'S SCHEDULE",
    "─" * 40,
    "Morning  — Post X tweet (your 20K audience sees it immediately)",
    "Noon     — Post Instagram (caption above, stories after)",
    "Afternoon — Film TikTok concept above (10 min max)",
    "Evening  — Send 3 brand DMs",
    "",
    "NO FACE NEEDED TODAY — start with the no-face format above.",
    "Build comfort first. Face cam comes when you're ready.",
    "",
    f"⚠️  Replace {affiliate['placeholder']} with your real affiliate link before posting.",
]

with open(f"fitness/CONTENT_{today}.txt", "w") as f:
    f.write("\n".join(lines))

print(f"\n✅ Saved: fitness/CONTENT_{today}.txt")
print("\n" + "=" * 60)
print("READY. Here's your day:")
print(f"  Pillar: {pillar_name}")
print(f"  Affiliate: {affiliate['name']}")
print("  No face needed — no-face format today")
print("  Handle ideas included — pick one today")
print("=" * 60)
