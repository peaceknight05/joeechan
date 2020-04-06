import discord
from discord.ext import commands
import random
import requests
import json
import math
from datetime import datetime
import datetime as dt

key = "poAUDhKVDwQYFQQXhkMlC6j6B0H6lTp2mzmtKgwR"

class Fun(commands.Cog):
    """Fun Stuff"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="slap", description="After being slapped, a user cannot slap anyone else for 30 seconds as he/she recoils in shock.")
    async def slap(self, ctx, member: discord.Member):
        """Slaps some one. In style."""

        if "TRYHARD" in [x.name for x in ctx.message.author.roles]:
            await ctx.send("HAHA THE TRYHARD WANTS TO SLAP SOMEONE! LMAO KOMEDI GOLD! " + ctx.author.mention)
            return

        if member == bot.user:
            await ctx.send("**YOU DARE TRY TO SLAP ME** _I will holy slap you!_\n"+ctx.author.mention+" has been sent into a 1-day long shock by my holy slap! Maybe that will teach you peasants a lesson.")
            end = datetime.now() + dt.timedelta(days=1)
            if str(ctx.author.id) in j.keys():
                payload = {
                    "end": end.timestamp()
                }
                requests.patch(f'https://joneechan-610b3.firebaseio.com/shock/{str(ctx.author.id)}.json?auth={key}', data=json.dumps(payload))
            else:
                payload = {str(ctx.author.id): {
                    "ID" : ctx.author.id,
                    "end" : end.timestamp()
                }}
                requests.patch(f'https://joneechan-610b3.firebaseio.com/shock.json?auth={key}', data=json.dumps(payload))
            return

        slap = discord.File('./assets/img/slap.gif')
        selfslap = discord.File('./assets/img/selfslap.gif')

        res = requests.get(f'https://joneechan-610b3.firebaseio.com/shock.json?auth={key}')
        j = json.loads(res.text)
        if j == None: j = {}
        if str(ctx.author.id) in j.keys():
            if datetime.fromtimestamp(j[str(ctx.author.id)]["end"]) < datetime.now():
                requests.delete(f'https://joneechan-610b3.firebaseio.com/shock/{ctx.author.id}.json?auth={key}')
                j.pop(str(ctx.author.id))
                await ctx.message.delete()
                await ctx.send(f'{ctx.author.mention} has recovered from their shock.')
                if member.id == ctx.author.id:
                    await ctx.send(f'{ctx.author.mention} slapped themself!')
                    await ctx.send(file=selfslap)
                else:
                    await ctx.send(f'{ctx.author.mention} slapped {member.mention}!')
                    await ctx.send(file=slap)
                if not str(member.id) in j.keys():
                    payload = {str(member.id): {
                        "ID": member.id,
                        "end": datetime.now().timestamp()+30
                    }}
                    requests.patch(f'https://joneechan-610b3.firebaseio.com/shock.json?auth={key}', data=json.dumps(payload))
                    await ctx.send(f'{member.mention} is now recoiling from the shock of being slapped!')
                else:
                    if datetime.fromtimestamp(j[str(member.id)]["end"]) < datetime.now():
                        payload = {
                            "end": datetime.now().timestamp()+30
                        }
                        requests.patch(f'https://joneechan-610b3.firebaseio.com/shock/{str(member.id)}.json?auth={key}', data=json.dumps(payload))
                        await ctx.send(f'{member.mention} has recovered from their shock. But is brutally sent into shock again.')
                    else:
                        if member.id == ctx.author.id:
                            await ctx.send(f'{member.mention} is already recoiling from shock! What a dumbass.')
                        else:
                            await ctx.send(f'{member.mention} is already recoiling from shock! What a bully.')
            else:
                await ctx.message.delete()
                await ctx.send(f'You are still recoiling from shock. {math.floor(j[str(ctx.author.id)]["end"]-datetime.now().timestamp())} seconds of shock remaining.')
        else:
            await ctx.message.delete()
            if member.id == ctx.author.id:
                await ctx.send(f'{ctx.author.mention} slapped themself!')
                await ctx.send(file=selfslap)
            else:
                await ctx.send(f'{ctx.author.mention} slapped {member.mention}!')
                await ctx.send(file=slap)
            if not str(member.id) in j.keys():
                payload = {str(member.id): {
                    "ID": member.id,
                    "end": datetime.now().timestamp()+30
                }}
                requests.patch(f'https://joneechan-610b3.firebaseio.com/shock.json?auth={key}', data=json.dumps(payload))
                await ctx.send(f'{member.mention} is now recoiling from the shock of being slapped!')
            else:
                if datetime.fromtimestamp(j[str(member.id)]["end"]) < datetime.now():
                    payload = {
                        "end": datetime.now().timestamp()+30
                    }
                    requests.patch(f'https://joneechan-610b3.firebaseio.com/shock/{str(member.id)}.json?auth={key}', data=json.dumps(payload))
                    await ctx.send(f'{member.mention} has recovered from their shock. But is brutally sent into shock again.')
                else:
                    if member.id == ctx.author.id:
                        await ctx.send(f'{member.mention} is already recoiling from shock! What a dumbass.')
                    else:
                        await ctx.send(f'{member.mention} is already recoiling from shock! What a bully.')

    @commands.command(name="pat", description="Because why not. But that person may not like it tho.")
    async def pat(self, ctx, member: discord.Member):
        """Pats some one. KAWAIII!"""

        pat = discord.File('./assets/img/pat.gif')
        selfpat = discord.File('./assets/img/selfpat.png')
        swat = discord.File('./assets/img/swat.gif')

        await ctx.message.delete()
        if ctx.author == member:
            await ctx.send(f'{ctx.author.mention} pet themself! Thats so sad!')
            await ctx.send(file=selfpat)
        else:
            if random.randint(0,3) == 0:
                await ctx.send(f'{ctx.author.mention} tried to pet {member.mention}!')
                await ctx.send(f'{member.mention} swatted {ctx.author.mention}\'s hand away!')
                await ctx.send(file=swat)
            else:
                await ctx.send(f'{ctx.author.mention} pet {member.mention}!')
                await ctx.send(file=pat)

    @commands.command(name="roll", description="The number of dice rolled cannot exceed 500. The type of dice rolled must be at least a d2 or at most a d1000.\nYou can add \"-onlyTotal at the end\" to only show the total.", pass_context=True)
    async def roll(self, ctx, dice : str, *args : str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
            if rolls > 500: raise commands.errors.UserInputError
            if limit < 2 or limit > 1000: raise commands.errors.UserInputError
        except Exception:
            raise commands.errors.UserInputError

        await ctx.message.delete()
        if rolls > 100:
            result = f'Total ({rolls} die): {sum([random.randint(1, limit) for r in range(rolls)])}\n_Compressed to reduce spam_'
        elif "-onlyTotal" in args:
            result = f'Total ({rolls} die): {sum([random.randint(1, limit) for r in range(rolls)])}'
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
        if (message.content.split(" ")[-1] == '--spongeText') and (len(message.content.split(" ")) > 1):
            t = " ".join(message.content.split(" ")[:-1])
            s = ""
            for c in t:
                s += random.choice([c.upper(), c.lower()])
            await message.delete()
            await message.channel.send(s)

    @commands.command(name="choose", pass_context=True, description="Must be given at least 2 choices.\nYou can add \"-hideChoices\" to the end to hide the choices and only show the outcome. Do not include \"-\" at the front of any options or it will be taken to be a flag.")
    async def choose(self, ctx, *choices : str):
        """Chooses between multiple choices."""
        if len(choices) < 2: raise commands.errors.UserInputError
        hide = False
        if "-hideChoices" in choices:
            hide = True
        choices = [x for x in choices if x[0] != '-']
        embed=discord.Embed(title="Choice", description="For indecisive people.", color=0x32cd32)
        embed.add_field(name="Choices", value=("Hidden by user" if hide else ', '.join(choices)), inline=False)
        embed.add_field(name="Outcome", value=random.choice(choices), inline=False)
        embed.set_footer(text="Fun Fact: You can put more than one word as an argument in any command that accepts strings. Surround the argument in double inverted commas \"like this\".")
        await ctx.message.delete()
        await ctx.send(embed=embed)

    @commands.command(name='clap', description="You can clap from 0 to 10 claps.", pass_context=True)
    async def clap(self, ctx):
        """A command to clap."""
        claps = random.randint(0,10)
        await ctx.message.delete()
        await ctx.send(f'{ctx.author.mention} failed at clapping!' if claps == 0 else f'{ctx.author.mention} clapped! {":clap:" * claps}')

def setup(bot):
    bot.add_cog(Fun(bot))