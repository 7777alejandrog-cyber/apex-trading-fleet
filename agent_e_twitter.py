"""
AGENT E — TWITTER/X CONTENT ENGINE
=====================================
You have 20K followers on X. This agent turns that into income.

Every run produces:
- 3 tweet threads (affiliate-optimized, engagement-driven)
- 5 standalone viral tweets
- 1 "income transparency" post (builds trust = more followers + sales)
- Affiliate link placement strategy per post

MONETIZATION STRATEGY:
- Threads about AI tools → affiliate links in replies
- Income transparency posts → drives DMs → UGC clients
- "I built this" posts → Gumroad digital product sales
- Consistent posting → brand deal inquiries ($500-2000/post at 20K)
"""

import os
import re
import json
import requests
from datetime import datetime

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "").strip()

CREATOR_CONTEXT = {
    "platform": "X (Twitter)",
    "followers": "20,000",
    "niche": "AI tools, passive income, building in public",
    "tone": "direct, real, no fluff — like someone who actually figured it out",
    "goal": "drive affiliate clicks, UGC client inquiries, digital product sales",
    "affiliate_links": {
        "ClickUp": "[CLICKUP_LINK]",
        "Jasper AI": "[JASPER_LINK]",
        "Hostinger": "[HOSTINGER_LINK]",
        "Notion": "[NOTION_LINK]",
    }
}

THREAD_TOPICS = [
    {
        "topic": "I automated my income using AI agents — here's exactly how",
        "affiliate": "ClickUp",
        "style": "building in public + step by step reveal",
        "cta": "drive DMs for UGC inquiries"
    },
    {
        "topic": "5 AI tools that replaced $2,000/month of work for me",
        "affiliate": "Jasper AI",
        "style": "listicle with honest takes, one limitation per tool",
        "cta": "affiliate link in thread reply"
    },
    {
        "topic": "How I'm making money while I sleep (real numbers, no BS)",
        "affiliate": "Hostinger",
        "style": "income transparency, vulnerable and real",
        "cta": "drive to digital product + affiliate"
    },
]

VIRAL_TWEET_ANGLES = [
    "controversial take on traditional jobs vs AI income",
    "specific number reveal about passive income progress",
    "mistake I made building income agents (gets engagement)",
    "one sentence that captures the AI income opportunity",
    "reply bait: what's stopping you from starting?",
]


def call_claude(prompt, max_tokens=800):
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


def write_thread(topic_data):
    prompt = f"""Write a high-engagement Twitter/X thread for a creator with {CREATOR_CONTEXT['followers']} followers.

TOPIC: {topic_data['topic']}
AFFILIATE TO FEATURE: {topic_data['affiliate']} — use placeholder {CREATOR_CONTEXT['affiliate_links'][topic_data['affiliate']]}
STYLE: {topic_data['style']}
CTA GOAL: {topic_data['cta']}
TONE: {CREATOR_CONTEXT['tone']}

THREAD RULES:
- Tweet 1: HOOK — bold claim or number that stops scrolling. Under 200 chars.
- Tweets 2-6: one insight per tweet, specific and actionable
- Tweet 7: the affiliate mention — natural, story-based, not salesy
- Tweet 8: CTA — "Follow for more" + what they'll get
- Each tweet numbered: 1/ 2/ 3/ etc.
- No hashtags (they kill reach in 2026)
- No "I hope this helps" or generic closings
- Write like a real person, not a content creator

Write the complete thread now."""

    return call_claude(prompt, 1000)


def write_viral_tweets():
    prompt = f"""Write 5 standalone viral tweets for a creator in the AI/passive income niche.
Followers: {CREATOR_CONTEXT['followers']}
Tone: {CREATOR_CONTEXT['tone']}

One tweet per angle:
1. {VIRAL_TWEET_ANGLES[0]}
2. {VIRAL_TWEET_ANGLES[1]}
3. {VIRAL_TWEET_ANGLES[2]}
4. {VIRAL_TWEET_ANGLES[3]}
5. {VIRAL_TWEET_ANGLES[4]}

Rules:
- Each under 240 characters
- No hashtags
- Must make someone stop scrolling
- Real and specific, not generic
- Format: Tweet 1: [text] (newline) Tweet 2: [text] etc."""

    return call_claude(prompt, 600)


