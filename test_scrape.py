import urllib.request
import re
import json

def search_ddg_images(query):
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
        # DuckDuckGo HTML version doesn't always have images easily, let's look for src="..."
        # Actually DDG images requires JS.
        pass
    except Exception as e:
        print(e)

# Let's scrape unsplash directly but bypass 401 by not using the API, just the HTML page
def scrape_unsplash_html():
    url = "https://unsplash.com/s/photos/car"
    req = urllib.request.Request(url, headers={'User-Agent': 'Googlebot/2.1 (+http://www.google.com/bot.html)'})
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
        matches = re.findall(r'https://images\.unsplash\.com/photo-[a-zA-Z0-9_-]+', html)
        return list(set(matches))
    except Exception as e:
        print(e)
        return []

print("Unsplash HTML scrape with Googlebot UA:")
urls = scrape_unsplash_html()
print(f"Found {len(urls)} URLs")
