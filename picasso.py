import discord
import os
import requests
import io
from PIL import Image

HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

def inference(prompt):
	url = "https://api-inference.huggingface.co/models/cagliostrolab/animagine-xl-3.1"
	header = { "Authorization": f"Bearer {HUGGINGFACE_TOKEN}" }
	payload = { "inputs": prompt }
	result = requests.post(url, headers=header, json=payload).content
	return result

async def play(client, message):
    prompt = message.content[8:]
    image = Image.open(io.BytesIO(inference(prompt)))
    bytesio = io.BytesIO()
    image.save(bytesio, format="png")
    bytesio.seek(0)
    await message.channel.send(file=discord.File(fp=bytesio, filename="picasso.png"))
