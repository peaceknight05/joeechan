import discord
from discord.ext import commands
import random

class Fun(commands.Cog):
    """Fun Stuff."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="roll", description="The number of dice rolled cannot exceed 500. The type of dice rolled must be at least a d2 or at most a d100.", pass_context=True)
    async def roll(self, ctx, dice : str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
            if rolls > 500: raise commands.errors.UserInputError
            if limit < 2 or limit > 100: raise commands.errors.UserInputError
        except Exception:
            raise commands.errors.UserInputError

        await ctx.message.delete()
        if rolls > 100:
            result = f'Total ({rolls} die): {sum([random.randint(1, limit) for r in range(rolls)])}\n_Compressed to reduce spam_'
        else:
            result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if 'yoyoke' in [x.lower() for x in message.content.split(" ")]:
            await message.channel.send("HAHA YOYOKE!")
        if message.content.startswith("kids these days") or message.content.startswith("Kids these days"):
            await message.channel.send("ok boomer")

    @commands.command(name="choose", pass_context=True, description="Must be given at least 2 choices.\nYou can add \"-hideChoices\" to the end to hide the choices and only show the outcome.")
    async def choose(self, ctx, *choices : str):
        """Chooses between multiple choices."""
        if len(choices) < 2: raise commands.errors.UserInputError
        await ctx.message.delete()
        hide = False
        if "-hideChoices" in choices:
            hide = True
        choices = [x for x in choices if x[0] != '-']
        embed=discord.Embed(title="Choice", description="For indecisive people.", color=0x32cd32)
        embed.add_field(name="Choices", value=("Hidden by user" if hide else ', '.join(choices)), inline=False)
        embed.add_field(name="Outcome", value=random.choice(choices), inline=False)
        embed.set_footer(text="Fun Fact: You can put more than one word as an argument in any command that accepts strings. Surround the argument in double inverted commas \"like this\".")
        await ctx.send(embed=embed)

    @commands.command(name='clap', description="You can clap from 0 to 10 claps.", pass_context=True)
    async def clap(self, ctx):
        """A command to clap."""
        claps = random.randint(0,10)
        await ctx.message.delete()
        await ctx.send(f'{ctx.author.mention} failed at clapping!' if claps == 0 else f'{ctx.author.mention} clapped! {":clap:" * claps}')

def setup(bot):
    bot.add_cog(Fun(bot))