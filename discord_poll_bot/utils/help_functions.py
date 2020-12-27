from playhouse.shortcuts import model_to_dict

from discord_poll_bot.songs import Song


def create_top(state):
    top_list = Song.select().order_by(Song.mark.desc(), Song.pos)
    for song in top_list:
        state.config["top_songs"].append(model_to_dict(song))


def _download_music_link(music_link, name):
    import requests
    ok_status_code = 200
    link = music_link
    req = requests.get(link, stream=True)
    if req.status_code == ok_status_code:
        with open(name, 'wb') as mp3:
            mp3.write(req.content)


def upload_song(song, ctx):
    song_name = f'{song["author"]} - {song["title"]}.mp3'.replace('/', '|')
    _download_music_link(song["link"], song_name)
    return song_name