def write_income_transparency_post():
    prompt = f"""Write an "income transparency" post for X/Twitter.

This creator is building AI passive income agents and has {CREATOR_CONTEXT['followers']} followers.
It's Saturday March 14, 2026. They've been building for a few weeks.

Write a raw, honest update post that:
- Shares a specific real number (can be small — authenticity > hype)
- Mentions what's working and what failed
- Invites engagement with a question at the end
- Subtly shows they're available for UGC work
- Under 280 characters OR a 3-tweet mini-thread if needed

This post builds trust which = more followers, more clients, more sales.
Write it now — raw and real."""

    return call_claude(prompt, 400)


def write_posting_strategy():
    prompt = f"""Create a 7-day X/Twitter posting schedule for someone with {CREATOR_CONTEXT['followers']} followers
in the AI/passive income niche. Goal: maximize affiliate clicks and UGC client inquiries.

Include:
- Best posting times (EST)
- Content type per day
- Which affiliate to feature each day
- How to use replies to drive affiliate clicks without being spammy
- How to turn engagement into UGC client leads

Keep it practical — this person posts from their phone."""

    return call_claude(prompt, 500)


# ── MAIN ─────────────────────────────────────────────────
print("=" * 60)
print("  TWITTER/X CONTENT ENGINE")
print(f"  {datetime.now().strftime('%m/%d/%Y %H:%M')}")
print(f"  Audience: {CREATOR_CONTEXT['followers']} followers")
print("=" * 60)

os.makedirs("twitter", exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M")

# 1. Tweet threads
print("\n[1/4] Writing tweet threads...")
all_threads = []
for t in THREAD_TOPICS:
    print(f"  Thread: {t['topic'][:50]}...")
    thread = write_thread(t)
    all_threads.append(f"TOPIC: {t['topic']}\nAFFILIATE: {t['affiliate']}\n{'='*55}\n{thread}\n\n")

with open(f"twitter/TWEET_THREADS_{timestamp}.txt", "w") as f:
    f.write("READY-TO-POST TWEET THREADS\n")
    f.write("Replace [AFFILIATE_LINK] with your real link before posting\n")
    f.write("=" * 60 + "\n\n")
    f.write("\n".join(all_threads))
print("  ✅ Saved tweet threads")

# 2. Viral tweets
print("\n[2/4] Writing viral standalone tweets...")
viral = write_viral_tweets()
with open(f"twitter/VIRAL_TWEETS_{timestamp}.txt", "w") as f:
    f.write("VIRAL STANDALONE TWEETS\n")
    f.write("Post 1-2 of these per day between threads\n")
    f.write("=" * 60 + "\n\n")
    f.write(viral)
print("  ✅ Saved viral tweets")

# 3. Income transparency
print("\n[3/4] Writing income transparency post...")
transparency = write_income_transparency_post()
with open(f"twitter/INCOME_TRANSPARENCY_{timestamp}.txt", "w") as f:
    f.write("INCOME TRANSPARENCY POST\n")
    f.write("Post this today — builds massive trust with audience\n")
    f.write("=" * 60 + "\n\n")
    f.write(transparency)
print("  ✅ Saved transparency post")

# 4. Posting strategy
print("\n[4/4] Building 7-day posting strategy...")
strategy = write_posting_strategy()
with open("twitter/7_DAY_POSTING_STRATEGY.txt", "w") as f:
    f.write("7-DAY X/TWITTER STRATEGY\n")
    f.write("=" * 60 + "\n\n")
    f.write(strategy)
print("  ✅ Saved posting strategy")

print("\n" + "=" * 60)
print("DONE. Check twitter/ folder for all content.")
print("\nPOST ORDER FOR TODAY:")
print("  1. Income transparency post (builds trust)")
print("  2. First viral tweet (30 min later)")
print("  3. First thread (2 hours later)")
print("\nREMEMBER: Replace all [AFFILIATE_LINK] placeholders")
print("with your real affiliate URLs before posting")
print("=" * 60)
