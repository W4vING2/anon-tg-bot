from aiogram import Router
from aiogram.types import Message

from config import bot, active_chats
from keyboards import main_menu

router = Router()


@router.message()
async def relay_message(message: Message):
    user_id = message.from_user.id

    if user_id not in active_chats:
        await message.answer(
            "ℹ️ Ты не в чате. Нажми '🔗 Создать приглашение' чтобы начать.",
            reply_markup=main_menu
        )
        return

    partner_id = active_chats[user_id]

    try:
        if message.text:
            await bot.send_message(partner_id, message.text)
        elif message.photo:
            await bot.send_photo(partner_id, message.photo[-1].file_id, caption=message.caption)
        elif message.video:
            await bot.send_video(partner_id, message.video.file_id, caption=message.caption)
        elif message.voice:
            await bot.send_voice(partner_id, message.voice.file_id)
        elif message.video_note:
            await bot.send_video_note(partner_id, message.video_note.file_id)
        elif message.sticker:
            await bot.send_sticker(partner_id, message.sticker.file_id)
        elif message.document:
            await bot.send_document(partner_id, message.document.file_id, caption=message.caption)
        elif message.audio:
            await bot.send_audio(partner_id, message.audio.file_id, caption=message.caption)
        elif message.animation:
            await bot.send_animation(partner_id, message.animation.file_id, caption=message.caption)
        else:
            await message.answer("⚠️ Этот тип сообщения не поддерживается.")
    except Exception:
        await message.answer("❌ Не удалось отправить сообщение — возможно, собеседник заблокировал бота.")
