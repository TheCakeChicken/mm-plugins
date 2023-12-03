import asyncio
import copy
from datetime import datetime

import discord
from discord.channel import CategoryChannel
from discord.ext import commands

from core import checks
from core.models import DummyMessage, PermissionLevel


class Deleter(commands.Cog):
    """Channel name changer for Whitehill. (by @prpldev)"""
    def __init__(self, bot):
        self.bot = bot
        self.db = self.bot.plugin_db.get_partition(self)

    def user_resp(self, channel, member, *, timeout=15):
        return self.bot.wait_for('message', check=lambda m: getattr(m.channel, 'recipient', m.channel) == channel and m.author == member, timeout=timeout)

    @commands.Cog.listener()
    async def on_thread_reply(thread, from_mod, message, anonymous, plain):
        """Waits for delete messages to be sent"""
        if not message.author.bot: return
        if not 'User ID: ' in thread.topic: return
        if 'It seems this problem has been solved.' in plain:
            thread.edit(name="scheduled-close")
        elif 'Scheduled close has been cancelled.' in plain:
            firstsplit = thread.topic.split(':')[-1]
            id = firstsplit.split(' ')[-1]
            user = bot.fetch_user(id)
            thread.edit(name=user.username+"-"+user.discriminator)

async def setup(bot):
    await bot.add_cog(Deleter(bot))
