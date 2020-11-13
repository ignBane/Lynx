import requests, json, discord, datetime, asyncio
from discord.ext import commands
from discord.ext import tasks
from discord.utils import get

x = datetime.datetime.now()

with open('setup.json') as f:
    config = json.load(f)

if config['api-key'] == 'Fortnite API Key Here (If Not Leave Default)':
    apikey = False
else:
    apikey = True

bot = commands.Bot(command_prefix=config['prefix'])

@tasks.loop(seconds=10)
async def taskbrnews():
    with open('Saves/news.json', 'r') as file:
        old = json.load(file)
    if apikey == True:
        response=requests.get(
            'https://fortnite-api.com/v2/news/br',
            headers={"Authorization":config["api-key"]}
        ).json()
        if response != old:
            channel = bot.get_channel(config['news-channel'])
            embed=discord.Embed(
                title='Br News',
            )
            embed.set_image(url=response['data']['image'])
            await channel.send(embed=embed)
        with open('Saves/news.json', 'w') as file:
            json.dump(response, file, indent=3)
    else:
        response=requests.get('https://fortnite-api.com/v2/news/br').json()
        if response != old:
            channel = bot.get_channel(config['news-channel'])
            embed=discord.Embed(
                title='Br News',
            )
            embed.set_image(url=response['data']['image'])
            await channel.send(embed=embed)
        with open('Saves/news.json', 'w') as file:
            json.dump(response, file, indent=3)

@tasks.loop(seconds=10)
async def autoshopbr():
    with open('Saves/shop.json', 'r') as file:
        old = json.load(file)
    response=requests.get('https://api.peely.de/v1/shop').json()
    if response != old:
        channel = bot.get_channel(config['shop-channel'])
        await channel.send(response['time'])
        await channel.send(response['uniqueurl'])
    with open('Saves/shop.json', 'w') as file:
        json.dump(response, file, indent=3)

@tasks.loop(seconds=10)
async def autobuild():
    with open('Saves/build.json', 'r') as file:
        old = json.load(file)
    status=requests.get(
        'https://benbotfn.tk/api/v1/status'
    ).json()
    if status != old:
        await bot.change_presence(activity=discord.Game(name=f"{status['currentFortniteVersion']}"))
        response = requests.get(
            'https://benbotfn.tk/api/v1/aes'
        ).json()
        embed=discord.Embed(
            title="New Build Detected", 
            color=0xff0a0a
        )
        channel = bot.get_channel(config["build-channel"])
        pak = 0
        for sub_dict in response['dynamicKeys']:
            pak += 1
        embed.add_field(name=f"BuildVersion", value=f"{response['version']}", inline=True)
        if pak == 0:
            embed.add_field(name="Pak Files", value=f"Unkown", inline=True)
        else:
            embed.add_field(name="Pak Files", value=f"{pak}", inline=True)
        await channel.send(embed=embed)
    with open('Saves/build.json', 'w') as file:
        json.dump(status, file, indent=3)

@tasks.loop(seconds=10)
async def autotournament():
    try:
        with open('Saves/tournament.json', 'r') as file:
            Cached = json.load(file)
        data = requests.get(
            f'https://api.peely.de/v1/tournaments')
        new = data.json()
        if data.status_code != 200:
            return
    except:
        return
    if new["data"]["tournaments"] != Cached["data"]["tournaments"]:
        for i in new["data"]["tournaments"]:
            if i not in Cached["data"]["tournaments"]:
                name = i["name"]
                short_description = i["description"]
                image = i['image']
                try:
                    channel = bot.get_channel(config["tournamnet-channel"])
                    embed=discord.Embed(title=f'{name}', description=f'{short_description}')
                    embed.set_image(url=f'{image}')
                    await channel.send(embed=embed)
                except:
                    channel = bot.get_channel(config["tournamnet-channel"])
                    embed=discord.Embed(title=f'{name}', description=f'{short_description}')
                    embed.set_image(url=f'{image}')
                    await channel.send(embed=embed)
    with open('Saves/tournament.json', 'w') as file:
        json.dump(new, file, indent=3)
    
@tasks.loop(seconds=10)
async def autonotices():
    with open('Saves/notices.json', 'r') as file:
        old = json.load(file)
    response=requests.get(
        'https://api.peely.de/v1/notices'
    ).json()
    if response != old:
        if response['status'] == 200:
            for sub_dict in response['data']['messages']:
                channel = bot.get_channel(config['notices-channel'])
                embed=discord.Embed(title="Notice Changed ", color=0xff0000)
                embed.add_field(name=f"{sub_dict['title']}", value=f"{sub_dict['body']}", inline=True)
                await channel.send(embed=embed)
        else:
            channel = bot.get_channel(config['notices-channel'])
            embed=discord.Embed(title="Notice Changed", color=0xff0000)
            embed.add_field(name=f"???", value=f"???", inline=True)
            await channel.send(embed=embed)
    with open('Saves/notices.json', 'w') as file:
        json.dump(response, file, indent=3)

