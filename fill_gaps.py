import os
import re
import urllib.request
import json
import time

# Get remaining Wiki URLs
print("Fetching extra images from Wikimedia Commons...")
extra_urls = []
queries = ['sports car', 'luxury vehicle', 'SUV']
for q in queries:
    url = f"https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch={urllib.parse.quote(q)}&gsrnamespace=6&gsrlimit=50&prop=imageinfo&iiprop=url&format=json"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    try:
        data = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
        urls = [p['imageinfo'][0]['url'] for p in data['query']['pages'].values() if 'imageinfo' in p]
        extra_urls.extend(urls)
    except Exception as e:
        print(f"Failed wiki fetch for {q}: {e}")
        
# Sort so we get stable results, or reverse so we don't hit the ones that failed
extra_urls = extra_urls[::-1] 

files = [f for f in os.listdir('.') if f.endswith('.html')]

extra_url_index = 0
image_counter = 60

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find remaining Unsplash URLs
    matches = re.findall(r'(https://images\.unsplash\.com/[^\s\"\'\>]+)', content)
    
    for match in matches:
        if extra_url_index >= len(extra_urls):
            print("Ran out of extra URLs!")
            break
            
        download_url = extra_urls[extra_url_index]
        extra_url_index += 1
        
        local_filename = f"assets/images/img_{image_counter}.jpg"

        # Download the image
        if not os.path.exists(local_filename):
            try:
                print(f"Downloading {download_url} to {local_filename}")
                req = urllib.request.Request(download_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
                with urllib.request.urlopen(req) as response, open(local_filename, 'wb') as out_file:
                    out_file.write(response.read())
                time.sleep(2) # Avoid 429
            except Exception as e:
                print(f"Failed to download {download_url}: {e}")
                continue
                
        # Replace only ONE occurrence
        content = content.replace(match, local_filename, 1)
        image_counter += 1

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Done filling gaps. Replaced {image_counter - 60} images.")
