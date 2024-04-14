import discord
import os
from keep_alive import keep_alive

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print('ログインしました')

@client.event
async def on_message(message):
    if message.content.startswith("greet"):
        await message.channel.send("おはよう")

TOKEN = os.getenv("DISCORD_TOKEN")

keep_alive()
client.run(TOKEN)
