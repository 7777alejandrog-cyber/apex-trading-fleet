"""
AGENT F — DIGITAL PRODUCT GENERATOR
======================================
Creates a complete, sellable digital product using Claude.

PRODUCT: "The AI Income Playbook: How I Built a Passive Income
          System With AI Agents in 30 Days"

Sells on Gumroad for $17-27. Zero cost to produce. Pure profit.
One sale per day = $500+/month completely passive.

THIS AGENT WRITES THE ENTIRE EBOOK:
- Introduction + your story
- 7 chapters covering each income stream
- Real strategies, not generic advice
- Action steps at end of each chapter
- Formatted as clean markdown (easy to convert to PDF)
"""

import os
import requests
from datetime import datetime

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "").strip()

BOOK_CONFIG = {
    "title": "The AI Income Playbook",
    "subtitle": "How to Build a Passive Income System With AI Agents",
    "author": "A",
    "price_point": "$17",
    "target_reader": "people who want to make money with AI but don't know where to start",
    "unique_angle": "built by someone actually doing it, not a guru — real systems, real mistakes, real numbers",
    "chapters": [
        {
            "num": 1,
            "title": "Why AI Changes Everything About Making Money Online",
            "focus": "The opportunity window, why now is different, what most people miss"
        },
        {
            "num": 2,
            "title": "The 5 Income Streams I built with automation Agents",
            "focus": "Overview of UGC, freelance, content, affiliate, trading — honest about what works fastest"
        },
        {
            "num": 3,
            "title": "UGC Creation: Getting Paid $150-500 Per Video With No Followers",
            "focus": "Full UGC playbook — platforms, pitching, filming, pricing"
        },
        {
            "num": 4,
            "title": "The Freelance Automation Stack: Letting AI Find and Win Jobs",
            "focus": "How to use AI to scan job boards, write proposals, win clients"
        },
        {
            "num": 5,
            "title": "Building a Faceless Content Machine",
            "focus": "YouTube Shorts + affiliate marketing system, tools, realistic timeline"
        },
        {
            "num": 6,
            "title": "GitHub Actions: Running Income Agents 24/7 For Free",
            "focus": "The technical setup explained simply — anyone can do this"
        },
        {
            "num": 7,
            "title": "Your 30-Day Launch Plan",
            "focus": "Day by day action steps, realistic income milestones, what to do first"
        },
    ]
}


def call_claude(prompt, max_tokens=1500):
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
            timeout=60,
        )
        return r.json()["content"][0]["text"]
    except Exception as e:
        return f"API error: {e}"


def write_intro():
    prompt = f"""Write the introduction for a digital ebook called "{BOOK_CONFIG['title']}".

Target reader: {BOOK_CONFIG['target_reader']}
Unique angle: {BOOK_CONFIG['unique_angle']}
Tone: Honest, direct, like a friend who figured something out and is sharing it

The intro should:
- Open with a specific moment or realization (not generic)
- Explain what AI income actually is (cut through the hype)
- Be honest about the timeline (weeks/months, not overnight)
- Preview the 7 systems covered in the book
- End with a promise of what they'll have after reading
- About 400 words

Write in first person. No fluff. Real talk."""

    return call_claude(prompt)


def write_chapter(chapter):
    prompt = f"""Write Chapter {chapter['num']} of "{BOOK_CONFIG['title']}".

Chapter title: {chapter['title']}
Core focus: {chapter['focus']}

Author context: Someone who actually built these systems, not a guru.
Writing style: Direct, specific, honest about what works and what doesn't.
Target reader: {BOOK_CONFIG['target_reader']}

Structure this chapter with:
- Opening hook (specific story or stat)
- Main content (practical, step by step where relevant)
- At least 2 specific examples or real numbers
- One honest "mistake I made" or "what doesn't work"
- Action steps at the end (3-5 specific things to do)
- About 600-800 words

Write in markdown format with ## subheadings.
First person voice. No fluff. Real strategies only."""

    return call_claude(prompt, 1500)


