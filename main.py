import discord
from discord.ext import commands
import os

TOKEN = os.getenv("DISCORD_BOT_TOKEN")  # Make sure it's set in your .env or hosting environment
RADIO_URL = "http://stream.radiojar.com/0tpy1h0kxtzuv"

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Load Opus (optional in some environments)
if not discord.opus.is_loaded():
    try:
        discord.opus.load_opus("libopus.so.0")
    except Exception as e:
        print(f"Failed to load opus: {e}")

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def join(ctx):
    """Bot joins your voice channel"""
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"✅ Joined {channel.name}")
    else:
        await ctx.send("❌ You must be in a voice channel first!")

@bot.command()
async def play(ctx):
    """Plays Quran radio"""
    if ctx.voice_client is None:
        await ctx.send("❌ Bot is not in a voice channel. Use `!join` first.")
        return

    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()

    ctx.voice_client.play(
        discord.FFmpegPCMAudio(RADIO_URL),
        after=lambda e: print("✅ Finished playing" if not e else f"Error: {e}")
    )
    await ctx.send("🎧 Playing Quran radio...")

@bot.command()
async def leave(ctx):
    """Bot leaves the voice channel"""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Left the voice channel.")
    else:
        await ctx.send("❌ I'm not in a voice channel.")

bot.run(TOKEN)
