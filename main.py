# Discord
import discord
from discord.ext import commands

# OS
import os
# Dotenv
from dotenv import load_dotenv

# Commands
from commands import bot
# Error handler
import error_handler


load_dotenv(dotenv_path='config.env')
AUTH_TOKEN = os.environ.get('AUTH_TOKEN')

# Connecting


@bot.event
async def on_ready():
    print('Launched successfully')


bot.run(f'{AUTH_TOKEN}')
