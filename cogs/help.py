import tomllib

import discord
from discord.app_commands import command
from discord.ext import commands

with open("config.toml", "rb") as f:
    config = tomllib.load(f)
    questions: dict[list[dict]] = config["questions"]
    color: dict = config["color"]
    quiz_length: int = config["quiz"]["lenght"]


class Help(commands.Cog):
    """Single question mode"""

    def __init__(self, bot):
        self.bot = bot

    @command(name="help", description="Provides basic usage information.")
    async def help_command(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Usage", color=color["waiting"])

        embed.add_field(
            name="Quizzes",
            value=f"Want to try a {quiz_length} question quiz? Use `/quiz [subject]` ",
            inline=False,
        )

        embed.add_field(
            name="Multiple choice questions",
            value="""Or if you just want to get a single multiple choice question.
            Use `/multiple_choice [subject]`""",
            inline=False,
        )

        embed.add_field(
            name="Inspiration",
            value="""Get inspired by various people using `/quote`""",
            inline=False,
        )

        embed.add_field(
            name="Available subjects",
            value=f"""You can choose between the following subjects:
            {'; '.join(questions.keys()).title()}""",
            inline=False,
        )

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))
