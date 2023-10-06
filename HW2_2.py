# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 16:01:30 2023

@author: June
"""

import requests
from bs4 import BeautifulSoup

def is_press(page):
    name_tags = page.find_all(class_ = 'ep_name')
    
    for tag in name_tags:
        if "Plenary session" in tag.get_text():
            return True

    return False

def target(seed_url, key, max_res):
    press_release = []
    seen_urls = set()
    queue = [seed_url]

    while queue and len(press_release) < max_res:
        url = queue.pop(0)

        if url in seen_urls:
            #print('Already Seen')
            continue
        else:
            seen_urls.add(url)

        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            if is_press(soup) and key.lower() in soup.get_text().lower():
                press_release.append(url)

            links = soup.find_all('a', href = True)
            
            for link in links:
                absolute_url = link['href']
                
                if absolute_url.startswith(seed_url):
                    queue.append(absolute_url)

    return press_release

if __name__ == "__main__":
    seed_url = "https://www.europarl.europa.eu/news/en/press-room"
    key = "crisis"
    max_res = 15

    press_release = target(seed_url, key, max_res)

    if len(press_release) >= max_res:
        for i, url in enumerate(press_release):
            print(f"{i+1} is {url}")
    else:
        print("Insufficient plenary session press releases")

