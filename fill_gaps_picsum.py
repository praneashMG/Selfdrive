import os
import re
import urllib.request
import time

files = [f for f in os.listdir('.') if f.endswith('.html')]

image_counter = 60

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find remaining Unsplash URLs
    matches = re.findall(r'(https://images\.unsplash\.com/[^\s\"\'\>]+)', content)
    
    for match in matches:
        local_filename = f"assets/images/img_{image_counter}.jpg"

        # Download from picsum using a known ID to guarantee uniqueness and no 429
        # Picsum IDs go from 1 to 1000+
        download_url = f"https://picsum.photos/id/{image_counter + 100}/800/600"
        
        if not os.path.exists(local_filename):
            try:
                print(f"Downloading {download_url} to {local_filename}")
                req = urllib.request.Request(download_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as response, open(local_filename, 'wb') as out_file:
                    out_file.write(response.read())
            except Exception as e:
                print(f"Failed to download {download_url}: {e}")
                continue
                
        # Replace only ONE occurrence
        content = content.replace(match, local_filename, 1)
        image_counter += 1

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Done filling gaps. Replaced {image_counter - 60} images.")
