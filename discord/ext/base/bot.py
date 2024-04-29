# pyright: reportIncompatibleMethodOverride=false
from __future__ import annotations

import pkgutil
import traceback
import typing

from discord.ext.commands.bot import PrefixType

import discord
from discord.ext import commands

from .configuration import CONFIGURATION

__all__ = ("Bot",)


class Bot(commands.Bot):
    async def on_extension_error(self, extension: str, error: commands.ExtensionError):
        traceback_ = "".join(traceback.format_exception(type(error), error, error.__traceback__))

        print(f"An error occurred when loading {extension}:\n\n{traceback_}", end="\n\n")

    async def on_extension_load(self, extension: str):
        print(f"Successfully loaded {extension}", end="\n\n")

    async def load_extension(self, name: str, *, package: str | None = None):
        try:
            await self.load_extension(name, package=package)
        except commands.ExtensionError as error:
            await self.on_extension_error(name, error)
        else:
            await self.on_extension_load(name)

    async def load_default_extensions(self):
        if CONFIGURATION.JISHKAU:
            await self.load_extension("jishaku")

        if not CONFIGURATION.EXTENSIONS_FOLDER:
            return

        extension_folder_path = CONFIGURATION.EXTENSIONS_FOLDER.replace(".", "/")

        for module_info in pkgutil.walk_packages([extension_folder_path], prefix=f"{CONFIGURATION.EXTENSIONS_FOLDER}."):
            module_path = module_info.name

            await self.load_extension(module_path)

    def __init_subclass__(cls):
        real_setup_hook = cls.setup_hook

        async def setup_hook(self: typing.Self):
            await self.load_default_extensions()
            await real_setup_hook(self)

        cls.setup_hook = setup_hook

        return super().__init_subclass__()

    def __init__(
        self,
        *,
        command_prefix: PrefixType[typing.Self] = discord.utils.MISSING,
        help_command: commands.HelpCommand | None = None,
        **kwargs: typing.Any,
    ):
        command_prefix = command_prefix if command_prefix is not discord.utils.MISSING else CONFIGURATION.PREFIX

        super().__init__(command_prefix=command_prefix, help_command=help_command, **kwargs)
