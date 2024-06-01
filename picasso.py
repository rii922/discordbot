import discord
from diffusers import StableDiffusionPipeline, EulerAncestralDiscreteScheduler
import torch
import spaces

model_id = "aipicasso/picasso-diffusion-1-1"
scheduler = EulerAncestralDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler")
pipe = StableDiffusionPipeline.from_pretrained(model_id, scheduler=scheduler)
pipe.to("cuda")

@spaces.GPU
def inference(prompt):
	prompt = "masterpiece, anime, " + prompt
	negative_prompt="lowres , kanji,  monochrome, ((bad anatomy)), ((bad hands)), text, missing finger, extra digits, fewer digits, blurry, ((mutated hands and fingers)), (poorly drawn face), ((mutation)), ((deformed face)), (ugly), ((bad proportions)), ((extra limbs)), extra face, (double head), (extra head), ((extra feet)), monster, logo, cropped, jpeg, humpbacked, long body, long neck, ((jpeg artifacts)), ((censored)), ((bad aesthetic))"
	return pipe(prompt, negative_prompt=negative_prompt).images

async def play(client, message):
    prompt = message.content[8:]
    image = inference(prompt)[0]
    image.save("picasso.png")
    await message.channel.send(file=discord.File("picasso.png"))
