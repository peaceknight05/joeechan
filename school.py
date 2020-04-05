import discord
from discord.ext import commands
import requests
import json
import datetime

key = "poAUDhKVDwQYFQQXhkMlC6j6B0H6lTp2mzmtKgwR"

class School(commands.Cog):
    """Stuff relating to school in general."""
    def __init__(self, bot):
        self.bot = bot

    def is_rep():
        def predicate(ctx):
            return ("Subject Representatives" in [x.name for x in ctx.message.author.roles]) or (("House Representatives") in [x.name for x in ctx.message.author.roles])
        return commands.check(predicate)

    @commands.command(name="homework", pass_context=True, description="You can pass an argument (the subject name) to the command to get the homework for only that subject (works for only one subject).\nThe subjects are in short form (el, mt, em, am, chem, phy, ss, geog, comp, snw, others).\nYou can pass the flag -dueTmr to only see hw due tmr. You procrastinator.\n You can also pass the flag -noOpt to not see optional homework.\nYou can also pass the flag -pt to only see pt-related homework, or -noPt to not see pt-related homework.")
    async def homework(self, ctx, *args : str):
        """Gives the homework and due date."""
        subject = [x for x in args if x[0] != '-']
        if len(subject) > 1:
            raise commands.errors.UserInputError
        elif len(subject) == 1:
            subject = subject[0]
        else:
            subject = None
        if ("-pt" in args) and ("-noPt" in args):
            await ctx.send("You cannot have the flags -pt and -noPt at the same time!")
            raise commands.errors.UserInputError
        if subject != None:
            if not subject in ["el", "mt", "em", "am", "chem", "phy", "ss", "geog", "comp", "snw", "other"]:
                raise commands.errors.UserInputError
        await ctx.message.delete()
        res = requests.get(f'https://joneechan-610b3.firebaseio.com/homework.json?auth={key}')
        j = json.loads(res.text)
        if j == None:
            await ctx.send("No homework.")
            return
        if '-dueTmr' in args:
            hw = [x for x in j.values() if ((datetime.date.fromtimestamp(x["duedate"])) == (datetime.date.today() + datetime.timedelta(days=1))) and (not ((x["optional"]) and ("-noOpt" in args))) and (not ((x["pt"]) and ("-noPt" in args))) and (not ((not x["pt"]) and ("-pt" in args)))]
            if subject != None:
                hw = [x for x in hw if (x["subject"] == subject) and (not ((x["pt"]) and ("-noPt" in args))) and (not ((not x["pt"]) and ("-pt" in args)))]
            if len(hw) == 0:
                await ctx.send("No homework that falls under these conditions.")
                return
            t = ", ".join(args)
            tags = f'Tags: {t if len(f) > 0 else ""}'
            embed=discord.Embed(title="Homework", description=f'For the lazy.\n{tags}', color=0xbababa)
            for work in hw:
                time = datetime.datetime.fromtimestamp(work["duedate"])
                embed.add_field(name=f'{work["title"]} [{work["subject"].upper()}]', value=f'Due tomorrow on {time.hour}:{"{:0>2d}".format(time.minute)}.{" This homework is optional." if work["optional"] else ""}')
            embed.set_footer(text="I am as reliable as your subject reps, so rely on me at your own risk. I am a bot so I feel no guilt if you miss your homework.")
            await ctx.send(embed=embed)
        else:
            hw =[x for x in j.values() if (not ((x["optional"]) and ("-noOpt" in args))) and (not ((x["pt"]) and ("-noPt" in args))) and (not ((not x["pt"]) and ("-pt" in args)))]
            if subject != None:
                hw = [x for x in hw if x["subject"] == subject and (not ((x["pt"]) and ("-noPt" in args))) and (not ((not x["pt"]) and ("-pt" in args)))]
            if len(hw) == 0:
                await ctx.send("No homework that falls under these conditions.")
                return
            t = ", ".join(args)
            tags = f'Tags: {t if len(f) > 0 else ""}'
            embed=discord.Embed(title="Homework", description=f'For the lazy.\n{tags}', color=0xbababa)
            for work in hw:
                time = datetime.datetime.fromtimestamp(work["duedate"])
                embed.add_field(name=f'{work["title"]} [{work["subject"].upper()}]', value=f'Due on {time.day}/{time.month} on {time.hour}:{"{:0>2d}".format(time.minute)}.{" This homework is optional." if work["optional"] else ""}')
            embed.set_footer(text="I am as reliable as your subject reps, so rely on me at your own risk. I am a bot so I feel no guilt if you miss your homework.")
            await ctx.send(embed=embed)

    @commands.command(name="assign", pass_context=True, description="Date should be passed in the format DD/MM. Time should be passed in the format HH:MM in 24 hr format. The subjects are in short form (el, mt, em, am, chem, phy, ss, geog, comp, snw, others).\nYou can pass the flag -optional to mark the homework as optional.\nYou can add the flag -pt to mark the homework as pt-related.\nIf homework with the same name as another is assigned, the old homework is updated. Names are case-sensitive.")
    @is_rep()
    async def assign(self, ctx, subject : str, title : str, date : str, time : str, *args : str):
        """Adds homework to homework database."""
        t = time.split(":")
        if len(t) < 2: raise commands.errors.UserInputError
        d = date.split("/")
        if len(d) < 2: raise commands.errors.UserInputError
        if not (d[0].isnumeric() and d[1].isnumeric()): raise commands.errors.UserInputError
        if not subject in ["el", "mt", "em", "am", "chem", "phy", "ss", "geog", "comp", "snw", "other"]: raise commands.errors.UserInputError
        payload = {title: {
            "duedate" : datetime.datetime(year=datetime.datetime.now().year, month=int(d[1]), day=int(d[0]), hour=int(t[0]), minute=int(t[1])).timestamp(),
            "optional" : "-optional" in args,
            "pt" : "-pt" in args,
            "subject" : subject,
            "title" : title,
            "waiting" : [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
        }}
        requests.patch(f'https://joneechan-610b3.firebaseio.com/homework.json?auth={key}', data=json.dumps(payload))
        await ctx.message.delete()
        await ctx.send("Homework Assigned!")

    @commands.command(name="unassign", pass_context=True, description="Do note that the title name is case-sensitive!")
    @is_rep()
    async def unassign(self, ctx, title : str):
        """Deletes homework from homework database."""
        req = requests.get(f'https://joneechan-610b3.firebaseio.com/homework.json?auth={key}')
        j = json.loads(req.text)
        if j == None:
            await ctx.send("There are no homework assigned!")
            return
        if not title in j.keys():
            await ctx.send("No such homework was assigned.")
            return
        requests.delete(f'https://joneechan-610b3.firebaseio.com/homework/{title}.json?auth={key}')
        await ctx.message.delete()
        await ctx.send("Done")

    @commands.command(name="chase", pass_context=True, description="")
    async def chase(self, ctx, *args : str):
        """Prints the homework and people that have not handed up. WIP"""
        pass

    @commands.command(name="handup", pass_contect=True, description="")
    @is_rep()
    async def handup(self, ctx, *args : str):
        """Marks someone or a group of people as \"handed in\". WIP"""
        pass

def setup(bot):
    bot.add_cog(School(bot))