import importlib
import os
import sys
import time

import discord
from discord.ext import commands

from discord_poll_bot.utils import permissions


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    @commands.command()
    @commands.check(permissions.is_owner)
    async def reload(self, ctx, name: str):
        """ Reloads an extension. """
        try:
            self.bot.reload_extension(name)
        except Exception as e:
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send(f"Reloaded extension **{name}.py**")

    @commands.command(name="reloadall")
    @commands.check(permissions.is_owner)
    async def reload_all(self, ctx):
        """ Reloads all extensions. """
        for file in os.listdir("discord_poll_bot/cogs"):
            if file.endswith(".py") and not file.startswith("_"):
                name = file[:-3]
                try:
                    self.bot.reload_extension(f"discord_poll_bot.cogs.{name}")
                except Exception as e:
                    await ctx.send('{}: {}'.format(type(e).__name__, e))
                else:
                    await ctx.send('\N{OK HAND SIGN}')
                    await ctx.send(f"Reloaded extension **{name}.py**")

        await ctx.send("Successfully reloaded all extensions")

    @commands.command()
    @commands.check(permissions.is_owner)
    async def reboot(self, ctx):
        """ Reboot the bot """
        await ctx.send('Rebooting now...')
        time.sleep(1)
        sys.exit(0)

    @commands.command()
    @commands.check(permissions.is_owner)
    async def dm(self, ctx, user_id: int, *, message: str):
        """ DM the user of your choice """
        user = self.bot.get_user(user_id)
        if not user:
            return await ctx.send(f"Could not find any UserID matching **{user_id}**")

        try:
            await user.send(message)
            await ctx.send(f"✉️ Sent a DM to **{user_id}**")
        except discord.Forbidden:
            await ctx.send("This user might be having DMs blocked or it's a bot account...")

    @commands.command(name="reloadutils")
    @commands.check(permissions.is_owner)
    async def reload_utils(self, ctx, name: str):
        """ Reloads a utils module. """
        name_maker = f"discord_poll_bot/utils/{name}.py"
        try:
            module_name = importlib.import_module(f"discord_poll_bot.utils.{name}")
            importlib.reload(module_name)
        except ModuleNotFoundError:
            await ctx.send(f"Couldn't find module named **{name_maker}**")
        except Exception as e:
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send(f"Reloaded utils module **{name_maker}**")


def setup(bot):
    bot.add_cog(Admin(bot))
