import os
import re
import urllib.request
import json
import time

if not os.path.exists('assets/images'):
    os.makedirs('assets/images')

print("Fetching extra images from Wikimedia Commons...")
extra_urls = []
queries = ['sports car', 'luxury vehicle', 'SUV']
for q in queries:
    url = f"https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch={urllib.parse.quote(q)}&gsrnamespace=6&gsrlimit=50&prop=imageinfo&iiprop=url&format=json"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        data = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
        urls = [p['imageinfo'][0]['url'] for p in data['query']['pages'].values() if 'imageinfo' in p]
        extra_urls.extend(urls)
    except Exception as e:
        print(f"Failed wiki fetch for {q}: {e}")

print(f"Fetched {len(extra_urls)} extra image URLs.")

files = [f for f in os.listdir('.') if f.endswith('.html')]

# We want to replace ALL image URLs in the HTML files with a unique local image.
# An image URL is considered anything starting with https://images.unsplash.com/...
# We will track which Unsplash URLs we have already downloaded. If we see it again, we use an extra_url instead!

used_unsplash_urls = set()
extra_url_index = 0
image_counter = 1

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all Unsplash URLs
    matches = re.findall(r'(https://images\.unsplash\.com/[^\s\"\'\>]+)', content)
    
    for match in matches:
        local_filename = f"assets/images/img_{image_counter}.jpg"
        
        # Decide which URL to download
        if match not in used_unsplash_urls:
            download_url = match
            used_unsplash_urls.add(match)
        else:
            if extra_url_index < len(extra_urls):
                download_url = extra_urls[extra_url_index]
                extra_url_index += 1
            else:
                print("Ran out of extra URLs!")
                continue

        # Download the image
        if not os.path.exists(local_filename):
            try:
                print(f"Downloading {download_url} to {local_filename}")
                req = urllib.request.Request(download_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as response, open(local_filename, 'wb') as out_file:
                    out_file.write(response.read())
            except Exception as e:
                print(f"Failed to download {download_url}: {e}")
                continue
                
        # Replace only ONE occurrence (since we want unique images everywhere)
        content = content.replace(match, local_filename, 1)
        image_counter += 1

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Done! Downloaded and replaced {image_counter - 1} images.")
