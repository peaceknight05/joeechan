import os
import discord
import random
from dotenv import load_dotenv
from discord.ext import commands
import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
VERSION = os.getenv('VERSION')

bot = commands.Bot(command_prefix='^')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='99', help="Responds with a random quote from Brooklyn 99")
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.message.delete()
    await ctx.send(response)

@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.message.delete()
    await ctx.send(', '.join(dice))

@bot.command(name='info', help='Get info about the bot.')
async def info(ctx):
    await ctx.message.delete()
    embed=discord.Embed(title="Info", description="Info about the bot.", color=0xb1c900)
    embed.add_field(name="Creator", value="Jonathan Tan", inline=True)
    embed.add_field(name="Version", value=VERSION, inline=True)
    embed.set_footer(text="I was created in my author's freetime. But he has no more, so don't expect much updates.")
    file = discord.File("assets/img/icon.png", filename="icon.png")
    embed.set_thumbnail(url="attachment://icon.png")
    await ctx.send(file=file, embed=embed)

@bot.event
async def on_error(event, *args, **kwargs):
    if event == 'on_message':
        await args[0].author.create_dm()
        await args[0].author.dm_channel.send(f'Unhandled message: {args[0]}\n')
    else:
        raise

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

bot.run(TOKEN)