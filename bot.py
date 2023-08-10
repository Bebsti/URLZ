import aiohttp
from pyrogram import Client, filters
import os

API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
API_KEY = os.environ.get('API_KEY', '')

bot = Client(
    'pdiskshortner bot',
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=50,
    sleep_threshold=10
)

@bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**Hi {message.chat.first_name}!**\n\n"
        "I'm URL Shortener Bot. Just send me a link and I'll provide you with a short link."
    )

@bot.on_message(filters.regex(r'https?://[^\s]+') & filters.private)
async def link_handler(bot, message):
    link = message.matches[0].group(0)
    try:
        short_link = await get_shortlink(link)
        await message.reply(
            f'Here is your [Short Link]({short_link})',
            quote=True,
            disable_web_page_preview=True
        )
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)

async def get_shortlink(link):
    url = 'https://cpm.link/api'
    params = {'api': API_KEY, 'url': link, 'alias': '', 'ct': 1}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, raise_for_status=True) as response:
            data = await response.json()
            return data["shortenedUrl"]

if __name__ == '__main__':
    bot.run()
