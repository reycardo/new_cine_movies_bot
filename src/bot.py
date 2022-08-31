import os
import discord
from discord import Embed
from dotenv import load_dotenv
from scrap import Cine_Movies

load_dotenv()
TOKEN = os.getenv('TOKEN')



intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(intents=intents)


cine = Cine_Movies()

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    message_content = message.content.lower()  
    
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    
    if f'$cinema' in message_content:
        cinema = ' '.join(message_content.split()[1:])
        await message.channel.send(f'set cinema to: {cinema}')

    if f'$search' in message_content:
        key_words, search_words = cine.key_words_search_words(message_content)
        dates_hours,image = cine.search_film(key_words,cine='vasco da gama')                    
        embed = Embed()
        fields = [(f"**{key}**", f"{value}", False) for key, value in dates_hours.items()]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
            embed.set_author(name=f"{search_words}")
            embed.set_thumbnail(url=f"{image}")
        await message.channel.send(embed=embed)

bot.run(TOKEN)