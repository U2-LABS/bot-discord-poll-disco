import csv

import requests
from bs4 import BeautifulSoup as BS

ZAYCEV_URL = r'https://zaycev.net'


def create_csv(file_name, amount):
    """This is function create csv file from ZAYCEV.NET
    ```
    title, author, link
    ```
    ```py
    create_csv("music.csv")
    ```
    Args:
        file_name (str): Path to csv file
        amount (str): amount of songs
    """
    songs = []

    response = requests.get(ZAYCEV_URL)
    soup = BS(response.content, 'html.parser')

    all_top_songs = soup.find_all(class_='musicset-track__download-link')

    for song_a in all_top_songs[:amount]:
        song = {}
        song['author'], song['title'] = song_a.get('title').split(' ', 2)[-1].split(' – ', 1)
        song['link'] = ZAYCEV_URL + song_a.get('href')
        if song["author"] and song["title"] and song["link"]:
            songs.append(song)

    with open(file_name, mode="w", encoding='utf-8') as w_file:
        names = ["title", "author", "link"]
        csv_writer = csv.DictWriter(w_file, delimiter=',', lineterminator='\r', fieldnames=names)
        csv_writer.writeheader()
        for song in songs:
            csv_writer.writerow(song)


def get_music_csv(file_name):
    """This is function return a list that contain song
    ```py
    get_music_csv("music.csv")
    ```
    Args:
        file_name (str): Path to csv file
    Returns:
        list[dict]: List with list of music with ```title, author, link```
    """
    songs = []
    with open(file_name, encoding='utf-8') as r_file:
        csv_reader = csv.DictReader(r_file, delimiter=',')
        for idx, song in enumerate(csv_reader):
            song['mark'] = 0
            song['pos'] = idx + 1
            song['voted_users'] = []
            songs.append(song)
    return sorted(songs, key=lambda song: song["author"])
