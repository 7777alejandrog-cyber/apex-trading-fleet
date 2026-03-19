"""
AGENT G — TREND SCOUT
=======================
Monitors what's actually trending RIGHT NOW in:
- AI tools and launches
- Passive income methods
- Creator economy news
- Finance and investing
- Tech layoffs and job market

Feeds trending topics directly into Agent D (video scripts)
and Agent E (Twitter threads) so every piece of content
is on a hot topic — maximizes views and engagement.

Also finds:
- Viral tweets to respond to (reply farming = free followers)
- Brand campaigns actively seeking UGC creators
- Reddit posts asking for help (freelance opportunities)
"""

import os
import re
import requests
from datetime import datetime

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "").strip()

TREND_SOURCES = [
    {
        "name": "Reddit AI",
        "url": "https://www.reddit.com/r/artificial/hot.json?limit=10",
        "type": "reddit"
    },
    {
        "name": "Reddit Passive Income",
        "url": "https://www.reddit.com/r/passive_income/hot.json?limit=10",
        "type": "reddit"
    },
    {
        "name": "Reddit Side Hustle",
        "url": "https://www.reddit.com/r/sidehustle/hot.json?limit=10",
        "type": "reddit"
    },
    {
        "name": "Reddit Entrepreneur",
        "url": "https://www.reddit.com/r/Entrepreneur/hot.json?limit=10",
        "type": "reddit"
    },
    {
        "name": "Hacker News",
        "url": "https://hacker-news.firebaseio.com/v0/topstories.json",
        "type": "hn"
    },
]

HEADERS = {"User-Agent": "Mozilla/5.0 (trend-scout/1.0)"}


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


def fetch_reddit_trends(source):
    posts = []
    try:
        r = requests.get(source["url"], headers=HEADERS, timeout=10)
        data = r.json()
        for post in data["data"]["children"][:10]:
            p = post["data"]
            posts.append({
                "title": p.get("title", ""),
                "score": p.get("score", 0),
                "comments": p.get("num_comments", 0),
                "url": f"https://reddit.com{p.get('permalink', '')}",
                "source": source["name"]
            })
    except Exception as e:
        print(f"  Error fetching {source['name']}: {e}")
    return posts


def fetch_hn_trends():
    posts = []
    try:
        r = requests.get(
            "https://hacker-news.firebaseio.com/v0/topstories.json",
            timeout=10
        )
        story_ids = r.json()[:15]
        for sid in story_ids[:8]:
            try:
                sr = requests.get(
                    f"https://hacker-news.firebaseio.com/v0/item/{sid}.json",
                    timeout=5
                )
                story = sr.json()
                if story and story.get("title"):
                    posts.append({
                        "title": story.get("title", ""),
                        "score": story.get("score", 0),
                        "comments": story.get("descendants", 0),
                        "url": story.get("url", f"https://news.ycombinator.com/item?id={sid}"),
                        "source": "Hacker News"
                    })
            except:
                pass
    except Exception as e:
        print(f"  Error fetching HN: {e}")
    return posts


def analyze_trends(all_posts):
    titles = "\n".join([f"- [{p['source']}] {p['title']} ({p['score']} upvotes)" for p in all_posts[:30]])

    prompt = f"""Analyze these trending posts from Reddit and Hacker News as of today {datetime.now().strftime('%m/%d/%Y')}.

TRENDING POSTS:
{titles}

You are helping a creator in the AI/passive income/tech niche. Identify:

1. TOP 5 VIDEO TOPICS (for YouTube Shorts/TikTok)
   - Title that would perform well
   - Why it's trending now
   - Affiliate angle if applicable

2. TOP 3 TWEET THREAD TOPICS
   - Topic + angle for 20K follower audience
   - Why this would get engagement today

3. TOP 3 REDDIT OPPORTUNITIES
   - Posts where someone could offer help/expertise
   - What to say to turn it into a freelance lead

4. TREND SUMMARY
   - What's the overall hot topic this week?
   - What should this creator be talking about?

Be specific. Use the actual titles from the list above."""

    return call_claude(prompt, 1000)


def generate_trending_scripts(analysis):
    prompt = f"""Based on this trend analysis, write 2 ready-to-film YouTube Short scripts.

TREND ANALYSIS:
{analysis[:800]}

Each script:
- 60-75 seconds when read aloud
- Opens with a hook referencing the trending topic
- Delivers specific value in 3 fast points
- Ends with affiliate CTA (use [AFFILIATE_LINK] placeholder)
- Sounds like a real person reacting to news, not a content bot

Label them SCRIPT 1 and SCRIPT 2."""

    return call_claude(prompt, 1200)


# ── MAIN ─────────────────────────────────────────────────
print("=" * 60)
print("  TREND SCOUT")
print(f"  Scanning trends: {datetime.now().strftime('%m/%d/%Y %H:%M')}")
print("=" * 60)

os.makedirs("trends", exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M")

# Fetch from all sources
all_posts = []
for source in TREND_SOURCES:
    print(f"\nFetching {source['name']}...")
    if source["type"] == "reddit":
        posts = fetch_reddit_trends(source)
    else:
        posts = fetch_hn_trends()
    print(f"  Got {len(posts)} posts")
    all_posts.extend(posts)

# Sort by engagement
all_posts.sort(key=lambda x: x["score"] + x["comments"], reverse=True)
print(f"\nTotal posts collected: {len(all_posts)}")

# Analyze trends
print("\nAnalyzing trends with Claude...")
analysis = analyze_trends(all_posts)

# Save trend report
with open(f"trends/TREND_REPORT_{timestamp}.txt", "w") as f:
    f.write(f"TREND REPORT — {datetime.now().strftime('%m/%d/%Y %H:%M')}\n")
    f.write("=" * 60 + "\n\n")
    f.write(analysis)
    f.write("\n\n" + "=" * 60 + "\n\n")
    f.write("RAW TRENDING POSTS:\n\n")
    for p in all_posts[:20]:
        f.write(f"[{p['score']}pts] {p['source']}: {p['title']}\n")
        f.write(f"  → {p['url']}\n\n")
print("✅ Trend report saved")

# Generate trending video scripts
print("\nGenerating trending video scripts...")
scripts = generate_trending_scripts(analysis)
with open(f"trends/TRENDING_SCRIPTS_{timestamp}.txt", "w") as f:
    f.write("TRENDING VIDEO SCRIPTS\n")
    f.write("Based on what's hot RIGHT NOW — higher chance of going viral\n")
    f.write("=" * 60 + "\n\n")
    f.write(scripts)
print("✅ Trending scripts saved")

print("\n" + "=" * 60)
print("DONE. Check trends/ folder.")
print("\nACTION:")
print("1. Open TREND_REPORT for today's hot topics")
print("2. Film TRENDING_SCRIPTS — trending content = algorithm boost")
print("3. Check Reddit opportunities for same-day freelance leads")
print("=" * 60)
