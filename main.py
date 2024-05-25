import discord
import os
from keep_alive import keep_alive
import urllib.parse
import random
import asyncio

import tinitu
import hangman
import maketen
import akinator
import picasso

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    hangman.init()
    maketen.init()
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
    # 10を作るゲーム
    elif message.content == "maketen":
        quiz, ans = maketen.generate_quiz()
        ans_choices = random.choices(ans, k=min(len(ans), 5))
        view = maketen.ArithmeticInputView(client, message.channel, quiz)
        await message.channel.send("__**10を作るゲーム**__\n四則演算と括弧を使って、次の数字から10を作ろう！\n- 使える記号は**+ - \\* / ( )**です\n- 割り算でも切り捨てなどを行わず、分数として扱います\n- 数字の順番は自由に入れ替えられます\n- 複数の数字を繋げて読んではいけません\n**" + " ".join(map(str, quiz)) + "**")
        await message.channel.send(view=view)
        def check(ans_message):
            if ans_message.channel != message.channel:
                return False
            arithmetic = ans_message.content.replace("\\*", "*")
            return maketen.check_format(arithmetic, quiz) and maketen.check_value(arithmetic)
        try:
            ans_message = await view.wait_correct_ans()
        except asyncio.TimeoutError:
            hint_message = "まだ分からない？しょうがないなあ...例えばこんな感じの式が作れるよ～"
            for ans_choice in ans_choices:
                hint = ""
                for c in ans_choice:
                    hint += "?" if "0" <= c <= "9" else c
                hint_message += "\n- " + hint
            await message.channel.send(hint_message)
            try:
                ans_message = await view.wait_correct_ans()
            except asyncio.TimeoutError:
                await message.channel.send("残念...時間切れだよ！\n例えばこんな式があるよ～" + "".join(["\n- " + ans_choice for ans_choice in ans_choices]))
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
