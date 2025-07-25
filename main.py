import asyncio
import nest_asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    filters,
)
from gpt import ask_gpt

nest_asyncio.apply()

BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

GET_BIRTHDATA = 1
user_data = {}

main_menu_keyboard = [
    ["🎁 Получить подарок от звёзд"],
    ["🌟 Мой личный прогноз", "🔢 Нумерология и сила имени"],
    ["🧠 Поговорить с астрологом или психологом"],
    ["🪐 Кармическая карта и задачи души"],
    ["❤️ Совместимость и кармическая связь"],
    ["💌 Поделиться добром с другом"],
    ["📚 Что это за место и как оно работает?"]
]
markup = ReplyKeyboardMarkup(main_menu_keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✨ Привет! Добро пожаловать в «Ты не один» — пространство, где тебя слышат.

"
        "Чтобы мы могли точно понять твою ситуацию и помочь, пожалуйста, отправь:

"
        "🔹 Имя
"
        "🔹 Дату рождения (дд.мм.гггг)
"
        "🔹 Время рождения (если знаешь)
"
        "🔹 Город рождения

"
        "📌 Пример: Анна, 25.10.1993, 14:20, Казань

"
        "⚠️ Вводи всё в одном сообщении. Это важно, чтобы мы могли синхронизироваться с твоей картой судьбы.

"
        "🔐 Все данные остаются строго конфиденциальными и не передаются третьим лицам.",
    )
    return GET_BIRTHDATA

async def collect_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    user_id = update.effective_user.id
    user_data[user_id] = user_input

    await update.message.reply_text(
        f"✅ Спасибо! Мы сохранили твои данные:

{user_input}

"
        "Нажми на нужный пункт меню ниже 👇",
        reply_markup=markup
    )
    return ConversationHandler.END

async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    if "подарок" in message:
        await update.message.reply_text("🎁 Сегодня ты не один. Всё имеет значение 🌟")
    elif "прогноз" in message:
        await update.message.reply_text("🔮 На какой период ты хочешь прогноз? Сегодня, неделя, месяц?")
    elif "астролог" in message:
        await update.message.reply_text("🧠 Напиши /consult для консультации.")
    elif "нумерология" in message:
        await update.message.reply_text("🔢 Напиши /number и мы всё рассчитаем.")
    elif "кармическая" in message:
        await update.message.reply_text("🪐 Напиши /karma для анализа задач души.")
    elif "совместимость" in message:
        await update.message.reply_text("❤️ Напиши /match для анализа совместимости.")
    elif "поделиться" in message:
        await update.message.reply_text("💌 Напиши /share чтобы отправить добро другу.")
    elif "что это" in message:
        await update.message.reply_text("📚 Это бот-помощник, который работает с астрологией, психологией и энергией.")
    else:
        await update.message.reply_text("❓ Не понял. Нажми нужный пункт меню.")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={GET_BIRTHDATA: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect_data)]},
        fallbacks=[]
    )

    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))

    print("🤖 Бот запущен.")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())