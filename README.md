# Exam Bot

is a Discord bot that helps you study for math and english exams by giving you questions and problems.

[Add to your Discord guild](https://discord.com/oauth2/authorize?client_id=1240727602986225825&permissions=137439235136&scope=bot)

## Installation

### Prerequisites

- `Python >= 3.11`
- [Python Poetry](https://python-poetry.org/docs/)

### Install dependencies

`$ poetry install`

### Configure

1. Copy `.env.example` to `.env`
1. Edit `.env` and add the required values
1. Optionally, edit `config.toml` to add your own questions and personalize the bot
1. Optionally, add a profile picture picture to your bot (`./assets/profile_picture.png`)

### Run it!

- Activate your virtual environment

  1. `$ poetry shell`

  and start the bot

  2. `$ python main.py`

- Or, without spawning a new shell:

  1. `$ poetry run python main.py`

## Usage

### Commands

`/quiz {subject}`  
Starts a 10 question quiz

`/multiple_choice {subject}`  
Gives a single multiple choice question

`/quote`  
Provides an inspirational quote

`/help`  
Usage information (kind of like this ^^)

`/reload {cog}`  
Reloads a given Discord.py cog (only available in dev server to bot owner)
