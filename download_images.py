import urllib.request
import re
import os
import json
import uuid
import time

def get_unsplash_ids(query, count):
    url = f"https://unsplash.com/napi/search/photos?query={query}&per_page={count}&page=1"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode('utf-8'))
        return [result['id'] for result in data['results']]
    except Exception as e:
        print(f"Error fetching {query}: {e}")
        return []

print("Fetching IDs...")
car_ids = get_unsplash_ids('car', 30)
driving_ids = get_unsplash_ids('driving', 20)
city_ids = get_unsplash_ids('city', 20)
road_ids = get_unsplash_ids('road', 15)
travel_ids = get_unsplash_ids('vacation', 15)

all_ids = list(set(car_ids + driving_ids + city_ids + road_ids + travel_ids))
print(f"Total unique IDs fetched: {len(all_ids)}")

if not os.path.exists('assets/images'):
    os.makedirs('assets/images')

files = [f for f in os.listdir('.') if f.endswith('.html')]

# We need to replace all `<img src="...">` and `background-image: url(...)` and `src="..."` that point to unsplash.
# Wait, let's just replace all occurrences of `https://images.unsplash.com/...` with a local asset.

id_index = 0

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all Unsplash URLs
    matches = re.findall(r'(https://images\.unsplash\.com/[^\s\"\'\>]+)', content)
    
    for match in matches:
        if id_index >= len(all_ids):
            print("Ran out of unique IDs!")
            break
            
        current_id = all_ids[id_index]
        id_index += 1
        
        # Download the new image
        local_filename = f"assets/images/img_{current_id}.jpg"
        
        # Determine size from original URL to download appropriate size
        # Or just download a standard high-res size
        download_url = f"https://images.unsplash.com/photo-{current_id}?q=80&w=1000&auto=format&fit=crop"
        
        if not os.path.exists(local_filename):
            try:
                print(f"Downloading {download_url} to {local_filename}")
                req = urllib.request.Request(download_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as response, open(local_filename, 'wb') as out_file:
                    out_file.write(response.read())
                time.sleep(0.5) # Be nice to Unsplash
            except Exception as e:
                print(f"Failed to download {current_id}: {e}")
                continue
                
        # Replace only ONE occurrence (since we want unique images everywhere)
        content = content.replace(match, local_filename, 1)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Done replacing and downloading images!")
