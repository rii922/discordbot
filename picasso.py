import discord
import spaces
from diffusers import DiffusionPipeline

pipe = DiffusionPipeline.from_pretrained("aipicasso/emi-2")
pipe.to("cuda")

@spaces.GPU
def inference(prompt):
    return pipe(prompt).images

async def play(client, message):
    prompt = message.content[8:]
    image = pipe(prompt).images[0]
    image.save("picasso.png")
    await message.channel.send(file=discord.File("picasso.png"))
