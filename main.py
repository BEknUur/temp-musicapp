import asyncio
from pytgcalls import idle
from config import call_py
from MusicTelethon.play import arq

async def main():
    await call_py.start()
    print("""
    ------------------
   | Music Drox has started! |
    ------------------
    """)
    await idle()
    await arq.close()

loop = asyncio.get_event_loop()
loop
