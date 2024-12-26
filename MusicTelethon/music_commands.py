import os
import sys
from datetime import datetime
from time import time
from pyrogram import Client, filters
from pyrogram.types import Message
from config import HNDLR, SUDO_USERS

START_TIME = datetime.utcnow()
TIME_DURATION_UNITS = (
    ("Weeks", 60 * 60 * 24 * 7),
    ("Days", 60 * 60 * 24),
    ("Hours", 60 * 60),
    ("Minutes", 60),
    ("Seconds", 1),
)

async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else ""))
    return ", ".join(parts)


@Client.on_message(filters.user(SUDO_USERS) & filters.command(["restart"], prefixes=f"{HNDLR}"))
async def restart(client, m: Message):
    await m.delete()
    loli = await m.reply("1")
    await loli.edit("2")
    await loli.edit("3")
    await loli.edit("4")
    await loli.edit("5")
    await loli.edit("6")
    await loli.edit("7")
    await loli.edit("8")
    await loli.edit("9")
    await loli.edit("**✅ Music Drox has been restarted successfully**")
    os.execl(sys.executable, sys.executable, *sys.argv)
    quit()

@Client.on_message(filters.command(["music_commands"], prefixes=f"{HNDLR}"))
async def help(client, m: Message):
    await m.delete()
    HELP = f"""
<b>‹ Hello {m.from_user.mention}!

𝘔𝘶𝘴𝘪𝘤 𝘛𝘦𝘭𝘦𝘵𝘩𝘰𝘯 𝘖𝘳𝘥𝘦𝘳𝘴
——————×—————

‹ To play an audio in call ⇦ [ `{HNDLR}play + song name` ]
‹ To play a video in call ⇦ [ `{HNDLR}play_video + song name` ]
———————×———————

‹ To pause the song or video ⇦ [ `{HNDLR}pause` ] 
‹ To resume the song ⇦ [ `{HNDLR}resume` ]
‹ To stop the song ⇦ [ `{HNDLR}stop` ] 
———————×———————

‹ To download an audio ⇦ [ `{HNDLR}download + song name or link` ]
‹ To download a video ⇦ [ `{HNDLR}download_video + song name or link` ]
———————×———————

‹ To restart the bot ⇦ [ `{HNDLR}restart` ]
———————×———————

‹ @DroxTeAm
‹ @P222P"""
    await m.reply(HELP)

@Client.on_message(filters.command(["repo"], prefixes=f"{HNDLR}"))
async def repo(client, m: Message):
    await m.delete()
    REPO = f"""
<b>‹ Hello {m.from_user.mention}!

‹ Source Channel: @DroxTeAm
‹ Developer: @P222P
"""
    await m.reply(REPO, disable_web_page_preview=True)
