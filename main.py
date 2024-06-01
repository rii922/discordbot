import discord
import os
from keep_alive import keep_alive
import urllib.parse
import random
import asyncio

import tinitu
import hangman
import akinator
import picasso

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    hangman.init()
    print("rii botが来たよ～")

@client.event
async def on_message(message):
    if message.author.bot:
        return
    # 数式を画像化
    if message.content.startswith("math "):
        tex = urllib.parse.quote(message.content[5:])
        url = "https://api.excelapi.org/math/tex2image?math=" + tex
        await message.channel.send(url)
    # 清一色何待ちクイズ
    elif message.content == "tinitu":
        await tinitu.play(client, message)
    # hangman
    elif message.content == "hangman":
        await hangman.play(client, message)
    # Akinator
    elif message.content == "akinator":
        await akinator.play(client, message)
    # AIアニメ画像生成
    elif message.content.startswith("picasso"):
        await picasso.play(client, message)
    # botを終了
    elif message.content == "exit":
        await message.channel.send("ばいばーい")
        exit()

TOKEN = os.getenv("DISCORD_TOKEN")

keep_alive()
client.run(TOKEN)
