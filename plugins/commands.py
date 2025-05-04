import asyncio
import base64
from pyrogram import Client, filters, __version__ as pyrogram_version
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait

from bot import Bot
from config import CHANNEL_ID, ADMINS, START_MSG, OWNER_ID

# 1. Start command
@Bot.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    text = message.text

    # Handle start parameter (e.g. /start encoded_string)
    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
            decoded = base64.b64decode(base64_string.encode("ascii")).decode("ascii")
            argument = decoded.split("-")
        except Exception:
            return

        try:
            if len(argument) == 3:  # Batch of messages
                start, end = int(argument[1]), int(argument[2])
                ids = range(start, end + 1) if start <= end else list(range(start, end - 1, -1))
            elif len(argument) == 2:  # Single message
                ids = [int(argument[1])]
            else:
                return
        except Exception:
            return

        try:
            msgs = await client.get_messages(chat_id=CHANNEL_ID, message_ids=ids)
        except Exception:
            await message.reply_text("Kuna shida..!", quote=True)
            return

        for msg in msgs:
            try:
                await msg.copy(chat_id=message.from_user.id)
                await asyncio.sleep(0.5)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await msg.copy(chat_id=message.from_user.id)
            except Exception:
                pass
        return

    # Show normal menu
    reply_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("😊 Kuhusu Mimi", callback_data="about"),
            InlineKeyboardButton("🔒 Funga", callback_data="close")
        ]
    ])
    await message.reply_text(
        text=START_MSG.format(firstname=message.chat.first_name),
        reply_markup=reply_markup,
        disable_web_page_preview=True,
        quote=True,
        parse_mode="HTML"
    )

# 2. Callback button handler
@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data

    if data == "about":
        await query.message.edit_text(
            text=(
                f"○ Mwenye: Huyu Mtu\n"
                f"○ Lugha: Python3\n"
                f"○ Maktaba: Pyrogram asyncio {pyrogram_version}\n"
                f"○ Chanzo: Bonyeza hapa\n"
                f"○ Kituo: @CodeXBotz\n"
                f"○ Kikundi cha Usaidizi: @CodeXBotzSupport"
            ),
            disable_web_page_preview=True,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔒 Funga", callback_data="close")]
            ])
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass

# 3. Post to channel
@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(["start", "batch"]))
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("Subiri kidogo...!", quote=True)

    try:
        post_message = await message.copy(chat_id=CHANNEL_ID, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id=CHANNEL_ID, disable_notification=True)
    except:
        await reply_text.edit_text("Kuna shida..!", quote=True)
        return

    encoded = base64.b64encode(f"get-{post_message.message_id}".encode("ascii")).decode("ascii")
    link = f"https://t.me/{client.username}?start={encoded}"

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔁 Shiriki URL", url=f'https://telegram.me/share/url?url={link}')]
    ])

    await reply_text.edit(
        f"<b>Hapa kuna kiungo chako</b>\n\n{link}",
        parse_mode="HTML",
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

# 4. Batch command
@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command("batch"))
async def batch(client: Client, message: Message):
    async def ask_forward(text_prompt):
        while True:
            try:
                msg = await client.ask(
                    text=text_prompt,
                    chat_id=message.from_user.id,
                    filters=filters.forwarded,
                    timeout=30
                )
                if msg.forward_from_chat and msg.forward_from_chat.id == CHANNEL_ID:
                    return msg.forward_from_message_id
                await msg.reply_text("Tuma kutoka kwenye Channel uliyobakiwa tu...", quote=True)
            except asyncio.TimeoutError:
                return None

    f_msg_id = await ask_forward("Tuma Ujumbe wa Kwanza kutoka Channel (kwa quotes)..")
    if not f_msg_id:
        return

    s_msg_id = await ask_forward("Tuma Ujumbe wa Mwisho kutoka Channel (kwa quotes)..")
    if not s_msg_id:
        return

    encoded = base64.b64encode(f"get-{f_msg_id}-{s_msg_id}".encode("ascii")).decode("ascii")
    link = f"https://t.me/{client.username}?start={encoded}"

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔁 Shiriki URL", url=f'https://telegram.me/share/url?url={link}')]
    ])

    await message.reply_text(
        f"<b>Hapa kuna kiungo chako</b>\n\n{link}",
        quote=True,
        parse_mode="HTML",
        reply_markup=reply_markup
    )
