from commands import bot
from discord.ext import commands

# Error handler


@bot.event
async def on_command_error(context, error):
    if isinstance(error, commands.ExpectedClosingQuoteError):
        await context.send('**ERROR**: Invalid syntax')
    if isinstance(error, commands.MissingRequiredArgument):
        await context.send('**ERROR**: Required arguments not provided, see:```.commands``` for more info')