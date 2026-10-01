import os
import re

files = [f for f in os.listdir('.') if f.endswith('.html')]
urls = []
for f in files:
    content = open(f, encoding='utf-8').read()
    found = re.findall(r'src=\"(https://images\.unsplash\.com/[^\"]+)\"', content)
    for u in found:
        urls.append((f, u))

print(f"Total occurrences: {len(urls)}")
unique_urls = set([u[1] for u in urls])
print(f"Unique URLs: {len(unique_urls)}")

# Check for repetitions
counts = {}
for f, u in urls:
    counts[u] = counts.get(u, 0) + 1

for u, c in counts.items():
    if c > 1:
        print(f"Repeated {c} times: {u}")
