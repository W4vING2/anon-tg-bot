import uuid

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.utils.deep_linking import create_start_link

from config import bot, pending_invites, active_chats
from keyboards import main_menu, INFO_TEXT

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, command: CommandStart):
    user_id = message.from_user.id
    args = command.args

    if args:
        invite_code = args

        if invite_code not in pending_invites:
            await message.answer("❌ Приглашение недействительно или уже использовано.", reply_markup=main_menu)
            return

        inviter_id = pending_invites[invite_code]

        if inviter_id == user_id:
            await message.answer("❌ Нельзя начать чат с самим собой.", reply_markup=main_menu)
            return

        if user_id in active_chats:
            await message.answer("⚠️ Ты уже в активном чате. Нажми '🔴 Завершить чат' чтобы выйти.", reply_markup=main_menu)
            return

        if inviter_id in active_chats:
            await message.answer("❌ Пользователь уже в другом чате.", reply_markup=main_menu)
            del pending_invites[invite_code]
            return

        del pending_invites[invite_code]
        active_chats[user_id] = inviter_id
        active_chats[inviter_id] = user_id

        await message.answer(
            "✅ Анонимный чат начат!\n"
            "Пиши сообщения — собеседник получит их без твоего имени.\n"
            "Нажми '🔴 Завершить чат' чтобы выйти.",
            reply_markup=main_menu
        )
        await bot.send_message(
            inviter_id,
            "✅ Собеседник принял приглашение! Чат начат.\n"
            "Нажми '🔴 Завершить чат' чтобы выйти."
        )
        return

    await message.answer(
        "👋 Привет! Я бот анонимного чата.\n"
        "Нажми кнопку ниже чтобы создать приглашение для друга.",
        reply_markup=main_menu
    )


@router.message(Command("invite"))
@router.message(lambda m: m.text == "🔗 Создать приглашение")
async def cmd_invite(message: Message):
    user_id = message.from_user.id

    if user_id in active_chats:
        await message.answer("⚠️ Ты уже в активном чате. Нажми '🔴 Завершить чат' чтобы выйти.", reply_markup=main_menu)
        return

    invite_code = str(uuid.uuid4())[:10]
    pending_invites[invite_code] = user_id
    link = await create_start_link(bot, invite_code)

    await message.answer(
        f"🔗 Отправь эту ссылку другу:\n{link}\n\n"
        "Когда он перейдёт по ней — чат начнётся автоматически.\n"
        "Никто из вас не увидит имя или юзернейм другого. 🔒",
        reply_markup=main_menu
    )


@router.message(Command("stop"))
@router.message(lambda m: m.text == "🔴 Завершить чат")
async def cmd_stop(message: Message):
    user_id = message.from_user.id

    if user_id not in active_chats:
        await message.answer("ℹ️ Ты не в активном чате.", reply_markup=main_menu)
        return

    partner_id = active_chats.pop(user_id)
    active_chats.pop(partner_id, None)

    await message.answer("🔴 Чат завершён.", reply_markup=main_menu)
    try:
        await bot.send_message(partner_id, "🔴 Собеседник завершил чат.")
    except Exception:
        pass


@router.message(lambda m: m.text == "ℹ️ О боте")
async def btn_info(message: Message):
    await message.answer(INFO_TEXT, parse_mode="HTML", reply_markup=main_menu)
