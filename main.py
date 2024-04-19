import discord
import os
from keep_alive import keep_alive
import urllib.parse
import random
import asyncio
import tinitu
import hangman

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
        hand, ans = tinitu.generate_quiz()
        hand_list = []
        for i in range(9):
            hand_list += ["**" + str(i+1) + "**" for _ in range(hand[i])]
        hand_str = " ".join(hand_list)
        random.shuffle(hand_list)
        hand_str_shuffled = " ".join(hand_list)
        ans_list = ["**" + str(wait+1) + "**" for wait in ans]
        ans_list.sort()
        await message.channel.send("__**清一色何待ちクイズ**__\nこの清一色、何待ち？\n" + hand_str_shuffled)
        def check(ans_message):
            if ans_message.channel != message.channel:
                return False
            user_ans = set()
            for i in range(9):
                if str(i+1) in ans_message.content:
                    user_ans.add(i)
            return user_ans == ans
        async def send_correct_message(ans_message):
            await ans_message.channel.send(ans_message.author.mention + "正解！(" + ", ".join(ans_list) + "待ち)")
            await ans_message.add_reaction("👍")
        try:
            ans_message = await client.wait_for("message", check=check, timeout=30)
            await send_correct_message(ans_message)
        except asyncio.TimeoutError:
            await message.channel.send("分からない？...じゃあ理牌してあげる～\n" + hand_str)
            try:
                ans_message = await client.wait_for("message", check=check, timeout=30)
                await send_correct_message(ans_message)
            except asyncio.TimeoutError:
                await message.channel.send("まだ分からない？仕方がないなあ...この待ちは**" + str(len(ans)) + "**種あるよ～")
                try:
                    ans_message = await client.wait_for("message", check=check, timeout=30)
                    await send_correct_message(ans_message)
                except asyncio.TimeoutError:
                    await message.channel.send("正解は" + ", ".join(ans_list) + "待ちでした！難しかったかな？")
    # hangman
    elif message.content == "hangman":
        word = hangman.choose_word()
        life = len(word)
        opened = [False for _ in range(len(word))]
        chars = []
        await message.channel.send("__**hangman**__\nアルファベット1文字または予想する単語を答えてね")
        def check(ans_message):
            if ans_message.channel != message.channel:
                return False
            for c in ans_message.content:
                if not ("a" <= c <= "z" or "A" <= c <= "Z"):
                    return False
            return True
        while life > 0:
            await message.channel.send(" ".join([(word[i] if opened[i] else "\\_") for i in range(len(word))]) + "\n残機: " + str(life) + "\n使った文字: " + " ".join(chars))
            try:
                ans_message = await client.wait_for("message", check=check, timeout=180)
                if len(ans_message.content) == 1:
                    chars.append(ans_message.content)
                    for i in range(len(word)):
                        if word[i] == ans_message.content:
                            opened[i] = True
                    if not ans_message.content in word:
                        life -= 1
                else:
                    predict = ans_message.content.lower()
                    if predict == word:
                        await message.channel.send(ans_message.author.mention + "正解！")
                        await ans_message.add_reaction("👍")
                        break
                    else:
                        life -= 1
            except asyncio.TimeoutError:
                await message.channel.send("3分間無言だったので終了するよ\n正解は" + word + "でした！")
                break
        if life == 0:
            await message.channel.send("正解は" + word + "でした！")
    # botを終了
    elif message.content == "exit":
        await message.channel.send("ばいばーい")
        exit()

TOKEN = os.getenv("DISCORD_TOKEN")

keep_alive()
client.run(TOKEN)
