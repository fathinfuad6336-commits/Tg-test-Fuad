import asyncio
import os
from telethon import TelegramClient, events

# --- আপনার Credentials ---
API_ID = 26288557
API_HASH = 'f2c5cc7974b87a2ee5ee229b88dd20e5'
BOT_TOKEN = '8770799697:AAGPVMyZZSyVr4XVxDuCzzlm7164oAqGrM0'

bot = TelegramClient('bot_session_v2', API_ID, API_HASH)

user_states = {}

def get_sessions():
    """সব সেভ হওয়া সেশন ফাইল বের করার ফাংশন"""
    return [f for f in os.listdir('.') if f.endswith('.session')]

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    first_name = event.sender.first_name if event.sender else "User"
    msg = (
        f"👋 **হ্যালো {first_name}!**\n\n"
        "📊 /store : সামারি\n"
        "📊 /my_numbers : কান্ট্রি লিস্ট\n"
        "➕ /add_number : নম্বর যোগ করুন\n"
        "⚡ /terminate `[phone]` : সেশন ক্লিয়ার\n"
        "📤 /send `[phone]` `[ID]` : ট্রান্সফার\n"
    )
    await event.respond(msg)

async def main():
    # bot_token দিয়ে সার্ভিস স্টার্ট করা হচ্ছে
    await bot.start(bot_token=BOT_TOKEN)
    print("Bot is running...")
    await bot.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
