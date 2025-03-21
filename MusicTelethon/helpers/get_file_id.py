from pyrogram.types import Message
def get_file_id(msg: Message):
    if msg.media:
        for message_type in ("photo","animation","audio","document",   "video",  "video_note",  "voice",  "contact", "dice","poll",  "location", "venue", "sticker"):
            obj = getattr(msg, message_type)
            if obj:
                setattr(obj, "message_type", message_type)
                return obj
