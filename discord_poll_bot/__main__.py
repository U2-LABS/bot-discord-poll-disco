import os

import discord
from discord.ext import commands

from .bot_config import settings, state

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.messages = True
intents.reactions = True
intents.presences = True

bot = commands.Bot(command_prefix=settings['prefix'], intents=intents, owner_id=settings['owner_id'])

import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

import random



@bot.command()
async def hello(ctx):
    author = ctx.message.author
    await ctx.send(
        f'Hello, {author.mention}!')

for file in os.listdir("discord_poll_bot/cogs"):
    if file.endswith(".py") and not file.startswith("_"):
        name = file[:-3]
        bot.load_extension(f"discord_poll_bot.cogs.{name}")


if __name__ == "__main__":
    with state:
        try:
            bot.run(settings['token'])
        except Exception as e:
            print(f'Error when logging in: {e}')
