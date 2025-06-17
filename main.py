from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes
import os

# Настройки (можно будет сохранить в базу)
settings = {
    "autobuy": False,
    "price_min": 0,
    "price_max": 999,
    "supply_limit": 100,
    "buy_cycles": 1
}

# Меню
def get_main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"🔁 Автопокупка: {'ВКЛ' if settings['autobuy'] else 'ВЫКЛ'}", callback_data='toggle_autobuy')],
        [InlineKeyboardButton(f"💰 Лимит цены: {settings['price_min']} - {settings['price_max']}", callback_data='set_price')],
        [InlineKeyboardButton(f"📦 Лимит supply: {settings['supply_limit']}", callback_data='set_supply')],
        [InlineKeyboardButton(f"🔂 Циклы покупки: {settings['buy_cycles']}", callback_data='set_cycles')],
        [InlineKeyboardButton("🔄 Обновить", callback_data='refresh')]
    ])

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Вот твои настройки автопокупки:", reply_markup=get_main_menu())

# Обработка кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "toggle_autobuy":
        settings["autobuy"] = not settings["autobuy"]
    elif query.data == "refresh":
        pass  # просто обновить
    elif query.data == "set_price":
        await query.edit_message_text("💡 Напиши лимиты цены через пробел, например: `10 100`")
        context.user_data["awaiting"] = "price"
        return
    elif query.data == "set_supply":
        await query.edit_message_text("💡 Напиши лимит supply, например: `50`")
        context.user_data["awaiting"] = "supply"
        return
    elif query.data == "set_cycles":
        await query.edit_message_text("💡 Напиши количество циклов покупки, например: `2`")
        context.user_data["awaiting"] = "cycles"
        return

    await query.edit_message_text("✅ Настройки обновлены:", reply_markup=get_main_menu())

# Обработка текстов от пользователя (ввод лимитов)
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "awaiting" not in context.user_data:
        return

    mode = context.user_data["awaiting"]
    text = update.message.text.strip()

    try:
        if mode == "price":
            parts = list(map(int, text.split()))
            settings["price_min"], settings["price_max"] = parts[0], parts[1]
        elif mode == "supply":
            settings["supply_limit"] = int(text)
        elif mode == "cycles":
            settings["buy_cycles"] = int(text)
        context.user_data.pop("awaiting")
        await update.message.reply_text("✅ Успешно сохранено!", reply_markup=get_main_menu())
    except:
        await update.message.reply_text("❌ Неверный формат. Попробуй ещё раз.")

# Запуск бота
if __name__ == '__main__':
    import asyncio
    from telegram.ext import MessageHandler, filters

    token = os.getenv("BOT_TOKEN")

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), text_handler))

    print("🤖 Бот запущен...")
    app.run_polling()
