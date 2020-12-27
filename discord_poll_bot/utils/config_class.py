import json
import os

from discord_poll_bot.songs import Song
from discord_poll_bot.utils.marsh_schemas import StateSchema
from discord_poll_bot.utils.work_with_csv import get_music_csv, create_csv


class State:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(State, cls).__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self, path_to_config=None, path_to_save_config=None):
        self.schema = StateSchema()
        self.filename = os.getenv("MUSIC_FILE")
        self.path_to_config, self.path_to_save_config = self.get_config_path(path_to_config, path_to_save_config)
        self.config = self.loads_config()

    def loads_config(self):
        with open(self.path_to_config) as r_file:
            json_data = json.load(r_file)
            config = self.schema.load(json_data)

        if Song.select().count() == 0:
            create_csv(self.filename, config["count_music"])
            for song in self.get_songs():
                Song.create(
                    title=song.get('title'),
                    link=song.get('link'),
                    author=song.get('author'),
                    voted_users=[]
                )

        for idx in range(Song.select().count()):
            Song.update(pos=idx + 1).where(Song.id_music == idx + 1).execute()
        return config

    def get_songs(self):
        return get_music_csv(self.filename)

    def save_config(self):
        with open(self.path_to_save_config, 'w') as w_file:
            json_data = self.schema.dump(self.config)
            json.dump(json_data, w_file, indent=4)

    @staticmethod
    def get_config_path(path_to_config, path_to_save_config):
        if not path_to_config:
            path_to_config = (
                os.getenv("SAVED_JSON")
                if os.path.exists(os.getenv("SAVED_JSON"))
                else os.getenv("DEFAULT_JSON")
            )
        if not path_to_save_config:
            path_to_save_config = os.getenv("SAVED_JSON")
        return path_to_config, path_to_save_config

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        self.save_config()
