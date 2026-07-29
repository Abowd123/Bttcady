###############################
# ███████╗░█████╗░██╗██████╗░ #
# ╚════██║██╔══██╗██║██╔══██╗ #
# ░░███╔═╝███████║██║██║░░██║ #
# ██╔══╝░░██╔══██║██║██║░░██║ #
# ███████╗██║░░██║██║██████╔╝ #
# ╚══════╝╚═╝░░╚═╝╚═╝╚═════╝░ #
##############################
#   https://t.me/m_f_u9      #
###############################
import asyncio
import redis.asyncio as redis
from pyrogram import Client, filters, idle
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from datetime import datetime, timedelta
from config import api_hash, api_id, redis_url, token

chats_db = {}
db = redis.Redis.from_url(redis_url, decode_responses=True)

DevZaid = Client(
    "cleaner",
    api_id,
    api_hash,
    bot_token=token,
    in_memory=True
)
ZAID = token.split(':')[0]


@DevZaid.on_message(filters.group & filters.media, group=1)
async def add_messages(c: Client, m: Message):
    chat_id = str(m.chat.id)
    if m.from_user:
        id = m.from_user.id
        mention = m.from_user.mention
    elif m.sender_chat:
        id = m.sender_chat.id
        mention = m.sender_chat.title
    
    if m.chat.id not in chats_db:
        chats_db[m.chat.id]=[]
    
    if (m.media) and not m.audio and not m.voice and not m.game:
        if await db.hget(ZAID+str(m.chat.id), "ena-clean"):
            secs = int(await db.hget(ZAID+chat_id, "clean-secs") or "60")
            time_now = datetime.now()
            data = {"id":m.id, "time":time_now + timedelta(seconds=secs)}
            chats_db[m.chat.id].append(data)
            
    
    if m.media_group_id and await db.hget(ZAID+str(m.chat.id), "ena-clean"):
        secs = int(await db.hget(ZAID+chat_id, "clean-secs") or "60")
        time_now = datetime.now()
        msgs = await c.get_media_group(m.chat.id, m.id)
        for msg in msgs:
            data = {"id":msg.id, "time":time_now + timedelta(seconds=secs)}
            chats_db[m.chat.id].append(data)
    
    # print(chats_db)

async def auto_clean_function():
    while True:
        await asyncio.sleep(1.7)
        now = datetime.now()
        for chat_id, messages in list(chats_db.items()):
            expired = [item["id"] for item in messages if now > item["time"]]
            chats_db[chat_id] = [item for item in messages if now <= item["time"]]
            if not expired:
                continue
            try:
                await DevZaid.delete_messages(chat_id, expired)
            except FloodWait as flood:
                await asyncio.sleep(flood.value)
            except Exception:
                continue

async def main():
    await DevZaid.start()
    print(DevZaid.me.username)
    cleaner_task = asyncio.create_task(auto_clean_function())
    try:
        await idle()
    finally:
        cleaner_task.cancel()
        await DevZaid.stop()
    
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())

