import asyncio
import os
from telethon import TelegramClient, events, Button
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

# বাটন লেআউট
def get_main_buttons():
    return [
        [Button.inline("📊 Store Summary", data="btn_store"), Button.inline("📊 Country List", data="btn_numbers")],
        [Button.inline("➕ Add Number", data="btn_add")],
        [Button.inline("⚡ Terminate Session", data="btn_term"), Button.inline("📤 Send Transfer", data="btn_send")]
    ]

# /start কমান্ড হ্যান্ডলার
@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    first_name = event.sender.first_name if event.sender else "User"
    text = (
        f"👋 **হ্যালো {first_name}!**\n\n"
        "নিচের বাটনগুলো ব্যবহার করে কাজ করুন:"
    )
    await event.respond(text, buttons=get_main_buttons())

# বাটন ক্লিক করার পর মেসেজ আপডেট বা নতুন বাটন দেখানোর হ্যান্ডলার
@bot.on(events.CallbackQuery)
async def callback_handler(event):
    data = event.data.decode('utf-8')
    
    if data == "btn_store":
        await event.edit("📊 **Store Summary:**\nবর্তমানে কোনো ডেটা জমা নেই।", buttons=get_main_buttons())
    elif data == "btn_numbers":
        await event.edit("📊 **Country List:**\nআপনার সেভ করা কোনো নম্বর পাওয়া যায়নি।", buttons=get_main_buttons())
    elif data == "btn_add":
        await event.edit("➕ **Add Number:**\nদেশের কোডসহ ফোন নম্বর পাঠান। (যেমন: +88017...)", buttons=get_main_buttons())
    elif data == "btn_term":
        await event.edit("⚡ **Terminate Session:**\nসেশন ক্লিয়ার করার জন্য `/terminate [phone]` লিখুন।", buttons=get_main_buttons())
    elif data == "btn_send":
        await event.edit("📤 **Send Transfer:**\nট্রান্সফার করতে `/send [phone] [ID]` লিখুন।", buttons=get_main_buttons())

# মেসেজ টেক্সট কমান্ডের ব্যাকআপ
@bot.on(events.NewMessage(pattern='/store'))
async def store_handler(event):
    await event.respond("📊 **Store Summary:**\nবর্তমানে কোনো ডেটা জমা নেই।", buttons=get_main_buttons())

@bot.on(events.NewMessage(pattern='/my_numbers'))
async def numbers_handler(event):
    await event.respond("📊 **Country List:**\nআপনার সেভ করা কোনো নম্বর পাওয়া যায়নি।", buttons=get_main_buttons())

@bot.on(events.NewMessage(pattern='/add_number'))
async def add_number_handler(event):
    await event.respond("➕ নম্বর যোগ করতে দেশের কোডসহ ফোন নম্বর পাঠান।", buttons=get_main_buttons())

async def main():
    threading.Thread(target=run_http_server, daemon=True).start()
    await bot.start(bot_token=BOT_TOKEN)
    print("Bot is running...")
    await bot.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
