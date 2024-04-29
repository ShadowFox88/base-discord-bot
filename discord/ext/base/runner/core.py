import asyncio
import contextlib
import traceback

import discord

from ..configuration import CONFIGURATION

__all__ = ("run",)


async def run(bot: discord.Client, *, with_token: str = CONFIGURATION.TOKEN):
    try:
        with contextlib.suppress(asyncio.CancelledError, KeyboardInterrupt):
            await bot.start(with_token)
    except Exception as error:
        traceback.print_exception(type(error), error, error.__traceback__)
    finally:
        await bot.close()
