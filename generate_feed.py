import feedparser
from datetime import datetime
import html

# 🔎 ZDROJE
FEEDS = {
    "SME": "https://rss.sme.sk/rss/rss.asp?sek=sme",
    "DennikN": "https://dennikn.sk/feed/",
    "Aktuality": "https://www.aktuality.sk/rss/",
    "TASR": "https://www.teraz.sk/rss/vsetky-spravy.rss",
    "Pravda": "https://spravy.pravda.sk/rss/xml/"
}

# ✅ POVOLENÉ ZDROJE (môžeš upraviť)
ALLOWED_SOURCES = ["SME", "DennikN", "Aktuality", "TASR", "Pravda"]

# 🔎 KĽÚČOVÉ SLOVÁ (filter kategórií)
KEYWORDS = [
    "ekonomika", "ai", "technológie", "slovensko", "konsolidácia", "dane", "sociálne veci"
]

# ❌ BLOKOVANÉ SLOVÁ
EXCLUDE = [
    "šport", "bulvár", "celebrity"
]

entries = []

for source, url in FEEDS.items():
    if source not in ALLOWED_SOURCES:
        continue

    feed = feedparser.parse(url)

    for e in feed.entries:
        title = e.get("title", "")
        summary = e.get("summary", "")

        text = (title + " " + summary).lower()

        # filter include
        if not any(k in text for k in KEYWORDS):
            continue

        # filter exclude
        if any(x in text for x in EXCLUDE):
            continue

        entries.append({
            "title": title,
            "link": e.get("link", "#"),
            "summary": summary,
            "source": source,
            "date": e.get("published_parsed") or datetime.now().timetuple()
        })

# zoradenie
entries.sort(key=lambda x: x["date"], reverse=True)

# RSS položky
rss_items = ""
for e in entries[:40]:
    title = html.escape(e["title"])
    link = e["link"]
    desc = html.escape(e["summary"])
    source = e["source"]

    rss_items += f"""
    <item>
        <title>[{source}] {title}</title>
        <link>{link}</link>
        <description>{desc}</description>
    </item>
    """

rss = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
<title>Filtrované správy</title>
<description>Len relevantné správy (AI, politika, ekonomika)</description>
<link>https://github.com</link>
{rss_items}
</channel>
</rss>
"""

with open("feed.xml", "w", encoding="utf-8") as f:
    f.write(rss)
