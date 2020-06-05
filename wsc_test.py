import socks
from telethon import TelegramClient


session_name = 'anon'
api_id = 876492
api_hash = '56e9d4797c57f43772f9d343e4499846'
client = TelegramClient(session_name, api_id, api_hash,
                        proxy=(socks.HTTP, '192.168.1.55', 4411))


async def get_message():
    username = 'NigeriaMMM'
    chat_item = await client.get_entity(username)
    print(chat_item)


with client:
    client.loop.run_until_complete(get_message())

