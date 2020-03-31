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

@bot.command(name='clap', help="A command to clap.")
async def clap(ctx):
    claps = random.randint(0,10)
    await ctx.message.delete()
    await ctx.send(f'{ctx.author.mention} failed at clapping!' if claps == 0 else f'{ctx.author.mention} clapped! {":clap:" * claps}')

@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: str):
    if not number_of_sides in ["d4", "d6", "d8", "d10", "d12", "d20", "d100"]:
        raise commands.errors.UserInputError
    elif number_of_sices > 500:
        await ctx.send("Too many dice (max = 500).")
    else:
        dice = [
            str(random.choice(range(1, int(number_of_sides[1:]) + 1)))
            for _ in range(number_of_dice)
        ]
        await ctx.message.delete()
        if number_of_dice > 100:
            await ctx.send(f'Total {number_of_dice}: {sum([int(x) for x in dice])}\n_Collapsed to reduce spam._')
        else:
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
async def on_message(message):
    if message.author == bot.user:
        return
    if 'yoyoke' in message.content.split(" "):
        await message.channel.send("HAHA YOYOKE!")

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
    elif isinstance(error, commands.errors.UserInputError):
        await ctx.send('Argument error.')
    elif isinstance(error, asyncio.TimeoutError):
        await ctx.send('Timeout. It has been 30 seconds.')

bot.run(TOKEN)