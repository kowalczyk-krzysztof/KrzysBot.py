# Dotenv
from dotenv import load_dotenv
# OS
import os
# Discord
import discord
from discord.ext import commands


def main():
    pass


main()

bot = commands.Bot(command_prefix='.', help_command=None)
load_dotenv(dotenv_path='config.env')
AUTH_TOKEN: str = os.environ.get('AUTH_TOKEN')


@bot.command
async def load(context, extension):
    bot.load_extension(f'cogs.{extension}')


@bot.command
async def unload(context, extension):
    bot.unload_extension(f'cogs.{extension}')

# Errors


@bot.event
async def on_command_error(context, error):
    if isinstance(error, commands.ExpectedClosingQuoteError):
        return await context.send('**ERROR**: Invalid syntax')
    if isinstance(error, commands.MissingRequiredArgument):
        return await context.send('**ERROR**: Required arguments not provided, see:```.commands``` for more info')

# Loading cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and not filename.startswith('__init__'):
        bot.load_extension(f'cogs.{filename[:-3]}')


# Connecting


@bot.event
async def on_ready():
    print('Launched successfully')

bot.run(f'{AUTH_TOKEN}')
