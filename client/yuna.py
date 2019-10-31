import discord
from discord.ext import commands
import os
from core import Code, afd, getFname

TOKEN = os.getenv('YUNA_TOKEN')
bot = commands.Bot(command_prefix='!')

@bot.command()
async def detect(ctx, *args):
    url = None
    if (len(ctx.message.attachments) > 0):
        url = ctx.message.attachments[0].url
    elif (len(args) > 0):
        url = args[0]
    else:
        return None
    await ctx.send(f'Observing at [{url}]...')

    result = afd(url)
    if (result == Code.EUPSTREAM):
        return await ctx.send(f'[{url}] is unsupported!')

    unknowns = 0
    total = len(result)
    file = None
    embed = None
    for item in result:
        if (item == Code.EUNCERTAIN):
            unknowns += 1
        elif (file is None):
            file = discord.File(item, filename=getFname(item))
            embed = discord.Embed(
                title=f'1st of {total}',
                type='rich',
                description=f'{unknowns} of {total} were low confidence'
            ).set_image(url=f'attachment://{getFname(item)}')

    if (file is None):
        return await ctx.send(f'Identified {total} results, of which {unknowns} were low confidence.')
    return await ctx.send(file=file, embed=embed)

bot.run(TOKEN)