@bot.event
async def on_ready():
    print('Bot Ready/Logged In')
    status=requests.get(
        'https://benbotfn.tk/api/v1/status'
    ).json()
    await bot.change_presence(activity=discord.Game(name=f"{status['currentFortniteVersion']}"))
    taskbrnews.start()
    autoshopbr.start()
    autobuild.start()
    autotournament.start()
    autonotices.start()

@bot.command()
async def stats(ctx, arg):
  r = requests.get(f'https://fortnite-api.com/v1/stats/br/v2?name={arg}&image=all')
  rr = r.json()
  embed=discord.Embed()
  embed.set_image(url=f"{rr['data']['image']}")
  await ctx.send(embed=embed)

@bot.command()
async def brnews(ctx):
    response=requests.get(
        'https://fortnite-api.com/v2/news/br'
    ).json()
    embed=discord.Embed(
        title='Br News'
    )
    embed.set_image(
        url=response['data']['image']
    )
    await ctx.send(embed=embed)

@bot.command()
async def creativenews(ctx):
    response=requests.get(
        'https://fortnite-api.com/v2/news/creative'
    ).json()
    embed=discord.Embed(
        title='Creative News'
    )
    embed.set_image(
        url=response['data']['image']
    )
    await ctx.send(embed=embed)

@bot.command()
async def stwnews(ctx):
    response=requests.get(
        'https://api.peely.de/v1/stw/news'
    ).json()
    embed=discord.Embed(
        title='Save The World News'
    )
    embed.set_image(
        url=response['data']['image']
    )
    await ctx.send(embed=embed)

@bot.command()
async def search(ctx, cosnamee):
  r = requests.get(f'https://fortnite-api.com/v2/cosmetics/br/search/all?name={cosnamee}')
  rr = r.json()
  if rr['status'] == 200:
    for sub_dict in rr['data']:
      embed = discord.Embed(color=0x0d95fd)
      embed.add_field(name='Name', value=f"``{sub_dict['name']}``", inline=False)
      embed.add_field(name='ID', value=f"``{sub_dict['id']}``", inline=False)
      embed.add_field(name='Rarity', value=f"``{sub_dict['description']}``", inline=False)
      embed.add_field(name='Type', value=f"``{sub_dict['type']['value']}``", inline=False)
      embed.add_field(name='Display Type', value=f"``{sub_dict['type']['displayValue']}``", inline=False)
      embed.add_field(name='Backend Value', value=f"``{sub_dict['type']['backendValue']}``", inline=False)
      embed.add_field(name='Rarity', value=f"``{sub_dict['rarity']['value']}``", inline=False)
      embed.add_field(name='Backend Rarity', value=f"``{sub_dict['rarity']['backendValue']}``", inline=False)
      embed.add_field(name='Series', value=f"``{sub_dict['series']}``", inline=False)
      if sub_dict['introduction'] == None:
        pass
      else:
        embed.add_field(name='Introduction', value=f"``{sub_dict['introduction']['text']}``", inline=False)
        embed.add_field(name='Display Asset Path', value=f"``{sub_dict['displayAssetPath']}``", inline=False)
        embed.add_field(name='Definition Path', value=f"``{sub_dict['definitionPath']}``", inline=False)
        embed.set_thumbnail(url=f"https://fortnite-api.com/images/cosmetics/br/{sub_dict['id'].lower()}/icon.png")
        embed.set_footer(text=f"{bot.user.name} | Made By Bane#9999", icon_url='https://media.fortniteapi.io/images/9322d17f0c849c8d1859753ef237c669/transparent.png')
        message = await ctx.send(embed=embed)
  else:
    embed = discord.Embed(color=0xff0f0f)
    embed.add_field(name='Error', value=f"``{rr['error']}``", inline=False)
    embed.set_footer(text=f"{bot.user.name} | Made By Bane#9999", icon_url='https://media.fortniteapi.io/images/9322d17f0c849c8d1859753ef237c669/transparent.png')
    message = await ctx.send(embed=embed)
    await asyncio.sleep(60)
    await message.delete()

bot.run(config["token"], reconnect=True)