def write_conclusion():
    prompt = f"""Write the conclusion for "{BOOK_CONFIG['title']}".

This should:
- Remind reader of the full system they now have
- Be honest: this takes work, but it's worth it
- Give a final motivating push
- Tell them exactly what to do in the next 24 hours
- End with something memorable
- About 300 words

Real talk, no hype."""

    return call_claude(prompt, 600)


def write_gumroad_listing():
    prompt = f"""Write a Gumroad product listing for this ebook:

Title: {BOOK_CONFIG['title']}
Subtitle: {BOOK_CONFIG['subtitle']}
Price: {BOOK_CONFIG['price_point']}
Target reader: {BOOK_CONFIG['target_reader']}

Write:
1. PRODUCT DESCRIPTION (200 words) — what's inside, who it's for
2. BULLET POINTS (6 bullets) — specific things they'll learn
3. SHORT PITCH (50 words) — for sharing on social media
4. PREVIEW HOOK (first paragraph to show as free preview)

Make it convert. Specific over vague. Real over hyped."""

    return call_claude(prompt, 700)


# ── MAIN ─────────────────────────────────────────────────
print("=" * 60)
print("  DIGITAL PRODUCT GENERATOR")
print(f"  Writing: {BOOK_CONFIG['title']}")
print(f"  {datetime.now().strftime('%m/%d/%Y %H:%M')}")
print("=" * 60)

os.makedirs("ebook", exist_ok=True)
ebook_content = []

# Header
ebook_content.append(f"# {BOOK_CONFIG['title']}")
ebook_content.append(f"## {BOOK_CONFIG['subtitle']}")
ebook_content.append(f"\n*By {BOOK_CONFIG['author']}*\n")
ebook_content.append("---\n")

# Introduction
print("\n[1/9] Writing introduction...")
intro = write_intro()
ebook_content.append("# Introduction\n")
ebook_content.append(intro)
ebook_content.append("\n---\n")
print("  ✅ Introduction done")

# Chapters
for i, chapter in enumerate(BOOK_CONFIG['chapters']):
    print(f"\n[{i+2}/9] Writing Chapter {chapter['num']}: {chapter['title'][:45]}...")
    content = write_chapter(chapter)
    ebook_content.append(f"# Chapter {chapter['num']}: {chapter['title']}\n")
    ebook_content.append(content)
    ebook_content.append("\n---\n")
    print(f"  ✅ Chapter {chapter['num']} done")

# Conclusion
print("\n[9/9] Writing conclusion...")
conclusion = write_conclusion()
ebook_content.append("# Conclusion\n")
ebook_content.append(conclusion)
print("  ✅ Conclusion done")

# Save ebook
ebook_text = "\n\n".join(ebook_content)
with open("ebook/AI_INCOME_PLAYBOOK.md", "w") as f:
    f.write(ebook_text)
print("\n✅ Ebook saved: ebook/AI_INCOME_PLAYBOOK.md")

# Gumroad listing
print("\nWriting Gumroad listing...")
listing = write_gumroad_listing()
with open("ebook/GUMROAD_LISTING.txt", "w") as f:
    f.write("GUMROAD PRODUCT LISTING\n")
    f.write("Upload ebook as PDF, use this text for the listing\n")
    f.write("=" * 60 + "\n\n")
    f.write(listing)
    f.write("\n\n" + "=" * 60)
    f.write(f"\nSELL AT: gumroad.com — create free account, upload PDF")
    f.write(f"\nSUGGESTED PRICE: {BOOK_CONFIG['price_point']}")
    f.write(f"\nESTIMATED MONTHLY: $500-2,000 (1-4 sales/day with promotion)")
print("✅ Gumroad listing saved: ebook/GUMROAD_LISTING.txt")

print("\n" + "=" * 60)
print("EBOOK COMPLETE.")
print("\nNEXT STEPS:")
print("1. Download AI_INCOME_PLAYBOOK.md from artifacts")
print("2. Paste into Notion or Google Docs")
print("3. Export as PDF")
print("4. Upload to gumroad.com (free account)")
print("5. Set price at $17, post link on X today")
print("6. Every sale = $17 pure profit, zero cost")
print(f"\nAt 1 sale/day: $510/month")
print(f"At 3 sales/day: $1,530/month")
print(f"At 10 sales/day: $5,100/month")
print("=" * 60)
