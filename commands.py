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
from utils import empty_check, string_stripper, create_command_list, background
# Simpleeval - safe eval(), need it for my calculator
from simpleeval import simple_eval

bot = commands.Bot(command_prefix='.', help_command=None)


# List of commands

class BotCommand:
    def __init__(self, command_name: str, example_input: str, command_desc: str):
        self.command_name = command_name
        self.example_input = example_input
        self.command_desc = command_desc


__compatibility = BotCommand(
    'compatibility', 'Romeo Juliet', 'Check how compatibile two users are')
__quote = BotCommand('quote', 'Albert Einstein',
                     'Get a random quote from author of your choice')
__temple = BotCommand('temple', 'zezima', 'Get a link to TempleOSRS profile')
__calc = BotCommand('calc', '(10*5) + 73',
                    'Perform basic arithmetic operations')


@bot.command(aliases=['commands', 'help'])
async def _commands(context):
    embed = create_command_list(__compatibility, __quote, __temple, __calc)
    await context.send(embed=embed)

# User compatibility


@bot.command()
async def compatibility(context, name1: str, name2: str):

    n: int = random.randint(0, 100)
    await context.send(f'{name1} is {n}% compatible with {name2}')

# Link to TempleOSRS profile


@bot.command()
async def temple(context, value: str):
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
    search_term: str = " ".join(author)
    # Empty string check
    if empty_check(search_term):
        return await context.send('Please provide an author')

    # Result is a list of dictionaries with keys "author", "book", "quote"
    result: list or None = quote(search_term)

    if result == None:
        await context.send(f'Author with name **{search_term}** not found')
    else:
        # INDEXES HAS TO BE OUTSIDE THE LOOP!!!!
        indexes: list = []
        stripped_search_term: str = string_stripper(search_term)
        for dict_item in result:

            stripped_authors: str = string_stripper(dict_item["author"])

            if stripped_search_term in stripped_authors:
                indexes.append(result.index(dict_item))

        if len(indexes) == 0:
            await context.send(f'Author with name **{search_term}** not found')
        else:
            random_quote: int = random.choice(indexes)

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


# Command below uses simpleeval (https://github.com/danthedeckie/simpleeval). Although it seems safe, there's always risk, just like with any form of eval(), although it uses ast.literal_eval
# Simple calculator. First whitespaces are removed from user_input and the result is assigned to variable "initial_equation". This is done so input like "2+2 - 2" becomes "2+2-2".
# Then "^" in initial_equation is replaced with "**" and "," is replaced with ".'. The result is assigned to variable equation. This is done because most Discord users are used to using "^" for power but Python uses "**" and some users prefer to use "," for decimals.
# Then check if equation has any valid_operators (this takes care of empty check too).
# Then check if any of valid_operators is last index of equation (to prevent doing something like ".calc 2+").
# Then check if equation has any letters (by checking if there's any uppercase or lowercase in it).
# If any of above checks fails, return a msg "Invalid input".
# Then pass equation to simple_eval function - this is similar to .eval() but it doesn't have any of the risks eval has.
# Assign the result of simple_eval as a float to variable result.
# If result is an integer, then return it as an integer, so I don't send values like "4.0" to the user.
# If result is a float then just send it as it is.
@bot.command()
async def calc(context, *user_input):

    initial_equation: str = " ".join(user_input)
    # IMPORTANT: strings are not mutable so you have to assign the .replace result to a variable
    equation = initial_equation.replace('^', "**").replace(",", ".")

    valid_operators: list = ["+", "-", "/", "*", "%", "^"]
    # operator_check is how I check if a string contains any element from a list, it will also return false if the iterable is empty, so this covers empty check too
    operator_check: bool = any(
        operator in equation for operator in valid_operators)
    # checks if arithmetic operator is last element in equation, to prevent doing something like ".calc 2+"

    def last_element(equation: str):
        for operator in valid_operators:
            if operator == equation[-1]:
                return True

    if not operator_check or last_element(equation) or equation.isupper() or equation.islower():
        return await context.send("Invalid input")

    result: float = float(simple_eval(equation))
    # returning initial_equation here so user sees "^" instead of "**"
    if result.is_integer():
        await context.send(f'**Input:** ```fix\n{initial_equation}```**Result:** ```fix\n{int(result)}```')
    else:
        await context.send(f'**Input:** ```fix\n{initial_equation}```**Result:** ```fix\n{result}```')
