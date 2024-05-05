import discord
import requests
import re

class Akinator:
    def __init__(self):
        self.question = None
        self.step = None
        self.progression = None
        self.guessed = None
        self.guess_name = None
        self.guess_description = None
        self.guess_image = None
        self.uri = None
        self.language = None
        self.child_mode = None
        self.session = None
        self.signature = None
    
    def start_game(self, language=None, child_mode=False):
        self.language = language
        self.uri = f"https://{self.language}.akinator.com"
        self.child_mode = child_mode
        url = f"{self.uri}/game"
        json = {"sid": 1, "cm": str(self.child_mode).lower()}
        response = requests.post(url, json=json)
        match_session = re.search(r"session:\s*'(.+)'", response.text)
        match_signature = re.search(r"signature:\s*'(.+)'", response.text)
        if match_session is None or match_signature is None:
            raise Exception("failed to get session or signature")
        self.session = match_session.group(1)
        self.signature = match_signature.group(1)
        match_question = re.search(r"<p class=\"question-text\" id=\"question-label\">\s*(.+)\s*</p>", response.text)
        if match_question is None:
            raise Exception("failed to get question")
        self.question = match_question.group(1)
        # match_step = re.search(r"'step', '(.+)'", response.text)
        # match_progression = re.search(r"'progression', '(.+)'", response.text)
        # if match_step is None or match_progression is None:
        #     raise Exception("technical error has occured")
        # self.step = int(match_step.group(1))
        # self.progression = float(match_progression.group(1))
        self.step = 0
        self.progression = 0.0
        self.guessed = False
    
    def answer(self, ans):
        url = f"{self.uri}/answer"
        json = {"sid": 1, "cm": str(self.child_mode).lower(), "answer": ans, "step": self.step, "progression": self.progression, "session": self.session, "signature": self.signature}
        response = requests.post(url, json=json).json()
        if response["completion"] != "OK":
            raise Exception("technical error has occured")
        if "id_base_proposition" in response:
            self.guessed = True
            self.guess_name = response["name_proposition"]
            self.guess_description = response["description_proposition"]
            self.guess_image = response["photo"]
        else:
            self.question = response["question"]
            self.step = int(response["step"])
            self.progression = float(response["progression"])
    
    # def back(self):
    #     if self.step == 0:
    #         raise Exception("cannot go back any further")
    #     url = f"{self.uri}/cancel_answer"
    #     json = {"sid": 1, "cm": str(self.child_mode).lower(), "step": self.step, "progression": self.progression, "session": self.session, "signature": self.signature}
    #     response = requests.post(url, json=json).json()
    #     if response["completion"] != "OK":
    #         raise Exception("technical error has occured")
    #     self.question = response["question"]
    #     self.step = int(response["step"])
    #     self.progression = float(response["progression"])

class ChoicesView(discord.ui.View):
    def __init__(self, timeout=180):
        self.value = None
        super().__init__(timeout=timeout)
    
    @discord.ui.button(label="はい", style=discord.ButtonStyle.blurple)
    async def button_y(self, interaction, button: discord.Button):
        self.value = 0
        await interaction.response.send_message("はい")
        self.stop()
    
    @discord.ui.button(label="いいえ", style=discord.ButtonStyle.blurple)
    async def button_n(self, interaction, button: discord.Button):
        self.value = 1
        await interaction.response.send_message("いいえ")
        self.stop()
    
    @discord.ui.button(label="わからない", style=discord.ButtonStyle.blurple)
    async def button_idk(self, interaction, button: discord.Button):
        self.value = 2
        await interaction.response.send_message("わからない")
        self.stop()
    
    @discord.ui.button(label="たぶんそう 部分的にそう", style=discord.ButtonStyle.blurple)
    async def button_p(self, interaction, button: discord.Button):
        self.value = 3
        await interaction.response.send_message("たぶんそう 部分的にそう")
        self.stop()
    
    @discord.ui.button(label="たぶん違う そうでもない", style=discord.ButtonStyle.blurple)
    async def button_pn(self, interaction, button: discord.Button):
        self.value = 4
        await interaction.response.send_message("たぶん違う そうでもない")
        self.stop()

def float_to_hex(x):
    return min(max(round(x*256), 0), 255)

def float_to_color(x):
    x = min(max(x, 0.0), 1.0)
    if x < 1/6:
        r, g, b = 1.0, x*6, 0.0
    elif x < 2/6:
        r, g, b = 1.0-(x-1/6)*6, 1.0, 0.0
    elif x < 3/6:
        r, g, b = 0.0, 1.0, (x-2/6)*6
    elif x < 4/6:
        r, g, b = 0.0, 1.0-(x-3/6)*6, 1.0
    elif x < 5/6:
        r, g, b = (x-4/6)*6, 0.0, 1.0
    else:
        r, g, b = 1.0, 0.0, 1.0-(x-5/6)*6
    return float_to_hex(r)*0x10000 + float_to_hex(g)*0x100 + float_to_hex(b)

async def play(client, message):
    aki = Akinator()
    try:
        aki.start_game("jp")
    except Exception as e:
        await message.channel.send(e)
        return
    await message.channel.send("__**Akinator**__\nやあ、私はアキネイターです\n有名な人物やキャラクターを思い浮かべて。魔人が誰でも当ててみせよう。魔人は何でもお見通しさ")
    while not aki.guessed:
        embed = discord.Embed(title="質問"+str(aki.step+1), color=float_to_color(aki.progression/100))
        embed.add_field(name=aki.question, value="下のモーダルから答えてね")
        view = ChoicesView()
        await message.channel.send(embed=embed, view=view)
        await view.wait()
        try:
            aki.answer(view.value)
        except Exception as e:
            await message.channel.send(e)
            return
    guess_embed = discord.Embed(title="予想したのは...", color=float_to_color(aki.progression/100))
    guess_embed.add_field(name=aki.guess_name, value=aki.guess_description)
    guess_embed.set_image(url=aki.guess_image)
    await message.channel.send(embed=guess_embed)
