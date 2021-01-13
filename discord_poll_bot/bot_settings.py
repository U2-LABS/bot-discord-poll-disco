import os

from dotenv import load_dotenv

from discord_poll_bot.utils.config_class import State

load_dotenv()

settings = {
    "token": os.getenv("BOT_TOKEN"),
    'id': 790873108130693130,
    'owner_id': 319534891329126401,
    'prefix': '/'
}

state = State()
