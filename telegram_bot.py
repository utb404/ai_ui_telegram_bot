import asyncio

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, ConversationHandler
import os
import json
import re

from ai_agent import ai_generate
from prompt_generator import form_prompt

CHOOSING_TYPE, CHOOSING_ARTIFACT = range(2)

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

ARTIFACT_DIRS = {
    'test_case': 'test_cases',
}

def escape_markdown_v2(text: str) -> str:
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(r'([{}])'.format(re.escape(escape_chars)), r'\\\1', text)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    buttons = [
        [InlineKeyboardButton(text=key, callback_data=key)]
        for key in ARTIFACT_DIRS.keys()
    ]
    await update.message.reply_text(
        'Привет! Выбери тип артефакта, который хочешь получить:'
    )
    await update.message.reply_text(
        'Выберите тип артефакта:',
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    return CHOOSING_TYPE

async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    buttons = [
        [InlineKeyboardButton(text=key, callback_data=key)]
        for key in ARTIFACT_DIRS.keys()
    ]
    await update.message.reply_text(
        'Привет! Выбери тест-кейс, который хочешь покрыть автотестами:'
    )
    await update.message.reply_text(
        'Выберите тест-кейс:',
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    return CHOOSING_TYPE


async def choosing_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    artifact_type = query.data
    context.user_data['artifact_type'] = artifact_type

    artifact_path = ARTIFACT_DIRS.get(artifact_type)

    if not artifact_path or not os.path.exists(artifact_path):
        await query.edit_message_text(f'Артефакты для типа {artifact_type} не найдены.')
        return ConversationHandler.END

    files = [f[:-5] for f in os.listdir(artifact_path) if f.endswith('.json')]
    if not files:
        await query.edit_message_text(f'В папке {artifact_path} нет артефактов.')
        return ConversationHandler.END

    buttons = [
        [InlineKeyboardButton(text=file_id, callback_data=file_id)]
        for file_id in files
    ]
    await query.edit_message_text(
        f'Выбери ID артефакта типа {artifact_type}:',
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    return CHOOSING_ARTIFACT

async def choosing_artifact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    artifact_type = context.user_data.get('artifact_type')
    artifact_id = query.data
    artifact_path = ARTIFACT_DIRS[artifact_type]
    file_path = os.path.join(artifact_path, f'{artifact_id}.json')

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        text = json.dumps(data, ensure_ascii=False, indent=2)
        text = escape_markdown_v2(text)
        await query.edit_message_text(f"Артефакт {artifact_id}:\n{json.dumps(data, ensure_ascii=False, indent=2)}")
    except Exception as e:
        await query.edit_message_text(f'Ошибка при чтении файла: {e}')

    return ConversationHandler.END


async def choosing_test_case(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    artifact_type = "test_case"
    artifact_id = query.data
    artifact_path = ARTIFACT_DIRS[artifact_type]
    file_path = os.path.join(artifact_path, f'{artifact_id}.json')
    test_case = ""

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        test_case = json.dumps(data, ensure_ascii=False, indent=2)
    except Exception as e:
        await query.edit_message_text(f'Ошибка при чтении файла: {e}')

    prompt = form_prompt(test_case)
    gen_result = await ai_generate(prompt)

    # Telegram ограничивает длину текста сообщения ~4096 символами
    max_len = 4000
    if len(gen_result) <= max_len:
        await query.edit_message_text(gen_result)
    else:
        await query.edit_message_text('Результат большой, отправляю частями...')
        chat_id = getattr(query.message, 'chat_id', None) or query.message.chat.id
        for i in range(0, len(gen_result), max_len):
            part = gen_result[i:i+max_len]
            await context.bot.send_message(chat_id=chat_id, text=part)

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Операция отменена.')
    return ConversationHandler.END

def main():
    token = TELEGRAM_BOT_TOKEN

    application = ApplicationBuilder().token(token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING_TYPE: [CallbackQueryHandler(choosing_type)],
            CHOOSING_ARTIFACT: [CallbackQueryHandler(choosing_artifact)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(conv_handler)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('generate', generate)],
        states={
            CHOOSING_TYPE: [CallbackQueryHandler(choosing_type)],
            CHOOSING_ARTIFACT: [CallbackQueryHandler(choosing_test_case)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(conv_handler)

    print("Бот запущен...")
    application.run_polling()

if __name__ == '__main__':
    main()
