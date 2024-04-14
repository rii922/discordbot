import discord
import os
from keep_alive import keep_alive
from sympy import *

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
	print('ログインしました')

@client.event
async def on_message(message):
	if (message.content[:4] == "math"):
		sympy.preview(message.content[4:], viewer="file", filename="math.png")
		await message.channel.send(file=discord.File("math.png"))

TOKEN = os.getenv("DISCORD_TOKEN")

keep_alive()
client.run(TOKEN)
