import asyncio
import os
from telethon import TelegramClient, events
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# --- ডামি HTTP সার্ভার (Render Port Error দূর করতে) ---
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is active!")

def run_http_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), DummyHandler)
    server.serve_forever()

# --- Credentials ---
API_ID = 26288557
API_HASH = 'f2c5cc7974b87a2ee5ee229b88dd20e5'
BOT_TOKEN = '8770799697:AAGPVMyZZSyVr4XVxDuCzzlm7164oAqGrM0'

bot = TelegramClient('bot_session_v2', API_ID, API_HASH)

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
    threading.Thread(target=run_http_server, daemon=True).start()
    await bot.start(bot_token=BOT_TOKEN)
    print("Bot is running...")
    await bot.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
