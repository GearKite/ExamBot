from os import environ as env

import discord
from discord import app_commands
from discord.ext import commands


class Management(commands.Cog):
    """Management commands for the bot"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="reload", description="Reloads a specified cog.")
    async def reload(
        self,
        interaction: discord.Interaction,
        cog: str,
        sync_commands: bool = False,
    ):
        """Reloads a specified cog."""
        if (
            str(interaction.user.id) != self.bot.owner_id
        ):  # Only the bot owner can use this command
            await interaction.response.send_message(
                "You do not have permission to use this command.", ephemeral=True
            )
            return

        try:
            await self.bot.reload_extension(f"cogs.{cog}")

            if sync_commands:
                await self.bot.tree.sync(guild=discord.Object(env["DEV_GUILD_ID"]))

            await interaction.response.send_message(
                f"`{cog}` has been reloaded successfully.", ephemeral=True
            )
        except commands.ExtensionNotLoaded:
            await interaction.response.send_message(
                f"`{cog}` is not loaded.", ephemeral=True
            )
        except commands.ExtensionNotFound:
            await interaction.response.send_message(
                f"`{cog}` does not exist.", ephemeral=True
            )
        except commands.NoEntryPointError:
            await interaction.response.send_message(
                f"`{cog}` does not have a setup function.", ephemeral=True
            )
        except commands.ExtensionFailed as e:
            await interaction.response.send_message(
                f"`{cog}` failed to reload.\n{type(e).__name__}: {e}", ephemeral=True
            )
        except Exception as e:  # pylint: disable=broad-exception-caught
            await interaction.response.send_message(
                f"An error occurred: {type(e).__name__}: {e}", ephemeral=True
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Management(bot), guilds=[discord.Object(env["DEV_GUILD_ID"])])
