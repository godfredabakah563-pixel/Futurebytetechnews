import feedparser, json, os, requests
from bs4 import BeautifulSoup

FEED_URL = "https://feeds.bbci.co.uk/news/technology/rss.xml"
PUBLIC_DIR = "public"
IMG_DIR = os.path.join(PUBLIC_DIR, "images")

os.makedirs(IMG_DIR, exist_ok=True)

feed = feedparser.parse(FEED_URL)
articles = []

for entry in feed.entries[:10]:
    title = entry.title
    link = entry.link
    description = entry.get("summary", "")
    image = None
    try:
        html = requests.get(link, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")
        img_tag = soup.find("img")
        if img_tag and img_tag.get("src"):
            img_url = img_tag["src"]
            if img_url.startswith("//"):
                img_url = "https:" + img_url
            img_name = os.path.basename(img_url.split("?")[0])
            img_path = os.path.join(IMG_DIR, img_name)
            with open(img_path, "wb") as f:
                f.write(requests.get(img_url, timeout=10).content)
            image = "images/" + img_name
    except Exception as e:
        print("Error fetching image:", e)
    articles.append({
        "title": title,
        "link": link,
        "description": description,
        "image": image or "https://ichef.bbci.co.uk/news/1024/branded_news/17E63/production/_128612315_bbc_news_logo.png"
    })

with open(os.path.join(PUBLIC_DIR, "articles.json"), "w") as f:
    json.dump({"articles": articles}, f, indent=2)

print("Fetched", len(articles), "BBC tech articles.")
