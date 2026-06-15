import feedparser
from datetime import datetime
import html

FEEDS = {
    "SME": "https://rss.sme.sk/rss/rss.asp?sek=sme",
    "DennikN": "https://dennikn.sk/feed/",
    "Aktuality": "https://www.aktuality.sk/rss/",
    "TASR": "https://www.teraz.sk/rss/vsetky-spravy.rss",
    "Pravda": "https://spravy.pravda.sk/rss/xml/"
}

ALLOWED_SOURCES = ["SME", "DennikN", "Aktuality", "TASR", "Pravda"]

KEYWORDS = [
    "ekonomika", "ai", "technológie", "slovensko", "konsolidácia", "dane", "sociálne veci"
]

EXCLUDE = ["šport", "bulvár", "celebrity"]

entries = []

for source, url in FEEDS.items():

    if source not in ALLOWED_SOURCES:
        continue

    try:
        feed = feedparser.parse(url)

        if not feed or not hasattr(feed, "entries"):
            continue

    except Exception as e:
        print("FEED ERROR:", source, url, e)
        continue

    for e in feed.entries:

        title = (e.get("title") or "")
        summary = (e.get("summary") or "")

        text = (title + " " + summary).lower()

        if not any(k in text for k in KEYWORDS):
            continue

        if any(x in text for x in EXCLUDE):
            continue

        entries.append({
            "title": title,
            "link": e.get("link", "#"),
            "summary": summary,
            "source": source,
            "date": e.get("published_parsed") or datetime.now().timetuple()
        })

entries.sort(key=lambda x: x["date"], reverse=True)

rss_items = ""

for e in entries[:40]:
    rss_items += f"""
    <item>
        <title>[{e['source']}] {html.escape(e['title'])}</title>
        <link>{e['link']}</link>
        <description>{html.escape(e['summary'])}</description>
    </item>
    """

rss = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
<title>Filtrované správy</title>
<description>AI + ekonomika + Slovensko správy</description>
<link>https://github.com</link>
{rss_items}
</channel>
</rss>
"""

with open("feed.xml", "w", encoding="utf-8") as f:
    f.write(rss)

print("RSS generated:", len(entries), "items")
