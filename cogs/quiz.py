import enum
import random
import tomllib
import typing
from datetime import datetime
from os import environ as env

import discord
from discord.app_commands import command
from discord.ext import commands

with open("config.toml", "rb") as f:
    config = tomllib.load(f)
    questions: dict[list[dict]] = config["questions"]
    color: dict = config["color"]
    r: dict = config["strings"]
    quiz_length: int = config["quiz"]["lenght"]

# 'questions' keys are the available subjects, make an ENUM out of them for Discord autocomplete
Subjects = enum.Enum("Subjects", " ".join(questions.keys()).title())


class Quiz(commands.Cog):
    """Single question mode"""

    def __init__(self, bot):
        self.bot = bot

    @command(
        name="quiz",
        description="Starts a 10 multiple choice question quiz.",
    )
    async def quiz_command(self, interaction: discord.Interaction, subject: Subjects):
        """Quiz with 10 questions."""
        await start_quiz(
            interaction=interaction, subject=subject, question_amount=10, results=True
        )

    @command(
        name="multiple_choice",
        description="Asks a single multiple choice question.",
    )
    async def multiple_choice_command(
        self, interaction: discord.Interaction, subject: Subjects
    ):
        """Single multiple choice question"""
        await start_quiz(
            interaction=interaction, subject=subject, question_amount=1, results=False
        )


async def start_quiz(
    interaction: discord.Interaction,
    subject: Subjects,
    question_amount: int,
    results: bool,
):
    questions_left = random.sample(questions[subject.name.lower()], question_amount)

    total_correct = 0

    async def send_results():
        embed = discord.Embed(
            title=r["quiz_complete_embed_title"], color=color["quiz_complete"]
        )

        embed.add_field(name="Punkti", value=f"**{total_correct}/{quiz_length}**")

        embed.set_footer(text=interaction.user.name)
        embed.timestamp = datetime.now()

        await interaction.followup.send(embed=embed)

    async def on_answer(answered_correctly: bool):
        if answered_correctly:
            nonlocal total_correct
            total_correct += 1

        await send_new_question()

    async def send_new_question():
        # Send results if we don't have any more questions
        if len(questions_left) == 0 and results:
            await send_results()
            return

        question = questions_left[0]

        question_text = question["question"]
        answer = str(question["answer"])
        incorrect_options = question["incorrect_options"]

        # Add 3 random incorrect options and 1 correct option
        random.shuffle(incorrect_options)
        options = incorrect_options[:3] + [answer]
        random.shuffle(options)

        embed = discord.Embed(title=f"❓{question_text}", color=color["waiting"])

        view = QuizQuestionView(
            question=question,
            answer=answer,
            options=options,
            callback=on_answer,
            results=results,
        )

        # Send first question as response, next questions as followups
        if len(questions_left) == question_amount:
            await interaction.response.send_message(
                embed=embed,
                view=view,
            )
        else:
            await interaction.followup.send(embed=embed, view=view)

        questions_left.pop(0)

    await send_new_question()


class QuizQuestionAnswerButton(discord.ui.Button):
    def __init__(
        self,
        label: str,
        question: dict,
        is_correct: bool,
        callback: typing.Coroutine,
    ):
        super().__init__(label=label, style=discord.ButtonStyle.secondary)
        self.is_correct = is_correct
        self.question = question
        self.answered_callback = callback

    async def callback(self, interaction: discord.Interaction):
        view: QuizQuestionView = self.view

        # Ignore button presses for already answered questions
        if view.answered and view.results:
            await interaction.response.send_message(
                r["question_already_answered_error"], ephemeral=True
            )
            return
        view.answered = True

        if self.is_correct:
            self.style = discord.ButtonStyle.success
            for child in view.children:
                if isinstance(child, QuizQuestionAnswerButton) and not child.is_correct:
                    child.disabled = True

            embed = discord.Embed(
                title=f":white_check_mark: {self.question['question']}",
                color=color["correct"],
            )
        else:
            self.style = discord.ButtonStyle.danger
            self.disabled = True

            if view.results:
                for child in view.children:
                    if isinstance(child, QuizQuestionAnswerButton):
                        if child.is_correct:
                            # Color the correct answer green
                            child.style = discord.ButtonStyle.success
                        else:
                            # Disable all incorrect answer buttons
                            child.disabled = True

            embed = discord.Embed(
                title=f":x: {self.question['question']}", color=color["incorrect"]
            )

        embed.add_field(name=r["explanation_label"], value=self.question["explanation"])
        embed.set_footer(text=interaction.user.name)
        embed.timestamp = datetime.now()

        await interaction.response.edit_message(embed=embed, view=view)

        await self.answered_callback(self.is_correct)


class QuizQuestionView(discord.ui.View):
    def __init__(
        self,
        question: dict,
        answer: str,
        options: list,
        callback: typing.Coroutine,
        results: bool,
    ):
        super().__init__(timeout=600)

        self.answered = False
        self.results = results

        for option in options:
            self.add_item(
                QuizQuestionAnswerButton(
                    label=option,
                    question=question,
                    is_correct=(option == answer),
                    callback=callback,
                )
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Quiz(bot), guilds=[discord.Object(env["DEV_GUILD_ID"])])
