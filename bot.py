import asyncio
import random
import interactions
from interactions import slash_command, SlashContext, listen, Intents, slash_option, OptionType, SlashCommandChoice

intents = Intents.ALL
client = interactions.Client(intents=intents,status=interactions.Status.ONLINE,activity=interactions.Activity(name="Yggdrasil sucks", type=interactions.ActivityType.GAME))
userphone = True

@interactions.listen()
async def on_startup():
    print("Bot is ready!")

@slash_command(name="my_command", description="My first command :)")
async def firstcommand(ctx: SlashContext):
    await ctx.send("Hello World")

@slash_command(name="randomnum", description="Generates a random number from a specified range")
@slash_option(
    name="minnum",
    description="Minimum number",
    required=True,
    opt_type=OptionType.INTEGER,
    min_value=0
)
@slash_option(
    name="maxnum",
    description="Maximun number",
    required=True,
    opt_type=OptionType.INTEGER,
)
async def randomnum(ctx: SlashContext, minnum: int, maxnum: int):
    if minnum < 0:
        await ctx.send("Error: Minimun number cannot be less than 0")
        return
    else:
        randomout = random.randrange(minnum, maxnum)
        await ctx.send(f"Your random number is: {randomout}")

@slash_command(name="toggleuserphone", description="Toggle the userphone timer")
@slash_option(
    name="toggle",
    description="Toggle the userphone timer On or Off",
    required=True,
    opt_type=OptionType.BOOLEAN,
    choices=[
        SlashCommandChoice(name="On", value=True),
        SlashCommandChoice(name="Off", value=False)
    ]
)
async def toggleuserphone(ctx: SlashContext, toggle: bool):
    global userphone
    if toggle == True: 
        userphone = True
        await ctx.send("Userphone timer is now turned On.")
    elif toggle == False:
        userphone = False
        await ctx.send("Userphone timer is now turned Off.")       


@listen()
async def on_message_create(event):
    if userphone == False:
        return
    else:
        if "You hung up the userphone" in event.message.content:
            emoji = '\N{HOURGLASS WITH FLOWING SAND}'
            await event.message.add_reaction(emoji)
            await asyncio.sleep(50)
            await event.message.reply('Ready to `--userphone` again!', mention_author=True)
            await event.message.remove_reaction(emoji,client.user)
        if "The other party hung up the userphone" in event.message.content:
            emoji = '\N{HOURGLASS WITH FLOWING SAND}'
            await event.message.add_reaction(emoji)
            await asyncio.sleep(5)
            await event.message.reply('Ready to `--userphone` again!', mention_author=True)
            await event.message.remove_reaction(emoji,client.user)

client.start("")
