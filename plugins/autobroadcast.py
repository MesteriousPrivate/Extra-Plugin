import asyncio
from datetime import datetime, timedelta
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters

from config import AUTO_GCAST, AUTO_GCAST_MSG, LOGGER_ID
from ChampuMusic import app
from ChampuMusic.utils.database import get_served_chats

# Convert AUTO_GCAST to boolean based on "On" or "Off"
AUTO_GCASTS = AUTO_GCAST.strip().lower() == "on"

START_IMG_URLS = "https://envs.sh/hUg.jpg"

MESSAGE = """**╭━━━〔 ✨ <b>𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐎𝐔𝐑 𝐁𝐎𝐓𝐒 𝐖𝐎𝐑𝐋𝐃!</b> ✨ 〕━━━╮

<b>🔮 ᴛᴀᴘ ᴛʜᴇ ʙᴜᴛᴛᴏɴꜱ ʙᴇʟᴏᴡ ᴛᴏ ᴇxᴘʟᴏʀᴇ:</b>

🎶 <b>ᴍᴜsɪᴄ𝟺ᴠᴄ</b> 🎶
  ├ 🎵 <b>ʜɪɢʜ ǫᴜᴀʟɪᴛʏ ᴠᴄ ᴘʟᴀʏ</b>
  ├ 🎼 <b>ʏᴏᴜᴛᴜʙᴇ, sᴘᴏᴛɪғʏ, ᴀᴘᴘʟᴇ ᴍᴜsɪᴄ</b>
  ├ 🔄 <b>𝟸𝟺/𝟳 ᴘʟᴀʏ & ᴀᴜᴛᴏ-ᴘʟᴀʏ</b>

🎼 <b>ᴀᴀᴅʜɪʀᴀ ᴍᴜsɪᴄ</b> 🎼
  ├ 🎥 <b>ᴀᴅᴠᴀɴᴄᴇᴅ ᴀᴜᴅɪᴏ/ᴠɪᴅᴇᴏ ᴘʟᴀʏᴇʀ</b>
  ├ 📻 <b>ʟɪᴠᴇ ʀᴀᴅɪᴏ & ᴅᴏᴡɴʟᴏᴀᴅ ᴏᴘᴛɪᴏɴ</b>

🤖 <b>ᴄʜᴀᴛ ʙᴏᴛ</b> 🤖
  ├ 🧠 <b>ᴀɪ-ᴘᴏᴡᴇʀᴇᴅ ᴄʜᴀᴛ ʙᴏᴛ</b>
  ├ 🎭 <b>ғᴜɴ, ǫᴜᴏᴛᴇs, ᴀᴜᴛᴏ ʀᴇᴘʟʏ</b>
  ├ 🔥 <b>𝟸𝟺/𝟳 ᴀᴄᴛɪᴠᴇ & sᴍᴀʀᴛ ᴀɪ</b>

🛠 <b>ʜᴇʟᴘ ʙᴏᴛ</b> 🛠
  ├ 📜 <b>ᴄᴏᴍᴍᴀɴᴅ ʜᴇʟᴘ, ᴜsᴇʀ ɢᴜɪᴅᴇs</b>
  ├ 🔧 <b>ᴀᴅᴍɪɴ ᴛᴀᴏʟs & sᴜᴘᴘᴏʀᴛ</b>

╰━━━━━━━━━━━━━━━━━━━━━━━⊷⊷**"""

BUTTON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "🎵 ᴍᴜsɪᴄ𝟺ᴠᴄ 🎵", url="https://t.me/Music4vcbot?start=_tgr_ImDrXR4xZGNl"
            ),
        ],
        [
            InlineKeyboardButton(
                "🎼 ᴀᴀᴅʜɪʀᴀ ᴍᴜsɪᴄ 🎼", url="https://t.me/TheAadhiraBot?start=_tgr_bed7dlNmNTBl"
            ),
            InlineKeyboardButton(
                "🤖 ᴄʜᴀᴛ ʙᴏᴛ 🤖", url="https://t.me/NYChatBot?start=_tgr_RsYGx-4xNmQ1"
            ),
        ],
        [
            InlineKeyboardButton(
                "🛠 ʜᴇʟᴘ ʙᴏᴛ 🛠", url="https://t.me/NYCREATION_BOT?start=_tgr__gObg3Y4ZmJl"
            ),
        ],
    ]
)

# Check if AUTO_GCASTS is enabled
async def send_text_once():
    try:
        await app.send_message(LOGGER_ID, MESSAGE)
    except Exception as e:
        pass

# Send broadcast message to all chats
async def send_message_to_chats():
    try:
        chats = await get_served_chats()
        for chat_info in chats:
            chat_id = chat_info.get("chat_id")
            if isinstance(chat_id, int):  # Check if chat_id is an integer
                try:
                    await app.send_photo(
                        chat_id,
                        photo=START_IMG_URLS,
                        caption=MESSAGE,
                        reply_markup=BUTTON,
                    )
                    await asyncio.sleep(20)  # Sleep for 20 seconds between sending messages
                except Exception as e:
                    pass
    except Exception as e:
        pass

# Scheduled broadcast every day at 2 PM
async def scheduled_broadcast():
    while True:
        now = datetime.now()
        # Wait until 2 PM the next day
        next_run = datetime.combine(now, datetime.min.time()) + timedelta(days=1, hours=14)
        wait_time = (next_run - now).total_seconds()
        await asyncio.sleep(wait_time)
        if AUTO_GCASTS:
            try:
                await send_message_to_chats()
            except Exception as e:
                pass

# Manual broadcast command handler
@app.on_message(filters.command('agcast') & filters.user(1786683163))
async def manual_broadcast(client, message):
    if AUTO_GCASTS:
        await send_message_to_chats()
        await message.reply("Manual broadcast sent!")

# Start the scheduled broadcast loop if AUTO_GCASTS is True
if AUTO_GCASTS:
    asyncio.create_task(scheduled_broadcast())

