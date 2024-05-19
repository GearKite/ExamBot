import tomllib
from os import environ as env

import aiohttp
import discord
from discord.app_commands import command
from discord.ext import commands

with open("config.toml", "rb") as f:
    config = tomllib.load(f)
    quotes: dict = config["quotes"]
    color: dict = config["color"]


class Quotes(commands.Cog):
    """Single question mode"""

    def __init__(self, bot):
        self.bot = bot

    @command(name="quote", description="Gives you an inspirational quote.")
    async def quote_command(self, interaction: discord.Interaction):
        quote = await self.get_quote()

        if len(quote) > 255:
            embed = discord.Embed(
                description=f"**{quote['quote']}**", color=color["quiz_complete"]
            )
        else:
            embed = discord.Embed(title=quote["quote"], color=color["quiz_complete"])

        embed.set_footer(text=quote["author"])
        await interaction.response.send_message(embed=embed)

    async def get_quote(self) -> dict:
        if not env["QUOTES_API_KEY"]:
            raise NoAPIKeyError(
                "No API key was provided. This is expected if you left QUOTES_API_KEY blank."
            )

        async with aiohttp.ClientSession() as session:
            async with session.get(
                quotes["api"], headers={"X-Api-Key": env["QUOTES_API_KEY"]}
            ) as resp:
                if resp.status != 200:
                    raise CouldntGetQuoteError(f"{resp.status} - {resp.text}")
                return (await resp.json())[0]


async def setup(bot: commands.Bot):
    await bot.add_cog(Quotes(bot))


class CouldntGetQuoteError(Exception):
    """Couldn't fetch a quote from the API"""


class NoAPIKeyError(Exception):
    "No API key was provided"
