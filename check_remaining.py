import os
import re

files = [f for f in os.listdir('.') if f.endswith('.html')]
urls = 0
for f in files:
    content = open(f, encoding='utf-8').read()
    found = re.findall(r'https://images\.unsplash\.com/[^\s\"\'\>]+', content)
    urls += len(found)
    if len(found) > 0:
        print(f"{f}: {len(found)} left")
print(f'Remaining Unsplash URLs: {urls}')
