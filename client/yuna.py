import discord
from discord.ext import commands
import os
import requests
from PIL import Image

HOST = os.getenv('YUNA_HOST')
TOKEN = os.getenv('YUNA_TOKEN')
bot = commands.Bot(command_prefix='!')

def postDetect(url):
    req = requests.post(
        HOST + '/api/detect',
        json={'url': url}
    )
    if (req.status_code != 200):
        return None
    return req.json()

def getImage(path):
    dst = 'cache/' + path.split('/')[-1]
    req = requests.get(HOST + '/' + path)
    if (req.status_code != 200):
        return None
    with open(dst, 'wb') as f:
        f.write(req.content)
    return dst

def crop(path, bounds):
    img = Image.open(path)
    cimg = img.crop((bounds[0], bounds[1], bounds[2], bounds[3]))
    cimg.save(path)
    return path

@bot.command()
async def scan(ctx, *args):
    url = None
    if (len(ctx.message.attachments) > 0):
        url = ctx.message.attachments[0].url
    elif (len(args) > 0):
        url = args[0]
    else:
        return None
    await ctx.send('Okay, please be patient.')
    res = postDetect(url)
    if (res is None):
        return await ctx.send('Something broke.')
    # Only check the first face for now to avoid load balancing
    for path in res:
        for face in res[path]:
            if (face['score'] < 0.7):
                return await ctx.send('Over 30% uncertainty, dropping.')
            localPath = getImage(path)
            if (localPath is None):
                return await ctx.send('System missing original image.')
            croppedLocalPath = crop(localPath, face['bbox'])
            return await ctx.send(file=discord.File(croppedLocalPath))
    return await ctx.send('Found nothing of interest.')

bot.run(TOKEN)
