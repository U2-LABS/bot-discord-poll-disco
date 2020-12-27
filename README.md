# bot-discord-poll-disco
___
## Start 
1. Install all requirements from txt file
```sh
$ pip3 install -r requirements.txt
```
2. Create _.env_ file in main directory
```sh
$ touch .env
```
3. Run bot
```sh
$ python3 -m discord_poll_bot
```

## List of commands

### Commands for all users
- __/help__ - to call the bot help 
- __/top__ [num] - returns the top of the _num_ of songs
- __/vote__ [num] - adds voice to song under number _num_
        `if you vote for first time your vote will be add, else your vote will be removed`

### Commands only for admins

- __/disco__ - start music-poll
- __/poptop__ [num] - takes a song from the top at number _num_ and unloads its title or mp3, depending on the settings. If you enter _/poptop_ without num you will get song #1
- __/finish__ - finish music-poll
- __/setting_mp3 on|off__ - changes the upload of the song to the chat. If _setting_mp3 on_ you will get mp3 file in the chat. If _setting_mp3 off_ you will get only title and author for top song
- __/poll_status__ - print settings of bot
- __/setDJ__ @[username] - give **DJ** role for user

## Environment variables

```sh
BOT_TOKEN = "Discord Token"
CONFIG_PATH = "configs/"
DEFAULT_JSON = "${CONFIG_PATH}default_config.json"
SAVED_JSON = "${CONFIG_PATH}saved_config.json"
MUSIC_FILE = "music.csv"
USER_DB = "postgres"
PASSWORD_DB = "postgres"
HOST_DB = "localhost"
PORT_DB = 5432
NAME_DB = "music_db"
```
__BOT_TOKEN__  - Your token for using bot in discord. 
:warning:`Don't add your token in repository`

__CONFIG_PATH__ - Path to your directory where you storage your config jsons files *.json.

__DEFAULT_JSON__ - Name of json file, that will be loaded when bot start for first time.

__SAVED_JSON__ - Name of json file, that will be created and then bot will loaded from this file, when the music-poll finish.

__MUSIC_FILE__ - Name of the *.csv file that contains song in format belong

__USER_DB__ - Login for connect to the database (PostgreSQL)

__PASSWORD_DB__ - Password need for connect to the database (PostgreSQL)

__HOST_DB__ - IP_Address to the PostgreSQL database that stores information about songs

__PORT_DB__ - Port to the PostgreSQL database

__NAME_DB__ - Name of the PostgreSQL database

| title | author | link |
| :---: | :---: | :---: |
| ... | ... | ... |
