import asyncio

import discord
from discord.ext import base
from discord.ext.base import runner


class Bot(base.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="balls ",
            intents=discord.Intents(
                guild_messages=True,
                guild_reactions=True,
                guilds=True,
                members=True,
                message_content=True,
                messages=True,
                reactions=True,
            ),
        )

    async def setup_hook(self):
        if self.user:
            print(self.user.name)


if __name__ == "__main__":
    bot = Bot()

    asyncio.run(runner.run(bot))
