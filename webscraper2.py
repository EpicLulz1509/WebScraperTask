import requests
import csv
from bs4 import BeautifulSoup
import time

query = "site:youtube.com openinapp.co"
num_results = 100
results = []
num_pages = (num_results - 1) // 10 + 1
headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
    }

for page in range(num_pages):
    start = page * 10
    url = f"https://www.google.com/search?q={query}&start={start}"
    
    response = requests.get(url, headers=headers)
    time.sleep(2) 
    response.raise_for_status()
    html = response.text

    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a")
    youtube_links = []
    for link in links:
        href = link.get("href")
        if href and "youtube.com" in href:
            if "maps.google.com" not in href:
                youtube_links.append(href)

    results.extend(youtube_links)
    if len(results) >= num_results:
        break

links = results[:num_results]

with open("youtube_links.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows([[link] for link in links])

print(f"Total links scraped: {len(links)}")
print("Links saved to links.csv")
