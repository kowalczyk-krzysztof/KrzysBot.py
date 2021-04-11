# Python modules
from decimal import Decimal
# Discord
import discord
from discord.ext import commands
from discord.embeds import Embed
from discord.colour import Colour
from discord.guild import Guild
# Abstract Syntax Tree
import ast
# Random
import random
# Quotes
from quote import quote
# Utils
# from discord_bot.utilities.utils import create_command_list, empty_check, string_stripper, background, decistmt
from utilities.utils import background, create_command_list, empty_check, string_stripper, decistmt


class BotCommand:
    def __init__(self, command_name: str, example_input: str, command_desc: str):
        self.command_name = command_name
        self.example_input = example_input
        self.command_desc = command_desc


class Various(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    # List of commands
    @commands.command(aliases=['commands', 'help'])
    async def _commands(self, context):
        __compatibility = BotCommand(
            'compatibility', 'Romeo Juliet', 'Check how compatibile two users are')

        __quote = BotCommand('quote', 'Albert Einstein',
                             'Get a random quote from author of your choice')
        __temple = BotCommand('temple', 'zezima',
                              'Get a link to TempleOSRS profile')
        __calc = BotCommand('calc', '(10*5) + 73',
                            'Perform basic arithmetic operations')
        embed = create_command_list(__compatibility, __quote, __temple, __calc)
        await context.send(embed=embed)
    # User compatibility

    @commands.command()
    async def compatibility(self, context, name1: str, name2: str):

        n: int = random.randint(0, 100)
        await context.send(f'{name1} is {n}% compatible with {name2}')
    # Link to TempleOSRS profile

    @commands.command()
    async def temple(self, context, value: str):
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

    @commands.command(aliases=['quote'])
    # *author is how I spread arguments in Python
    async def _quote(self, context, *, author: str):

        # " ".join is how I join items in a list
        search_term: str = author
        # Empty string check
        if empty_check(search_term):
            return await context.send('Please provide an author')

        # Result is a list of dictionaries with keys "author", "book", "quote"
        result: list or None = quote(search_term)

        async def author_not_found(author: str):
            await context.send(f'Author with name **{author}** not found')

        if result == None:
            await author_not_found(search_term)
        else:
            # INDEXES HAS TO BE OUTSIDE THE LOOP!!!!
            indexes: list = []
            stripped_search_term: str = string_stripper(search_term)
            for dict_item in result:
                stripped_authors: str = string_stripper(dict_item["author"])
                if stripped_search_term in stripped_authors:
                    indexes.append(result.index(dict_item))

        if len(indexes) == 0:
            await author_not_found(search_term)
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
        # Take user input which is a string, then:
        # 1. Strip whitespaces
        # 2. Check the length, if > 100 (random nr, idk what it should #3. Check if input has any characters not in `set("0123456789.,+-*/^%()")`, if true return error. note: I allow `,` and `^` because some people use `,` for decimals and most people use `^` for power but it's invalid python syntax
        # 4. Check if input has arithmetic operators `set("+-/*%^")` if false, return eror. note: this is so ".calc 2" etc. is invalid input
        # 5. Check if arithmetic operator is last or first character in input (for first character, make exception for "-" to allow negative numbers) it true, return error. note: This is done so ".calc +2" or ".calc 2+" is invalid input.
        # 6. Replace all instances of `^` with `**` and all `,` with `.` so input has valid Python syntax
        # 7. Use a method that replaces all floats in a string with Decimal objects (from decimal module). This method uses tokenize module.
        # 8. Parse the result of this function into an AST (Abstract Syntax Tree) node with mode 'eval'
        # 9. Compile the AST node
        # 10. eval() the compiled result
        # 11. Check if the result is int or decimal to avoid sending results like "4.0" to user
        # 12. Send result to user
        # TODO: A way to stop running if calc takes too long

    @commands.command()
    async def calc(self, context, *, user_input: str):
        # strip all whitespace to, otherwise check for allowed characters would fail if input has spaces
        stripped_user_input = user_input.replace(" ", "")
        # limiting max length
        if len(stripped_user_input) > 100:
            return await context.send(f'**ERROR**: Input too big')
        # limiting allowed characters
        allowed_characters = set("0123456789.,+-*/^%()")
        if any(character not in allowed_characters for character in stripped_user_input):
            return await context.send("Invalid input")
        # check if input has arithmetic operators - note: no point adding "**" since "*" will take care of this check
        valid_operators = set("+-/*%^")
        if not any(operator in stripped_user_input for operator in valid_operators):
            return await context.send("Invalid input")
        # checks if arithmetic operator is last or first element in equation, to prevent doing something like ".calc 2+" or ".calc +2"

        def is_last_or_first(equation: str):
            for operator in valid_operators:
                if operator == stripped_user_input[-1]:
                    return True
                elif operator == stripped_user_input[0]:
                    if operator == "-":
                        return False
                    else:
                        return True

        if is_last_or_first(stripped_user_input):
            return await context.send("Invalid input")
        # sanitize input to valid python syntax
        equation = stripped_user_input.replace('^', "**").replace(",", ".")
        # convert all floats to Decimal objects then ast.parse
        tree = ast.parse(decistmt(equation), mode='eval')

        def calculation(tree):
            result = eval(compile(tree, '', 'eval'))
            return result

        future = await context.bot.loop.run_in_executor(None, calculation, tree)
        print(future)

        result = future

        result = float(result)

        async def result_generator(result: int or float):
            await context.send(f'**Input:** ```fix\n{user_input}```**Result:** ```fix\n{result}```')
        if result.is_integer():
            await result_generator(int(result))
        else:
            await result_generator(result)


def setup(bot):
    bot.add_cog(Various(bot))
