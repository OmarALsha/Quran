import os
import discord
from discord.ext import commands

# Load environment variables
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
VC_CHANNEL_ID = int(os.getenv("VC_CHANNEL_ID"))

# Check Opus
if not discord.opus.is_loaded():
    discord.opus.load_opus("libopus.so.0")

# Intents
intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

    guild = bot.get_guild(GUILD_ID)
    if not guild:
        print("❌ Guild not found.")
        return

    channel = guild.get_channel(VC_CHANNEL_ID)
    if not channel or not isinstance(channel, discord.VoiceChannel):
        print("❌ Voice channel not found or invalid.")
        return

    vc = await channel.connect()
    vc.play(
        discord.FFmpegPCMAudio("http://stream.radiojar.com/0tpy1h0kxtzuv"),
        after=lambda e: print("✅ Finished playing.")
    )
    print("🎧 Playing Quran radio...")

bot.run(TOKEN)
