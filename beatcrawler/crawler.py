import requests
import asyncio
import itertools
import csv
from bs4 import BeautifulSoup

async def _run_async_request(url):
    loop = asyncio.get_event_loop()
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    future = loop.run_in_executor(None, requests.get, url, headers)
    return await future


async def _get_song_id(url):
    response = await _run_async_request(url)
    soup = BeautifulSoup(response.content, features="html.parser")
    all_song_img_tags = soup.find_all('img', {'style': 'width: 46px; height: 46px;'})
    id_tags = [tag['src'].split(r"/")[-1].split(r".")[0] for tag in all_song_img_tags]
    return id_tags

async def _process_multiple_page_ids(url, page_max):
    all_url_pages = [url+f"&page={page}&sort=1" for page in range(1, page_max + 1)]
    response = asyncio.gather(*[_get_song_id(page) for page in all_url_pages])
    return await response

async def _get_beatsaver_download_urls(song_id):
    beatsaver_url = f'https://beatsaver.com/search?q={song_id}'
    response = await _run_async_request(beatsaver_url)
    soup =  BeautifulSoup(response.content, features="html.parser")
    li_key_tag = soup.find_all('li', {'style': 'font-size: 1rem'})[0] #this key is the first tag
    key = li_key_tag.split(' ')[0]#the key follows like this: "d771 🔑"
    beatsaver_download_url = f'https://beatsaver.com/cdn/{key}/{song_id}.zip'#the url follows this format
    return beatsaver_download_url

async def _process_beatsaver_download_urls(song_ids):
    response = asyncio.gather(*[_get_beatsaver_download_urls(song_id) for song_id in song_ids])
    return await response

def get_all_download_urls(song_ids):
    loop=asyncio.get_event_loop()
    page_ids = loop.run_until_complete(_process_beatsaver_download_urls(song_ids))
    return list(itertools.chain(*page_ids))    


def get_all_page_ids(url, page_max):
    loop=asyncio.get_event_loop()
    page_ids = loop.run_until_complete(_process_multiple_page_ids(url, page_max))
    return list(itertools.chain(*page_ids))

def write_song_ids_to_file(user_id, save_path, max_pages=1):
    scoresaber_url = f'https://scoresaber.com/u/{user_id}'
    page_ids = get_all_page_ids(scoresaber_url, max_pages)
    with open(save_path, "w") as f:
        for page_id in page_ids:
            f.write(page_id + "\n")