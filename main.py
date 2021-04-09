# Discord
import discord
from discord.ext import commands
from discord.embeds import Embed
from discord.colour import Colour
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
background = Colour.dark_gold()

# List of commands - need to use an alias coz commands is reserved


@client.command(aliases=['commands'])
async def _commands(context):
    embed = Embed(
        title="Command List",
        colour=background
    )
    embed.add_field(name='.compatibility',
                    value='Example: ```.compatibility Romeo Juliet```\nCheck how compatibile two users are', inline=False)
    embed.add_field(name='.quote',
                    value='Example: ```.quote Albert Einstein```\nGet a random quote from author of your choice', inline=False)
    embed.add_field(name='.temple',
                    value='Example: ```.temple zezima```\nGet a link to TempleOSRS profile', inline=False)

    await context.send(embed=embed)

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
    search_term = " ".join(author)
    # Empty string check
    if "".__eq__(search_term):
        return await context.send('Please provide an author')

    # Result is a list of dictionaries with keys "author", "book", "quote"
    result = quote(search_term)
    # Strips whitespace and dots

    def string_stripper(input_string):
        return input_string.upper().replace(
            " ", "").replace(".", "")

    if result == None:
        await context.send(f'Author with name **{search_term}** not found')
    else:
        # INDEXES HAS TO BE OUTSIDE THE LOOP!!!!
        indexes = []
        stripped_search_term = string_stripper(search_term)
        for dict_item in result:

            stripped_authors = string_stripper(dict_item["author"])

            if stripped_search_term in stripped_authors:
                indexes.append(result.index(dict_item))

        if len(indexes) == 0:
            await context.send(f'Author with name **{search_term}** not found')
        else:
            random_quote = random.choice(indexes)

            embed = Embed(
                title="Random Quote",
                colour=background
            )
            embed.add_field(name="Author:", value=(
                f'{result[random_quote]["author"]}'), inline=False)

            embed.add_field(name="Quote:", value=(
                f'{result[random_quote]["quote"]}'), inline=False)

            await context.send(embed=embed)


# Connecting


@ client.event
async def on_ready():
    print('Launched successfully')


client.run(f'{AUTH_TOKEN}')
