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

# List of commands


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

# Get a random quote using quote pip library.
# First, join user input (author) and assing it to variable search_term, so "Albert Einstein" becomes "AlbertEinstein".
# Then check if search_term is empty (if True, return a msg).
# Then use quote method to find quotes and assign them to a variable result. The result will be a list of dictioanries with fields "author", "book", "quote". Quote method search if any of those fields contains search_term.
# If result == None, return a msg.
# Else pass search term to string_stripper() and assign it to variable stripperd_search_term (this makes the string uppercase and removes all whitespace and ",").
# Then do the same for every key "author" in dictionaries in result and assign it to stripepd_authors variable and check if stripped_authors contains stripped_search term. If true, append the index of that dictionary to a list indexes.
# If indexes is empty (so there was no author that is equal to search term) return a msg.
# Else pick a random number from indexes and assign it to random quote variable.
# Return result[random_quote] to user as an Embed with fields "Author" (result[random_quote]["author"] as value) and "Quote" (result[random_quote]["quote"] as value)


@bot.command(aliases=['quote'])
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


# Simple calculator. First whitespaces are removed and the result is assigned to variable "equation". This is done so input like "2+2 - 2" becomes "2+2-2".
# Then check if equation has any valid_operators (this takes care of empty check too).
# Then check if any of valid_operators is last index of equation (to prevent doing something like ".calc 2+").
# Then check if equation has any letters (by checking if there's any uppercase or lowercase in it).
# Then check if equation has "," (some users like to use "," instead of ".")
# If any of above checks fails, return a msg "Invalid input".
# Else check for "^" symbol in equation (often people use "^" for power but in Python you need to use "**" so I had to make a check for that). if true, return msg "Syntax Error"
# Then pass equation to simple_eval function - this is similar to .eval() but it doesn't have any of the risks eval has.
# Assign the result of simple_eval as a float to variable result.
# If result is an integer, then return it as an integer, so I don't send values like "4.0" to the user.
# If result is a float then just send it as it is.
@bot.command()
async def calc(context, *user_input):

    equation = " ".join(user_input)

    valid_operators = ["+", "-", "/", "*", "%", "**"]
    # operator_check is how I check if a string contains any element from a list, it will also return false if the iterable is empty, so this covers empty check too
    operator_check = any(operator in equation for operator in valid_operators)
    # checks if arithmetic operator is last element in equation, to prevent doing something like ".calc 2+"

    def last_element(equation: str):
        for operator in valid_operators:
            if operator == equation[-1]:
                return True

    if not operator_check or last_element(equation) or equation.isupper() or equation.islower() or ',' in equation:
        return await context.send("Invalid input")

    elif "^" in equation:
        valid_power_symbol = '**'
        invalid_power_symbol = '^'
        return await context.send(f'**Syntax error**: To use power, use **{valid_power_symbol}**  instead of **{invalid_power_symbol}**')

    else:
        result = float(simple_eval(equation))
        if result.is_integer():
            await context.send(f'**Input:** ```fix\n{equation}```**Result:** ```fix\n{int(result)}```')
        else:
            await context.send(f'**Input:** ```fix\n{equation}```**Result:** ```fix\n{result}```')
