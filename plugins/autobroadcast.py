import asyncio
import datetime
import pytz
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import AUTO_GCAST, LOGGER_ID, API_ID, API_HASH, BOT_TOKEN
from ChampuMusic.utils.database import get_served_chats

# Bot Client
app = Client("BroadcastBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Configurations
AUTO_GCASTS = AUTO_GCAST.strip().lower() == "on"
OWNER_ID = 1786683163
CHANNEL_ID = -1002324275347  # Direct channel ID
FALLBACK_MESSAGE_ID = 14  # Manually defined message ID if fetching fails

def get_ist_time():
    """Fetch current IST time."""
    now_utc = datetime.datetime.now(pytz.utc)
    return now_utc.astimezone(pytz.timezone("Asia/Kolkata"))

async def fetch_last_post():
    """Fetch the last post, else fallback to a defined message."""
    try:
        messages = await app.search_messages(CHANNEL_ID, limit=1)
        if messages:
            return messages[0]  # Return the latest message
    except Exception as e:
        print(f"⚠️ Error fetching last post: {e}")
    
    # If fetch fails, return the fallback message
    try:
        return await app.get_messages(CHANNEL_ID, FALLBACK_MESSAGE_ID)
    except Exception as e:
        print(f"⚠️ Error fetching fallback message: {e}")
        return None

async def send_message_to_chats(message):
    """Send the given message to all served chats."""
    chats = await get_served_chats()
    count = 0
    for chat_info in chats:
        chat_id = chat_info.get("chat_id")
        if isinstance(chat_id, int):
            try:
                await message.copy(chat_id)
                count += 1
                await asyncio.sleep(10)  # Sleep to prevent flood limits
            except:
                pass  # Ignore errors
    return count

async def auto_broadcast():
    """Automatically broadcasts the last channel message daily at 2:00 PM IST."""
    while True:
        now_ist = get_ist_time()
        target_time = now_ist.replace(hour=14, minute=0, second=0, microsecond=0)
        if now_ist > target_time:
            target_time += datetime.timedelta(days=1)
        sleep_time = (target_time - now_ist).total_seconds()
        await asyncio.sleep(sleep_time)

        if AUTO_GCASTS:
            message = await fetch_last_post()
            if message:
                count = await send_message_to_chats(message)
                await app.send_message(OWNER_ID, f"✅ Auto Broadcast sent to {count} chats at 2:00 PM IST.")

@app.on_message(filters.command("autog") & filters.user(OWNER_ID))
async def manual_broadcast(_, message):
    """Allows the owner to manually trigger a broadcast with /autog."""
    await message.reply_text("⏳ Starting manual broadcast... Please wait.")
    
    msg = await fetch_last_post()
    if msg:
        count = await send_message_to_chats(msg)
        await message.reply_text(f"✅ Manual Broadcast Sent to {count} chats!")
    else:
        await message.reply_text("❌ No message found in the channel or fallback message!")

if AUTO_GCASTS:
    asyncio.create_task(auto_broadcast())

if __name__ == "__main__":
    app.run()
