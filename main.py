import discord
import os
from keep_alive import keep_alive
import urllib.parse
import random
import asyncio
import tinitu

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('ログインしました')

@client.event
async def on_message(message):
    # 数式を画像化
    if message.content.startswith("math "):
        tex = urllib.parse.quote(message.content[5:])
        url = "https://api.excelapi.org/math/tex2image?math=" + tex
        await message.channel.send(url)
    # チンイツ待ちクイズ
    elif message.content == "tinitu":
        tinitu_correct = False
        hand, ans = tinitu.generate_quiz()
        hand_str = ""
        for i in range(9):
            hand_str += str(i+1)*hand[i]
        hand_str_shuffled = hand_str[:]
        random.shuffle(hand_str_shuffled)
        await message.channel.send("このチンイツ、何待ち？\n" + hand_str_shuffled)
        def check(ans_message):
            if ans_message.channel != message.channel:
                return False
            user_ans = set()
            for i in range(9):
                if str(i+1) in ans_message:
                    user_ans.add(i)
            return user_ans == ans
        async def send_correct_message(ans_message):
            await message.channel.send(ans_message.author.mention + "正解！")
        try:
            ans_message = await client.wait_for("message", check=check, timeout=30)
        except asyncio.TimeoutError:
            await message.channel.send("分からない？...じゃあ理牌してあげるよ！\n" + hand_str)
            try:
                ans_message = await client.wait_for("message", check=check, timeout=30)
            except asyncio.TimeoutError:
                await message.channel.send("正解は" + ", ".join(ans) + "待ちでした！難しかったかな？")
            else:
                send_correct_message(ans_message)
        else:
            send_correct_message(ans_message)
    # botを終了
    elif message.content == "exit":
        await message.channel.send("ばいばーい")
        exit()

TOKEN = os.getenv("DISCORD_TOKEN")

keep_alive()
client.run(TOKEN)
