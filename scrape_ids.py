import urllib.request
import re

queries = ['car', 'driving', 'vacation', 'city-street', 'luxury-car', 'road-trip']
all_ids = set()

for q in queries:
    url = f'https://unsplash.com/s/photos/{q}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
        # Look for the slug or photo IDs in the react state or just the page
        # Unsplash HTML changed recently, it might use different keys
        # Let's just look for "images.unsplash.com/photo-{id}"
        matches = re.findall(r'https://images\.unsplash\.com/photo-([a-zA-Z0-9_-]+)', html)
        for m in matches:
            all_ids.add(m)
        print(f"Found {len(matches)} matches for {q}")
    except Exception as e:
        print(f"Failed to fetch {q}: {e}")

all_ids = list(all_ids)
print(f"Total unique IDs: {len(all_ids)}")

with open('ids.txt', 'w') as f:
    for i in all_ids:
        f.write(i + '\n')
