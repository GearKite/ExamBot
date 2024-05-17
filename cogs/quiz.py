import random
import tomllib
from os import environ as env

import discord
from discord.app_commands import command
from discord.ext import commands

with open("assets/questions.toml", "rb") as f:
    questions = tomllib.load(f)


class Quiz(commands.Cog):
    """Single question mode"""

    def __init__(self, bot):
        self.bot = bot


async def setup(bot: commands.Bot):
    await bot.add_cog(Quiz(bot), guilds=[discord.Object(env["DEV_GUILD_ID"])])
