import discord
import akinator

THRESHOLD = 80

def format_question(aki):
    return "**質問" + str(aki.step+1) + "**\n" + aki.question

class AnswerView(discord.ui.View):
    def __init__(self, aki, timeout=180):
        self.aki = aki
        super().__init__(timeout=timeout)
    
    async def update(self, interaction):
        await interaction.response.edit_message(format_question(self.aki))
        if self.aki.progression > THRESHOLD:
            guess = self.aki.win()
            await interaction.channel.send("思い浮かべているのは\n**" + guess["name"] + "**\n" + guess["description"] + "\n" + guess["absolute_picture_path"])

    @discord.ui.button(label="はい", style=discord.ButtonStyle.blurple)
    async def button_yes(self, interaction, button: discord.Button):
        self.aki.answer(0)
        await self.update(interaction)
    
    @discord.ui.button(label="いいえ", style=discord.ButtonStyle.blurple)
    async def button_no(self, interaction, button: discord.Button):
        self.aki.answer(1)
        await self.update(interaction)
    
    @discord.ui.button(label="分からない", style=discord.ButtonStyle.blurple)
    async def button_i_dont_know(self, interaction, button: discord.Button):
        self.aki.answer(2)
        await self.update(interaction)
    
    @discord.ui.button(label="たぶんそう部分的にそう", style=discord.ButtonStyle.blurple)
    async def button_probably(self, interaction, button: discord.Button):
        self.aki.answer(3)
        await self.update(interaction)
    
    @discord.ui.button(label="たぶん違う そうでもない", style=discord.ButtonStyle.blurple)
    async def button_yes(self, interaction, button: discord.Button):
        self.aki.answer(4)
        await self.update(interaction)
    
    @discord.ui.button(label="修正する", style=discord.ButtonStyle.gray)
    async def button_back(self, interaction, button: discord.Button):
        try:
            self.aki.back()
        except akinator.CantGoBackAnyFurther:
            pass
        await self.update(interaction)

async def play(client, message):
    abo = akinator.Akinator()
    abo.start_game()
    await message.channel.send("__**Akinator**__\nやあ、私はアキネイターです\n有名な人物やキャラクターを思い浮かべて。魔人が誰でも当ててみせよう。魔人は何でもお見通しさ")
    await message.channel.send(format_question(abo), view=AnswerView(abo, 180))
