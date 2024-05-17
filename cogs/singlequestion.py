import random
import tomllib
from os import environ as env

import discord
from discord.app_commands import command
from discord.ext import commands

with open("assets/questions.toml", "rb") as f:
    toml = tomllib.load(f)
    questions: list[dict] = toml["question"]
    color: dict = toml["color"]


class SingleQuestion(commands.Cog):
    """Single question mode"""

    def __init__(self, bot):
        self.bot = bot

    @command(
        name="multiple_choice",
        description="Gives you a multiple choice question with answer options.",
    )
    async def multiple_choice(self, interaction: discord.Interaction):
        """Multiple choice question with answer options"""
        question = random.choice(questions)
        question_text = question["question"]
        answer = str(question["answer"])
        incorrect_options = question["incorrect_options"]

        # Add 3 random incorrect options and 1 correct option
        random.shuffle(incorrect_options)
        options = incorrect_options[:3] + [answer]
        random.shuffle(options)

        # Define the Button class
        class QuizButton(discord.ui.Button):
            def __init__(self, label: str, is_correct: bool):
                super().__init__(label=label, style=discord.ButtonStyle.secondary)
                self.is_correct = is_correct

            async def callback(self, interaction: discord.Interaction):
                view: QuizView = self.view
                if self.is_correct:
                    self.style = discord.ButtonStyle.success
                    for child in view.children:
                        if isinstance(child, QuizButton) and not child.is_correct:
                            child.disabled = True
                    embed = discord.Embed(
                        title=f"❓{question_text}", color=color["correct"]
                    )
                else:
                    self.style = discord.ButtonStyle.danger
                    self.disabled = True
                    embed = discord.Embed(
                        title=f"❓{question_text}", color=color["incorrect"]
                    )
                await interaction.response.edit_message(embed=embed, view=view)

        # Define the View containing the Buttons
        class QuizView(discord.ui.View):
            def __init__(self):
                super().__init__()
                for option in options:
                    self.add_item(
                        QuizButton(label=option, is_correct=(option == answer))
                    )

        embed = discord.Embed(title=f"❓{question_text}", color=color["waiting"])

        await interaction.response.send_message(embed=embed, view=QuizView())


async def setup(bot: commands.Bot):
    await bot.add_cog(SingleQuestion(bot), guilds=[discord.Object(env["DEV_GUILD_ID"])])
