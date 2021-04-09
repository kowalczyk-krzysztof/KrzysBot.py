from discord.embeds import Embed
from discord.colour import Colour
background: Colour = Colour.dark_gold()

# Creating list of bot commands


def create_command_list(*commands):

    embed = Embed(
        title="Command List",
        colour=background
    )
    commands = commands
    for command in commands:
        embed.add_field(
            name=f'.{command.command_name}', value=f'Example: ```.{command.command_name} {command.example_input}```\n{command.command_desc}', inline=False)
    return embed

# Check if stirng is empty


def empty_check(input_string: str):
    return "".__eq__(input_string)

# Strips whitespace and dots


def string_stripper(input_string: str):
    return input_string.upper().replace(
        " ", "").replace(".", "")
