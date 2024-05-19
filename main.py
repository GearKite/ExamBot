import logging
import os
from os import environ as env

import discord
from discord.ext import commands
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG, force=True)
try:
    import coloredlogs  # type: ignore

    coloredlogs.install()
except ImportError:
    pass

load_dotenv()

intents = discord.Intents.default()

bot = commands.Bot(command_prefix=".", intents=intents, owner_id=env["OWNER_ID"])


@bot.event
async def on_ready():
    logging.info("We have logged in as %s", bot.user)


@bot.event
async def setup_hook():
    for cog in os.listdir("cogs"):
        if not cog.endswith(".py"):
            continue
        logging.debug("Loading cog %s", cog)

        await bot.load_extension(f"cogs.{cog[:-3]}")
        logging.info("Done loading %s", cog)

    await bot.tree.sync()
    await bot.tree.sync(guild=discord.Object(env["DEV_GUILD_ID"]))


bot.run(env["TOKEN"])
