import os
import discord
import random
from dotenv import load_dotenv
from discord.ext import commands
import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
VERSION = os.getenv('VERSION')

startup_extensions = ["fun", "school"]

UPDATES = """Dice upgrade (next minor change - 0.0.x)
8 ball (next minor change - 0.0.x)
awards system (next major change - x.0.0)
currency (next major change - x.0.0)
games (next major change = x.0.0)
"""

bot = commands.Bot(command_prefix='^')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='info', decription='Get info about the bot, its creator and future changes.')
async def info(ctx):
    """Get info about the bot."""
    await ctx.message.delete()
    embed=discord.Embed(title="Info", description="Info about the bot.", color=0xb1c900)
    embed.add_field(name="Creator", value="Jonathan Tan", inline=True)
    embed.add_field(name="Version", value=VERSION, inline=True)
    embed.add_field(name="Future Updates", value=UPDATES, inline=False)
    embed.set_footer(text="I was created in my author's freetime. But he has no more, so don't expect much updates.")
    file = discord.File("assets/img/icon.png", filename="icon.png")
    embed.set_thumbnail(url="attachment://icon.png")
    await ctx.send(file=file, embed=embed)

@bot.event
async def on_error(event, *args, **kwargs):
    if event == 'on_message':
        await args[0].author.create_dm()
        await args[0].author.dm_channel.send(f'Unhandled message: {args}\n')
        await args[0].author.dm_channel.send("Send this to the bot creator.")
    else:
        raise

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')
    elif isinstance(error, commands.errors.UserInputError):
        await ctx.send('Argument error.\n_You can do ^help <command> to dee the syntax and notes on valid inputs._')
    elif isinstance(error, asyncio.TimeoutError):
        await ctx.send('Timeout. It has been 30 seconds.')

for extension in startup_extensions:
    try:
        bot.load_extension(extension)
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        print('Failed to load extension {}\n{}'.format(extension, exc))

bot.run(TOKEN)