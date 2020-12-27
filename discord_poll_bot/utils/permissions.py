from discord.ext import commands

from discord_poll_bot.bot_settings import settings, state


class PollDoNotStarted(commands.CheckFailure):
    pass


def is_owner(ctx):
    """ Checks if the author is one of the owners """
    return ctx.author.id == settings["owner_id"]


def poll_is_started(ctx):
    if state.config["poll_started"]:
        return True
    raise PollDoNotStarted


def is_guild(ctx):
    return ctx.guild is not None
