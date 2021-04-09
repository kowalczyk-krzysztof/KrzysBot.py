# Discord
import discord
from discord.ext import commands
from discord.embeds import Embed
from discord.colour import Colour
# Random
import random
# Quotes
from quote import quote
# Utils
from utils import empty_check, string_stripper
# Simpleeval - safe eval(), need it for my calculator
from simpleeval import simple_eval

# Bot variables
bot = commands.Bot(command_prefix='.', help_command=None)
background = Colour.dark_gold()


@bot.command(aliases=['commands', 'help'])
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
    embed.add_field(name='.calc',
                    value='Example: ```.calc (10*5) + 73```\nPerform basic arithmetic operations', inline=False)

    await context.send(embed=embed)

# User compatibility


@bot.command()
async def compatibility(context, name1, name2):

    n = random.randint(0, 100)
    await context.send(f'{name1} is {n}% compatible with {name2}')

# Link to TempleOSRS profile


@bot.command()
async def temple(context, value):
    await context.send(f'https://templeosrs.com/player/overview.php?player={value}')

# Random quote


@bot.command(aliases=['quote'])
# Logic: Join user input then fetch quotes containing user input. Concatenate user input into uppercase, splitting whitespaces and dots. Do the same for each dict_item["author"] in result. Then if concatenated dict_item["author"] contains concatenated user input, append it's index to a list. Then use random.choice() to pick one number from that list and return result[randomIndex]["quote"]
# *author is how I spread arguments in Python
async def _quote(context, *author):
    # " ".join is how I join items in a list
    search_term = " ".join(author)
    # Empty string check
    if empty_check(search_term):
        return await context.send('Please provide an author')

    # Result is a list of dictionaries with keys "author", "book", "quote"
    result = quote(search_term)

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

# Simple calculator, equation is a string like "2+2". Now I don't really know how to handle parsing something like "2+2-3" so I'm just returning a message if that happens. One solution could be to use eval() but eval = evil so I should avoid using it. EDIT: Turns out simpleeval library exists and does exactly what I want. Leaving the old code below for future if so I can laugh at myself.
# @bot.command()
# async def calc(context, equation):

#     async def equation_splitter(equation, operator):
#         y = equation.split(operator)
#         if len(y) > 2 or y[1].isnumeric() == False:
#             return await context.send("Fuck off this is a simple calculator")
#         else:
#             return y

#     if equation.isupper() or equation.islower():
#         return await context.send("Invalid input")
#     elif '+' in equation:
#         y = await equation_splitter(equation, '+')
#         result = float(y[0]) + float(y[1])
#     elif '-' in equation:
#         y = await equation_splitter(equation, '-')
#         result = float(y[0]) - float(y[1])
#     elif '*' in equation:
#         y = await equation_splitter(equation, '*')
#         result = float(y[0]) * float(y[1])
#     elif '/' in equation:
#         y = await equation_splitter(equation, '/')
#         if y[1] == '0':
#             return await context.send("You can't divide by 0")
#         else:
#             result = float(y[0]) / float(y[1])
#     elif '^' in equation:
#         y = await equation_splitter(equation, '^')
#         result = float(y[0])**float(y[1])
#     else:
#         return await context.send("Invalid input")

#     if result.is_integer():
#         await context.send(f'**Result:** ```{int(result)}```')
#     else:
#         await context.send(f'**Result:** ```{result}```')


# Simple calculator. First whitespaces are removed, then a check is performed if user_input has any letters in it (if True, return a msg), then a check for "^" symbol is performed - often people use ^ for power but in Python you need to use ** so I had to make a check for that. Now, I don't want to return results like "4.0" so I'm checking whether result is an integer or not and sending a message based on that.
@bot.command()
async def calc(context, *user_input):
    equation = " ".join(user_input)

    valid_power_symbol = '**'
    invalid_power_symbol = '^'

    if equation.isupper() or equation.islower():
        return await context.send("Invalid input")

    elif "^" in equation:
        return await context.send(f'**Syntax error**: To use power, use **{valid_power_symbol}**  instead of **{invalid_power_symbol}**')

    else:
        result = float(simple_eval(equation))

        if result.is_integer():
            await context.send(f'**Result:** ```{int(result)}```')
        else:
            await context.send(f'**Result:** ```{result}```')
