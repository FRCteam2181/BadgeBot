import os
import discord
import json
from discord.ext import commands
from dotenv import load_dotenv

badge = ["Basic", "Hours", "Events", "Leadership", "CAD", "Build", "Electrical", "Programming", "Business", "Safety/FMEA", "Scouting/Strategy", "Media"]
level = ["1", "2", "3", "4"]

DATA_FILE = "badge_data.json"

def save_badge_data(user_id, username, badge_type, badge_level ):

    data = {}

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}

    user_key = str(user_id)

    if user_key not in data:
        data[user_key] = {
            "username": username,
            "badges": []
        }

    new_badge = {
        "badge_type": badge_type,
        "level": badge_level
    }

    if new_badge not in data[user_key]["badges"]:
        data[user_key]["badges"].append(new_badge)
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
        return "new"
    return "repeat"



load_dotenv()

APP_ID = os.getenv("APP_ID")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
PUBLIC_KEY = os.getenv("PUBLIC_KEY")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print("Bot is ready!")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")

@bot.command()
async def info(ctx):
    await ctx.send(
        "**Badges available:** Basic, Hours, Events, Leadership, CAD, Build, Electrical, Programming, Business, Safety/FMEA, Scouting/Strategy \n" \
        "**Levels available:** 1,2,3,4 \n" \
        "\n" \
        "For each command the [@user] is optional, if not done will apply the command to yourself.\n" 
        "The [badge] and [level] are not. \n" \
        "\n" \
        "!info ----------------------------------------- Gives list of commands and badges \n" \
        "!badges [@user] ------------------------------- See list of badges \n" \
        "!badge_completed [badge] [level] [@user] ------ Add a badge to a user \n" \
        "!remove_badge [badge] [level] [@user] --------- Reove a badge from a user \n"
    )

@bot.command()
async def badges(ctx, member: discord.Member = None):

    if member == None:
        member = ctx.author
    member_key = str(member.id)

    #TODO: make it errors if the json doesnt exist
    if os.path.isfile("badge_data.json"):
        with open('badge_data.json', 'r') as f:
            data = json.load(f)

        if member_key in data:
            if data[member_key]["badges"]:
                badges_completed = ""
                for badge in data[member_key]["badges"]:
                    badges_completed += f"{badge["badge_type"]} {badge["level"]} \n"
                await ctx.send(badges_completed)
            else:
                await ctx.send(f'{member.name} does not have any badges, please log a badge.')
        else:
            await ctx.send(f'{member.name} does not have nay badges, please log a badge first.')
    else:
        await ctx.send('No json file exist for badges, please add a badge first.')

@bot.command()
async def badge_completed(ctx, badgetype: str, badgelevel:str, member: discord.Member = None):

    if member is None:
        member = ctx.author

    if badgetype not in badge:
        await ctx.send("Invalid command")
        return

    if badgelevel not in level:
        await ctx.send("Invalid command")
        return

    repeatBadge = save_badge_data(member.id, str(member), badgetype, badgelevel)

    if repeatBadge == "new":
        await ctx.send(f'{member.name} has earned {badgetype}  level {badgelevel}.')
    elif repeatBadge == "repeat":
        await ctx.send(f"{member.name} has already earned {badgetype} level {badgelevel}.")

@bot.command()
async def remove_badge(ctx, badgetype: str, badgelevel: str, member: discord.Member = None):

    if member == None:
        member = ctx.author
    member_key = str(member.id)

    if os.path.isfile('badge_data.json'):
        with open('badge_data.json', 'r') as f:
            data = json.load(f)

        badge_to_remove = {
            "badge_type": badgetype,
            "level": badgelevel
        }
        if member_key in data:
            if badge_to_remove in data[member_key]["badges"]:
                data[member_key]["badges"].remove(badge_to_remove)
                with open(DATA_FILE, "w") as f:
                    json.dump(data, f, indent=4)
                await ctx.send("Badge Removed")
            else:
                await ctx.send(f"{member} does not have {badgetype} level {badgelevel}.")
        else:
            await ctx.send('User not in list, please add a badge to the user first')
    else:
        await ctx.send('No json file exist for badges, please add a badge first.')

bot.run(DISCORD_TOKEN)