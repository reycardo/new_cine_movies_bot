import os
import discord
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
    
    if f'$search' in message_content:
        key_words, search_words = cine.key_words_search_words(message_content)
        result_links = cine.search_film(key_words)
        links = cine.send_link(result_links, search_words)

    if len(links) > 0:
        for link in links:
            await message.channel.send(link)
    else:
        await message.channel.send('rip')

bot.run(TOKEN)