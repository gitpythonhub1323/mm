import feedparser
from datetime import datetime

feeds = [
    "https://rss.sme.sk/rss/rss.asp?sek=sme",
    "https://dennikn.sk/feed/",
    "https://www.aktuality.sk/rss/"
]

entries = []

for url in feeds:
    feed = feedparser.parse(url)
    entries.extend(feed.entries)

def get_date(e):
    return e.get("published_parsed") or datetime.now().timetuple()

entries.sort(key=get_date, reverse=True)

rss_items = ""
for e in entries[:30]:
    rss_items += f"""
    <item>
        <title>{e.title}</title>
        <link>{e.link}</link>
    </item>
    """

rss = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
<title>Moje správy</title>
<description>SME + Denník N + Aktuality</description>
<link>https://github.com/</link>
{rss_items}
</channel>
</rss>
"""

with open("feed.xml", "w", encoding="utf-8") as f:
    f.write(rss)
