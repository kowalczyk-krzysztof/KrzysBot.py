# Discord
import requests
import discord
from discord.ext import commands
# OS
import os
# Dotenv
from dotenv import load_dotenv
# Random
import random
# Quotes
from quote import quote

load_dotenv(dotenv_path='config.env')
AUTH_TOKEN = os.environ.get('AUTH_TOKEN')

client = commands.Bot(command_prefix='.')

# List of commands - need to use an alias coz commands is reserved


@client.command(aliases=['commands'])
async def _commands(context):
    await context.send('COMMAND LIST:\n\n.compatibility - shows how compatibile you are with other user\n.temple - link to templeOSRS profile')

# User compatibility


@client.command()
async def compatibility(context, name1, name2):
    n = random.randint(0, 100)
    await context.send(f'{name1} is {n}% compatible with {name2}')

# Link to TempleOSRS profile


@client.command()
async def temple(context, value):
    await context.send(f'https://templeosrs.com/player/overview.php?player={value}')

# Random quote


@client.command(aliases=['quote'])
# Logic: Join user input then fetch quotes containing user input. Concatenate user input into uppercase, splitting whitespaces and dots. Do the same for each dict_item["author"] in result. Then if concatenated dict_item["author"] contains concatenated user input, append it's index to a list. Then use random.choice() to pick one number from that list and return result[randomIndex]["quote"]
# *author is how I spread arguments in Python
async def _quote(context, *author):
    # " ".join is how I join items in a list
    searchTerm = " ".join(author)

    searchTermFormatted = ",".join(author).replace(',', " ")

    # Result is a list of dictionaries with keys "author", "book", "quote"
    result = quote(searchTerm)
    # Strips whitespace and dots

    def stringStripper(inputString):
        return inputString.upper().replace(
            " ", "").replace(".", "")

    if result == None:
        await context.send(f'Author with name **{searchTermFormatted}** not found')
    else:
        # INDEXES HAS TO BE OUTSIDE THE LOOP!!!!
        indexes = []
        strippedSearchTerm = stringStripper(searchTerm)
        for dict_item in result:

            strippedAuthors = stringStripper(dict_item["author"])

            if strippedSearchTerm in strippedAuthors:
                indexes.append(result.index(dict_item))

        if len(indexes) == 0:
            await context.send(f'Author with name **{searchTermFormatted}** not found')
        else:
            randomQuote = random.choice(indexes)
            await context.send(f'**Author**: {result[randomQuote]["author"]}\n**Quote**: {result[randomQuote]["quote"]}')


# Connecting


@ client.event
async def on_ready():
    print('Launched successfully')


client.run(f'{AUTH_TOKEN}')
