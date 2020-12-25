def create_top(songs):
    top_list = sorted(songs, key=lambda song: song["mark"], reverse=True)
    return top_list


def _download_music_link(music_link, name):
    import requests
    ok_status_code = 200
    link = music_link
    req = requests.get(link, stream=True)
    if req.status_code == ok_status_code:
        with open(name, 'wb') as mp3:
            mp3.write(req.content)


def upload_song(song, ctx):
    song_name = f'{song["author"]} - {song["title"]}.mp3'
    _download_music_link(song["link"], song_name)
    return song_name
