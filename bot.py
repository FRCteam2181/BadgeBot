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
async def badge_completed(ctx, badgetype: str, badgelevel:str):

    user = ctx.author

    if badgetype not in badge:
        await ctx.send("Invalid command")
        return

    if badgelevel not in level:
        await ctx.send("Invalid command")
        return

    repeatBadge = save_badge_data(user.id, str(user), badgetype, badgelevel)

    if repeatBadge == "new":
        await ctx.send(f'{badgetype}  level {badgelevel}')
    elif repeatBadge == "repeat":
        await ctx.send("Badge already earned.")

@bot.command()
async def badges(ctx):

    user = ctx.author
    user_key = str(user.id)

    #TODO: make it errors if the json doesnt exist, user not in list, no badges
    with open('badge_data.json', 'r') as f:
        data = json.load(f)

    if user_key in data:
        badges_completed = ""
        for badge in data[user_key]["badges"]:
            badges_completed += f"{badge["badge_type"]} {badge["level"]} \n"
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
        await ctx.send(badges_completed)

@bot.command()
async def remove_badge(ctx, badgetype: str, badgelevel: str):

    user = ctx.author
    user_key = str(user.id)

    #TODO: make it errors if the json doesnt exist, user not in list, no badges
    with open('badge_data.json', 'r') as f:
        data = json.load(f)

    badge_to_remove = {
        "badge_type": badgetype,
        "level": badgelevel
    }

    if badge_to_remove in data[user_key]["badges"]:
        data[user_key]["badges"].remove(badge_to_remove)
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
        await ctx.send("Badge Removed")




bot.run(DISCORD_TOKEN)