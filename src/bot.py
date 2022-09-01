import os
import discord
from discord import Embed
from dotenv import load_dotenv
from scrap import Cine_Scraper

load_dotenv()
TOKEN = os.getenv('TOKEN')


# message content intent is being enforced
intents = discord.Intents.default()
intents.message_content = True

# Init bot with intents
bot = discord.Bot(intents=intents)

# Init scraper
scraper = Cine_Scraper()

# So we know the bot is ready
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.event
async def on_message(message):
    
    # so bot isn't listening to himself
    if message.author == bot.user:
        return            
    
    # responds with Hello! to a $hello
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    
    # searches for the days/hours the movie in message will screen in cinema
    if message.content.startswith('$search'):    
        cinema = 'vasco da gama'
        key_words, search_words = scraper.key_words_search_words(message.content)
        dates_hours,image = scraper.search_film(key_words,cine=cinema)
        embed = Embed()
        fields = [(f"**{key}**", f"{value}", False) for key, value in dates_hours.items()]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
            embed.set_author(name=f"{search_words} @ {cinema.title()}")
            embed.set_thumbnail(url=f"{image}")
        await message.channel.send(embed=embed)

bot.run(TOKEN)