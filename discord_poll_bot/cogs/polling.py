import os

import discord
from discord.ext import commands
from peewee import fn

from discord_poll_bot.bot_settings import state
from discord_poll_bot.utils.songs import Song
from discord_poll_bot.utils import permissions
from discord_poll_bot.utils.help_functions import create_top, upload_song


class Polling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot was connected.')

    @commands.command(name='help_poll')
    async def get_help(self, ctx):
        help_message = (
            "**Admin commands**\n"
            "/disco to start poll\n"
            "/poptop [num] output referenced song (e.g. /poptop or /poptop 5)\n"
            "/finish to end poll\n"
            "/setDJ [mentioned user] set mentioned people a DJ (e.g. /setDJ @Admin)\n"
            "/settings_mp3 on|off (e.g. /settings_mp3 or /settings_mp3 on)\n"
            "/poll_status to print status of poll in this chat\n"
            "**User commands**\n"
            "/top [num] output top songs(e.g. /top 5)\n"
            "/vote [num] vote for song from poll (e.g. /vote 5)\n"
        )

        embed_message = discord.Embed(
            title="Help commands",
            description=help_message,
            colour=discord.Colour.dark_blue()
        )

        await ctx.send(embed=embed_message)

    @commands.command(name='disco')
    @commands.check(permissions.is_owner)
    async def create_poll(self, ctx):
        if state.config["poll_started"]:
            await ctx.send("Previous poll hasn't finished yet. Type /finish or use pined Message")
        else:
            state.config["poll_started"] = True

            try:
                state.config["chat_id"] = ctx.guild.id
            except AttributeError:
                pass

            music_poll = ''
            for idx, song in enumerate(Song.select().execute()):
                music_poll += f'{idx + 1}. {song.author} | {song.title}\n'

            poll_embed = discord.Embed(
                title="Songs",
                description=music_poll,
                colour=discord.Colour.gold()
            )

            await ctx.send(embed=poll_embed)

    @commands.command(name='top')
    @commands.check(permissions.poll_is_started)
    async def get_songs_top_list(self, ctx, amount: int = 5):
        state.config["top_songs"].clear()
        create_top(state)
        music_poll = ''
        for idx, song in enumerate(state.config["top_songs"][:amount]):
            music_poll += f'{idx + 1}. {song["author"]} | {song["title"]} | {song["mark"]} Votes\n'
        await ctx.send(music_poll)

    @commands.command(name='vote')
    @commands.check(permissions.poll_is_started)
    async def vote_for_song(self, ctx, song_position: int):
        if 0 >= song_position or song_position > state.config["count_music"]:
            reply_message = f'Number should be less than {state.config["count_music"]} and greater than 0'
            await ctx.send(reply_message)
        else:
            idx = song_position
            if (author_id := str(ctx.message.author.id)) not in Song.get_by_id(idx).voted_users:
                song_item = Song.get_by_id(idx)
                song_item.update(mark=song_item.mark + 1) \
                    .where(Song.id_music == song_item.id_music) \
                    .execute()
                song_item.update(voted_users=fn.array_append(Song.voted_users, author_id)) \
                    .where(Song.id_music == song_item.id_music) \
                    .execute()
            else:
                song_item = Song.get_by_id(idx)
                song_item.update(mark=song_item.mark - 1) \
                    .where(Song.id_music == song_item.id_music) \
                    .execute()
                song_item.update(voted_users=fn.array_remove(Song.voted_users, author_id)) \
                    .where(Song.id_music == song_item.id_music) \
                    .execute()

    @commands.command(name='poptop')
    @commands.check(permissions.is_owner)
    @commands.check(permissions.poll_is_started)
    async def pop_element_from_top(self, ctx, song_position: int = None):
        if song_position is not None and (0 >= song_position or song_position > state.config["count_music"]):
            reply_message = f'Number should be less than {state.config["count_music"]} and greater than 0'
            await ctx.send(reply_message)
        else:
            idx = 0 if song_position is None else song_position - 1
            if not state.config["top_songs"]:
                create_top(state)
            song_item = state.config["top_songs"][idx]
            if state.config["upload_flag"]:
                song_file = upload_song(song_item, ctx)
                await ctx.send(file=discord.File(song_file))
                os.remove(song_file)
            else:
                bot_reply_message = f'{song_item["author"]} | {song_item["title"]}'
                await ctx.send(bot_reply_message)

            song_index = song_item["pos"]
            song_item = Song.get_by_id(song_index)
            Song.update(voted_users=[]) \
                .where(Song.id_music == song_item.id_music) \
                .execute()
            Song.update(mark=0) \
                .where(Song.id_music == song_item.id_music) \
                .execute()
            state.config["top_songs"] = []

    @commands.command(name='finish')
    @commands.check(permissions.is_owner)
    @commands.check(permissions.poll_is_started)
    async def finish_poll(self, ctx):
        state.config["poll_started"] = False
        Song.truncate_table(restart_identity=True)
        state.save_config()
        state.__init__()
        await ctx.send("Poll was finished")

    @finish_poll.error
    async def finish_poll_error(self, ctx, error):
        if isinstance(error, permissions.PollDoNotStarted):
            await ctx.send("Poll hasn't started yet. Type /disco to start")

    @commands.command(name='settings_mp3')
    @commands.check(permissions.is_owner)
    async def change_upload_flag(self, ctx, toggle: str = None):
        if toggle is None:
            state.config["upload_flag"] = False if state.config["upload_flag"] else True
        else:
            if toggle == 'on':
                state.config["upload_flag"] = True
            elif toggle == 'off':
                state.config["upload_flag"] = False
        bot_message = f'uploading songs is **{"Enabled" if state.config["upload_flag"] else "Disabled"}**'
        await ctx.send(bot_message)

    @commands.command(name='poll_status')
    @commands.check(permissions.is_owner)
    async def get_poll_status(self, ctx):
        status = (
            'Poll status\n'
            '———————————\n'
            f'Poll started: {state.config["poll_started"]}\n'
            f'Upload mp3: {"on" if state.config["upload_flag"] else "off"}'
        )
        await ctx.send(status)

    @commands.command(name='setDJ')
    @commands.check(permissions.is_owner)
    @commands.check(permissions.is_guild)
    async def set_dj_by_user_id(self, ctx, member: discord.Member):
        dj_role = discord.utils.get(ctx.guild.roles, name="DJ")
        await member.add_roles(dj_role)

    @set_dj_by_user_id.error
    async def set_dj_by_user_id_error(self, ctx, error):
        await ctx.send(error)


def setup(bot):
    bot.add_cog(Polling(bot))
