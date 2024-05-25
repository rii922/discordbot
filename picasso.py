import discord
from diffusers import StableDiffusionXLPipeline, EulerAncestralDiscreteScheduler
import torch

model_id = "aipicasso/emi-2"

scheduler = EulerAncestralDiscreteScheduler.from_pretrained(model_id,subfolder="scheduler")
pipe = StableDiffusionXLPipeline.from_pretrained(model_id, scheduler=scheduler)
pipe = pipe.to("cpu")

# prompt = "1girl, upper body, brown bob short hair, brown eyes, looking at viewer, cherry blossom"
# images = pipe(prompt, num_inference_steps=20).images
# images[0].save("girl.png")

async def play(client, message):
    prompt = message.content[8:]
    image = pipe(prompt, num_inference_steps=20).images[0]
    image.save("picasso.png")
    await message.channel.send(file=discord.File("picasso.png"))