import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

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

bot.command()
async def hello(ctx):
    await ctx.send("Hello!")

bot.run(PUBLIC_KEY)