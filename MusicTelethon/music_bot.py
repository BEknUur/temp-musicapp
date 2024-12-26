import asyncio
import math
import os
import time
import aiofiles
import aiohttp
import wget
import aiohttp
from io import BytesIO
from traceback import format_exc
from pyrogram import Client, filters
from pyrogram.types import Message
from Python_ARQ import ARQ
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio, HighQualityVideo, LowQualityVideo, MediumQualityVideo
from youtubesearchpython import VideosSearch
from config import HNDLR, bot, call_py
from MusicTelethon.helpers.queues import QUEUE, add_to_queue, get_queue, clear_queue
from MusicTelethon.helpers.decorators import authorized_users_only
from MusicTelethon.helpers.handlers import skip_current_song, skip_item
from pyrogram.errors import FloodWait, MessageNotModified
from yt_dlp import YoutubeDL
from MusicTelethon.helpers.merrors import capture_err

ARQ_API_KEY = "QFOTZM-GSZUFY-CHGHRX-TDEHOZ-ARQ"
aiohttpsession = aiohttp.ClientSession()
arq = ARQ("https://thearq.tech", ARQ_API_KEY, aiohttpsession)

def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = f"https://i.ytimg.com/vi/{data['id']}/hqdefault.jpg"
        return [songname, url, duration, thumbnail]
    except Exception as e:
        print(e)
        return 0

async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp", "-g", "-f", "bestaudio", f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()

@Client.on_message(filters.command(["play"], prefixes=f"{HNDLR}"))
async def play(client, m: Message):
    replied = m.reply_to_message
    chat_id = m.chat.id
    if replied:
        if replied.audio or replied.voice:
            await m.delete()
            huehue = await replied.reply("**🔄 Processing and playing...**")
            dl = await replied.download()
            link = replied.link
            if replied.audio:
                songname = replied.audio.title[:35] + "..." if replied.audio.title else replied.audio.file_name[:35] + "..."
            elif replied.voice:
                songname = "Voice Note"
            if chat_id in QUEUE:
                add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await huehue.delete()
                await m.reply_photo(
                    photo="https://telegra.ph/file/40c0ab31719a780e37b5c.jpg",
                    caption=f"""
**‹ Title: [{songname}]({link})
‹ Chat ID: {chat_id}
‹ Requested by: {m.from_user.mention}**
""",
                )
            else:
                await call_py.join_group_call(
                    chat_id,
                    AudioPiped(dl),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await huehue.delete()
                await m.reply_photo(
                    photo="https://telegra.ph/file/40c0ab31719a780e37b5c.jpg",
                    caption=f"""
**‹ Title: [{songname}]({link})
‹ Chat ID: {chat_id}
‹ Requested by: {m.from_user.mention}**
""",
                )

@Client.on_message(filters.command(["skip"], prefixes=f"{HNDLR}"))
@authorized_users_only
async def skip(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if len(m.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await m.reply("**No songs in the queue to skip!**")
        elif op == 1:
            await m.reply("**Queue is empty, leaving the voice chat.**")
        else:
            await m.reply(
                f"**⏭ Skipped! Now playing:** [{op[0]}]({op[1]}) | `{op[2]}`",
                disable_web_page_preview=True,
            )

@Client.on_message(filters.command(["stop"], prefixes=f"{HNDLR}"))
@authorized_users_only
async def stop(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await m.reply("**Music playback stopped successfully.**")
        except Exception as e:
            await m.reply(f"**Error:**\n`{e}`")
    else:
        await m.reply("**No active playback!**")

@Client.on_message(filters.command(["pause"], prefixes=f"{HNDLR}"))
@authorized_users_only
async def pause(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await m.reply(
                f"**⏸ Playback paused.**\n\n• To resume, send `{HNDLR}resume`"
            )
        except Exception as e:
            await m.reply(f"**Error:**\n`{e}`")
    else:
        await m.reply("**No active playback to pause!**")

@Client.on_message(filters.command(["resume"], prefixes=f"{HNDLR}"))
@authorized_users_only
async def resume(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await m.reply("**▶ Playback resumed.**")
        except Exception as e:
            await m.reply(f"**Error:**\n`{e}`")
    else:
        await m.reply("**No paused playback to resume!**")
