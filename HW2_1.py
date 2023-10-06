# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 14:38:54 2023

@author: June
"""

from bs4 import BeautifulSoup
import urllib
import requests


def is_press(tag):
    return tag.name == 'a' and tag.has_attr('href') and tag['href'] == '/en/press-release'

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

            if any(is_press(tag) for tag in soup.find_all(is_press)):
                
                if key.lower() in soup.get_text().lower():
                    press_release.append(url)

            for link in soup.find_all('a', href = True):
                absolute_url = urllib.parse.urljoin(seed_url, link['href'])
                
                if absolute_url.startswith(seed_url):
                    queue.append(absolute_url)

    return press_release


if __name__ == "__main__":
    seed_url = "https://press.un.org/en"
    key = "crisis"
    max_res = 15

    press_release = target(seed_url, key, max_res)

    if len(press_release) >= max_res:
        for i, url in enumerate(press_release):
            print(f"{i + 1} is {url}")
    else:
        print("Insufficient press releases")

    print('Change Made')
