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
        "type": badge_type,
        "level": badge_level
    }
    data[user_key]["badges"].append(new_badge)

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

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
async def badge_completed(ctx, type: str, badgelevel:str):

    user = ctx.author

    sent_badge = False
    sent_level = False

    for badgetype in badge:
        if type == badgetype:
            sent_badge = True
            pass

    for leveltype in level:
        if badgelevel == leveltype:
            sent_level = True
            pass

    if sent_badge and sent_level:

        save_badge_data(user.id, str(user), type, badgelevel)
    
        await ctx.send(f'{type}  level {badgelevel}')
    else:
        await ctx.send("invalid command")

bot.run(DISCORD_TOKEN)